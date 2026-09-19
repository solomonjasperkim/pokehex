"""Species available in Pokemon Legends: Z-A's Lumiose Pokedex, keyed by
National Pokedex number (the numbering PA9.species actually uses).

Source: the regional availability list published at
https://www.serebii.net/legendsz-a/availablepokemon.shtml (232 species,
matching the game's own Lumiose Pokedex count). This is name/number
reference data, not artwork.

Note: this is the base species list only -- alternate forms (regional forms,
Mega Evolutions, Vivillon patterns, etc.) share the same National Dex number
as their base species and aren't separately enumerated here. Use the `form`
field for those.
"""

from __future__ import annotations

ZA_SPECIES: dict[int, str] = {
    1: "Bulbasaur", 2: "Ivysaur", 3: "Venusaur",
    4: "Charmander", 5: "Charmeleon", 6: "Charizard",
    7: "Squirtle", 8: "Wartortle", 9: "Blastoise",
    13: "Weedle", 14: "Kakuna", 15: "Beedrill",
    16: "Pidgey", 17: "Pidgeotto", 18: "Pidgeot",
    23: "Ekans", 24: "Arbok",
    25: "Pikachu", 26: "Raichu",
    35: "Clefairy", 36: "Clefable",
    63: "Abra", 64: "Kadabra", 65: "Alakazam",
    66: "Machop", 67: "Machoke", 68: "Machamp",
    69: "Bellsprout", 70: "Weepinbell", 71: "Victreebel",
    79: "Slowpoke", 80: "Slowbro",
    92: "Gastly", 93: "Haunter", 94: "Gengar",
    95: "Onix",
    115: "Kangaskhan",
    120: "Staryu", 121: "Starmie",
    123: "Scyther",
    127: "Pinsir",
    129: "Magikarp", 130: "Gyarados",
    133: "Eevee", 134: "Vaporeon", 135: "Jolteon", 136: "Flareon",
    142: "Aerodactyl",
    147: "Dratini", 148: "Dragonair", 149: "Dragonite",
    150: "Mewtwo",
    152: "Chikorita", 153: "Bayleef", 154: "Meganium",
    158: "Totodile", 159: "Croconaw", 160: "Feraligatr",
    167: "Spinarak", 168: "Ariados",
    172: "Pichu", 173: "Cleffa",
    179: "Mareep", 180: "Flaaffy", 181: "Ampharos",
    196: "Espeon", 197: "Umbreon",
    199: "Slowking",
    208: "Steelix",
    212: "Scizor",
    214: "Heracross",
    225: "Delibird",
    227: "Skarmory",
    228: "Houndour", 229: "Houndoom",
    246: "Larvitar", 247: "Pupitar", 248: "Tyranitar",
    280: "Ralts", 281: "Kirlia", 282: "Gardevoir",
    302: "Sableye",
    303: "Mawile",
    304: "Aron", 305: "Lairon", 306: "Aggron",
    307: "Meditite", 308: "Medicham",
    309: "Electrike", 310: "Manectric",
    315: "Roselia",
    318: "Carvanha", 319: "Sharpedo",
    322: "Numel", 323: "Camerupt",
    333: "Swablu", 334: "Altaria",
    353: "Shuppet", 354: "Banette",
    359: "Absol",
    361: "Snorunt", 362: "Glalie",
    371: "Bagon", 372: "Shelgon", 373: "Salamence",
    374: "Beldum", 375: "Metang", 376: "Metagross",
    406: "Budew", 407: "Roserade",
    427: "Buneary", 428: "Lopunny",
    443: "Gible", 444: "Gabite", 445: "Garchomp",
    447: "Riolu", 448: "Lucario",
    449: "Hippopotas", 450: "Hippowdon",
    459: "Snover", 460: "Abomasnow",
    470: "Leafeon", 471: "Glaceon",
    475: "Gallade",
    478: "Froslass",
    498: "Tepig", 499: "Pignite", 500: "Emboar",
    504: "Patrat", 505: "Watchog",
    511: "Pansage", 512: "Simisage",
    513: "Pansear", 514: "Simisear",
    515: "Panpour", 516: "Simipour",
    529: "Drilbur", 530: "Excadrill",
    531: "Audino",
    543: "Venipede", 544: "Whirlipede", 545: "Scolipede",
    551: "Sandile", 552: "Krokorok", 553: "Krookodile",
    559: "Scraggy", 560: "Scrafty",
    568: "Trubbish", 569: "Garbodor",
    582: "Vanillite", 583: "Vanillish", 584: "Vanilluxe",
    587: "Emolga",
    602: "Tynamo", 603: "Eelektrik", 604: "Eelektross",
    607: "Litwick", 608: "Lampent", 609: "Chandelure",
    618: "Stunfisk",
    650: "Chespin", 651: "Quilladin", 652: "Chesnaught",
    653: "Fennekin", 654: "Braixen", 655: "Delphox",
    656: "Froakie", 657: "Frogadier", 658: "Greninja",
    659: "Bunnelby", 660: "Diggersby",
    661: "Fletchling", 662: "Fletchinder", 663: "Talonflame",
    664: "Scatterbug", 665: "Spewpa", 666: "Vivillon",
    667: "Litleo", 668: "Pyroar",
    669: "Flabebe", 670: "Floette", 671: "Florges",
    672: "Skiddo", 673: "Gogoat",
    674: "Pancham", 675: "Pangoro",
    676: "Furfrou",
    677: "Espurr", 678: "Meowstic",
    679: "Honedge", 680: "Doublade", 681: "Aegislash",
    682: "Spritzee", 683: "Aromatisse",
    684: "Swirlix", 685: "Slurpuff",
    686: "Inkay", 687: "Malamar",
    688: "Binacle", 689: "Barbaracle",
    690: "Skrelp", 691: "Dragalge",
    692: "Clauncher", 693: "Clawitzer",
    694: "Helioptile", 695: "Heliolisk",
    696: "Tyrunt", 697: "Tyrantrum",
    698: "Amaura", 699: "Aurorus",
    700: "Sylveon",
    701: "Hawlucha",
    702: "Dedenne",
    703: "Carbink",
    704: "Goomy", 705: "Sliggoo", 706: "Goodra",
    707: "Klefki",
    708: "Phantump", 709: "Trevenant",
    710: "Pumpkaboo", 711: "Gourgeist",
    712: "Bergmite", 713: "Avalugg",
    714: "Noibat", 715: "Noivern",
    716: "Xerneas", 717: "Yveltal", 718: "Zygarde", 719: "Diancie",
    780: "Drampa",
    870: "Falinks",
}


def display_options() -> list[str]:
    """'### Name' strings sorted by National Dex number, for a picker UI."""
    return [f"{num:03d}  {name}" for num, name in sorted(ZA_SPECIES.items())]


def name_for(species_number: int) -> str | None:
    return ZA_SPECIES.get(species_number)


def parse_selection(text: str) -> int:
    """Parses a picker selection or free-typed value back into a species
    number. Accepts '### Name', a bare number, or an exact species name."""
    text = text.strip()
    if not text:
        return 0
    head = text.split(None, 1)[0]
    if head.isdigit():
        return int(head)
    lowered = text.lower()
    for num, name in ZA_SPECIES.items():
        if name.lower() == lowered:
            return num
    return 0
