# Termination of Term Rewriting Systems

## Input data syntax
```ebnf
'lexicographic' | 'anti-lexicographic';
'constructors = ' {Character '(' NaturalNumber '),'} Character '(' NaturalNumber ')';
'variables = ' {Character ','} Character;
Term '=' Term {'\n' Term '=' Term};
```
Where
```ebnf
Term = variable | constructor '(' {Term ','} Term ')'.
```
* variable and constructor are characters from the input `variables` and `constructors` respectively;
* sets of variables and constructors names are disjoint;

## Output data
Program prints `True` and constructors precedence which leads to TRS termination if the specifed TRS is terminating and `False` otherwise.

> NB: The lexicographic order method can only determine whether the TRS is terminating. If this method gives a negative result, further research using other methods is required.

## Example of the correct input data:
```
lexicographic
constructors = a(2), s(1)
variables = x, y
a(x, y) = y
a(s(x), y) = s(a(x, y))
```

## Output for the example above:
```
True
a > s
```

## Running the program
```main.py [file_path]```

For example, run a program with the specified file:
```
main.py tests/test1.txt > output.txt
```