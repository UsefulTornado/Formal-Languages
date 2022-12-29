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
<RestRHSTerm> ::= <RHSFactor> | <Eps>.
<RHSFactor> ::= <Term> | <Nterm> |
                <GroupStart> <RHS> <GroupEnd> |
                <OptionalStart> <RHS> <OptionalEnd> |
                <IterStart> <RHS> <IterEnd>.
<Nterm> ::= <Nstart> <Str> <Nend>.
```
