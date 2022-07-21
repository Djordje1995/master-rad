import requests
import csv
from bs4 import BeautifulSoup
import constant

base_url = "https://www.polovniautomobili.com"

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                  " Chrome/102.0.5005.63 Safari/537.36"
}

# ukupan broj automobila na stranici polovni automobili 59783
car_links = []


def get_car_list_page_url(page):
    return f'https://www.polovniautomobili.com/auto-oglasi/pretraga?page={page}' \
           '&sort=basic&city_distance=0&showOldNew=old&without_price=1'


car_data = []
csv_columns = []


def visit_car_page(url):
    try:
        single_car_data = {}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, features="html.parser")
        data_divs = soup.findAll('div', class_="divider")
        for row in data_divs:
            try:
                dt = row.findAll('div', class_="uk-width-1-2")
                single_car_data[dt[0].text] = dt[1].text
                if dt[0].text not in csv_columns:
                    csv_columns.append(dt[0].text)
            except:
                print("STA SE DESILO?? 1")
                pass
        price = soup.findAll('span', class_='priceClassified')[0].text
        single_car_data['Cena'] = price.split()[0]
        if 'Cena' not in csv_columns:
            csv_columns.append('Cena')
        print(single_car_data)
        car_data.append(single_car_data)
    except:
        print("STA SE DESILO?? 2")
        pass


def collect_cars_data():
    page = 1
    while len(car_links) < 58000:
        try:
            r = requests.get(get_car_list_page_url(page), headers=headers)
            page += 1
            if r.status_code == 404:
                print("STA SE DESILO?? 404")
                break
            soup = BeautifulSoup(r.content, features="html.parser")
            article_list = soup.findAll('article', class_='classified')
            for article in article_list:
                image_div = article.find_all('div', class_="image")
                link = image_div[0].find_all('a', href=True)[0]
                car_links.append(base_url + link['href'])
                visit_car_page(base_url + link['href'])
                print(str(len(car_links)) + ". " + base_url + link['href'])
        except:
            print("STA SE DESILO?? LINK")
            pass

    with open(constant.DATA_FOLDER + constant.CAR_LINKS + constant.CSV, mode='w', newline='\n', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=csv_columns)
        writer.writeheader()
        for row in car_data:
            writer.writerow(row)


collect_cars_data()
