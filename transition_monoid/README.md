# Building a transition monoid

## Input data syntax
Input data is a deterministic finite automaton.

First line of the input is a tuple with an initial state and a set of final states. Next, the transition rules of the DFA are entered.
```ebnf
FirstLine = '<' State ', {' State {', ' State} '}>';
Transition = '<' State ', ' Letter '> -> ' State.
```
Where
```re
State ::= [A-Z][0-9]?;
Letter ::= [a-z].
```

### Example of the correct input data:
```
<Q0, {Q0, Q1, Q3}>
<Q0, a> -> Q1
<Q0, b> -> Q3
<Q1, a> -> Q1
<Q1, b> -> Q2
<Q2, a> -> Q1
<Q2, b> -> Q2
<Q3, a> -> Q4
<Q3, b> -> Q3
<Q4, a> -> Q4
<Q4, b> -> Q3
```

## Output data
Program returns:
* a list of the transformation monoid rewriting rules and it's equivalence classes;
* equivalence classes that are accepted by the DFA;
* for each class $w$:
  * Equivalence classes $v$ such that DFA accepts $vw$;
  * Equivalence classes $u$ such that DFA accepts $wu$;
  * Equivalence classes $v$ and $u$ such that DFA accepts $vwu$;
  * the state to which $w$ synchronizes the DFA or the message that $w$ is not synchronizing.

Optionally, the DFA can be tested for minimality and, if it's minimal, information about Myhill-Nerode equivalence classes will be extracted from the monoid (with a list of representatives of these classes and suffixes that distinguish them, in the form of a table).

## Running the program
```main.py [-h] [-f file_path] [-mn]```

```-f, --file_path``` - path to the file with DFA input data.

```-f, --file_path``` - whether to print information about Myhill-Nerode equivalence classes.

For example, run a program with the specified file:
```
main.py -f tests/test01.txt > output.txt
```

Or run a program with printing information about Myhill-Nerode equivalence classes in the form of a table:
```
main.py -f tests/test01.txt -mn > output.txt
```
