# Python-to-RISC-V Custom Compiler

## Overview
A fully custom, multi-pass compiler built entirely in Python that translates a high-level, custom programming language (`.cpy`) into executable RISC-V assembly code (`.asm`). The project encompasses the entire compilation pipeline, from raw source code parsing to intermediate representation, scope management, and final machine-level code generation tailored for the RARS simulator.

This project was built to demonstrate a deep understanding of computer science fundamentals, including finite state automata, recursive-descent parsing, intermediate code backpatching, and stack-based memory management.

## Architecture & Compilation Pipeline

* **Lexical Analysis (`Lex`):** Implements a custom Deterministic Finite Automaton (DFA) to tokenize source code. It recognizes language-specific keywords (`main`, `def`, `#int`, `global`, etc.) and handles strict error validation (e.g., out-of-bounds integers, identifiers exceeding 30 characters).
* **Syntax Analysis (`SyntaxAnalyzer`):** A recursive-descent parser that evaluates the syntactic structure of the token stream. It handles nested control flow (`if`, `elif`, `else`, `while`) and complex arithmetic/logical expressions respecting operator precedence.
* **Intermediate Code Generation (`IntermediateCode`):** Translates parsed syntax into Three-Address Code (Quads). Utilizes list-merging and backpatching algorithms to resolve unknown jump addresses for loops and boolean evaluations.
* **Symbol Table (`Table`, `Scope`, `Entity`):** Dynamically tracks variable lifecycles, global definitions, and nested function parameters. It calculates precise memory offsets (4 bytes per entity) for accurate stack frame allocation.
* **Final Code Generation (`FinalCode`):** Maps intermediate quads into standard RISC-V assembly. Manages the call stack, utilizing the stack pointer (`sp`), frame pointer (`fp`), and global pointer (`gp`), along with system calls (`ecall`) for I/O operations.

## Language Syntax

The custom `.cpy` language shares similarities with Python but features distinct block declarations using `#{ ... }#` and explicit typing for globals and integers. 

### Quick Start Example: `factorial.cpy`
```python
## Calculates the factorial of a user-input number ##

def factorial(n):
#{  
    if n == 0 or n == 1:
        return 1
    else:
         return n*factorial(n - 1)
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
