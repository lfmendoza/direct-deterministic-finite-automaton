"""
Algoritmo Shunting-Yard para convertir expresiones regulares de notacion
infija a postfija. Maneja insercion de concatenacion implicita, desazucarado
de operadores (+ y ?) y precedencia de operadores.
"""

from __future__ import annotations

OPERATORS = {"|", ".", "*", "+", "?"}
PRECEDENCE = {"|": 1, ".": 2, "*": 3, "+": 3, "?": 3}
RIGHT_ASSOC = {"*", "+", "?"}


def _is_operand(c: str) -> bool:
    return c not in OPERATORS and c not in ("(", ")")


def insert_explicit_concat(regex: str) -> str:
    """Inserta el operador de concatenacion explicito '.' donde esta implicito."""
    result: list[str] = []
    i = 0
    while i < len(regex):
        c = regex[i]
        result.append(c)

        if i + 1 < len(regex):
            next_c = regex[i + 1]
            # Se inserta '.' entre: operando|)|*|+|? seguido de operando|(
            if (
                (_is_operand(c) or c in (")", "*", "+", "?"))
                and (_is_operand(next_c) or next_c == "(")
            ):
                result.append(".")
        i += 1

    return "".join(result)


def _desugar(regex: str) -> str:
    """Expande azucar sintactico: a+ -> a.a* y a? -> (a|ε)."""
    result: list[str] = []
    i = 0
    while i < len(regex):
        c = regex[i]
        if c == "+":
            # a+ se convierte en a.a*; si el token previo es ')' se duplica el grupo
            if result and result[-1] == ")":
                depth = 1
                j = len(result) - 2
                while j >= 0 and depth > 0:
                    if result[j] == ")":
                        depth += 1
                    elif result[j] == "(":
                        depth -= 1
                    j -= 1
                group = result[j + 1 :]
                result.extend(["."] + list(group) + ["*"])
            elif result:
                prev = result[-1]
                result.extend([".", prev, "*"])
        elif c == "?":
            # a? se convierte en (a|ε)
            if result and result[-1] == ")":
                depth = 1
                j = len(result) - 2
                while j >= 0 and depth > 0:
                    if result[j] == ")":
                        depth += 1
                    elif result[j] == "(":
                        depth -= 1
                    j -= 1
                group = result[j + 1 :]
                result[j + 1 :] = ["("] + list(group) + ["|", "ε", ")"]
            elif result:
                prev = result.pop()
                result.extend(["(", prev, "|", "ε", ")"])
        else:
            result.append(c)
        i += 1
    return "".join(result)


def shunting_yard(regex: str) -> str:
    """Convierte una regex infija a notacion postfija.

    Operadores soportados: | (union), . (concatenacion), * (cerradura de Kleene),
    + (cerradura positiva), ? (opcional).
    """
    # Primero desazucarar + y ?, luego insertar concatenacion explicita
    regex = _desugar(regex)
    regex = insert_explicit_concat(regex)

    output: list[str] = []
    stack: list[str] = []

    for c in regex:
        if _is_operand(c):
            output.append(c)
        elif c == "(":
            stack.append(c)
        elif c == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            if stack:
                stack.pop()
        else:
            # Es un operador: sacar del stack mientras tenga mayor precedencia
            while (
                stack
                and stack[-1] != "("
                and stack[-1] in PRECEDENCE
                and (
                    PRECEDENCE[stack[-1]] > PRECEDENCE[c]
                    or (PRECEDENCE[stack[-1]] == PRECEDENCE[c] and c not in RIGHT_ASSOC)
                )
            ):
                output.append(stack.pop())
            stack.append(c)

    while stack:
        output.append(stack.pop())

    return "".join(output)
