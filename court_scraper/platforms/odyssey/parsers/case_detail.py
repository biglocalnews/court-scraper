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

    def _get_text_from_p_tag(self, lookup_text):
        # Select last text node of span's parent p tag
        xpath = "//span[contains(text(), '{}')]/../text()[last()]".format(
            lookup_text
        )
        return self.tree.xpath(xpath)[0].strip()
