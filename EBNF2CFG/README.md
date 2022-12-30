# Transforming grammar in custom EBNF syntax to CFG

## Grammar:

```bnf
<Grammar> ::= <Rules>.
<Rules> ::= <Rule> <RestRules>.
<RestRules> ::= <Sep> <Rule> <RestRules> | .
<Rule> ::= <Nterm> <Assignment> <RHS>.
<RHS> ::= <RHSTerm> <RestRHS>.
<RestRHS> ::= <Alt> <RHSTerm> <RestRHS> | .
<RHSTerm> ::= <RHSFactor> <RestRHSTerm>.
<RestRHSTerm> ::= <Concat> <RHSFactor> <RestRHSTerm> | .
<RHSFactor> ::= <Eps> | <Term> | <Nterm> | <Group> | <Optional> | <Iter>.
<Nterm> ::= <Nstart> <Str> <Nend>.
<Group> ::= <GroupStart> <RHS> <GroupEnd>.
<Optional> ::= <OptionalStart> <RHS> <OptionalEnd>.
<Iter> ::= <IterStart> <RHS> <IterEnd>.
```
