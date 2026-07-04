$ErrorActionPreference = "Stop"

Write-Host "[1/4] Criando ambiente virtual..."
python -m venv .venv

Write-Host "[2/4] Ativando ambiente..."
& .\.venv\Scripts\Activate.ps1

Write-Host "[3/4] Instalando o projeto e dependencias..."
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"

Write-Host "[4/4] Executando testes..."
python -m pytest

Write-Host "Ambiente preparado com sucesso."
Write-Host "Para ativar novamente: .\.venv\Scripts\Activate.ps1"
