# RAFMATH
This is a small console application that evaluates math and boolean expressions with support for variables.

## Overview
The application has a basic command line interface that the user interacts with, it supports most of the math/boolean expression logic that the Python console does, it even supports the use of variables.

## Implementation details
The application is consisted of a lexer and an interpreter. The interpreter evaluates complex expressions by recursively calling functions in the order dictated by operator precedence. The lexer parses the input string into appropriate tokens which are then provided to the appropriate interpreter functions which use them for calculations and evaluations. 

A token represents a part of the input string that has a certain semantic value, so we assign a corresponding type to it which the interpreter later uses to determine what to do next.

For an example if the lexer detects a sequence of characters in the input string that represents a whole number it will make a token with the value of the detected number and assign an INTEGER type to it.

## Supported operations:
* Addition / subtraction (+, -)
* Multiplication / division (*, /)
* Exponent (POW) / Square root (SQRT)
* Comparisons (>, <, >=, <=, ==, !=)
* Trigonometry functions (SIN, COS, TAN, CTG)
* Variable declaration and use in expressions

## Console interaction example:
\>>>c = POW(2, (57 - 54) * 2)<br>
64<br>
\>>>a = COS(TAN(450)) < c<br>
True<br>

## Sidenote
This project was an assignment as part of the course - Program interpreters/compilers in the 3rd year at the Faculty of Computer Science in Belgrade.

## Contributors
- Stefan Ginic - <stefangwars@gmail.com>
