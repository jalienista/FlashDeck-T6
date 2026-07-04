# Relatório de validação do pacote

Validação executada em 03/07/2026.

## Testes automatizados

```text
26 passed
```

## Empacotamento

- bytecode de todos os módulos compilado sem erros;
- wheel `flashdeck_compiler-1.0.0-py3-none-any.whl` construído com sucesso;
- wheel instalado em ambiente virtual limpo;
- comando `flashdeck` executado a partir da instalação limpa.

## Geração

O exemplo `examples/valid/compiladores.fdeck` gerou com sucesso:

- HTML autocontido;
- CSV UTF-8 com BOM;
- JSON válido.

## Inspeções adicionais

- HTML processado por parser HTML sem placeholders restantes;
- JavaScript extraído do HTML aprovado por `node --check`;
- CSV lido novamente pelo módulo `csv`;
- JSON lido novamente pelo módulo `json`.

Este relatório registra a validação realizada no pacote entregue. Recomenda-se repetir `python -m pytest` no computador do grupo antes do envio ao professor.
