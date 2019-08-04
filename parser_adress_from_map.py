from selenium import webdriver
import time
import csv
from datetime import datetime


def parser(region, query):
    link = 'https://www.google.com/maps/place/{}'.format(region)
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome('chromedriver.exe', chrome_options=options)
    # browser = webdriver.Chrome()
    # browser.implicitly_wait(10)
    browser.get(link)
    print('Запускаем поиск...')
    time.sleep(2)
    search = browser.find_element_by_xpath('//*[@id="searchboxinput"]')
    search.clear()
    search.send_keys(query + ', ' + region)
    print('Применяем фильтр...')
    search_btn = browser.find_element_by_xpath('//*[@id="searchbox-searchbutton"]').click()
    time.sleep(2)

    result_search = []

    print('Ищем...')

    while True:
        try:
            for i in range(1, 39, 2):

                try:
                    step_result = browser.find_element_by_xpath(
                        '//*[@id="pane"]/div/div[1]/div/div/div[2]/div[{}]'.format(i)).click()
                    time.sleep(2)
                    name = browser.find_element_by_xpath(
                        '//*[@id="pane"]/div/div[1]/div/div/div[3]/div[1]/div[1]/h1').text.strip()
                except:
                    step_result = browser.find_element_by_xpath(
                        '//*[@id="pane"]/div/div[1]/div/div/div[3]/div[{}]'.format(i)).click()
                    time.sleep(2)
                    name = browser.find_element_by_xpath(
                        '//*[@id="pane"]/div/div[1]/div/div/div[3]/div[1]/div[1]/h1').text.strip()
                adress = browser.find_element_by_xpath(
                    '//*[@id="pane"]/div/div[1]/div/div/div[8]/div/div[1]/span[3]/span[3]').text.strip()
                try:
                    site = browser.find_element_by_xpath(
                        '//*[@id="pane"]/div/div[1]/div/div/div[10]/div/div[1]/span[3]/span[3]').text.strip()
                except:
                    site = ''
                try:
                    phone = browser.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[11]/div/div[1]').text.strip()
                except:
                    phone = ''
                result_search.append({'name': name,
                                      'adress': adress,
                                      'site': site,
                                      'phone': phone})
                back_btn = browser.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/button').click()
                print('Организаций найдено: {}'.format(len(result_search)))
                time.sleep(2)
            next_page_btn = browser.find_element_by_xpath(
                '//*[@id="n7lv7yjyC35__section-pagination-button-next"]').click()
            time.sleep(2)

        except Exception as err:
            print(err)
            break
    browser.close()
    return result_search


def add_to_csv(path, result_search):
    print('Записываем в таблицу...')
    with open('{}.csv'.format(path), 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(('Название', 'Адрес', 'Сайт', 'Телефон'))
        writer.writerows((result['name'], result['adress'], result['site'], result['phone'])
                         for result in result_search)


def main():
    start = datetime.now()
    region = str(input('Введите регион поиска: '))
    query = str(input('Введите запрос: '))
    path = query + '_' + region
    result = parser(region, query)
    add_to_csv(path, result)
    end = datetime.now()
    total = end - start
    print('Время поиска: ' + str(total))
    for_exit = input('Для выхода нажмите "Enter"')

if __name__ == '__main__':
    main()
