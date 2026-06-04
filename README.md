# CutePy-to-RISC-V Custom Compiler

## Overview
A fully custom, multi-pass compiler built entirely in Python that translates a high-level educational programming language called **CutePy** (`.cpy`) into executable RISC-V assembly code (`.asm`). 

This project encompasses the entire compilation pipeline—from raw source code parsing to intermediate representation, scope management, and final machine-level code generation tailored for the RARS simulator. It was built to demonstrate a deep understanding of computer science fundamentals, including finite state automata, recursive-descent parsing based on EBNF grammars, intermediate code backpatching, and stack-based memory management.

## Lexical & Syntactic Rules
[cite_start]CutePy is heavily inspired by Python but features unique syntax requirements, strict scoping, and is strictly typed (integer only)[cite: 1669, 1673, 1728, 2041, 2067]. The compiler enforces the following language specifications:

* [cite_start]**Lexical Constraints:** Identifiers are limited to 30 characters[cite: 1698, 2063]. [cite_start]The language only supports integer data types within a strict 16-bit range (`-32767` to `32767`)[cite: 2068]. 
* [cite_start]**Custom Block Syntax:** Instead of relying on indentation, code blocks for functions and control structures are enclosed in `#{` and `#}`[cite: 1691, 1759, 1760].
* [cite_start]**Declarations:** Variables must be explicitly declared using `#int` [cite: 2068] [cite_start]for local scope or `global` [cite: 2134] for global scope. [cite_start]The main program is distinctly declared with `#def main`[cite: 1635].
* [cite_start]**Functions & Scoping:** Supports nested local functions with Pascal-like scoping rules[cite: 1794, 2128]. [cite_start]Parameters are passed strictly by value[cite: 1802].
* [cite_start]**Control Flow:** Fully supports `if-elif-else` and `while` structures [cite: 2088, 2091, 2101][cite_start], relying on a recursive-descent parser to handle operator precedence (e.g., `not`, `*`, `+`, `<`, `and`, `or`)[cite: 2073, 2074, 2077, 2078, 2079, 2080].

## Architecture & Compilation Pipeline

* **Lexical Analysis (`Lex`):** Implements a custom Deterministic Finite Automaton (DFA) to tokenize the `.cpy` source code. 
* **Syntax Analysis (`SyntaxAnalyzer`):** A recursive-descent parser that evaluates the syntactic structure of the token stream against the language's formal EBNF grammar.
* **Intermediate Code Generation (`IntermediateCode`):** Translates parsed syntax into Three-Address Code (Quads). Utilizes list-merging and backpatching algorithms to resolve unknown jump addresses for loops and boolean evaluations.
* **Symbol Table (`Table`, `Scope`, `Entity`):** Dynamically tracks variable lifecycles, global definitions, and nested function parameters. It calculates precise memory offsets (4 bytes per entity) for accurate stack frame allocation.
* **Final Code Generation (`FinalCode`):** Maps intermediate quads into standard RISC-V assembly. Manages the call stack, utilizing the stack pointer (`sp`), frame pointer (`fp`), and global pointer (`gp`), along with system calls (`ecall`) for I/O operations.

## Language Syntax: `factorial.cpy`
```python
## Calculates the factorial of a user-input number ##

def factorial(n):
#{  
    if n == 0 or n == 1:
        return 1
    else:
         return n * factorial(n - 1)
#}

#def main
#int n
    
n = int(input())
print(factorial(n))
```

## Usage & Execution

### Prerequisites
* **Python 3.10+**
* **RARS** (RISC-V Assembler and Runtime Simulator) to assemble and simulate the compiled code.

### Running the Compiler
The entire compilation pipeline is executed via a single Python script. 

1. Clone the repository and run the main compiler script:
   ```bash
   python compiler.py
   ```
2. When prompted, input the name of your source file:
   ```text
   Give me the name of the file : factorial.cpy
   ```

### Outputs
Upon a successful compilation, the script generates three output files in the same directory:
1.  **`[filename].int`**: The Intermediate Code formatted as Three-Address Quads.
2.  **`[filename].sym`**: The Symbol Table dump, mapping the scope levels, datatypes, and memory offsets.
3.  **`[filename].asm`**: The Final RISC-V assembly code.

Load the generated `.asm` file into RARS, assemble, and run the program to see the executing logic and interact with the standard input/output.
