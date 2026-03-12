import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from apyds_bnf import unparse
from .orm import Facts, Ideas


async def main(session: async_sessionmaker[AsyncSession]) -> None:
    try:
        async with session() as sess:
            for i in await sess.scalars(select(Ideas)):
                print("idea:", unparse(i.data))
            for f in await sess.scalars(select(Facts)):
                print("fact:", unparse(f.data))
    except asyncio.CancelledError:
        pass
