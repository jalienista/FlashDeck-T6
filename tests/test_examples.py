from __future__ import annotations

from pathlib import Path

import pytest

from flashdeck.compiler import FlashDeckCompiler


ROOT = Path(__file__).resolve().parents[1]
VALID_EXAMPLES = sorted((ROOT / "examples" / "valid").glob("*.fdeck"))
INVALID_EXAMPLES = sorted((ROOT / "examples" / "invalid").glob("*.fdeck"))


@pytest.mark.parametrize("source_path", VALID_EXAMPLES, ids=lambda path: path.name)
def test_all_valid_examples_compile(source_path, tmp_path):
    result = FlashDeckCompiler().compile_file(
        input_path=source_path,
        output_dir=tmp_path,
        formats=("html", "csv"),
    )

    assert result.succeeded, [diagnostic.message for diagnostic in result.errors]
    assert result.artifacts


@pytest.mark.parametrize("source_path", INVALID_EXAMPLES, ids=lambda path: path.name)
def test_all_invalid_examples_fail(source_path, tmp_path):
    result = FlashDeckCompiler().compile_file(
        input_path=source_path,
        output_dir=tmp_path,
        formats=("html", "csv"),
    )

    assert not result.succeeded
    assert result.errors
    assert result.artifacts == ()
