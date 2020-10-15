from lxml import etree
from io import StringIO, BytesIO

class Parser:
    
    def __init__(self):
        self.lxml_parser = etree.HTMLParser()

    
    def open_html(self, html_file):
        self.html_file = html_file
        self.html = open(self.html_file, "r")
        self.html = self.html.read()
        return etree.parse(StringIO(self.html), self.lxml_parser)
    
    def _get_info(self, location):
        self.location = location
        return self.tree.xpath(self.location)
    
    def clean(self, dirty):
        self.dirty = dirty
        self.dirty = self.dirty.lower().strip().replace('\n', ' ')
        return self.dirty

    def assign_element(self, location):
        self.info = self._get_info(location)
        if isinstance(self.info, list):
            if len(self.info) == 0:
                #print('length is 0')
                return 'none'
            elif self.info[0].text != None and self.clean(self.info[0].text) != '':
                #print('position 1 is not none')
                return self.clean(self.info[0].text)
            else:
                #print('should be returning string of none')
                return 'none'
        elif self.info == None:
            #print('not a list, is none')
            return 'none'
        else:
            #print('not a list, not none')
            return self.info
    
    def assign_elements(self, location):
        self.info = self._get_info(location)
        return self.info
        if isinstance(self.info, list):
            if len(self.info) == 1:
                raise ElementException('Element only returned one element. Try assign_element (singular)')
            else:
                return self.info
        else:
            raise ElementException('Element only returned one element. Try assign_element (singular).')
    
    
    def get_length(self, location):
        self.info = self._get_info(location)
        return len(self.info)
    
    # this function writes multiples 'none's to a given list until that list is 3 items long
    def expand_list(self, list, length):
        self.list = list
        self.length = length
        while len(self.list) < self.length:
            try:
                self.list.append('none')
            except:
                pass
        return self.list

    def more_than(self, list, count):
        self.list = list
        self.count = count
        if len(self.list) > self.count:
            return 'yes'
        else:
            return 'no'
        
    def text_between(self, text, before, after):
        self.text = text
        self.before = before
        self.after = after
        try:
            self.parse = self.text.split(self.before)
            self.parse = self.parse[1].split(self.after)
            self.parse = self.clean(self.parse[0])
        except:
            self.parse = 'none'
        return self.parse

    def does_string_appear(self, text, string):
        self.text = text
        self.string = string
        self.test = self.text.find(self.string)
        if self.test != -1:
            return 'yes'
        else:
            return 'no'
    
    #this function provides an entry_point to the best xpath logic for new users
    #it follows this logic{div/table item is in}/{div/html element text is in}/{text to search}/{xpath to follow to get to relative field}
    def string_search(self, text, table, route=None, text_location=None):
        self.text = text
        self.table = table
        self.route = route
        self.text_location = text_location
        if self.text_location == None and self.route == None:
            #('no location and no route')
            return self.assign_element(f'{self.table}//*[contains(text(), "{text}")]')
        elif self.text_location == None and self.route != None:
            #('no location')
            return self.assign_element(f'{self.table}//*[contains(text(), "{text}")]/{self.route}')
        elif self.text_location != None and self.route == None:
            #('no route')
            return self.assign_element(f'{self.table}//{self.text_location}[contains(text(), "{text}")]')
        elif self.text_location != None and self.route != None:
            #('location and route')
            return self.assign_element(f'{self.table}//{self.text_location}[contains(text(), "{text}")]/{self.route}')
    
    
    # this function creates a new database and failure log but wont overwrite existing one
    def create_dataframe(self, database_name, header):
        self.database_name = database_name
        self.header = header
        self.file = f'{file_path}/{self.database_name}'
        if path.exists(self.file):
            print('CSV already exists.')
        else:
            with open(self.file, 'w', newline='') as self.outfile:
                self.writer = csv.writer(self.outfile)
                self.writer.writerow(self.header)
            print('New CSV created.')
    
    def write_data(self, data_out, database_name):
        #writing data to csv
        self.data_out = data_out
        self.database_name = database_name
        self.file = f'{file_path}/{self.database_name}'
        with open(self.file, 'a', newline='') as self.outfile:
            self.writer = csv.writer(self.outfile, delimiter=',')
            self.writer.writerow(self.data_out)