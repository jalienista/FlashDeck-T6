# FlashDeck Compiler

> O FlashDeck é uma linguagem desenvolvida para criação de baralhos de flashcards. O compilador realiza análise léxica, sintática e semântica dos arquivos .fdeck e gera os formatos HTML, CSV e JSON.

## Identificação do trabalho

- **Disciplina:** Construção de Compiladores
- **Trabalho:** T6 - compilador completo para uma linguagem específica
- **Linguagem criada:** FlashDeck
- **Integrantes:**
  - João Manoel Ribeiro Machado - 822447
  - Julia Campanelli Granja - 823835
  - Kevyn Marques - 820895
- **Vídeo demonstrativo:** `PREENCHER - link do vídeo`

---

## 1. Visão geral

FlashDeck é uma linguagem de domínio específico, pequena e declarativa. Ela permite descrever decks de estudo por meio de:

- nome e descrição;
- tags e categorias declaradas no cabeçalho;
- cards com frente, verso, tags, categoria e dificuldade;
- comentários de linha e de bloco.

O compilador executa três fases principais:

```text
arquivo .fdeck
      |
      v
análise léxica e sintática (Lark + gramática LALR)
      |
      v
AST - árvore sintática abstrata
      |
      v
análise semântica
      |
      v
modelo válido
      |
      +--> página HTML interativa
      +--> CSV para Anki
      +--> JSON opcional
```

A página HTML gerada é autocontida: não precisa de servidor, biblioteca JavaScript nem internet. Basta abrir o arquivo no navegador.

---

## 2. Relação com os critérios do T6

| Critério | Implementação no projeto |
|---|---|
| **ALS - 25%** | Gramática em `flashdeck/grammar.lark`, lexer contextual e parser LALR(1) gerados pela biblioteca Lark, diagnóstico com linha e coluna e casos válidos/inválidos. |
| **AS - 25%** | Mais de quatro verificações semânticas, incluindo frentes duplicadas, tags e categorias não declaradas, dificuldade fora de 1 a 5 e quantidade mínima de cards. |
| **GCI - 25%** | Geração de HTML interativo, CSV para Anki e JSON opcional. |
| **Entrega - 25%** | README, código documentado, testes automatizados, exemplos e scripts de instalação. |

---

## 3. Exemplo da linguagem

```fdeck
deck "Compiladores" {
    description: "Perguntas para revisão da disciplina.";
    tags: [lexico, sintatico, semantica];
    categories: [conceitos, pratica];

    card analisador_lexico {
        front: "Qual é a função do analisador léxico?";
        back: "Agrupar caracteres em tokens e identificar erros léxicos.";
        tags: [lexico];
        category: conceitos;
        difficulty: 1;
    }

    card parser {
        front: "O que o parser verifica?";
        back: "Se a sequência de tokens pertence à linguagem definida pela gramática.";
        tags: [sintatico];
        category: conceitos;
        difficulty: 2;
    }
}
```

A ordem dos campos de um card é livre, mas cada campo obrigatório deve aparecer exatamente uma vez.

---

## 4. Requisitos

- Python 3.10 ou mais recente;
- `pip`;
- navegador moderno para abrir o HTML gerado.

Dependências Python:

- `lark` para geração do lexer/parser;
- `pytest` somente para os testes.

---

## 5. Instalação

### Windows - PowerShell

Na raiz do projeto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Também é possível executar:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup_windows.ps1
```

### Linux ou macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Ou:

```bash
bash scripts/setup_unix.sh
```

---

## 6. Como executar o compilador

Sem instalar o comando global:

```bash
python run.py examples/valid/compiladores.fdeck
```

Após instalar o projeto com `pip install -e .`:

```bash
flashdeck examples/valid/compiladores.fdeck
```

Por padrão, os arquivos são escritos em `dist/` nos formatos HTML e CSV.

### Gerar todos os formatos

```bash
python run.py examples/valid/compiladores.fdeck --format all -o dist
```

### Executar somente as análises

```bash
python run.py examples/valid/compiladores.fdeck --check
```

### Alterar a quantidade mínima de cards

```bash
python run.py deck.fdeck --min-cards 3
```

### Ajuda completa

```bash
python run.py --help
```

### Códigos de saída

- `0`: compilação concluída;
- `1`: erro léxico, sintático, semântico, de leitura ou de geração;
- `2`: uso inválido da linha de comando.

---

## 7. Arquivos gerados

Para um deck chamado `Compiladores - Conceitos Essenciais`, o compilador pode gerar:

```text
dist/
├── compiladores-conceitos-essenciais.html
├── compiladores-conceitos-essenciais-anki.csv
└── compiladores-conceitos-essenciais.json
```

### HTML

A aplicação inclui:

- clique para revelar o verso;
- botões anterior e próximo;
- filtros por texto, tag, categoria e dificuldade;
- embaralhamento;
- barra de progresso;
- atalhos de teclado;
- layout responsivo;
- modo claro ou escuro conforme o sistema.

### CSV para Anki

O CSV possui as colunas:

```text
Front, Back, Tags
```

A categoria e a dificuldade são convertidas em tags hierárquicas, por exemplo:

```text
lexico category::conceitos difficulty::2
```

Na importação do Anki, associe as colunas `Front`, `Back` e `Tags` aos campos correspondentes.

### JSON

O formato JSON é opcional e serve para inspeção, depuração ou integração com outras aplicações.

---

## 8. Verificações semânticas

A gramática garante a forma geral do arquivo. As seguintes regras exigem informações de contexto e são verificadas depois do parsing:

| Código | Regra |
|---|---|
| `SEM001` | Nome do deck não pode ser vazio. |
| `SEM002` | Nomes de decks devem ser únicos no mesmo arquivo. |
| `SEM003` | Cabeçalhos `description`, `tags` e `categories` são obrigatórios. |
| `SEM004` | Um campo de cabeçalho não pode ser repetido. |
| `SEM005` | Cada deck deve ter no mínimo N cards, sendo N = 2 por padrão. |
| `SEM101` | IDs de cards devem ser únicos dentro do deck. |
| `SEM102` | Todo card deve conter os cinco campos obrigatórios. |
| `SEM103` | Um campo de card não pode ser repetido. |
| `SEM104` | Frente e verso não podem ser vazios. |
| `SEM105` | Frente e verso de um card devem ser diferentes. |
| `SEM106` | Dois cards não podem ter a mesma frente no mesmo deck. A comparação ignora maiúsculas e espaços excedentes. |
| `SEM107` | Toda tag usada por um card deve estar declarada no cabeçalho. |
| `SEM108` | Toda categoria usada por um card deve estar declarada no cabeçalho. |
| `SEM109` | A dificuldade deve estar no intervalo de 1 a 5. |
| `SEM110` | Uma lista não pode repetir a mesma tag ou categoria. |

Avisos não interrompem a compilação:

- `WARN001`: tag declarada e não utilizada;
- `WARN002`: categoria declarada e não utilizada.

---

## 9. Diagnóstico de erros

Exemplo:

```text
examples/invalid/semantic_invalid_difficulty.fdeck:10:9:
erro [SEM109] (análise semântica) a dificuldade do card 'primeiro'
deve estar entre 1 e 5, mas foi informada como 0.
```

O diagnóstico contém:

1. arquivo;
2. linha;
3. coluna;
4. gravidade;
5. código estável;
6. fase do compilador;
7. descrição do problema.

O compilador coleta vários erros semânticos na mesma execução. Erros léxicos e sintáticos interrompem o processo antes da análise semântica.

---

## 10. Testes

Execute:

```bash
python -m pytest
```

No estado entregue neste repositório, a suíte possui **26 testes automatizados**, cobrindo:

- programas válidos;
- erro léxico;
- erro sintático;
- regras semânticas principais;
- geração de HTML, CSV e JSON;
- modo `--check`;
- todos os exemplos válidos e inválidos do repositório.

Também é possível executar uma demonstração completa:

```bash
bash scripts/demo_unix.sh
```

No Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\demo_windows.ps1
```

Consulte `docs/TESTING.md` para o roteiro de testes manuais e os resultados esperados.

---

## 11. Estrutura do repositório

```text
FlashDeck-T6/
├── flashdeck/
│   ├── grammar.lark              # gramática da linguagem
│   ├── parser.py                 # análise léxica/sintática e AST
│   ├── semantic.py               # verificações semânticas
│   ├── compiler.py               # coordenação das fases
│   ├── cli.py                    # interface de linha de comando
│   ├── ast_nodes.py              # nós da AST
│   ├── model.py                  # modelo semântico válido
│   ├── diagnostics.py            # erros e avisos
│   ├── generators/               # geradores HTML, CSV e JSON
│   └── templates/deck.html       # aplicação HTML gerada
├── examples/
│   ├── valid/                    # entradas aceitas
│   └── invalid/                  # entradas rejeitadas de propósito
├── tests/                        # testes automatizados
├── docs/                         # documentação complementar
├── scripts/                      # instalação e demonstração
├── run.py                        # atalho de execução
├── pyproject.toml                # empacotamento e dependências
└── README.md
```

---

## 12. Documentação complementar

- [`docs/LANGUAGE.md`](docs/LANGUAGE.md): especificação lexical, sintática e exemplos;
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md): decisões de implementação e fluxo interno;
- [`docs/TESTING.md`](docs/TESTING.md): testes automatizados e manuais;
- [`docs/TECHNICAL_REPORT.md`](docs/TECHNICAL_REPORT.md): relatório técnico do projeto;
- [`docs/VIDEO_SCRIPT.md`](docs/VIDEO_SCRIPT.md): roteiro pronto para o vídeo;
- [`docs/DELIVERY_CHECKLIST.md`](docs/DELIVERY_CHECKLIST.md): itens a conferir antes de enviar;
- [`docs/ORAL_DEFENSE.md`](docs/ORAL_DEFENSE.md): perguntas prováveis e respostas para apresentação;
- [`docs/VALIDATION_REPORT.md`](docs/VALIDATION_REPORT.md): registro das validações executadas.

---

## 13. Limitações e evoluções possíveis

- o HTML não salva o histórico de revisão entre dispositivos;
- o CSV não cria automaticamente um baralho no Anki, pois a criação ocorre no momento da importação;
- a linguagem aceita somente texto, sem imagens ou áudio;
- a quantidade mínima de cards é uma opção do compilador, não uma declaração do arquivo.

Possíveis extensões:

- cards do tipo lacuna ou *cloze*;
- suporte a imagens e links;
- agendamento de revisão espaçada;
- geração de pacote `.apkg`;
- importação de vários decks em uma única página;
- servidor local com persistência do progresso.

---

## 14. Licença

Projeto disponibilizado sob a licença MIT.
