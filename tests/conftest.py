from __future__ import annotations

import textwrap

import pytest


@pytest.fixture
def valid_source() -> str:
    return textwrap.dedent(
        '''
        deck "Deck de Teste" {
            description: "Descrição para testes automatizados.";
            tags: [tag_a, tag_b];
            categories: [teoria, pratica];

            card c1 {
                front: "Pergunta um";
                back: "Resposta um";
                tags: [tag_a];
                category: teoria;
                difficulty: 1;
            }

            card c2 {
                front: "Pergunta dois";
                back: "Resposta dois";
                tags: [tag_b];
                category: pratica;
                difficulty: 5;
            }
        }
        '''
    ).strip()
