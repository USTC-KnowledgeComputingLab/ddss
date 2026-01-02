import asyncio
from sqlalchemy import select
from apyds_bnf import unparse
from .orm import Facts, Ideas


async def main(session):
    try:
        max_fact = -1
        max_idea = -1

        while True:
            count = 0
            async with session() as sess:
                for i in await sess.scalars(select(Ideas).where(Ideas.id > max_idea)):
                    max_idea = max(max_idea, i.id)
                    print("idea:", unparse(i.data))
                    count += 1
                for i in await sess.scalars(select(Facts).where(Facts.id > max_fact)):
                    max_fact = max(max_fact, i.id)
                    print("fact:", unparse(i.data))
                    count += 1
                await sess.commit()

            if count == 0:
                await asyncio.sleep(0)
    except asyncio.CancelledError:
        pass
