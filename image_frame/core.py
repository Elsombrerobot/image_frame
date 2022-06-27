import os
from argparse import ArgumentTypeError, Namespace
from pathlib import Path

from PIL import Image

from config import VALID_EXT, VALID_FRAME_SHAPES, VALID_LOCATIONS
from process_image import process_image
from utils import COLORS, available_color


def validate_args(args: Namespace):
    """Validate the content and type off all args."""
    if not args.input:
        raise ValueError(
            "You need to specify one input dir, or one input file" " with --input."
        )
    if not Path(args.input).exists():
        raise ArgumentTypeError(f"{args.input} does not exists.")

    if args.frame_shape and args.frame_shape not in VALID_FRAME_SHAPES:
        raise ArgumentTypeError(
            f"-frame-shape {args.frame_shape} is not valid, it must be in :"
            f" {', '.join(VALID_FRAME_SHAPES)}"
        )

    if args.description and args.description[1] not in VALID_LOCATIONS:
        raise ArgumentTypeError(
            f"--description second arg {args.description[1]} is not valid, it"
            f" must be in : {', '.join(VALID_LOCATIONS)}"
        )

    if args.frame_size and args.frame_size <= 0:
        raise ArgumentTypeError(
            f"--frame-size {args.frame_size} is not valid, it must be superior" " to 0."
        )

    if args.font_color and args.font_color not in COLORS:
        raise ArgumentTypeError(
            f"--font-color {args.font_color} is not valid, it must be in :"
            + f"\n\n{COLORS}\n\nSee --available-colors."
        )
    if args.color and args.color not in COLORS:
        raise ArgumentTypeError(
            f"--frame-color {args.font_color} is not valid, it must be in :"
            + f"\n\n{COLORS}\n\nSee --available-colors."
        )


def main(args):

    # Print available colors and return
    if args.available_colors:
        available_color()
        return

    # Validate args
    validate_args(args)

    source = Path(args.input)
    name_format = "{name}_framed{ext}"

    # Return if invalid input
    if not source.exists():
        print(f"{source} does not exists.")
        return

    # Return if source is not a file

    if not source.is_file():
        print(f"{source} is not a file.")
        return

    if source.suffix in VALID_EXT:
        if not args.output:
            dest = source.with_name(
                name_format.format(name=source.stem, ext=source.suffix)
            )
        else:
            os.chdir(source.parent)
            filename = name_format.format(name=source.stem, ext=source.suffix)
            dest = Path(args.output.format(filename=filename)).resolve()

        dest.parent.mkdir(exist_ok=True, parents=True)
        print(f"Processing {source.name}...")
        process_image(source, dest, args)
        print(f"Saved to {dest}")
