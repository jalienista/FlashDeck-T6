# Relatório técnico - FlashDeck Compiler

## 1. Introdução

O projeto implementa um compilador completo para uma linguagem de domínio específico denominada FlashDeck. A linguagem foi criada para descrever baralhos de flashcards usados em estudos acadêmicos. O domínio foi escolhido porque permite manter a linguagem pequena e declarativa, ao mesmo tempo em que oferece regras semânticas relevantes e uma saída diretamente utilizável.

O compilador recebe um arquivo textual com decks e cards, executa análise léxica, sintática e semântica e, quando não há erros, gera uma página HTML interativa, um arquivo CSV compatível com o Anki e, opcionalmente, uma representação JSON.

## 2. Objetivos

### Objetivo geral

Projetar e implementar uma linguagem e um compilador completos, com gramática formal, verificações contextuais e geração de artefatos úteis.

### Objetivos específicos

- especificar os elementos léxicos e a gramática;
- construir uma AST independente da biblioteca de parsing;
- detectar e localizar erros;
- implementar pelo menos quatro verificações semânticas;
- separar o modelo sintático do modelo semanticamente válido;
- gerar uma interface de estudo autocontida;
- oferecer casos de teste e documentação reproduzível.

## 3. Definição da linguagem

Cada deck contém uma descrição, listas de tags e categorias e um conjunto de cards. Cada card possui identificador, frente, verso, tags, categoria e dificuldade.

A linguagem usa blocos delimitados por chaves, listas delimitadas por colchetes, strings entre aspas e ponto e vírgula ao final de cada campo. Comentários de linha e bloco são aceitos.

A especificação detalhada está em `docs/LANGUAGE.md` e a gramática executável em `flashdeck/grammar.lark`.

## 4. Ferramentas e tecnologias

- Python 3.10 ou superior;
- Lark para geração do lexer e parser LALR(1);
- `dataclasses` para AST e modelo semântico;
- módulos padrão `csv`, `json`, `argparse` e `pathlib`;
- Pytest para testes automatizados;
- HTML, CSS e JavaScript sem dependências externas para a aplicação gerada.

## 5. Implementação

### 5.1 Análise léxica e sintática

A gramática reconhece decks, cabeçalhos, cards e campos. O Lark produz tokens e uma árvore concreta. Um transformer percorre essa árvore e cria uma AST com localização de origem.

Erros léxicos e sintáticos são convertidos em diagnósticos próprios, contendo arquivo, linha, coluna, código e mensagem.

### 5.2 Análise semântica

A fase semântica percorre a AST e usa tabelas baseadas em dicionários e conjuntos. As quatro regras centrais da proposta são:

1. frentes de cards não podem se repetir no mesmo deck;
2. tags usadas devem estar declaradas;
3. dificuldade deve estar entre 1 e 5;
4. o deck deve ter uma quantidade mínima de cards.

Também foram implementadas regras adicionais para categorias, IDs, campos obrigatórios, repetições de campos, conteúdo vazio e consistência entre frente e verso.

### 5.3 Geração

O HTML gerado inclui o conjunto de cards em formato JSON e uma aplicação JavaScript para navegar, revelar, filtrar e embaralhar. O CSV contém frente, verso e tags em formato adequado para importação. O JSON opcional permite integração e depuração.

## 6. Testes e resultados

A suíte automatizada contém 26 testes. Na validação final do pacote, todos foram aprovados. Os testes incluem entradas válidas, erros léxicos e sintáticos, cada regra semântica principal e inspeção dos três formatos gerados.

Além dos testes automatizados, foram incluídos exemplos independentes na pasta `examples/`. Os exemplos inválidos são separados por finalidade, permitindo demonstrar cada etapa durante o vídeo ou apresentação.

## 7. Complexidade

A análise sintática é realizada pelo parser LALR. Na fase semântica, cada card e cada referência a tag são processados uma quantidade constante de vezes. Com consultas médias `O(1)` em conjuntos e dicionários, a complexidade esperada da análise semântica é linear no tamanho do modelo, `Theta(n + m)`, em que `n` é o número de cards e `m` o total de tags usadas.

A memória também é linear, pois AST, modelo e tabelas armazenam informações proporcionais ao arquivo de entrada.

## 8. Limitações

O projeto não implementa revisão espaçada persistente nem mídia nos cards. O CSV depende do processo de importação do Anki. A página HTML guarda o estado apenas durante sua execução e não sincroniza entre dispositivos.

Essas limitações não impedem o objetivo do T6, pois o compilador realiza as três fases exigidas e produz saídas úteis e demonstráveis.

## 9. Conclusão

O FlashDeck atende ao escopo de uma linguagem específica e declarativa. A separação entre gramática, AST, análise semântica e geradores facilita testes, manutenção e extensão. O resultado pode ser usado como ferramenta de estudo e como demonstração completa de conceitos de compiladores.
