#!/usr/bin/env python3
"""
Analyse du dataset d'images pour équilibrer les minerais et biomes.
"""

import os
import re
from collections import defaultdict
from pathlib import Path

# Mapping des codes vers les noms
MINERAIS = {
    'c': 'charbon',
    'f': 'fer',
    'u': 'cuivre',
    'o': 'or',
    'd': 'diamant',
    'e': 'émeraude',
    'l': 'lapis',
    'r': 'redstone',
    'q': 'quartz',
    'a': 'ancient debris',
    'n': 'or nether',
}

def parse_filename(filename):
    """
    Parse un nom de fichier selon la nomenclature:
    {indice}_{a_minerai|s}_{biome}.png
    
    Retourne (indice, type, minerais_list, biome) ou None si format invalide
    """
    # Ignorer les fichiers sans le bon format (comme charbon1.png, .xml, .DS_Store)
    # Pattern: nombre_a/s_xxx_biome.ext ou nombre-a-xxx-biome.ext
    pattern = r'^(\d+)[_-](a|s)[_-]?([a-z]*)[_-]([a-z]+)\.(png|jpeg|jpg)$'
    match = re.match(pattern, filename, re.IGNORECASE)
    
    if not match:
        return None
    
    indice = int(match.group(1))
    type_img = match.group(2)  # 'a' (avec) ou 's' (sans)
    minerais_code = match.group(3)  # codes des minerais
    biome = match.group(4).lower()
    
    # Parser les minerais individuels
    minerais_list = []
    if type_img == 'a' and minerais_code:
        for char in minerais_code:
            if char in MINERAIS:
                minerais_list.append(char)
    
    return {
        'indice': indice,
        'type': type_img,
        'minerais_codes': minerais_list,
        'minerais_noms': [MINERAIS.get(m, m) for m in minerais_list],
        'biome': biome,
        'filename': filename
    }

def analyze_dataset(images_dir):
    """Analyse le dataset et retourne les statistiques."""
    
    # Compteurs
    minerais_count = defaultdict(int)
    biomes_count = defaultdict(int)
    minerais_par_biome = defaultdict(lambda: defaultdict(int))
    biomes_par_minerai = defaultdict(lambda: defaultdict(int))
    
    images_avec = []
    images_sans = []
    images_invalides = []
    
    # Parcourir les fichiers
    for filename in os.listdir(images_dir):
        if filename.startswith('.'):
            continue
        if filename.endswith('.xml'):
            continue
            
        parsed = parse_filename(filename)
        
        if parsed is None:
            images_invalides.append(filename)
            continue
        
        biome = parsed['biome']
        biomes_count[biome] += 1
        
        if parsed['type'] == 's':
            images_sans.append(parsed)
            # Compter comme "sans minerai"
            minerais_count['(sans)'] += 1
            minerais_par_biome[biome]['(sans)'] += 1
        else:
            images_avec.append(parsed)
            for minerai in parsed['minerais_codes']:
                minerais_count[minerai] += 1
                minerais_par_biome[biome][minerai] += 1
                biomes_par_minerai[minerai][biome] += 1
    
    return {
        'minerais_count': dict(minerais_count),
        'biomes_count': dict(biomes_count),
        'minerais_par_biome': {k: dict(v) for k, v in minerais_par_biome.items()},
        'biomes_par_minerai': {k: dict(v) for k, v in biomes_par_minerai.items()},
        'images_avec': images_avec,
        'images_sans': images_sans,
        'images_invalides': images_invalides,
        'total': len(images_avec) + len(images_sans)
    }

def print_report(stats):
    """Affiche un rapport détaillé."""
    
    print("=" * 60)
    print("ANALYSE DU DATASET")
    print("=" * 60)
    
    print(f"\nTotal d'images valides: {stats['total']}")
    print(f"  - Images AVEC minerai(s): {len(stats['images_avec'])}")
    print(f"  - Images SANS minerai: {len(stats['images_sans'])}")
    
    if stats['images_invalides']:
        print(f"  - Fichiers ignorés (format invalide): {len(stats['images_invalides'])}")
        for f in stats['images_invalides']:
            print(f"      • {f}")
    
    # Statistiques par minerai
    print("\n" + "-" * 60)
    print("RÉPARTITION PAR MINERAI")
    print("-" * 60)
    
    minerais_sorted = sorted(
        [(k, v) for k, v in stats['minerais_count'].items() if k != '(sans)'],
        key=lambda x: x[1],
        reverse=True
    )
    
    print(f"\n{'Code':<6} {'Minerai':<15} {'Nombre':<10} {'Barre'}")
    print("-" * 50)
    
    max_count = max(v for k, v in minerais_sorted) if minerais_sorted else 1
    
    for code, count in minerais_sorted:
        nom = MINERAIS.get(code, code)
        bar = "█" * int(30 * count / max_count)
        print(f"{code:<6} {nom:<15} {count:<10} {bar}")
    
    # Images sans minerai
    sans_count = stats['minerais_count'].get('(sans)', 0)
    print(f"\n{'(s)':<6} {'(sans minerai)':<15} {sans_count:<10}")
    
    # Statistiques par biome
    print("\n" + "-" * 60)
    print("RÉPARTITION PAR BIOME")
    print("-" * 60)
    
    biomes_sorted = sorted(
        stats['biomes_count'].items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    print(f"\n{'Biome':<15} {'Nombre':<10} {'Barre'}")
    print("-" * 50)
    
    max_biome = max(v for k, v in biomes_sorted) if biomes_sorted else 1
    
    for biome, count in biomes_sorted:
        bar = "█" * int(30 * count / max_biome)
        print(f"{biome:<15} {count:<10} {bar}")
    
    # Matrice minerai x biome
    print("\n" + "-" * 60)
    print("DÉTAIL PAR MINERAI ET BIOME")
    print("-" * 60)
    
    for code, count in minerais_sorted:
        nom = MINERAIS.get(code, code)
        biomes_for_minerai = stats['biomes_par_minerai'].get(code, {})
        biomes_str = ", ".join([f"{b}({c})" for b, c in sorted(biomes_for_minerai.items(), key=lambda x: -x[1])])
        print(f"\n{nom.upper()} ({count} total):")
        print(f"  {biomes_str}")
    
    # Recommandations pour équilibrer
    print("\n" + "=" * 60)
    print("RECOMMANDATIONS POUR ÉQUILIBRER")
    print("=" * 60)
    
    if minerais_sorted:
        max_minerai = minerais_sorted[0][1]
        min_minerai = minerais_sorted[-1][1]
        
        print("\nMinerais sous-représentés (à ajouter):")
        for code, count in minerais_sorted:
            if count < max_minerai * 0.5:  # Moins de 50% du max
                nom = MINERAIS.get(code, code)
                needed = max_minerai - count
                print(f"  • {nom}: {count} images (ajouter ~{needed} pour équilibrer)")
    
    if biomes_sorted:
        max_biome_count = biomes_sorted[0][1]
        
        print("\nBiomes sous-représentés:")
        for biome, count in biomes_sorted:
            if count < max_biome_count * 0.3:  # Moins de 30% du max
                print(f"  • {biome}: seulement {count} images")

def main():
    script_dir = Path(__file__).parent
    images_dir = script_dir / "dataset" / "images"
    
    if not images_dir.exists():
        print(f"Erreur: Le dossier {images_dir} n'existe pas")
        return
    
    stats = analyze_dataset(images_dir)
    print_report(stats)

if __name__ == "__main__":
    main()
