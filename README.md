# Formal-Languages

> Based on this [Formal Languages Theory course](https://github.com/TonitaN/FormalLanguageTheory) materials.

# 1. Termination of Term Rewriting Systems.

## Term Rewriting systems
Informally, a term rewriting system (TRS) is a set of rules that show how terms from the left-hand side can be rewritten in terms from the right-hand side.

### **Formal definition**
Let $V$ be the *variables* set and $F$ be the *constructors* set; $T(F)$ is a set of *terms* over the constructors set. Then $TRS$ could be defined as a set of rewriting rules, written $\Phi_i \rightarrow \Psi_i$, where $\Phi_i$ and $\Psi_i$ are terms from $T(F)$.

A rewriting rule $\Phi_i \rightarrow \Psi_i$ can be applied to a term $t$ if the left term $\Phi_i$ matches some subterm of $t$.

### **Termination**
A relation $\rightarrow$ is **well-founded** iff there is no infinite set $\{t_0, t_1, t_2, ...\}$ with $t_0 \rightarrow t_1 \rightarrow t_2 \rightarrow ...$

A TRS $\{l_i \rightarrow r_i\}$ is **terminating** iff term rewriting relation $\rightarrow$ is well-founded.

### **Termination analysis**
In this case, only the method with lexicographic ordering over the $F$ will be considered.

#### **Lexicographic order $>_{lo}$**
$f(t_1, ..., t_n) >_{lo} g(u_1, ..., u_m)$ iff one of the conditions below is met:

1. $\exists i \space (1 \le i \le n \space \And \space t_i = g(u_1, ..., u_m))$;
2. $\exists i \space (1 \le i \le n \space \And \space t_i >_{lo} g(u_1, ..., u_m))$;
3. $(f > g) \space \And \space \forall i \space (1 \le i \le m \Rightarrow f(t_1, ..., t_n) >_{lo} u_i)$;
4. $(f = g) \space \And \space \forall i \space (1 \le i \le m \Rightarrow f(t_1, ..., t_n) >_{lo} u_i)$ and $(t_1, ..., t_n)$ is lexicographic greater than $(u_1, ..., u_m)$.

If all the rewriting rules of the TRS satisfy the lexicographic order with some constructors precedence, TRS is terminating.

The lexicographic ordering method can only determine whether the TRS is terminating. If this method gives a negative result, further research using other methods is required.

> See the implementation of this approach in [TRS_termination](./TRS_termination/) folder.

# 2. Building a transition monoid.
Information: coming soon
