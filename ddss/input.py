import asyncio
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from apyds_bnf import parse
from .orm import insert_or_ignore, Facts, Ideas
from .utility import str_rule_get_str_idea


async def main(session):
    try:
        prompt = PromptSession()
        while True:
            try:
                with patch_stdout():
                    line = await prompt.prompt_async("input: ")
            except (EOFError, KeyboardInterrupt):
                raise asyncio.CancelledError()

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

            async with session() as sess:
                await insert_or_ignore(sess, Facts, ds)
                if idea := str_rule_get_str_idea(ds):
                    await insert_or_ignore(sess, Ideas, idea)
                await sess.commit()
    except asyncio.CancelledError:
        pass
