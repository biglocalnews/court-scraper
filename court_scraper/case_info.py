class CaseInfo:
    """
    Encapsulates data from web scraping search results,
    and provides the ability to map fields to standardized names.

    Args:
        data (dict): Dict used to create instance attributes

    Usage:
        Configure CaseInfo class with a dictionary that maps
        raw field name (key) to standardized field name (value):

        >>> from court_scraper.case_info import CaseInfo
        >>> CaseInfo._map = { 'case_num': 'number' }

        Instantiate the class with data:

        >>> data = { 'case_num': 1, 'foo': 'bar' }
        >>> case_info = CaseInfo(data)

        Mapped fields will be accessible via dotted-attribute notation
        using the standardized name:

        >>> assert case_info.number = 1

        Unmapped fields will be accessible using raw field name:

        >>> assert case_info.foo == bar

    """

    _map = {}

    def __init__(self, data):
        self.data = data
        self._set_attrs(data)

    @property
    def standard_data(self):
        """
        Return data dict of fields that map
        to Case table columns.
        """
        data = {
            'place_id': self.place_id,
            'number': self.number,
        }
        # Strongly encouraged, not always available
        for attr in ['filing_date', 'status']:
            try:
                data[attr] = getattr(self, attr)
            except AttributeError:
                data[attr] = None
        return data

    def merge(self, case_info):
        self.data.update(case_info.data)
        self._set_attrs(case_info.data)

    def _set_attrs(self, data):
        for key, val in data.items():
            try:
                field = self._map[key]
            except KeyError:
                field = key
            setattr(self, field, val)
