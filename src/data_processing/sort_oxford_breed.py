import shutil
from pathlib import Path

from src.constants import DREW_ROOT_PATH

DATA_ROOT = Path.home() / "Downloads" / "oxford_images" / "images"

OUT_DIR = DREW_ROOT_PATH / "pets_breeds"

CAT_DIR = OUT_DIR / "cat"
DOG_DIR = OUT_DIR / "dog"

CAT_DIR.mkdir(parents=True, exist_ok=True)
DOG_DIR.mkdir(parents=True, exist_ok=True)


for img_path in DATA_ROOT.glob("*.jpg"):
    stem = img_path.stem
    breed_part = stem.split("_")[0]
    first_char = breed_part[0]
    breed_dir = OUT_DIR / breed_part
    breed_dir.mkdir(parents=True, exist_ok=True)
    
    dst = breed_dir / img_path.name
    shutil.copy2(img_path, dst)
    print(stem + "  " + breed_dir.name)
    

print(f"Output in: {OUT_DIR.resolve()}")