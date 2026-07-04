"""Análise léxica/sintática e construção da AST da linguagem FlashDeck."""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib.resources import files

from lark import Lark, Token, Transformer, UnexpectedCharacters, UnexpectedInput, UnexpectedToken, v_args

from flashdeck.ast_nodes import (
    CardFieldNode,
    CardNode,
    DeckFieldNode,
    DeckNode,
    ProgramNode,
    SourceLocation,
)
from flashdeck.diagnostics import Diagnostic


@dataclass(frozen=True)
class ParseOutcome:
    program: ProgramNode | None
    diagnostics: tuple[Diagnostic, ...]

    @property
    def succeeded(self) -> bool:
        return self.program is not None and not self.diagnostics


def _decode_string(token: Token) -> str:
    """Decodifica uma STRING da linguagem, respeitando escapes como \n e \"."""

    return json.loads(str(token))


@v_args(meta=True)
class _AstTransformer(Transformer):
    """Converte a árvore concreta do Lark em uma AST pequena e independente."""

    def start(self, meta, children):  # noqa: ARG002 - meta mantido por uniformidade
        return ProgramNode(decks=list(children))

    def deck_item(self, meta, children):  # noqa: ARG002
        return children[0]

    def card_field(self, meta, children):  # noqa: ARG002
        return children[0]

    def identifier_list(self, meta, children):  # noqa: ARG002
        return [str(item) for item in children]

    def description_decl(self, meta, children):
        return DeckFieldNode(
            kind="description",
            value=_decode_string(children[0]),
            location=SourceLocation(meta.line, meta.column),
        )

    def tags_decl(self, meta, children):
        values = children[0] if children else []
        return DeckFieldNode(
            kind="tags",
            value=values,
            location=SourceLocation(meta.line, meta.column),
        )

    def categories_decl(self, meta, children):
        values = children[0] if children else []
        return DeckFieldNode(
            kind="categories",
            value=values,
            location=SourceLocation(meta.line, meta.column),
        )

    def front_field(self, meta, children):
        return CardFieldNode(
            kind="front",
            value=_decode_string(children[0]),
            location=SourceLocation(meta.line, meta.column),
        )

    def back_field(self, meta, children):
        return CardFieldNode(
            kind="back",
            value=_decode_string(children[0]),
            location=SourceLocation(meta.line, meta.column),
        )

    def card_tags_field(self, meta, children):
        values = children[0] if children else []
        return CardFieldNode(
            kind="tags",
            value=values,
            location=SourceLocation(meta.line, meta.column),
        )

    def category_field(self, meta, children):
        return CardFieldNode(
            kind="category",
            value=str(children[0]),
            location=SourceLocation(meta.line, meta.column),
        )

    def difficulty_field(self, meta, children):
        return CardFieldNode(
            kind="difficulty",
            value=int(str(children[0])),
            location=SourceLocation(meta.line, meta.column),
        )

    def card_decl(self, meta, children):
        identifier = str(children[0])
        fields = [child for child in children[1:] if isinstance(child, CardFieldNode)]
        return CardNode(
            identifier=identifier,
            fields=fields,
            location=SourceLocation(meta.line, meta.column),
        )

    def deck(self, meta, children):
        name = _decode_string(children[0])
        fields = [child for child in children[1:] if isinstance(child, DeckFieldNode)]
        cards = [child for child in children[1:] if isinstance(child, CardNode)]
        return DeckNode(
            name=name,
            fields=fields,
            cards=cards,
            location=SourceLocation(meta.line, meta.column),
        )


class FlashDeckParser:
    """Fachada do parser LALR gerado a partir de ``grammar.lark``."""

    def __init__(self) -> None:
        grammar = files("flashdeck").joinpath("grammar.lark").read_text(encoding="utf-8")
        self._parser = Lark(
            grammar,
            parser="lalr",
            lexer="contextual",
            start="start",
            propagate_positions=True,
            maybe_placeholders=False,
        )

    def parse(self, source: str) -> ParseOutcome:
        try:
            tree = self._parser.parse(source)
            program = _AstTransformer().transform(tree)
            return ParseOutcome(program=program, diagnostics=())
        except UnexpectedCharacters as exc:
            char = repr(exc.char)
            diagnostic = Diagnostic(
                code="LEX001",
                message=f"caractere inesperado {char}.",
                line=exc.line,
                column=exc.column,
                phase="análise léxica",
            )
            return ParseOutcome(program=None, diagnostics=(diagnostic,))
        except UnexpectedToken as exc:
            found = "fim do arquivo" if exc.token.type == "$END" else repr(str(exc.token))
            expected = ", ".join(sorted(exc.expected)) if exc.expected else "outro símbolo"
            diagnostic = Diagnostic(
                code="SYN001",
                message=f"símbolo inesperado {found}; esperado: {expected}.",
                line=exc.line,
                column=exc.column,
                phase="análise sintática",
            )
            return ParseOutcome(program=None, diagnostics=(diagnostic,))
        except UnexpectedInput as exc:
            diagnostic = Diagnostic(
                code="SYN002",
                message="entrada inválida para a gramática FlashDeck.",
                line=getattr(exc, "line", 1),
                column=getattr(exc, "column", 1),
                phase="análise sintática",
            )
            return ParseOutcome(program=None, diagnostics=(diagnostic,))
