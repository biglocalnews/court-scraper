import re

from lxml import html
from bs4 import BeautifulSoup


class CaseDetailParser:

    def __init__(self, page_source):
        self.page_source = page_source
        self.tree = html.fromstring(page_source)
        self.soup = BeautifulSoup(page_source, 'html.parser')

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name) # e.g. case_number or court or file_date
        except AttributeError:
            titlecase_name = name.replace('_', ' ').title()
            return self._get_text_from_p_tag(titlecase_name)

    @property
    def parties(self):
        party_div = self._get_party_div()            
        party_types = ['Plaintiff','Defendant','Respondant']
        party_output = []
        for span in party_div.find_all(class_=re.compile("tyler-span")):
            party_dict = {}
            name_elem = span.find_all("p")[0]
            for party in party_types:
                if party in span.get_text():
                    party_dict['party_type'] = party
                    party_dict['party_name'] = ' '.join(name_elem.text.replace(party, '').split())
                    if 'Address' in span.get_text():
                        address_elem = span.find_all("p")[1]
                        party_dict['address'] = ' '.join(address_elem.text.split())
                    if 'Lead Attorney' in span.get_text():
                        for div in span.find_all("div"):
                            if 'Lead Attorney' in div.get_text():
                                attorney_elem = div
                                party_dict['attorney'] = ' '.join(attorney_elem.text.replace('Lead Attorney', '').split())
                    else:
                        for div in span.find_all("div"):
                            if 'Attorneys' in div.get_text():
                                attorney_elem = div.next_sibling.next_sibling
                                if attorney_elem:
                                    party_dict['attorney'] = ' '.join(attorney_elem.text.replace('Retained', '').split())
            if party_dict:
                party_output.append(party_dict)    
        return party_output

    @property
    def disposition(self):
        try:
            judgment_date = self.tree.xpath("//div[@id='dispositionInformationDiv']//text[text() = 'Judgment']/../text()")
        except:
            judgment_date = None
        try:
            judgment = self.tree.xpath("//div[@id='dispositionInformationDiv']//span[contains(text(), 'Judgment Type')]/../text()[last()]")
        except:
            judgment = None
        try:
            judgment_for = self.tree.xpath("//div[@id='dispositionInformationDiv']//span[contains(text(), 'Judgment For')]/following-sibling::span/text()")
        except:
            judgment_for = None
        disposition_output = []
        for i in range(len(judgment_date)):
            disposition_dict = {}
            disposition_dict['judgment_date'] = judgment_date[i].strip()
            disposition_dict['judgment'] = judgment[i].strip()
            if judgment_for:
                disposition_dict['judgment_for'] = judgment_for[i].strip()
            disposition_output.append(disposition_dict)
        return disposition_output

    def _get_text_from_p_tag(self, lookup_text):
        # Select last text node of span's parent p tag
        xpath = "//span[contains(text(), '{}')]/../text()[last()]".format(
            lookup_text
        )
        return self.tree.xpath(xpath)[0].strip()

    def _get_party_div(self):
        # Get the Party info div which contains
        # one or more parties
        return self.soup.select('#divPartyInformation_body')[0]

        