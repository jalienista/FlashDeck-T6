# Roteiro do vídeo demonstrativo

Duração recomendada: **4 a 6 minutos**.

## 1. Abertura - 20 segundos

> Olá, este é o FlashDeck, nosso trabalho final de Construção de Compiladores. Criamos uma linguagem declarativa para escrever baralhos de flashcards. O compilador valida o arquivo e gera uma página de estudo interativa e um CSV que pode ser importado no Anki.

Mostrar rapidamente o README e a estrutura do repositório.

## 2. Problema e proposta - 30 segundos

> Em vez de escrever HTML ou montar cada card manualmente, o usuário descreve somente os dados do deck. A linguagem possui uma sintaxe pequena, com nome, descrição, tags, categorias e cards.

Abrir `examples/valid/compiladores.fdeck` e destacar:

- cabeçalho;
- um card;
- dificuldade;
- comentários.

## 3. Análise léxica e sintática - 50 segundos

Abrir `flashdeck/grammar.lark`.

> A gramática é processada pelo Lark, que gera um lexer contextual e um parser LALR. O parser reconhece a estrutura e preserva linha e coluna. Depois, transformamos a árvore concreta em uma AST própria.

Executar:

```bash
python run.py examples/invalid/lexical_invalid_character.fdeck
python run.py examples/invalid/syntax_missing_semicolon.fdeck
```

Mostrar que os erros têm linha, coluna, fase e código.

## 4. Análise semântica - 1 minuto e 10 segundos

> Depois do parsing, verificamos regras que dependem de contexto. As quatro principais são: não repetir a frente, usar somente tags declaradas, manter a dificuldade entre 1 e 5 e possuir um número mínimo de cards.

Executar:

```bash
python run.py examples/invalid/semantic_duplicate_front.fdeck
python run.py examples/invalid/semantic_undeclared_tag.fdeck
python run.py examples/invalid/semantic_invalid_difficulty.fdeck
python run.py examples/invalid/semantic_too_few_cards.fdeck
```

Depois mostrar:

```bash
python run.py examples/invalid/semantic_multiple_errors.fdeck
```

> Também coletamos vários erros semânticos de uma vez, ajudando o autor a corrigir o arquivo sem precisar executar o compilador repetidamente.

## 5. Geração de código - 1 minuto e 20 segundos

Executar:

```bash
python run.py examples/valid/compiladores.fdeck --format all -o dist
```

Abrir o HTML e demonstrar:

1. revelar card;
2. próximo e anterior;
3. filtro por tag;
4. filtro por dificuldade;
5. busca;
6. embaralhar;
7. atalhos do teclado.

Abrir rapidamente o CSV e o JSON.

> O HTML é autocontido e funciona sem servidor. O CSV usa três colunas compatíveis com o processo de importação do Anki. A categoria e a dificuldade são preservadas como tags hierárquicas.

## 6. Testes - 35 segundos

Executar:

```bash
python -m pytest
```

> A suíte automatizada verifica parsing, regras semânticas, geração e todos os exemplos do repositório. No estado final, os 26 testes passam.

## 7. Encerramento - 20 segundos

> Assim, o projeto cobre análise léxica e sintática, análise semântica e geração de código, além de documentação, testes e exemplos reproduzíveis. O README apresenta todos os comandos necessários para instalar, executar e modificar o compilador.

## Dicas de gravação

- grave em 1080p;
- aumente a fonte do terminal;
- limpe `dist/` antes da demonstração;
- não edite o código durante o vídeo;
- mostre o resultado real dos comandos;
- deixe o link do vídeo no README antes da entrega.
