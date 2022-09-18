import sys
from termination import check_termination


def main():
    res, order = check_termination(sys.argv[1])
    print(res)
    if res:
        print(order)

if __name__ == "__main__":
    main()
