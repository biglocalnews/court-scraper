from ._last_date import LastDate

class SearchPageMixIn():

    lastdate = LastDate()

    def _county_specific_selenium_search(self):
        raise CountyNotSupported('County is not supported. Are you a developer? Did you forget to provide county-specific steps for searching?')
    
    def _get_last_workday(self, subtract_days = 1):
        self.subtract_days = subtract_days
        self.url_date = self.lastdate.date_to_search(self.year, subtract_days = subtract_days).strftime("%m/%d/%y")

    def _subtract_another_day(self, subtract_days = 1):
        self.subtract_days = self.subtract_days + subtract_days

    def _parse_case_table(self):
        if self.driver != None:
            self.single_case_result = None
            self.case_number = None
            try:
                self.single_case_result = self.driver.find_element(*self.single_case_locator).text
            except:
                pass
            try:
                self.case_rows = self.driver.find_elements(*self.row_locator)
            except:
                pass
        else:
            self.parser = etree.HTMLParser()
            self.tree = etree.parse(StringIO(self.output.text), self.parser)
            self.case_rows = self.tree.xpath(f'//*[contains(text(), "{self.case_prefix}-")]')
            self.case_number = self.case_rows[len(self.case_rows)-1].text
        if self.case_number != 'No records found' and self.case_number != None:
            return self.case_number
        elif self.single_case_result != None:
            return self.single_case_result
        else:
            raise IndexError()

    def _search_previous_day_until_success(self):
        result = None
        while result is None:
            try:
                print('subtracting another day')
                self._subtract_another_day()
                print('getting next workday')
                self._get_last_workday(subtract_days = self.subtract_days)
                print('calling new html search')
                if self.driver != None:
                    self._county_specific_selenium_steps()
                else:
                    self.output = self.get_html(self.url, payload = self.payload)
                print(f'attempting to parse case table for {self.url_date}')
                result = self._parse_case_table()
            except IndexError:
                pass  
        return result

    def most_recent_case(self, county, year, case_prefix, session=None, driver=None, row_locator=None, single_case_locator=None):
        self.county = county
        self.year = year
        self.case_prefix = case_prefix
        self.driver = driver
        self.row_locator = row_locator
        self.single_case_locator = single_case_locator
        self.session = session
        self._get_last_workday()
        if self.driver != None:
            self._county_specific_selenium_steps()
        else:
            self.output = self.get_html(self.url, payload = self.payload) 
        try:
            return self._parse_case_table()
        except:
            return self._search_previous_day_until_success()