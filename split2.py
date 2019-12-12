#! /usr/bin/python3

import argparse
import sys
from PIL import Image as pil_image
import typing
import base64


RESIZE_METHODS = {
    'NEAREST': 0,
    'NONE': 0,
    'FLOYDSTEINBERG': 3,
}

TILE_SIZE_DEFAULT_BIG = 64
TILE_SIZE_DEFAULT_SMALL = 32
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
    type=argparse.FileType('rb'), nargs='?', default=sys.stdin, help='Input image file name (STDIN by default).')
parser.add_argument(
    '-O', dest='outfile',
    type=argparse.FileType('w'), default=sys.stdout, help='File to write output (STDOUT by default).')
parser.add_argument(
    '--delimiter', type=str, default=DELIMITER_CHAR_DEFAULT,
    help=f'CSV fields delimiter char of output data ({DELIMITER_CHAR_DEFAULT} by default)')
parser.add_argument(
    '--big-size', dest='big_size', type=int, default=TILE_SIZE_DEFAULT_BIG,
    help=f'Big tiles size ({TILE_SIZE_DEFAULT_BIG} by default)')
parser.add_argument(
    '--small-size', dest='small_size', type=int, default=TILE_SIZE_DEFAULT_SMALL,
    help=f'Resized tiles size ({TILE_SIZE_DEFAULT_SMALL} by default)')
parser.add_argument(
    '--resize-method', dest='resize_method', type=str, default='NEAREST',
    help='Resize method: NEAREST (by default), FLOYDSTEINBERG')


def split_to_tiles(image: pil_image.Image, tile_size: int) -> typing.Generator[pil_image.Image, None, None]:
    w, h = image.size
    for i in range(h // tile_size):
        for j in range(w // tile_size):
            x, y = j * tile_size, i * tile_size
            yield image.crop((x, y, x + tile_size, y + tile_size))


def to_string(data: bytes) -> str:
    return base64.b64encode(data).decode('ascii')


def main(argv: list = None):
    args = parser.parse_args(argv)
    resize_method = RESIZE_METHODS.get(args.resize_method.upper(), None)
    assert resize_method is not None, f'Wrong resize method: {args.resize_method}'

    img = pil_image.open(args.infile)
    original_image_size = img.size
    k = args.big_size / args.small_size
    resized_image_size = tuple(int(v // k) for v in original_image_size)
    img_small = img.resize(resized_image_size, resample=resize_method)

    for orig_tile, small_tile in zip(
        split_to_tiles(img, args.big_size),
        split_to_tiles(img_small, args.small_size)
    ):
        line = (
            f'{args.infile.name}{args.delimiter}'
            f'{args.big_size}{args.delimiter}'
            f'{args.small_size}{args.delimiter}'
            f'{to_string(orig_tile.tobytes())}{args.delimiter}'
            f'{to_string(small_tile.tobytes())}\n'
        )
        try:
            args.outfile.write(line)
        except BrokenPipeError:
            sys.exit(1)


if __name__ == '__main__':
    main()
