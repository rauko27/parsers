import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
    r = requests.get(url)
    return r.text

#TODO сделать получение последней страницы
# def get_last_page(html):
#     soup = BeautifulSoup(html, 'lxml')
#     last_page = soup.find('ul', class_='ui-pagination__list')
#     print(last_page)
#     # a = last_page.find_all('a')[-2].text
#     # print(a)
#     # return int(last_page.find_all('a')[-2].text)


def parser(html):
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('table',
                      class_='standard-table standard-table--row-highlight margin-bottom-small margin-top-x-small')
    rows = table.find_all('tr')[2:]

    banks = []

    for row in rows:
        cols = row.find_all('td')
        try:
            banks.append({'rating': cols[0].text.strip().split()[0],
                          'rating_change': cols[0].text.strip().split()[1],
                          'name': cols[1].a.text.strip(),
                          'last_month': cols[2].text.strip(),
                          'month_before_last': cols[3].text.strip(),
                          'differences': cols[4].text.strip(),
                          'percent': cols[5].text.strip()})
        except:
            banks.append({'rating': cols[0].text.strip().split()[0],
                          'rating_change': '',
                          'name': cols[1].a.text.strip(),
                          'last_month': cols[2].text.strip(),
                          'month_before_last': cols[3].text.strip(),
                          'differences': cols[4].text.strip(),
                          'percent': cols[5].text.strip()})

    return banks


def add_to_csv(banks):
    with open('parser_banki.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(('Рейтинг', 'Изменение рейтинга', 'Банк', 'Прошлый месяц', 'Позапрошлый месяц', 'Разницы', 'Процент'))
        writer.writerows((bank['rating'], bank['rating_change'], bank['name'], bank['last_month'], bank['month_before_last'],
                         bank['differences'], bank['percent'])for bank in banks)


def main():
    url = 'https://www.banki.ru/banks/ratings/'
    total_page = 10
    banks = []
    for page in range(1, total_page+1):
        banks.extend(parser(get_html(url + '?PAGEN_1={}'.format(page))))
    add_to_csv(banks)

if __name__ == '__main__':
    main()
