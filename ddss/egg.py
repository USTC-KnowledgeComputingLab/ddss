import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from apyds import Rule
from .orm import insert_or_ignore, Facts, Ideas
from .egraph import Search


async def main(session: async_sessionmaker[AsyncSession]) -> None:
    try:
        search = Search()
        pool = []
        max_fact = -1
        max_idea = -1

        while True:
            async with session() as sess:
                for idea in await sess.scalars(select(Ideas).where(Ideas.id > max_idea)):
                    max_idea = max(max_idea, idea.id)
                    pool.append(Rule(idea.data))
                for fact in await sess.scalars(select(Facts).where(Facts.id > max_fact)):
                    max_fact = max(max_fact, fact.id)
                    search.add(Rule(fact.data))
                search.rebuild()
                tasks = []
                next_pool = []
                for i in pool:
                    for o in search.execute(i):
                        tasks.append(asyncio.create_task(insert_or_ignore(sess, Facts, str(o))))
                        if i == o:
                            break
                    else:
                        next_pool.append(i)
                pool = next_pool
                await asyncio.gather(*tasks)
                await sess.commit()

            await asyncio.sleep(0)
    except asyncio.CancelledError:
        pass
