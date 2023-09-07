from bs4 import BeautifulSoup
from urllib.request import urlopen


class Person:
    def __init__(self, name):
        self.link = 'https://en.wikipedia.org/' + name

        rows = find_infobox_rows(self.link)
        issue_list = []
        spouse_list = []

        for row in rows:
            label = row.find('th', {"class": 'infobox-label'})
            if label is not None:
                label_value = label.text
                if label_value.startswith('Issue'):
                    infobox_data = find_infobox_data_of_row(row)
                    plainlist = find_plainlist_of_infobox_data(infobox_data)
                    uls = plainlist.find_all('ul')
                    for ul in uls:
                        lis = ul.find_all('li')
                        for li in lis:
                            for a in li.find_all('a'):
                                print('new issue ' + a['href'])
                                issue_list.append(a['href'])
                if label_value.startswith('Spouse'):
                    infobox_data = find_infobox_data_of_row(row)
                    plainlist = find_plainlist_of_infobox_data(infobox_data)
                    if plainlist is not None:
                        for a in plainlist.find_all('a'):
                            print('new spouse ' + a['href'])
                            spouse_list.append(a['href'])
                    else:
                        for a in infobox_data.find_all('a'):
                            print('new spouse ' + a['href'])
                            spouse_list.append(a['href'])
                if label_value.lower() == 'father':
                    infobox_data = find_infobox_data_of_row(row)
                    a = infobox_data.find('a')
                    print('new father ' + a['href'])
                    self.father = a['href']
                if label_value.lower() == 'mother':
                    infobox_data = find_infobox_data_of_row(row)
                    a = infobox_data.find('a')
                    print('new mother ' + a['href'])
                    self.father = a['href']

        self.issue_list = issue_list
        self.spouse_list = spouse_list


def find_infobox_rows(url):
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')

    bodies = soup.find_all('body')
    body = bodies[0]
    container = body.find('div', {"class": 'mw-page-container'})
    inner_container = container.find('div', {"class": 'mw-page-container-inner'})
    content_container = inner_container.find('div', {"class": 'mw-content-container'})
    main_content = content_container.find('main', {"id": 'content'})
    body_content = main_content.find('div', {"id": 'bodyContent'})
    content_text = body_content.find('div', {"id": 'mw-content-text'})
    parser_output = content_text.find('div', {"class": 'mw-parser-output'})
    infobox_vcard = parser_output.find('table', {"class": 'infobox vcard'})
    tbody = infobox_vcard.find('tbody')
    rows = tbody.find_all('tr')

    return rows


def find_infobox_data_of_row(row):
    return row.find('td', {"class": 'infobox-data'})


def find_plainlist_of_infobox_data(infobox_data):
    return infobox_data.find('div', {"class": 'plainlist'})
