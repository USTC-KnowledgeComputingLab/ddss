import sys
import asyncio
import tempfile
import pathlib
from apyds_bnf import parse
from ddss.orm import initialize_database, insert_or_ignore, Facts, Ideas
from ddss.ds import main as ds
from ddss.egg import main as egg
from ddss.output import main as output
from ddss.utility import str_rule_get_str_idea


async def load(addr, engine, session, file_name):
    async with session() as sess:
        for line in open(file_name, "rt", encoding="utf-8"):
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


async def run(addr: str, file_name: str) -> None:
    engine, session = await initialize_database(addr)

    try:
        await load(addr, engine, session, file_name)

        await asyncio.wait(
            [
                asyncio.create_task(ds(addr, engine, session)),
                asyncio.create_task(egg(addr, engine, session)),
                asyncio.create_task(output(addr, engine, session)),
            ],
            return_when=asyncio.FIRST_COMPLETED,
        )
    except asyncio.CancelledError:
        pass
    finally:
        await engine.dispose()


def main() -> None:
    tmpdir = tempfile.TemporaryDirectory(prefix="ddss-")
    path = pathlib.Path(tmpdir.name) / "ddss.db"
    addr = f"sqlite+aiosqlite:///{path.as_posix()}"
    file_name = sys.argv[1]
    asyncio.run(run(addr, file_name))


if __name__ == "__main__":
    main()
