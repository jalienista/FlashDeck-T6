# Perguntas prováveis para apresentação

## Por que isso é um compilador e não apenas um conversor?

Porque existe uma linguagem formal com tokens e gramática, uma fase de parsing que constrói uma AST, uma análise semântica contextual e uma fase separada de geração de código. Entradas inválidas não chegam aos geradores.

## O que a gramática não verifica?

A gramática verifica a estrutura. Ela não sabe se uma tag foi declarada anteriormente, se outra frente igual já apareceu, se a dificuldade pertence ao intervalo permitido ou quantos cards existem. Essas regras dependem de contexto e ficam na análise semântica.

## Por que permitir campos repetidos na gramática?

Isso deixa a gramática menor e permite emitir um erro semântico mais claro, como “o campo difficulty foi declarado mais de uma vez”. A AST preserva o erro para a fase apropriada.

## Qual algoritmo de parsing foi usado?

LALR(1), gerado pela biblioteca Lark a partir de `grammar.lark`.

## Onde está a tabela de símbolos?

Ela é representada por dicionários e conjuntos na análise semântica. Há tabelas para nomes de decks, IDs de cards, frentes normalizadas, tags declaradas e categorias declaradas.

## Como frentes duplicadas são comparadas?

O compilador remove espaços excedentes, converte para comparação sem distinção de maiúsculas e usa a forma normalizada como chave de um dicionário. O texto original é preservado para geração.

## Por que os geradores recebem um modelo diferente da AST?

A AST pode conter erros. O modelo `Program/Deck/Card` só é criado após todas as validações. Isso reduz acoplamento e impede geração acidental de dados inconsistentes.

## Qual é a complexidade da análise semântica?

Esperada `Theta(n + m)`, sendo `n` o número de cards e `m` o total de tags usadas, porque cada item é visitado poucas vezes e as consultas em conjuntos/dicionários têm custo médio constante.

## O CSV é realmente compatível com Anki?

Ele usa as colunas `Front`, `Back` e `Tags`, codificação UTF-8 e aspas adequadas. Durante a importação, o usuário mapeia essas colunas para os campos do tipo de nota escolhido.

## O professor pode criar entradas diferentes?

Sim. O compilador não depende dos exemplos. Os testes demonstram regras gerais, e o parser lê qualquer arquivo que respeite a gramática.

## O que poderia ser melhorado?

Adicionar cards com lacunas, mídia, revisão espaçada persistente e geração direta de pacote do Anki. Essas extensões podem usar o mesmo modelo e adicionar novos geradores.
