#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from pysubs3.cli import Pysubs3CLI

if __name__ == "__main__":
    cli = Pysubs3CLI()
    rv = cli(sys.argv[1:])
    sys.exit(rv)
