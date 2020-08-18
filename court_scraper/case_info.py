class CaseInfo:
    """
    Encapsulates data from web scraping search results,
    and provides the ability to map fields to 
    standardized names.

    USAGE:

        from court_scraper.case_info import CaseInfo
        # Provide  a mapping of raw field -> standard field
        CaseInfo._map = { 'case_num': 'number' }

        # Supply data to class
        data = { 'foo': 'bar', 'case_num': 1 }
        ci = CaseInfo(data)

        # Mapped fields will appear under standard name
        assert ci.number = 1

        # Unmapped fields will appear under raw field name
        assert ci.foo == bar

    """

    _map = {}

    def __init__(self, data):
        self.data = data
        for key, val in data.items():
            try:
                field = self._map[key]
            except KeyError:
                field = key
            setattr(self, field, val)

    @property
    def standard_data(self):
        """
        Return data dict of fields that map
        to Case table columns.
        """
        return {
            'place_id': self.place_id,
            'number': self.number,
            'status': self.status,
        }
