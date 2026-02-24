# Structure du Dataset

| Colonne | Description |
| :--- | :--- |
| **id** | Identifiant de la ligne |
| **data** | Split du dataset (TRAIN, VAL, TEST) |
| **path** | Chemin vers l'image |
| **class** | Label / Étiquette de l'objet |
| **width / height** | Dimensions de l'image (px) |
| **xmin / ymin** | Coin haut-gauche du cadre |
| **xmax / ymax** | Coin bas-droite du cadre |
| **meta** | Informations additionnelles |

# Classes

| Classe | Description |
| :--- | :--- |
| **iron** | Minerai de fer |
| **coal** | Minerai de charbon |
| **redstone** | Minerai de charbon |
| **gold** | Minerai de or |
| **copper** | Minerai de cuivre |
| **lapis** | Minerai de lapis-lazuli |
| **emerald** | Minerai de émeraude |
| **diamond** | Minerai de diamant |
| **quartz** | Minerai de quartz |
| **nethergold** | Minerai de or nether |
| **debris** | Minerai de netherite |

# Nomenclature des images

Format : `{indice}_{a_minerai|s}_{biome}.png`

> **Note :** indices 1-303 déjà utilisés

**Préfixe :**
| Code | Signification |
| :--- | :--- |
| **a** | avec |
| **s** | sans |

**Minerais :**
| Code | Minerai |
| :--- | :--- |
| **c** | charbon |
| **f** | fer |
| **u** | cuivre |
| **o** | or |
| **d** | diamant |
| **e** | émeraude |
| **l** | lapis |
| **r** | redstone |
| **q** | quartz |
| **a** | ancient debris |
| **n** | or nether |

**Biomes :**
| Biome |
| :--- |
| unknown |
| mineshaft |
| lushcave |
| dripstone |
| deepdark |
| stronghold |
| trialchamber |
| mountain |
| ancientcity |
| water |
| mesa |
| dungeon |
| geode |
| lava |
| crimson |
| warped |
| fortress |
| bastion |
| basalt |
| soulsand |
| nether |
