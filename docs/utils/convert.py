import subprocess
import os
import sys
import itertools


def iterate_tex(doc_root):
    for root, dirnames, filenames in os.walk(doc_root):
        for filename in filenames:
            if filename.endswith('.tex'):
                tex_path = os.path.join(root, filename)
                rst_path = tex_path[:-4] + '.rst'
                yield tex_path, rst_path


def generate_rst_from_tex(tex_path, rst_path):
    with open(rst_path, 'w') as rst:
        print('Writing to {}'.format(rst_path))
        return subprocess.run([
            'pandoc',
            '--from', 'latex',
            '--to', 'rst',
            tex_path,
        ], stdout=rst)


def generate_rst(doc_root):
    for result in itertools.starmap(
        generate_rst_from_tex,
        iterate_tex(doc_root)
    ):
        print(result)


def main():
    doc_root = os.path.abspath(sys.argv[1])
    generate_rst(doc_root)


if __name__ == '__main__':
    main()

