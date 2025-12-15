import sys
from loguru import logger
from sqlalchemy import create_engine, Integer, Text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from apyds import Rule
from apyds_bnf import parse, unparse


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

    while True:
        data = input()
        with session() as sess:
            o = Rule(parse(data))

            fact = unparse(f"{o}")
            try:
                with sess.begin_nested():
                    sess.add(Facts(data=fact))
                logger.debug("output: {fact}", fact=fact)
            except IntegrityError:
                logger.debug("repeated output: {fact}", fact=fact)
            if len(o) != 0:
                idea = unparse(f"--\n{o[0]}")
                try:
                    with sess.begin_nested():
                        sess.add(Ideas(data=idea))
                    logger.debug("idea output: {idea}", idea=idea)
                except IntegrityError:
                    logger.debug("repeated idea output: {idea}", idea=idea)

            sess.commit()

    engine.dispose()


if __name__ == "__main__":
    main()
