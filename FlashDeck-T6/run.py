"""Atalho para executar o compilador sem instalar o comando `flashdeck`."""

from flashdeck.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
