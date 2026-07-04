"""Análise semântica da AST FlashDeck."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from flashdeck.ast_nodes import CardFieldNode, CardNode, DeckFieldNode, DeckNode, ProgramNode
from flashdeck.diagnostics import Diagnostic, Severity
from flashdeck.model import Card, Deck, Program


@dataclass(frozen=True)
class SemanticOutcome:
    program: Program | None
    diagnostics: tuple[Diagnostic, ...]

    @property
    def errors(self) -> tuple[Diagnostic, ...]:
        return tuple(d for d in self.diagnostics if d.severity == Severity.ERROR)

    @property
    def warnings(self) -> tuple[Diagnostic, ...]:
        return tuple(d for d in self.diagnostics if d.severity == Severity.WARNING)

    @property
    def succeeded(self) -> bool:
        return self.program is not None and not self.errors


class SemanticAnalyzer:
    """Valida regras que não são expressas diretamente pela gramática.

    As verificações incluem, entre outras:
    - nomes de decks e IDs de cards únicos;
    - cabeçalhos e campos obrigatórios e não repetidos;
    - frente não repetida no mesmo deck;
    - uso apenas de tags e categorias declaradas;
    - dificuldade no intervalo de 1 a 5;
    - quantidade mínima de cards.
    """

    REQUIRED_DECK_FIELDS = ("description", "tags", "categories")
    REQUIRED_CARD_FIELDS = ("front", "back", "tags", "category", "difficulty")

    def __init__(self, min_cards: int = 2) -> None:
        if min_cards < 1:
            raise ValueError("min_cards deve ser maior ou igual a 1")
        self.min_cards = min_cards

    def analyze(self, ast: ProgramNode) -> SemanticOutcome:
        diagnostics: list[Diagnostic] = []
        valid_decks: list[Deck] = []
        seen_deck_names: dict[str, DeckNode] = {}

        for deck_node in ast.decks:
            normalized_name = self._normalize_text(deck_node.name)

            if not normalized_name:
                diagnostics.append(
                    self._error("SEM001", "o nome do deck não pode ser vazio.", deck_node)
                )
            elif normalized_name in seen_deck_names:
                diagnostics.append(
                    self._error(
                        "SEM002",
                        f"já existe outro deck chamado {deck_node.name!r} neste arquivo.",
                        deck_node,
                    )
                )
            else:
                seen_deck_names[normalized_name] = deck_node

            deck = self._analyze_deck(deck_node, diagnostics)
            if deck is not None:
                valid_decks.append(deck)

        errors = [d for d in diagnostics if d.severity == Severity.ERROR]
        program = None if errors else Program(decks=tuple(valid_decks))
        return SemanticOutcome(program=program, diagnostics=tuple(diagnostics))

    def _analyze_deck(
        self,
        node: DeckNode,
        diagnostics: list[Diagnostic],
    ) -> Deck | None:
        error_count_before = self._error_count(diagnostics)
        grouped_fields = self._group_deck_fields(node.fields)

        for required in self.REQUIRED_DECK_FIELDS:
            declarations = grouped_fields.get(required, [])
            if not declarations:
                diagnostics.append(
                    self._error(
                        "SEM003",
                        f"o deck deve declarar o campo de cabeçalho obrigatório '{required}'.",
                        node,
                    )
                )
            elif len(declarations) > 1:
                for duplicate in declarations[1:]:
                    diagnostics.append(
                        self._error(
                            "SEM004",
                            f"o campo de cabeçalho '{required}' foi declarado mais de uma vez.",
                            duplicate,
                        )
                    )

        description = self._first_deck_value(grouped_fields, "description", "")
        declared_tags = list(self._first_deck_value(grouped_fields, "tags", []))
        declared_categories = list(self._first_deck_value(grouped_fields, "categories", []))

        self._check_duplicate_identifiers(
            declared_tags,
            "tag",
            self._first_deck_field(grouped_fields, "tags", node),
            diagnostics,
        )
        self._check_duplicate_identifiers(
            declared_categories,
            "categoria",
            self._first_deck_field(grouped_fields, "categories", node),
            diagnostics,
        )

        if len(node.cards) < self.min_cards:
            diagnostics.append(
                self._error(
                    "SEM005",
                    (
                        f"o deck deve possuir no mínimo {self.min_cards} cards, "
                        f"mas possui {len(node.cards)}."
                    ),
                    node,
                )
            )

        seen_ids: dict[str, CardNode] = {}
        seen_fronts: dict[str, CardNode] = {}
        cards: list[Card] = []
        used_tags: set[str] = set()
        used_categories: set[str] = set()

        for card_node in node.cards:
            if card_node.identifier in seen_ids:
                diagnostics.append(
                    self._error(
                        "SEM101",
                        f"o identificador de card '{card_node.identifier}' está repetido no deck.",
                        card_node,
                    )
                )
            else:
                seen_ids[card_node.identifier] = card_node

            card = self._analyze_card(
                card_node,
                declared_tags=set(declared_tags),
                declared_categories=set(declared_categories),
                diagnostics=diagnostics,
            )
            if card is None:
                continue

            normalized_front = self._normalize_text(card.front)
            if normalized_front in seen_fronts:
                diagnostics.append(
                    self._error(
                        "SEM106",
                        (
                            "dois cards não podem ter o mesmo texto na frente "
                            f"dentro do mesmo deck: {card.front!r}."
                        ),
                        card_node,
                    )
                )
            else:
                seen_fronts[normalized_front] = card_node

            used_tags.update(card.tags)
            used_categories.add(card.category)
            cards.append(card)

        if self._error_count(diagnostics) > error_count_before:
            return None

        for tag in sorted(set(declared_tags) - used_tags):
            location = self._first_deck_field(grouped_fields, "tags", node)
            diagnostics.append(
                self._warning(
                    "WARN001",
                    f"a tag declarada '{tag}' não é utilizada por nenhum card.",
                    location,
                )
            )

        for category in sorted(set(declared_categories) - used_categories):
            location = self._first_deck_field(grouped_fields, "categories", node)
            diagnostics.append(
                self._warning(
                    "WARN002",
                    f"a categoria declarada '{category}' não é utilizada por nenhum card.",
                    location,
                )
            )

        return Deck(
            name=node.name.strip(),
            description=str(description).strip(),
            declared_tags=tuple(declared_tags),
            declared_categories=tuple(declared_categories),
            cards=tuple(cards),
        )

    def _analyze_card(
        self,
        node: CardNode,
        declared_tags: set[str],
        declared_categories: set[str],
        diagnostics: list[Diagnostic],
    ) -> Card | None:
        error_count_before = self._error_count(diagnostics)
        grouped_fields = self._group_card_fields(node.fields)

        for required in self.REQUIRED_CARD_FIELDS:
            fields = grouped_fields.get(required, [])
            if not fields:
                diagnostics.append(
                    self._error(
                        "SEM102",
                        f"o card '{node.identifier}' não possui o campo obrigatório '{required}'.",
                        node,
                    )
                )
            elif len(fields) > 1:
                for duplicate in fields[1:]:
                    diagnostics.append(
                        self._error(
                            "SEM103",
                            (
                                f"o campo '{required}' foi declarado mais de uma vez "
                                f"no card '{node.identifier}'."
                            ),
                            duplicate,
                        )
                    )

        if any(not grouped_fields.get(field) for field in self.REQUIRED_CARD_FIELDS):
            return None

        front_field = grouped_fields["front"][0]
        back_field = grouped_fields["back"][0]
        tags_field = grouped_fields["tags"][0]
        category_field = grouped_fields["category"][0]
        difficulty_field = grouped_fields["difficulty"][0]

        front = str(front_field.value).strip()
        back = str(back_field.value).strip()
        tags = list(tags_field.value)
        category = str(category_field.value)
        difficulty = int(difficulty_field.value)

        if not front:
            diagnostics.append(
                self._error("SEM104", f"a frente do card '{node.identifier}' não pode ser vazia.", front_field)
            )
        if not back:
            diagnostics.append(
                self._error("SEM104", f"o verso do card '{node.identifier}' não pode ser vazio.", back_field)
            )
        if front and back and self._normalize_text(front) == self._normalize_text(back):
            diagnostics.append(
                self._error(
                    "SEM105",
                    f"a frente e o verso do card '{node.identifier}' devem ser diferentes.",
                    back_field,
                )
            )

        self._check_duplicate_identifiers(tags, "tag do card", tags_field, diagnostics)

        for tag in dict.fromkeys(tags):
            if tag not in declared_tags:
                diagnostics.append(
                    self._error(
                        "SEM107",
                        (
                            f"a tag '{tag}' usada no card '{node.identifier}' "
                            "não foi declarada no cabeçalho do deck."
                        ),
                        tags_field,
                    )
                )

        if category not in declared_categories:
            diagnostics.append(
                self._error(
                    "SEM108",
                    (
                        f"a categoria '{category}' usada no card '{node.identifier}' "
                        "não foi declarada no cabeçalho do deck."
                    ),
                    category_field,
                )
            )

        if not 1 <= difficulty <= 5:
            diagnostics.append(
                self._error(
                    "SEM109",
                    (
                        f"a dificuldade do card '{node.identifier}' deve estar "
                        f"entre 1 e 5, mas foi informada como {difficulty}."
                    ),
                    difficulty_field,
                )
            )

        if self._error_count(diagnostics) > error_count_before:
            return None

        return Card(
            identifier=node.identifier,
            front=front,
            back=back,
            tags=tuple(tags),
            category=category,
            difficulty=difficulty,
        )

    @staticmethod
    def _group_deck_fields(fields: list[DeckFieldNode]) -> dict[str, list[DeckFieldNode]]:
        grouped: dict[str, list[DeckFieldNode]] = defaultdict(list)
        for field in fields:
            grouped[field.kind].append(field)
        return grouped

    @staticmethod
    def _group_card_fields(fields: list[CardFieldNode]) -> dict[str, list[CardFieldNode]]:
        grouped: dict[str, list[CardFieldNode]] = defaultdict(list)
        for field in fields:
            grouped[field.kind].append(field)
        return grouped

    @staticmethod
    def _first_deck_value(grouped, kind: str, default):
        values = grouped.get(kind, [])
        return values[0].value if values else default

    @staticmethod
    def _first_deck_field(grouped, kind: str, default):
        values = grouped.get(kind, [])
        return values[0] if values else default

    def _check_duplicate_identifiers(
        self,
        values: list[str],
        item_name: str,
        located_node,
        diagnostics: list[Diagnostic],
    ) -> None:
        seen: set[str] = set()
        for value in values:
            if value in seen:
                diagnostics.append(
                    self._error(
                        "SEM110",
                        f"{item_name} '{value}' foi informado mais de uma vez na mesma lista.",
                        located_node,
                    )
                )
            seen.add(value)

    @staticmethod
    def _normalize_text(value: str) -> str:
        return " ".join(value.split()).casefold()

    @staticmethod
    def _error_count(diagnostics: list[Diagnostic]) -> int:
        return sum(1 for d in diagnostics if d.severity == Severity.ERROR)

    @staticmethod
    def _location(node) -> tuple[int, int]:
        location = node.location
        return location.line, location.column

    def _error(self, code: str, message: str, node) -> Diagnostic:
        line, column = self._location(node)
        return Diagnostic(
            code=code,
            message=message,
            line=line,
            column=column,
            severity=Severity.ERROR,
            phase="análise semântica",
        )

    def _warning(self, code: str, message: str, node) -> Diagnostic:
        line, column = self._location(node)
        return Diagnostic(
            code=code,
            message=message,
            line=line,
            column=column,
            severity=Severity.WARNING,
            phase="análise semântica",
        )
