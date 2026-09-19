"""Ability names, and which abilities each Legends: Z-A species can
actually have (regular slots 1/2 and the hidden ability). Game-mechanics
reference data, sourced from PokeAPI's public CSV dataset
(https://github.com/PokeAPI/pokeapi, BSD-3-Clause) -- not artwork.

This is the one field in PokeHex with real per-species legality checking,
unlike ball/item ids which are range-only.
"""

from __future__ import annotations

ABILITIES: dict[int, str] = {
    1: "Stench",
    2: "Drizzle",
    3: "Speed Boost",
    4: "Battle Armor",
    5: "Sturdy",
    6: "Damp",
    7: "Limber",
    8: "Sand Veil",
    9: "Static",
    10: "Volt Absorb",
    11: "Water Absorb",
    12: "Oblivious",
    13: "Cloud Nine",
    14: "Compound Eyes",
    15: "Insomnia",
    16: "Color Change",
    17: "Immunity",
    18: "Flash Fire",
    19: "Shield Dust",
    20: "Own Tempo",
    21: "Suction Cups",
    22: "Intimidate",
    23: "Shadow Tag",
    24: "Rough Skin",
    25: "Wonder Guard",
    26: "Levitate",
    27: "Effect Spore",
    28: "Synchronize",
    29: "Clear Body",
    30: "Natural Cure",
    31: "Lightning Rod",
    32: "Serene Grace",
    33: "Swift Swim",
    34: "Chlorophyll",
    35: "Illuminate",
    36: "Trace",
    37: "Huge Power",
    38: "Poison Point",
    39: "Inner Focus",
    40: "Magma Armor",
    41: "Water Veil",
    42: "Magnet Pull",
    43: "Soundproof",
    44: "Rain Dish",
    45: "Sand Stream",
    46: "Pressure",
    47: "Thick Fat",
    48: "Early Bird",
    49: "Flame Body",
    50: "Run Away",
    51: "Keen Eye",
    52: "Hyper Cutter",
    53: "Pickup",
    54: "Truant",
    55: "Hustle",
    56: "Cute Charm",
    57: "Plus",
    58: "Minus",
    59: "Forecast",
    60: "Sticky Hold",
    61: "Shed Skin",
    62: "Guts",
    63: "Marvel Scale",
    64: "Liquid Ooze",
    65: "Overgrow",
    66: "Blaze",
    67: "Torrent",
    68: "Swarm",
    69: "Rock Head",
    70: "Drought",
    71: "Arena Trap",
    72: "Vital Spirit",
    73: "White Smoke",
    74: "Pure Power",
    75: "Shell Armor",
    76: "Air Lock",
    77: "Tangled Feet",
    78: "Motor Drive",
    79: "Rivalry",
    80: "Steadfast",
    81: "Snow Cloak",
    82: "Gluttony",
    83: "Anger Point",
    84: "Unburden",
    85: "Heatproof",
    86: "Simple",
    87: "Dry Skin",
    88: "Download",
    89: "Iron Fist",
    90: "Poison Heal",
    91: "Adaptability",
    92: "Skill Link",
    93: "Hydration",
    94: "Solar Power",
    95: "Quick Feet",
    96: "Normalize",
    97: "Sniper",
    98: "Magic Guard",
    99: "No Guard",
    100: "Stall",
    101: "Technician",
    102: "Leaf Guard",
    103: "Klutz",
    104: "Mold Breaker",
    105: "Super Luck",
    106: "Aftermath",
    107: "Anticipation",
    108: "Forewarn",
    109: "Unaware",
    110: "Tinted Lens",
    111: "Filter",
    112: "Slow Start",
    113: "Scrappy",
    114: "Storm Drain",
    115: "Ice Body",
    116: "Solid Rock",
    117: "Snow Warning",
    118: "Honey Gather",
    119: "Frisk",
    120: "Reckless",
    121: "Multitype",
    122: "Flower Gift",
    123: "Bad Dreams",
    124: "Pickpocket",
    125: "Sheer Force",
    126: "Contrary",
    127: "Unnerve",
    128: "Defiant",
    129: "Defeatist",
    130: "Cursed Body",
    131: "Healer",
    132: "Friend Guard",
    133: "Weak Armor",
    134: "Heavy Metal",
    135: "Light Metal",
    136: "Multiscale",
    137: "Toxic Boost",
    138: "Flare Boost",
    139: "Harvest",
    140: "Telepathy",
    141: "Moody",
    142: "Overcoat",
    143: "Poison Touch",
    144: "Regenerator",
    145: "Big Pecks",
    146: "Sand Rush",
    147: "Wonder Skin",
    148: "Analytic",
    149: "Illusion",
    150: "Imposter",
    151: "Infiltrator",
    152: "Mummy",
    153: "Moxie",
    154: "Justified",
    155: "Rattled",
    156: "Magic Bounce",
    157: "Sap Sipper",
    158: "Prankster",
    159: "Sand Force",
    160: "Iron Barbs",
    161: "Zen Mode",
    162: "Victory Star",
    163: "Turboblaze",
    164: "Teravolt",
    165: "Aroma Veil",
    166: "Flower Veil",
    167: "Cheek Pouch",
    168: "Protean",
    169: "Fur Coat",
    170: "Magician",
    171: "Bulletproof",
    172: "Competitive",
    173: "Strong Jaw",
    174: "Refrigerate",
    175: "Sweet Veil",
    176: "Stance Change",
    177: "Gale Wings",
    178: "Mega Launcher",
    179: "Grass Pelt",
    180: "Symbiosis",
    181: "Tough Claws",
    182: "Pixilate",
    183: "Gooey",
    184: "Aerilate",
    185: "Parental Bond",
    186: "Dark Aura",
    187: "Fairy Aura",
    188: "Aura Break",
    189: "Primordial Sea",
    190: "Desolate Land",
    191: "Delta Stream",
    192: "Stamina",
    193: "Wimp Out",
    194: "Emergency Exit",
    195: "Water Compaction",
    196: "Merciless",
    197: "Shields Down",
    198: "Stakeout",
    199: "Water Bubble",
    200: "Steelworker",
    201: "Berserk",
    202: "Slush Rush",
    203: "Long Reach",
    204: "Liquid Voice",
    205: "Triage",
    206: "Galvanize",
    207: "Surge Surfer",
    208: "Schooling",
    209: "Disguise",
    210: "Battle Bond",
    211: "Power Construct",
    212: "Corrosion",
    213: "Comatose",
    214: "Queenly Majesty",
    215: "Innards Out",
    216: "Dancer",
    217: "Battery",
    218: "Fluffy",
    219: "Dazzling",
    220: "Soul-Heart",
    221: "Tangling Hair",
    222: "Receiver",
    223: "Power of Alchemy",
    224: "Beast Boost",
    225: "RKS System",
    226: "Electric Surge",
    227: "Psychic Surge",
    228: "Misty Surge",
    229: "Grassy Surge",
    230: "Full Metal Body",
    231: "Shadow Shield",
    232: "Prism Armor",
    233: "Neuroforce",
    234: "Intrepid Sword",
    235: "Dauntless Shield",
    236: "Libero",
    237: "Ball Fetch",
    238: "Cotton Down",
    239: "Propeller Tail",
    240: "Mirror Armor",
    241: "Gulp Missile",
    242: "Stalwart",
    243: "Steam Engine",
    244: "Punk Rock",
    245: "Sand Spit",
    246: "Ice Scales",
    247: "Ripen",
    248: "Ice Face",
    249: "Power Spot",
    250: "Mimicry",
    251: "Screen Cleaner",
    252: "Steely Spirit",
    253: "Perish Body",
    254: "Wandering Spirit",
    255: "Gorilla Tactics",
    256: "Neutralizing Gas",
    257: "Pastel Veil",
    258: "Hunger Switch",
    259: "Quick Draw",
    260: "Unseen Fist",
    261: "Curious Medicine",
    262: "Transistor",
    263: "Dragon’s Maw",
    264: "Chilling Neigh",
    265: "Grim Neigh",
    266: "As One",
    267: "As One",
    268: "Lingering Aroma",
    269: "Seed Sower",
    270: "Thermal Exchange",
    271: "Anger Shell",
    272: "Purifying Salt",
    273: "Well-Baked Body",
    274: "Wind Rider",
    275: "Guard Dog",
    276: "Rocky Payload",
    277: "Wind Power",
    278: "Zero to Hero",
    279: "Commander",
    280: "Electromorphosis",
    281: "Protosynthesis",
    282: "Quark Drive",
    283: "Good as Gold",
    284: "Vessel of Ruin",
    285: "Sword of Ruin",
    286: "Tablets of Ruin",
    287: "Beads of Ruin",
    288: "Orichalcum Pulse",
    289: "Hadron Engine",
    290: "Opportunist",
    291: "Cud Chew",
    292: "Sharpness",
    293: "Supreme Overlord",
    294: "Costar",
    295: "Toxic Debris",
    296: "Armor Tail",
    297: "Earth Eater",
    298: "Mycelium Might",
    299: "Mind’s Eye",
    300: "Supersweet Syrup",
    301: "Hospitality",
    302: "Toxic Chain",
    303: "Embody Aspect",
    304: "Tera Shift",
    305: "Tera Shell",
    306: "Teraform Zero",
    307: "Poison Puppeteer",
    308: "Piercing Drill",
    309: "Dragonize",
    310: "Mega Sol",
    311: "Spicy Spray",
    312: "Eelevate",
    313: "Fire Mane",
    314: "Aura Guard",
    10001: "Mountaineer",
    10002: "Wave Rider",
    10003: "Skater",
    10004: "Thrust",
    10005: "Perception",
    10006: "Parry",
    10007: "Instinct",
    10008: "Dodge",
    10009: "Jagged Edge",
    10010: "Frostbite",
    10011: "Tenacity",
    10012: "Pride",
    10013: "Deep Sleep",
    10014: "Power Nap",
    10015: "Spirit",
    10016: "Warm Blanket",
    10017: "Gulp",
    10018: "Herbivore",
    10019: "Sandpit",
    10020: "Hot Blooded",
    10021: "Medic",
    10022: "Life Force",
    10023: "Lunchbox",
    10024: "Nurse",
    10025: "Melee",
    10026: "Sponge",
    10027: "Bodyguard",
    10028: "Hero",
    10029: "Last Bastion",
    10030: "Stealth",
    10031: "Vanguard",
    10032: "Nomad",
    10033: "Sequence",
    10034: "Grass Cloak",
    10035: "Celebrate",
    10036: "Lullaby",
    10037: "Calming",
    10038: "Daze",
    10039: "Frighten",
    10040: "Interference",
    10041: "Mood Maker",
    10042: "Confidence",
    10043: "Fortune",
    10044: "Bonanza",
    10045: "Explode",
    10046: "Omnipotent",
    10047: "Share",
    10048: "Black Hole",
    10049: "Shadow Dash",
    10050: "Sprint",
    10051: "Disgust",
    10052: "High-rise",
    10053: "Climber",
    10054: "Flame Boost",
    10055: "Aqua Boost",
    10056: "Run Up",
    10057: "Conqueror",
    10058: "Shackle",
    10059: "Decoy",
    10060: "Shield",
}

# national dex number -> [(ability_id, slot)], slot: 1/2=regular, 3=hidden
SPECIES_ABILITIES: dict[int, list[tuple[int, int]]] = {
    1: [(65, 1), (34, 3)],  # Bulbasaur
    2: [(65, 1), (34, 3)],  # Ivysaur
    3: [(65, 1), (34, 3)],  # Venusaur
    4: [(66, 1), (94, 3)],  # Charmander
    5: [(66, 1), (94, 3)],  # Charmeleon
    6: [(66, 1), (94, 3)],  # Charizard
    7: [(67, 1), (44, 3)],  # Squirtle
    8: [(67, 1), (44, 3)],  # Wartortle
    9: [(67, 1), (44, 3)],  # Blastoise
    13: [(19, 1), (50, 3)],  # Weedle
    14: [(61, 1)],  # Kakuna
    15: [(68, 1), (97, 3)],  # Beedrill
    16: [(51, 1), (77, 2), (145, 3)],  # Pidgey
    17: [(51, 1), (77, 2), (145, 3)],  # Pidgeotto
    18: [(51, 1), (77, 2), (145, 3)],  # Pidgeot
    23: [(22, 1), (61, 2), (127, 3)],  # Ekans
    24: [(22, 1), (61, 2), (127, 3)],  # Arbok
    25: [(9, 1), (31, 3)],  # Pikachu
    26: [(9, 1), (31, 3)],  # Raichu
    35: [(56, 1), (98, 2), (132, 3)],  # Clefairy
    36: [(56, 1), (98, 2), (109, 3)],  # Clefable
    63: [(28, 1), (39, 2), (98, 3)],  # Abra
    64: [(28, 1), (39, 2), (98, 3)],  # Kadabra
    65: [(28, 1), (39, 2), (98, 3)],  # Alakazam
    66: [(62, 1), (99, 2), (80, 3)],  # Machop
    67: [(62, 1), (99, 2), (80, 3)],  # Machoke
    68: [(62, 1), (99, 2), (80, 3)],  # Machamp
    69: [(34, 1), (82, 3)],  # Bellsprout
    70: [(34, 1), (82, 3)],  # Weepinbell
    71: [(34, 1), (82, 3)],  # Victreebel
    79: [(12, 1), (20, 2), (144, 3)],  # Slowpoke
    80: [(12, 1), (20, 2), (144, 3)],  # Slowbro
    92: [(26, 1)],  # Gastly
    93: [(26, 1)],  # Haunter
    94: [(130, 1)],  # Gengar
    95: [(69, 1), (5, 2), (133, 3)],  # Onix
    115: [(48, 1), (113, 2), (39, 3)],  # Kangaskhan
    120: [(35, 1), (30, 2), (148, 3)],  # Staryu
    121: [(35, 1), (30, 2), (148, 3)],  # Starmie
    123: [(68, 1), (101, 2), (80, 3)],  # Scyther
    127: [(52, 1), (104, 2), (153, 3)],  # Pinsir
    129: [(33, 1), (155, 3)],  # Magikarp
    130: [(22, 1), (153, 3)],  # Gyarados
    133: [(50, 1), (91, 2), (107, 3)],  # Eevee
    134: [(11, 1), (93, 3)],  # Vaporeon
    135: [(10, 1), (95, 3)],  # Jolteon
    136: [(18, 1), (62, 3)],  # Flareon
    142: [(69, 1), (46, 2), (127, 3)],  # Aerodactyl
    147: [(61, 1), (63, 3)],  # Dratini
    148: [(61, 1), (63, 3)],  # Dragonair
    149: [(39, 1), (136, 3)],  # Dragonite
    150: [(46, 1), (127, 3)],  # Mewtwo
    152: [(65, 1), (102, 3)],  # Chikorita
    153: [(65, 1), (102, 3)],  # Bayleef
    154: [(65, 1), (102, 3)],  # Meganium
    158: [(67, 1), (125, 3)],  # Totodile
    159: [(67, 1), (125, 3)],  # Croconaw
    160: [(67, 1), (125, 3)],  # Feraligatr
    167: [(68, 1), (15, 2), (97, 3)],  # Spinarak
    168: [(68, 1), (15, 2), (97, 3)],  # Ariados
    172: [(9, 1), (31, 3)],  # Pichu
    173: [(56, 1), (98, 2), (132, 3)],  # Cleffa
    179: [(9, 1), (57, 3)],  # Mareep
    180: [(9, 1), (57, 3)],  # Flaaffy
    181: [(9, 1), (57, 3)],  # Ampharos
    196: [(28, 1), (156, 3)],  # Espeon
    197: [(28, 1), (39, 3)],  # Umbreon
    199: [(12, 1), (20, 2), (144, 3)],  # Slowking
    208: [(69, 1), (5, 2), (125, 3)],  # Steelix
    212: [(68, 1), (101, 2), (135, 3)],  # Scizor
    214: [(68, 1), (62, 2), (153, 3)],  # Heracross
    225: [(72, 1), (55, 2), (15, 3)],  # Delibird
    227: [(51, 1), (5, 2), (133, 3)],  # Skarmory
    228: [(48, 1), (18, 2), (127, 3)],  # Houndour
    229: [(48, 1), (18, 2), (127, 3)],  # Houndoom
    246: [(62, 1), (8, 3)],  # Larvitar
    247: [(61, 1)],  # Pupitar
    248: [(45, 1), (127, 3)],  # Tyranitar
    280: [(28, 1), (36, 2), (140, 3)],  # Ralts
    281: [(28, 1), (36, 2), (140, 3)],  # Kirlia
    282: [(28, 1), (36, 2), (140, 3)],  # Gardevoir
    302: [(51, 1), (100, 2), (158, 3)],  # Sableye
    303: [(52, 1), (22, 2), (125, 3)],  # Mawile
    304: [(5, 1), (69, 2), (134, 3)],  # Aron
    305: [(5, 1), (69, 2), (134, 3)],  # Lairon
    306: [(5, 1), (69, 2), (134, 3)],  # Aggron
    307: [(74, 1), (140, 3)],  # Meditite
    308: [(74, 1), (140, 3)],  # Medicham
    309: [(9, 1), (31, 2), (58, 3)],  # Electrike
    310: [(9, 1), (31, 2), (58, 3)],  # Manectric
    315: [(30, 1), (38, 2), (102, 3)],  # Roselia
    318: [(24, 1), (3, 3)],  # Carvanha
    319: [(24, 1), (3, 3)],  # Sharpedo
    322: [(12, 1), (86, 2), (20, 3)],  # Numel
    323: [(40, 1), (116, 2), (83, 3)],  # Camerupt
    333: [(30, 1), (13, 3)],  # Swablu
    334: [(30, 1), (13, 3)],  # Altaria
    353: [(15, 1), (119, 2), (130, 3)],  # Shuppet
    354: [(15, 1), (119, 2), (130, 3)],  # Banette
    359: [(46, 1), (105, 2), (154, 3)],  # Absol
    361: [(39, 1), (115, 2), (141, 3)],  # Snorunt
    362: [(39, 1), (115, 2), (141, 3)],  # Glalie
    371: [(69, 1), (125, 3)],  # Bagon
    372: [(69, 1), (142, 3)],  # Shelgon
    373: [(22, 1), (153, 3)],  # Salamence
    374: [(29, 1), (135, 3)],  # Beldum
    375: [(29, 1), (135, 3)],  # Metang
    376: [(29, 1), (135, 3)],  # Metagross
    406: [(30, 1), (38, 2), (102, 3)],  # Budew
    407: [(30, 1), (38, 2), (101, 3)],  # Roserade
    427: [(50, 1), (103, 2), (7, 3)],  # Buneary
    428: [(56, 1), (103, 2), (7, 3)],  # Lopunny
    443: [(8, 1), (24, 3)],  # Gible
    444: [(8, 1), (24, 3)],  # Gabite
    445: [(8, 1), (24, 3)],  # Garchomp
    447: [(80, 1), (39, 2), (158, 3)],  # Riolu
    448: [(80, 1), (39, 2), (154, 3)],  # Lucario
    449: [(45, 1), (159, 3)],  # Hippopotas
    450: [(45, 1), (159, 3)],  # Hippowdon
    459: [(117, 1), (43, 3)],  # Snover
    460: [(117, 1), (43, 3)],  # Abomasnow
    470: [(102, 1), (34, 3)],  # Leafeon
    471: [(81, 1), (115, 3)],  # Glaceon
    475: [(80, 1), (292, 2), (154, 3)],  # Gallade
    478: [(81, 1), (130, 3)],  # Froslass
    498: [(66, 1), (47, 3)],  # Tepig
    499: [(66, 1), (47, 3)],  # Pignite
    500: [(66, 1), (120, 3)],  # Emboar
    504: [(50, 1), (51, 2), (148, 3)],  # Patrat
    505: [(35, 1), (51, 2), (148, 3)],  # Watchog
    511: [(82, 1), (65, 3)],  # Pansage
    512: [(82, 1), (65, 3)],  # Simisage
    513: [(82, 1), (66, 3)],  # Pansear
    514: [(82, 1), (66, 3)],  # Simisear
    515: [(82, 1), (67, 3)],  # Panpour
    516: [(82, 1), (67, 3)],  # Simipour
    529: [(146, 1), (159, 2), (104, 3)],  # Drilbur
    530: [(146, 1), (159, 2), (104, 3)],  # Excadrill
    531: [(131, 1), (144, 2), (103, 3)],  # Audino
    543: [(38, 1), (68, 2), (3, 3)],  # Venipede
    544: [(38, 1), (68, 2), (3, 3)],  # Whirlipede
    545: [(38, 1), (68, 2), (3, 3)],  # Scolipede
    551: [(22, 1), (153, 2), (83, 3)],  # Sandile
    552: [(22, 1), (153, 2), (83, 3)],  # Krokorok
    553: [(22, 1), (153, 2), (83, 3)],  # Krookodile
    559: [(61, 1), (153, 2), (22, 3)],  # Scraggy
    560: [(61, 1), (153, 2), (22, 3)],  # Scrafty
    568: [(1, 1), (60, 2), (106, 3)],  # Trubbish
    569: [(1, 1), (133, 2), (106, 3)],  # Garbodor
    582: [(115, 1), (81, 2), (133, 3)],  # Vanillite
    583: [(115, 1), (81, 2), (133, 3)],  # Vanillish
    584: [(115, 1), (117, 2), (133, 3)],  # Vanilluxe
    587: [(9, 1), (78, 3)],  # Emolga
    602: [(26, 1)],  # Tynamo
    603: [(26, 1)],  # Eelektrik
    604: [(26, 1)],  # Eelektross
    607: [(18, 1), (49, 2), (151, 3)],  # Litwick
    608: [(18, 1), (49, 2), (151, 3)],  # Lampent
    609: [(18, 1), (49, 2), (151, 3)],  # Chandelure
    618: [(9, 1), (7, 2), (8, 3)],  # Stunfisk
    650: [(65, 1), (171, 3)],  # Chespin
    651: [(65, 1), (171, 3)],  # Quilladin
    652: [(65, 1), (171, 3)],  # Chesnaught
    653: [(66, 1), (170, 3)],  # Fennekin
    654: [(66, 1), (170, 3)],  # Braixen
    655: [(66, 1), (170, 3)],  # Delphox
    656: [(67, 1), (168, 3)],  # Froakie
    657: [(67, 1), (168, 3)],  # Frogadier
    658: [(67, 1), (168, 3)],  # Greninja
    659: [(53, 1), (167, 2), (37, 3)],  # Bunnelby
    660: [(53, 1), (167, 2), (37, 3)],  # Diggersby
    661: [(145, 1), (177, 3)],  # Fletchling
    662: [(49, 1), (177, 3)],  # Fletchinder
    663: [(49, 1), (177, 3)],  # Talonflame
    664: [(19, 1), (14, 2), (132, 3)],  # Scatterbug
    665: [(61, 1), (132, 3)],  # Spewpa
    666: [(19, 1), (14, 2), (132, 3)],  # Vivillon
    667: [(79, 1), (127, 2), (153, 3)],  # Litleo
    668: [(79, 1), (127, 2), (153, 3)],  # Pyroar
    669: [(166, 1), (180, 3)],  # Flabebe
    670: [(166, 1), (180, 3)],  # Floette
    671: [(166, 1), (180, 3)],  # Florges
    672: [(157, 1), (179, 3)],  # Skiddo
    673: [(157, 1), (179, 3)],  # Gogoat
    674: [(89, 1), (104, 2), (113, 3)],  # Pancham
    675: [(89, 1), (104, 2), (113, 3)],  # Pangoro
    676: [(169, 1)],  # Furfrou
    677: [(51, 1), (151, 2), (20, 3)],  # Espurr
    678: [(51, 1), (151, 2), (158, 3)],  # Meowstic
    679: [(99, 1)],  # Honedge
    680: [(99, 1)],  # Doublade
    681: [(176, 1)],  # Aegislash
    682: [(131, 1), (165, 3)],  # Spritzee
    683: [(131, 1), (165, 3)],  # Aromatisse
    684: [(175, 1), (84, 3)],  # Swirlix
    685: [(175, 1), (84, 3)],  # Slurpuff
    686: [(126, 1), (21, 2), (151, 3)],  # Inkay
    687: [(126, 1), (21, 2), (151, 3)],  # Malamar
    688: [(181, 1), (97, 2), (124, 3)],  # Binacle
    689: [(181, 1), (97, 2), (124, 3)],  # Barbaracle
    690: [(38, 1), (143, 2), (91, 3)],  # Skrelp
    691: [(38, 1), (143, 2), (91, 3)],  # Dragalge
    692: [(178, 1)],  # Clauncher
    693: [(178, 1)],  # Clawitzer
    694: [(87, 1), (8, 2), (94, 3)],  # Helioptile
    695: [(87, 1), (8, 2), (94, 3)],  # Heliolisk
    696: [(173, 1), (5, 3)],  # Tyrunt
    697: [(173, 1), (69, 3)],  # Tyrantrum
    698: [(174, 1), (117, 3)],  # Amaura
    699: [(174, 1), (117, 3)],  # Aurorus
    700: [(56, 1), (182, 3)],  # Sylveon
    701: [(7, 1), (84, 2), (104, 3)],  # Hawlucha
    702: [(167, 1), (53, 2), (57, 3)],  # Dedenne
    703: [(29, 1), (5, 3)],  # Carbink
    704: [(157, 1), (93, 2), (183, 3)],  # Goomy
    705: [(157, 1), (93, 2), (183, 3)],  # Sliggoo
    706: [(157, 1), (93, 2), (183, 3)],  # Goodra
    707: [(158, 1), (170, 3)],  # Klefki
    708: [(30, 1), (119, 2), (139, 3)],  # Phantump
    709: [(30, 1), (119, 2), (139, 3)],  # Trevenant
    710: [(53, 1), (119, 2), (15, 3)],  # Pumpkaboo
    711: [(53, 1), (119, 2), (15, 3)],  # Gourgeist
    712: [(20, 1), (115, 2), (5, 3)],  # Bergmite
    713: [(20, 1), (115, 2), (5, 3)],  # Avalugg
    714: [(119, 1), (151, 2), (140, 3)],  # Noibat
    715: [(119, 1), (151, 2), (140, 3)],  # Noivern
    716: [(187, 1)],  # Xerneas
    717: [(186, 1)],  # Yveltal
    718: [(188, 1)],  # Zygarde
    719: [(29, 1)],  # Diancie
    780: [(201, 1), (157, 2), (13, 3)],  # Drampa
    870: [(4, 1), (128, 3)],  # Falinks
}
