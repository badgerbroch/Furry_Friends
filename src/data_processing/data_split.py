import random
from pathlib import Path
from shutil import copy2, rmtree

from src.constants import DREW_ROOT_PATH

# from constants import DREW_ROOT_PATH



def make_splits(
    raw_root: str,
    out_root: str,
    train_ratio: float = 0.7,
    val_ratio: float = 0.15,
    seed: int = 42,
):
    raw_root = Path(raw_root)
    out_root = Path(out_root)

    random.seed(seed)

    # Clean output dir
    if out_root.exists():
        rmtree(out_root)
    for split in ["train", "val", "test"]:
        (out_root / split).mkdir(parents=True, exist_ok=True)

    # cat dog sub folders
    for class_dir in raw_root.iterdir():
        if not class_dir.is_dir():
            continue
        class_name = class_dir.name

        # Collect image paths
        imgs = [p for p in class_dir.iterdir() if p.is_file()]
        random.shuffle(imgs)

        n = len(imgs)
        n_train = int(n * train_ratio)
        n_val = int(n * val_ratio)

        splits = {
            "train": imgs[:n_train],
            "val": imgs[n_train:n_train + n_val],
            "test": imgs[n_train + n_val:],
        }

        for split_name, split_imgs in splits.items():
            class_out_dir = out_root / split_name / class_name
            class_out_dir.mkdir(parents=True, exist_ok=True)

            for img_path in split_imgs:
                dst = class_out_dir / img_path.name
                copy2(img_path, dst)

    print("Created splits at:", out_root)


if __name__ == "__main__":
    raw_root = DREW_ROOT_PATH / "pets_breeds"
    out_root = DREW_ROOT_PATH / "pets_breed_split"
    make_splits(
        raw_root=raw_root,
        out_root=out_root,
        train_ratio=0.7,
        val_ratio=0.15,
        seed=42,
    )
