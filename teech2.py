#! /usr/bin/python3

import sys
import argparse
import base64
import csv
import numpy as np


DELIMITER_CHAR_DEFAULT = ';'


parser = argparse.ArgumentParser(
    description='Image splitter to pars of square tiles.',
    formatter_class=argparse.RawTextHelpFormatter,
    epilog=(
        'Return samples in csv format with fields:\n'
        '   - path to original image file;\n'
        '   - size of original square tile;\n'
        '   - size of square tile of resized image;\n'
        '   - tile bitmap data of original image;\n'
        '   - tile bitmap data of resized image\n\n'
        'Tiles data represented as square bitmap matrix with 3 bytes per pixel (RGB).\n'
        'For example 64*64*3 bytes array.\n'
    ),
)
parser.add_argument(
    'infile',
    type=argparse.FileType('rb'), nargs='?', default=sys.stdin, help='Input csv stream file name (STDIN by default).')
parser.add_argument(
    '-O', dest='outfile',
    type=argparse.FileType('w'), default=sys.stdout, help='File to write output (STDOUT by default).')
parser.add_argument(
    '--delimiter', type=str, default=DELIMITER_CHAR_DEFAULT,
    help=f'CSV fields delimiter char of input data ({DELIMITER_CHAR_DEFAULT} by default)')


def tile_from_string(data: str, size: int) -> np.ndarray:
    """Load tile matrix (with dimentions [size, size, 3]) from base64 string."""
    data = base64.b64decode(data)
    arr = np.frombuffer(data, dtype=np.uint8)
    arr = arr.reshape(size, size, 3)
    arr = arr / 256
    return arr


def main(argv: list = None):
    args = parser.parse_args(argv)

    inp = csv.reader(args.infile, delimiter=args.delimiter)

    for i, (filename, size_big, size_small, tile_big, tile_small) in enumerate(inp):
        size_big = int(size_big)
        size_small = int(size_small)

        tile_big = tile_from_string(tile_big, size_big)
        tile_small = tile_from_string(tile_small, size_small)

        print(i, filename, file=args.outfile)
        # print(tile_small, file=args.outfile)
        # TODO: Make something with tiles


if __name__ == '__main__':
    main()
