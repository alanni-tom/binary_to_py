#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/9/9 13:15
# @Author  : Alanni
import argparse

from binary_to_pyc import main

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Python binary rebuilding to py.")
    parser.add_argument('-f', '--file', help='python binary file', required=True)
    parser.add_argument('-o', '--output', help='output file', required=True)
    args = parser.parse_args()

    main(args.file, args.output)
