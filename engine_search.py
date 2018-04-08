import tkinter as tk
import re
from pprint import pformat
import bs4 as bs
import urllib.request as uq


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        # make a label
        self.label = tk.Label(self, text="Where's my _______? (Enter word below)", fg="gray")
        self.label.grid(columnspan=4)
        # make a user input
        self.entry = tk.Entry(self)
        self.entry.grid(row=1)
        # make a search button
        self.submitButton = tk.Button(self, text='Search',
            command=self.getURLs)
        self.submitButton.grid(row=1, column=1)
        # make a rate button
        self.resetButton = tk.Button(self, text='PG-rate', fg="red",
            command=self.rate)
        self.resetButton.grid(row=1, column=2)
        # make a quit button
        self.quitButton = tk.Button(self, text='Quit', fg="red",
            command=self.quit)
        self.quitButton.grid(row=1, column=3)
        # make a text widget
        self.text = tk.Text(self)
        self.text.grid(columnspan=4)
        # make another label
        self.canv_lable = tk.Label(self, text="")
        self.canv_lable.grid(columnspan=4)

    def rate(self):
        self.text.insert('1.0', "XXX")

    def getURLs(self):
        # add URLs to expand the places to search in
        self.site_list = ["https://en.wikipedia.org/wiki/Hickory",
                        "https://en.wikipedia.org/wiki/Eastern_bluebird",
                        "http://road.cc/content/tech-news/177135-breaking-suspected-hidden-engine-bike-2016-cyclocross-world-champs"]
        # create the tasty waters
        self.soup_bowl = self.make_soups(self.site_list)

    def make_soups(self, site_list):
        """creates BeautifulSoup objects from input URLs.

        :param site_list: a list of URLs
        :type site_list: list
        :return: a dictionary mapping the URLs to the bs objects
        :rtype: dict{str : BeautifulSoupObject, str : BeautifulSoupObject}
        """
        self.soup_bowl = {}
        for site in site_list:
            sauce = uq.urlopen(site).read()
            soup = bs.BeautifulSoup(sauce, "lxml")
            self.soup_bowl[site] = soup
        self.find_word_in_alphabet_soup(self.soup_bowl)

    def find_word_in_alphabet_soup(self, soup_bowl):
        """displays all BeautifulSoup text content that includes the search term"""
        word = self.entry.get()
        search_term = re.compile(r"(?i){}".format(word)) # adding case insensitivity
        annotated_results = []
        flag = False
        for site, soup in self.soup_bowl.items():
            results = soup.body.findAll(text = search_term)
            if results:
                flag = True
            annotated_results.append((site, results))
        # show the results pprinted in a text field (user can copy results)
        self.text.delete('1.0', tk.END)
        self.text.insert(tk.END, pformat(annotated_results))
        if flag:
            self.canv_lable["text"] = "Yay! ... and off you go."
            self.canv_lable["fg"] = "black"
        else:
            self.canv_lable["text"] = "Nothing here... Try again!"
            self.canv_lable["fg"] = "red"


root = tk.Tk()
app = Application(master=root)
app.master.title('Engine Search')
app.mainloop()
