import argparse

from lock_on.backtracker import BackTracker
from lock_on.pubgrub import PubGrub


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("solver", choices=["backtrack", "pubgrub"])
    args = parser.parse_args()

    if args.solver == "backtrack":
        b = BackTracker()
        b.resolve(verbose=args.verbose)
    else:
        p = PubGrub()
        p.resolve(verbose=args.verbose)


if __name__ == "__main__":
    main()
