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
    1: [0.0],    # Balogun
    2: [0.0],   # Cedric
    3: [3.0],  # Elneny
    4: [20.0],  # Vieira
    5: [85.0],  # Gabriel
    6: [65.0],  # Havertz               
    7: [0.0],  # Holding
    8: [15.0],  # Jesus                  
    9: [30.0],  # Jorginho
    10: [35.0], # Kiwior
    11: [0.0], # Marquinhos
    12: [70.0], # Martinelli        
    13: [75.0], # Nketiah               
    14: [85.0], # Odegaard               
    15: [0.0], # Partey                 INJJ    
    16: [3.0], # Pepe
    17: [3.0], # Ramsdale
    113: [87.0],    # Raya
    18: [0.0], # Runaarsson
    19: [85.0], # Saka                  FIXX                       
    20: [88.0], # Saliba                          
    21: [5.0], # Sambi
    22: [0.0], # Smith Rowe             INJURED
    23: [1.0], # Tavares
    24: [0.0], # Tierney
    25: [50.0], # Tomiyasu               INJURED
    26: [35.0], # Trossard              FIXXX
    29: [80.0], # White
    30: [0.0], # Xhaka
    31: [58.0], # Zinchenko
    578: [11.0],    # Nelson
    540: [85.0],    # Rice                  
    585: [0.0],    # J.Timber
    646: [0.0],    # Hein
# Aston Villa
    686: [0.0], # Zych
    699: [15.0], # Lenglet
    32: [55.0], # Alex Moreno                    
    34: [65.0], # Bailey                        
    35: [0.0], # Buendia
    36: [20.0], # Cash                          FIXXXXX
    37: [4.0], # Chambers
    38: [0.0], # Coutinho
    39: [0.0], # Davis
    40: [0.0], # Dendoncker
    41: [20.0], # Diego Carlos
    42: [0.0], # Digne 
    43: [85.0], # Douglas Luiz
    44: [4.0], # Duran
    45: [0.0], # Hause 
    46: [0.0], # Iroegbunam
    47: [0.0], # Kamara                 susp            
    48: [85.0], # Konsa
    49: [89.0], # Martinez
    50: [83.0], # McGinn
    51: [0.0], # Mings
    53: [1.0], # Olsen
    54: [0.0], # Philogene-Bidace
    55: [60.0], # Ramsey                 FIXXXX
    56: [0.0], # Sanson
    57: [0.0], # Sinisalo
    58: [45.0], # Tielemans
    59: [6.0], # Traore
    60: [89.0], # Watkins              
    61: [0.0], # Wesley
    584: [85.0],    # Pau Torres        
    599: [60.0],    # Diaby             
    618: [0.0],    # Kellyman
    670: [0.0],    # Marschall
    672: [25.0],    # Zaniolo
# Bournemouth
    705: [0.0], # Sinisterra
    62: [3.0], # Anthony
    63: [60.0], # Billing
    64: [22.0], # Brooks
    65: [64.0], # Christie
    66: [80.0], # Cook               
    67: [12.0], # Dembele
    68: [0.0], # Fredericks
    69: [0.0], # Hill
    70: [0.0], # Kelly              FIXXXX
    71: [0.0], # Kilkenny
    72: [60.0], # Kluivert
    73: [0.0], # Lowe
    74: [0.0], # Marcondes
    75: [10.0], # Mepham
    76: [5.0], # Moore
    77: [90.0], # Neto               INJJ
    78: [35.0], # Ouattara
    79: [0.0], # Pearson
    80: [0.0], # Randolph
    81: [7.0], # Rothwell
    82: [65.0], # Semenyo
    83: [78.0], # Senesi
    84: [12.0], # Smith
    85: [90.0], # Solanke           
    86: [80.0], # Tavernier
    87: [12.0], # H.Traore
    88: [0.0], # Travers
    89: [80.0], # Zabarnyi
    595: [70.0],    # Kerkez
    607: [0.0],    # Radu              
    619: [0.0],    # Ben Greenwood
    643: [0.0],    # Aarons             FIXXX
    644: [60.0],    # Scott              
    673: [0.0],    # Tyler Adams
# Brentford
    90: [6.0], # Ajer
    701: [65.0], # Ghoddos
    91: [0.0], # Balcombe
    92: [0.0], # Baptiste
    93: [0.0], # Bech
    94: [0.0], # Bidstrup
    95: [55.0], # Canos
    96: [80.0], # Collins    `       INJ`
    97: [0.0], # Cox
    98: [0.0], # Damsgaard
    99: [0.0], # Dasilva
    100: [0.0],  # Dervisoglu
    101: [89.0],    # Flekken        
    102: [0.0],    # Goode
    103: [0.0],    # Henry          FIXXXXX
    104: [0.0],    # Hickey         FIXXXXX SUSP YC
    105: [74.0],    # Janelt
    106: [75.0],    # Jensen
    107: [60.0],    # Lewis-Potter
    108: [0.0],    # Mbeumo         FIXXXXX
    258: [35.0],    # Maupay
    109: [0.0],    # Mee           FIXXXXX
    110: [67.0],    # Norgaard
    111: [12.0],    # Onyeka
    112: [88.0],    # Pinnock
    114: [60.0],    # Roerslev
    115: [0.0],    # Schade
    116: [1.0],    # Strakosha         
    117: [80.0],    # Toney
    118: [0.0],    # Trevitt
    119: [70.0],    # Wissa
    120: [0.0],    # Yarmolyuk
    121: [67.0],    #Zanka              FIXXXX
    620: [0.0],    # Olakigbe
# Brighton
    122: [65.0],    # Adingra
    123: [0.0],    # Alzate
    700: [50.0],     # Fati
    124: [0.0],    # Ayari
    125: [20.0],    # Buonanotte
    127: [3.0],    # Connolly
    128: [0.0],    # Dahoud
    129: [80.0],    # Dunk                   
    130: [0.0],    # Enciso
    131: [74.0],    # Estupinan
    132: [55.0],    # Ferguson
    133: [64.0],    # Gilmour
    134: [78.0],    # Gross                  
    135: [72.0],    # Joao Pedro
    136: [0.0],    # Karbownik
    137: [0.0],    # Kozlowski
    138: [30.0],    # Lallana                FIXXXX
    139: [0.0],    # Lamptey                FIXXXXXX
    140: [0.0],    # March                  FIXXXX INJURED
    141: [0.0],    # McGill
    142: [40.0],    # Milner                               
    143: [65.0],    # Mitoma                 
    144: [0.0],    # Moder
    146: [12.0],    # Sarmiento
    147: [0.0],    # Scherpen
    148: [50.0],    # Steele
    149: [0.0],    # Undav
    150: [60.0],    # Van Hecke
    151: [60.0],    # Veltman
    152: [50.0],    # Verbruggen
    153: [52.0],    # Webster
    154: [0.0],    # Wellbeck               FIXXXX INJ
    155: [0.0],    # Zeqiri
    606: [50.0],    # Igor
    621: [20.0],    # Hinshelwood
# Burnley
    156: [0.0],    # Agyei
    706: [12.0],     # M.Tressor
    674: [0.0],     # Delcroix
    179: [0.0],     # Thomas
    675: [42.0],     # Ramsey
    157: [80.0],    # Al-Dakhil
    158: [0.0],    # Bastien
    159: [0.0],    # Benson         FIXXXX
    160: [80.0],    # Beyer
    161: [75.0],    # Brownhill
    162: [0.0],    # Churlinov
    163: [15.0],    # Cork
    164: [0.0],    # Costelloe
    165: [0.0],    # Cullen         SUSP
    166: [0.0],    # Egan-Riley    
    167: [0.0],    # Ekdal
    168: [75.0],    # Foster                
    169: [0.0],    # Franchi    
    170: [60.0],    # Gudmundsson
    171: [0.0],    # McNally
    172: [1.0],    # Muric
    173: [85.0],    # O'Shea
    174: [11.0],    # Obafemi
    175: [0.0],    # Peacock-Farrell
    176: [59.0],    # Roberts
    177: [60.0],    # Rodriguez
    178: [63.0],    # Taylor
    179: [0.0],    # Thomas
    180: [0.0],    # Twine
    181: [0.0],    # Vigouroux
    182: [66.0],    # Vitinho
    183: [0.0],    # Weghorst
    184: [30.0],    # Zaroury
    185: [0.0],    # Ampadu
    186: [0.0],    # Andrey Santos
    594: [67.0],    # Amdouni
    600: [15.0],    # Redmond
    596: [89.0],    # Trafford
    605: [0.0],    # Koleosho
    608: [15.0],    # Bruun Larsen
    622: [0.0],    # Dodgson
    660: [50.0],    # Odobert
# Chelsea
    145: [0.0],    # Sanchez                 fixxxxxx
    126: [63.0],    # Caicedo
    187: [0.0],    # Arrizabalaga
    188: [0.0],    # Aubameyang
    189: [0.0],    # Azpilicueta
    190: [0.0],    # Baba Rahman
    191: [57.0],    # Badiashile
    192: [0.0],    # Bettinelli
    193: [50.0],    # Broja                 
    194: [0.0],    # Chalobah
    195: [0.0],    # Chilwell               FIXXX
    362: [82.0],    # Palmer
    196: [0.0],    # Chukwuemeka
    197: [75.0],    # Colwill
    198: [0.0],    # Cucurella
    199: [70.0],    # Enzo
    200: [0.0],    # D.D.Fofana
    201: [0.0],    # W.Fofana
    202: [0.0],    # Gallagher              SUSP
    203: [70.0],    # Gusto                  
    205: [0.0],    # Hudson-Odoi
    206: [0.0],    # James             
    207: [0.0],    # Lukaku
    208: [45.0],    # Madueke
    210: [60.0],    # Mudryk             
    211: [65.0],    # N.Jackson         
    212: [5.0],    # Nkunku
    213: [0.0],    # Pulisic
    214: [0.0],    # Sarr
    215: [0.0],    # Slonina
    216: [66.0],    # Sterling
    217: [80.0],    # Thiago Silva
    218: [0.0],    # Ziyech
    589: [0.0],    # Angelo
    609: [5.0],    # Maatsen
    611: [60.0],    # Disasi            
    613: [10.0],    # Ugochukwu
    623: [0.0],    # Burtsow
    659: [0.0],    # Bergstrom
    667: [0.0],    # Lavia
    671: [0.0],    # Humphreys
# Crystal Palace
    219: [0.0],    # Ahamada
    220: [88.0],    # Andersen
    221: [75.0],    # J.Ayew
    222: [78.0],    # Clyne
    223: [0.0],    # C.Doucoure            FIXXXXXX
    224: [0.0],    # Ebiowei
    225: [40.0],    # Edouard                fixxxx                   
    226: [85.0],    # Eze                   
    227: [0.0],    # Guaita
    228: [87.0],    # Guehi
    229: [45.0],    # Hughes
    230: [0.0],    # Johnstone
    385: [90.0],    # Henderson
    231: [65.0],    # Lerma                       
    232: [65.0],    # Mateta                    
    233: [0.0],    # Matthews
    234: [83.0],    # Mitchell
    235: [0.0],    # O'Brien
    236: [0.0],    # Olise
    237: [0.0],    # Plange
    238: [65.0],    # Richards
    239: [0.0],    # Riedewald
    240: [20.0],    # Schlupp                   
    241: [0.0],    # Tomkins                   
    242: [7.0],    # Ward
    243: [0.0],    # Whitworth
    615: [0.0],    # Matheus de Oliveira
    657: [30.0],    # Rak-Sakyi
    658: [0.0],    # Gordon
# Everton
    244: [10.0],    # Andre Gomes
    245: [84.0],    # Branthwaite
    246: [70.0],    # Calvert-Lewin
    247: [33.0],    # Coleman
    248: [0.0],    # Dele
    249: [85.0],    # A.Doucoure
    250: [75.0],    # Garner
    251: [0.0],    # Gbamin
    252: [12.0],    # Godfrey
    253: [0.0],    # Gray
    691: [20.0],     # Beto
    254: [74.0],    # Gueye
    255: [0.0],    # Holgate
    257: [30.0],    # Keane
    259: [75.0],    # McNeil
    260: [82.0],    # Mykolenko
    261: [0.0],    # Onana                  FIXXX
    262: [65.0],    # Patterson
    263: [89.0],    # Pickford
    264: [3.0],    # Simms
    265: [86.0],    # Tarkowski
    266: [0.0],    # Virginia
    579: [0.0],    # Lonergan
    588: [50.0],    # Young                  
    601: [45.0],    # Danjuma
    624: [5.0],    # Dobbin
    645: [0.0],    # Chermiti
    649: [0.0],    # Cannon
    650: [0.0],    # Onyango
    661: [76.0],    # Harrison
# Fulham
    267: [70.0],    # Andreas
    683: [0.0],     # Harris
    688: [82.0],    # Castagne
    256: [75.0],    # Iwobi
    268: [55.0],    # Cairney
    269: [0.0],    # Cavaleiro
    270: [45.0],    # De Cordova-Reid
    271: [0.0],    # Diop                   FIXXXX
    272: [0.0],     # Francois
    273: [0.0],     # Knockaert
    274: [0.0],     # Kongolo
    275: [89.0],    # Leno
    276: [1.0],     # Lukic
    277: [12.0],    # Mbabu
    278: [0.0],    # Mitrovic
    279: [0.0],     # Muniz             INJ
    280: [85.0],    # Palinha
    281: [20.0],    # Ream
    282: [34.0],    # Reed
    283: [84.0],    # Robinson
    284: [1.0],     # Rodak
    285: [0.0],    # Tete           FIXXXX
    286: [80.0],    # Tosin          
    287: [20.0],    # Vinicius
    288: [40.0],    # Wilson
    558: [80.0],    # Jimenez            
    591: [60.0],    # Willian
    610: [78.0],    # Bassey            FIXXXXX
    625: [0.0],    # De Fugerolles
    651: [0.0],    # Stansfield
    652: [0.0],    # Dibley-Dias
    662: [0.0],    # Adama Traore       FIXXXX
# Liverpool
    289: [0.0],     # Adrian
    290: [80.0],    # Alexander-Arnold      
    291: [90.0],    # Alisson
    292: [0.0],    # Bajcetic      
    708: [55.0],     # Gravenberch
    293: [67.0],    # Darwin                
    294: [65.0],    # Diogo Jota               
    295: [33.0],    # Eliott
    296: [0.0],     # Fabinho
    297: [55.0],    # Gakpo         
    298: [75.0],    # Gomez         
    299: [0.0],     # Henderson
    300: [30.0],    # Jones               SUSPP
    301: [0.0],    # Kelleher
    302: [78.0],    # Konate
    303: [70.0],    # Luis Diaz         FIXXXXX
    304: [60.0],    # Mac Allister
    305: [10.0],    # Matip
    306: [0.0],    # Phillips
    307: [0.0],    # Robertson          FIXXXXX
    308: [85.0],    # Salah
    309: [0.0],    # Szoboszlai  
    310: [0.0],    # Thiago
    311: [0.0],    # Tsimikas          
    312: [0.0],    # Van den Berg
    313: [85.0],    # Van Dijk
    626: [0.0],    # Quansah
    627: [0.0],    # Clark
    628: [0.0],    # Doak
    629: [0.0],    # McConnell
    668: [65.0],    # Wataru Endo
# Luton
    52: [0.0],     # Nakamba
    314: [73.0],    # Adebayo
    315: [0.0],    # Andersen           INJURED MONTHS
    316: [85.0],    # Bell              
    317: [0.0],    # Burry
    318: [0.0],    # Burke
    319: [0.0],    # Campbell
    320: [0.0],    # Clark          FIXXXX
    321: [78.0],    # Doughty
    322: [0.0],    # Freeman
    323: [0.0],    # Macey
    324: [0.0],    # McAtee
    325: [0.0],    # Mendes
    326: [50.0],    # Morris
    582: [7.0],    # Mpanzu
    586: [35.0],    # Chong
    602: [60.0],    # Kabore         FIXXXX
    327: [0.0],    # Muskwe
    328: [55.0],    # Ogbene
    329: [0.0],    # Onyedinma
    330: [70.0],    # Osho
    331: [0.0],    # Pepple
    332: [0.0],    # Pereira
    333: [15.0],    # Potts
    334: [0.0],    # Rea
    335: [89.0],    # Shea
    336: [0.0],    # Taylor
    337: [0.0],    # Thorpe
    338: [0.0],    # Walton
    339: [0.0],    # Watson
    340: [10.0],    # Woodrow            INJ
    553: [7.0],    # Giles
    575: [0.0],    # Lockyer
    393: [85.0],    # Mengi
    614: [90.0],    # Kaminski
    630: [83.0],    # Barkley
    631: [55.0],    # Brown
    648: [0.0],    # Francis-Clarke
    665: [0.0],    # Krul
# Man City
    341: [50.0],    # Akanji         
    342: [63.0],    # Ake
    343: [65.0],    # Alvarez
    344: [70.0],    # Bernardo
    345: [20.0],    # Bobb
    346: [0.0],    # Cancelo
    347: [0.0],    # Carson
    348: [0.0],    # Charles
    349: [70.0],    # De Bruyne
    350: [67.0],    # Dias
    351: [0.0],    # Doyle
    352: [89.0],    # Ederson
    353: [70.0],    # Foden
    354: [60.0],    # Grealish
    566: [15.0],    # Matheus Nunes
    355: [96.0],    # Haaland
    678: [60.0],     # Doku                  INJ
    356: [20.0],    # Kovacic
    357: [0.0],    # Laporte
    358: [14.0],    # Lewis
    359: [0.0],    # Mahrez
    361: [1.0],    # Ortega
    363: [0.0],    # Perrone
    364: [0.0],    # Phillips              
    365: [85.0],    # Rodri                  
    366: [3.0],    # Sergio Gomez
    367: [0.0],    # Steffen
    368: [0.0],    # Stones
    369: [77.0],    # Walker
    616: [68.0],    # Gvardiol
# Man United
    370: [0.0],    # Telles
    371: [0.0],    # Amad
    372: [64.0],    # Antony                
    373: [88.0],    # Fernandes
    209: [35.0],    # Mount
    374: [0.0],    # B.Williams
    375: [0.0],    # Bailly
    376: [0.0],    # Casemiro               INJURY
    377: [84.0],    # Dalot
    379: [63.0],    # Eriksen
    380: [0.0],    # Alvaro Fernandez
    381: [5.0],    # Fred
    382: [75.0],    # Garnacho
    383: [5.0],    # Hannibal Mejbri
    384: [0.0],    # Heaton
    386: [0.0],    # Lindelof
    387: [0.0],    # Maguire
    703: [70.0],     # Evans                 INJ
    388: [60.0],    # Mainoo
    389: [0.0],    # Malacia
    390: [15.0],    # Martial
    391: [0.0],    # Martinez
    392: [55.0],    # McTominay
    394: [24.0],    # Pellistri
    395: [70.0],    # Varane        
    396: [78.0],    # Rashford      
    709: [60.0],     # Amrabat      FIXXXX  
    397: [0.0],    # Sancho
    398: [0.0],    # Shaw
    508: [0.0],    # Reguillon           
    399: [0.0],    # Shoretire
    400: [0.0],    # Van de Beek
    401: [70.0],    # Wan-Bissaka
    597: [89.0],    # Onana
    617: [75.0],    # Hojlund
    632: [0.0],    # Forson
    669: [0.0],    # Vitek
# Newcastle
    402: [68.0],    # Almiron
    403: [0.0],    # Anderson
    404: [0.0],    # Ashby
    405: [85.0],    # Botman                                                  
    406: [85.0],    # Bruno Guimaraes    
    407: [75.0],    # Burn               
    204: [40.0],    # Hall
    408: [0.0],    # Darlow
    409: [89.0],    # Dubravka
    410: [5.0],    # Fraser
    411: [0.0],    # Gillespie
    412: [80.0],    # Gordon                         
    413: [0.0],    # Hayden
    414: [0.0],    # Hendrick
    415: [67.0],    # Isak              FIXXXXX
    416: [0.0],    # Joelinton
    417: [0.0],    # Krafth
    418: [0.0],    # Kuol
    419: [30.0],    # Lascelles         FIXXXX     
    420: [0.0],    # Lewis
    421: [60.0],    # S.Longstaff
    422: [0.0],    # Manquillo
    423: [0.0],    # Murphy             INJURED
    424: [0.0],    # Pope               INJURED
    425: [0.0],    # Ritchie
    426: [0.0],    # Saint-Maximin
    427: [85.0],    # Schar
    428: [0.0],    # Targett            INJURED
    429: [0.0],    # Tonali             SUSPENDED    
    430: [85.0],    # Trippier
    431: [0.0],    # Watts
    432: [20.0],    # Willock              
    433: [55.0],    # Wilson                           
    633: [15.0],    # Livramento
    634: [0.0],    # Alex Murphy
    635: [70.0],    # Miley
# Nottingham Forest
    378: [70.0],    # Elanga
    28: [85.0],     # Turner
    434: [0.0],    # B.Aguilera
    435: [0.0],    # Arter
    436: [27.0],    # Aurier
    437: [0.0],    # Awoniyi            INJURED    
    438: [0.0],    # Biancone
    439: [78.0],    # Boly
    440: [0.0],    # Bowler
    441: [0.0],    # Cook
    442: [2.0],    # Danilo
    443: [0.0],    # Dennis
    444: [0.0],    # Drager
    445: [0.0],    # Felipe
    446: [0.0],    # Freuler
    447: [84.0],    # Gibbs-White
    679: [75.0],     # Montiel
    710: [5.0],     # Vlachodimos
    713: [60.0],     # Sangare
    711: [0.0],     # Omobamidelle
    714: [15.0],     # Origi
    448: [0.0],    # Hennessey
    449: [0.0],    # Horvath
    451: [26.0],    # Kouyate
    452: [0.0],    # Laryea
    453: [8.0],    # Mangala
    454: [0.0],    # Mbe Soh
    455: [0.0],    # McKenna
    456: [0.0],    # Mighten
    457: [75.0],    # Niakhate
    458: [0.0],    # O'Brien
    459: [0.0],    # Ojeda
    460: [0.0],    # Panzo
    461: [0.0],    # Richards
    462: [0.0],    # Scarpa
    463: [0.0],    # Shelvey
    464: [0.0],    # Surridge
    465: [0.0],    # Toffolo
    466: [0.0],    # Ui-Jo
    467: [65.0],    # N.Williams
    468: [70.0],    # Wood                           
    469: [0.0],    # Worrall
    470: [78.0],    # Yates
    636: [0.0],    # Shelvey
    637: [0.0],    # Powell
# Sheffield United 
    471: [68.0],    # Ahmedhodzic           
    472: [0.0],    # Amissah
    473: [12.0],    # Baldock
    474: [0.0],    # Basham                 FIXXXXX
    475: [50.0],    # Berge
    476: [60.0],    # Bogle
    477: [0.0],    # Brewster
    478: [0.0],    # Coulibaly
    479: [1.0],    # Davies
    480: [0.0],    # Egan                   FIXXXXXX
    481: [67.0],    # Fleck
    482: [89.0],    # Foderingham
    27: [77.0],     # Trusty
    483: [0.0],    # Jebbison
    484: [62.0],    # Lowe
    485: [78.0],    # McBurnie          
    360: [60.0],    # McAtee
    486: [55.0],    # Ndiaye
    487: [0.0],    # Norrington-Davies
    488: [74.0],    # Norwood
    489: [55.0],    # Osborn
    490: [0.0],    # Osula
    33: [78.0],     # Archer
    491: [0.0],    # Austin
    587: [20.0],    # Slimane
    576: [75.0],    # Jack Robinson 
    638: [65.0],    # Vini de Souza Costa
    653: [0.0],    # Seriki
    654: [0.0],    # Marsh
    655: [0.0],    # Brooks
    656: [0.0],    # Hackford
    663: [50.0],    # Hamer
    666: [17.0],    # Davies
# Spurs
    492: [0.0],    # Bentancur
    493: [0.0],    # Bissouma
    494: [35.0],    # Bryan
    495: [70.0],    # Davies             INJ
    496: [80.0],    # Dier
    497: [65.0],    # Emerson Royal     
    498: [1.0],    # Forster
    499: [25.0],    # Hojberg
    500: [0.0],    # Kane
    501: [78.0],    # Kulusevski
    502: [0.0],    # LLoris
    503: [65.0],    # Lo Celso
    504: [0.0],    # Maddison           INJ
    583: [0.0],    # Solomon            FIXXXX
    450: [70.0],    # Johnson            
    505: [0.0],    # Ndombele
    506: [85.0],    # Pedro Porro
    507: [0.0],    # Perisic  
    509: [73.0],    # Richarlison            
    510: [0.0],    # Rodon
    511: [86.0],    # Romero             
    512: [0.0],    # Sanchez
    513: [77.0],    # Sarr
    514: [0.0],    # R.Sessegnon
    515: [30.0],    # Skipp
    516: [84.0],    # Son               
    517: [0.0],    # Spence
    518: [0.0],    # Tanganga
    519: [85.0],    # Udogie                 
    520: [89.0],    # Vicario
    521: [0.0],    # Whiteman
    639: [60.0],    # Van de Ven         
    640: [0.0],    # Scarlett
    641: [2.0],    # Veliz
# West Ham
    577: [1.0],    # Ogbonna
    522: [85.0],    # Aguerd
    523: [0.0],    # Antonio            INJURED       
    524: [89.0],    # Areola             FIXXX
    525: [20.0],    # Benrahma          
    526: [80.0],    # Bowen             
    689: [80.0],     # Kudus
    527: [10.0],    # Cornet
    528: [77.0],    # Coufal
    529: [0.0],    # Coventry
    530: [8.0],    # Cresswell      
    531: [0.0],    # Downes
    532: [78.0],    # Emerson        
    533: [1.0],    # Fabianski
    534: [7.0],    # Fornals
    535: [68.0],    # Ings
    536: [0.0],    # Johnson
    537: [5.0],    # Kehrer
    538: [1.0],    # Mubama
    539: [0.0],    # Paqueta            
    541: [0.0],    # Scamacca
    542: [77.0],    # Soucek            
    543: [0.0],    # Vlasic
    544: [86.0],    # Zouma             
    676: [65.0],     # Mavropanos       
    642: [80.0],    # Alvarez            
    647: [0.0],    # Anang
    664: [86.0],    # Ward prowse
# Wolves
    545: [70.0],    # Ait-Nouri
    704: [0.0],     # Fraser
    546: [0.0],    # Bentley
    547: [0.0],    # Bolla
    548: [35.0],    # Bueno
    549: [4.0],    # Chiquinho
    550: [0.0],    # Cundle
    551: [84.0],    # Dawson             
    552: [0.0],    # Fabio silva
    554: [0.0],    # Guedes
    555: [0.0],    # Hodge
    556: [0.0],    # Hoever
    557: [80.0],    # Hwang
    590: [78.0],    # Cunha
    559: [50.0],    # Joao Gomes
    560: [0.0],    # Jonny
    561: [0.0],    #  Jordao
    562: [10.0],    # Kalajdzic
    563: [85.0],    # Kilman
    564: [0.0],    # King
    565: [55.0],    # Lemina         
    567: [80.0],    # Neto              
    568: [0.0],    # Podence
    569: [89.0],    # Sa
    570: [65.0],    # Sarabia
    571: [1.0],    # Sarkic
    572: [75.0],    # Semedo         
    573: [75.0],    # Toti              
    598: [5.0],    # Doherty
    574: [5.0],    # B.Traore
    715: [40.0],     # Bellegarde
# extra
  
    580: [0.0],    # Karius
    581: [0.0],    # Dummet
    694: [0.0],     # Massengo

    677: [0.0],     # Deivid
    681: [0.0],     # D.Moreira
    697: [0.0],     # S.Bueno
    
    592: [0.0],    # Larouci
    593: [0.0],    # T.Benie

    690: [0.0],     # Baleba
    603: [0.0],    # Barnes
    604: [69.0]    # Aina
    
 }



def add_extra_players(master, players_raw):
    n = 41
    master_extra = pd.DataFrame({'code': [535818, 536694, 441302, 503714, 220362, 497894, 489639, 108796, 492831, 222683, 118342, 168090, 578614, 189776, 183751, 250735, 435973, 482609, 517052, 213198, 424876, 432422, 201440, 233821, 487053, 184254, 244954, 202641, 243557, 487702, 223434, 174310, 208904, 165183, 82738, 244262, 156700, 229164, 91046, 54738, 476369], 
                                'first_name': ['Simon', 'Matheus', 'Ian', 'Lesley', 'Axel', 'Rasmus', 'Bart', 'Tom', 'Zeki', 'Justin', 'Mark', 'Mahmoud', 'Enock', 'Samuel', 'Manuel Benson', 'Darko', 'Lyle', 'Malo', 'Nicolas', 'Christopher', 'Dominik', 'Sandro', 'Hwang', 'Anel', 'Destiny', 'Guglielmo', 'Pau', 'André', 'Moussa', 'Luca', 'Igor Julio', 'Elijah', 'Mads Juel', 'Amari\'i', 'Luke', 'Alfie', 'Carlton', 'Chiedozie', 'Cauley', 'Thomas', 'Issa'], 
                                'second_name': ['Adingra', 'França de Oliveira', 'Maatsen', 'Ugochukwu', 'Disasi', 'Højlund', 'Verbruggen', 'Lockyer', 'Amdouni', 'Kluivert', 'Flekken', 'Dahoud', 'Agyei', 'Bastien', 'Hedilazio', 'Churlinov', 'Foster', 'Gusto', 'Jackson', 'Nkunku', 'Szoboszlai', 'Tonali', 'Ui-jo', 'Ahmedhodžić', 'Udogie', 'Vicario', 'Torres', 'Onana', 'Diaby', 'Koleosho', 'dos Santos de Paulo', 'Adebayo', 'Andersen', 'Bell', 'Berry', 'Doughty', 'Morris', 'Ogbene', 'Woodrow', 'Kaminski', 'Kabore'], 
                                'web_name': ['Adingra', 'Matheus França', 'Maatsen', 'Ugochukwu', 'Disasi', 'Højlund', 'Verbruggen', 'Lockyer', 'Amdouni', 'Kluivert', 'Flekken', 'Dahoud', 'Agyei', 'Bastien', 'Benson', 'Churlinov', 'Foster', 'Gusto', 'N.Jackson', 'Nkunku', 'Szoboszlai', 'Tonali', 'Ui-jo', 'Ahmedhodžić', 'Udogie', 'Vicario', 'Pau', 'Onana', 'Diaby', 'Koleosho', 'Igor', 'Adebayo', 'Andersen', 'Bell', 'Berry', 'Doughty', 'Morris', 'Ogbene', 'Woodrow', 'Kaminski', 'Kabore'], 
                                '16-17': [np.NaN]*n, '17-18': [np.NaN]*n, '18-19': [np.NaN]*n, '19-20': [np.NaN]*n, '20-21': [np.NaN]*n, '21-22': [np.NaN]*n, '22-23': [np.NaN]*n,
                                'fbref': [np.NaN]*n,
                                'understat': [11710.0, 12152.0, 11807.0, 9451.0, 6885.0, 11055.0, 11711.0, 11714.0, 11701.0, 6963.0, 7047.0, 205.0, 5563.0, 1343.0, 7383.0, 7790.0, 7498.0, 9017.0, 10048.0, 3300.0, 9788.0, 7958.0, 7746.0, 10386.0, 8831.0, 8858.0, 6221.0, 10913.0, 6556.0, 10620.0, 7943.0, 11718.0, 11715.0, 11713.0, 11722.0, 11723.0, 11717.0, 11719.0, 11721.0, 11712.0, 9619.0],
                                'transfermarkt': [np.NaN]*n,
                                '23-24': [393.0, 122.0, 615.0, 609.0, 613.0, 611.0, 617.0, 152.0, 575.0, 594.0, 72.0, 101.0, 128.0, 156.0, 158.0, 159.0, 162.0, 168.0, 203.0, 211.0, 212.0, 309.0, 429.0, 466.0, 471.0, 519.0, 520.0, 584.0, 597.0, 599.0, 605.0, 606.0, 314.0, 315.0, 316.0, 317.0, 321.0, 326.0, 328.0, 340.0, 614.0, 602.0]})
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

# Add expected fixtures
def expand(team_fix_list, tid, season, gw):
    if season == '2023-24':
        # Man City vs Brentford
        if gw == 25:
            if tid == 13:
                team_fix_list.append(('Brentford', True, '2024-01-04T15:00:00Z', np.nan, np.nan, 1))
            if tid == 4:
                team_fix_list.append(('Man City', False, '2024-01-04T15:00:00Z', np.nan, np.nan, 1))

        # Bournemouth Luton
        if gw == 23:
            if tid == 3:
                team_fix_list.append(('Luton', True, '2024-01-04T15:00:00Z', np.nan, np.nan, 0.0))
            if tid == 12:
                team_fix_list.append(('Bournemouth', False, '2024-01-04T15:00:00Z', np.nan, np.nan, 0.0))
        if gw == 24:
            if tid == 3:
                team_fix_list.append(('Luton', True, '2024-01-04T15:00:00Z', np.nan, np.nan, 0.0))
            if tid == 12:
                team_fix_list.append(('Bournemouth', False, '2024-01-04T15:00:00Z', np.nan, np.nan, 0.0))
        if gw == 25:
            if tid == 3:
                team_fix_list.append(('Luton', True, '2024-01-04T15:00:00Z', np.nan, np.nan, 0.1))
            if tid == 12:
                team_fix_list.append(('Bournemouth', False, '2024-01-04T15:00:00Z', np.nan, np.nan, 0.1))
        if gw == 26:
            if tid == 3:
                team_fix_list.append(('Luton', True, '2024-01-04T15:00:00Z', np.nan, np.nan, 0.1))
            if tid == 12:
                team_fix_list.append(('Bournemouth', False, '2024-01-04T15:00:00Z', np.nan, np.nan, 0.1))


        # Liverpool Luton
        if gw == 24:
            if tid == 11:
                team_fix_list.append(('Luton', True, '2024-01-04T15:00:00Z', np.nan, np.nan, 0.0))
            if tid == 12:
                team_fix_list.append(('Liverpool', False, '2024-01-04T15:00:00Z', np.nan, np.nan, 0.0))
        if gw == 25:
            if tid == 11:
                team_fix_list.append(('Luton', True, '2024-01-04T15:00:00Z', np.nan, np.nan, 0.7))
            if tid == 12:
                team_fix_list.append(('Liverpool', False, '2024-01-04T15:00:00Z', np.nan, np.nan, 0.7))
        if gw == 26:
            if tid == 11:
                team_fix_list.append(('Luton', True, '2024-01-04T15:00:00Z', np.nan, np.nan, 0.11))
            if tid == 12:
                team_fix_list.append(('Liverpool', False, '2024-01-04T15:00:00Z', np.nan, np.nan, 0.11))
        
        # Tottenham Chelsea
        if gw == 26:
            if tid == 18:
                team_fix_list.append(('Chelsea', False, '2024-02-04T15:00:00Z', np.nan, np.nan, 0.3))
            if tid == 7:
                team_fix_list.append(('Spurs', True, '2024-02-04T15:00:00Z', np.nan, np.nan, 0.3))
        
        # Man Utd Fulham
        if gw == 26:
            if tid == 14:
                team_fix_list.append(('Fulham', True, '2024-02-04T15:00:00Z', np.nan, np.nan, 0.9))
            if tid == 10:
                team_fix_list.append(('Man Utd', False, '2024-02-04T15:00:00Z', np.nan, np.nan, 0.9))


        # BGW29
        if gw == 29:
            if tid == 6:
                team_fix_list.append(('Brentford', True, '2024-02-04T15:00:00Z', np.nan, np.nan, 0.88))
            if tid == 4:
                team_fix_list.append(('Burnley', False, '2024-02-04T15:00:00Z', np.nan, np.nan, 0.88))

            if tid == 12:
                team_fix_list.append(('Nott\'m Forest', True, '2024-02-04T15:00:00Z', np.nan, np.nan, 0.75))
            if tid == 16:
                team_fix_list.append(('Luton', False, '2024-02-04T15:00:00Z', np.nan, np.nan, 0.75))

            if tid == 1:
                team_fix_list.append(('Chelsea', True, '2024-02-04T15:00:00Z', np.nan, np.nan, 0.6))
            if tid == 7:
                team_fix_list.append(('Arsenal', False, '2024-02-04T15:00:00Z', np.nan, np.nan, 0.6))

            if tid == 20:
                team_fix_list.append(('Bournemouth', True, '2024-02-04T15:00:00Z', np.nan, np.nan, 0.5))
            if tid == 3:
                team_fix_list.append(('Wolves', False, '2024-02-04T15:00:00Z', np.nan, np.nan, 0.5))

            if tid == 14:
                team_fix_list.append(('Sheffield Utd', True, '2024-02-04T15:00:00Z', np.nan, np.nan, 0.38))
            if tid == 17:
                team_fix_list.append(('Man Utd', False, '2024-02-04T15:00:00Z', np.nan, np.nan, 0.38))

            if tid == 8:
                team_fix_list.append(('Newcastle', True, '2024-02-04T15:00:00Z', np.nan, np.nan, 0.53))
            if tid == 15:
                team_fix_list.append(('Crystal Palace', False, '2024-02-04T15:00:00Z', np.nan, np.nan, 0.53))

            if tid == 19:
                team_fix_list.append(('Aston Villa', True, '2024-02-04T15:00:00Z', np.nan, np.nan, 0.52))
            if tid == 2:
                team_fix_list.append(('West Ham', False, '2024-02-04T15:00:00Z', np.nan, np.nan, 0.52))

            if tid == 10:
                team_fix_list.append(('Spurs', True, '2024-02-04T15:00:00Z', np.nan, np.nan, 0.57))
            if tid == 18:
                team_fix_list.append(('Fulham', False, '2024-02-04T15:00:00Z', np.nan, np.nan, 0.57))

            if tid == 9:
                team_fix_list.append(('Liverpool', True, '2024-02-04T15:00:00Z', np.nan, np.nan, 0.21))
            if tid == 11:
                team_fix_list.append(('Everton', False, '2024-02-04T15:00:00Z', np.nan, np.nan, 0.21))

            if tid == 5:
                team_fix_list.append(('Man City', True, '2024-02-04T15:00:00Z', np.nan, np.nan, 0.31))
            if tid == 13:
                team_fix_list.append(('Brighton', False, '2024-02-04T15:00:00Z', np.nan, np.nan, 0.31))


    return team_fix_list

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
        tid = team_id(id, season, players_raw)
        short_teams.append(teams2023[teams2023['id']==tid]['short_name'].iloc[0])
        positions.append(df_aux['element_type'].iloc[0])
        prices.append(df_aux['now_cost'].iloc[0])
        for it, gw in enumerate(gws):
            try:
                expected_mins = expected_minutes[id][0]
            except:
                expected_mins = 0.0
            
            # suspensions
            # Haaland
            if id == 355:
                if gw == 22:
                    expected_mins = 30.0

            # De Bruyne
            if id == 349:
                if gw == 21:
                    expected_mins = 50.0
                if gw == 22:
                    expected_mins = 57.0
                if gw == 23:
                    expected_mins = 65.0

            # Alvarez
            if id == 343:
                if gw == 22:
                    expected_mins = 75.0
                if gw == 23:
                    expected_mins = 73.0
                if gw == 24:
                    expected_mins = 67.0

            # DARWIN
            if id == 293:
                if gw == 21:
                    expected_mins = 75.0
                if gw == 22:
                    expected_mins = 73.0
                if gw == 23:
                    expected_mins = 70.0

            # Bowen
            if id == 526:
                if gw == 21:
                    expected_mins = 0.0
                if gw == 22:
                    expected_mins = 55.0
                if gw == 23:
                    expected_mins = 65.0

            # TAA
            if id == 290:
                if gw == 21:
                    expected_mins = 0.0
                if gw == 22:
                    expected_mins = 45.0
                if gw == 23:
                    expected_mins = 60.0

            # Foden
            if id == 353:
                if gw == 22:
                    expected_mins = 75.0
                if gw == 23:
                    expected_mins = 72.0
                if gw == 24:
                    expected_mins = 68.0

            # Moreno
            if id == 32:
                if gw > 22:
                    expected_mins = 50.0


            # mins reductions
            if gw == 20 and (id == 129 or id == 501):
                expected_mins = 0.0


            if id == 516:
                if gw == 21:
                    expected_mins = 84 * 0.0
                if gw == 22:
                    expected_mins = 84 * 0.01
                if gw == 23:
                    expected_mins = 84 * 0.31
                if gw == 24:
                    expected_mins = 84 * 0.74

            if id == 308:
                if gw == 21:
                    expected_mins = 86 * 0.0
                if gw == 22:
                    expected_mins = 86 * 0.05
                if gw == 23:
                    expected_mins = 86 * 0.35
                if gw == 24:
                    expected_mins = 86 * 0.72


            afix = []
            admins = []
            alikelihood = []
            team_fix_list = fixture_info2(tid, season, gw, fixtures, teams)
            team_fix_list = expand(team_fix_list, tid, season, gw)
            for i in range(len(team_fix_list)):
                opp_team, was_home, kickoff_time, score1, score2, chance = team_fix_list[i]
                afix.append(home[was_home] + teams2023[teams2023['name']==opp_team]['short_name'].iloc[0])
                admins.append(expected_mins)
                alikelihood.append(chance)
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
            opp_team, home, kickoff_time, score1, score2, chance = fixture_info2(tid, season, next_gw-1, fixtures, teams)[i]
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
