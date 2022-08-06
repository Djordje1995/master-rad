import csv
import math

from sklearn.model_selection import train_test_split

import constant
import csv_handler
import pandas as pd


def get_file_list():
    return [constant.AUDI,
            constant.FORD,
            constant.BMW,
            constant.HYUNDI,
            constant.MERCEDES,
            constant.SKODA,
            constant.TOYOTA,
            constant.VW,
            constant.VAUXHALL]


models_to_exclude = [
    ' R8',
    ' RS7',
    ' S4',
    ' S5',
    ' S8',
    ' SQ5',
    ' SQ7',
    ' i3',
    ' i8',
    ' X7',
    ' Z3',
    ' M2',
    ' M3',
    ' M5',
    ' M6',
    ' Getz',
    ' Terracan',
    ' Veloster',
    ' Fusion',
    ' Ranger',
    ' Ampera',
    ' Cascada',
    ' Kadjar',
    ' Tigra',
    ' Caddy',
    ' Caddy Life',
    ' Eos',
    ' Fox',
    ' Camry',
    ' IQ',
    ' PROACE VERSO',
    ' Supra',
    ' Urban Cruiser',
    ' Verso-S',
    ' CLC Class',
    ' CLK',
    ' G Class',
    ' GLB Class',
    ' R Class',
    ' California',
    ' Caddy Maxi',
    ' RS3',
    ' RS4',
    ' RS5',
    ' RS6',
    ' S3',
    ' Vivaro',
    ' Agila'
]


def append_file(master, file):
    for row in file:
        master.append(row)
    return master


def init_data(learning_data, testing_data):
    learning_data.append(csv_handler.get_header())
    testing_data.append(csv_handler.get_header())


def transfer_file_data(learning_data, testing_data, file_data):
    header = False
    i = 0
    for row in file_data:
        if not header:
            header = True
            continue
        if i < 2:
            learning_data.append(row)
            i += 1
        else:
            testing_data.append(row)
            i = 0


def map_brand_to_model(data):
    model = ""
    brand_model_map = {}
    for item in data:
        if item[constant.BR_MODEL] != model:
            model = item[constant.BR_MODEL]
            brand_model_map[model] = item[constant.BRAND]
    return brand_model_map


def print_file(file):
    for item in file:
        print(item)


def remove_difficult_data(file):
    new_file = []
    for row in file:
        if row[constant.TRANSMISSION] != 'Other' and row[constant.FUEL_TYPE] != 'Other' \
                and 2002 <= int(row[constant.YEAR]) <= 2021 and row[constant.ENGINE_SIZE] != '0' \
                and 150000 > int(row[constant.MILEAGE]) > 1000 and row[constant.BR_MODEL] != ' A2' \
                and row[constant.BR_MODEL] != ' Transit Tourneo' and 2000 <= int(row[constant.PRICE]) <= 40000 \
                and float(row[constant.MPG].replace(',', '.')) > 20 \
                and row[constant.FUEL_TYPE] != 'Electric' \
                and float(row[constant.ENGINE_SIZE].replace(',', '.')) < 6 \
                and float(row[constant.MPG].replace(',', '.')) < 100 \
                and row[constant.BR_MODEL] not in models_to_exclude:
            row[constant.ENGINE_SIZE] = float(row[constant.ENGINE_SIZE].replace(',', '.'))
            row[constant.MPG] = float(row[constant.MPG].replace(',', '.'))
            new_file.append(row)
    for item in new_file:
        if item[constant.BR_MODEL] == ' Focus' and item[constant.PRICE] > 50000:
            new_file.remove(item)
            continue
        if item[constant.BR_MODEL] == ' Puma' and item[constant.PRICE] < 10000:
            new_file.remove(item)
            continue
        if item[constant.BR_MODEL] == ' Mokka' and item[constant.PRICE] > 50000:
            new_file.remove(item)
            continue
        if item[constant.BR_MODEL] == ' Corolla' and item[constant.PRICE] < 10000:
            new_file.remove(item)
            continue
        if item[constant.BR_MODEL] == ' A Class' and item[constant.PRICE] > 50000:
            new_file.remove(item)
            continue
        if item[constant.BR_MODEL] == ' CL Class' and item[constant.PRICE] > 50000:
            new_file.remove(item)
            continue
        if item[constant.BR_MODEL] == ' CLA Class' and item[constant.PRICE] > 50000:
            new_file.remove(item)
            continue
        if item[constant.BR_MODEL] == ' GLE Class' and item[constant.PRICE] < 10000:
            new_file.remove(item)
            continue

    return new_file


def recreate_file(file_name):
    """Needs to be reworked since I changed the way the csv_handler now works"""
    read_file = ''
    write_file = ''
    if file_name == constant.LEARNING:
        read_file = constant.LEARNING
        write_file = constant.LEARNING_DATA
    else:
        read_file = constant.TESTING
        write_file = constant.TESTING_DATA

    file = csv_handler.get_by_file_name(read_file)
    new_file = remove_difficult_data(file)
    csv_handler.write_csv(new_file, write_file, csv_handler.get_header())


############## serbian specific changes ###################


old_headers = ['Stanje:', 'Marka', 'Model', 'Godište', 'Kilometraža', 'Karoserija', 'Gorivo', 'Kubikaža',
               'Snaga motora', 'Fiksna cena', 'Zamena:', 'Broj oglasa:', 'Plivajući zamajac', 'Emisiona klasa motora',
               'Pogon', 'Menjač', 'Broj vrata', 'Broj sedišta', 'Strana volana', 'Klima', 'Boja',
               'Materijal enterijera', 'Boja enterijera', 'Registrovan do', 'Poreklo vozila', 'Oštećenje',
               'Zemlja uvoza', 'Vlasništvo', 'Broj šasije', 'Način prodaje', 'Kredit', 'Beskamatni kredit', 'Lizing',
               'Atestiran', 'U ponudi od:', 'Učešće (depozit)', 'Broj vrata', 'Gotovinska uplata', 'Visina rate',
               'Kapacitet baterije', 'Domet sa punom baterijom(km)', 'Cena']

new_headers = ['Marka', 'Model', 'Godište', 'Kilometraža', 'Karoserija', 'Gorivo', 'Kubikaža',
               'Snaga motora', 'Emisiona klasa motora', 'Pogon', 'Menjač', 'Cena']

fixed_headers = ['Model', 'Godište', 'Kilometraža', 'Karoserija', 'Gorivo', 'Kubikaža',
                 'Snaga motora', 'Emisiona klasa motora', 'Pogon', 'Menjač', 'Cena']

x_header = ['Model', 'Godište', 'Kilometraža', 'Karoserija', 'Gorivo', 'Kubikaža',
            'Snaga motora', 'Emisiona klasa motora', 'Pogon', 'Menjač']
y_header = ['Cena']


def reformat_new_data_file(in_file):
    df = pd.read_csv(constant.DATA_FOLDER + in_file + constant.CSV, low_memory=False)
    df.columns = (df.columns.str.strip()
                  .str.replace(':', ''))
    file = df.T.to_dict()
    new_file = []
    for row in file.values():
        if isinstance(row['Visina rate'], float):
            row['Visina rate'] = ""
        if isinstance(row['Gotovinska uplata'], float):
            row['Gotovinska uplata'] = ""
        if isinstance(row['Učešće (depozit)'], float):
            row['Učešće (depozit)'] = ""
        if isinstance(row['Lizing'], float):
            row['Lizing'] = ""
        if isinstance(row['Beskamatni kredit'], float):
            row['Beskamatni kredit'] = ""
        if isinstance(row['Kredit'], float):
            row['Kredit'] = ""
        if row['Visina rate'] == "" and row['Gotovinska uplata'] == "" and row['Učešće (depozit)'] == "" \
                and row['Lizing'] == "" and row['Beskamatni kredit'] == "" and row['Kredit'] == "":
            new_file.append(row)

    data = pd.DataFrame(new_file)
    grouped = data[new_headers].sort_values(by=['Marka'])
    file_to_write = grouped.T.to_dict()

    with open(constant.DATA_FOLDER + constant.SERBIAN_CAR_DATA + constant.CSV, mode='w', newline='\n', encoding='utf-8') \
            as out_file:
        writer = csv.DictWriter(out_file, fieldnames=new_headers)
        writer.writeheader()
        for row in list(file_to_write.values()):
            writer.writerow(row)


def count_brand(data):
    brands = {}
    for row in data:
        if row['Marka'] not in brands.keys():
            brands[row['Marka']] = 1
        else:
            brands[row['Marka']] += 1
    print(brands)


def count_model(data):
    models = {}
    for row in data:
        if (row['Marka'] + ' : ' + row['Model']) not in models.keys():
            models[row['Marka'] + ' : ' + row['Model']] = 1
        else:
            models[row['Marka'] + ' : ' + row['Model']] += 1
    print(models)


brands_to_exclude = ['AC',
                     'Alpina',
                     'Aro',
                     'Asia Motors',
                     'Austin',
                     'Bentley',
                     'Buick',
                     'Cadillac',
                     'Chery',
                     'Chevrolet',
                     'Chrysler',
                     'Cupra',
                     'DR',
                     'Dacia',
                     'Daewoo',
                     'Daihatsu',
                     'Dodge',
                     'Ferrari',
                     'GAZ',
                     'Great Wall',
                     'Honda',
                     'Hummer',
                     'Infiniti',
                     'Isuzu',
                     'Jaguar',
                     'Jeep',
                     'Kia',
                     'Lada',
                     'Lamborghini',
                     'Lancia',
                     'Land Rover',
                     'Lexus',
                     'Lincoln',
                     'Linzda',
                     'MG',
                     'MINI',
                     'Mahindra',
                     'Maserati',
                     'Mitsubishi',
                     'Moskvitch',
                     'NSU',
                     'Ostalo',
                     'Piaggio',
                     'Polski Fiat',
                     'Porsche',
                     'Rolls Royce',
                     'Rover',
                     'Saab',
                     'Smart',
                     'SsangYong',
                     'Subaru',
                     'Suzuki',
                     'Tata',
                     'Tavria',
                     'Tesla',
                     'Trabant',
                     'UAZ',
                     'Vauxhall',
                     'Wartburg',
                     'Zastava',
                     'ZhiDou']

models_to_exclude = ['Alfa Romeo : 156 Crosswagon',
                     'Alfa Romeo : 146',
                     'Alfa Romeo : 166',
                     'Alfa Romeo : Giulia',
                     'Alfa Romeo : Stelvio',
                     'Alfa Romeo : 145',
                     'Alfa Romeo : GTV',
                     'Alfa Romeo : Brera',
                     'Alfa Romeo : 75',
                     'Alfa Romeo : 33',
                     'Alfa Romeo : Spider',
                     'Alfa Romeo : 164',
                     'Alfa Romeo : 155',

                     'Audi : A4 Allroad',
                     'Audi : TTS',
                     'Audi : 100',
                     'Audi : RS4',
                     'Audi : RS3',
                     'Audi : SQ7',
                     'Audi : S5',
                     'Audi : Quattro',
                     'Audi : S8',
                     'Audi : S3',
                     'Audi : SQ8',
                     'Audi : SQ5',
                     'Audi : S4',
                     'Audi : A6 Allroad',
                     'Audi : 200',
                     'Audi : 90',
                     'Audi : RS e-tron GT',
                     'Audi : RS Q3',
                     'Audi : R8',
                     'Audi : S1',
                     'Audi : RS Q5',
                     'Audi : S6',
                     'Audi : S7',
                     'Audi : e-tron',
                     'Audi : RS Q8',

                     'BMW : 320 GT',
                     'BMW : 740',
                     'BMW : 218',
                     'BMW : M 135i',
                     'BMW : 535',
                     'BMW : 530 GT',
                     'BMW : 523',
                     'BMW : X2',
                     'BMW : X4 M',
                     'BMW : 330',
                     'BMW : 325',
                     'BMW : 225',
                     'BMW : 440',
                     'BMW : 430',
                     'BMW : 630 GT',
                     'BMW : 216',
                     'BMW : 640',
                     'BMW : 518',
                     'BMW : 328',
                     'BMW : 520 GT',
                     'BMW : 420',
                     'BMW : M5',
                     'BMW : Compact',
                     'BMW : 318 GT',
                     'BMW : 750',
                     'BMW : 123',
                     'BMW : M 340i',
                     'BMW : Serija M',
                     'BMW : 745',
                     'BMW : 418',
                     'BMW : 550',
                     'BMW : i8',
                     'BMW : Z4',
                     'BMW : 840',
                     'BMW : 335',
                     'BMW : 650',
                     'BMW : X7',
                     'BMW : 850',
                     'BMW : M4',
                     'BMW : 214',
                     'BMW : X5 M',
                     'BMW : 528',
                     'BMW : 550 GT',
                     'BMW : 220',
                     'BMW : 340i',
                     'BMW : 635',
                     'BMW : 114',
                     'BMW : i3',
                     'BMW : 630',
                     'BMW : Z3',
                     'BMW : 524',
                     'BMW : M3',
                     'BMW : 540',
                     'BMW : 645',
                     'BMW : Serija i',
                     'BMW : 735',
                     'BMW : M550',
                     'BMW : 125',
                     'BMW : 323',
                     'BMW : Ostalo',
                     'BMW : X3 M',
                     'BMW : 435',
                     'BMW : 330 GT',
                     'BMW : 760',
                     'BMW : M2',
                     'BMW : M 550i',
                     'BMW : 425',
                     'BMW : 728',
                     'BMW : 428',
                     'BMW : X6 M',
                     'BMW : 1602',
                     'BMW : M 235i',
                     'BMW : 725',
                     'BMW : 545',
                     'BMW : 535 GT',

                     'Citroen : GSA',
                     'Citroen : Dyane',
                     'Citroen : C6',
                     'Citroen : 2CV',
                     'Citroen : GS',
                     'Citroen : C5 Aircross',
                     'Citroen : Nemo',
                     'Citroen : Xantia',
                     'Citroen : C-ELYSEE',
                     'Citroen : DS7',
                     'Citroen : Jumpy',
                     'Citroen : C4 Aircross',
                     'Citroen : C-Zero',
                     'Citroen : C3 Aircross',
                     'Citroen : Evasion',
                     'Citroen : XM',
                     'Citroen : C-Crosser',
                     'Citroen : Ami',
                     'Citroen : ZX',
                     'Citroen : Visa',
                     'Citroen : CX',
                     'Citroen : C4 SpaceTourer',
                     'Citroen : C-Aircross',
                     'Citroen : AX',

                     'Fiat : Qubo',
                     'Fiat : 500X',
                     'Fiat : Ulysse',
                     'Fiat : Uno',
                     'Fiat : 126',
                     'Fiat : Fiorino',
                     'Fiat : Sedici',
                     'Fiat : Scudo',
                     'Fiat : 500C',
                     'Fiat : Freemont',
                     'Fiat : Linea',
                     'Fiat : 124 Spider',
                     'Fiat : Palio',
                     'Fiat : Tempra',
                     'Fiat : 1107',
                     'Fiat : Marengo',
                     'Fiat : Coupe',
                     'Fiat : Barchetta',
                     'Fiat : 125',
                     'Fiat : Spider Europa',
                     'Fiat : Ostalo',
                     'Fiat : Cinquecento',
                     'Fiat : Elba',
                     'Ford : Tourneo Connect',
                     'Ford : Ranger',
                     'Ford : Street Ka',
                     'Ford : Edge',
                     'Ford : Explorer',
                     'Ford : Grand C-Max',
                     'Ford : Granada',
                     'Ford : Scorpio',
                     'Ford : Ka+',
                     'Ford : EcoSport',
                     'Ford : B-Max',
                     'Ford : Maverick',
                     'Ford : Ostalo',
                     'Ford : Taunus',
                     'Ford : Mustang',
                     'Ford : F 250',
                     'Ford : Sierra',
                     'Ford : Festiva',
                     'Ford : Puma',
                     'Ford : F 150',
                     'Ford : Capri',
                     'Ford : Cortina',
                     'Ford : Probe',
                     'Ford : Tourneo Custom',

                     'Hyundai : Matrix',
                     'Hyundai : Atos',
                     'Hyundai : Coupe',
                     'Hyundai : ix20',
                     'Hyundai : Terracan',
                     'Hyundai : i40',
                     'Hyundai : Galloper',
                     'Hyundai : Kona',
                     'Hyundai : Genesis',
                     'Hyundai : Trajet',
                     'Hyundai : Lantra',
                     'Hyundai : Pony',
                     'Hyundai : Ostalo',
                     'Hyundai : Ioniq',
                     'Hyundai : H 100',
                     'Hyundai : ix55',
                     'Hyundai : Venue',

                     'Mazda : B 250',
                     'Mazda : 323',
                     'Mazda : CX-5',
                     'Mazda : Tribute',
                     'Mazda : CX-3',
                     'Mazda : Premacy',
                     'Mazda : RX-8',
                     'Mazda : Demio',
                     'Mazda : MX-5',
                     'Mazda : CX-7',
                     'Mazda : 626',
                     'Mazda : MPV',
                     'Mazda : BT-50',
                     'Mazda : MX-6',
                     'Mazda : Xedos',
                     'Mazda : RX-7',
                     'Mazda : 121',
                     'Mazda : 929',

                     'Mercedes Benz : S 400',
                     'Mercedes Benz : ML 350',
                     'Mercedes Benz : ML 250',
                     'Mercedes Benz : GLA 200',
                     'Mercedes Benz : GLK 200',
                     'Mercedes Benz : E 300',
                     'Mercedes Benz : Vaneo',
                     'Mercedes Benz : GLA 180',
                     'Mercedes Benz : A 200',
                     'Mercedes Benz : CLS 350',
                     'Mercedes Benz : B 170',
                     'Mercedes Benz : C 350',
                     'Mercedes Benz : CLK 240',
                     'Mercedes Benz : B 150',
                     'Mercedes Benz : GL 320',
                     'Mercedes Benz : CLS 500',
                     'Mercedes Benz : GLC 350',
                     'Mercedes Benz : G 250',
                     'Mercedes Benz : CLC 200',
                     'Mercedes Benz : CLA 180',
                     'Mercedes Benz : CLS 320',
                     'Mercedes Benz : CLA 200',
                     'Mercedes Benz : SLK 200',
                     'Mercedes Benz : CLK 270',
                     'Mercedes Benz : E 290',
                     'Mercedes Benz : Ostalo',
                     'Mercedes Benz : GLC 300',
                     'Mercedes Benz : CLK 220',
                     'Mercedes Benz : GLE 400',
                     'Mercedes Benz : C 250',
                     'Mercedes Benz : ML 63 AMG',
                     'Mercedes Benz : C 300',
                     'Mercedes Benz : E 124',
                     'Mercedes Benz : CLS 400',
                     'Mercedes Benz : CLA 220',
                     'Mercedes Benz : CLK 200',
                     'Mercedes Benz : SL 350',
                     'Mercedes Benz : SLK 250'
                     'Mercedes Benz : ML 420',
                     'Mercedes Benz : A 220',
                     'Mercedes Benz : CL 63 AMG',
                     'Mercedes Benz : E 320',
                     'Mercedes Benz : GLS 500',
                     'Mercedes Benz : ML 500',
                     'Mercedes Benz : S 63 AMG',
                     'Mercedes Benz : E 280',
                     'Mercedes Benz : GLE 350',
                     'Mercedes Benz : ML 280',
                     'Mercedes Benz : GLC 250',
                     'Mercedes Benz : E 43 AMG',
                     'Mercedes Benz : GL 500',
                     'Mercedes Benz : R 280',
                     'Mercedes Benz : S 500',
                     'Mercedes Benz : GLK 250',
                     'Mercedes Benz : C 63 AMG',
                     'Mercedes Benz : A 190',
                     'Mercedes Benz : GLA 220',
                     'Mercedes Benz : GL 420',
                     'Mercedes Benz : GLE 300',
                     'Mercedes Benz : E 240',
                     'Mercedes Benz : E 260',
                     'Mercedes Benz : S 250',
                     'Mercedes Benz : GLE 250',
                     'Mercedes Benz : E 63 AMG',
                     'Mercedes Benz : CL 500',
                     'Mercedes Benz : CLS 300',
                     'Mercedes Benz : B 160',
                     'Mercedes Benz : A 45 AMG',
                     'Mercedes Benz : CLC 180',
                     'Mercedes Benz : G 400',
                     'Mercedes Benz : CLK 320',
                     'Mercedes Benz : C 160',
                     'Mercedes Benz : CLK 230',
                     'Mercedes Benz : S 300',
                     'Mercedes Benz : E 230',
                     'Mercedes Benz : GLK 220',
                     'Mercedes Benz : S 420',
                     'Mercedes Benz : 180',
                     'Mercedes Benz : GLB 200',
                     'Mercedes Benz : ML 400',
                     'Mercedes Benz : CLA 180 Shooting Brake',
                     'Mercedes Benz : GLE 53 AMG',
                     'Mercedes Benz : GLC 43 AMG',
                     'Mercedes Benz : CE 200',
                     'Mercedes Benz : S 600',
                     'Mercedes Benz : GLK 320',
                     'Mercedes Benz : GLC 200',
                     'Mercedes Benz : Citan',
                     'Mercedes Benz : CLS 250',
                     'Mercedes Benz : GLS 350 D',
                     'Mercedes Benz : CLS 350 Shooting Brake'
                     'Mercedes Benz : GL 350',
                     'Mercedes Benz : C 270',
                     'Mercedes Benz : G 350',
                     'Mercedes Benz : R 350',
                     'Mercedes Benz : GLS 600',
                     'Mercedes Benz : E 53 AMG',
                     'Mercedes Benz : SL 280',
                     'Mercedes Benz : G 63 AMG',
                     'Mercedes Benz : V Klasa',
                     'Mercedes Benz : CLA 250',
                     'Mercedes Benz : A 210',
                     'Mercedes Benz : S 550',
                     'Mercedes Benz : R 320',
                     'Mercedes Benz : E 400',
                     'Mercedes Benz : CL 600',
                     'Mercedes Benz : G 300',
                     'Mercedes Benz : GLK 350',
                     'Mercedes Benz : G 55 AMG',
                     'Mercedes Benz : G 500',
                     'Mercedes Benz : SLK 230',
                     'Mercedes Benz : S 280',
                     'Mercedes Benz : S 430',
                     'Mercedes Benz : GLA 45 AMG',
                     'Mercedes Benz : ML 230',
                     'Mercedes Benz : A 250',
                     'Mercedes Benz : GLE 63 AMG',
                     'Mercedes Benz : GLS 400',
                     'Mercedes Benz : GLS 580',
                     'Mercedes Benz : GLS 63 AMG',
                     'Mercedes Benz : S 450',
                     'Mercedes Benz : CLA 200 Shooting Brake',
                     'Mercedes Benz : CLA 45 AMG',
                     'Mercedes Benz : C 320',
                     'Mercedes Benz : GT 63 AMG',
                     'Mercedes Benz : ML 300',
                     'Mercedes Benz : S 560 Maybach',
                     'Mercedes Benz : S 580',
                     'Mercedes Benz : G 320',
                     'Mercedes Benz : GLE 580',
                     'Mercedes Benz : GL 450',
                     'Mercedes Benz : E 450',
                     'Mercedes Benz : S 220',
                     'Mercedes Benz : X klasa',
                     'Mercedes Benz : C 32 AMG',
                     'Mercedes Benz : E 500',
                     'Mercedes Benz : G 270',
                     'Mercedes Benz : GT',
                     'Mercedes Benz : CLS 250 Shooting Brake',
                     'Mercedes Benz : GLE 43 AMG',
                     'Mercedes Benz : C 55 AMG',
                     'Mercedes Benz : CE 300',
                     'Mercedes Benz : C 43 AMG'
                     'Mercedes Benz : CLS 220',

                     'Nissan : Primastar',
                     'Nissan : Almera',
                     'Nissan : Patrol',
                     'Nissan : Murano',
                     'Nissan : Terrano',
                     'Nissan : Pathfinder',
                     'Nissan : Sunny',
                     'Nissan : Serena',
                     'Nissan : Leaf',
                     'Nissan : Pixo',
                     'Nissan : Almera Tino',
                     'Nissan : Pulsar',
                     'Nissan : Tiida',
                     'Nissan : 350Z',

                     'Opel : Ascona',
                     'Opel : Adam',
                     'Opel : Rekord',
                     'Opel : Crossland X ',
                     'Opel : Mokka X',
                     'Opel : Frontera',
                     'Opel : Mokka',
                     'Opel : Corsa F',
                     'Opel : Karl',
                     'Opel : Cascada',
                     'Opel : Signum',
                     'Opel : Omega',
                     'Opel : Calibra',
                     'Opel : GT',
                     'Opel : Grandland X',
                     'Opel : Ostalo',
                     'Opel : Commodore',
                     'Opel : Monterey',
                     'Opel : Corsa A',
                     'Opel : Senator',
                     'Opel : Manta',
                     'Opel : Ampera',
                     'Opel : Sintra',

                     'Peugeot : Bipper',
                     'Peugeot : iOn',
                     'Peugeot : RCZ',
                     'Peugeot : 108',
                     'Peugeot : 504',
                     'Peugeot : 4007',
                     'Peugeot : 605',
                     'Peugeot : Expert',
                     'Peugeot : 205',
                     'Peugeot : 405',
                     'Peugeot : 806',
                     'Peugeot : 305',
                     'Peugeot : 309',
                     'Peugeot : 104',
                     'Peugeot : 4008',
                     'Peugeot : 505',
                     'Peugeot : 301',
                     'Peugeot : Ranch',
                     'Peugeot : TePee',

                     'Renault : Grand Modus',
                     'Renault : Thalia',
                     'Renault : RX',
                     'Renault : Vel Satis',
                     'Renault : Fluence',
                     'Renault : R 4',
                     'Renault : R 18',
                     'Renault : R 9',
                     'Renault : R 19',
                     'Renault : Twizy',
                     'Renault : Grand Espace',
                     'Renault : R 5',
                     'Renault : Latitude',
                     'Renault : R 21',
                     'Renault : Express',
                     'Renault : Safrane',
                     'Renault : Zoe',
                     'Renault : Ostalo',
                     'Renault : R 10',
                     'Renault : R 11',
                     'Renault : R 25',

                     'Seat : Toledo',
                     'Seat : Ateca',
                     'Seat : Arona',
                     'Seat : Exeo',
                     'Seat : Arosa',
                     'Seat : Tarraco',
                     'Seat : Mii',
                     'Seat : Marbella',

                     'Toyota : Urban Cruiser',
                     'Toyota : Verso',
                     'Toyota : Hilux',
                     'Toyota : iQ',
                     'Toyota : Prius',
                     'Toyota : 4Runner',
                     'Toyota : Yaris Verso',
                     'Toyota : Celica',
                     'Toyota : Camry',
                     'Toyota : MR2',
                     'Toyota : Starlet',
                     'Toyota : C-HR',
                     'Toyota : Avensis Verso',
                     'Toyota : Verso-S',
                     'Toyota : Corona',
                     'Toyota : FJ',
                     'Toyota : Paseo',
                     'Toyota : Crown',
                     'Toyota : Highlander',
                     'Toyota : Previa',

                     'Volkswagen : Golf Sportsvan',
                     'Volkswagen : Passat B2',
                     'Volkswagen : Lupo',
                     'Volkswagen : up!',
                     'Volkswagen : Phaeton',
                     'Volkswagen : Arteon',
                     'Volkswagen : Amarok',
                     'Volkswagen : Passat B4',
                     'Volkswagen : Passat B7 Alltrack',
                     'Volkswagen : Cross Polo',
                     'Volkswagen : Vento',
                     'Volkswagen : Passat B8 Alltrack',
                     'Volkswagen : T-Roc',
                     'Volkswagen : Passat B1',
                     'Volkswagen : Ostalo',
                     'Volkswagen : 181',
                     'Volkswagen : Buggy',

                     'Volvo : S90',
                     'Volvo : XC40',
                     'Volvo : V70',
                     'Volvo : C70',
                     'Volvo : V60',
                     'Volvo : V90',
                     'Volvo : 340',
                     'Volvo : S70',
                     'Volvo : 740',
                     'Volvo : XC70',
                     'Volvo : 244',
                     'Volvo : 460',
                     'Volvo : 245',
                     'Volvo : Amazon',
                     'Volvo : 440',
                     'Volvo : 850',
                     'Volvo : 945',

                     'Škoda : Citigo',
                     'Škoda : Kamiq',
                     'Škoda : Praktik',
                     'Škoda : Favorit',
                     'Škoda : 120',
                     'Škoda : 100',
                     'Škoda : 105',
                     'Škoda : Ostalo',
                     'Škoda : Scala']


def filter_brand_data(data):
    new_data = []
    for row in data:
        if row['Marka'] not in brands_to_exclude:
            new_data.append(row)
    return new_data


def filter_model_data(data):
    new_data = []
    for row in data:
        row['Model'] = str(row['Marka'] + " : " + row['Model'])
        if row['Model'] not in models_to_exclude:
            new_data.append(row)
    return new_data


def write_csv(file_name, data, header):
    with open(constant.DATA_FOLDER + file_name + constant.CSV, mode='w', newline='\n', encoding='utf-8') \
            as out_file:
        writer = csv.DictWriter(out_file, fieldnames=header)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def filter_suspicious_data(data):
    filtered_data = []
    for row in data:
        if row['Cena'] != 'Po' and not isinstance(row['Kubikaža'], float) \
                and row['Menjač'] != 'Manuelni 4 brzine ' \
                and row['Gorivo'] != 'Metan CNG' and row['Gorivo'] != 'Hibridni pogon' \
                and int(row['Kilometraža'].split()[0].replace('.', '')) != 1111 \
                and int(row['Kilometraža'].split()[0].replace('.', '')) != 11111 \
                and int(row['Kilometraža'].split()[0].replace('.', '')) != 12345 \
                and int(row['Kilometraža'].split()[0].replace('.', '')) != 1234 \
                and int(row['Kilometraža'].split()[0].replace('.', '')) > 1000:
            # and 40000 >= int(row['Cena'].replace('.', '').replace(',', '')):

            if (int(row['Kilometraža'].split()[0].replace('.', '')) <= 10000 and int(row['Godište']) > 2010) \
                    or int(row['Kilometraža'].split()[0].replace('.', '')) > 10000:
                new_row = {'Marka': row['Marka'],
                           'Model': row['Model'],
                           'Godište': int(row['Godište']),
                           'Kilometraža': int(row['Kilometraža'].split()[0].replace('.', '')),
                           'Karoserija': row['Karoserija'],
                           'Gorivo': row['Gorivo'],
                           'Kubikaža': int(row['Kubikaža'].split()[0]),
                           'Snaga motora': int(row['Snaga motora'].split('/')[1].split()[0]),
                           'Emisiona klasa motora': row['Emisiona klasa motora'],
                           'Pogon': row['Pogon'],
                           'Menjač': row['Menjač'],
                           'Cena': int(row['Cena'].replace('.', '').replace(',', ''))}
                filtered_data.append(new_row)
    return filtered_data


def print_unique_column_data(column, data):
    unique_list = {}
    for row in data:
        if row[column] not in unique_list:
            unique_list[row[column]] = 1
        else:
            unique_list[row[column]] += 1
    print(unique_list)


def fix_data(data):
    fixed_data = []
    for row in data:
        row['Emisiona klasa motora'] = row['Emisiona klasa motora'].strip()
        row['Pogon'] = row['Pogon'].strip()
        row['Menjač'] = row['Menjač'].strip()
        if row['Menjač'] == 'Automatski / poluautomatski' \
                or row['Menjač'] == 'Poluautomatski' \
                or row['Menjač'] == 'Automatski':
            row['Menjač'] = 'Automatski'
        if row['Pogon'] == '4x4 reduktor':
            row['Pogon'] = '4x4'
        if row['Gorivo'] == 'Benzin + Gas (TNG)' \
                or row['Gorivo'] == 'Benzin + Metan (CNG)':
            row['Gorivo'] = 'Benzin'
        if row['Kilometraža'] > 1000000:
            row['Kilometraža'] = int(row['Kilometraža'] / 5)
        fixed_data.append(row)
    return fixed_data


def filter_again(data):
    new_data = []
    for row in data:
        new_row = {'Model': row['Model'], 'Godište': row['Godište'], 'Kilometraža': row['Kilometraža'],
                   'Karoserija': row['Karoserija'], 'Gorivo': row['Gorivo'], 'Kubikaža': row['Kubikaža'],
                   'Snaga motora': row['Snaga motora'], 'Emisiona klasa motora': row['Emisiona klasa motora'],
                   'Pogon': row['Pogon'], 'Menjač': row['Menjač'], 'Cena': row['Cena']}
        if row['Kilometraža'] != row['Kubikaža'] \
                and row['Kubikaža'] < 25000 \
                and 40000 >= row['Cena'] >= 400 \
                and row['Godište'] > 1995:
            new_data.append(new_row)
        else:
            print(new_row)
    return new_data


def select_distinct(data, column):
    distinct_data = []
    for row in data:
        if row[column] not in distinct_data:
            distinct_data.append(row[column])
    print(distinct_data)


def clean_data():
    df = pd.read_csv(constant.DATA_FOLDER + constant.SERBIAN_CAR_DATA + constant.CSV, low_memory=False)
    data = list(df.T.to_dict().values())
    # count_brand(data)
    filtered_brand = filter_brand_data(data)
    # count_model(filtered_brand)
    filtered_model = filter_model_data(filtered_brand)
    # count_brand(filtered_model)

    everything_filtered = filter_suspicious_data(filtered_model)
    sorted_data = sorted(everything_filtered, key=lambda e: (e['Model'], e['Cena'], e['Emisiona klasa motora'],
                                                             e['Godište'], e['Kilometraža'], e['Kubikaža'],
                                                             e['Snaga motora']))
    fixed_data = fix_data(sorted_data)
    last_filtered = filter_again(fixed_data)
    write_csv(constant.FULL_DATA_SERBIAN, last_filtered, fixed_headers)

    learning_data = []
    testing_data = []
    count = 0
    current_model = ""
    for row in last_filtered:
        if (row['Model']) != current_model:
            current_model = row['Model']
            learning_data.append(row)
            count = 1
        else:
            if count in [0, 1, 2]:
                learning_data.append(row)
                count += 1
            else:
                testing_data.append(row)
                count = 0

    write_csv(constant.LEARNING_DATA_SERBIAN, learning_data, fixed_headers)
    write_csv(constant.TESTING_DATA_SERBIAN, testing_data, fixed_headers)
