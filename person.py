from bs4 import BeautifulSoup
from urllib.request import urlopen


class Person:
    def __init__(self, name):
        self.link = 'https://en.wikipedia.org/' + name

        rows = self.find_infobox_rows(self.link)
        issue_list = []
        spouse_list = []

        for row in rows:
            label = row.find('th', {"class": 'infobox-label'})
            if label is not None:
                label_value = label.text
                if label_value.startswith('Issue'):
                    Person.append_all_links(issue_list, row)
                if label_value.startswith('Spouse'):
                    Person.append_all_links(spouse_list, row)
                if label_value.lower() == 'father':
                    infobox_data = Person.find_infobox_data_of_row(row)
                    a = infobox_data.find('a')
                    if a is not None and a['href'] is not None:
                        print('new father ' + a['href'])
                        self.father = a['href']
                if label_value.lower() == 'mother':
                    infobox_data = Person.find_infobox_data_of_row(row)
                    a = infobox_data.find('a')
                    if a is not None and a['href'] is not None:
                        print('new mother ' + a['href'])
                        self.mother = a['href']

        self.issue_list = issue_list
        self.spouse_list = spouse_list

    @staticmethod
    def find_infobox_rows(url):
        html = urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')

        container = soup.find_all('body')[0].find('div', {"class": 'mw-page-container'})
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

    @staticmethod
    def find_infobox_data_of_row(row):
        return row.find('td', {"class": 'infobox-data'})

    @staticmethod
    def find_plainlist_of_infobox_data(infobox_data):
        return infobox_data.find('div', {"class": 'plainlist'})

    @staticmethod
    def append_all_links(list_to_append_to, row):
        infobox_data = Person.find_infobox_data_of_row(row)

        if infobox_data is None:
            print('None infobox_data')
        else:
            for a in infobox_data.find_all('a'):
                if a is not None and a['href'] is not None:
                    print('new issue ' + a['href'])
                    list_to_append_to.append(a['href'])
