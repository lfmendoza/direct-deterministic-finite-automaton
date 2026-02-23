"""
Paquete automaton: construccion directa de AFD a partir de expresiones regulares.
"""

from automaton.direct_dfa import DFA, build_direct_dfa
from automaton.minimization import minimize_dfa
from automaton.simulation import simulate_dfa

__all__ = [
    "DFA",
    "build_direct_dfa",
    "minimize_dfa",
    "simulate_dfa",
]
