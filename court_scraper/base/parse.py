import os
import csv
import json
from lxml import etree
from io import StringIO


class ElementException(Exception):
    """
    When using this class inside of court scraper's automation, the cache_directory from runner should be
    passed to all file_directories.
    """
    pass


class Parser:

    def __init__(self):
        self.lxml_parser = etree.HTMLParser()

    # opens html file
    def open_html(self, html_file):
        self.html_file = html_file
        self.html = open(self.html_file, "r")
        self.html = self.html.read()
        # lxml will not access text after <br> tags and xpaths to their location return nothing,
        # thus removal solves the problem with no known drawbacks
        self.html = self.html.replace('<br>', '')
        return etree.parse(StringIO(self.html), self.lxml_parser)

    def clean(self, dirty_str):
        """
        Base function for cleaning string return from xpath text.
        """
        self.dirty_str = dirty_str
        self.clean_str = self.dirty_str.lower().strip().replace('\n', ' ')
        return self.clean_str

    """
    lxml and Selenium do not return information from xpaths the same.

    The following functions modify base lxml to return information using the same logic as Selenium:
        - find_text_by_xpath will always return a string from the first element found with the provided xpath
            - or it will return a string of 'none'
        - find_elements_by_xpath will return a list of all elements found with with the provided xpath
            - or it will return a string of 'none'
        - get_length_by_xpath returns the length of the list of elements found
            - this is often used for counting rows in a party table
    """

    # base return of lxml, other functions build on it
    def _get_info(self, input_xpath):
        self.input_xpath = input_xpath
        return self.tree.xpath(self.input_xpath)

    # equivalent of Selenium's driver.find_element_by_xpath('xpath').text
    def find_text_by_xpath(self, input_xpath):
        self.input_xpath = input_xpath
        self.info = self._get_info(input_xpath)
        if isinstance(self.info, list):
            if len(self.info) == 0:
                # length is 0
                return 'none'
            # test ensures the return isn't junk
            elif self.info[0].text is not None and self.clean(self.info[0].text) != '':
                # position 1 is not none
                return self.clean(self.info[0].text)
            else:
                # none
                return 'none'
        elif self.info is None:
            # not a list, is none
            return 'none'
        else:
            # not a list, not none
            return self.info

    # equivalent of Selenium's driver.find_elements_by_xpath('xpath')
    def find_elements_by_xpath(self, location):
        self.info = self._get_info(location)
        return self.info
        if isinstance(self.info, list):
            if len(self.info) == 1:
                raise ElementException('Element only returned one element. Try find_text_by_xpath')
            else:
                return self.info
        else:
            raise ElementException('Element only returned one element. Try find_text_by_xpath.')

    # equivalent of Selenium's len(driver.find_elements_by_xpath('xpath'))
    def get_length_by_xpath(self, location):
        self.info = self.find_elements_by_xpath
        return len(self.info)

    # this function writes multiples 'none's to a given list until that list is the desired length
    def expand_list(self, list, length):
        self.list = list
        self.length = length
        while len(self.list) < self.length:
            try:
                self.list.append('none')
            except Exception:
                pass
        return self.list

    # this function returns a string 'yes' or 'no' if the length of a list is greater than the input
    def more_than(self, list, count):
        self.list = list
        self.count = count
        if len(self.list) > self.count:
            return 'yes'
        else:
            return 'no'

    # this function parses string text to return the text between two given strings
    def text_between(self, text, before, after):
        self.text = text
        self.before = before
        self.after = after
        try:
            self.parse = self.text.split(self.before)
            self.parse = self.parse[1].split(self.after)
            self.parse = self.clean(self.parse[0])
        except Exception:
            self.parse = 'none'
        return self.parse

    # this function returns a string 'yes' or 'no' if provided string appears in the provided text
    def does_string_appear(self, text, string):
        self.text = text
        self.string = string
        self.test = self.text.find(self.string)
        if self.test != -1:
            return 'yes'
        else:
            return 'no'

    """
    string_search provides an entry_point to the best xpath logic for new users
    it follows this logic
    {div/table item}/{div/html element text is in}/{text to search}/{xpath to follow to getto relative field}
    """
    def string_search(self, text, table='', route=None, text_location=None):
        self.text = text
        self.table = table
        self.route = route
        self.text_location = text_location
        if self.text_location is None and self.route is None:
            # ('no location and no route')
            return self.find_text_by_xpath(f'{self.table}//*[contains(text(), "{text}")]')
        elif self.text_location is None and self.route is not None:
            # ('no location')
            return self.find_text_by_xpath(f'{self.table}//*[contains(text(), "{text}")]/{self.route}')
        elif self.text_location is not None and self.route is None:
            # ('no route')
            return self.find_text_by_xpath(f'{self.table}//{self.text_location}[contains(text(), "{text}")]')
        elif self.text_location is not None and self.route is not None:
            # ('location and route')
            return self.find_text_by_xpath(
                f'{self.table}//{self.text_location}[contains(text(), "{text}")]/{self.route}'
            )

    """
    These functions parse keys and values to dictionaries destined for json files
    """
    # this function creates dicts of a lists of keys and values
    def lists_to_dict(self, keys, values):
        self.keys = self.keys
        self.values = self.values
        self.output_dictionary = dict(zip(self.keys, self.values))
        if self.output_dictionary == {}:
            return 'none'
        else:
            return self.output_dictionary

    # this function write dicts to json files
    def write_to_json(self, input_data, save_dir, file_name):
        self.input_data = input_data
        self.save_dir = save_dir
        self.file_name = file_name
        with open(f'{self.save_dir}/{self.file_name}.json', 'w') as self.outfile:
            json.dump(self.json_data, self.outfile)

    # this function creates a list of given files in a given file directory
    def get_files(self, input_file_dir, file_type):
        self.input_file_dir = input_file_dir
        self.file_type = file_type
        self.file_list = []
        for self.entry in os.scandir(self.file_dir):
            if (self.entry.path.endswith(self.file_type)):
                self.file_list.append(self.entry.path)
        return self.file_list

    # this function opens a json file
    def open_json(self, file):
        self.file = file
        with open(self.file) as self.temp_load:
            self.json_data = json.load(self.temp_load)
        return self.json_data

    # this function creates a new database and failure log but wont overwrite existing one
    def create_csv(self, database_name, file_path, header):
        self.database_name = database_name
        self.header = header
        self.file_path = file_path
        self.file = f'{self.file_path}/{self.database_name}.csv'
        if os.path.exists(self.file):
            print('CSV already exists.')
        else:
            with open(self.file, 'w', newline='') as self.outfile:
                self.writer = csv.writer(self.outfile)
                self.writer.writerow(self.header)

    # write data to csv
    def write_to_csv(self, data_out, database_name, file_path):
        self.data_out = data_out
        self.database_name = database_name
        self.file_path = file_path
        self.file = f'{file_path}/{self.database_name}'
        with open(self.file, 'a', newline='') as self.outfile:
            self.writer = csv.writer(self.outfile, delimiter=',')
            self.writer.writerow(self.data_out)

    def json_to_csv(self, json_list, database_name, file_path, header, row):
        self.json_list = json_list
        self.database_name = database_name
        self.file_path = file_path
        self.header = header
        self.row = row
        self.create_csv(self.database_name, self.file_path, self.header)
        for self.json in self.json_list:
            self.write_to_csv(self.row, self.database_name, self.file_path)
