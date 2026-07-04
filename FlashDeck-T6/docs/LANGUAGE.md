# Especificação da linguagem FlashDeck

## 1. Objetivo

FlashDeck é uma linguagem declarativa para especificar baralhos de flashcards. Seu arquivo-fonte usa a extensão `.fdeck` e deve estar codificado em UTF-8.

## 2. Elementos léxicos

### Palavras reservadas

```text
deck description tags categories card front back category difficulty
```

### Identificadores

Identificadores são usados para IDs, tags e categorias.

```text
NAME = letra ou sublinhado, seguido de letras, algarismos ou sublinhados
```

Exemplos válidos:

```text
lexico
analise_semantica
card_01
_compiladores
```

Exemplos inválidos:

```text
1card
analise-semantica
minha tag
```

### Strings

Strings são delimitadas por aspas duplas e aceitam escapes usuais:

```fdeck
"Texto simples"
"Linha 1\nLinha 2"
"Ele disse: \"olá\""
```

### Números

O token numérico aceita inteiros com sinal. A gramática aceita qualquer inteiro, enquanto a análise semântica restringe a dificuldade ao intervalo de 1 a 5.

### Comentários

```fdeck
// comentário de linha

/* comentário
   de bloco */
```

### Espaços

Espaços, tabulações e quebras de linha são ignorados fora das strings.

## 3. Gramática

A gramática executável está em `flashdeck/grammar.lark`. Em forma simplificada:

```ebnf
programa          = deck, { deck } ;
deck              = "deck", STRING, "{", { item_deck }, "}" ;
item_deck         = descricao | tags_deck | categorias | card ;
descricao         = "description", ":", STRING, ";" ;
tags_deck         = "tags", ":", "[", [ lista_ids ], "]", ";" ;
categorias        = "categories", ":", "[", [ lista_ids ], "]", ";" ;
card              = "card", NAME, "{", { campo_card }, "}" ;
campo_card        = frente | verso | tags_card | categoria | dificuldade ;
frente            = "front", ":", STRING, ";" ;
verso             = "back", ":", STRING, ";" ;
tags_card          = "tags", ":", "[", [ lista_ids ], "]", ";" ;
categoria         = "category", ":", NAME, ";" ;
dificuldade       = "difficulty", ":", INTEIRO, ";" ;
lista_ids         = NAME, { ",", NAME } ;
```

## 4. Regras semânticas

A gramática propositalmente permite alguns estados que são rejeitados depois. Isso mantém a gramática simples e demonstra uma fase semântica separada.

### 4.1 Escopo do arquivo

- deve existir pelo menos um deck;
- nomes de decks não podem ser vazios;
- nomes de decks devem ser únicos no arquivo.

### 4.2 Cabeçalho do deck

- `description`, `tags` e `categories` são obrigatórios;
- cada um pode aparecer apenas uma vez;
- tags e categorias não podem se repetir em suas listas.

### 4.3 Cards

- o deck precisa ter pelo menos dois cards por padrão;
- IDs são únicos dentro do deck;
- `front`, `back`, `tags`, `category` e `difficulty` são obrigatórios e únicos no card;
- frente e verso não podem ser vazios nem iguais;
- frentes não podem se repetir dentro do deck;
- tags usadas devem estar declaradas;
- a categoria usada deve estar declarada;
- dificuldade deve estar entre 1 e 5.

## 5. Sensibilidade a maiúsculas

- palavras reservadas e identificadores são sensíveis a maiúsculas;
- a comparação de frentes duplicadas ignora maiúsculas/minúsculas e normaliza espaços;
- o texto exibido preserva a grafia original.

Exemplo: `"O que é AST?"` e `"  o QUE é ast?  "` são considerados a mesma frente.

## 6. Exemplo válido

Consulte `examples/valid/compiladores.fdeck`.

## 7. Exemplos inválidos

A pasta `examples/invalid/` separa casos de:

- caractere inválido;
- ponto e vírgula ausente;
- frente duplicada;
- tag não declarada;
- dificuldade inválida;
- quantidade insuficiente de cards;
- múltiplos erros semânticos.
