import asyncio
import sys
from apyds_bnf import parse
from .orm import insert_or_ignore, Facts, Ideas
from .utility import str_rule_get_str_idea


async def main(session):
    try:
        async with session() as sess:
            for line in sys.stdin:
                data = line.strip()
                if data == "":
                    continue
                if data.startswith("//"):
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
