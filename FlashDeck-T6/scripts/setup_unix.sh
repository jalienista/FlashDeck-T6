#!/usr/bin/env bash
set -euo pipefail

printf '[1/4] Criando ambiente virtual...\n'
python3 -m venv .venv

printf '[2/4] Ativando ambiente...\n'
# shellcheck disable=SC1091
source .venv/bin/activate

printf '[3/4] Instalando o projeto e dependencias...\n'
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'

printf '[4/4] Executando testes...\n'
python -m pytest

printf 'Ambiente preparado com sucesso.\n'
printf 'Para ativar novamente: source .venv/bin/activate\n'
