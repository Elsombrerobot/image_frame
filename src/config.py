from pathlib import Path

"""Configure global variable for the app."""

RESSOURCES = Path(__file__).parents[1] / "resources"
FONT_PATH = RESSOURCES / "CutiveMonoRegular.ttf"
VALID_EXT = [".jpg", ".png", ".jpeg"]
VALID_EXT.append([ext.upper() for ext in VALID_EXT])
VALID_FRAME_SHAPES = ["same", "square"]
VALID_LOCATIONS = ["bottom", "top"]
