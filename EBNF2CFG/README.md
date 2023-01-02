# Transforming grammar in custom EBNF syntax to CFG

This program converts a grammar in EBNF with tokens that can be configured into a context-free grammar with a custom syntax

## Input data
The program requires 3 files:
* **syntax.json** - file with custom tokens for grammar in EBNF;
* **cfg_syntax.json** - file with custom tokens for output CFG;
* **grammar.txt** - file with grammar in EBNF.

For this, new files can be added or files with default values can be used.

## Grammar for EBNF:

```
<Grammar> ::= <Rules>.

<Rules> ::= <Rule> <RestRules>.
<RestRules> ::= <Sep> <Rule> <RestRules> | .

<Rule> ::= <Nterm> <Assignment> <RHS>.

<RHS> ::= <RHSTerm> <RestRHS>.
<RestRHS> ::= <Alt> <RHSTerm> <RestRHS> | .

<RHSTerm> ::= <RHSFactor> <RestRHSTerm>.
<RestRHSTerm> ::= <Concat> <RHSFactor> <RestRHSTerm> | .

<RHSFactor> ::= <Empty> | <Term> | <Nterm> | <Group> | <Optional> | <Iter>.

<Nterm> ::= <Nstart> <NtermStr> <Nend>.
<Group> ::= <GroupStart> <RHS> <GroupEnd>.
<Optional> ::= <OptionalStart> <RHS> <OptionalEnd>.
<Iter> ::= <IterStart> <RHS> <IterEnd>.
```
Tokens for `<Sep>`, `<Assignment>`, `<Alt>`, `<Concat>`, `Empty`, `Term`, `<NtermStr>`, `<GroupStart>`, `<GroupEnd>`, `<OptionalStart>`, `<OptionalEnd>`, `<IterStart>`, `<IterEnd>` are configured in `syntax.json` file.

## Output data

The program returns a context-free grammar in custom syntax. Tokens to configure can be found in the `cfg_syntax.json` file.

## Running the program

`main.py [-h] [-s syntax] [-g grammar] [sc --syntax_cfg]`

`-s, --syntax` - path to the file with custom syntax.

`-g, --grammar` - path to the file with grammar in custom EBNF syntax.

`-sc, --syntax_cfg` - path to the file with grammar in custom CFG syntax.

For example, run the program with default files:
```
main.py -s syntax.json -g grammar.txt -sc cfg_syntax.json > output.txt
```