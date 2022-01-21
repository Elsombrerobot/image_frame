from pathlib import Path

"""Configure global variable for the app."""

RESSOURCES = Path(__file__).parents[1] / "resources"
FONT_PATH = RESSOURCES / "CutiveMonoRegular.ttf"
VALID_EXT = [".jpg", ".png", ".jpeg"]
