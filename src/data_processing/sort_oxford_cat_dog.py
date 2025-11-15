import shutil
from pathlib import Path

from Furry_Friends.src.constants import DREW_ROOT_PATH

DATA_ROOT = Path.home() / "Downloads" / "oxford_images" / "images"

OUT_DIR = DREW_ROOT_PATH / "pets_raw"

CAT_DIR = OUT_DIR / "cat"
DOG_DIR = OUT_DIR / "dog"

CAT_DIR.mkdir(parents=True, exist_ok=True)
DOG_DIR.mkdir(parents=True, exist_ok=True)


num_cats = 0
num_dogs = 0

for img_path in DATA_ROOT.glob("*.jpg"):
    stem = img_path.stem
    breed_part = stem.split("_")[0]
    first_char = breed_part[0]
    
    # upper case for cat and lower case for dog (first char of filename)
    if first_char.isupper():
        dst_dir = CAT_DIR
        num_cats += 1
    else:
        dst_dir = DOG_DIR
        num_dogs += 1
    dst = dst_dir / img_path.name
    shutil.copy2(img_path, dst)
    print(stem + "  " + dst_dir.name)
    

print(f"Cats: {num_cats}")
print(f"Dogs: {num_dogs}")
print(f"Output in: {OUT_DIR.resolve()}")