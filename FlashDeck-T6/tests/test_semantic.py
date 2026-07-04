from __future__ import annotations

import pytest

from flashdeck.parser import FlashDeckParser
from flashdeck.semantic import SemanticAnalyzer


def analyze(source: str):
    parse_outcome = FlashDeckParser().parse(source)
    assert parse_outcome.succeeded
    assert parse_outcome.program is not None
    return SemanticAnalyzer(min_cards=2).analyze(parse_outcome.program)


def error_codes(outcome) -> set[str]:
    return {diagnostic.code for diagnostic in outcome.errors}


def test_valid_semantics(valid_source):
    outcome = analyze(valid_source)

    assert outcome.succeeded
    assert outcome.program is not None
    assert len(outcome.program.decks[0].cards) == 2


def test_duplicate_front_is_rejected(valid_source):
    source = valid_source.replace('front: "Pergunta dois";', 'front: "  PERGUNTA UM  ";')
    outcome = analyze(source)

    assert not outcome.succeeded
    assert "SEM106" in error_codes(outcome)


def test_undeclared_tag_is_rejected(valid_source):
    source = valid_source.replace("tags: [tag_a];", "tags: [nao_declarada];", 1)
    outcome = analyze(source)

    assert not outcome.succeeded
    assert "SEM107" in error_codes(outcome)


@pytest.mark.parametrize("difficulty", [0, 6, -1, 99])
def test_difficulty_outside_1_to_5_is_rejected(valid_source, difficulty):
    source = valid_source.replace("difficulty: 1;", f"difficulty: {difficulty};", 1)
    outcome = analyze(source)

    assert not outcome.succeeded
    assert "SEM109" in error_codes(outcome)


def test_minimum_number_of_cards_is_enforced(valid_source):
    source = valid_source.split("\n    card c2", 1)[0] + "\n}"
    outcome = analyze(source)

    assert not outcome.succeeded
    assert "SEM005" in error_codes(outcome)


def test_undeclared_category_is_rejected(valid_source):
    source = valid_source.replace("category: teoria;", "category: inexistente;", 1)
    outcome = analyze(source)

    assert not outcome.succeeded
    assert "SEM108" in error_codes(outcome)


def test_duplicate_card_identifier_is_rejected(valid_source):
    source = valid_source.replace("card c2", "card c1")
    outcome = analyze(source)

    assert not outcome.succeeded
    assert "SEM101" in error_codes(outcome)


def test_missing_required_card_field_is_rejected(valid_source):
    source = valid_source.replace('back: "Resposta um";\n', "", 1)
    outcome = analyze(source)

    assert not outcome.succeeded
    assert "SEM102" in error_codes(outcome)
