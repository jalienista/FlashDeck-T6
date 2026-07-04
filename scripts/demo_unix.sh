#!/usr/bin/env bash
set -u

printf '=== 1. Testes automatizados ===\n'
python -m pytest || exit $?

printf '\n=== 2. Compilacao valida ===\n'
python run.py examples/valid/compiladores.fdeck --format all -o dist || exit $?

printf '\n=== 3. Erro lexico esperado ===\n'
python run.py examples/invalid/lexical_invalid_character.fdeck --check || true

printf '\n=== 4. Erro sintatico esperado ===\n'
python run.py examples/invalid/syntax_missing_semicolon.fdeck --check || true

printf '\n=== 5. Erros semanticos esperados ===\n'
python run.py examples/invalid/semantic_multiple_errors.fdeck --check || true

printf '\nDemonstracao finalizada. Os comandos invalidos devem terminar com erro proposital.\n'
printf 'Abra dist/compiladores-conceitos-essenciais.html no navegador.\n'
