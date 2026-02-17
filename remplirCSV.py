import csv
import os
import glob
import xml.etree.ElementTree as ET

CSV_PATH = "dataset/index.csv"
IMAGES_DIR = "dataset/images"

def parse_xml(xml_path):
    """Parse un fichier XML Pascal VOC et retourne une liste d'objets"""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    size = root.find("size")
    width = size.findtext("width") if size is not None else ""
    height = size.findtext("height") if size is not None else ""
    
    objects = []
    for obj in root.findall("object"):
        class_name = obj.findtext("name", "").upper()
        bndbox = obj.find("bndbox")
        if bndbox is not None:
            objects.append({
                "width": width,
                "height": height,
                "class": class_name,
                "xmin": bndbox.findtext("xmin", ""),
                "ymin": bndbox.findtext("ymin", ""),
                "xmax": bndbox.findtext("xmax", ""),
                "ymax": bndbox.findtext("ymax", ""),
            })
    
    return objects

def main():
    fieldnames = ["id", "data", "path", "class", "width", "height", "xmin", "ymin", "xmax", "ymax", "meta"]
    
    # Lire les entrées existantes
    existing_rows = []
    existing_entries = set()  # (path, class, xmin, ymin, xmax, ymax)
    max_id = 0
    
    if os.path.exists(CSV_PATH):
        with open(CSV_PATH, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_rows.append(row)
                key = (row["path"], row["class"], row["xmin"], row["ymin"], row["xmax"], row["ymax"])
                existing_entries.add(key)
                try:
                    max_id = max(max_id, int(row["id"]))
                except ValueError:
                    pass
    
    # Scanner tous les fichiers XML
    xml_files = glob.glob(os.path.join(IMAGES_DIR, "*.xml"))
    new_rows = []
    
    for xml_path in sorted(xml_files):
        basename = os.path.basename(xml_path).replace(".xml", "")
        relative_path = f"images/{basename}.png"
        
        objects = parse_xml(xml_path)
        for data in objects:
            key = (relative_path, data["class"], data["xmin"], data["ymin"], data["xmax"], data["ymax"])
            
            if key not in existing_entries:
                max_id += 1
                new_row = {
                    "id": max_id,
                    "data": "TRAIN",
                    "path": relative_path,
                    "class": data["class"],
                    "width": data["width"],
                    "height": data["height"],
                    "xmin": data["xmin"],
                    "ymin": data["ymin"],
                    "xmax": data["xmax"],
                    "ymax": data["ymax"],
                    "meta": "",
                }
                new_rows.append(new_row)
                existing_entries.add(key)
                print(f"+ {relative_path}: {data['class']} bbox=({data['xmin']},{data['ymin']})-({data['xmax']},{data['ymax']})")
    
    if new_rows:
        all_rows = existing_rows + new_rows
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_rows)
        print(f"\n{len(new_rows)} nouvelle(s) ligne(s) ajoutée(s)")
    else:
        print("Aucune nouvelle entrée à ajouter")

if __name__ == "__main__":
    main()

