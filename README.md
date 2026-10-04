# Nexion

Nexion is an experimental programming language built from scratch in Python.

It is currently focused on developing a complete programming-language core with simple syntax, clear semantics, and an interpreter-based execution model.

## About

Nexion is built using a traditional language pipeline:

**Source Code → Lexer → Parser → AST → Interpreter**

The language is being developed from scratch rather than relying on an existing parser or interpreter framework.

## Current Features

- Variables
- Variable reassignment
- Numbers
- Strings
- Booleans
- "none"
- Arithmetic operators
- Operator precedence
- Comparisons
- Unary "not"
- Unary minus
- "and" / "or"
- "if" / "else-if" / "else"
- "while" loops
- "next"
- "exit"
- Blocks and nested scopes
- Functions
- Function parameters
- Function calls
- Nested function calls
- Recursive functions
- Return statements
- Global and local variable access

## Example
``` Nexion
fun factorial(n) {
    if (n <= 1) { 
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}


say(factorial(5));
```
**Output:**
```code
120
```
## Architecture

Nexion currently consists of four main stages:

### Lexer

Converts source code into tokens.

### Parser

Converts tokens into an Abstract Syntax Tree (AST).

### AST

Represents the structure of the Nexion program.

### Interpreter

Evaluates the AST and executes the program.

## Built With

- Python
- Python standard library

The core lexer, parser, AST, and interpreter are implemented from scratch.

## Project Status

Nexion is actively under development.

The current focus is expanding and stabilizing the core language before moving toward higher-level features.

## Future Direction

The long-term goal is to explore Nexion as a programming language designed with data analysis in mind.

Planned areas include:

- Collections and data structures
- File I/O
- Modules and imports
- Error handling
- Standard library
- Data processing
- Data inspection and cleaning
- Data analysis workflows
- Visualization
- Data provenance and explainability

## License

This project is currently experimental and under active development.

