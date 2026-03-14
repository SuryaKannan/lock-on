import argparse

from lock_on import DPLL, BackTracker


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("solver", choices=["backtrack", "dpll"])
    args = parser.parse_args()

    if args.solver == "backtrack":
        b = BackTracker()
        b.resolve(verbose=args.verbose)
    else:
        d = DPLL()
        d.resolve(verbose=args.verbose)


if __name__ == "__main__":
    main()
