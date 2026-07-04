# Comece aqui

O projeto já está implementado. Antes de entregar, faça estas etapas no seu computador.

## 1. Personalize os dados do grupo

Procure por `PREENCHER` nos arquivos:

- `README.md`;
- `pyproject.toml`;
- `LICENSE`.

Inclua nomes, RAs, e-mails e, depois de gravar, o link do vídeo.

## 2. Instale no Windows

Abra o PowerShell na pasta do projeto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## 3. Teste tudo

```powershell
python -m pytest
python run.py examples/valid/compiladores.fdeck --format all -o dist
```

Abra:

```text
dist\compiladores-conceitos-essenciais.html
```

Teste os botões, filtros e atalhos.

## 4. Demonstre os erros

```powershell
python run.py examples/invalid/lexical_invalid_character.fdeck --check
python run.py examples/invalid/syntax_missing_semicolon.fdeck --check
python run.py examples/invalid/semantic_duplicate_front.fdeck --check
python run.py examples/invalid/semantic_undeclared_tag.fdeck --check
python run.py examples/invalid/semantic_invalid_difficulty.fdeck --check
python run.py examples/invalid/semantic_too_few_cards.fdeck --check
```

Esses comandos devem falhar de propósito e mostrar os diagnósticos esperados.

## 5. Grave o vídeo

Use o roteiro `docs/VIDEO_SCRIPT.md`. Mostre a linguagem, a gramática, os erros, a geração e os testes.

## 6. Publique

Crie um repositório, envie os arquivos, confirme que o README aparece corretamente e teste uma instalação limpa. Depois, entregue o link no AVA.

O checklist completo está em `docs/DELIVERY_CHECKLIST.md`.
