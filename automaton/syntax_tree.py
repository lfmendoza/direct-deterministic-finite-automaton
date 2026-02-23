"""
Construccion del arbol sintactico a partir de una expresion regular en postfijo.
Calcula nullable, firstpos, lastpos y followpos para la construccion directa
del AFD (Dragon Book, Seccion 3.9).
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Node:
    """Nodo base del arbol sintactico."""

    nullable: bool = False
    firstpos: set[int] = field(default_factory=set)
    lastpos: set[int] = field(default_factory=set)


@dataclass
class LeafNode(Node):
    """Hoja que representa un simbolo individual o epsilon."""

    symbol: str = ""
    position: int = -1


@dataclass
class CatNode(Node):
    """Nodo de concatenacion (c1 . c2)."""

    left: Node = field(default_factory=Node)
    right: Node = field(default_factory=Node)


@dataclass
class OrNode(Node):
    """Nodo de union (c1 | c2)."""

    left: Node = field(default_factory=Node)
    right: Node = field(default_factory=Node)


@dataclass
class StarNode(Node):
    """Nodo de cerradura de Kleene (c1*)."""

    child: Node = field(default_factory=Node)


def build_syntax_tree(
    postfix: str,
) -> tuple[Node, dict[int, str], dict[int, set[int]]]:
    """Construye el arbol sintactico a partir de la regex en postfijo.

    Retorna la raiz del arbol, el mapeo posicion->simbolo y la tabla followpos.
    """
    stack: list[Node] = []
    pos_counter = 0
    pos_symbols: dict[int, str] = {}

    for c in postfix:
        if c == ".":
            right = stack.pop()
            left = stack.pop()
            node = CatNode(left=left, right=right)
            node.nullable = left.nullable and right.nullable
            node.firstpos = (
                left.firstpos | right.firstpos if left.nullable else set(left.firstpos)
            )
            node.lastpos = (
                right.lastpos | left.lastpos if right.nullable else set(right.lastpos)
            )
            stack.append(node)

        elif c == "|":
            right = stack.pop()
            left = stack.pop()
            node = OrNode(left=left, right=right)
            node.nullable = left.nullable or right.nullable
            node.firstpos = left.firstpos | right.firstpos
            node.lastpos = left.lastpos | right.lastpos
            stack.append(node)

        elif c == "*":
            child = stack.pop()
            node = StarNode(child=child)
            node.nullable = True
            node.firstpos = set(child.firstpos)
            node.lastpos = set(child.lastpos)
            stack.append(node)

        elif c == "ε":
            node = LeafNode(symbol="ε", position=-1)
            node.nullable = True
            node.firstpos = set()
            node.lastpos = set()
            stack.append(node)

        else:
            # Hoja con simbolo del alfabeto
            pos_counter += 1
            pos = pos_counter
            pos_symbols[pos] = c
            node = LeafNode(symbol=c, position=pos)
            node.nullable = False
            node.firstpos = {pos}
            node.lastpos = {pos}
            stack.append(node)

    root = stack[0] if stack else LeafNode()

    followpos: dict[int, set[int]] = {p: set() for p in pos_symbols}
    _compute_followpos(root, followpos)

    return root, pos_symbols, followpos


def _compute_followpos(node: Node, followpos: dict[int, set[int]]) -> None:
    """Calcula followpos recursivamente para todas las posiciones del arbol."""
    if isinstance(node, CatNode):
        _compute_followpos(node.left, followpos)
        _compute_followpos(node.right, followpos)
        # Regla CAT: para cada i en lastpos(izq), agregar firstpos(der) a followpos(i)
        for i in node.left.lastpos:
            followpos[i] |= node.right.firstpos

    elif isinstance(node, OrNode):
        _compute_followpos(node.left, followpos)
        _compute_followpos(node.right, followpos)

    elif isinstance(node, StarNode):
        _compute_followpos(node.child, followpos)
        # Regla STAR: para cada i en lastpos(hijo), agregar firstpos(hijo) a followpos(i)
        for i in node.child.lastpos:
            followpos[i] |= node.child.firstpos
