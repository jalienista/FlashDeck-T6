"""Representação e formatação uniforme de erros e avisos."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Severity(str, Enum):
    ERROR = "error"
    WARNING = "warning"


@dataclass(frozen=True)
class Diagnostic:
    code: str
    message: str
    line: int = 1
    column: int = 1
    severity: Severity = Severity.ERROR
    phase: str = "compilação"

    def format(self, filename: str) -> str:
        label = "erro" if self.severity == Severity.ERROR else "aviso"
        return (
            f"{filename}:{self.line}:{self.column}: "
            f"{label} [{self.code}] ({self.phase}) {self.message}"
        )
