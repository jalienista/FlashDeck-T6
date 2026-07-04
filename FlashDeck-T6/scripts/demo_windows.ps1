$ErrorActionPreference = "Continue"

Write-Host "=== 1. Testes automatizados ==="
python -m pytest
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "`n=== 2. Compilacao valida ==="
python run.py examples/valid/compiladores.fdeck --format all -o dist
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "`n=== 3. Erro lexico esperado ==="
python run.py examples/invalid/lexical_invalid_character.fdeck --check

Write-Host "`n=== 4. Erro sintatico esperado ==="
python run.py examples/invalid/syntax_missing_semicolon.fdeck --check

Write-Host "`n=== 5. Erros semanticos esperados ==="
python run.py examples/invalid/semantic_multiple_errors.fdeck --check

Write-Host "`nDemonstracao finalizada. Os comandos invalidos devem terminar com erro proposital."
Write-Host "Abra dist\compiladores-conceitos-essenciais.html no navegador."
