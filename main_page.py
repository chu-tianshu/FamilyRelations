import tkinter as tk

from person import Person


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
        person1_name = self.entry_person1.get()
        person1 = Person('/wiki/' + person1_name)
        person2_name = self.entry_person2.get()
        person2 = Person('/wiki/' + person2_name)

