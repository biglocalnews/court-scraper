class CaseManager:
    
    parse = Parser()
    
    def _clean_existing_case_list(self, existing_case_list):
        self.existing_case_list = existing_case_list
        self.clean_existing_cases = []
        for self.case_item in self.existing_case_list:
            self.clean_existing_cases.append(self.case_item.split('\\')[1].replace(self.file_type, ''))
        return self.clean_existing_cases
    
    def _assemble_possible_range(self, range_start, range_end, prefix='', suffix=''):
        self.prefix = prefix
        self.suffix = suffix
        self.range_start = range_start
        self.range_end = range_end
        self.all_case_numbers = []
        for self.possible_number in range(self.range_start, self.range_end):
                self.all_case_numbers.append(f'{self.prefix}{self.possible_number}{self.suffix}')
        return self.all_case_numbers
    
    def strip_case_list(self, input_case_list, prefix='', suffix=''):
        self.input_case_list = input_case_list
        self.strip_prefix = prefix
        self.strip_suffix = suffix
        self.output_case_list = []
        for self.case_item in self.input_case_list:
            self.output_case_list.append(self.case_item.replace(self.strip_prefix, '').replace(self.strip_suffix, ''))
        return self.output_case_list
    
    def find_missing_cases(self, html_dir, file_type, range_start, range_end, prefix='', suffix='', strip=False):
        self.prefix = prefix
        self.suffix = suffix
        self.range_start = range_start
        self.range_end = range_end + 1
        self.html_dir = html_dir
        self.file_type = file_type
        self.strip = strip
        self.existing_case_list = self.parse.get_files(self.html_dir, self.file_type)
        self.clean_existing_cases = self._clean_existing_case_list(self.existing_case_list)
        self.possible_case_range = self._assemble_possible_range(self.range_start, self.range_end, self.prefix, self.suffix)
        self.missing_cases = []
        for self.possible_case_item in self.possible_case_range:
            if self.possible_case_item not in self.clean_existing_cases:
                self.missing_cases.append(self.possible_case_item)
        if self.strip:
            self.missing_cases = self.strip_case_list(self.missing_cases, self.prefix, self.suffix)
        return self.missing_cases
