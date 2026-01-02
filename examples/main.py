import sys
import asyncio
import tempfile
import pathlib
from sqlalchemy import select
from apyds import Rule, List, Variable
from apyds_bnf import parse, unparse
from ddss.orm import initialize_database, insert_or_ignore, Facts, Ideas
from ddss.ds import main as ds
from ddss.egg import main as egg
from ddss.utility import str_rule_get_str_idea


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
                    if len(rule) == 0:
                        term = rule.conclusion.term
                        if isinstance(term, List):
                            if len(term) == 4 and str(term[0]) == "binary" and str(term[1]) == "==":
                                lhs = term[2].term
                                rhs = term[3].term

                                if isinstance(lhs, Variable):
                                    if isinstance(rhs, List):
                                        if len(rhs) == 4 and str(rhs[0]) == "binary" and str(rhs[1]) == "+":
                                            try:
                                                # TODO: stronger typing
                                                a = int(str(rhs[2]))
                                                b = int(str(rhs[3]))
                                            except Exception:
                                                continue
                                            # TODO: other operators
                                            value = a + b
                                            fact = Rule(f"(binary == {value} (binary + {a} {b}))")
                                            await insert_or_ignore(sess, Facts, str(fact))
                                elif isinstance(rhs, Variable):
                                    if isinstance(lhs, List):
                                        if len(lhs) == 4 and str(lhs[0]) == "binary" and str(lhs[1]) == "+":
                                            try:
                                                a = int(str(lhs[2]))
                                                b = int(str(lhs[3]))
                                            except Exception:
                                                continue
                                            value = a + b
                                            fact = Rule(f"(binary == {value} (binary + {a} {b}))")
                                            await insert_or_ignore(sess, Facts, str(fact))

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
