import os
from pathlib import Path

from PIL import Image

from config import VALID_EXT
from process_image import process_image
from utils import available_color


def main(args):

    # Print available colors and return
    if args.available_colors:
        available_color()
        return

    source = Path(args.input)
    name_format = "{name}_framed{ext}"

    # Return if invalid input
    if not source.exists():
        print(f"{source} does not exists.")
        return

    # Format destination path
    if source.is_dir():
        for f in list(source.iterdir()):
            if f.suffix in VALID_EXT:
                if not args.output:
                    dest = source / name_format.format(
                        name=f.stem, ext=f.suffix
                    )
                else:
                    os.chdir(source)
                    filename = name_format.format(name=f.stem, ext=f.suffix)
                    dest = Path(
                        args.output.format(filename=filename)
                    ).resolve()

                if dest.is_dir():
                    dest = dest / name_format.format(name=f.stem, ext=f.suffix)

                dest.parent.mkdir(exist_ok=True, parents=True)
                print(f"Processing {f.name}...")
                process_image(f, dest, args)
                print(f"Saved to {dest}")

    elif source.is_file():
        if source.suffix in VALID_EXT:
            if not args.output:
                dest = source.with_name(
                    name_format.format(name=source.stem, ext=source.suffix)
                )
            else:
                os.chdir(source.parent)
                filename = name_format.format(
                    name=source.stem, ext=source.suffix
                )
                dest = Path(args.output.format(filename=filename)).resolve()

            if dest.is_dir():
                dest = dest / name_format.format(
                    name=source.stem, ext=source.suffix
                )
            dest.parent.mkdir(exist_ok=True, parents=True)
            print(f"Processing {source.name}...")
            process_image(source, dest, args)
            print(f"Saved to {dest}")
