import math

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from numpy import random
import time

from scipy.stats import binom

from .forms import RawCounterForm, ChooseCounterForm, CountCounterForm
# Create your views here.
from .models import Counter

POKEDEX_NUMBER_LOOKUP = {
    'Bulbasaur': '1',
    'Ivysaur': '2',
    'Venusaur': '3',
    'Charmander': '4',
    'Charmeleon': '5',
    'Charizard': '6',
    'Squirtle': '7',
    'Wartortle': '8',
    'Blastoise': '9',
    'Caterpie': '10',
    'Metapod': '11',
    'Butterfree': '12',
    'Weedle': '13',
    'Kakuna': '14',
    'Beedrill': '15',
    'Pidgey': '16',
    'Pidgeotto': '17',
    'Pidgeot': '18',
    'Rattata': '19',
    'Alolan Rattata': '19-a',
    'Raticate': '20',
    'Alolan Raticate': '20-a',
    'Spearow': '21',
    'Fearow': '22',
    'Ekans': '23',
    'Arbok': '24',
    'Pikachu': '25',
    'Raichu': '26',
    'Alolan Raichu': '26-a',
    'Sandshrew': '27',
    'Alolan Sandshrew': '27-a',
    'Sandslash': '28',
    'Alolan Sandslash': '28-a',
    'Nidoran♀': '29',
    'Nidorina': '30',
    'Nidoqueen': '31',
    'Nidoran♂': '32',
    'Nidorino': '33',
    'Nidoking': '34',
    'Clefairy': '35',
    'Clefable': '36',
    'Vulpix': '37',
    'Alolan Vulpix': '37-a',
    'Ninetales': '38',
    'Alolan Ninetales': '38-a',
    'Jigglypuff': '39',
    'Wigglytuff': '40',
    'Zubat': '41',
    'Golbat': '42',
    'Oddish': '43',
    'Gloom': '44',
    'Vileplume': '45',
    'Paras': '46',
    'Parasect': '47',
    'Venonat': '48',
    'Venomoth': '49',
    'Diglett': '50',
    'Alolan Diglett': '50-a',
    'Dugtrio': '51',
    'Alolan Dugtrio': '51-a',
    'Meowth': '52',
    'Alolan Meowth': '52-a',
    'Galarian Meowth': '52-g',
    'Persian': '53',
    'Alolan Persian': '53-a',
    'Psyduck': '54',
    'Golduck': '55',
    'Mankey': '56',
    'Primeape': '57',
    'Growlithe': '58',
    'Arcanine': '59',
    'Poliwag': '60',
    'Poliwhirl': '61',
    'Poliwrath': '62',
    'Abra': '63',
    'Kadabra': '64',
    'Alakazam': '65',
    'Machop': '66',
    'Machoke': '67',
    'Machamp': '68',
    'Bellsprout': '69',
    'Weepinbell': '70',
    'Victreebel': '71',
    'Tentacool': '72',
    'Tentacruel': '73',
    'Geodude': '74',
    'Alolan Geodude': '74-a',
    'Graveler': '75',
    'Alolan Graveler': '75-a',
    'Golem': '76',
    'Alolan Golem': '76-a',
    'Ponyta': '77',
    'Galarian Ponyta': '77-g',
    'Rapidash': '78',
    'Galarian Rapidash': '78-g',
    'Slowpoke': '79',
    'Galarian Slowpoke': '79-g',
    'Slowbro': '80',
    'Galarian Slowbro': '80-g',
    'Magnemite': '81',
    'Magneton': '82',
    'Farfetch’d': '83',
    'Galarian Farfetch’d': '83-g',
    'Doduo': '84',
    'Dodrio': '85',
    'Seel': '86',
    'Dewgong': '87',
    'Grimer': '88',
    'Alolan Grimer': '88-a',
    'Muk': '89',
    'Alolan Muk': '89-a',
    'Shellder': '90',
    'Cloyster': '91',
    'Gastly': '92',
    'Haunter': '93',
    'Gengar': '94',
    'Onix': '95',
    'Drowzee': '96',
    'Hypno': '97',
    'Krabby': '98',
    'Kingler': '99',
    'Voltorb': '100',
    'Electrode': '101',
    'Exeggcute': '102',
    'Exeggutor': '103',
    'Alolan Exeggutor': '103-a',
    'Cubone': '104',
    'Marowak': '105',
    'Alolan Marowak': '105-a',
    'Hitmonlee': '106',
    'Hitmonchan': '107',
    'Lickitung': '108',
    'Koffing': '109',
    'Weezing': '110',
    'Galarian Weezing': '110-g',
    'Rhyhorn': '111',
    'Rhydon': '112',
    'Chansey': '113',
    'Tangela': '114',
    'Kangaskhan': '115',
    'Horsea': '116',
    'Seadra': '117',
    'Goldeen': '118',
    'Seaking': '119',
    'Staryu': '120',
    'Starmie': '121',
    'Mr. Mime': '122',
    'Galarian Mr. Mime': '122-g',
    'Scyther': '123',
    'Jynx': '124',
    'Electabuzz': '125',
    'Magmar': '126',
    'Pinsir': '127',
    'Tauros': '128',
    'Magikarp': '129',
    'Gyarados': '130',
    'Lapras': '131',
    'Ditto': '132',
    'Eevee': '133',
    'Vaporeon': '134',
    'Jolteon': '135',
    'Flareon': '136',
    'Porygon': '137',
    'Omanyte': '138',
    'Omastar': '139',
    'Kabuto': '140',
    'Kabutops': '141',
    'Aerodactyl': '142',
    'Snorlax': '143',
    'Articuno': '144',
    'Galarian Articuno': '144-g',
    'Zapdos': '145',
    'Galarian Zapdos': '145-g',
    'Moltres': '146',
    'Galarian Moltres': '146-g',
    'Dratini': '147',
    'Dragonair': '148',
    'Dragonite': '149',
    'Mewtwo': '150',
    'Mew': '151',
    'Chikorita': '152',
    'Bayleef': '153',
    'Meganium': '154',
    'Cyndaquil': '155',
    'Quilava': '156',
    'Typhlosion': '157',
    'Totodile': '158',
    'Croconaw': '159',
    'Feraligatr': '160',
    'Sentret': '161',
    'Furret': '162',
    'Hoothoot': '163',
    'Noctowl': '164',
    'Ledyba': '165',
    'Ledian': '166',
    'Spinarak': '167',
    'Ariados': '168',
    'Crobat': '169',
    'Chinchou': '170',
    'Lanturn': '171',
    'Pichu': '172',
    'Cleffa': '173',
    'Igglybuff': '174',
    'Togepi': '175',
    'Togetic': '176',
    'Natu': '177',
    'Xatu': '178',
    'Mareep': '179',
    'Flaaffy': '180',
    'Ampharos': '181',
    'Bellossom': '182',
    'Marill': '183',
    'Azumarill': '184',
    'Sudowoodo': '185',
    'Politoed': '186',
    'Hoppip': '187',
    'Skiploom': '188',
    'Jumpluff': '189',
    'Aipom': '190',
    'Sunkern': '191',
    'Sunflora': '192',
    'Yanma': '193',
    'Wooper': '194',
    'Quagsire': '195',
    'Espeon': '196',
    'Umbreon': '197',
    'Murkrow': '198',
    'Slowking': '199',
    'Galarian Slowking': '199-g',
    'Misdreavus': '200',
    'Unown': '201',
    'Wobbuffet': '202',
    'Girafarig': '203',
    'Pineco': '204',
    'Forretress': '205',
    'Dunsparce': '206',
    'Gligar': '207',
    'Steelix': '208',
    'Snubbull': '209',
    'Granbull': '210',
    'Qwilfish': '211',
    'Scizor': '212',
    'Shuckle': '213',
    'Heracross': '214',
    'Sneasel': '215',
    'Teddiursa': '216',
    'Ursaring': '217',
    'Slugma': '218',
    'Magcargo': '219',
    'Swinub': '220',
    'Piloswine': '221',
    'Corsola': '222',
    'Galarian Corsola': '222-g',
    'Remoraid': '223',
    'Octillery': '224',
    'Delibird': '225',
    'Mantine': '226',
    'Skarmory': '227',
    'Houndour': '228',
    'Houndoom': '229',
    'Kingdra': '230',
    'Phanpy': '231',
    'Donphan': '232',
    'Porygon2': '233',
    'Stantler': '234',
    'Smeargle': '235',
    'Tyrogue': '236',
    'Hitmontop': '237',
    'Smoochum': '238',
    'Elekid': '239',
    'Magby': '240',
    'Miltank': '241',
    'Blissey': '242',
    'Raikou': '243',
    'Entei': '244',
    'Suicune': '245',
    'Larvitar': '246',
    'Pupitar': '247',
    'Tyranitar': '248',
    'Lugia': '249',
    'Ho-Oh': '250',
    'Celebi': '251',
    'Treecko': '252',
    'Grovyle': '253',
    'Sceptile': '254',
    'Torchic': '255',
    'Combusken': '256',
    'Blaziken': '257',
    'Mudkip': '258',
    'Marshtomp': '259',
    'Swampert': '260',
    'Poochyena': '261',
    'Mightyena': '262',
    'Zigzagoon': '263',
    'Galarian Zigzagoon': '263-g',
    'Linoone': '264',
    'Galarian Linoone': '264-g',
    'Wurmple': '265',
    'Silcoon': '266',
    'Beautifly': '267',
    'Cascoon': '268',
    'Dustox': '269',
    'Lotad': '270',
    'Lombre': '271',
    'Ludicolo': '272',
    'Seedot': '273',
    'Nuzleaf': '274',
    'Shiftry': '275',
    'Taillow': '276',
    'Swellow': '277',
    'Wingull': '278',
    'Pelipper': '279',
    'Ralts': '280',
    'Kirlia': '281',
    'Gardevoir': '282',
    'Surskit': '283',
    'Masquerain': '284',
    'Shroomish': '285',
    'Breloom': '286',
    'Slakoth': '287',
    'Vigoroth': '288',
    'Slaking': '289',
    'Nincada': '290',
    'Ninjask': '291',
    'Shedinja': '292',
    'Whismur': '293',
    'Loudred': '294',
    'Exploud': '295',
    'Makuhita': '296',
    'Hariyama': '297',
    'Azurill': '298',
    'Nosepass': '299',
    'Skitty': '300',
    'Delcatty': '301',
    'Sableye': '302',
    'Mawile': '303',
    'Aron': '304',
    'Lairon': '305',
    'Aggron': '306',
    'Meditite': '307',
    'Medicham': '308',
    'Electrike': '309',
    'Manectric': '310',
    'Plusle': '311',
    'Minun': '312',
    'Volbeat': '313',
    'Illumise': '314',
    'Roselia': '315',
    'Gulpin': '316',
    'Swalot': '317',
    'Carvanha': '318',
    'Sharpedo': '319',
    'Wailmer': '320',
    'Wailord': '321',
    'Numel': '322',
    'Camerupt': '323',
    'Torkoal': '324',
    'Spoink': '325',
    'Grumpig': '326',
    'Spinda': '327',
    'Trapinch': '328',
    'Vibrava': '329',
    'Flygon': '330',
    'Cacnea': '331',
    'Cacturne': '332',
    'Swablu': '333',
    'Altaria': '334',
    'Zangoose': '335',
    'Seviper': '336',
    'Lunatone': '337',
    'Solrock': '338',
    'Barboach': '339',
    'Whiscash': '340',
    'Corphish': '341',
    'Crawdaunt': '342',
    'Baltoy': '343',
    'Claydol': '344',
    'Lileep': '345',
    'Cradily': '346',
    'Anorith': '347',
    'Armaldo': '348',
    'Feebas': '349',
    'Milotic': '350',
    'Castform': '351',
    'Kecleon': '352',
    'Shuppet': '353',
    'Banette': '354',
    'Duskull': '355',
    'Dusclops': '356',
    'Tropius': '357',
    'Chimecho': '358',
    'Absol': '359',
    'Wynaut': '360',
    'Snorunt': '361',
    'Glalie': '362',
    'Spheal': '363',
    'Sealeo': '364',
    'Walrein': '365',
    'Clamperl': '366',
    'Huntail': '367',
    'Gorebyss': '368',
    'Relicanth': '369',
    'Luvdisc': '370',
    'Bagon': '371',
    'Shelgon': '372',
    'Salamence': '373',
    'Beldum': '374',
    'Metang': '375',
    'Metagross': '376',
    'Regirock': '377',
    'Regice': '378',
    'Registeel': '379',
    'Latias': '380',
    'Latios': '381',
    'Kyogre': '382',
    'Groudon': '383',
    'Rayquaza': '384',
    'Jirachi': '385',
    'Deoxys': '386',
    'Turtwig': '387',
    'Grotle': '388',
    'Torterra': '389',
    'Chimchar': '390',
    'Monferno': '391',
    'Infernape': '392',
    'Piplup': '393',
    'Prinplup': '394',
    'Empoleon': '395',
    'Starly': '396',
    'Staravia': '397',
    'Staraptor': '398',
    'Bidoof': '399',
    'Bibarel': '400',
    'Kricketot': '401',
    'Kricketune': '402',
    'Shinx': '403',
    'Luxio': '404',
    'Luxray': '405',
    'Budew': '406',
    'Roserade': '407',
    'Cranidos': '408',
    'Rampardos': '409',
    'Shieldon': '410',
    'Bastiodon': '411',
    'Burmy': '412',
    'Wormadam': '413',
    'Mothim': '414',
    'Combee': '415',
    'Vespiquen': '416',
    'Pachirisu': '417',
    'Buizel': '418',
    'Floatzel': '419',
    'Cherubi': '420',
    'Cherrim': '421',
    'Shellos': '422',
    'Gastrodon': '423',
    'Ambipom': '424',
    'Drifloon': '425',
    'Drifblim': '426',
    'Buneary': '427',
    'Lopunny': '428',
    'Mismagius': '429',
    'Honchkrow': '430',
    'Glameow': '431',
    'Purugly': '432',
    'Chingling': '433',
    'Stunky': '434',
    'Skuntank': '435',
    'Bronzor': '436',
    'Bronzong': '437',
    'Bonsly': '438',
    'Mime Jr.': '439',
    'Happiny': '440',
    'Chatot': '441',
    'Spiritomb': '442',
    'Gible': '443',
    'Gabite': '444',
    'Garchomp': '445',
    'Munchlax': '446',
    'Riolu': '447',
    'Lucario': '448',
    'Hippopotas': '449',
    'Hippowdon': '450',
    'Skorupi': '451',
    'Drapion': '452',
    'Croagunk': '453',
    'Toxicroak': '454',
    'Carnivine': '455',
    'Finneon': '456',
    'Lumineon': '457',
    'Mantyke': '458',
    'Snover': '459',
    'Abomasnow': '460',
    'Weavile': '461',
    'Magnezone': '462',
    'Lickilicky': '463',
    'Rhyperior': '464',
    'Tangrowth': '465',
    'Electivire': '466',
    'Magmortar': '467',
    'Togekiss': '468',
    'Yanmega': '469',
    'Leafeon': '470',
    'Glaceon': '471',
    'Gliscor': '472',
    'Mamoswine': '473',
    'Porygon-Z': '474',
    'Gallade': '475',
    'Probopass': '476',
    'Dusknoir': '477',
    'Froslass': '478',
    'Rotom': '479',
    'Uxie': '480',
    'Mesprit': '481',
    'Azelf': '482',
    'Dialga': '483',
    'Palkia': '484',
    'Heatran': '485',
    'Regigigas': '486',
    'Giratina': '487',
    'Cresselia': '488',
    'Phione': '489',
    'Manaphy': '490',
    'Darkrai': '491',
    'Shaymin': '492',
    'Arceus': '493',
    'Victini': '494',
    'Snivy': '495',
    'Servine': '496',
    'Serperior': '497',
    'Tepig': '498',
    'Pignite': '499',
    'Emboar': '500',
    'Oshawott': '501',
    'Dewott': '502',
    'Samurott': '503',
    'Patrat': '504',
    'Watchog': '505',
    'Lillipup': '506',
    'Herdier': '507',
    'Stoutland': '508',
    'Purrloin': '509',
    'Liepard': '510',
    'Pansage': '511',
    'Simisage': '512',
    'Pansear': '513',
    'Simisear': '514',
    'Panpour': '515',
    'Simipour': '516',
    'Munna': '517',
    'Musharna': '518',
    'Pidove': '519',
    'Tranquill': '520',
    'Unfezant': '521',
    'Blitzle': '522',
    'Zebstrika': '523',
    'Roggenrola': '524',
    'Boldore': '525',
    'Gigalith': '526',
    'Woobat': '527',
    'Swoobat': '528',
    'Drilbur': '529',
    'Excadrill': '530',
    'Audino': '531',
    'Timburr': '532',
    'Gurdurr': '533',
    'Conkeldurr': '534',
    'Tympole': '535',
    'Palpitoad': '536',
    'Seismitoad': '537',
    'Throh': '538',
    'Sawk': '539',
    'Sewaddle': '540',
    'Swadloon': '541',
    'Leavanny': '542',
    'Venipede': '543',
    'Whirlipede': '544',
    'Scolipede': '545',
    'Cottonee': '546',
    'Whimsicott': '547',
    'Petilil': '548',
    'Lilligant': '549',
    'Basculin': '550',
    'Sandile': '551',
    'Krokorok': '552',
    'Krookodile': '553',
    'Darumaka': '554',
    'Galarian Darumaka': '554-g',
    'Darmanitan': '555',
    'Galarian Darmanitan': '555-g',
    'Maractus': '556',
    'Dwebble': '557',
    'Crustle': '558',
    'Scraggy': '559',
    'Scrafty': '560',
    'Sigilyph': '561',
    'Yamask': '562',
    'Galarian Yamask': '562-g',
    'Cofagrigus': '563',
    'Tirtouga': '564',
    'Carracosta': '565',
    'Archen': '566',
    'Archeops': '567',
    'Trubbish': '568',
    'Garbodor': '569',
    'Zorua': '570',
    'Zoroark': '571',
    'Minccino': '572',
    'Cinccino': '573',
    'Gothita': '574',
    'Gothorita': '575',
    'Gothitelle': '576',
    'Solosis': '577',
    'Duosion': '578',
    'Reuniclus': '579',
    'Ducklett': '580',
    'Swanna': '581',
    'Vanillite': '582',
    'Vanillish': '583',
    'Vanilluxe': '584',
    'Deerling': '585',
    'Sawsbuck': '586',
    'Emolga': '587',
    'Karrablast': '588',
    'Escavalier': '589',
    'Foongus': '590',
    'Amoonguss': '591',
    'Frillish': '592',
    'Jellicent': '593',
    'Alomomola': '594',
    'Joltik': '595',
    'Galvantula': '596',
    'Ferroseed': '597',
    'Ferrothorn': '598',
    'Klink': '599',
    'Klang': '600',
    'Klinklang': '601',
    'Tynamo': '602',
    'Eelektrik': '603',
    'Eelektross': '604',
    'Elgyem': '605',
    'Beheeyem': '606',
    'Litwick': '607',
    'Lampent': '608',
    'Chandelure': '609',
    'Axew': '610',
    'Fraxure': '611',
    'Haxorus': '612',
    'Cubchoo': '613',
    'Beartic': '614',
    'Cryogonal': '615',
    'Shelmet': '616',
    'Accelgor': '617',
    'Stunfisk': '618',
    'Galarian Stunfisk': '618-g',
    'Mienfoo': '619',
    'Mienshao': '620',
    'Druddigon': '621',
    'Golett': '622',
    'Golurk': '623',
    'Pawniard': '624',
    'Bisharp': '625',
    'Bouffalant': '626',
    'Rufflet': '627',
    'Braviary': '628',
    'Vullaby': '629',
    'Mandibuzz': '630',
    'Heatmor': '631',
    'Durant': '632',
    'Deino': '633',
    'Zweilous': '634',
    'Hydreigon': '635',
    'Larvesta': '636',
    'Volcarona': '637',
    'Cobalion': '638',
    'Terrakion': '639',
    'Virizion': '640',
    'Tornadus': '641',
    'Thundurus': '642',
    'Reshiram': '643',
    'Zekrom': '644',
    'Landorus': '645',
    'Kyurem': '646',
    'Keldeo': '647',
    'Meloetta': '648',
    'Genesect': '649',
    'Chespin': '650',
    'Quilladin': '651',
    'Chesnaught': '652',
    'Fennekin': '653',
    'Braixen': '654',
    'Delphox': '655',
    'Froakie': '656',
    'Frogadier': '657',
    'Greninja': '658',
    'Bunnelby': '659',
    'Diggersby': '660',
    'Fletchling': '661',
    'Fletchinder': '662',
    'Talonflame': '663',
    'Scatterbug': '664',
    'Spewpa': '665',
    'Vivillon': '666',
    'Litleo': '667',
    'Pyroar': '668',
    'Flabébé': '669',
    'Floette': '670',
    'Florges': '671',
    'Skiddo': '672',
    'Gogoat': '673',
    'Pancham': '674',
    'Pangoro': '675',
    'Furfrou': '676',
    'Espurr': '677',
    'Meowstic': '678',
    'Honedge': '679',
    'Doublade': '680',
    'Aegislash': '681',
    'Spritzee': '682',
    'Aromatisse': '683',
    'Swirlix': '684',
    'Slurpuff': '685',
    'Inkay': '686',
    'Malamar': '687',
    'Binacle': '688',
    'Barbaracle': '689',
    'Skrelp': '690',
    'Dragalge': '691',
    'Clauncher': '692',
    'Clawitzer': '693',
    'Helioptile': '694',
    'Heliolisk': '695',
    'Tyrunt': '696',
    'Tyrantrum': '697',
    'Amaura': '698',
    'Aurorus': '699',
    'Sylveon': '700',
    'Hawlucha': '701',
    'Dedenne': '702',
    'Carbink': '703',
    'Goomy': '704',
    'Sliggoo': '705',
    'Goodra': '706',
    'Klefki': '707',
    'Phantump': '708',
    'Trevenant': '709',
    'Pumpkaboo': '710',
    'Gourgeist': '711',
    'Bergmite': '712',
    'Avalugg': '713',
    'Noibat': '714',
    'Noivern': '715',
    'Xerneas': '716',
    'Yveltal': '717',
    'Zygarde': '718',
    'Diancie': '719',
    'Hoopa': '720',
    'Volcanion': '721',
    'Rowlet': '722',
    'Dartrix': '723',
    'Decidueye': '724',
    'Litten': '725',
    'Torracat': '726',
    'Incineroar': '727',
    'Popplio': '728',
    'Brionne': '729',
    'Primarina': '730',
    'Pikipek': '731',
    'Trumbeak': '732',
    'Toucannon': '733',
    'Yungoos': '734',
    'Gumshoos': '735',
    'Grubbin': '736',
    'Charjabug': '737',
    'Vikavolt': '738',
    'Crabrawler': '739',
    'Crabominable': '740',
    'Oricorio': '741',
    'Cutiefly': '742',
    'Ribombee': '743',
    'Rockruff': '744',
    'Lycanroc': '745',
    'Wishiwashi': '746',
    'Mareanie': '747',
    'Toxapex': '748',
    'Mudbray': '749',
    'Mudsdale': '750',
    'Dewpider': '751',
    'Araquanid': '752',
    'Fomantis': '753',
    'Lurantis': '754',
    'Morelull': '755',
    'Shiinotic': '756',
    'Salandit': '757',
    'Salazzle': '758',
    'Stufful': '759',
    'Bewear': '760',
    'Bounsweet': '761',
    'Steenee': '762',
    'Tsareena': '763',
    'Comfey': '764',
    'Oranguru': '765',
    'Passimian': '766',
    'Wimpod': '767',
    'Golisopod': '768',
    'Sandygast': '769',
    'Palossand': '770',
    'Pyukumuku': '771',
    'Type: Null': '772',
    'Silvally': '773',
    'Minior': '774',
    'Komala': '775',
    'Turtonator': '776',
    'Togedemaru': '777',
    'Mimikyu': '778',
    'Bruxish': '779',
    'Drampa': '780',
    'Dhelmise': '781',
    'Jangmo-o': '782',
    'Hakamo-o': '783',
    'Kommo-o': '784',
    'Tapu Koko': '785',
    'Tapu Lele': '786',
    'Tapu Bulu': '787',
    'Tapu Fini': '788',
    'Cosmog': '789',
    'Cosmoem': '790',
    'Solgaleo': '791',
    'Lunala': '792',
    'Nihilego': '793',
    'Buzzwole': '794',
    'Pheromosa': '795',
    'Xurkitree': '796',
    'Celesteela': '797',
    'Kartana': '798',
    'Guzzlord': '799',
    'Necrozma': '800',
    'Magearna': '801',
    'Marshadow': '802',
    'Poipole': '803',
    'Naganadel': '804',
    'Stakataka': '805',
    'Blacephalon': '806',
    'Zeraora': '807',
    'Meltan': '808',
    'Melmetal': '809',
    'Grookey': '810',
    'Thwackey': '811',
    'Rillaboom': '812',
    'Scorbunny': '813',
    'Raboot': '814',
    'Cinderace': '815',
    'Sobble': '816',
    'Drizzile': '817',
    'Inteleon': '818',
    'Skwovet': '819',
    'Greedent': '820',
    'Rookidee': '821',
    'Corvisquire': '822',
    'Corviknight': '823',
    'Blipbug': '824',
    'Dottler': '825',
    'Orbeetle': '826',
    'Nickit': '827',
    'Thievul': '828',
    'Gossifleur': '829',
    'Eldegoss': '830',
    'Wooloo': '831',
    'Dubwool': '832',
    'Chewtle': '833',
    'Drednaw': '834',
    'Yamper': '835',
    'Boltund': '836',
    'Rolycoly': '837',
    'Carkol': '838',
    'Coalossal': '839',
    'Applin': '840',
    'Flapple': '841',
    'Appletun': '842',
    'Silicobra': '843',
    'Sandaconda': '844',
    'Cramorant': '845',
    'Arrokuda': '846',
    'Barraskewda': '847',
    'Toxel': '848',
    'Toxtricity': '849',
    'Sizzlipede': '850',
    'Centiskorch': '851',
    'Clobbopus': '852',
    'Grapploct': '853',
    'Sinistea': '854',
    'Polteageist': '855',
    'Hatenna': '856',
    'Hattrem': '857',
    'Hatterene': '858',
    'Impidimp': '859',
    'Morgrem': '860',
    'Grimmsnarl': '861',
    'Obstagoon': '862',
    'Perrserker': '863',
    'Cursola': '864',
    'Sirfetch’d': '865',
    'Mr. Rime': '866',
    'Runerigus': '867',
    'Milcery': '868',
    'Alcremie': '869',
    'Falinks': '870',
    'Pincurchin': '871',
    'Snom': '872',
    'Frosmoth': '873',
    'Stonjourner': '874',
    'Eiscue': '875',
    'Indeedee': '876',
    'Morpeko': '877',
    'Cufant': '878',
    'Copperajah': '879',
    'Dracozolt': '880',
    'Arctozolt': '881',
    'Dracovish': '882',
    'Arctovish': '883',
    'Duraludon': '884',
    'Dreepy': '885',
    'Drakloak': '886',
    'Dragapult': '887',
    'Zacian': '888',
    'Zamazenta': '889',
    'Eternatus': '890',
    'Kubfu': '891',
    'Urshifu': '892',
    'Zarude': '893',
    'Regieleki': '894',
    'Regidrago': '895',
    'Glastrier': '896',
    'Spectrier': '897',
    'Calyrex': '898',
}
COUNTER_CHANCE_LOOKUP = {
    '0.0122070312': '1/8192',
    '0.0610351562': '1/1636',
    '0.0732439757': '1/1364',
    '0.500488281': '1/200',
    '0.0366210938': '1/2727',
    '0.09765625': '1/1022',
    '0.1953125': '1/512',
    '1': '1/100',
    '0.170898438': '1/585',
    '0.0244140625': '1/4096',
    '0.146484375': '1/683',
    '0.122070312': '1/819',
    '0.366210938': '1/273',
    '0.317382812': '1/315',
    '0.146484368': '1/683',
    '0.333333333': '1/300',
    '0.048828125': '1/2048'
}


def home_view(request, *args, **kwargs):
    return render(request, "home.html", {})


def counter_view(request, id, *args, **kwargs):
    if request.method == 'POST' and 'ui button minus' in request.POST:
        obj = get_object_or_404(Counter, id=id)
        if obj.count != 1:
            obj.count = obj.count - 1
            obj.chance = get_shiny_chance(obj.hunting_method, obj.pokemon_game, obj.count, obj.shiny_charm)
            obj.binomial_distribution = calculate_binomial_distribution(obj.count, obj.chance)
            obj.chance_string = COUNTER_CHANCE_LOOKUP[str(obj.chance)]
            obj.save()
            context = {
                'user': obj.user,
                'pokemon_id': obj.pokemon_id,
                'pokemon_name': obj.pokemon_name,
                'pokemon_game': obj.pokemon_game,
                'count': obj.count,
                'chance': obj.chance,
                'chance_string': obj.chance_string,
                'hunting_method': obj.hunting_method,
                'binomial_distribution': obj.binomial_distribution,
                'shiny_charm': obj.shiny_charm,
                'caught': obj.caught
            }
            return render(request, "counter/counter_main.html", context)
        else:
            obj.chance = get_shiny_chance(obj.hunting_method, obj.pokemon_game, obj.count, obj.shiny_charm)
            obj.binomial_distribution = calculate_binomial_distribution(obj.count, obj.chance)
            obj.chance_string = COUNTER_CHANCE_LOOKUP[str(obj.chance)]
            obj.save()
            context = {
                'user': obj.user,
                'pokemon_id': obj.pokemon_id,
                'pokemon_name': obj.pokemon_name,
                'pokemon_game': obj.pokemon_game,
                'count': obj.count,
                'chance': obj.chance,
                'chance_string': obj.chance_string,
                'hunting_method': obj.hunting_method,
                'binomial_distribution': obj.binomial_distribution,
                'shiny_charm': obj.shiny_charm,
                'caught': obj.caught
            }
            return render(request, "counter/counter_main.html", context)
    if request.method == 'POST' and 'ui button plus' in request.POST:
        obj = get_object_or_404(Counter, id=id)
        obj.count = obj.count + 1
        obj.chance = get_shiny_chance(obj.hunting_method, obj.pokemon_game, obj.count, obj.shiny_charm)
        obj.binomial_distribution = calculate_binomial_distribution(obj.count, obj.chance)
        obj.chance_string = COUNTER_CHANCE_LOOKUP[str(obj.chance)]
        obj.save()
        context = {
            'user': obj.user,
            'pokemon_id': obj.pokemon_id,
            'pokemon_name': obj.pokemon_name,
            'pokemon_game': obj.pokemon_game,
            'count': obj.count,
            'chance': obj.chance,
            'chance_string': obj.chance_string,
            'hunting_method': obj.hunting_method,
            'binomial_distribution': obj.binomial_distribution,
            'shiny_charm': obj.shiny_charm,
            'caught': obj.caught
        }
        return render(request, "counter/counter_main.html", context)
    if request.method == 'POST' and 'ui button save' in request.POST:
        obj = get_object_or_404(Counter, id=id)
        obj.chance = get_shiny_chance(obj.hunting_method, obj.pokemon_game, obj.count, obj.shiny_charm)
        obj.binomial_distribution = calculate_binomial_distribution(obj.count, obj.chance)
        obj.chance_string = COUNTER_CHANCE_LOOKUP[str(obj.chance)]
        obj.save()
        return redirect('home')
    if request.method == 'POST' and 'ui button caught' in request.POST:
        obj = get_object_or_404(Counter, id=id)
        obj.chance = get_shiny_chance(obj.hunting_method, obj.pokemon_game, obj.count, obj.shiny_charm)
        obj.binomial_distribution = calculate_binomial_distribution(obj.count, obj.chance)
        obj.chance_string = COUNTER_CHANCE_LOOKUP[str(obj.chance)]
        obj.caught = True
        obj.save()
        return redirect('counter_detail', id=obj.id)

    obj = get_object_or_404(Counter, id=id)
    obj.chance = get_shiny_chance(obj.hunting_method, obj.pokemon_game, obj.count, obj.shiny_charm)
    obj.binomial_distribution = calculate_binomial_distribution(obj.count, obj.chance)
    obj.chance_string = COUNTER_CHANCE_LOOKUP[str(obj.chance)]
    context = {
        'user': obj.user,
        'pokemon_id': obj.pokemon_id,
        'pokemon_name': obj.pokemon_name,
        'pokemon_game': obj.pokemon_game,
        'count': obj.count,
        'chance': obj.chance,
        'chance_string': obj.chance_string,
        'hunting_method': obj.hunting_method,
        'binomial_distribution': obj.binomial_distribution,
        'shiny_charm': obj.shiny_charm,
        'caught': obj.caught
    }
    return render(request, "counter/counter_main.html", context)


def counter_choose_view(request, *args, **kwargs):
    form = ChooseCounterForm()
    if request.method == "POST":
        form = ChooseCounterForm(request.POST)
        if form.is_valid():
            form.cleaned_data['pokemon_id'] = POKEDEX_NUMBER_LOOKUP[form.cleaned_data.get('pokemon_name')]
            form.cleaned_data['user'] = request.user.get_username()
            form.cleaned_data['count'] = 1
            form.cleaned_data.values()
            Counter.objects.create(**form.cleaned_data)
            current_counter = Counter.objects.get(**form.cleaned_data)
            return redirect('counter', id=current_counter.id)
        else:
            print(form.errors)
    context = {
        'form': form
    }
    return render(request, "counter/counter_choose.html", context)


def counter_create_view(request):
    form = RawCounterForm()
    if request.method == "POST":
        form = RawCounterForm(request.POST)
        if form.is_valid():
            form.cleaned_data['pokemon_id'] = int(POKEDEX_NUMBER_LOOKUP[form.cleaned_data.get('pokemon_name')])
            form.cleaned_data['user'] = request.user.get_username()
            form.cleaned_data.values()
            Counter.objects.create(**form.cleaned_data)
        else:
            print(form.errors)
    context = {
        'form': form
    }
    return render(request, "counter/counter_create.html", context)


def counter_update_view(request, id):
    obj = get_object_or_404(Counter, id=id)
    form = RawCounterForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, "counter/counter_create.html", context)


def counter_detail_view(request, id, *args, **kwargs):
    if request.method == 'POST' and 'ui button continue' in request.POST:
        return redirect("counter", id=id)
    if request.method == 'POST' and 'ui button list' in request.POST:
        return redirect("counter_list")
    if request.method == 'POST' and 'ui button delete' in request.POST:
        return redirect("counter_delete", id=id)
    obj = get_object_or_404(Counter, id=id)
    obj.chance = get_shiny_chance(obj.hunting_method, obj.pokemon_game, obj.count, obj.shiny_charm)
    obj.binomial_distribution = calculate_binomial_distribution(obj.count, obj.chance)
    context = {
        'user': obj.user,
        'pokemon_id': obj.pokemon_id,
        'pokemon_name': obj.pokemon_name,
        'pokemon_game': obj.pokemon_game,
        'count': obj.count,
        'chance': obj.chance,
        'chance_string': obj.chance_string,
        'hunting_method': obj.hunting_method,
        'binomial_distribution': obj.binomial_distribution,
        'shiny_charm': obj.shiny_charm,
        'caught': obj.caught
    }
    return render(request, "counter/counter_detail.html", context)


def counter_list_view(request):
    queryset = Counter.objects.all().filter(user=request.user)
    context = {
        "object_list": queryset
    }
    return render(request, "counter/counter_list.html", context)


def counter_delete_view(request, id):
    obj = get_object_or_404(Counter, id=id)
    if request.method == "POST" and 'ui button yes' in request.POST:
        obj.delete()
        return redirect("counter_list")
    if request.method == "POST" and 'ui button list' in request.POST:
        return redirect("counter_list")
    context = {
        "object": obj
    }
    return render(request, "counter/counter_delete.html", context)


def get_shiny_chance(hunting_method, pokemon_game, count, shiny_charm):
    if pokemon_game == 'Gold' or pokemon_game == 'Silver' or pokemon_game == 'Crystal' or pokemon_game == 'Ruby' or pokemon_game == 'Sapphire' or pokemon_game == 'Emerald' or pokemon_game == 'FireRed' or pokemon_game == 'LeafGreen':
        return 0.0122070312
    elif pokemon_game == 'Diamond' or pokemon_game == 'Pearl' or pokemon_game == 'Platinum' or pokemon_game == 'HeartGold' or pokemon_game == 'SoulSilver' or pokemon_game == 'Black' or pokemon_game == 'White':
        if hunting_method == 'Random Encounters' or hunting_method == 'Soft Resetting':
            return 0.0122070312
        elif hunting_method == 'Masuda Method' and pokemon_game == 'Diamond' or pokemon_game == 'Pearl' or pokemon_game == 'Platinum' or pokemon_game == 'HeartGold' or pokemon_game == 'SoulSilver':
            return 0.0610351562
        elif hunting_method == 'Masuda Method' and pokemon_game == 'Black' or pokemon_game == 'White':
            return 0.0732439757
        elif hunting_method == 'Pokéradar':
            if count < 40:
                return 0.0122070312
            else:
                return 0.500488281
        else:
            return 0.0732439757
    elif pokemon_game == 'Black 2' or pokemon_game == 'White 2':
        if shiny_charm:
            if hunting_method == 'Random Encounters' or hunting_method == 'Soft Resetting':
                return 0.0366210938
            elif hunting_method == 'Masuda Method':
                return 0.09765625
            else:
                return 0.0366210938
        else:
            if hunting_method == 'Random Encounters' or hunting_method == 'Soft Resetting':
                return 0.0732439757
            elif hunting_method == 'Masuda Method':
                return 0.0732421875
            else:
                return 0.0732439757
    elif pokemon_game == 'X' or pokemon_game == 'Y' or pokemon_game == 'Omega Ruby' or pokemon_game == 'Alpha Sapphire':
        if shiny_charm:
            if hunting_method == 'Random Encounters' or hunting_method == 'Soft Resetting':
                return 0.0732439757
            elif hunting_method == 'Masuda Method':
                return 0.1953125
            elif hunting_method == 'Pokéradar':
                if count < 40:
                    return 0.0732439757
                else:
                    return 1
            elif hunting_method == 'Friend Safari':
                return 0.170898438
            elif hunting_method == 'Chain Fishing':
                if count < 41:
                    return 0.0732439757
                else:
                    return 1
            else:
                return 0.0732439757
        else:
            if hunting_method == 'Random Encounters' or hunting_method == 'Soft Resetting':
                return 0.0244140625
            elif hunting_method == 'Masuda Method':
                return 0.146484375
            elif hunting_method == 'Pokéradar':
                if count < 40:
                    return 0.0244140625
                else:
                    return 1
            elif hunting_method == 'Friend Safari':
                return 0.122070312
            elif hunting_method == 'Chain Fishing':
                if count < 41:
                    return 0.0244140625
                else:
                    return 1
            else:
                return 0.0244140625
    elif pokemon_game == 'Sun' or pokemon_game == 'Moon' or pokemon_game == 'Ultra Sun' or pokemon_game == 'Ultra Moon':
        if shiny_charm:
            if hunting_method == 'Random Encounters' or hunting_method == 'Soft Resetting':
                return 0.0732439757
            elif hunting_method == 'Masuda Method':
                return 0.1953125
            elif hunting_method == 'S.O.S. Battles':
                if count >= 31:
                    return 0.366210938
                else:
                    return 0.0732439757
            else:
                return 0.0732439757
        else:
            if hunting_method == 'Random Encounters' or hunting_method == 'Soft Resetting':
                return 0.0244140625
            elif hunting_method == 'Masuda Method':
                return 0.146484375
            elif hunting_method == 'S.O.S. Battles':
                if count >= 31:
                    return 0.317382812
                else:
                    return 0.0244140625
            else:
                return 0.0244140625
    elif pokemon_game == 'Sword' or pokemon_game == 'Shield':
        if shiny_charm:
            if hunting_method == 'Random Encounters' or hunting_method == 'Soft Resetting':
                if count <= 50:
                    return 0.0732439757
                elif 50 < count <= 100:
                    return 0.09765625
                elif 100 < count <= 200:
                    return 0.122070312
                elif 200 < count <= 300:
                    return 0.146484375
                elif 300 < count <= 500:
                    return 0.170898438
                else:
                    return 0.1953125
            elif hunting_method == 'Masuda Method':
                return 0.1953125
            elif hunting_method == 'Dynamax':
                return 1
        else:
            if hunting_method == 'Random Encounters' or hunting_method == 'Soft Resetting':
                if count <= 50:
                    return 0.0244140625
                elif 50 < count <= 100:
                    return 0.048828125
                elif 100 < count <= 200:
                    return 0.0732439757
                elif 200 < count <= 300:
                    return 0.09765625
                elif 300 < count <= 500:
                    return 0.122070312
                else:
                    return 0.146484375
            elif hunting_method == 'Masuda Method':
                return 0.146484375
            elif hunting_method == 'Dynamax':
                return 0.333333333
    else:
        return 1


def calculate_binomial_distribution(count, chance):
    binomial_distribution_mass = 0
    if chance == 1:
        binomial_distribution_mass = 0 - binom.logcdf(1, int(count), chance / 2)
    else:
        binomial_distribution_mass = 0 - binom.logcdf(1, int(count), chance)
    return round(binomial_distribution_mass, 2)
