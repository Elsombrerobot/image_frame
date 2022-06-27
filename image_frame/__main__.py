import argparse

from config import VALID_FRAME_SHAPES, VALID_LOCATIONS

parser = argparse.ArgumentParser(
    description="Frame images . Work only with jpeg and png.",
    usage="image_frame [options], use @file.txt for text file arguments.",
    epilog="Mainly used for instagram.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    fromfile_prefix_chars="@",
)

parser.add_argument(
    "-i",
    "--input",
    dest="input",
    type=str,
    help="The input to process. If is dir, will process all the jpegs.",
)

parser.add_argument(
    "-o",
    "--output",
    dest="output",
    type=str,
    help="TODO",
)

parser.add_argument(
    "-s",
    "--size",
    dest="size",
    type=int,
    default=0,
    help=(
        "Specify the size of the final image, if not specified, original size"
        " is kept and the program just add the frame, so it will be bigger."
    ),
)

parser.add_argument(
    "-fs",
    "--frame-size",
    dest="frame_size",
    type=float,
    default="5",
    help=(
        "Specify the size of the frame, as precentage of the greater size of"
        " the image."
    ),
)

parser.add_argument(
    "-fsh",
    "--frame-shape",
    dest="frame_shape",
    default="same",
    type=str,
    help="Specify the shape of the frame. Values : same, square.",
    choices=VALID_FRAME_SHAPES,
)

parser.add_argument(
    "-fc",
    "--frame-color",
    dest="color",
    type=str,
    default="white",
    help=(
        "Specify the color of the frame. Values : median (see -ac,"
        " --available_colors for all colors) (to implement : acrylic)."
    ),
)

parser.add_argument(
    "-te",
    "--tag-exifs",
    dest="exif_loc",
    type=str,
    help=(
        "Tag the frame with exif tag at the given location if one location arg"
        " is specified. Values : top, bottom"
    ),
    choices=VALID_LOCATIONS,
)

parser.add_argument(
    "-d",
    "--description",
    dest="description",
    nargs=2,
    type=str,
    help=(
        "Tag the frame with given string at the given location if one location"
        " arg is specified. Locations : top, bottom. Take 2 args, exemple : -d"
        " 'Cool description' bottom"
    ),
)

parser.add_argument(
    "-ftw",
    "--font-size-weight",
    dest="font_size_weight",
    default=1,
    type=float,
    help="Specify the multiplier for the font size.",
)

parser.add_argument(
    "-fco",
    "--font-color",
    dest="font_color",
    default="black",
    type=str,
    help="Specify the color of the font.",
)

parser.add_argument(
    "-ac",
    "--available-colors",
    dest="available_colors",
    action="store_true",
    help=(
        "Print all the available color options for --frame_color and"
        " --font-color, skip any other arg."
    ),
)

if __name__ == "__main__":
    from core import main

    args = parser.parse_args()
    main(args)
