"""Access metadata about the sites we cover."""
import csv
import io
import pkgutil
import typing


class SitesMeta:
    """Metadata about the places supported by court-scraper."""

    def __init__(self):
        self.data = self._get_sites_data()

    def get(self, place_id):
        """Get metadata about the provided place."""
        state = place_id[:2]
        county = place_id[3:].replace("_", " ")
        key = (state, county)
        return self.data[key]

    def get_url(self, state=None, county=None):
        """Get the home URL of the provided state and county."""
        key = (state, county)
        return self.data[key]["home_url"]

    def get_state_list(self, postal_code: str) -> typing.List:
        """Get a list of all sites in the provided state."""
        site_list = []
        for (state, county), site in self.data.items():
            if state.lower() == postal_code.lower():
                site_list.append(site)
        if len(site_list) == 0:
            raise ValueError("No sites found!")
        return site_list

    def _get_sites_data(self):
        try:
            # If the metadata is already in the cache, use that
            return self._data
        except AttributeError:
            # If we haven't pulled the data before read in the CSV
            text = self._get_sites_csv_text()
            reader = csv.DictReader(io.StringIO(text))
            data = {}
            for row in reader:
                state = row.pop("state")
                county = row.pop("county")
                row["place_id"] = f"{state.lower()}_{county.lower().replace(' ', '_')}"
                key = (state, county)
                data[key] = row
            self._data = data
            return self._data

    def _get_sites_csv_text(self):
        return pkgutil.get_data(__name__, "data/sites_meta.csv").decode("utf-8")
