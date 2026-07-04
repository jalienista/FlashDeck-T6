"""Modelo semântico válido usado pelos geradores de código."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Card:
    identifier: str
    front: str
    back: str
    tags: tuple[str, ...]
    category: str
    difficulty: int


@dataclass(frozen=True)
class Deck:
    name: str
    description: str
    declared_tags: tuple[str, ...]
    declared_categories: tuple[str, ...]
    cards: tuple[Card, ...]


@dataclass(frozen=True)
class Program:
    decks: tuple[Deck, ...] = field(default_factory=tuple)
