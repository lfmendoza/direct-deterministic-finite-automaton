"""
Simulacion de AFD: procesa una cadena de entrada y determina si es aceptada.
"""

from __future__ import annotations

from automaton.direct_dfa import DFA


def simulate_dfa(dfa: DFA, input_string: str) -> bool:
    """Simula el AFD sobre la cadena dada.
    Retorna True si la cadena es aceptada, False en caso contrario.
    """
    current_state = dfa.start_state

    for symbol in input_string:
        if symbol not in dfa.alphabet:
            return False

        next_state = dfa.transitions.get((current_state, symbol))
        if next_state is None:
            return False

        current_state = next_state

    return current_state in dfa.accept_states
