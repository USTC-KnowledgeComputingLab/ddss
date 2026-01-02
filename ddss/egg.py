import asyncio
from sqlalchemy import select
from apyds import Rule
from .orm import insert_or_ignore, Facts, Ideas
from .egraph import Search


async def main(session):
    try:
        search = Search()
        pool = []
        max_fact = -1
        max_idea = -1

        while True:
            async with session() as sess:
                for i in await sess.scalars(select(Ideas).where(Ideas.id > max_idea)):
                    max_idea = max(max_idea, i.id)
                    pool.append(Rule(i.data))
                for i in await sess.scalars(select(Facts).where(Facts.id > max_fact)):
                    max_fact = max(max_fact, i.id)
                    search.add(Rule(i.data))
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
