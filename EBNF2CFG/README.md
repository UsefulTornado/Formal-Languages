# Transforming grammar in custom EBNF syntax to CFG

## Grammar:

```bnf
<Grammar> ::= <Rules>.
<Rules> ::= <Rule> <RestRules>.
<RestRules> ::= <Sep> <Rule> <RestRules> | <Eps>.
<Rule> ::= <Nterm> <Assignment> <RHS>.
<RHS> ::= <RHSTerm> <RestRHS>.
<RestRHS> ::= <Alt> <RHSTerm> <RestRHS> | <Eps>.
<RHSTerm> ::= <RHSFactor> <RestRHSTerm>.
<RestRHSTerm> ::= <Concat> <RHSFactor> <RestRHSTerm> | <Eps>.
<RHSFactor> ::= <Term> | <Nterm> | <Group> | <Optional> | <Iter>.
<Nterm> ::= <Nstart> <Str> <Nend>.
<Group> ::= <GroupStart> <RHS> <GroupEnd>.
<Optional> ::= <OptionalStart> <RHS> <OptionalEnd>.
<Iter> ::= <IterStart> <RHS> <IterEnd>.
```
