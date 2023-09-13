from urllib.error import HTTPError

from bs4 import BeautifulSoup
from urllib.request import urlopen


class Person:
    def __init__(self, name):
        # Title seems to be the reliable ID of a page because sometimes different urls point to the same page without
        # redirection. An example: https://en.wikipedia.org/wiki/Henry_VIII_of_England and
        # https://en.wikipedia.org/wiki/Henry_VIII

        self.link = 'https://en.wikipedia.org/' + name
        self.title = None
        self.issue_list = []
        self.spouse_list = []
        self.father = None
        self.mother = None

        self.populate_family_members()

    def populate_family_members(self):
        html = None

        try:
            html = urlopen(self.link)
        except HTTPError as e:
            print("Error occurred when trying to open page " + self.link + " Error code: " + str(e.code))
            return

        soup = BeautifulSoup(html, 'html.parser')

        self.title = Person.find_title(soup)
        rows = Person.find_infobox_rows(soup)

        if rows is None:
            return

        for row in rows:
            label = row.find('th', {"class": 'infobox-label'})
            if label is not None:
                label_value = label.text
                if label_value.startswith('Issue'):
                    Person.append_all_links(self.issue_list, row)
                if label_value.startswith('Spouse'):
                    Person.append_all_links(self.spouse_list, row)
                if label_value.lower() == 'father':
                    infobox_data = Person.find_infobox_data_of_row(row)
                    a = infobox_data.find('a')
                    if a is not None and a['href'] is not None:
                        self.father = a['href']
                if label_value.lower() == 'mother':
                    infobox_data = Person.find_infobox_data_of_row(row)
                    a = infobox_data.find('a')
                    if a is not None and a['href'] is not None:
                        self.mother = a['href']

    @staticmethod
    def find_title(soup):
        head = soup.find('head')
        title = head.find('title').text

        return title

    @staticmethod
    def find_infobox_rows(soup):
        container = soup.find_all('body')[0].find('div', {"class": 'mw-page-container'})
        inner_container = container.find('div', {"class": 'mw-page-container-inner'})
        content_container = inner_container.find('div', {"class": 'mw-content-container'})
        main_content = content_container.find('main', {"id": 'content'})
        body_content = main_content.find('div', {"id": 'bodyContent'})
        content_text = body_content.find('div', {"id": 'mw-content-text'})
        parser_output = content_text.find('div', {"class": 'mw-parser-output'})
        infobox_vcard = parser_output.find('table', {"class": 'infobox vcard'})

        if infobox_vcard is None:
            return

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
                    list_to_append_to.append(a['href'])
