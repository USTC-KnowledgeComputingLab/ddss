import sys
import time
from loguru import logger
from sqlalchemy import create_engine, Integer, Text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
import egglog
from apyds import Rule
from apyds_bnf import parse, unparse


class EGraphTerm(egglog.Expr):
    def __init__(self, name: egglog.StringLike) -> None: ...


class Search:
    def __init__(self):
        self.egraph = egglog.EGraph()
        self.terms = set()

    def _is_equality(self, data):
        return data.startswith("----\n(binary == ")

    def _extract_lhs_rhs(self, data):
        term = Rule(data).conclusion
        lhs = str(term.term[2])
        rhs = str(term.term[3])
        return lhs, rhs

    def _ast(self, data):
        # TODO: 现在只支持原子
        return EGraphTerm(data)

    def _set_equality(self, lhs, rhs):
        self.egraph.register(egglog.union(self._ast(lhs)).with_(self._ast(rhs)))

    def _get_equality(self, lhs, rhs):
        return self.egraph.check_bool(self._ast(lhs) == self._ast(rhs))

    def _search_equality(self, data):
        for result in self.terms:
            if self._get_equality(data, result):
                yield result

    def _build_equality(self, lhs, rhs):
        return f"----\n(binary == {lhs} {rhs})"

    def add(self, data):
        data = parse(data)
        if not self._is_equality(data):
            return
        lhs, rhs = self._extract_lhs_rhs(data)
        self.terms.add(lhs)
        self.terms.add(rhs)
        self._set_equality(lhs, rhs)

    def execute(self, data):
        data = parse(data)
        if not self._is_equality(data):
            return
        lhs, rhs = self._extract_lhs_rhs(data)
        if self._get_equality(lhs, rhs):
            result = self._build_equality(lhs, rhs)
            yield unparse(result)
            return
        if lhs.startswith("`"):
            for result in self._search_equality(rhs):
                result = self._build_equality(result, rhs)
                yield unparse(result)
        if rhs.startswith("`"):
            for result in self._search_equality(lhs):
                result = self._build_equality(lhs, result)
                yield unparse(result)


class Base(DeclarativeBase):
    pass


class Facts(Base):
    __tablename__ = "facts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    data: Mapped[str] = mapped_column(Text, unique=True, nullable=False)


class Ideas(Base):
    __tablename__ = "ideas"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    data: Mapped[str] = mapped_column(Text, unique=True, nullable=False)


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <database-addr>")
        sys.exit(1)
    addr = sys.argv[1]

    logger.remove()
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <5}</level> | <cyan>{message}</cyan>",
    )

    engine = create_engine(addr)
    session = sessionmaker(engine)
    logger.info("Engine initialized")

    Base.metadata.create_all(engine)
    logger.info("Database schema ensured")

    search = Search()
    max_fact = -1
    max_idea = -1
    logger.info("Search initialized")

    while True:
        count = 0
        begin = time.time()
        with session() as sess:
            query = sess.query(Facts).filter(Facts.id > max_fact)
            for i in query:
                max_fact = max(max_fact, i.id)
                search.add(i.data)
                logger.debug("input: {data}", data=i.data)

            query = sess.query(Ideas).filter(Ideas.id > max_idea)
            for i in query:
                max_idea = max(max_idea, i.id)
                logger.debug("idea input: {data}", data=i.data)
                for o in search.execute(i.data):
                    try:
                        with sess.begin_nested():
                            sess.add(Facts(data=o))
                        count += 1
                        logger.debug("output: {fact}", fact=o)
                    except IntegrityError:
                        logger.debug("repeated output: {fact}", fact=o)

            sess.commit()

        end = time.time()
        duration = end - begin
        logger.info("duration: {duration:0.3f}s", duration=duration)
        if count == 0:
            delay = max(0, 1 - duration)
            logger.info("sleeping: {delay:0.3f}s", delay=delay)
            time.sleep(delay)

    engine.dispose()


if __name__ == "__main__":
    main()
