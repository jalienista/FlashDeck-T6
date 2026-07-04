"""Geração de uma aplicação HTML autocontida para estudar os cards."""

from __future__ import annotations

import html
import json
from importlib.resources import files
from pathlib import Path

from flashdeck.model import Deck
from flashdeck.utils import slugify


class HtmlGenerator:
    format_name = "html"

    def generate(self, deck: Deck, output_dir: Path) -> Path:
        output_dir.mkdir(parents=True, exist_ok=True)
        template = (
            files("flashdeck")
            .joinpath("templates/deck.html")
            .read_text(encoding="utf-8")
        )

        payload = {
            "name": deck.name,
            "description": deck.description,
            "tags": list(deck.declared_tags),
            "categories": list(deck.declared_categories),
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
        deck_json = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")

        rendered = (
            template.replace("@@TITLE@@", html.escape(deck.name))
            .replace("@@DESCRIPTION@@", html.escape(deck.description))
            .replace("@@DECK_JSON@@", deck_json)
        )

        path = output_dir / f"{slugify(deck.name)}.html"
        path.write_text(rendered, encoding="utf-8")
        return path
