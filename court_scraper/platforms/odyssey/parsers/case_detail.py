from lxml import html


class CaseDetailParser:

    def __init__(self, page_source):
        self.page_source = page_source
        self.tree = html.fromstring(page_source)

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            titlecase_name = name.replace('_', ' ').title()
            return self._get_text_from_p_tag(titlecase_name)

    @property
    def plaintiffs(self):
        party_div = self._get_party_div()
        breakpoint()
        # TODO: Need to extract plaintiffs
        return None

    @property
    def defendants(self):
        pass

    def _get_text_from_p_tag(self, lookup_text):
        # Select last text node of span's parent p tag
        xpath = "//span[contains(text(), '{}')]/../text()[last()]".format(
            lookup_text
        )
        return self.tree.xpath(xpath)[0].strip()

    def _get_party_div(self):
        # Get the Party info div which contains
        # one or more parties
        return self.tree.cssselect('#divPartyInformation_body')[0]