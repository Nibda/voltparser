'''Parse site https://www.ria.com for new required positions'''

from bs4 import BeautifulSoup
import requests
import os.path
import json
import webbrowser
import time
import re


chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
data = [
    {
    'label': 'Фари',
    'url': r'https://www.ria.com/advertisement/search/?&search_text=%D1%84%D0%B0%D1%80%D0%B0&category_id=9&subcategory_id=81&options[0][151]=13&options[0][152]=33783&options[0][149]=18&search_result_sort_order=1',
    'save_results': 'headlights.json',
    },
    {
    'label': 'Усі запчастини',
    'url': r'https://www.ria.com/advertisement/search/?&category_id=9&subcategory_id=81&options[0][151]=13&options[0][152]=33783s',
    'save_results': 'voltAll.json',
    }
]


def parse(url, save_results, label):
    print('+' * 50, label, '+' * 50, '\n')
    response = requests.get(url).content
    # print(response.text)
    soup = BeautifulSoup(response, "lxml")
    tags = soup.find_all('div', class_='ticket-clean')
    ignor_phrase = r"в наличии, и под заказ 2-4 дня. Не требуем предоплаты на карточку."
    # trash = soup.find_all() 
    # p.descriptions-ticket mhide480
    # print(tags['id'])
    result_list = [result_list['id'] for result_list in tags]
    print('result_list: ', result_list, '\n', 'found:', len(result_list), 'positions')
    if not os.path.isfile(save_results):
        with open(save_results, 'w') as file:
            json.dump(result_list, file, indent=2, ensure_ascii=False)
    else:
        with open(save_results, 'r') as file:
            old_list = json.load(file)
            flag = False
            for el in result_list:
                print(el)
                ignor_text_sourse = soup.find('div', id=el).p.text
                # return "None" or matching text 
                match_with_ignor_text = re.search(ignor_phrase, ignor_text_sourse)
                # print(match_with_ignor_text)
                if el not in old_list and not match_with_ignor_text:
                    link = soup.find('div', id=el).a['href']
                    webbrowser.get(chrome_path).open(link)
                    flag = True
                    time.sleep(2)

        if not flag:
            print('*' * 10, 'No results', '*' * 10, '\n')
        else:
            print('*' * 10, '!!! found new position !!!', '*' * 10, '\n')
        with open(save_results, 'w') as file:
            json.dump(result_list, file, indent=2, ensure_ascii=False)


if __name__ == '__main__':

    for parts in data:
        parse(parts['url'], parts['save_results'], parts['label'])
    time.sleep(3)
