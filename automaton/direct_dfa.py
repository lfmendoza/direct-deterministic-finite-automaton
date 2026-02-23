"""
Construccion directa de un AFD a partir de una expresion regular
utilizando el metodo de followpos (Dragon Book, Seccion 3.9.5).

Pasos del algoritmo:
1. Aumentar la regex r -> (r)#
2. Construir arbol sintactico desde postfijo
3. Calcular nullable, firstpos, lastpos, followpos
4. Estado inicial = firstpos(raiz)
5. Construir transiciones usando la tabla followpos
6. Estados de aceptacion = aquellos que contienen la posicion de #
"""

from __future__ import annotations

from dataclasses import dataclass, field

from automaton.shunting_yard import shunting_yard
from automaton.syntax_tree import build_syntax_tree


@dataclass
class DFA:
    """Representacion de un automata finito determinista."""

    states: list[frozenset[int]] = field(default_factory=list)
    alphabet: set[str] = field(default_factory=set)
    transitions: dict[tuple[int, str], int] = field(default_factory=dict)
    start_state: int = 0
    accept_states: set[int] = field(default_factory=set)


def build_direct_dfa(regex: str) -> DFA:
    """Construye un AFD directamente desde la regex usando followpos."""
    augmented = f"({regex})#"
    postfix = shunting_yard(augmented)
    root, pos_symbols, followpos = build_syntax_tree(postfix)

    # Encontrar la posicion del marcador de fin #
    end_pos = None
    for pos, sym in pos_symbols.items():
        if sym == "#":
            end_pos = pos
            break

    alphabet = {sym for sym in pos_symbols.values() if sym != "#"}
    start = frozenset(root.firstpos)

    dfa = DFA()
    dfa.alphabet = alphabet
    dfa.start_state = 0

    # Cola de estados no marcados para procesar
    unmarked: list[frozenset[int]] = [start]
    dfa.states.append(start)
    state_map: dict[frozenset[int], int] = {start: 0}

    if end_pos is not None and end_pos in start:
        dfa.accept_states.add(0)

    while unmarked:
        current = unmarked.pop(0)
        current_id = state_map[current]

        for symbol in sorted(alphabet):
            # Unir followpos de todas las posiciones con este simbolo
            next_state_positions: set[int] = set()
            for p in current:
                if pos_symbols.get(p) == symbol:
                    next_state_positions |= followpos.get(p, set())

            if not next_state_positions:
                continue

            next_state = frozenset(next_state_positions)

            if next_state not in state_map:
                state_id = len(dfa.states)
                state_map[next_state] = state_id
                dfa.states.append(next_state)
                unmarked.append(next_state)

                if end_pos is not None and end_pos in next_state:
                    dfa.accept_states.add(state_id)

            dfa.transitions[(current_id, symbol)] = state_map[next_state]

    return dfa
