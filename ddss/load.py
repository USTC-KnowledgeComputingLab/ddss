import asyncio
import sys
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from apyds_bnf import parse
from .orm import insert_or_ignore, Facts, Ideas
from .utility import str_rule_get_str_idea


async def main(session: async_sessionmaker[AsyncSession]) -> None:
    try:
        async with session() as sess:
            for line in sys.stdin:
                data = line.strip()
                if data == "" or data.startswith("//"):
                    continue

                try:
                    ds = parse(data)
                except Exception as e:
                    print(f"error: {e}")
                    continue

                await insert_or_ignore(sess, Facts, ds)
                if idea := str_rule_get_str_idea(ds):
                    await insert_or_ignore(sess, Ideas, idea)
            await sess.commit()
    except asyncio.CancelledError:
        pass
