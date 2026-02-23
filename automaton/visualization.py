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

    # Configuracion general del grafo para mayor claridad
    dot.attr(
        rankdir="LR",
        dpi="150",
        bgcolor="white",
        fontname="Helvetica",
        nodesep="0.8",
        ranksep="1.0",
        pad="0.5",
        margin="0.3",
    )

    # Estilo por defecto de los nodos
    dot.attr(
        "node",
        fontname="Helvetica",
        fontsize="14",
        style="filled",
        fillcolor="#e8edf2",
        color="#3b4a5a",
        penwidth="2",
        width="0.6",
        height="0.6",
    )

    # Estilo por defecto de las aristas
    dot.attr(
        "edge",
        fontname="Helvetica",
        fontsize="13",
        color="#5a6a7a",
        fontcolor="#1a1a1a",
        penwidth="1.5",
        arrowsize="0.9",
    )

    # Flecha de entrada al estado inicial
    dot.node("start", shape="point", width="0.0", height="0.0")
    dot.edge("start", f"q{dfa.start_state}", penwidth="2", color="#2c3e50")

    for i in range(len(dfa.states)):
        label = f"q{i}"

        if i in dfa.accept_states and i == dfa.start_state:
            # Estado inicial y de aceptacion
            dot.node(
                f"q{i}", label=label, shape="doublecircle",
                fillcolor="#a8d8a8", color="#2e7d32", fontcolor="#1b5e20",
                penwidth="3",
            )
        elif i in dfa.accept_states:
            # Estado de aceptacion
            dot.node(
                f"q{i}", label=label, shape="doublecircle",
                fillcolor="#a8d8a8", color="#2e7d32", fontcolor="#1b5e20",
                penwidth="3",
            )
        elif i == dfa.start_state:
            # Estado inicial (no de aceptacion)
            dot.node(
                f"q{i}", label=label, shape="circle",
                fillcolor="#bbdefb", color="#1565c0", fontcolor="#0d47a1",
                penwidth="2.5",
            )
        else:
            # Estado regular
            dot.node(f"q{i}", label=label, shape="circle")

    # Agrupar transiciones con mismo (origen, destino) para combinar etiquetas
    edge_labels: dict[tuple[int, int], list[str]] = {}
    for (src, symbol), dst in dfa.transitions.items():
        key = (src, dst)
        if key not in edge_labels:
            edge_labels[key] = []
        edge_labels[key].append(symbol)

    for (src, dst), symbols in edge_labels.items():
        label = ", ".join(sorted(symbols))

        if src == dst:
            # Self-loop: resaltar para que sea facil de identificar
            dot.edge(
                f"q{src}", f"q{dst}", label=f"  {label}  ",
                color="#8e44ad", fontcolor="#6a1b9a",
                penwidth="1.8",
            )
        else:
            dot.edge(f"q{src}", f"q{dst}", label=f"  {label}  ")

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
