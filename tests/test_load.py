import tempfile
import pathlib
from unittest.mock import patch
from io import StringIO
import pytest
import pytest_asyncio
from sqlalchemy import select
from ddss.orm import initialize_database, Facts, Ideas
from ddss.load import main


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
async def test_load_valid_fact(temp_db):
    """Test that valid input is parsed and stored as a Fact in the database."""
    addr, engine, session = temp_db

    # Mock stdin with valid input
    mock_stdin = StringIO("a => b\n")

    with patch("sys.stdin", mock_stdin):
        await main(addr, engine, session)

    # Verify data was stored
    async with session() as sess:
        facts = await sess.scalars(select(Facts))
        facts_list = list(facts)
        assert len(facts_list) == 1
        assert facts_list[0].data == "a\n----\nb\n"


@pytest.mark.asyncio
async def test_load_generates_idea(temp_db):
    """Test that input that parses to non-dashed form generates an Idea."""
    addr, engine, session = temp_db

    # Mock stdin with valid input
    mock_stdin = StringIO("a => b\n")

    with patch("sys.stdin", mock_stdin):
        await main(addr, engine, session)

    # Verify both Fact and Idea were stored
    async with session() as sess:
        facts = await sess.scalars(select(Facts))
        facts_list = list(facts)
        assert len(facts_list) == 1
        assert facts_list[0].data == "a\n----\nb\n"

        ideas = await sess.scalars(select(Ideas))
        ideas_list = list(ideas)
        assert len(ideas_list) == 1
        assert ideas_list[0].data == "----\na\n"


@pytest.mark.asyncio
async def test_load_invalid_input_handling(temp_db, capsys):
    """Test that invalid/malformed input is handled gracefully with error message."""
    addr, engine, session = temp_db

    # Mock stdin with invalid input
    mock_stdin = StringIO("=>\n")

    with patch("sys.stdin", mock_stdin):
        await main(addr, engine, session)

    # Check that error was printed to stderr
    captured = capsys.readouterr()
    assert "error:" in captured.err

    # Verify no data was stored
    async with session() as sess:
        facts = await sess.scalars(select(Facts))
        facts_list = list(facts)
        assert len(facts_list) == 0


@pytest.mark.asyncio
async def test_load_empty_input_skipped(temp_db):
    """Test that empty lines are skipped."""
    addr, engine, session = temp_db

    # Mock stdin with empty lines and valid input
    mock_stdin = StringIO("\n  \na => b\n")

    with patch("sys.stdin", mock_stdin):
        await main(addr, engine, session)

    # Verify only the valid input was stored
    async with session() as sess:
        facts = await sess.scalars(select(Facts))
        facts_list = list(facts)
        assert len(facts_list) == 1
        assert facts_list[0].data == "a\n----\nb\n"


@pytest.mark.asyncio
async def test_load_multiple_entries(temp_db):
    """Test that multiple valid inputs are stored correctly."""
    addr, engine, session = temp_db

    # Mock stdin with multiple valid inputs
    mock_stdin = StringIO("a => b\nc => d\nsimple\n")

    with patch("sys.stdin", mock_stdin):
        await main(addr, engine, session)

    # Verify all data was stored
    async with session() as sess:
        facts = await sess.scalars(select(Facts))
        facts_list = list(facts)
        # Should have 3 facts
        assert len(facts_list) == 3
        fact_data = [f.data for f in facts_list]
        assert "a\n----\nb\n" in fact_data
        assert "c\n----\nd\n" in fact_data
        assert "----\nsimple\n" in fact_data

        # Should have 2 ideas (from "a => b" and "c => d")
        ideas = await sess.scalars(select(Ideas))
        ideas_list = list(ideas)
        assert len(ideas_list) == 2
        idea_data = [i.data for i in ideas_list]
        assert "----\na\n" in idea_data
        assert "----\nc\n" in idea_data


@pytest.mark.asyncio
async def test_load_mixed_valid_and_invalid(temp_db, capsys):
    """Test that valid inputs are stored even when mixed with invalid ones."""
    addr, engine, session = temp_db

    # Mock stdin with mixed valid and invalid inputs
    mock_stdin = StringIO("a => b\n=>\nc => d\n")

    with patch("sys.stdin", mock_stdin):
        await main(addr, engine, session)

    # Check that error was printed for invalid input
    captured = capsys.readouterr()
    assert "error:" in captured.err

    # Verify valid data was stored
    async with session() as sess:
        facts = await sess.scalars(select(Facts))
        facts_list = list(facts)
        assert len(facts_list) == 2
        fact_data = [f.data for f in facts_list]
        assert "a\n----\nb\n" in fact_data
        assert "c\n----\nd\n" in fact_data


@pytest.mark.asyncio
async def test_load_empty_stdin(temp_db):
    """Test that loading from empty stdin completes without errors."""
    addr, engine, session = temp_db

    # Mock empty stdin
    mock_stdin = StringIO("")

    with patch("sys.stdin", mock_stdin):
        await main(addr, engine, session)

    # Verify no data was stored
    async with session() as sess:
        facts = await sess.scalars(select(Facts))
        facts_list = list(facts)
        assert len(facts_list) == 0


@pytest.mark.asyncio
async def test_load_duplicate_entries(temp_db):
    """Test that duplicate entries are ignored due to unique constraint."""
    addr, engine, session = temp_db

    # Pre-populate with one entry
    async with session() as sess:
        sess.add(Facts(data="a\n----\nb\n"))
        await sess.commit()

    # Try to load the same entry again
    mock_stdin = StringIO("a => b\n")

    with patch("sys.stdin", mock_stdin):
        await main(addr, engine, session)

    # Verify only one entry exists (duplicate was ignored)
    async with session() as sess:
        facts = await sess.scalars(select(Facts))
        facts_list = list(facts)
        assert len(facts_list) == 1
