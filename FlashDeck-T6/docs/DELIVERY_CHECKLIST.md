# Checklist de entrega

## Identificação

- [ ] Preencher nomes, RAs e e-mails no `README.md`.
- [ ] Preencher autores em `pyproject.toml`.
- [ ] Atualizar o nome no `LICENSE`.
- [ ] Colocar o link do vídeo no `README.md`.

## Repositório

- [ ] Criar o repositório no GitHub ou GitLab.
- [ ] Fazer commit de todo o código-fonte e da gramática.
- [ ] Conferir se `examples/`, `tests/`, `docs/` e `scripts/` foram enviados.
- [ ] Não enviar `.venv`, caches ou arquivos temporários.
- [ ] Se o repositório for privado, adicionar o professor.

## Validação técnica

- [ ] Clonar o repositório em uma pasta limpa.
- [ ] Criar um ambiente virtual.
- [ ] Executar `python -m pip install -e ".[dev]"`.
- [ ] Executar `python -m pytest` e confirmar que todos os testes passam.
- [ ] Compilar `examples/valid/compiladores.fdeck`.
- [ ] Abrir e testar o HTML gerado.
- [ ] Executar ao menos um caso léxico, um sintático e quatro semânticos.
- [ ] Conferir acentos no CSV.

## Vídeo

- [ ] Explicar para que serve a linguagem.
- [ ] Mostrar a sintaxe.
- [ ] Mostrar a gramática.
- [ ] Demonstrar erro léxico.
- [ ] Demonstrar erro sintático.
- [ ] Demonstrar as quatro regras semânticas centrais.
- [ ] Gerar e abrir a saída HTML.
- [ ] Mostrar testes automatizados.
- [ ] Verificar se o link está acessível sem solicitar permissão.

## Entrega no AVA

- [ ] Escolher um integrante para enviar.
- [ ] Colar o link do repositório como comentário na atividade.
- [ ] Abrir o link após o envio para confirmar que está correto.
- [ ] Guardar uma cópia do ZIP final e do vídeo.

## Texto sugerido para o comentário no AVA

```text
Olá, professor. Segue o repositório do Trabalho 6 - FlashDeck Compiler:

LINK_DO_REPOSITORIO

O README contém instruções de instalação, execução, testes, exemplos e o link do vídeo demonstrativo.
```
