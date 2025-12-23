import tempfile
import pathlib
import pytest
import pytest_asyncio
from ddss.orm import initialize_database, Facts, Ideas
from ddss.dump import main


@pytest_asyncio.fixture
async def temp_db():
    """Fixture to create a temporary database."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = pathlib.Path(tmpdir) / "test.db"
        addr = f"sqlite+aiosqlite:///{db_path.as_posix()}"
        engine, session = await initialize_database(addr)
        yield addr, engine, session
        await engine.dispose()


@pytest.mark.asyncio
async def test_dump_facts_correctly(temp_db, capsys):
    """Test that Facts data is dumped correctly using unparse()."""
    addr, engine, session = temp_db

    # Add test data
    async with session() as sess:
        sess.add(Facts(data="a\n----\nb\n"))
        await sess.commit()

    # Run the dump function
    await main(addr, engine, session)

    # Check output
    captured = capsys.readouterr()
    assert "fact: a => b" in captured.out


@pytest.mark.asyncio
async def test_dump_ideas_correctly(temp_db, capsys):
    """Test that Ideas data is dumped correctly using unparse()."""
    addr, engine, session = temp_db

    # Add test data
    async with session() as sess:
        sess.add(Ideas(data="x\n----\ny\n"))
        await sess.commit()

    # Run the dump function
    await main(addr, engine, session)

    # Check output
    captured = capsys.readouterr()
    assert "idea: x => y" in captured.out


@pytest.mark.asyncio
async def test_dump_multiple_entries(temp_db, capsys):
    """Test that dump handles multiple Facts and Ideas correctly."""
    addr, engine, session = temp_db

    # Add test data
    async with session() as sess:
        sess.add(Facts(data="a\n----\nb\n"))
        sess.add(Facts(data="c\n----\nd\n"))
        sess.add(Ideas(data="x\n----\ny\n"))
        sess.add(Ideas(data="p\n----\nq\n"))
        await sess.commit()

    # Run the dump function
    await main(addr, engine, session)

    # Check output
    captured = capsys.readouterr()
    assert "idea: x => y" in captured.out
    assert "idea: p => q" in captured.out
    assert "fact: a => b" in captured.out
    assert "fact: c => d" in captured.out


@pytest.mark.asyncio
async def test_dump_empty_database(temp_db, capsys):
    """Test that dump handles an empty database correctly."""
    addr, engine, session = temp_db

    # Run the dump function with no data
    await main(addr, engine, session)

    # Check output - should be empty or just whitespace
    captured = capsys.readouterr()
    assert captured.out.strip() == ""


@pytest.mark.asyncio
async def test_dump_order(temp_db, capsys):
    """Test that ideas are dumped before facts."""
    addr, engine, session = temp_db

    # Add test data
    async with session() as sess:
        sess.add(Facts(data="a\n----\nb\n"))
        sess.add(Ideas(data="x\n----\ny\n"))
        await sess.commit()

    # Run the dump function
    await main(addr, engine, session)

    # Check output order - ideas should come before facts
    captured = capsys.readouterr()
    idea_pos = captured.out.find("idea: x => y")
    fact_pos = captured.out.find("fact: a => b")
    assert idea_pos < fact_pos, "Ideas should be printed before facts"


@pytest.mark.asyncio
async def test_dump_with_simple_fact(temp_db, capsys):
    """Test dumping a fact that starts with dashes."""
    addr, engine, session = temp_db

    # Add test data - a fact that starts with "--"
    async with session() as sess:
        sess.add(Facts(data="----\nsimple\n"))
        await sess.commit()

    # Run the dump function
    await main(addr, engine, session)

    # Check output - unparse converts "----\nsimple\n" to " => simple"
    captured = capsys.readouterr()
    assert "fact:  => simple" in captured.out
