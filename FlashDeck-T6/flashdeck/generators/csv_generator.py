"""Geração de CSV compatível com importação no Anki."""

from __future__ import annotations

import csv
from pathlib import Path

from flashdeck.model import Deck
from flashdeck.utils import slugify


class CsvGenerator:
    format_name = "csv"

    def generate(self, deck: Deck, output_dir: Path) -> Path:
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / f"{slugify(deck.name)}-anki.csv"

        # utf-8-sig inclui BOM, facilitando a abertura no Excel sem quebrar acentos.
        with path.open("w", encoding="utf-8-sig", newline="") as file:
            writer = csv.writer(file, quoting=csv.QUOTE_ALL, lineterminator="\n")
            writer.writerow(["Front", "Back", "Tags"])
            for card in deck.cards:
                anki_tags = [
                    *card.tags,
                    f"category::{card.category}",
                    f"difficulty::{card.difficulty}",
                ]
                writer.writerow([card.front, card.back, " ".join(anki_tags)])

        return path
