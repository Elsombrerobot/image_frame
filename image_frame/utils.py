from PIL import ExifTags, Image, ImageColor

COLORS = [name for name, _ in ImageColor.colormap.items()]


def available_color():
    """Print all the available colors for the color arg."""
    for name, code in ImageColor.colormap.items():
        print(f"{name:20} : {code}")


def image_orientation(img: Image):
    """Get the orienation of an image."""
    return "portrait" if img.size[0] < img.size[1] else "landscape"


def average_color(img: Image):
    """Get the average color of an image as hexadecimal value."""
    result = img.copy().resize((1, 1)).getpixel((0, 0))
    return "#{:02x}{:02x}{:02x}".format(*result)
