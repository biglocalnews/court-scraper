class FultonParser(Parser):
    
    def fulton_eviction(self):
        
        #section/div identifiers
        self.case_summary = '//*[@ng-if="::data.roaSections.caseSummary"]'
        self.case_info = '//*[@ng-if="::data.roaSections.caseInformation"]'
        self.assignment_info = '//*[@ng-if="::data.roaSections.assignmentInformation"]'
        self.party_info = '//*[@ng-if="::data.roaSections.partySection"]'
        self.events = '//*[@ng-if="::data.roaSections.combinedEvents"]'
        self.financial_info = '//*[@ng-if="::data.roaSections.financialSummarySection"]'
        
        #xpath route from key to value
        self.standard_route = '/following::div/span'
        
        
        #string_search(self, text, table='', route=None, text_location=None):
        #case_summary div
        self.case_number = self.string_search('No.', table=self.case_summary, route='/ancestor::div/span[2]')
        self.case_name = self.string_search('vs', table=self.case_summary)
        #self.location = self.find_text_by_xpath('//*[@ng-if="::data.roaSections.caseSummary"]//*[contains(text(), "Location:")]//following::div/span')
        self.location = self.string_search('Location:', table=self.case_summary, route=self.standard_route)
        self.judge = self.string_search('Judicial Officer:', table=self.case_summary, route=self.standard_route)
        self.filed_on = self.string_search('Filed on:', table=self.case_summary, route=self.standard_route)
    
        #case_information
        self.case_type = self.string_search('Type:', table=self.case_info, route='/following::td')
        self.case_status = self.string_search('Status:', table=self.case_info, route='/following::td/div/div/span[3]')
        self.case_status_date = self.string_search('Status:', table=self.case_info, route='/following::td/div/div/span[1]')
        
        #assignment_information
        self.date_judge_assigned = self.string_search('Assigned', table=self.assignment_info, route='/following::div/span')
        
        #party info
        #'//*[@ng-if="::data.roaSections.partySection"]//*[contains(text(), "Defendant")]/'
        #self.defendant_name = self.string_search('Defendant', table=self.party_info, route='/parent::td/following::td/table/tbody/tr/td')
        self.defendant_name = self.case_name.split('vs.')[1].replace(',',' ').replace('all others', '').replace(' and', '').strip()
        self.defendant_attorney = self.string_search('Defendant', table=self.party_info, route='/parent::td/following::td[3]/div/div/div/div/div')
        #self.plaintiff_name = self.string_search('Plaintiff', table=self.party_info, route='/parent::td/following::td/table/tbody/tr/td')
        self.plaintiff_name = self.case_name.split('vs.')[0]
        self.plaintiff_attorney = self.string_search('Plaintiff', table=self.party_info, route='/parent::td/following::td[3]/div/div/div/div/div')
        
            
        #events and orders
        self.writ_of_possession = self.find_text_by_xpath('//*[@label="WRIT OF POSSESSION"]//parent::div/parent::div/parent::div/parent::div/div/div/span')
        self.writ_to_marshall =  self.string_search('Served:', table=self.events, route='/parent::div/parent::div/parent::div/parent::div/parent::div/parent::div/div/div/span')
        self.writ_served =  self.string_search('Served:', table=self.events).replace('served: ', '')
        self.writ_vacated = self.find_text_by_xpath('//*[@label="WRIT OF POSSESSION (VACATED)"]//parent::div/parent::div/parent::div/parent::div/div/div/span') 
        self.writ_held_up = self.find_text_by_xpath('//*[@label="WRIT OF POSSESSION (HELD UP)"]//parent::div/parent::div/parent::div/parent::div/div/div/span') 
        self.default_judgment = self.find_text_by_xpath('//*[@label="DEFAULT JUDGMENT"]//parent::div/parent::div/parent::div/parent::div/div/div/span')
        self.consent_order = self.find_text_by_xpath('//*[@label="CONSENT ORDER"]//parent::div/parent::div/parent::div/parent::div/div/div/span') 
        self.consent_agreement = self.find_text_by_xpath('//*[@label="CONSENT AGREEMENT"]//parent::div/parent::div/parent::div/parent::div/div/div/span')
        self.order_and_judgment = self.find_text_by_xpath('//*[@label="ORDER AND JUDGMENT"]//parent::div/parent::div/parent::div/parent::div/div/div/span')  
        self.satisfaction = self.string_search('SATISFACTION OF JUDGMENT', table=self.events, route='/parent::div/parent::div/parent::div/parent::div/parent::div/div/div/span')
        self.transfer_date = self.string_search('TRANSFER', table=self.events, route='/parent::div/parent::div/parent::div/parent::div/parent::div/div/div/span')
        #old scrapes show that this xpath only returned cases that fit the timeline of the cares act
        self.cares_act = self.find_text_by_xpath('//*[@label="AFFIDAVIT"]//parent::div/parent::div/parent::div/parent::div/div/div/span')
        
        #financial info
        self.plaintiff_fees = self.string_search('Total Financial Assessment', table=self.financial_info, route='/following::div')
        
        ### data out
        self.data_out = {
            #case summary div
            'case_number' : self.case_number, 
            'location' : self.location, 
            'judge' : self.judge, 
            'date_filed' : self.filed_on,
            #case_information
            'case_type' : self.case_type,
            'case_status' : self.case_status, 
            'case_status_data' : self.case_status_date,
            #party_information
            'defendant_name' : self.defendant_name,
            'defendant_attorney' : self.defendant_attorney, 
            'plaintiff_name' : self.plaintiff_name,
            'plaintiff_attorney' : self.plaintiff_attorney,
            #assignment_information
            'date_judge_assigned' : self.date_judge_assigned,
            #events and orders
            'writ_of_possession' : self.writ_of_possession,
            'writ_to_marshall' : self.writ_to_marshall, 
            'writ_served' : self.writ_served, 
            'writ_vacated' : self.writ_vacated,
            'writ_held_up' self.writ_held_up,
            'default_judgment' : self.default_judgment, 
            'consent_order' : self.consent_order,
            'consent_agreement' : self.consent_agreement,
            'order_and_judgment' : self.order_and_judgment,
            'satisfaction' : self.satisfaction,
            'transfer_date' : self.transfer_date,
            'cares_act' : self.cares_act,
            #financial info
            'plaintiff_fees' : self.plaintiff_fees,
            'case_name' : self.case_name
        }