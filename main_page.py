import tkinter as tk
import urllib.request

from node import Node
from person import Person
from relationship import Relationship


class MainPage:

    def __init__(self):
        self.root = tk.Tk('')
        self.root.geometry("400x200")
        self.label_person1 = tk.Label(text='Person 1')
        self.label_person1.grid(column=0, row=0)
        self.entry_person1 = tk.Entry(self.root)
        self.entry_person1.grid(column=1, row=0)
        self.label_person2 = tk.Label(text='Person 2')
        self.label_person2.grid(column=0, row=1)
        self.entry_person2 = tk.Entry(self.root)
        self.entry_person2.grid(column=1, row=1)
        self.submit_button = tk.Button(self.root, text="submit", command=self.evaluate)
        self.submit_button.grid(column=0, row=2, columnspan=2)

        self.root.mainloop()

    def evaluate(self):
        response = urllib.request.urlopen('https://en.wikipedia.org/wiki/Henry_VIII_of_England')
        u = response.geturl()

        path = MainPage.find_path('/wiki/' + self.entry_person1.get(), '/wiki/' + self.entry_person2.get())

        for node in path:
            print(node.link)
            print(node.relationship)

    @staticmethod
    def find_path(link1, link2):
        visited = set()
        queue = [[Node(link1, Relationship.SELF)]]

        while queue:
            path = queue.pop(0)
            node = path[-1]

            if node.link == link2:
                return path

            visited.add(node.link)
            person = Person(node.link)

            if person.father is not None and person.father not in visited:
                new_path_father = list(path)
                new_path_father.append(Node(person.father, Relationship.FATHER))
                queue.append(new_path_father)
                visited.add(person.father)

            if person.mother is not None and person.mother not in visited:
                new_path_mother = list(path)
                new_path_mother.append(Node(person.mother, Relationship.MOTHER))
                queue.append(new_path_mother)
                visited.add(person.mother)

            if person.issue_list is not None:
                for issue in person.issue_list:
                    if issue not in visited:
                        new_path_issue = list(path)
                        new_path_issue.append(Node(issue, Relationship.CHILD))
                        queue.append(new_path_issue)
                        visited.add(issue)

            if person.spouse_list is not None:
                for spouse in person.spouse_list:
                    if spouse not in visited:
                        new_path_spouse = list(path)
                        new_path_spouse.append(Node(spouse, Relationship.SPOUSE))
                        queue.append(new_path_spouse)
                        visited.add(spouse)
