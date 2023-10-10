import pandas as pd
import requests
import numpy as np
from modules.useful_functions import team_id, fixture_info2, avg
import pickle
from datetime import datetime
from zoneinfo import ZoneInfo
from modules.useful_functions import convert_date


expected_minutes = {
# Arsenal
    1: [0.0],  # Balogun
    2: [0.0],  # Cedric
    3: [3.0],  # Elneny
    4: [50.0],  # Vieira
    5: [77.0],  # Gabriel
    6: [60.0],  # Havertz
    7: [3.0],  # Holding
    8: [75.0],  # Jesus
    9: [10.0],  # Jorginho
    10: [12.0], # Kiwior
    11: [0.0], # Marquinhos
    12: [73.0], # Martinelli        
    13: [65.0], # Nketiah
    14: [84.0], # Odegaard
    15: [55.0], # Partey        FIXXXXXXX
    16: [3.0], # Pepe
    17: [5.0], # Ramsdale
    113: [85.0],    # Raya
    18: [0.0], # Runaarsson
    19: [75.0], # Saka              FIXXXX              
    20: [85.0], # Saliba                
    21: [5.0], # Sambi
    22: [7.0], # Smith Rowe
    23: [1.0], # Tavares
    24: [0.0], # Tierney
    25: [0.0], # Tomiyasu
    26: [25.0], # Trossard
    27: [0.0],  # Trusty
    29: [84.0], # White
    30: [0.0], # Xhaka
    31: [76.0], # Zinchenko
    578: [11.0],    # Nelson
    540: [85.0],    # Rice                  
    585: [0.0],    # J.Timber
    646: [0.0],    # Hein
# Aston Villa
    686: [0.0], # Zych
    699: [5.0], # Lenglet
    32: [0.0], # Alex Moreno                    FIXXXXX
    34: [55.0], # Bailey                            FIXXXXX
    35: [15.0], # Buendia
    36: [80.0], # Cash
    37: [4.0], # Chambers
    38: [15.0], # Coutinho
    39: [0.0], # Davis
    40: [0.0], # Dendoncker
    41: [0.0], # Diego Carlos
    42: [75.0], # Digne 
    43: [80.0], # Douglas Luiz
    44: [4.0], # Duran
    45: [8.0], # Hause 
    46: [0.0], # Iroegbunam
    47: [75.0], # Kamara                FIXXXX
    48: [77.0], # Konsa
    49: [89.0], # Martinez
    50: [78.0], # McGinn
    51: [0.0], # Mings
    53: [1.0], # Olsen
    54: [0.0], # Philogene-Bidace
    55: [0.0], # Ramsey                 FIXXXX
    56: [0.0], # Sanson
    57: [0.0], # Sinisalo
    58: [10.0], # Tielemans
    59: [10.0], # Traore
    60: [86.0], # Watkins
    61: [0.0], # Wesley
    584: [78.0],    # Pau Torres
    599: [75.0],    # Diaby             FIXXXXX
    618: [0.0],    # Kellyman
    670: [0.0],    # Marschall
    672: [55.0],    # Zaniolo
# Bournemouth
    705: [0.0], # Sinisterra
    62: [3.0], # Anthony
    63: [75.0], # Billing
    64: [22.0], # Brooks
    65: [64.0], # Christie
    66: [77.0], # Cook
    67: [12.0], # Dembele
    68: [4.0], # Fredericks
    69: [0.0], # Hill
    70: [0.0], # Kelly              FIXXXX
    71: [0.0], # Kilkenny
    72: [60.0], # Kluivert
    73: [0.0], # Lowe
    74: [0.0], # Marcondes
    75: [0.0], # Mepham
    76: [0.0], # Moore
    77: [89.0], # Neto
    78: [35.0], # Ouattara
    79: [0.0], # Pearson
    80: [0.0], # Randolph
    81: [7.0], # Rothwell
    82: [10.0], # Semenyo
    83: [22.0], # Senesi
    84: [12.0], # Smith
    85: [88.0], # Solanke           
    86: [72.0], # Tavernier
    87: [12.0], # H.Traore
    88: [0.0], # Travers
    89: [78.0], # Zabarnyi
    595: [77.0],    # Kerkez
    607: [1.0],    # Radu
    619: [0.0],    # Ben Greenwood
    643: [77.0],    # Aarons
    644: [0.0],    # Scott
    673: [0.0],    # Tyler Adams
# Brentford
    90: [6.0], # Ajer
    701: [15.0], # Ghoddos
    91: [0.0], # Balcombe
    92: [11.0], # Baptiste
    93: [0.0], # Bech
    94: [0.0], # Bidstrup
    95: [55.0], # Canos
    96: [82.0], # Collins
    97: [0.0], # Cox
    98: [47.0], # Damsgaard
    99: [23.0], # Dasilva
    100: [0.0],  # Dervisoglu
    101: [0.0],    # Flekken        FIXXXXX
    102: [0.0],    # Goode
    103: [0.0],    # Henry          FIXXXXX
    104: [75.0],    # Hickey
    105: [74.0],    # Janelt
    106: [75.0],    # Jensen
    107: [0.0],    # Lewis-Potter
    108: [83.0],    # Mbeumo
    109: [65.0],    # Mee
    110: [77.0],    # Norgaard
    111: [12.0],    # Onyeka
    112: [85.0],    # Pinnock
    114: [0.0],    # Roerslev
    115: [0.0],    # Schade
    116: [85.0],    # Strakosha
    117: [0.0],    # Toney
    118: [0.0],    # Trevitt
    119: [75.0],    # Wissa
    120: [0.0],    # Yarmolyuk
    121: [3.0],    #Zanka
    620: [0.0],    # Olakigbe
# Brighton
    122: [55.0],    # Adingra
    123: [0.0],    # Alzate
    700: [50.0],     # Fati
    124: [0.0],    # Ayari
    125: [22.0],    # Buonanotte
    127: [3.0],    # Connolly
    128: [40.0],    # Dahoud
    129: [84.0],    # Dunk
    130: [0.0],    # Enciso
    131: [0.0],    # Estupinan
    132: [50.0],    # Ferguson
    133: [64.0],    # Gilmour
    134: [75.0],    # Gross                  
    135: [52.0],    # Joao Pedro
    136: [0.0],    # Karbownik
    137: [0.0],    # Kozlowski
    138: [0.0],    # Lallana                FIXXXX
    139: [60.0],    # Lamptey
    140: [63.0],    # March
    141: [0.0],    # McGill
    142: [0.0],    # Milner                    FIXXXXXXX
    143: [73.0],    # Mitoma
    144: [0.0],    # Moder
    146: [12.0],    # Sarmiento
    147: [0.0],    # Scherpen
    148: [30.0],    # Steele
    149: [0.0],    # Undav
    150: [60.0],    # Van Hecke
    151: [60.0],    # Veltman
    152: [60.0],    # Verbruggen
    153: [52.0],    # Webster
    154: [58.0],    # Wellbeck
    155: [0.0],    # Zeqiri
    606: [32.0],    # Igor
    621: [0.0],    # Hinshelwood
# Burnley
    156: [0.0],    # Agyei
    706: [12.0],     # M.Tressor
    674: [0.0],     # Delcroix
    179: [0.0],     # Thomas
    675: [62.0],     # Ramsey
    157: [80.0],    # Al-Dakhil
    158: [0.0],    # Bastien
    159: [0.0],    # Benson         FIXXXX
    160: [69.0],    # Beyer
    161: [73.0],    # Brownhill
    162: [0.0],    # Churlinov
    163: [15.0],    # Cork
    164: [0.0],    # Costelloe
    165: [85.0],    # Cullen
    166: [0.0],    # Egan-Riley    
    167: [0.0],    # Ekdal
    168: [75.0],    # Foster        
    169: [0.0],    # Franchi    
    170: [50.0],    # Gudmundsson
    171: [0.0],    # McNally
    172: [1.0],    # Muric
    173: [82.0],    # O'Shea
    174: [11.0],    # Obafemi
    175: [0.0],    # Peacock-Farrell
    176: [79.0],    # Roberts
    177: [25.0],    # Rodriguez
    178: [79.0],    # Taylor
    179: [0.0],    # Thomas
    180: [0.0],    # Twine
    181: [0.0],    # Vigouroux
    182: [6.0],    # Vitinho
    183: [0.0],    # Weghorst
    184: [30.0],    # Zaroury
    185: [0.0],    # Ampadu
    186: [0.0],    # Andrey Santos
    594: [64.0],    # Amdouni
    600: [15.0],    # Redmond
    596: [89.0],    # Trafford
    605: [65.0],    # Koleosho
    608: [15.0],    # Bruun Larsen
    622: [0.0],    # Dodgson
    660: [0.0],    # Odobert
# Chelsea
    145: [89.0],    # Sanchez
    126: [77.0],    # Caicedo
    187: [0.0],    # Arrizabalaga
    188: [0.0],    # Aubameyang
    189: [0.0],    # Azpilicueta
    190: [0.0],    # Baba Rahman
    191: [0.0],    # Badiashile
    192: [0.0],    # Bettinelli
    193: [45.0],    # Broja
    194: [0.0],    # Chalobah
    195: [0.0],    # Chilwell               FIXXX
    362: [68.0],    # Palmer
    196: [0.0],    # Chukwuemeka
    197: [82.0],    # Colwill
    198: [60.0],    # Cucurella
    199: [85.0],    # Enzo
    200: [0.0],    # D.D.Fofana
    201: [0.0],    # W.Fofana
    202: [77.0],    # Gallagher
    203: [0.0],    # Gusto                  FIXXXX
    205: [0.0],    # Hudson-Odoi
    206: [0.0],    # James
    207: [0.0],    # Lukaku
    208: [0.0],    # Madueke
    210: [60.0],    # Mudryk
    211: [62.0],    # N.Jackson
    212: [0.0],    # Nkunku
    213: [0.0],    # Pulisic
    214: [0.0],    # Sarr
    215: [0.0],    # Slonina
    216: [75.0],    # Sterling
    217: [87.0],    # Thiago Silva
    218: [0.0],    # Ziyech
    589: [0.0],    # Angelo
    609: [5.0],    # Maatsen
    611: [82.0],    # Disasi 
    613: [17.0],    # Ugochukwu
    623: [2.0],    # Burtsow
    659: [0.0],    # Bergstrom
    667: [0.0],    # Lavia
    671: [0.0],    # Humphreys
# Crystal Palace
    219: [0.0],    # Ahamada
    220: [85.0],    # Andersen
    221: [77.0],    # J.Ayew
    222: [72.0],    # Clyne
    223: [65.0],    # C.Doucoure
    224: [0.0],    # Ebiowei
    225: [75.0],    # Edouard                    
    226: [0.0],    # Eze
    227: [1.0],    # Guaita
    228: [85.0],    # Guehi
    229: [45.0],    # Hughes
    230: [85.0],    # Johnstone
    385: [0.0],    # Henderson
    231: [0.0],    # Lerma                       FIXXXX
    232: [50.0],    # Mateta                    FIXXXXXXX
    233: [0.0],    # Matthews
    234: [77.0],    # Mitchell
    235: [0.0],    # O'Brien
    236: [0.0],    # Olise
    237: [0.0],    # Plange
    238: [0.0],    # Richards
    239: [0.0],    # Riedewald
    240: [74.0],    # Schlupp
    241: [32.0],    # Tomkins                   FIXXXX
    242: [77.0],    # Ward
    243: [0.0],    # Whitworth
    615: [0.0],    # Matheus de Oliveira
    657: [30.0],    # Rak-Sakyi
    658: [0.0],    # Gordon
# Everton
    244: [24.0],    # Andre Gomes
    245: [34.0],    # Branthwaite
    246: [72.0],    # Calvert-Lewin
    247: [73.0],    # Coleman
    248: [0.0],    # Dele
    249: [83.0],    # A.Doucoure
    250: [0.0],    # Garner
    251: [0.0],    # Gbamin
    252: [22.0],    # Godfrey
    253: [0.0],    # Gray
    691: [20.0],     # Beto
    254: [74.0],    # Gueye
    255: [13.0],    # Holgate
    257: [80.0],    # Keane
    258: [35.0],    # Maupay
    259: [75.0],    # McNeil
    260: [65.0],    # Mykolenko
    261: [77.0],    # Onana
    262: [67.0],    # Patterson
    263: [89.0],    # Pickford
    264: [3.0],    # Simms
    265: [82.0],    # Tarkowski
    266: [0.0],    # Virginia
    579: [0.0],    # Lonergan
    588: [74.0],    # Young
    601: [65.0],    # Danjuma
    624: [0.0],    # Dobbin
    645: [0.0],    # Chermiti
    649: [0.0],    # Cannon
    650: [0.0],    # Onyango
    661: [0.0],    # Harrison
# Fulham
    267: [83.0],    # Andreas
    683: [0.0],     # Harris
    688: [74.0],    # Castagne
    256: [35.0],    # Iwobi
    268: [25.0],    # Cairney
    269: [0.0],    # Cavaleiro
    270: [75.0],    # De Cordova-Reid
    271: [84.0],    # Diop
    272: [0.0],     # Francois
    273: [0.0],     # Knockaert
    274: [0.0],     # Kongolo
    275: [89.0],    # Leno
    276: [1.0],     # Lukic
    277: [12.0],    # Mbabu
    278: [0.0],    # Mitrovic
    279: [0.0],     # Muniz
    280: [85.0],    # Palinha
    281: [72.0],    # Ream
    282: [64.0],    # Reed
    283: [75.0],    # Robinson
    284: [1.0],     # Rodak
    285: [0.0],    # Tete           FIXXXX
    286: [0.0],    # Tosin          FIXXX
    287: [20.0],    # Vinicius
    288: [70.0],    # Wilson
    558: [63.0],    # Jimenez
    591: [53.0],    # Willian
    610: [18.0],    # Bassey
    625: [0.0],    # De Fugerolles
    651: [0.0],    # Stansfield
    652: [0.0],    # Dibley-Dias
    662: [0.0],    # Adama Traore       FIXXXX
# Liverpool
    289: [0.0],     # Adrian
    290: [85.0],    # Alexander-Arnold      FIXXXX
    291: [89.0],    # Alisson
    292: [0.0],    # Bajcetic      
    708: [15.0],     # Gravenberch
    293: [55.0],    # Darwin                FIXXXX
    294: [0.0],    # Diogo Jota             FIXXXX
    295: [13.0],    # Eliott
    296: [0.0],     # Fabinho
    297: [65.0],    # Gakpo
    298: [12.0],    # Gomez
    299: [0.0],     # Henderson
    300: [43.0],    # Jones
    301: [1.0],    # Kelleher
    302: [10.0],    # Konate
    303: [62.0],    # Luis Diaz
    304: [72.0],    # Mac Allister
    305: [75.0],    # Matip
    306: [0.0],    # Phillips
    307: [80.0],    # Robertson
    308: [87.0],    # Salah
    309: [78.0],    # Szoboszlai  
    310: [15.0],    # Thiago
    311: [8.0],    # Tsimikas
    312: [0.0],    # Van den Berg
    313: [85.0],    # Van Dijk
    626: [0.0],    # Quansah
    627: [0.0],    # Clark
    628: [0.0],    # Doak
    629: [0.0],    # McConnell
    668: [0.0],    # Wataru Endo
# Luton
    52: [84.0],     # Nakamba
    314: [55.0],    # Adebayo
    315: [5.0],    # Andersen
    316: [84.0],    # Bell
    317: [0.0],    # Burry
    318: [77.0],    # Burke
    319: [75.0],    # Campbell
    320: [0.0],    # Clark          FIXXXX
    321: [55.0],    # Doughty
    322: [0.0],    # Freeman
    323: [0.0],    # Macey
    324: [0.0],    # McAtee
    325: [0.0],    # Mendes
    326: [75.0],    # Morris
    582: [37.0],    # Mpanzu
    586: [55.0],    # Chong
    602: [73.0],    # Kabore
    327: [0.0],    # Muskwe
    328: [55.0],    # Ogbene
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
    340: [15.0],    # Woodrow
    553: [17.0],    # Giles
    575: [85.0],    # Lockyer
    614: [89.0],    # Kaminski
    630: [5.0],    # Barkley
    631: [55.0],    # Brown
    648: [0.0],    # Francis-Clarke
    665: [0.0],    # Krul
# Man City
    341: [65.0],    # Akanji
    342: [63.0],    # Ake
    343: [75.0],    # Alvarez
    344: [0.0],    # Bernardo
    345: [0.0],    # Bobb
    346: [0.0],    # Cancelo
    347: [0.0],    # Carson
    348: [0.0],    # Charles
    349: [0.0],    # De Bruyne
    350: [78.0],    # Dias
    351: [0.0],    # Doyle
    352: [89.0],    # Ederson
    353: [74.0],    # Foden
    354: [50.0],    # Grealish
    566: [65.0],    # Matheus Nunes
    355: [88.0],    # Haaland
    678: [60.0],     # Doku
    356: [60.0],    # Kovacic
    357: [0.0],    # Laporte
    358: [24.0],    # Lewis
    359: [0.0],    # Mahrez
    360: [4.0],    # McAtee
    361: [1.0],    # Ortega
    363: [0.0],    # Perrone
    364: [5.0],    # Phillips              
    365: [85.0],    # Rodri                  
    366: [10.0],    # Sergio Gomez
    367: [0.0],    # Steffen
    368: [60.0],    # Stones
    369: [76.0],    # Walker
    616: [65.0],    # Gvardiol
# Man United
    370: [12.0],    # Telles
    371: [0.0],    # Amad
    372: [50.0],    # Antony                FIXXXX
    373: [88.0],    # Fernandes
    209: [0.0],    # Mount
    374: [0.0],    # B.Williams
    375: [0.0],    # Bailly
    376: [82.0],    # Casemiro
    377: [82.0],    # Dalot
    379: [63.0],    # Eriksen
    380: [0.0],    # Alvaro Fernandez
    381: [45.0],    # Fred
    382: [60.0],    # Garnacho
    383: [55.0],    # Hannibal Mejbri
    384: [0.0],    # Heaton
    386: [75.0],    # Lindelof
    387: [0.0],    # Maguire
    703: [13.0],     # Evans
    388: [0.0],    # Mainoo
    389: [23.0],    # Malacia
    390: [65.0],    # Martial
    391: [0.0],    # Martinez
    392: [22.0],    # McTominay
    393: [0.0],    # Mengi
    394: [64.0],    # Pellistri
    395: [80.0],    # Varane
    396: [84.0],    # Rashford
    709: [45.0],     # Amrabat
    397: [0.0],    # Sancho
    398: [0.0],    # Shaw
    508: [0.0],    # Reguillon           FIXXXX
    399: [0.0],    # Shoretire
    400: [0.0],    # Van de Beek
    401: [0.0],    # Wan-Bissaka
    597: [89.0],    # Onana
    617: [76.0],    # Hojlund
    632: [0.0],    # Forson
    669: [0.0],    # Vitek
# Newcastle
    402: [71.0],    # Almiron
    403: [45.0],    # Anderson
    404: [0.0],    # Ashby
    405: [0.0],    # Botman                   FIXXXX                      
    406: [85.0],    # Bruno Guimaraes
    407: [84.0],    # Burn
    204: [60.0],    # Hall
    408: [0.0],    # Darlow
    409: [1.0],    # Dubravka
    410: [8.0],    # Fraser
    411: [0.0],    # Gillespie
    412: [0.0],    # Gordon             FIXXXX SUSP
    413: [0.0],    # Hayden
    414: [0.0],    # Hendrick
    415: [70.0],    # Isak              FIXXXXX
    416: [75.0],    # Joelinton
    417: [0.0],    # Krafth
    418: [0.0],    # Kuol
    419: [65.0],    # Lascelles         FIXXXXX
    420: [0.0],    # Lewis
    421: [60.0],    # S.Longstaff
    422: [0.0],    # Manquillo
    423: [27.0],    # Murphy
    424: [89.0],    # Pope
    425: [0.0],    # Ritchie
    426: [0.0],    # Saint-Maximin
    427: [85.0],    # Schar
    428: [12.0],    # Targett
    429: [70.0],    # Tonali
    430: [87.0],    # Trippier
    431: [0.0],    # Watts
    432: [25.0],    # Willock    
    433: [25.0],    # Wilson            FIXXX
    633: [15.0],    # Livramento
    634: [0.0],    # Alex Murphy
    635: [0.0],    # Miley
# Nottingham Forest
    378: [60.0],    # Elanga
    28: [75.0],     # Turner
    434: [0.0],    # B.Aguilera
    435: [0.0],    # Arter
    436: [73.0],    # Aurier
    437: [0.0],    # Awoniyi            FIXXXX
    438: [0.0],    # Biancone
    439: [78.0],    # Boly
    440: [0.0],    # Bowler
    441: [0.0],    # Cook
    442: [2.0],    # Danilo
    443: [0.0],    # Dennis
    444: [0.0],    # Drager
    445: [0.0],    # Felipe
    446: [0.0],    # Freuler
    447: [80.0],    # Gibbs-White
    679: [12.0],     # Montiel
    710: [15.0],     # Vlachodimos
    713: [60.0],     # Sangare
    711: [0.0],     # Omobamidelle
    714: [20.0],     # Origi
    448: [0.0],    # Hennessey
    449: [0.0],    # Horvath
    451: [26.0],    # Kouyate
    452: [0.0],    # Laryea
    453: [68.0],    # Mangala
    454: [0.0],    # Mbe Soh
    455: [0.0],    # McKenna
    456: [0.0],    # Mighten
    457: [65.0],    # Niakhate
    458: [0.0],    # O'Brien
    459: [0.0],    # Ojeda
    460: [0.0],    # Panzo
    461: [0.0],    # Richards
    462: [0.0],    # Scarpa
    463: [0.0],    # Shelvey
    464: [0.0],    # Surridge
    465: [34.0],    # Toffolo
    466: [0.0],    # Ui-Jo
    467: [0.0],    # N.Williams
    468: [67.0],    # Wood              FIXXXX
    469: [0.0],    # Worrall
    470: [58.0],    # Yates
    636: [0.0],    # Shelvey
    637: [0.0],    # Powell
# Sheffield United 
    471: [78.0],    # Ahmedhodzic
    472: [0.0],    # Amissah
    473: [0.0],    # Baldock
    474: [80.0],    # Basham
    475: [50.0],    # Berge
    476: [0.0],    # Bogle
    477: [0.0],    # Brewster
    478: [0.0],    # Coulibaly
    479: [1.0],    # Davies
    480: [85.0],    # Egan
    481: [67.0],    # Fleck
    482: [89.0],    # Foderingham
    483: [0.0],    # Jebbison
    484: [62.0],    # Lowe
    485: [70.0],    # McBurnie
    486: [55.0],    # Ndiaye
    487: [0.0],    # Norrington-Davies
    488: [74.0],    # Norwood
    489: [55.0],    # Osborn
    490: [15.0],    # Osula
    33: [78.0], # Archer
    491: [0.0],    # Austin
    587: [20.0],    # Slimane
    576: [75.0],    # Jack Robinson 
    638: [65.0],    # Vini de Souza Costa
    653: [0.0],    # Seriki
    654: [0.0],    # Marsh
    655: [0.0],    # Brooks
    656: [0.0],    # Hackford
    663: [60.0],    # Hamer
    666: [17.0],    # Davies
# Spurs
    492: [0.0],    # Bentancur
    493: [79.0],    # Bissouma
    494: [8.0],    # Bryan
    495: [5.0],    # Davies
    496: [5.0],    # Dier
    497: [20.0],    # Emerson Royal
    498: [1.0],    # Forster
    499: [15.0],    # Hojberg
    500: [0.0],    # Kane
    501: [78.0],    # Kulusevski
    502: [0.0],    # LLoris
    503: [0.0],    # Lo Celso
    504: [85.0],    # Maddison
    583: [0.0],    # Solomon            FIXXXX
    450: [0.0],    # Johnson            FIXXXX
    505: [0.0],    # Ndombele
    506: [76.0],    # Pedro Porro
    507: [0.0],    # Perisic  
    509: [67.0],    # Richarlison       FIXXX
    510: [0.0],    # Rodon
    511: [84.0],    # Romero
    512: [0.0],    # Sanchez
    513: [72.0],    # Sarr
    514: [0.0],    # R.Sessegnon
    515: [60.0],    # Skipp
    516: [75.0],    # Son               FIXXXXXX
    517: [0.0],    # Spence
    518: [0.0],    # Tanganga
    519: [80.0],    # Udogie
    520: [89.0],    # Vicario
    521: [0.0],    # Whiteman
    639: [78.0],    # Van de Ven
    640: [0.0],    # Scarlett
    641: [2.0],    # Veliz
# West Ham
    577: [5.0],    # Ogbonna
    522: [85.0],    # Aguerd
    523: [55.0],    # Antonio           FIXXXXX
    524: [89.0],    # Areola
    525: [35.0],    # Benrahma
    526: [84.0],    # Bowen
    689: [30.0],     # Kudus
    527: [10.0],    # Cornet
    528: [77.0],    # Coufal
    529: [0.0],    # Coventry
    530: [15.0],    # Cresswell
    531: [0.0],    # Downes
    532: [77.0],    # Emerson
    533: [1.0],    # Fabianski
    534: [32.0],    # Fornals
    535: [10.0],    # Ings
    536: [0.0],    # Johnson
    537: [5.0],    # Kehrer
    538: [1.0],    # Mubama
    539: [86.0],    # Paqueta
    541: [5.0],    # Scamacca
    542: [82.0],    # Soucek
    543: [0.0],    # Vlasic
    544: [86.0],    # Zouma
    676: [5.0],     # Mavropanos
    642: [80.0],    # Alvarez
    647: [0.0],    # Anang
    664: [83.0],    # Ward prowse
# Wolves
    545: [76.0],    # Ait-Nouri
    704: [0.0],     # Fraser
    546: [0.0],    # Bentley
    547: [0.0],    # Bolla
    548: [12.0],    # Bueno
    549: [4.0],    # Chiquinho
    550: [0.0],    # Cundle
    551: [84.0],    # Dawson
    552: [35.0],    # Fabio silva
    554: [7.0],    # Guedes
    555: [0.0],    # Hodge
    556: [0.0],    # Hoever
    557: [68.0],    # Hwang
    559: [0.0],    # Joao Gomes
    560: [15.0],    # Jonny
    561: [0.0],    #  Jordao
    562: [10.0],    # Kalajdzic
    563: [83.0],    # Kilman
    564: [0.0],    # King
    565: [74.0],    # Lemina
    567: [84.0],    # Neto
    568: [0.0],    # Podence
    569: [89.0],    # Sa
    570: [55.0],    # Sarabia
    571: [1.0],    # Sarkic
    572: [80.0],    # Semedo
    573: [5.0],    # Toti
    598: [0.0],    # Doherty
    574: [5.0],    # B.Traore
    715: [0.0],     # Bellegarde
# extra
  
    580: [0.0],    # Karius
    581: [0.0],    # Dummet
    694: [0.0],     # Massengo

    677: [0.0],     # Deivid
    681: [0.0],     # D.Moreira
    697: [0.0],     # S.Bueno
    590: [66.0],    # Cunha
    
    592: [0.0],    # Larouci
    593: [0.0],    # T.Benie

    690: [0.0],     # Baleba
    603: [0.0],    # Barnes
    604: [69.0]    # Aina
    
 }


def add_extra_players(master, players_raw):
    n = 34
    master_extra = pd.DataFrame({'code': [108796, 492831, 222683, 118342, 168090, 578614, 189776, 183751, 250735, 435973, 482609, 517052, 213198, 424876, 432422, 201440, 233821, 487053, 184254, 244954, 202641, 243557, 487702, 223434, 174310, 208904, 165183, 82738, 244262, 156700, 229164, 91046, 54738, 476369], 
                                'first_name': ['Tom', 'Zeki', 'Justin', 'Mark', 'Mahmoud', 'Enock', 'Samuel', 'Manuel Benson', 'Darko', 'Lyle', 'Malo', 'Nicolas', 'Christopher', 'Dominik', 'Sandro', 'Hwang', 'Anel', 'Destiny', 'Guglielmo', 'Pau', 'André', 'Moussa', 'Luca', 'Igor Julio', 'Elijah', 'Mads Juel', 'Amari\'i', 'Luke', 'Alfie', 'Carlton', 'Chiedozie', 'Cauley', 'Thomas', 'Issa'], 
                                'second_name': ['Lockyer', 'Amdouni', 'Kluivert', 'Flekken', 'Dahoud', 'Agyei', 'Bastien', 'Hedilazio', 'Churlinov', 'Foster', 'Gusto', 'Jackson', 'Nkunku', 'Szoboszlai', 'Tonali', 'Ui-jo', 'Ahmedhodžić', 'Udogie', 'Vicario', 'Torres', 'Onana', 'Diaby', 'Koleosho', 'dos Santos de Paulo', 'Adebayo', 'Andersen', 'Bell', 'Berry', 'Doughty', 'Morris', 'Ogbene', 'Woodrow', 'Kaminski', 'Kabore'], 
                                'web_name': ['Lockyer', 'Amdouni', 'Kluivert', 'Flekken', 'Dahoud', 'Agyei', 'Bastien', 'Benson', 'Churlinov', 'Foster', 'Gusto', 'N.Jackson', 'Nkunku', 'Szoboszlai', 'Tonali', 'Ui-jo', 'Ahmedhodžić', 'Udogie', 'Vicario', 'Pau', 'Onana', 'Diaby', 'Koleosho', 'Igor', 'Adebayo', 'Andersen', 'Bell', 'Berry', 'Doughty', 'Morris', 'Ogbene', 'Woodrow', 'Kaminski', 'Kabore'], 
                                '16-17': [np.NaN]*n, '17-18': [np.NaN]*n, '18-19': [np.NaN]*n, '19-20': [np.NaN]*n, '20-21': [np.NaN]*n, '21-22': [np.NaN]*n, '22-23': [np.NaN]*n,
                                'fbref': [np.NaN]*n,
                                'understat': [11714.0, 11701.0, 6963.0, 7047.0, 205.0, 5563.0, 1343.0, 7383.0, 7790.0, 7498.0, 9017.0, 10048.0, 3300.0, 9788.0, 7958.0, 7746.0, 10386.0, 8831.0, 8858.0, 6221.0, 10913.0, 6556.0, 10620.0, 7943.0, 11718.0, 11715.0, 11713.0, 11722.0, 11723.0, 11717.0, 11719.0, 11721.0, 11712.0, 9619.0],
                                'transfermarkt': [np.NaN]*n,
                                '23-24': [575.0, 594.0, 72.0, 101.0, 128.0, 156.0, 158.0, 159.0, 162.0, 168.0, 203.0, 211.0, 212.0, 309.0, 429.0, 466.0, 471.0, 519.0, 520.0, 584.0, 597.0, 599.0, 605.0, 606.0, 314.0, 315.0, 316.0, 317.0, 321.0, 326.0, 328.0, 340.0, 614.0, 602.0]})
    master = master.append(master_extra, ignore_index=True)

    new_players = pd.read_csv('new_players_after6.csv')

    master = master.append(new_players, ignore_index=True)
    return master

'''
add new players

PART1

import numpy as np
pr = players_raw['2023-24']
next_gw = 7

last_proj = pd.read_csv('../Projections/ALEX-23/alex-GW' + str(next_gw-1) + '.csv')
new_players = pr[pr['id']>673][['code', 'first_name', 'second_name', 'web_name', 'id']].reset_index()
drop_ids = []
for i in range(new_players.shape[0]):
    if new_players['id'].iloc[i] in last_proj['ID'].to_list():
        print(new_players['web_name'].iloc[i])
        drop_ids.append(i)
        continue
new_players.drop(drop_ids, inplace=True)
new_players.drop(columns=['index'], inplace=True)
new_players


PART2
# Get the understat ids of the new players
understat_ids = [np.NaN, 10527, 7967, 11998, 7264, 12094, 4072, np.NaN, 11978, np.NaN, np.NaN, np.NaN, np.NaN, 9983, np.NaN, np.NaN, 10697, np.NaN, 8981, np.NaN, np.NaN, 7927, 9897, np.NaN, 375, np.NaN, 5722, np.NaN, 12027, 10945, np.NaN, 7762]

new_players.insert(4, '16-17', [np.NaN]*new_players.shape[0], True)
new_players.insert(5, '17-18', [np.NaN]*new_players.shape[0], True)
new_players.insert(6, '18-19', [np.NaN]*new_players.shape[0], True)
new_players.insert(7, '19-20', [np.NaN]*new_players.shape[0], True)
new_players.insert(8, '20-21', [np.NaN]*new_players.shape[0], True)
new_players.insert(9, '21-22', [np.NaN]*new_players.shape[0], True)
new_players.insert(10, '22-23', [np.NaN]*new_players.shape[0], True)
new_players.insert(11, 'fbref', [np.NaN]*new_players.shape[0], True)
new_players.insert(12, 'understat', understat_ids, True)
new_players.insert(13, 'transfermarkt', [np.NaN]*new_players.shape[0], True)
new_players.rename(columns={'id': '23-24'}, inplace=True)
new_players = new_players[new_players['understat'].notna()]

# Add new players df
'''

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
    master = add_extra_players(master, players_raw)
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
            print(id)
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



def compute_new_spis(spi_model, teams, team_stats_dict, fixtures, season, df, next_gw):
    if next_gw == 1:
        return initial_spis2023
    
    with open('spis.pkl', 'rb') as f:
        old_spis = pickle.load(f)
    if next_gw == 2:
        old_spis = initial_spis2023
    #old_spis = initial_spis2023
    t = teams[season]
    spis = {}

    gws_left = 38 - next_gw + 1

    for team in t['name'].to_list():
        tid = t[t['name']==team]['id'].iloc[0]
        #last_gw_fixtures = fixture_info2(tid, season, next_gw-1, fixtures, teams)
        #old_spis_list = old_spis[team][:next_gw-1]
        #new_spis[team] = old_spis_list + [old_spis_list[-1]]*gws_left
        x = 0
        xlist = []
        team_und = team_stats_dict[season][team]
        for x in range(team_und.shape[0]):
            if team_und.loc[x]['date'] > convert_date(df['deadline_time'].iloc[next_gw-2]) and team_und.loc[x]['date'] < convert_date(df['deadline_time'].iloc[next_gw-1]):
                 xlist.append(x)

        spi_dif = []
        for i in range(len(xlist)):
            opp_team, home, kickoff_time, score1, score2 = fixture_info2(tid, season, next_gw-1, fixtures, teams)[i]
            old_spi_team = old_spis[team][next_gw-2]
            old_spi_opp_team = old_spis[opp_team][next_gw-2]
            #df = team_stats_dict[season][team].loc[next_gw-2]
            xg1 = team_und.loc[xlist[i]]['xG']
            xg2 = team_und.loc[xlist[i]]['xGA']

            new_spi = spi_model.predict([[old_spi_team, old_spi_opp_team, score1, score2, xg1, xg2, home]])[0]
            spi_dif.append(new_spi - old_spi_team)
            spis[team] = old_spis[team][:next_gw-1] + [old_spi_team + sum(spi_dif)]*gws_left
        
        if len(xlist) == 0:
            spis[team] = old_spis[team]

    with open('spis.pkl', 'wb') as f:
        pickle.dump(spis, f)
    return spis

def spis_from_season_beginning(strengths, teams, team_stats_dict, fixtures, season, df, next_gw):
    for gw in range(2,next_gw+1):
        spis = compute_new_spis(strengths, teams, team_stats_dict, fixtures, season, df, gw)
    return spis

def get_next_gw():
    now = datetime.now(ZoneInfo('Europe/London'))
    dt_string = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    df = pd.DataFrame(requests.get(url).json()['events'])
    i=0
    while dt_string > df['deadline_time'].iloc[i]:
        i = i + 1
    next_gw = df['id'].iloc[i]
    return next_gw
