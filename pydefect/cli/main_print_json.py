# -*- coding: utf-8 -*-
#  Copyright (c) 2020 Kumagai group.
import sys

from monty.serialization import loadfn


def main():
    if sys.argv[1] == "repr":
        filenames = sys.argv[2:]
        use_repr = True
    else:
        filenames = sys.argv[1:]
        use_repr = False

    for filename in filenames:
        print("-"*80)
        print(f"file: {filename}")
        obj = loadfn(filename)
        print(obj.__repr__()) if use_repr else print(obj.__str__())


if __name__ == "__main__":
    main()
