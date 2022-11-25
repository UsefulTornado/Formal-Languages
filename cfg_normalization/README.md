# Chomsky / Greibach normalization of a context-free grammar.

## Usage: ```main.py [-h] [-f FILE_PATH] [-cnf] [-bk] [-bs] [-v]```

---

```-f, --file_path``` - Path to the file with context-free grammar input data.

```-cnf, --chomsky``` - Whether to use Chomsky normalization. If not specified, Greibach normalization is used.

```-bk, --blum_koch``` - Whether to use Blum-Koch algorithm for Greibach normalization. If not specified, elimination of left recursion is used.

```-bs, --bisimulate``` - Whether to simplify grammar with bisimulation.

```-v, --verbose``` - Whether to print additional information.

---

For example, run a program with the specified file:
```
main.py -f tests/test01.txt -bk -bs -v > output.txt
```