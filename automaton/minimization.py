"""
Minimizacion de AFD usando el algoritmo de refinamiento de particiones
de Hopcroft. Produce un AFD equivalente con el numero minimo de estados,
fusionando estados indistinguibles.
"""

from __future__ import annotations

from automaton.direct_dfa import DFA


def minimize_dfa(dfa: DFA) -> DFA:
    """Minimiza el AFD y retorna uno nuevo equivalente con menos estados."""
    n = len(dfa.states)
    if n == 0:
        return dfa

    all_states = set(range(n))
    non_accept = all_states - dfa.accept_states

    # Particion inicial: estados de aceptacion vs no aceptacion
    partitions: list[set[int]] = []
    if dfa.accept_states:
        partitions.append(set(dfa.accept_states))
    if non_accept:
        partitions.append(non_accept)

    worklist: list[set[int]] = list(partitions)
    alphabet = sorted(dfa.alphabet)

    while worklist:
        splitter = worklist.pop(0)

        for symbol in alphabet:
            # Estados que transicionan hacia el splitter con este simbolo
            predecessors: set[int] = set()
            for s in all_states:
                target = dfa.transitions.get((s, symbol))
                if target is not None and target in splitter:
                    predecessors.add(s)

            if not predecessors:
                continue

            new_partitions: list[set[int]] = []
            for group in partitions:
                intersection = group & predecessors
                difference = group - predecessors

                if intersection and difference:
                    # Se divide el grupo en dos
                    new_partitions.append(intersection)
                    new_partitions.append(difference)

                    if group in worklist:
                        worklist.remove(group)
                        worklist.append(intersection)
                        worklist.append(difference)
                    else:
                        # Agregar el subgrupo mas pequeno al worklist
                        if len(intersection) <= len(difference):
                            worklist.append(intersection)
                        else:
                            worklist.append(difference)
                else:
                    new_partitions.append(group)

            partitions = new_partitions

    # Construir el AFD minimizado
    state_to_partition: dict[int, int] = {}
    for idx, group in enumerate(partitions):
        for s in group:
            state_to_partition[s] = idx

    min_dfa = DFA()
    min_dfa.alphabet = set(dfa.alphabet)
    min_dfa.states = [frozenset() for _ in partitions]
    min_dfa.start_state = state_to_partition[dfa.start_state]

    for idx, group in enumerate(partitions):
        if group & dfa.accept_states:
            min_dfa.accept_states.add(idx)

    for idx, group in enumerate(partitions):
        representative = next(iter(group))
        for symbol in alphabet:
            target = dfa.transitions.get((representative, symbol))
            if target is not None:
                min_dfa.transitions[(idx, symbol)] = state_to_partition[target]

    # Renumerar para que el estado inicial sea 0
    if min_dfa.start_state != 0:
        old_start = min_dfa.start_state
        remap = {i: i for i in range(len(partitions))}
        remap[0] = old_start
        remap[old_start] = 0

        new_transitions: dict[tuple[int, str], int] = {}
        for (s, sym), t in min_dfa.transitions.items():
            new_transitions[(remap[s], sym)] = remap[t]

        new_accept = {remap[s] for s in min_dfa.accept_states}

        min_dfa.transitions = new_transitions
        min_dfa.accept_states = new_accept
        min_dfa.start_state = 0

    return min_dfa
