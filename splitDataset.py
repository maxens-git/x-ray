import csv
import os
import random
import argparse
from collections import defaultdict

CSV_INPUT = "dataset/index.csv"
CSV_OUTPUT = "dataset/split.csv"

# Mapping code minerai -> classe CSV
MINERAL_CODE_TO_CLASS = {
    "c": "COAL",
    "f": "IRON",
    "u": "COPPER",
    "o": "GOLD",
    "d": "DIAMOND",
    "e": "EMERALD",
    "l": "LAPIS",
    "r": "REDSTONE",
    "q": "QUARTZ",
    "a": "DEBRIS",
    "n": "NETHERGOLD",
}


def parse_image_name(path):
    """Extrait le biome depuis le nom de l'image.
    Format: {indice}_{a_minerai|s}_{biome}.png
    """
    basename = os.path.basename(path).replace(".png", "")
    parts = basename.split("_")
    # Le biome est le dernier élément
    if len(parts) >= 3:
        return parts[-1]
    return "unknown"


def main():
    parser = argparse.ArgumentParser(description="Split le dataset en TRAIN / VAL / TEST")
    parser.add_argument("--train", type=float, default=0.6, help="Proportion train (défaut: 0.7)")
    parser.add_argument("--val", type=float, default=0.2, help="Proportion val (défaut: 0.15)")
    parser.add_argument("--test", type=float, default=0.2, help="Proportion test (défaut: 0.15)")
    args = parser.parse_args()

    total = args.train + args.val + args.test
    if abs(total - 1.0) > 0.01:
        print(f"Erreur: les proportions doivent sommer à 1.0 (actuellement {total:.2f})")
        return

    # Lire le CSV
    with open(CSV_INPUT, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Grouper les lignes par image
    image_rows = defaultdict(list)
    for row in rows:
        image_rows[row["path"]].append(row)

    # Pour chaque image: extraire biome et classes présentes
    image_info = {}
    for path, img_rows in image_rows.items():
        biome = parse_image_name(path)
        classes = set(r["class"] for r in img_rows)
        image_info[path] = {"biome": biome, "classes": classes}

    # Collecter toutes les classes
    all_classes = set()
    for info in image_info.values():
        all_classes.update(info["classes"])
    all_classes = sorted(all_classes)

    # Stratification par (classe, biome)
    # Pour chaque classe, grouper les images par biome
    # Puis splitter proportionnellement dans chaque groupe
    # On accumule des votes par image, et l'attribution finale sera le split majoritaire

    # Approche : on split par biome (car le biome est le facteur de stratification principal)
    # Cela garantit un équilibre biome pour toutes les classes

    biome_images = defaultdict(list)
    for path, info in image_info.items():
        biome_images[info["biome"]].append(path)

    image_split = {}

    print("=== Split par biome ===\n")
    for biome in sorted(biome_images.keys()):
        images = biome_images[biome]
        random.shuffle(images)
        n = len(images)

        n_train = round(n * args.train)
        n_val = round(n * args.val)
        n_test = n - n_train - n_val

        # Ajuster si arrondi donne des négatifs
        if n_test < 0:
            n_test = 0
            n_val = n - n_train

        for img in images[:n_train]:
            image_split[img] = "TRAIN"
        for img in images[n_train:n_train + n_val]:
            image_split[img] = "VAL"
        for img in images[n_train + n_val:]:
            image_split[img] = "TEST"

        print(f"  {biome:20s} -> {n:3d} images | TRAIN={n_train} VAL={n_val} TEST={n_test}")

    # Assigner la colonne data
    fieldnames = ["id", "data", "path", "class", "width", "height", "xmin", "ymin", "xmax", "ymax", "meta"]
    for row in rows:
        row["data"] = image_split[row["path"]]

    # Écrire le CSV de sortie
    with open(CSV_OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    # Statistiques détaillées
    print("\n=== Distribution par classe et split ===\n")
    print(f"  {'Classe':15s} {'TRAIN':>6s} {'VAL':>6s} {'TEST':>6s} {'TOTAL':>6s}")
    print("  " + "-" * 45)

    class_split_counts = defaultdict(lambda: defaultdict(int))
    for row in rows:
        class_split_counts[row["class"]][row["data"]] += 1

    for cls in sorted(class_split_counts.keys()):
        counts = class_split_counts[cls]
        t, v, te = counts["TRAIN"], counts["VAL"], counts["TEST"]
        total = t + v + te
        print(f"  {cls:15s} {t:6d} {v:6d} {te:6d} {total:6d}")

    # Totaux
    print("  " + "-" * 45)
    t_all = sum(c["TRAIN"] for c in class_split_counts.values())
    v_all = sum(c["VAL"] for c in class_split_counts.values())
    te_all = sum(c["TEST"] for c in class_split_counts.values())
    print(f"  {'TOTAL':15s} {t_all:6d} {v_all:6d} {te_all:6d} {t_all + v_all + te_all:6d}")

    # Stats par images
    split_img_counts = defaultdict(int)
    for s in image_split.values():
        split_img_counts[s] += 1
    n_img = len(image_split)
    print(f"\n=== Images ===\n")
    print(f"  TRAIN: {split_img_counts['TRAIN']:3d} ({split_img_counts['TRAIN']/n_img*100:.1f}%)")
    print(f"  VAL:   {split_img_counts['VAL']:3d} ({split_img_counts['VAL']/n_img*100:.1f}%)")
    print(f"  TEST:  {split_img_counts['TEST']:3d} ({split_img_counts['TEST']/n_img*100:.1f}%)")
    print(f"  TOTAL: {n_img:3d}")

    print(f"\nCSV écrit: {CSV_OUTPUT}")


if __name__ == "__main__":
    main()
