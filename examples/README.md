# Exemplos

## Válidos

- `valid/compiladores.fdeck`: deck principal para demonstração;
- `valid/estruturas_de_dados.fdeck`: segundo domínio para mostrar que o compilador não depende de conteúdo fixo.

## Inválidos

- `lexical_invalid_character.fdeck`: caractere `@` inesperado;
- `syntax_missing_semicolon.fdeck`: ponto e vírgula ausente;
- `semantic_duplicate_front.fdeck`: frentes equivalentes;
- `semantic_undeclared_tag.fdeck`: referência a tag ausente;
- `semantic_invalid_difficulty.fdeck`: valores 0 e 6;
- `semantic_too_few_cards.fdeck`: somente um card;
- `semantic_multiple_errors.fdeck`: vários erros coletados na mesma análise.

Compile um exemplo válido:

```bash
python run.py examples/valid/compiladores.fdeck --format all
```

Execute um exemplo inválido:

```bash
python run.py examples/invalid/semantic_multiple_errors.fdeck
```
