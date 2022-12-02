# Implementation of the $First_k$ and $Follow_k$ sets computing.

## Usage: ```main.py [-h] [-f FILE_PATH] [-k]```

---

```-f, --file_path``` - Path to the file with context-free grammar input data.

```-k``` - Number of terminals for computing $First_k$ and $Follow_k$ sets.

---

For example, run a program with the specified file:
```
main.py -f tests/test01.txt -k 5 > output.txt
```