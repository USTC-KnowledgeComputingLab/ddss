import asyncio
from loguru import logger
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select
from sqlalchemy import Integer, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from apyds import Search
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


async def main():
    engine = create_async_engine("sqlite+aiosqlite:///./data.db")
    session = async_sessionmaker(engine)
    logger.info("Engine initialized and session factory created")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database schema ensured")

    search = Search()
    count = -1
    logger.info("Search initialized")

    while True:
        begin = asyncio.get_event_loop().time()
        async with session() as sess:
            query = await sess.execute(select(Facts).where(Facts.id > count))
            input = list(query.scalars())
            logger.info("Loaded {n} new data", n=len(input))
            for i in input:
                count = max(count, i.id)
                search.add(parse(i.data))
                logger.debug("input: {data}", data=i.data)
            output = []
            search.execute(lambda x: output.append(x))
            logger.info("Generated {n} new data", n=len(output))
            for o in output:
                logger.debug("output: {data}", data=unparse(f"{o}"))
            sess.add_all(Facts(data=unparse(f"{o}")) for o in output)
            sess.add_all(Ideas(data=unparse(f"--\n{o[0]}")) for o in output if len(o) != 0)
            await sess.commit()
        end = asyncio.get_event_loop().time()
        duration = end - begin
        delay = max(0, 1 - duration)
        logger.info("Cycle timing: duration={duration} delay={delay}", duration=duration, delay=delay)
        await asyncio.sleep(delay)

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
