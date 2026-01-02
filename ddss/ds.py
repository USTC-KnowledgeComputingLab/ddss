import asyncio
from sqlalchemy import select
from apyds import Search
from .orm import insert_or_ignore, Facts, Ideas
from .utility import str_rule_get_str_idea


async def main(session):
    try:
        search = Search()
        max_fact = -1

        while True:
            async with session() as sess:
                for i in await sess.scalars(select(Facts).where(Facts.id > max_fact)):
                    max_fact = max(max_fact, i.id)
                    search.add(i.data)
                tasks = []

                def handler(rule):
                    ds = str(rule)
                    tasks.append(asyncio.create_task(insert_or_ignore(sess, Facts, ds)))
                    if idea := str_rule_get_str_idea(ds):
                        tasks.append(asyncio.create_task(insert_or_ignore(sess, Ideas, idea)))
                    return False

                count = search.execute(handler)
                await asyncio.gather(*tasks)
                await sess.commit()

            if count == 0:
                await asyncio.sleep(0)
    except asyncio.CancelledError:
        pass
