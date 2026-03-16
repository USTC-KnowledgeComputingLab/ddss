import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from apyds_bnf import unparse
from .orm import Facts, Ideas


async def main(session: async_sessionmaker[AsyncSession]) -> None:
    try:
        max_fact = -1
        max_idea = -1

        while True:
            async with session() as sess:
                for idea in await sess.scalars(select(Ideas).where(Ideas.id > max_idea)):
                    max_idea = max(max_idea, idea.id)
                    print("idea:", unparse(idea.data))
                for fact in await sess.scalars(select(Facts).where(Facts.id > max_fact)):
                    max_fact = max(max_fact, fact.id)
                    print("fact:", unparse(fact.data))
                await sess.commit()

            await asyncio.sleep(0)
    except asyncio.CancelledError:
        pass
