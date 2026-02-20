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
| **IRON** | Minerai de fer |
| **COAL** | Minerai de charbon |
| **REDSTONE** | Minerai de charbon |
| **GOLD** | Minerai de or |
| **COPPER** | Minerai de cuivre |
| **LAPISLAZULI** | Minerai de lapis-lazuli |
| **EMERALD** | Minerai de émeraude |
| **DIAMOND** | Minerai de diamant |
| **NETHERQUARTZ** | Minerai de quartz |
| **NETHERGOLD** | Minerai de or nether |
| **ANCIENTDEBRIS** | Minerai de netherite |

# Nomenclature des images

Format : `{indice}_{a_minerai|s}_{biome}.png`

> **Note :** indices 1-100 et 200-258 déjà utilisés

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
