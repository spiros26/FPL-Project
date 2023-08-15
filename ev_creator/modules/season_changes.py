import pandas as pd
import requests
import numpy as np
from modules.useful_functions import team_id, fixture_info2, avg
import pickle


expected_minutes = {
# Arsenal
    1: [0.0],  # Balogun
    2: [0.0],  # Cedric
    3: [3.0],  # Elneny
    4: [15.0],  # Vieira
    5: [50.0],  # Gabriel
    6: [72.0],  # Havertz
    7: [4.0],  # Holding
    8: [0.0],  # Jesus
    9: [10.0],  # Jorginho
    10: [6.0], # Kiwior
    11: [0.0], # Marquinhos
    12: [76.0], # Martinelli
    13: [76.0], # Nketiah
    14: [83.0], # Odegaard
    15: [78.0], # Partey
    16: [3.0], # Pepe
    17: [85.0], # Ramsdale
    113: [35.0],    # Raya
    18: [0.0], # Runaarsson
    19: [85.0], # Saka
    20: [82.0], # Saliba
    21: [5.0], # Sambi
    22: [13.0], # Smith Rowe
    23: [2.0], # Tavares
    24: [8.0], # Tierney
    25: [63.0], # Tomiyasu
    26: [55.0], # Trossard
    27: [0.0],  # Trusty
    29: [75.0], # White
    30: [79.0], # Xhaka
    31: [17.0], # Zinchenko
    578: [11.0],    # Nelson
    540: [80.0],    # Rice
    585: [27.0],    # J.Timber
# Aston Villa
    32: [20.0], # Alex Moreno
    33: [3.0], # Archer
    34: [62.0], # Bailey
    35: [65.0], # Buendia
    36: [77.0], # Cash
    37: [8.0], # Chambers
    38: [7.0], # Coutinho
    39: [0.0], # Davis
    40: [13.0], # Dendoncker
    41: [57.0], # Diego Carlos
    42: [75.0], # Digne 
    43: [79.0], # Douglas Luiz
    44: [13.0], # Duran
    45: [8.0], # Hause 
    46: [3.0], # Iroegbunam
    47: [3.0], # Kamara
    48: [77.0], # Konsa
    49: [89.0], # Martinez
    50: [74.0], # McGinn
    51: [70.0], # Mings
    53: [1.0], # Olsen
    54: [0.0], # Philogene-Bidace
    55: [55.0], # Ramsey
    56: [8.0], # Sanson
    57: [0.0], # Sinisalo
    58: [36.0], # Tielemans
    59: [15.0], # Traore
    60: [86.0], # Watkins
    61: [1.0], # Wesley
    584: [72.0],    # Pau Torres
    599: [79.0],    # Diaby
# Bournemouth
    62: [3.0], # Anthony
    63: [75.0], # Billing
    64: [65.0], # Brooks
    65: [62.0], # Christie
    66: [77.0], # Cook
    67: [12.0], # Dembele
    68: [4.0], # Fredericks
    69: [0.0], # Hill
    70: [0.0], # Kelly
    71: [0.0], # Kilkenny
    72: [8.0], # Kluivert
    73: [0.0], # Lowe
    74: [0.0], # Marcondes
    75: [3.0], # Mepham
    76: [14.0], # Moore
    77: [89.0], # Neto
    78: [65.0], # Ouattara
    79: [15.0], # Pearson
    80: [0.0], # Randolph
    81: [77.0], # Rothwell
    82: [12.0], # Semenyo
    83: [62.0], # Senesi
    84: [65.0], # Smith
    85: [85.0], # Solanke
    86: [48.0], # Tavernier
    87: [32.0], # H.Traore
    88: [1.0], # Travers
    89: [78.0], # Zabarnyi
    595: [77.0],    # Kerkez
    607: [0.0],    # Radu
# Brentford
    90: [73.0], # Ajer
    91: [0.0], # Balcombe
    92: [11.0], # Baptiste
    93: [0.0], # Bech
    94: [0.0], # Bidstrup
    95: [55.0], # Canos
    96: [78.0], # Collins
    97: [0.0], # Cox
    98: [67.0], # Damsgaard
    99: [23.0], # Dasilva
    100: [0.0],  # Dervisoglu
    101: [89.0],    # Flekken
    102: [0.0],    # Goode
    103: [79.0],    # Henry
    104: [70.0],    # Hickey
    105: [74.0],    # Janelt
    106: [57.0],    # Jensen
    107: [0.0],    # Lewis-Potter
    108: [83.0],    # Mbeumo
    109: [0.0],    # Mee
    110: [72.0],    # Norgaard
    111: [12.0],    # Onyeka
    112: [85.0],    # Pinnock
    114: [0.0],    # Roerslev
    115: [0.0],    # Schade
    116: [0.0],    # Strakosha
    117: [0.0],    # Toney
    118: [0.0],    # Trevitt
    119: [75.0],    # Wissa
    120: [0.0],    # Yarmolyuk
    121: [3.0],    #Zanka
    122: [0.0],    # Adingra
# Brighton
    123: [8.0],    # Alzate
    124: [8.0],    # Ayari
    125: [22.0],    # Buonanotte
    127: [3.0],    # Connolly
    128: [3.0],    # Dahoud
    129: [85.0],    # Dunk
    130: [62.0],    # Enciso
    131: [77.0],    # Estupinan
    132: [60.0],    # Ferguson
    133: [22.0],    # Gilmour
    134: [82.0],    # Gross
    135: [75.0],    # Joao Pedro
    136: [0.0],    # Karbownik
    137: [0.0],    # Kozlowski
    138: [12.0],    # Lallana
    139: [15.0],    # Lamptey
    140: [77.0],    # March
    141: [0.0],    # McGill
    142: [75.0],    # Milner
    143: [76.0],    # Mitoma
    144: [14.0],    # Moder
    146: [12.0],    # Sarmiento
    147: [0.0],    # Scherpen
    148: [89.0],    # Steele
    149: [12.0],    # Undav
    150: [76.0],    # Van Hecke
    151: [15.0],    # Veltman
    152: [0.0],    # Verbruggen
    153: [82.0],    # Webster
    154: [65.0],    # Wellbeck
    155: [0.0],    # Zeqiri
    606: [12.0],    # Igor
# Burnley
    156: [0.0],    # Agyei
    157: [80.0],    # Al-Dakhil
    158: [0.0],    # Bastien
    159: [65.0],    # Benson
    160: [19.0],    # Beyer
    161: [82.0],    # Brownhill
    162: [0.0],    # Churlinov
    163: [15.0],    # Cork
    164: [0.0],    # Costelloe
    165: [87.0],    # Cullen
    166: [0.0],    # Egan-Riley    
    167: [0.0],    # Ekdal
    168: [78.0],    # Foster
    169: [0.0],    # Franchi    
    170: [15.0],    # Gudmundsson
    171: [0.0],    # McNally
    172: [1.0],    # Muric
    173: [82.0],    # O'Shea
    174: [11.0],    # Obafemi
    175: [0.0],    # Peacock-Farrell
    176: [79.0],    # Roberts
    177: [0.0],    # Rodriguez
    178: [75.0],    # Taylor
    179: [0.0],    # Thomas
    180: [0.0],    # Twine
    181: [0.0],    # Vigouroux
    182: [76.0],    # Vitinho
    183: [0.0],    # Weghorst
    184: [0.0],    # Zaroury
    185: [0.0],    # Ampadu
    186: [0.0],    # Andrey Santos
    594: [60.0],    # Amdouni
    600: [15.0],    # Redmond
    596: [89.0],    # Trafford
    605: [65.0],    # Koleosho
    608: [45.0],    # Bruun Larsen
# Chelsea
    145: [89.0],    # Sanchez
    126: [68.0],    # Caicedo
    187: [0.0],    # Arrizabalaga
    188: [0.0],    # Aubameyang
    189: [0.0],    # Azpilicueta
    190: [0.0],    # Baba Rahman
    191: [15.0],    # Badiashile
    192: [0.0],    # Bettinelli
    193: [3.0],    # Broja
    194: [22.0],    # Chalobah
    195: [77.0],    # Chilwell
    196: [62.0],    # Chukwuemeka
    197: [77.0],    # Colwill
    198: [55.0],    # Cucurella
    199: [82.0],    # Enzo
    200: [12.0],    # D.D.Fofana
    201: [0.0],    # W.Fofana
    202: [66.0],    # Gallagher
    203: [14.0],    # Gusto
    204: [5.0],    # Hall
    205: [0.0],    # Hudson-Odoi
    206: [74.0],    # James
    207: [0.0],    # Lukaku
    208: [25.0],    # Madueke
    210: [62.0],    # Mudryk
    211: [72.0],    # N.Jackson
    212: [0.0],    # Nkunku
    213: [0.0],    # Pulisic
    214: [4.0],    # Sarr
    215: [0.0],    # Slonina
    216: [73.0],    # Sterling
    217: [84.0],    # Thiago Silva
    218: [0.0],    # Ziyech
    589: [0.0],    # Angelo
    609: [24.0],    # Maatsen
    611: [75.0],    # Disasi 
    613: [0.0],    # Ugochukwu
# Crystal Palace
    219: [0.0],    # Ahamada
    220: [85.0],    # Andersen
    221: [73.0],    # J.Ayew
    222: [72.0],    # Clyne
    223: [55.0],    # C.Doucoure
    224: [0.0],    # Ebiowei
    225: [68.0],    # Edouard
    226: [85.0],    # Eze
    227: [1.0],    # Guaita
    228: [85.0],    # Guehi
    229: [25.0],    # Hughes
    230: [88.0],    # Johnstone
    231: [74.0],    # Lerma
    232: [35.0],    # Mateta
    233: [0.0],    # Matthews
    234: [77.0],    # Mitchell
    235: [0.0],    # O'Brien
    236: [0.0],    # Olise
    237: [0.0],    # Plange
    238: [0.0],    # Richards
    239: [0.0],    # Riedewald
    240: [74.0],    # Schlupp
    241: [8.0],    # Tomkins
    242: [77.0],    # Ward
    243: [0.0],    # Whitworth
    615: [0.0],    # Matheus de Oliveira
# Everton
    244: [24.0],    # Andre Gomes
    245: [12.0],    # Branthwaite
    246: [74.0],    # Calvert-Lewin
    247: [73.0],    # Coleman
    248: [5.0],    # Dele
    249: [83.0],    # A.Doucoure
    250: [0.0],    # Garner
    251: [0.0],    # Gbamin
    252: [22.0],    # Godfrey
    253: [57.0],    # Gray
    254: [74.0],    # Gueye
    255: [13.0],    # Holgate
    256: [77.0],    # Iwobi
    257: [80.0],    # Keane
    258: [65.0],    # Maupay
    259: [75.0],    # McNeil
    260: [33.0],    # Mykolenko
    261: [67.0],    # Onana
    262: [77.0],    # Patterson
    263: [89.0],    # Pickford
    264: [8.0],    # Simms
    265: [82.0],    # Tarkowski
    266: [0.0],    # Virginia
    579: [0.0],    # Lonergan
    588: [73.0],    # Young
    601: [60.0],    # Danjuma
# Fulham
    267: [80.0],    # Andreas
    268: [63.0],    # Cairney
    269: [8.0],    # Cavaleiro
    270: [22.0],    # De Cordova-Reid
    271: [80.0],    # Diop
    272: [0.0],     # Francois
    273: [0.0],     # Knockaert
    274: [0.0],     # Kongolo
    275: [89.0],    # Leno
    276: [75.0],     # Lukic
    277: [12.0],    # Mbabu
    278: [55.0],    # Mitrovic
    279: [0.0],     # Muniz
    280: [77.0],    # Palinha
    281: [80.0],    # Ream
    282: [74.0],    # Reed
    283: [78.0],    # Robinson
    284: [1.0],     # Rodak
    285: [75.0],    # Tete
    286: [82.0],    # Tosin
    287: [25.0],    # Vinicius
    288: [74.0],    # Wilson
    558: [55.0],    # Jimenez
    591: [53.0],    # Willian
    610: [13.0],    # Bassey
# Liverpool
    289: [0.0],     # Adrian
    290: [82.0],    # Alexander-Arnold
    291: [89.0],    # Alisson
    292: [15.0],    # Bajcetic
    293: [54.0],    # Darwin
    294: [65.0],    # Diogo Jota
    295: [13.0],    # Eliott
    296: [0.0],     # Fabinho
    297: [67.0],    # Gakpo
    298: [12.0],    # Gomez
    299: [0.0],     # Henderson
    300: [13.0],    # Jones
    301: [1.0],    # Kelleher
    302: [77.0],    # Konate
    303: [70.0],    # Luis Diaz
    304: [74.0],    # Mac Allister
    305: [32.0],    # Matip
    306: [0.0],    # Phillips
    307: [80.0],    # Robertson
    308: [86.0],    # Salah
    309: [65.0],    # Szoboszlai  
    310: [65.0],    # Thiago
    311: [22.0],    # Tsimikas
    312: [0.0],    # Van den Berg
    313: [85.0],    # Van Dijk
# Luton
    52: [80.0], # Nakamba
    314: [75.0],    # Adebayo
    315: [77.0],    # Andersen
    316: [82.0],    # Bell
    317: [10.0],    # Burry
    318: [23.0],    # Burke
    319: [75.0],    # Campbell
    320: [78.0],    # Clark
    321: [35.0],    # Doughty
    322: [0.0],    # Freeman
    323: [0.0],    # Macey
    324: [0.0],    # McAtee
    325: [0.0],    # Mendes
    326: [82.0],    # Morris
    582: [74.0],    # Mpanzu
    586: [65.0],    # Chong
    602: [74.0],    # Kabore
    327: [0.0],    # Muskwe
    328: [15.0],    # Ogbene
    329: [0.0],    # Onyedinma
    330: [0.0],    # Osho
    331: [0.0],    # Pepple
    332: [0.0],    # Pereira
    333: [15.0],    # Potts
    334: [0.0],    # Rea
    335: [89.0],    # Shea
    336: [0.0],    # Taylor
    337: [0.0],    # Thorpe
    338: [0.0],    # Walton
    339: [0.0],    # Watson
    340: [13.0],    # Woodrow
    553: [77.0],    # Giles
    575: [84.0],    # Lockyer
# Man City
    341: [68.0],    # Akanji
    342: [65.0],    # Ake
    343: [70.0],    # Alvarez
    344: [75.0],    # Bernardo
    345: [0.0],    # Bobb
    346: [0.0],    # Cancelo
    347: [0.0],    # Carson
    348: [0.0],    # Charles
    349: [10.0],    # De Bruyne
    350: [46.0],    # Dias
    351: [0.0],    # Doyle
    352: [88.0],    # Ederson
    353: [67.0],    # Foden
    354: [67.0],    # Grealish
    355: [80.0],    # Haaland
    356: [65.0],    # Kovacic
    357: [45.0],    # Laporte
    358: [63.0],    # Lewis
    359: [0.0],    # Mahrez
    360: [4.0],    # McAtee
    361: [2.0],    # Ortega
    362: [12.0],    # Palmer
    363: [0.0],    # Perrone
    364: [8.0],    # Phillips
    365: [82.0],    # Rodri
    366: [10.0],    # Sergio Gomez
    367: [0.0],    # Steffen
    368: [54.0],    # Stones
    369: [23.0],    # Walker
    616: [65.0],    # Gvardiol
# Man United
    370: [12.0],    # Telles
    371: [8.0],    # Amad
    372: [67.0],    # Antony
    373: [85.0],    # Fernandes
    209: [75.0],    # Mount
    374: [0.0],    # B.Williams
    375: [0.0],    # Bailly
    376: [82.0],    # Casemiro
    377: [57.0],    # Dalot
    378: [23.0],    # Elanga
    379: [73.0],    # Eriksen
    380: [0.0],    # Alvaro Fernandez
    381: [45.0],    # Fred
    382: [60.0],    # Garnacho
    383: [0.0],    # Mejbri
    384: [0.0],    # Heaton
    385: [1.0],    # Hendersonn
    386: [12.0],    # Lindelof
    387: [0.0],    # Maguire
    388: [0.0],    # Mainoo
    389: [23.0],    # Malacia
    390: [65.0],    # Martial
    391: [78.0],    # Martinez
    392: [22.0],    # McTominay
    393: [0.0],    # Mengi
    394: [12.0],    # Pellistri
    395: [84.0],    # Varane
    396: [80.0],    # Rashford
    397: [60.0],    # Sancho
    398: [84.0],    # Shaw
    399: [0.0],    # Shoretire
    400: [14.0],    # Van de Beek
    401: [72.0],    # Wan-Bissaka
    597: [89.0],    # Onana
    617: [55.0],    # Hojlund
# Newcastle
    402: [75.0],    # Almiron
    403: [0.0],    # Anderson
    404: [0.0],    # Ashby
    405: [84.0],    # Botman
    406: [82.0],    # Bruno Guimaraes
    407: [82.0],    # Burn
    408: [0.0],    # Darlow
    409: [1.0],    # Dubravka
    410: [8.0],    # Fraser
    411: [0.0],    # Gillespie
    412: [59.0],    # Gordon
    413: [0.0],    # Hayden
    414: [0.0],    # Hendrick
    415: [65.0],    # Isak
    416: [75.0],    # Joelinton
    417: [0.0],    # Krafth
    418: [0.0],    # Kuol
    419: [0.0],    # Lascelles
    420: [0.0],    # Lewis
    421: [57.0],    # S.Longstaff
    422: [0.0],    # Manquillo
    423: [27.0],    # Murphy
    424: [89.0],    # Pope
    425: [0.0],    # Ritchie
    426: [0.0],    # Saint-Maximin
    427: [85.0],    # Schar
    428: [12.0],    # Targett
    429: [79.0],    # Tonali
    430: [86.0],    # Trippier
    431: [0.0],    # Watts
    432: [65.0],    # Willock    
    433: [57.0],    # Wilson
# Nottingham Forest
    28: [89.0],     # Turner
    434: [0.0],    # B.Aguilera
    435: [0.0],    # Arter
    436: [69.0],    # Aurier
    437: [75.0],    # Awoniyi
    438: [0.0],    # Biancone
    439: [78.0],    # Boly
    440: [0.0],    # Bowler
    441: [75.0],    # Cook
    442: [12.0],    # Danilo
    443: [0.0],    # Dennis
    444: [0.0],    # Drager
    445: [0.0],    # Felipe
    446: [24.0],    # Freuler
    447: [80.0],    # Gibbs-White
    448: [1.0],    # Hennessey
    449: [5.0],    # Horvath
    450: [77.0],    # Johnson
    451: [76.0],    # Kouyate
    452: [0.0],    # Laryea
    453: [0.0],    # Mangala
    454: [0.0],    # Mbe Soh
    455: [82.0],    # McKenna
    456: [0.0],    # Mighten
    457: [0.0],    # Niakhate
    458: [0.0],    # O'Brien
    459: [0.0],    # Ojeda
    460: [0.0],    # Panzo
    461: [0.0],    # Richards
    462: [0.0],    # Scarpa
    463: [0.0],    # Shelvey
    464: [0.0],    # Surridge
    465: [34.0],    # Toffolo
    466: [0.0],    # Ui-Jo
    467: [73.0],    # N.Williams
    468: [55.0],    # Wood
    469: [78.0],    # Worrall
    470: [78.0],    # Yates
# Sheffield United 
    471: [78.0],    # Ahmedhodzic
    472: [0.0],    # Amissah
    473: [77.0],    # Baldock
    474: [74.0],    # Basham
    475: [80.0],    # Berge
    476: [0.0],    # Bogle
    477: [0.0],    # Brewster
    478: [0.0],    # Coulibaly
    479: [1.0],    # Davies
    480: [85.0],    # Egan
    481: [67.0],    # Fleck
    482: [89.0],    # Foderingham
    483: [0.0],    # Jebbison
    484: [72.0],    # Lowe
    485: [65.0],    # McBurnie
    486: [65.0],    # Ndiaye
    487: [0.0],    # Norrington-Davies
    488: [77.0],    # Norwood
    489: [75.0],    # Osborn
    490: [80.0],    # Osula
    491: [0.0],    # Austin
    574: [77.0],    # B.Traore
    587: [20.0],    # Slimane
    576: [75.0],    # Jack Robinson 
# Spurs
    492: [12.0],    # Bentancur
    493: [75.0],    # Bissouma
    494: [8.0],    # Bryan
    495: [12.0],    # Davies
    496: [78.0],    # Dier
    497: [67.0],    # Emerson Royal
    498: [1.0],    # Forster
    499: [35.0],    # Hojberg
    500: [0.0],    # Kane
    501: [72.0],    # Kulusevski
    502: [1.0],    # LLoris
    503: [2.0],    # Lo Celso
    504: [79.0],    # Maddison
    505: [12.0],    # Ndombele
    506: [62.0],    # Pedro Porro
    507: [45.0],    # Perisic
    508: [0.0],    # Reguillon  
    509: [77.0],    # Richarlison
    510: [0.0],    # Rodon
    511: [75.0],    # Romero
    512: [24.0],    # Sanchez
    513: [0.0],    # Sarr
    514: [15.0],    # R.Sessegnon
    515: [65.0],    # Skipp
    516: [77.0],    # Son
    517: [18.0],    # Spence
    518: [0.0],    # Tanganga
    519: [75.0],    # Udogie
    520: [89.0],    # Vicario
    521: [0.0],    # Whiteman
# West Ham
    522: [80.0],    # Aguerd
    523: [66.0],    # Antonio
    524: [85.0],    # Areola
    525: [65.0],    # Benrahma
    526: [79.0],    # Bowen
    527: [35.0],    # Cornet
    528: [75.0],    # Coufal
    529: [0.0],    # Coventry
    530: [15.0],    # Cresswell
    531: [0.0],    # Downes
    532: [45.0],    # Emerson
    533: [5.0],    # Fabianski
    534: [72.0],    # Fornals
    535: [50.0],    # Ings
    536: [45.0],    # Johnson
    537: [23.0],    # Kehrer
    538: [15.0],    # Mubama
    539: [80.0],    # Paqueta
    541: [5.0],    # Scamacca
    542: [77.0],    # Soucek
    543: [24.0],    # Vlasic
    544: [82.0],    # Zouma
# Wolves
    545: [73.0],    # Ait-Nouri
    546: [0.0],    # Bentley
    547: [0.0],    # Bolla
    548: [25.0],    # Bueno
    549: [24.0],    # Chiquinho
    550: [0.0],    # Cundle
    551: [77.0],    # Dawson
    552: [15.0],    # Fabio silva

    554: [7.0],    # Guedes
    555: [0.0],    # Hodge
    556: [0.0],    # Hoever
    557: [52.0],    # Hwang
    559: [0.0],    # Joao Gomes
    560: [15.0],    # Jonny
    561: [0.0],    #  Jordao
    562: [10.0],    # Kalajdzic
    563: [83.0],    # Kilman
    564: [0.0],    # King
    565: [74.0],    # Lemina
    566: [80.0],    # Matheus Nunes
    567: [75.0],    # Neto
    568: [67.0],    # Podence
    569: [89.0],    # Sa
    570: [70.0],    # Sarabia
    571: [1.0],    # Sarkic
    572: [78.0],    # Semedo
    573: [37.0],    # Toti
# extra
      
    577: [0.0],    # Ogbonna

    
    580: [0.0],    # Karius
    581: [0.0],    # Dummet
    583: [30.0],    # Solomon
    
    
    590: [62.0],    # Cunha
    
    592: [0.0],    # Larouci
    593: [0.0],    # T.Benie

    598: [63.0],    # Doherty
    
    614: [89.0],    # Kaminski
    603: [62.0],    # Barnes
    604: [32.0]    # Aina
    
 }


def add_extra_players(master):
    n = 32
    master_extra = pd.DataFrame({'code': [222683, 118342, 168090, 578614, 189776, 183751, 250735, 435973, 482609, 517052, 213198, 424876, 432422, 201440, 233821, 487053, 184254, 244954, 202641, 243557, 487702, 223434, 174310, 208904, 165183, 82738, 244262, 156700, 229164, 91046, 54738, 476369], 
                                'first_name': ['Justin', 'Mark', 'Mahmoud', 'Enock', 'Samuel', 'Manuel Benson', 'Darko', 'Lyle', 'Malo', 'Nicolas', 'Christopher', 'Dominik', 'Sandro', 'Hwang', 'Anel', 'Destiny', 'Guglielmo', 'Pau', 'André', 'Moussa', 'Luca', 'Igor Julio', 'Elijah', 'Mads Juel', 'Amari\'i', 'Luke', 'Alfie', 'Carlton', 'Chiedozie', 'Cauley', 'Thomas', 'Issa'], 
                                'second_name': ['Kluivert', 'Flekken', 'Dahoud', 'Agyei', 'Bastien', 'Hedilazio', 'Churlinov', 'Foster', 'Gusto', 'Jackson', 'Nkunku', 'Szoboszlai', 'Tonali', 'Ui-jo', 'Ahmedhodžić', 'Udogie', 'Vicario', 'Torres', 'Onana', 'Diaby', 'Koleosho', 'dos Santos de Paulo', 'Adebayo', 'Andersen', 'Bell', 'Berry', 'Doughty', 'Morris', 'Ogbene', 'Woodrow', 'Kaminski', 'Kabore'], 
                                'web_name': ['Kluivert', 'Flekken', 'Dahoud', 'Agyei', 'Bastien', 'Benson', 'Churlinov', 'Foster', 'Gusto', 'N.Jackson', 'Nkunku', 'Szoboszlai', 'Tonali', 'Ui-jo', 'Ahmedhodžić', 'Udogie', 'Vicario', 'Pau', 'Onana', 'Diaby', 'Koleosho', 'Igor', 'Adebayo', 'Andersen', 'Bell', 'Berry', 'Doughty', 'Morris', 'Ogbene', 'Woodrow', 'Kaminski', 'Kabore'], 
                                '16-17': [np.NaN]*n, '17-18': [np.NaN]*n, '18-19': [np.NaN]*n, '19-20': [np.NaN]*n, '20-21': [np.NaN]*n, '21-22': [np.NaN]*n, '22-23': [np.NaN]*n,
                                'fbref': [np.NaN]*n,
                                'understat': [6963.0, 7047.0, 205.0, 5563.0, 1343.0, 7383.0, 7790.0, 7498.0, 9017.0, 10048.0, 3300.0, 9788.0, 7958.0, 7746.0, 10386.0, 8831.0, 8858.0, 6221.0, 10913.0, 6556.0, 10620.0, 7943.0, 11718.0, 11715.0, 11713.0, 11722.0, 11723.0, 11717.0, 11719.0, 11721.0, 11712.0, 9619.0],
                                'transfermarkt': [np.NaN]*n,
                                '23-24': [72.0, 101.0, 128.0, 156.0, 158.0, 159.0, 162.0, 168.0, 203.0, 211.0, 212.0, 309.0, 429.0, 466.0, 471.0, 519.0, 520.0, 584.0, 597.0, 599.0, 605.0, 606.0, 314.0, 315.0, 316.0, 317.0, 321.0, 326.0, 328.0, 340.0, 614.0, 602.0]})
    master = master.append(master_extra, ignore_index=True)
    return master


def exp_mins(main_df):
    mins = main_df['minutes'].to_list()
    mins = [i for i in mins if i != 0 ]
    if len(mins) > 0 and sum(mins) > 1350:
        return round(sum(mins)/len(mins), 2)
    else:
        return 15.0

def convert(lst):     
    return ' '.join(str(item) for item in lst)

home = {
    True: '(H): ',
    False: '(A): '
}

def produce_player_dfs(season, master_path, players_raw, teams, fixtures, horizon, next_gw):
    df = players_raw[season]
    teams2023 = teams[season]
    master = pd.read_csv(master_path)
    gws = list(range(next_gw, next_gw + horizon))
    ids2023 = []
    short_teams = []
    positions = []
    prices = []
    fix = [ [] for _ in range(horizon) ]
    xmins = [ [] for _ in range(horizon) ]
    dmins = [ [] for _ in range(horizon) ]
    likelihood = [ [] for _ in range(horizon) ]

    for row in range(master.shape[0]):
        try:
            df_aux = df[df['code']==master['code'].iloc[row]]
            id = df_aux['id'].iloc[0]
            ids2023.append(id)
        except:
            ids2023.append(np.NaN)
    master['23-24'] = ids2023

    master = master[~master['23-24'].isna()]
    master = add_extra_players(master)
    master.to_csv('master.csv')

    for row in range(master.shape[0]):
        df_aux = df[df['code']==master['code'].iloc[row]]
        id = df_aux['id'].iloc[0]
        '''
        url = 'https://fantasy.premierleague.com/api/element-summary/' + str(int(id)) + '/'
        main_df = pd.DataFrame(requests.get(url).json()['history'])
        '''
        '''
        try:
            main_df = pd.read_csv('../data/Fantasy-Premier-League/data/2022-23/players/' + master['first_name'].iloc[row] + '_' + master['second_name'].iloc[row] + '_' + str(int(master['22-23'].iloc[row])) + '/gw.csv')
            expected_mins = exp_mins(main_df)
        except:
            expected_mins = 15.0
        '''
        try:
            expected_mins = expected_minutes[id][0]
        except:
            expected_mins = 0.0
        tid = team_id(id, season, players_raw)
        short_teams.append(teams2023[teams2023['id']==tid]['short_name'].iloc[0])
        positions.append(df_aux['element_type'].iloc[0])
        prices.append(df_aux['now_cost'].iloc[0])
        for gw in gws:
            afix = []
            admins = []
            alikelihood = []
            fix_list = fixture_info2(tid, season, gw, fixtures, teams)
            for i in range(len(fix_list)):
                opp_team, was_home, kickoff_time, score1, score2 = fixture_info2(tid, season, gw, fixtures, teams)[i]
                afix.append(home[was_home] + teams2023[teams2023['name']==opp_team]['short_name'].iloc[0])
                admins.append(expected_mins)
                alikelihood.append(1)
            fix[gw-next_gw].append(convert(afix))
            dmins[gw-next_gw].append(convert(admins))
            likelihood[gw-next_gw].append(convert(alikelihood))
            xmins[gw-next_gw].append(avg(admins))

    master['Team'] = short_teams
    master['Pos'] = positions
    master['Price'] = prices

    for gw in gws:
        master[str(gw)+ '_fix'] = fix[gw-next_gw]
        master[str(gw)+ '_xmins'] = xmins[gw-next_gw]
        master[str(gw)+ '_dmins'] = dmins[gw-next_gw]
        master[str(gw)+ '_likelihood'] = likelihood[gw-next_gw]

    review_detailed = master.drop(['code', 'first_name', 'second_name', '16-17', '17-18', '18-19', '19-20', '20-21', '21-22', '22-23', 'fbref', 'understat', 'transfermarkt'], axis=1)
    review_detailed = review_detailed.rename(columns={'web_name': 'Name', '23-24': 'ID'})


    fpl_review = pd.DataFrame()
    pos = {
        1: 'G',
        2: 'D',
        3: 'M',
        4: 'F'
    }
    fpl_review['Pos'] = [pos[review_detailed['Pos'].iloc[x]] for x in range(review_detailed.shape[0])] 
    fpl_review['ID'] = [review_detailed['ID'].iloc[x] for x in range(review_detailed.shape[0])] 
    fpl_review['Name'] = [review_detailed['Name'].iloc[x] for x in range(review_detailed.shape[0])] 
    fpl_review['BV'] = [review_detailed['Price'].iloc[x] for x in range(review_detailed.shape[0])] 
    fpl_review['SV'] = [review_detailed['Price'].iloc[x] for x in range(review_detailed.shape[0])] 
    fpl_review['Team'] = [teams2023[teams2023['short_name']==review_detailed['Team'].iloc[x]]['name'].iloc[0] for x in range(review_detailed.shape[0])]
    for gw in gws:
        fpl_review[str(gw)+ '_xMins'] = [review_detailed[str(gw)+ '_xmins'].iloc[x] for x in range(review_detailed.shape[0])] 
        fpl_review[str(gw)+ '_Pts'] = [0] * review_detailed.shape[0]

    review_df = fpl_review

    return review_detailed, review_df


gws_left = 38
initial_spis2023 = {
        'Arsenal': [83.9]*gws_left,
        'Aston Villa': [79.3]*gws_left,
        'Brentford': [77.1]*gws_left,
        'Brighton': [80.9]*gws_left,
        'Bournemouth': [59.6]*gws_left,
        'Chelsea': [75.8]*gws_left,
        'Crystal Palace': [73.5]*gws_left,
        'Everton': [63.6]*gws_left,
        'Sheffield Utd': [52.4]*gws_left,
        'Luton': [49.5]*gws_left,
        'Liverpool': [83.9]*gws_left,
        'Man City': [92.0]*gws_left,
        'Man Utd': [79.1]*gws_left,
        'Newcastle': [83.7]*gws_left,
        'Fulham': [68.2]*gws_left,
        'Burnley': [56.1]*gws_left,
        'Spurs': [72.1]*gws_left,
        'Nott\'m Forest': [56.1]*gws_left,
        'West Ham': [71.1]*gws_left,
        'Wolves': [59.1]*gws_left
    }


def compute_new_spis(spi_model, teams, team_stats_dict, fixtures, season, next_gw):
    if next_gw == 1:
        return initial_spis2023
    with open('spis.pkl', 'rb') as f:
        old_spis = pickle.load(f)
    t = teams[season]
    new_spis = {}
    gws_left = 38 - next_gw + 1

    for team in t['name'].to_list():
        tid = t[t['name']==team]['id'].iloc[0]
        opp_team, home, kickoff_time, score1, score2 = fixture_info2(tid, season, next_gw-1, fixtures, teams)[0]
        old_spi_team = old_spis[team][0]
        old_spi_opp_team = old_spis[opp_team][0]
        df = team_stats_dict[season][team].loc[0]
        xg1 = df['xG']
        xg2 = df['xGA']
        new_spi = spi_model.predict([[old_spi_team, old_spi_opp_team, score1, score2, xg1, xg2, home]])[0]
        new_spis[team] = [old_spi_team] + [new_spi]*gws_left
    with open('spis.pkl', 'wb') as f:
        pickle.dump(new_spis, f)



