"""Geração opcional de JSON para depuração e integração com outras aplicações."""

from __future__ import annotations

import json
from pathlib import Path

from flashdeck.model import Deck
from flashdeck.utils import slugify


class JsonGenerator:
    format_name = "json"

    def generate(self, deck: Deck, output_dir: Path) -> Path:
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / f"{slugify(deck.name)}.json"
        payload = {
            "deck": deck.name,
            "description": deck.description,
            "declaredTags": list(deck.declared_tags),
            "declaredCategories": list(deck.declared_categories),
            "cards": [
                {
                    "id": card.identifier,
                    "front": card.front,
                    "back": card.back,
                    "tags": list(card.tags),
                    "category": card.category,
                    "difficulty": card.difficulty,
                }
                for card in deck.cards
            ],
        }
        path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return path
