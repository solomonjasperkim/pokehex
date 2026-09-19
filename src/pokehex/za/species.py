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

# Order these species actually appear in Legends Z-A's own in-game Lumiose
# Pokedex (i.e. the order you'd "fill in" your dex playing normally), keyed
# by National Dex number. Source: the game's published Lumiose Pokedex
# listing at https://pokemondb.net/pokedex/game/legends-z-a
LOCAL_DEX_ORDER: dict[int, int] = {
    152: 1, 153: 2, 154: 3, 498: 4, 499: 5, 500: 6, 158: 7, 159: 8, 160: 9,
    661: 10, 662: 11, 663: 12, 659: 13, 660: 14, 664: 15, 665: 16, 666: 17,
    13: 18, 14: 19, 15: 20, 16: 21, 17: 22, 18: 23, 179: 24, 180: 25, 181: 26,
    504: 27, 505: 28, 406: 29, 315: 30, 407: 31, 129: 32, 130: 33, 688: 34,
    689: 35, 120: 36, 121: 37, 669: 38, 670: 39, 671: 40, 672: 41, 673: 42,
    677: 43, 678: 44, 667: 45, 668: 46, 674: 47, 675: 48, 568: 49, 569: 50,
    702: 51, 172: 52, 25: 53, 26: 54, 173: 55, 35: 56, 36: 57, 167: 58,
    168: 59, 23: 60, 24: 61, 63: 62, 64: 63, 65: 64, 92: 65, 93: 66, 94: 67,
    543: 68, 544: 69, 545: 70, 679: 71, 680: 72, 681: 73, 69: 74, 70: 75,
    71: 76, 511: 77, 512: 78, 513: 79, 514: 80, 515: 81, 516: 82, 307: 83,
    308: 84, 309: 85, 310: 86, 280: 87, 281: 88, 282: 89, 475: 90, 228: 91,
    229: 92, 333: 93, 334: 94, 531: 95, 682: 96, 683: 97, 684: 98, 685: 99,
    133: 100, 134: 101, 135: 102, 136: 103, 196: 104, 197: 105, 470: 106,
    471: 107, 700: 108, 427: 109, 428: 110, 353: 111, 354: 112, 582: 113,
    583: 114, 584: 115, 322: 116, 323: 117, 449: 118, 450: 119, 529: 120,
    530: 121, 551: 122, 552: 123, 553: 124, 66: 125, 67: 126, 68: 127,
    443: 128, 444: 129, 445: 130, 703: 131, 302: 132, 303: 133, 359: 134,
    447: 135, 448: 136, 79: 137, 80: 138, 199: 139, 318: 140, 319: 141,
    602: 142, 603: 143, 604: 144, 147: 145, 148: 146, 149: 147, 1: 148,
    2: 149, 3: 150, 4: 151, 5: 152, 6: 153, 7: 154, 8: 155, 9: 156, 618: 157,
    676: 158, 686: 159, 687: 160, 690: 161, 691: 162, 692: 163, 693: 164,
    704: 165, 705: 166, 706: 167, 225: 168, 361: 169, 362: 170, 478: 171,
    459: 172, 460: 173, 712: 174, 713: 175, 123: 176, 212: 177, 127: 178,
    214: 179, 587: 180, 701: 181, 708: 182, 709: 183, 559: 184, 560: 185,
    714: 186, 715: 187, 707: 188, 607: 189, 608: 190, 609: 191, 142: 192,
    696: 193, 697: 194, 698: 195, 699: 196, 95: 197, 208: 198, 304: 199,
    305: 200, 306: 201, 694: 202, 695: 203, 710: 204, 711: 205, 246: 206,
    247: 207, 248: 208, 656: 209, 657: 210, 658: 211, 870: 212, 650: 213,
    651: 214, 652: 215, 227: 216, 653: 217, 654: 218, 655: 219, 371: 220,
    372: 221, 373: 222, 115: 223, 780: 224, 374: 225, 375: 226, 376: 227,
    716: 228, 717: 229, 718: 230, 719: 231, 150: 232,
}


def display_options(sort_mode: str = "dex") -> list[str]:
    """'### Name' strings for a picker UI.

    sort_mode: "dex" (National Dex order, default), "alpha" (A-Z by name),
    or "fillin" (the order you'd fill these in playing Z-A's own Lumiose
    Pokedex).
    """
    items = list(ZA_SPECIES.items())
    if sort_mode == "alpha":
        items.sort(key=lambda kv: kv[1])
    elif sort_mode == "fillin":
        items.sort(key=lambda kv: LOCAL_DEX_ORDER.get(kv[0], 9999))
    else:
        items.sort(key=lambda kv: kv[0])
    return [f"{num:03d}  {name}" for num, name in items]


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
