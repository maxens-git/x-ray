import os
import glob
import csv
import xml.etree.ElementTree as ET
from pathlib import Path

def parse_voc_xml(xml_path: str):
    """
    Parse un XML type Pascal VOC et retourne une liste de lignes (dict)
    avec: filename,width,height,name,xmin,ymin,xmax,ymax
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # filename
    filename = root.findtext("filename")
    if not filename:
        # fallback: parfois absent -> on met le nom du xml
        filename = os.path.splitext(os.path.basename(xml_path))[0]

    # size
    size = root.find("size")
    width = size.findtext("width") if size is not None else ""
    height = size.findtext("height") if size is not None else ""

    rows = []
    for obj in root.findall("object"):
        name = obj.findtext("name", default="")

        bndbox = obj.find("bndbox")
        if bndbox is None:
            continue

        xmin = bndbox.findtext("xmin", default="")
        ymin = bndbox.findtext("ymin", default="")
        xmax = bndbox.findtext("xmax", default="")
        ymax = bndbox.findtext("ymax", default="")

        rows.append({
            "filename": filename,
            "width": width,
            "height": height,
            "name": name,
            "xmin": xmin,
            "ymin": ymin,
            "xmax": xmax,
            "ymax": ymax,
        })

    return rows


def xmls_to_csv(xml_input: str, csv_output: str):
    """
    xml_input peut être:
      - un fichier unique: /chemin/fichier.xml
      - un dossier: /chemin/dossier
      - un pattern glob: /chemin/*.xml
    """
    if os.path.isdir(xml_input):
        xml_files = sorted(glob.glob(os.path.join(xml_input, "*.xml")))
    elif any(ch in xml_input for ch in ["*", "?", "["]):
        xml_files = sorted(glob.glob(xml_input))
    else:
        xml_files = [xml_input]

    if not xml_files:
        raise FileNotFoundError(f"Aucun fichier XML trouvé pour: {xml_input}")

    fieldnames = ["filename", "width", "height", "name", "xmin", "ymin", "xmax", "ymax"]

    with open(csv_output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for xml_path in xml_files:
            for row in parse_voc_xml(xml_path):
                writer.writerow(row)

    print(f"OK -> CSV généré: {csv_output} ({len(xml_files)} XML traités)")


if __name__ == "__main__":
    # Exemple 1: fichier unique (ton cas)
    cwd = Path.cwd()
    xml_dir = cwd / "dataset/images" 
    csv_output = cwd / "annotations.csv"
    xmls_to_csv(str(xml_dir), str(csv_output))

