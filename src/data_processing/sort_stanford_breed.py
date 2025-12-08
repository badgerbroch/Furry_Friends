import shutil
from pathlib import Path

from src.constants import DREW_ROOT_PATH

DATA_ROOT = Path.home() / "Downloads" / "stanford_dataset" / "Images"


OUT_DIR = DREW_ROOT_PATH / "pets_breeds"

breed_dirs = list(DATA_ROOT.iterdir())

# create dictionary of all current breed names and paths to add stanford set to
curr_breed_names = {}
for breed in list(OUT_DIR.iterdir()):
    #print(breed.name)
    curr_breed_names[(breed.name).lower()] = breed

for breed_dir in breed_dirs:
    # print(breed_dir)
    breed_dir = Path(breed_dir)
    breed_name = ((breed_dir.name).split("-")[1]).lower()
    if breed_name in curr_breed_names:
        #print(breed_name)
        for image in breed_dir.iterdir():
            #print(image)
            image_name = image.name
            print(image_name)
            dst = OUT_DIR / breed_name / image_name
            
            shutil.copy2(image, dst)
    else:
        for image in breed_dir.iterdir():
            dst_folder = OUT_DIR / breed_name
            dst_folder.mkdir(exist_ok=True, parents=True)
            dst_path = dst_folder / image.name
            shutil.copy2(image, dst_path)