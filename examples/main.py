import sys
import asyncio
import tempfile
import pathlib
from sqlalchemy import select
from apyds import Rule, List, Variable, Term, Item
from apyds_bnf import parse, unparse
from ddss.orm import initialize_database, insert_or_ignore, Facts, Ideas
from ddss.ds import main as ds
from ddss.egg import main as egg
from ddss.utility import str_rule_get_str_idea


def extract_binary_from_term(term: Term) -> tuple[Item, Term, Term] | None:
    t = term.term
    if isinstance(t, List) and len(t) == 4 and str(t[0]) == "binary":
        if isinstance(t[1].term, Item):
            return t[1].term, t[2], t[3]
    return None


def extract_equality_from_rule(rule: Rule) -> tuple[Term, Term] | None:
    if len(rule) != 0:
        return None
    res = extract_binary_from_term(rule.conclusion)
    if res and str(res[0]) == "==":
        return res[1], res[2]
    return None


def extract_literal_from_term(term: Term) -> tuple[Item | Variable, Item] | None:
    res = extract_binary_from_term(term)
    if res and str(res[0]) == "::":
        lhs, rhs = res[1].term, res[2].term
        if isinstance(lhs, List) and isinstance(rhs, Item):
            if len(lhs) == 3 and str(lhs[0]) == "function" and str(lhs[1]) == "Literal":
                if isinstance(lhs[2].term, Item | Variable):
                    return lhs[2].term, rhs
    return None


async def arithmetic(session):
    try:
        max_idea = -1

        while True:
            count = 0
            begin = asyncio.get_running_loop().time()

            async with session() as sess:
                pool: list[Rule] = []
                for i in await sess.scalars(select(Ideas).where(Ideas.id > max_idea)):
                    max_idea = max(max_idea, i.id)
                    pool.append(Rule(i.data))

                for rule in pool:
                    if eq := extract_equality_from_rule(rule):
                        lhs_term, rhs_term = eq

                        # Case: (a + b) == res
                        if bin_lhs := extract_binary_from_term(lhs_term):
                            if str(bin_lhs[0]) == "+":
                                v1_lit = extract_literal_from_term(bin_lhs[1])
                                v2_lit = extract_literal_from_term(bin_lhs[2])
                                v_res_lit = extract_literal_from_term(rhs_term)
                                if v1_lit and v2_lit and v_res_lit:
                                    try:
                                        a, b = int(str(v1_lit[0])), int(str(v2_lit[0]))
                                    except TypeError:
                                        continue
                                    if isinstance(v_res_lit[0], Variable):
                                        res = a + b
                                        fact = f"(binary == (binary + (binary :: (function Literal {a}) Int) (binary :: (function Literal {b}) Int)) (binary :: (function Literal {res}) Int))"
                                        await insert_or_ignore(sess, Facts, str(Rule(fact)))

                        # Case: res == (a + b)
                        if bin_rhs := extract_binary_from_term(rhs_term):
                            if str(bin_rhs[0]) == "+":
                                v1_lit = extract_literal_from_term(bin_rhs[1])
                                v2_lit = extract_literal_from_term(bin_rhs[2])
                                v_res_lit = extract_literal_from_term(lhs_term)
                                if v1_lit and v2_lit and v_res_lit:
                                    try:
                                        a, b = int(str(v1_lit[0])), int(str(v2_lit[0]))
                                    except TypeError:
                                        continue
                                    if isinstance(v_res_lit[0], Variable):
                                        res = a + b
                                        fact = f"(binary == (binary :: (function Literal {res}) Int) (binary + (binary :: (function Literal {a}) Int) (binary :: (function Literal {b}) Int)))"
                                        await insert_or_ignore(sess, Facts, str(Rule(fact)))

                await sess.commit()

            end = asyncio.get_running_loop().time()
            duration = end - begin
            if count == 0:
                delay = max(0, 0.1 - duration)
                await asyncio.sleep(delay)
    except asyncio.CancelledError:
        pass


async def output(session):
    try:
        max_fact = -1
        max_idea = -1

        while True:
            count = 0
            begin = asyncio.get_running_loop().time()

            async with session() as sess:
                for i in await sess.scalars(select(Ideas).where(Ideas.id > max_idea)):
                    max_idea = max(max_idea, i.id)
                    print("idea:", unparse(i.data))
                    count += 1
                for i in await sess.scalars(select(Facts).where(Facts.id > max_fact)):
                    max_fact = max(max_fact, i.id)
                    print("fact:", unparse(i.data))
                    count += 1

                    rule = Rule(i.data)
                    if len(rule) == 0:
                        term = rule.conclusion.term
                        if isinstance(term, List):
                            if len(term) >= 2 and str(term[0]) == "function" and str(term[1]) == "Query":
                                print("status:", unparse(i.data))
                                raise asyncio.CancelledError()
                await sess.commit()

            end = asyncio.get_running_loop().time()
            duration = end - begin
            if count == 0:
                delay = max(0, 0.1 - duration)
                await asyncio.sleep(delay)
    except asyncio.CancelledError:
        pass


async def load(session, file_name):
    async with session() as sess:
        for line in open(file_name, "rt", encoding="utf-8"):
            data = line.strip()
            if data == "":
                continue
            if data.startswith("//"):
                continue

            try:
                ds = parse(data)
            except Exception as e:
                print(f"error: {e}")
                continue

            await insert_or_ignore(sess, Facts, ds)
            if idea := str_rule_get_str_idea(ds):
                await insert_or_ignore(sess, Ideas, idea)
        await sess.commit()


async def run(addr: str, file_name: str) -> None:
    engine, session = await initialize_database(addr)

    try:
        await load(session, file_name)
        tasks = [
            asyncio.create_task(ds(session)),
            asyncio.create_task(egg(session)),
            asyncio.create_task(output(session)),
            asyncio.create_task(arithmetic(session)),
        ]
        done, pending = await asyncio.wait(
            tasks,
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()
        for task in pending:
            try:
                await task
            except asyncio.CancelledError:
                pass
    except asyncio.CancelledError:
        pass
    finally:
        await engine.dispose()


def main() -> None:
    tmpdir = tempfile.TemporaryDirectory(prefix="ddss-")
    path = pathlib.Path(tmpdir.name) / "ddss.db"
    addr = f"sqlite+aiosqlite:///{path.as_posix()}"
    file_name = sys.argv[1]
    asyncio.run(run(addr, file_name))


if __name__ == "__main__":
    main()
