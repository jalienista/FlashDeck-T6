from flashdeck.parser import FlashDeckParser


def test_parser_accepts_valid_program(valid_source):
    outcome = FlashDeckParser().parse(valid_source)

    assert outcome.succeeded
    assert outcome.program is not None
    assert len(outcome.program.decks) == 1
    assert outcome.program.decks[0].name == "Deck de Teste"
    assert len(outcome.program.decks[0].cards) == 2


def test_lexical_error_is_reported(valid_source):
    source = valid_source.replace("difficulty: 1;", "difficulty: @;")
    outcome = FlashDeckParser().parse(source)

    assert not outcome.succeeded
    assert outcome.diagnostics[0].code == "LEX001"
    assert outcome.diagnostics[0].line > 0


def test_syntax_error_is_reported(valid_source):
    source = valid_source.replace("tags: [tag_a, tag_b];", "tags: [tag_a, tag_b]")
    outcome = FlashDeckParser().parse(source)

    assert not outcome.succeeded
    assert outcome.diagnostics[0].code.startswith("SYN")
