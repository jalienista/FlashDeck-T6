"""Funções auxiliares compartilhadas pelo compilador."""

from __future__ import annotations

import re
import unicodedata


def slugify(value: str) -> str:
    """Transforma um nome livre em um nome de arquivo portável."""

    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_value).strip("-").lower()
    return slug or "deck"
