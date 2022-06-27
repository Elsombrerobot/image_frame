"""Configure global variable for the app."""

from pathlib import Path


RESSOURCES = Path(__file__).parents[1] / "resources"
FONT_PATH = RESSOURCES / "CutiveMonoRegular.ttf"
VALID_EXT = ["jpg", "png", "jpeg"]
VALID_EXT.extend([ext.upper() for ext in VALID_EXT])
VALID_FRAME_SHAPES = ["same", "square"]
VALID_LOCATIONS = ["bottom", "top"]
