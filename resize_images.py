#!/usr/bin/env python3
"""
Script pour redimensionner toutes les images PNG à une taille uniforme.
"""

from pathlib import Path
from PIL import Image

# Configuration
IMAGES_DIR = Path(__file__).parent / "dataset" / "images"
TARGET_SIZE = (640, 360)  # (largeur, hauteur)


def resize_images():
    """Redimensionne toutes les images PNG du dossier à la taille cible."""
    images = list(IMAGES_DIR.glob("*.png"))
    print(f"Trouvé {len(images)} images PNG")

    resized = 0
    errors = []

    for img_path in images:
        try:
            with Image.open(img_path) as img:
                if img.size != TARGET_SIZE:
                    # Redimensionner et sauvegarder
                    resized_img = img.resize(TARGET_SIZE, Image.Resampling.LANCZOS)
                    resized_img.save(img_path)
                    resized += 1
                    print(f"✓ {img_path.name}: {img.size} → {TARGET_SIZE}")
        except Exception as e:
            errors.append((img_path.name, str(e)))
            print(f"✗ {img_path.name}: {e}")

    print(f"\n{resized} images redimensionnées")
    if errors:
        print(f"{len(errors)} erreurs")


if __name__ == "__main__":
    resize_images()
