import os
import sys


def iterate_rst(doc_root):
    for root, dirnames, filenames in os.walk(doc_root):
        for filename in filenames:
            if filename.endswith('.rst'):
                path = os.path.join(root, filename)
                yield path


def apply_pandoc(doc_root):
    for path in iterate_rst()


def main():
    doc_root = sys.argv[1]


if __name__ == '__main__':
    main()

