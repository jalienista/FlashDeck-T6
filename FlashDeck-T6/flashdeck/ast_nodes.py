"""Nós da árvore sintática abstrata produzida após o parsing."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class SourceLocation:
    """Posição de um elemento no arquivo-fonte."""

    line: int
    column: int


@dataclass(frozen=True)
class DeckFieldNode:
    """Declaração de cabeçalho de um deck."""

    kind: str
    value: Any
    location: SourceLocation


@dataclass(frozen=True)
class CardFieldNode:
    """Campo pertencente a um card."""

    kind: str
    value: Any
    location: SourceLocation


@dataclass
class CardNode:
    """Representação sintática de um card antes da validação semântica."""

    identifier: str
    fields: list[CardFieldNode] = field(default_factory=list)
    location: SourceLocation = field(default_factory=lambda: SourceLocation(1, 1))


@dataclass
class DeckNode:
    """Representação sintática de um deck antes da validação semântica."""

    name: str
    fields: list[DeckFieldNode] = field(default_factory=list)
    cards: list[CardNode] = field(default_factory=list)
    location: SourceLocation = field(default_factory=lambda: SourceLocation(1, 1))


@dataclass
class ProgramNode:
    """Raiz da AST de um arquivo FlashDeck."""

    decks: list[DeckNode] = field(default_factory=list)
