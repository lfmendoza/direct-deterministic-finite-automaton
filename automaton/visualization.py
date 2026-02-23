"""
Generacion de diagramas de AFD con Graphviz e impresion de la tabla
de transiciones en consola.
"""

from __future__ import annotations

import os

from automaton.direct_dfa import DFA

try:
    import graphviz
    HAS_GRAPHVIZ = True
except ImportError:
    HAS_GRAPHVIZ = False


def render_dfa(
    dfa: DFA,
    filename: str = "dfa",
    output_dir: str = "output",
    title: str = "DFA",
    view: bool = False,
) -> str | None:
    """Renderiza el AFD como imagen PNG usando Graphviz.
    Retorna la ruta de la imagen generada, o None si Graphviz no esta disponible.
    """
    if not HAS_GRAPHVIZ:
        print("[AVISO] paquete graphviz no instalado. Se omite la visualizacion.")
        print("  Instalar con: pip install graphviz")
        print("  Tambien instalar binarios de Graphviz: https://graphviz.org/download/")
        return None

    os.makedirs(output_dir, exist_ok=True)

    dot = graphviz.Digraph(title, format="png")
    dot.attr(rankdir="LR", fontsize="12")

    # Nodo invisible para la flecha de entrada
    dot.node("start", shape="point")
    dot.edge("start", f"q{dfa.start_state}")

    for i in range(len(dfa.states)):
        label = f"q{i}"
        shape = "doublecircle" if i in dfa.accept_states else "circle"
        dot.node(f"q{i}", label=label, shape=shape)

    # Agrupar transiciones con mismo (origen, destino) para combinar etiquetas
    edge_labels: dict[tuple[int, int], list[str]] = {}
    for (src, symbol), dst in dfa.transitions.items():
        key = (src, dst)
        if key not in edge_labels:
            edge_labels[key] = []
        edge_labels[key].append(symbol)

    for (src, dst), symbols in edge_labels.items():
        label = ", ".join(sorted(symbols))
        dot.edge(f"q{src}", f"q{dst}", label=label)

    filepath = os.path.join(output_dir, filename)
    dot.render(filepath, cleanup=True)

    output_path = f"{filepath}.png"
    print(f"  Diagrama del AFD guardado en: {output_path}")

    if view:
        try:
            dot.view()
        except Exception:
            pass

    return output_path


def print_dfa_table(dfa: DFA) -> None:
    """Imprime la tabla de transiciones del AFD en consola."""
    alphabet = sorted(dfa.alphabet)

    header = (
        f"{'Estado':>8} | "
        + " | ".join(f"{s:>6}" for s in alphabet)
        + " | Acepta"
    )
    print(header)
    print("-" * len(header))

    for i in range(len(dfa.states)):
        row = f"{'q' + str(i):>8} | "
        for symbol in alphabet:
            target = dfa.transitions.get((i, symbol))
            cell = f"q{target}" if target is not None else "-"
            row += f"{cell:>6} | "
        row += "Si" if i in dfa.accept_states else "No"
        print(row)
