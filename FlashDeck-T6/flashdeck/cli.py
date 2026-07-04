"""Interface de linha de comando do compilador FlashDeck."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from flashdeck import __version__
from flashdeck.compiler import FlashDeckCompiler
from flashdeck.diagnostics import Severity


VALID_FORMATS = ("html", "csv", "json")


def _parse_formats(raw: str) -> tuple[str, ...]:
    requested = [item.strip().lower() for item in raw.split(",") if item.strip()]
    if "all" in requested:
        return VALID_FORMATS

    invalid = sorted(set(requested) - set(VALID_FORMATS))
    if invalid:
        raise argparse.ArgumentTypeError(
            "formatos inválidos: " + ", ".join(invalid) + ". Use html,csv,json ou all."
        )

    # remove repetições preservando a ordem
    unique = tuple(dict.fromkeys(requested))
    if not unique:
        raise argparse.ArgumentTypeError("informe pelo menos um formato de saída.")
    return unique


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="flashdeck",
        description=(
            "Compila arquivos .fdeck, valida a linguagem e gera uma página HTML "
            "de estudo e/ou um CSV para Anki."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Exemplos:
  python run.py examples/valid/compiladores.fdeck
  python run.py deck.fdeck -o dist --format all
  python run.py deck.fdeck --check
  flashdeck deck.fdeck --format html,csv --min-cards 2
""",
    )
    parser.add_argument("input", type=Path, help="arquivo-fonte .fdeck")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("dist"),
        help="diretório de saída (padrão: dist)",
    )
    parser.add_argument(
        "--format",
        type=_parse_formats,
        default=("html", "csv"),
        metavar="LISTA",
        help="formatos separados por vírgula: html,csv,json ou all",
    )
    parser.add_argument(
        "--min-cards",
        type=int,
        default=2,
        metavar="N",
        help="quantidade mínima de cards por deck (padrão: 2)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="executa apenas as análises, sem gerar arquivos",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="exibe somente erros e avisos",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_argument_parser()
    args = parser.parse_args(argv)

    if args.min_cards < 1:
        parser.error("--min-cards deve ser maior ou igual a 1")

    compiler = FlashDeckCompiler(min_cards=args.min_cards)
    result = compiler.compile_file(
        input_path=args.input,
        output_dir=args.output,
        formats=args.format,
        check_only=args.check,
    )

    for diagnostic in result.diagnostics:
        stream = sys.stderr if diagnostic.severity == Severity.ERROR else sys.stdout
        print(diagnostic.format(str(args.input)), file=stream)

    if not result.succeeded:
        print(
            f"Compilação interrompida: {len(result.errors)} erro(s) encontrado(s).",
            file=sys.stderr,
        )
        return 1

    if not args.quiet:
        if args.check:
            print("Análises léxica, sintática e semântica concluídas com sucesso.")
        else:
            print("Compilação concluída com sucesso.")
            for artifact in result.artifacts:
                print(
                    f"  [{artifact.format_name.upper()}] "
                    f"{artifact.deck_name}: {artifact.path.resolve()}"
                )
        if result.warnings:
            print(f"Foram emitidos {len(result.warnings)} aviso(s).")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
