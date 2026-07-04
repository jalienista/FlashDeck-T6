# Arquitetura do compilador FlashDeck

## 1. Pipeline

```text
                    +----------------------+
arquivo UTF-8 ----> | FlashDeckParser      |
                    | Lark / LALR(1)       |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | ProgramNode / AST    |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | SemanticAnalyzer     |
                    | tabela de símbolos   |
                    | verificações globais |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Program / modelo     |
                    | semanticamente válido|
                    +----------+-----------+
                               |
              +----------------+----------------+
              |                |                |
              v                v                v
        HtmlGenerator     CsvGenerator     JsonGenerator
```

## 2. Análise léxica e sintática

A biblioteca Lark lê `grammar.lark` e constrói:

- lexer contextual;
- parser LALR(1);
- árvore sintática concreta com posições de origem.

O `_AstTransformer` converte a árvore concreta em nós próprios do projeto. A AST preserva os campos repetidos e ausentes para que essas situações sejam diagnosticadas pela fase semântica, em vez de ficarem escondidas na gramática.

## 3. AST e modelo semântico

Existem duas representações distintas:

### AST

Classes em `ast_nodes.py`:

- `ProgramNode`;
- `DeckNode`;
- `DeckFieldNode`;
- `CardNode`;
- `CardFieldNode`.

A AST pode representar programas incorretos. Cada nó relevante contém linha e coluna.

### Modelo semântico

Classes em `model.py`:

- `Program`;
- `Deck`;
- `Card`.

Esse modelo é criado somente quando não há erros. Os geradores não precisam repetir as validações, pois recebem dados já consistentes.

## 4. Análise semântica

A análise usa conjuntos e dicionários como tabelas de símbolos:

- `seen_deck_names` controla decks já declarados;
- `seen_ids` controla IDs de cards no escopo do deck;
- `seen_fronts` controla frentes normalizadas;
- `declared_tags` e `declared_categories` validam referências;
- agrupamentos por tipo detectam campos ausentes e repetidos.

Para um deck com `n` cards e `m` ocorrências totais de tags, o custo esperado é `Theta(n + m)`, pois as consultas em conjuntos e dicionários possuem custo médio constante.

## 5. Diagnósticos

A classe `Diagnostic` padroniza:

- código;
- mensagem;
- linha e coluna;
- gravidade;
- fase.

Os códigos tornam os testes estáveis e facilitam identificar a origem de cada falha.

## 6. Geração de código

### HTML

O gerador serializa o modelo em JSON e o insere em um template autocontido. O JavaScript manipula os textos com `textContent`, evitando interpretar conteúdo dos cards como HTML.

### CSV

O gerador usa o módulo `csv` da biblioteca padrão. O arquivo é escrito em `UTF-8 com BOM`, facilitando a abertura em planilhas sem perda de acentos.

### JSON

O formato JSON reflete o modelo validado e facilita testes e extensões.

## 7. Decisões de projeto

### Por que uma linguagem declarativa?

- escopo compatível com o prazo da disciplina;
- sintaxe pequena;
- semântica contextual clara;
- saída visual fácil de demonstrar;
- utilidade acadêmica direta.

### Por que Lark?

- é um gerador de parser para Python;
- mantém a gramática separada do código;
- suporta LALR e posições de origem;
- simplifica instalação e execução em diferentes sistemas.

### Por que separar AST e modelo válido?

Sem essa separação, os geradores precisariam lidar com campos ausentes, duplicados e referências inválidas. A arquitetura atual cria uma fronteira clara: depois da análise semântica, o restante do compilador pode assumir invariantes.
