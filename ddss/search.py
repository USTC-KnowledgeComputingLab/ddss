import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from apyds import Search
from .orm import insert_or_ignore, Facts, Ideas
from .utility import str_rule_get_str_idea


async def main(session: async_sessionmaker[AsyncSession]) -> None:
    try:
        search = Search()
        max_fact = -1

        while True:
            async with session() as sess:
                for i in await sess.scalars(select(Facts).where(Facts.id > max_fact)):
                    max_fact = max(max_fact, i.id)
                    search.add(i.data)

                for rule in search:
                    ds = str(rule)
                    await insert_or_ignore(sess, Facts, ds)
                    if idea := str_rule_get_str_idea(ds):
                        await insert_or_ignore(sess, Ideas, idea)

                await sess.commit()

            await asyncio.sleep(0)
    except asyncio.CancelledError:
        pass
