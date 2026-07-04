from __future__ import annotations

import csv
import json

from flashdeck.compiler import FlashDeckCompiler


def test_generates_html_csv_and_json(valid_source, tmp_path):
    result = FlashDeckCompiler().compile_source(
        source=valid_source,
        output_dir=tmp_path,
        formats=("html", "csv", "json"),
    )

    assert result.succeeded
    assert len(result.artifacts) == 3

    paths = {artifact.format_name: artifact.path for artifact in result.artifacts}
    assert all(path.exists() for path in paths.values())

    html = paths["html"].read_text(encoding="utf-8")
    assert "@@DECK_JSON@@" not in html
    assert "Deck de Teste" in html
    assert "Pergunta um" in html
    assert "Revelar resposta" in html

    with paths["csv"].open(encoding="utf-8-sig", newline="") as file:
        rows = list(csv.reader(file))
    assert rows[0] == ["Front", "Back", "Tags"]
    assert rows[1][0] == "Pergunta um"
    assert "category::teoria" in rows[1][2]

    payload = json.loads(paths["json"].read_text(encoding="utf-8"))
    assert payload["deck"] == "Deck de Teste"
    assert len(payload["cards"]) == 2


def test_check_only_does_not_generate_files(valid_source, tmp_path):
    result = FlashDeckCompiler().compile_source(
        source=valid_source,
        output_dir=tmp_path,
        check_only=True,
    )

    assert result.succeeded
    assert result.artifacts == ()
    assert list(tmp_path.iterdir()) == []


def test_invalid_program_does_not_generate_files(valid_source, tmp_path):
    invalid = valid_source.replace("difficulty: 1;", "difficulty: 10;", 1)
    result = FlashDeckCompiler().compile_source(
        source=invalid,
        output_dir=tmp_path,
    )

    assert not result.succeeded
    assert result.artifacts == ()
    assert list(tmp_path.iterdir()) == []
