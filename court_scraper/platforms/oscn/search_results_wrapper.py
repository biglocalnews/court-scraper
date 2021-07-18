
class SearchResultsWrapper(dict):

    def __repr__(self):
        return self.__class__.__name__

    @property
    def dates(self):
        return sorted([k for k in self.keys()])

    @property
    def cases(self):
        try:
            return self._cases
        except AttributeError:
            cases = []
            for date_key, data in self.items():
                cases.extend(data['cases'])
            self._cases = cases
            return self._cases

    @property
    def case_types(self):
        return sorted(list({case.type_short for case in self.cases}))

    @property
    def count_of_days(self):
        return len(self.keys())

    def add_case_data(self, day, results):
        data = self._get_data_by_key(day)
        data['cases'].extend(results)

    def add_html(self, day, html):
        data = self._get_data_by_key(day)
        data['html'] = html

    def _get_data_by_key(self, key):
        try:
            data = self[key]
        except KeyError:
            self[key] = {'html': None, 'cases': []}
            data = self[key]
        return data
