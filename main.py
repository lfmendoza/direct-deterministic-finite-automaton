"""
Programa principal: pipeline interactivo de regex a AFD.

Uso:
    python main.py

Solicita una expresion regular, construye y muestra el AFD,
luego permite probar cadenas para verificar aceptacion.
"""

from __future__ import annotations

import os
import platform

# Agregar Graphviz al PATH en Windows si no esta configurado
if platform.system() == "Windows":
    for gv_path in (
        r"C:\Program Files\Graphviz\bin",
        r"C:\Program Files (x86)\Graphviz\bin",
    ):
        if os.path.isdir(gv_path) and gv_path not in os.environ.get("PATH", ""):
            os.environ["PATH"] = gv_path + os.pathsep + os.environ.get("PATH", "")

from automaton.shunting_yard import shunting_yard, insert_explicit_concat, _desugar
from automaton.direct_dfa import build_direct_dfa
from automaton.minimization import minimize_dfa
from automaton.simulation import simulate_dfa
from automaton.visualization import render_dfa, print_dfa_table


def main() -> None:
    print("=" * 60)
    print("  Construccion Directa de AFD")
    print("  Diseno de Lenguajes de Programacion")
    print("=" * 60)

    while True:
        print()
        regex = input(
            "Ingrese una expresion regular (o 'salir' para terminar): "
        ).strip()

        if regex.lower() == "salir":
            print("Fin del programa.")
            break

        if not regex:
            print("Error: expresion vacia.")
            continue

        try:
            # Mostrar pasos intermedios de conversion
            desugared = _desugar(regex)
            with_concat = insert_explicit_concat(desugared)
            postfix = shunting_yard(regex)

            print(f"\n  Regex original:     {regex}")
            if desugared != regex:
                print(f"  Desugared:          {desugared}")
            print(f"  Con concatenacion:  {with_concat}")
            print(f"  Postfix:            {postfix}")

            # Construccion directa del AFD
            print("\n--- Construccion directa del AFD ---")
            dfa = build_direct_dfa(regex)
            print(f"  Estados: {len(dfa.states)}")
            print(f"  Alfabeto: {sorted(dfa.alphabet)}")
            print(f"  Estado inicial: q{dfa.start_state}")
            print(
                f"  Estados de aceptacion: "
                f"{{'q' + str(s) for s in sorted(dfa.accept_states)}}"
            )

            print("\nTabla de transiciones (AFD directo):")
            print_dfa_table(dfa)

            output_dir = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "output"
            )
            render_dfa(
                dfa,
                filename="dfa_direct",
                output_dir=output_dir,
                title="AFD - Construccion Directa",
            )

            # Minimizacion del AFD
            print("\n--- Minimizacion del AFD ---")
            min_dfa = minimize_dfa(dfa)
            print(f"  Estados: {len(min_dfa.states)}")
            print(f"  Estado inicial: q{min_dfa.start_state}")
            print(
                f"  Estados de aceptacion: "
                f"{{'q' + str(s) for s in sorted(min_dfa.accept_states)}}"
            )

            print("\nTabla de transiciones (AFD minimizado):")
            print_dfa_table(min_dfa)

            render_dfa(
                min_dfa,
                filename="dfa_minimized",
                output_dir=output_dir,
                title="AFD - Minimizado",
            )

            # Simulacion de cadenas
            print("\n--- Simulacion de cadenas ---")
            print(
                "  Ingrese cadenas para probar "
                "(vacio para nueva regex, 'salir' para terminar)"
            )

            while True:
                w = input("\n  Cadena w: ")

                if w.lower() == "salir":
                    print("Fin del programa.")
                    return

                if w == "":
                    break

                accepted = simulate_dfa(min_dfa, w)
                result = "ACEPTADA" if accepted else "RECHAZADA"
                print(f"  Resultado: '{w}' -> {result}")

        except Exception as e:
            print(f"\nError procesando la expresion: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
