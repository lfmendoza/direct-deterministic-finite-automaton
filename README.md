# Construccion Directa de AFD a partir de Expresiones Regulares

Diseno de Lenguajes de Programacion — Universidad del Valle de Guatemala

## Descripcion

Programa que construye un AFD (Automata Finito Determinista) directamente a partir de una expresion regular, utilizando el algoritmo de construccion directa basado en followpos (Dragon Book, Seccion 3.9.5). Incluye minimizacion por Hopcroft, visualizacion con Graphviz y simulacion de cadenas.

## Estructura del proyecto

```
direct-deterministic-finite-automaton/
├── automaton/                # Paquete principal
│   ├── __init__.py           # Re-exporta la API publica
│   ├── shunting_yard.py      # Conversion infija a postfija (Shunting-Yard)
│   ├── syntax_tree.py        # Arbol sintactico, nullable, firstpos, lastpos, followpos
│   ├── direct_dfa.py         # Construccion directa del AFD desde followpos
│   ├── minimization.py       # Minimizacion del AFD (algoritmo de Hopcroft)
│   ├── simulation.py         # Simulacion de aceptacion de cadenas
│   └── visualization.py      # Diagramas con Graphviz y tabla de transiciones
├── output/                   # Diagramas generados (no se versiona)
├── main.py                   # Punto de entrada interactivo
├── requirements.txt          # Dependencias de Python
└── README.md
```

## Requisitos previos

| Dependencia | Version | Enlace |
| ----------- | ------- | ------ |
| Python      | 3.10+   | https://www.python.org/downloads/ |
| Graphviz    | cualquiera | https://graphviz.org/download/ |

### Instalacion de Graphviz (binario del sistema)

**Windows** (cualquiera de las dos):

```bash
winget install Graphviz.Graphviz
```

```bash
choco install graphviz
```

**macOS**:

```bash
brew install graphviz
```

**Linux (Debian/Ubuntu)**:

```bash
sudo apt install graphviz
```

## Configuracion

1. Clonar el repositorio:

```bash
git clone https://github.com/lfmendoza/direct-deterministic-finite-automaton.git
cd direct-deterministic-finite-automaton
```

2. Crear y activar un ambiente virtual:

```bash
python -m venv venv
```

**Windows (PowerShell)**:
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD)**:
```cmd
venv\Scripts\activate.bat
```

**Windows (Git Bash) / macOS / Linux**:
```bash
source venv/bin/activate       # macOS/Linux
source venv/Scripts/activate   # Git Bash en Windows
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Ejecucion

```bash
python main.py
```

### Flujo de uso

1. Ingresar una expresion regular en el prompt.
2. El programa muestra la conversion a postfijo, construye el AFD por construccion directa y lo minimiza.
3. Para cada AFD se muestra:
   - Cantidad de estados, alfabeto, estado inicial y estados de aceptacion.
   - Tabla de transiciones en consola.
   - Diagrama PNG guardado en `output/`.
4. Ingresar cadenas para probar aceptacion o rechazo.
5. Presionar **Enter** (cadena vacia) para ingresar una nueva regex, o escribir `salir` para terminar.

### Ejemplo de uso

```
============================================================
  Construccion Directa de AFD
  Diseno de Lenguajes de Programacion
============================================================

Ingrese una expresion regular (o 'salir' para terminar): (a|b)*abb

  Regex original:     (a|b)*abb
  Con concatenacion:  (a|b)*.a.b.b
  Postfix:            ab|*a.b.b.

--- Construccion directa del AFD ---
  Estados: 4
  Alfabeto: ['a', 'b']
  Estado inicial: q0
  Estados de aceptacion: {'q3'}

Tabla de transiciones (AFD directo):
  Estado |      a |      b | Acepta
-----------------------------------
      q0 |     q1 |     q0 | No
      q1 |     q1 |     q2 | No
      q2 |     q1 |     q3 | No
      q3 |     q1 |     q0 | Si

--- Simulacion de cadenas ---
  Ingrese cadenas para probar (vacio para nueva regex, 'salir' para terminar)

  Cadena w: abb
  Resultado: 'abb' -> ACEPTADA

  Cadena w: abab
  Resultado: 'abab' -> RECHAZADA

  Cadena w: aabb
  Resultado: 'aabb' -> ACEPTADA
```

### Operadores soportados

| Operador | Significado        | Ejemplo   |
| -------- | ------------------ | --------- |
| `\|`     | Union              | `a\|b`    |
| `*`      | Cerradura de Kleene| `a*`      |
| `+`      | Cerradura positiva | `a+`      |
| `?`      | Opcional           | `a?`      |
| `()`     | Agrupacion         | `(a\|b)*` |

La concatenacion es implicita: `ab` significa `a` seguido de `b`.

## Arquitectura

```mermaid
flowchart LR
    A["Regex (infija)\n\n(a|b)*abb"] -->|"shunting_yard.py\n_desugar()\ninsert_explicit_concat()"| B["Desazucarado\n+\nConcatenacion explicita\n\n(a|b)*.a.b.b"]

    B -->|"shunting_yard.py\nshunting_yard()"| C["Postfijo\n\nab|*a.b.b."]

    C -->|"syntax_tree.py\nbuild_syntax_tree()"| D["Arbol Sintactico\n\nnullable, firstpos\nlastpos, followpos"]

    D -->|"direct_dfa.py\nbuild_direct_dfa()"| E["AFD\n(construccion directa)"]

    E -->|"minimization.py\nminimize_dfa()"| F["AFD Minimizado"]

    F --> G["visualization.py\nrender_dfa()\nprint_dfa_table()"]
    F --> H["simulation.py\nsimulate_dfa()"]

    G -->|"Salida"| I["Diagrama PNG\n+\nTabla de transiciones"]
    H -->|"Salida"| J["Cadena ACEPTADA\no RECHAZADA"]

    style A fill:#4a90d9,color:#fff
    style B fill:#5ba0e0,color:#fff
    style C fill:#5ba0e0,color:#fff
    style D fill:#6db33f,color:#fff
    style E fill:#e8a838,color:#fff
    style F fill:#e8a838,color:#fff
    style G fill:#9b59b6,color:#fff
    style H fill:#9b59b6,color:#fff
    style I fill:#2c3e50,color:#fff
    style J fill:#2c3e50,color:#fff
```

| Modulo                       | Descripcion                                              |
| ---------------------------- | -------------------------------------------------------- |
| `automaton/shunting_yard.py` | Conversion infija a postfija con concatenacion explicita |
| `automaton/syntax_tree.py`   | Arbol sintactico, nullable, firstpos, lastpos, followpos |
| `automaton/direct_dfa.py`    | Construccion directa del AFD desde followpos             |
| `automaton/minimization.py`  | Minimizacion por refinamiento de particiones (Hopcroft)  |
| `automaton/simulation.py`    | Prueba de aceptacion de cadenas                          |
| `automaton/visualization.py` | Generacion de diagramas PNG y tabla de transiciones      |
| `main.py`                    | Programa principal interactivo                           |

## Ejemplo resuelto: `(a|b)*` a AFD (procedimiento manual)

### Paso 1 — Regex aumentada

La expresion regular es `(a|b)*`. Se aumenta concatenando el marcador de fin `#`:

```
(a|b)*#
```

### Paso 2 — Arbol sintactico con posiciones

Se construye el arbol sintactico y se asignan posiciones a las hojas:

```
        . (CAT)
       / \
      *   #(3)
      |
      | (OR)
     / \
   a(1) b(2)
```

Posiciones:
- Posicion 1: `a`
- Posicion 2: `b`
- Posicion 3: `#` (marcador de fin)

### Paso 3 — Calculo de nullable, firstpos, lastpos

| Nodo       | nullable | firstpos  | lastpos |
| ---------- | -------- | --------- | ------- |
| a (pos 1)  | false    | {1}       | {1}     |
| b (pos 2)  | false    | {2}       | {2}     |
| `a \| b`   | false    | {1, 2}    | {1, 2}  |
| `(a\|b)*`  | true     | {1, 2}    | {1, 2}  |
| # (pos 3)  | false    | {3}       | {3}     |
| `. (raiz)` | false    | {1, 2, 3} | {3}     |

firstpos(raiz) = firstpos(star) U firstpos(#) porque nullable(star) = true, entonces {1, 2} U {3} = {1, 2, 3}.

### Paso 4 — Calculo de followpos

**Regla CAT** (nodo raiz `.`): para cada i en lastpos(star) = {1, 2}, agregar firstpos(#) = {3}:

- followpos(1) += {3}
- followpos(2) += {3}

**Regla STAR** (nodo `*`): para cada i en lastpos(hijo) = {1, 2}, agregar firstpos(hijo) = {1, 2}:

- followpos(1) += {1, 2}
- followpos(2) += {1, 2}

Tabla followpos resultante:

| Posicion | Simbolo | followpos   |
| -------- | ------- | ----------- |
| 1        | a       | {1, 2, 3}   |
| 2        | b       | {1, 2, 3}   |
| 3        | #       | {}          |

### Paso 5 — Construccion del AFD

**Estado inicial**: firstpos(raiz) = {1, 2, 3} -> estado **A**.

Como la posicion 3 (`#`) esta en A, **A es estado de aceptacion**.

**Transiciones desde A**:

| Desde | Simbolo | Posiciones | Hacia |
| ----- | ------- | ---------- | ----- |
| A     | a       | followpos(1) = {1, 2, 3} | A |
| A     | b       | followpos(2) = {1, 2, 3} | A |

### Paso 6 — AFD resultante

```
     a, b
  +------+
  |      |
  v      |
->(A)----+
```

Un unico estado de aceptacion que reconoce cualquier cadena de `a` y `b` (incluyendo la cadena vacia), lo cual es correcto para `(a|b)*`.

### Validacion

- `""` (vacio): se queda en A (aceptacion) -> ACEPTADA (correcto, cerradura de Kleene acepta vacio)
- `"a"`: A -> A (aceptacion) -> ACEPTADA
- `"b"`: A -> A (aceptacion) -> ACEPTADA
- `"abba"`: A -> A -> A -> A -> A (aceptacion) -> ACEPTADA
- `"c"`: no hay transicion con `c` -> RECHAZADA (correcto, `c` no esta en el alfabeto)

## Referencias

- Aho, Lam, Sethi, Ullman. *Compilers: Principles, Techniques, and Tools* (2nd ed.), Seccion 3.9.5 "Construction of a DFA Directly from a Regular Expression".
- Hopcroft, J.E. "An n log n algorithm for minimizing states in a finite automaton", 1971.
- Graphviz: https://graphviz.org/
- Paquete graphviz para Python: https://pypi.org/project/graphviz/

## Licencia

Proyecto con fines academicos para la Universidad del Valle de Guatemala.
