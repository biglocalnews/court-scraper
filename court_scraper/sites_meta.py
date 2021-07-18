import csv
import io
import pkgutil


class SitesMeta:

    def __init__(self):
        self.data = self._get_sites_data()

    def get(self, place_id):
        state = place_id[:2]
        county = place_id[3:].replace('_', ' ')
        key = (state, county)
        return self.data[key]

    def get_url(self, state=None, county=None):
        key = (state, county)
        return self.data[key]['home_url']

    def _get_sites_data(self):
        try:
            return self._data
        except AttributeError:
            text = self._get_sites_csv_text()
            reader = csv.DictReader(
                io.StringIO(text)
            )
            data = {}
            for row in reader:
                state = row.pop('state')
                county = row.pop('county')
                key = (state, county)
                data[key] = row
            self._data = data
            return self._data

    def _get_sites_csv_text(self):
        return pkgutil.get_data(
            __name__,
            'data/sites_meta.csv'
        ).decode('utf-8')
