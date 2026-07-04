"""Orquestra as fases de compilação: parsing, semântica e geração."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from flashdeck.diagnostics import Diagnostic, Severity
from flashdeck.generators import CsvGenerator, HtmlGenerator, JsonGenerator
from flashdeck.parser import FlashDeckParser
from flashdeck.semantic import SemanticAnalyzer


@dataclass(frozen=True)
class GeneratedArtifact:
    deck_name: str
    format_name: str
    path: Path


@dataclass(frozen=True)
class CompilationResult:
    diagnostics: tuple[Diagnostic, ...]
    artifacts: tuple[GeneratedArtifact, ...]

    @property
    def errors(self) -> tuple[Diagnostic, ...]:
        return tuple(d for d in self.diagnostics if d.severity == Severity.ERROR)

    @property
    def warnings(self) -> tuple[Diagnostic, ...]:
        return tuple(d for d in self.diagnostics if d.severity == Severity.WARNING)

    @property
    def succeeded(self) -> bool:
        return not self.errors


class FlashDeckCompiler:
    """Compilador completo da linguagem FlashDeck."""

    GENERATORS = {
        "html": HtmlGenerator,
        "csv": CsvGenerator,
        "json": JsonGenerator,
    }

    def __init__(self, min_cards: int = 2) -> None:
        self._parser = FlashDeckParser()
        self._semantic = SemanticAnalyzer(min_cards=min_cards)

    def compile_file(
        self,
        input_path: Path,
        output_dir: Path,
        formats: tuple[str, ...] = ("html", "csv"),
        check_only: bool = False,
    ) -> CompilationResult:
        try:
            source = input_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return CompilationResult(
                diagnostics=(
                    Diagnostic(
                        code="IO001",
                        message="o arquivo-fonte deve estar codificado em UTF-8.",
                        phase="leitura do arquivo",
                    ),
                ),
                artifacts=(),
            )
        except OSError as exc:
            return CompilationResult(
                diagnostics=(
                    Diagnostic(
                        code="IO002",
                        message=f"não foi possível ler o arquivo: {exc}.",
                        phase="leitura do arquivo",
                    ),
                ),
                artifacts=(),
            )

        return self.compile_source(
            source=source,
            output_dir=output_dir,
            formats=formats,
            check_only=check_only,
        )

    def compile_source(
        self,
        source: str,
        output_dir: Path,
        formats: tuple[str, ...] = ("html", "csv"),
        check_only: bool = False,
    ) -> CompilationResult:
        parse_outcome = self._parser.parse(source)
        if not parse_outcome.succeeded:
            return CompilationResult(
                diagnostics=parse_outcome.diagnostics,
                artifacts=(),
            )

        assert parse_outcome.program is not None
        semantic_outcome = self._semantic.analyze(parse_outcome.program)
        if not semantic_outcome.succeeded:
            return CompilationResult(
                diagnostics=semantic_outcome.diagnostics,
                artifacts=(),
            )

        if check_only:
            return CompilationResult(
                diagnostics=semantic_outcome.diagnostics,
                artifacts=(),
            )

        assert semantic_outcome.program is not None
        artifacts: list[GeneratedArtifact] = []
        diagnostics = list(semantic_outcome.diagnostics)

        try:
            for deck in semantic_outcome.program.decks:
                for format_name in formats:
                    generator_type = self.GENERATORS[format_name]
                    path = generator_type().generate(deck, output_dir)
                    artifacts.append(
                        GeneratedArtifact(
                            deck_name=deck.name,
                            format_name=format_name,
                            path=path,
                        )
                    )
        except (OSError, KeyError) as exc:
            diagnostics.append(
                Diagnostic(
                    code="GEN001",
                    message=f"falha durante a geração dos arquivos: {exc}.",
                    phase="geração de código",
                )
            )

        return CompilationResult(
            diagnostics=tuple(diagnostics),
            artifacts=tuple(artifacts),
        )
