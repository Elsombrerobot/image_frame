import os
from argparse import Namespace
from pathlib import Path
import sys


from image_frame.config import VALID_EXT, VALID_FRAME_SHAPES, VALID_LOCATIONS
from image_frame.process_image import process_image
from image_frame.utils import COLORS, available_color


def validate_args(args: Namespace):
    """Validate the content and type off all args."""
    if not args.input:
        print("You need to specify one input dir, or one input file" " with --input.")
        return False
    if not Path(args.input).exists():
        print(f"{args.input} does not exists.")
        return False
    if args.frame_shape and args.frame_shape not in VALID_FRAME_SHAPES:
        print(
            f"-frame-shape {args.frame_shape} is not valid, it must be in :"
            f" {', '.join(VALID_FRAME_SHAPES)}"
        )
        return False
    if args.description and args.description[1] not in VALID_LOCATIONS:
        print(
            f"--description second arg {args.description[1]} is not valid, it"
            f" must be in : {', '.join(VALID_LOCATIONS)}"
        )
        return False
    if args.frame_size and args.frame_size <= 0:
        print(
            f"--frame-size {args.frame_size} is not valid, it must be superior" " to 0."
        )
        return False
    if args.font_color and args.font_color not in COLORS:
        print(
            f"--font-color {args.font_color} is not valid, it must be in :"
            + f"\n\n{COLORS}\n\nSee --available-colors."
        )
        return False
    if args.color and args.color not in COLORS:
        print(
            f"--frame-color {args.font_color} is not valid, it must be in :"
            + f"\n\n{COLORS}\n\nSee --available-colors."
        )
        return False

    # Return if invalid input
    source = Path(args.input).resolve()
    if not source.exists():
        print(f"{source} does not exists.")
        return False
    return True


def prepare_files(source, output=None):
    """Iterate over files to process."""
    source = Path(source)
    output = Path(output) if output else None
    if source.is_file():
        if output:
            if output.is_dir():
                dest = output / f"{source.stem}_framed{source.suffix}"
                yield source, dest
            else:
                yield source, output
        else:
            dest = source.with_name(f"{source.stem}_framed{source.suffix}")
            yield source, dest

    elif source.is_dir():
        sources = []
        for ext in VALID_EXT:
            sources.extend(list(source.glob(f"*.{ext}")))

        if not output:
            for s in sources:
                dest = source.with_name(f"{s.stem}_framed{s.suffix}")
                yield s, dest

        elif output.exists() and output.is_dir():
            for s in sources:
                dest = output / f"{s.stem}_framed{s.suffix}"
                yield s, dest
        else:
            for s in sources:
                dest = output / f"{s.stem}_framed{s.suffix}"
                yield s, dest


def main(args):

    # Print available colors and return
    if args.available_colors:
        available_color()
        return

    # Validate args
    if not validate_args(args):
        sys.exit()

    for source, dest in prepare_files(args.input, args.output):
        dest.parent.mkdir(exist_ok=True, parents=True)
        print(f"Processing {source.name}...")
        process_image(source, dest, args)
        print(f"Saved to {dest}")
