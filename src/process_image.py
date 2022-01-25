from pathlib import Path
from pprint import pprint

from PIL import ExifTags, Image, ImageDraw, ImageFont, ImageOps

from config import FONT_PATH
from utils import average_color, image_orientation


def exif_dict(filepath):
    """Dict with simple exif data.

    Parameters
    ----------
    filepath : str, Path
        The filepath of the image to analyse.

    Returns
    -------
    dict
        Data with simple exif data.
    """
    img = Image.open(filepath, "r")

    exif = {
        ExifTags.TAGS[k]: v
        for k, v in img._getexif().items()
        if k in ExifTags.TAGS
    }

    # Exposure time
    if exif["ExposureTime"] < 1:
        exposure = f"1/{int(1/exif['ExposureTime'])}"
    else:
        exposure = f"1/{int(exif['ExposureTime']/1)}"

    # Model
    model = exif["Model"].lower()

    # Iso
    iso = f"iso {exif['ISOSpeedRatings']}"

    # Focal length
    focal_length = f"{exif['FocalLengthIn35mmFilm']} mm"

    # fstop
    if float(exif["FNumber"]).is_integer():
        fstop = f"f/{int(exif['FNumber'])}"
    else:
        fstop = f"f/{exif['FNumber']}"

    return {
        "exposure": exposure,
        "model": model,
        "iso": iso,
        "f_number": fstop,
        "focal_length": focal_length,
    }


def resize_img(img: Image, img_size):
    """
    Resize an image to the given size.

    Return
    ------
    Image
    """
    img = ImageOps.contain(img, (img_size, img_size), method=Image.LANCZOS)
    return img


def add_frame(img: Image, color, size, shape, acrylic=False):
    """Add a frame with the given pixel size, color, and shape.

    Parameters
    ----------
    img : Image
        Input image.
    color : str
        The color of the frame.
    size : int
        The size of the frame in px.
    shape : str
        The shape of the frame. Values : same, square.
    catrylic : Bool
        Use a blurred version of the image for the frame.

    Return
    ------
    Image
    """
    frame_color = average_color(img) if color == "median" else color

    if shape == "same":
        border = size
    elif shape == "square":
        square_size = round((max(img.size) + size * 2 - min(img.size)) / 2)

        if image_orientation(img) == "portrait":
            border = (square_size, size, square_size, size)
        else:
            border = (size, square_size, size, square_size)

    img = ImageOps.expand(img, border=border, fill=frame_color)

    return img


def tag_text(
    img: Image,
    text,
    location,
    font_size,
    font_color,
):

    font = ImageFont.truetype(str(FONT_PATH), round(font_size))
    fw, fh = font.getsize(text)

    if location == "top":
        offset = (
            round((img.size[0] / 2) - fw / 2),
            round(fh / 3),
        )
    elif location == "bottom":
        offset = (
            round((img.size[0] / 2) - fw / 2),
            round(img.size[1] - fh - fh / 2),
        )

    draw = ImageDraw.Draw(img)
    text = text.strip("'")
    draw.text(offset, text, font=font, fill=font_color)
    return img


def tag_exifs(
    img: Image, img_path, location, font_size, font_color, border_size
):
    """Add an exifs inscription in the frame at given location."""
    exifs = exif_dict(img_path)
    exif_stamp = (
        exifs["model"]
        + " "
        + exifs["focal_length"]
        + " "
        + exifs["f_number"]
        + " "
        + exifs["exposure"]
        + " "
        + exifs["iso"]
    ).lower()
    return tag_text(img, exif_stamp, location, font_size, font_color)


def process_image(source: Path, dest: Path, args):
    """Process the file given args."""
    img = Image.open(source)

    # Add frame to the image
    percentaged_border_size = round((max(img.size) / 100) * args.frame_size)
    img = add_frame(img, args.color, percentaged_border_size, args.frame_shape)

    # Resize the image
    if args.size:
        img = resize_img(img, args.size)

    # Generate font tsize if not specified
    font_size = round((max(img.size) / 35) * args.font_size_weight)

    # Add exifs inscription to the image
    if args.exif_loc:
        try:
            img = tag_exifs(
                img,
                source,
                args.exif_loc,
                font_size,
                args.font_color,
                percentaged_border_size,
            )
        except AttributeError:
            print("Error while tagging exifs, skipping exif tag.")

    # Add custom text inscription to the image
    if args.description:

        img = tag_text(
            img,
            args.description[0],
            args.description[1],
            font_size,
            args.font_color,
        )

    img.save(dest)
