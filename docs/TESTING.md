# Plano de testes

## 1. Testes automatizados

Na raiz do projeto:

```bash
python -m pytest
```

Resultado verificado na preparação da entrega:

```text
26 passed
```

## 2. Cobertura funcional

| Grupo | Casos cobertos |
|---|---|
| Léxico | caractere inesperado, comentários, strings e identificadores válidos |
| Sintático | ponto e vírgula ausente, estrutura de deck e cards |
| Semântico | frentes repetidas, tags/categorias não declaradas, dificuldade, cardinalidade, IDs, campos obrigatórios |
| Geração | existência e conteúdo básico de HTML, CSV e JSON |
| Integração | todos os arquivos de `examples/valid` compilam e todos os arquivos de `examples/invalid` falham |

## 3. Roteiro manual de demonstração

### Teste A - programa válido

```bash
python run.py examples/valid/compiladores.fdeck --format all -o dist
```

Esperado:

- código de saída 0;
- mensagem de sucesso;
- três arquivos em `dist/`.

Abra `dist/compiladores-conceitos-essenciais.html` e teste:

1. revelar o verso;
2. navegar pelos cards;
3. filtrar por `semantica`;
4. filtrar por categoria `pratica`;
5. pesquisar a palavra `parser`;
6. embaralhar;
7. usar as teclas esquerda, direita e espaço.

### Teste B - erro léxico

```bash
python run.py examples/invalid/lexical_invalid_character.fdeck
```

Esperado: `LEX001`, apontando o caractere `@`.

### Teste C - erro sintático

```bash
python run.py examples/invalid/syntax_missing_semicolon.fdeck
```

Esperado: código iniciado por `SYN`, próximo à declaração de tags.

### Teste D - frente repetida

```bash
python run.py examples/invalid/semantic_duplicate_front.fdeck
```

Esperado: `SEM106`.

### Teste E - tag não declarada

```bash
python run.py examples/invalid/semantic_undeclared_tag.fdeck
```

Esperado: `SEM107`.

### Teste F - dificuldade inválida

```bash
python run.py examples/invalid/semantic_invalid_difficulty.fdeck
```

Esperado: dois diagnósticos `SEM109`, para dificuldades 0 e 6.

### Teste G - deck pequeno

```bash
python run.py examples/invalid/semantic_too_few_cards.fdeck
```

Esperado: `SEM005`.

### Teste H - vários erros

```bash
python run.py examples/invalid/semantic_multiple_errors.fdeck
```

Esperado: vários diagnósticos na mesma execução, demonstrando que a fase semântica não para no primeiro erro.

## 4. Testes que o professor pode criar

O compilador não depende dos nomes ou textos dos exemplos. Ele deve responder corretamente a:

- novos nomes de deck;
- ordem diferente dos campos;
- múltiplos decks no mesmo arquivo;
- novos IDs, tags e categorias válidos;
- números negativos ou maiores que 5;
- campos duplicados;
- cabeçalhos ausentes;
- espaços e capitalização diferentes em frentes duplicadas;
- arquivos com comentários;
- strings com escapes.

## 5. Teste de instalação limpa

Em outra pasta ou máquina:

```bash
git clone URL_DO_REPOSITORIO
cd NOME_DO_REPOSITORIO
python -m venv .venv
# ativar o ambiente
python -m pip install -e ".[dev]"
python -m pytest
python run.py examples/valid/compiladores.fdeck --format all
```

Faça esse teste antes de enviar o link ao professor.
