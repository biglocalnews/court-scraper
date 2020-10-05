from datetime import timedelta, datetime
from pandas.tseries.holiday import USFederalHolidayCalendar

class LastDate:

    def __init__(self):
        now = datetime.today()
        self.current_year = now.year
        self.current_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        self.cal = USFederalHolidayCalendar()

    def _most_recent_workday(self, last_day):
        #returns most recent workday, accounting for federal holidays and weekends
        self.holidays = self.cal.holidays(datetime(self.input_year, 1, 1), datetime(self.input_year, 12, 31)).to_pydatetime()
        if self.search_date.weekday() < 5 and self.search_date not in self.holidays:
            pass
        elif self.search_date.weekday() < 5 and self.search_date in self.holidays:
            self.search_date = (self.search_date - timedelta(days = 1))
            if self.search_date.weekday() < 5:
                pass
            else:
                difference = (self.search_date.weekday() - 4)
                self.search_date = (self.search_date - timedelta(days=difference))
        else:
            difference = (self.search_date.weekday() - 4)
            self.search_date = (self.search_date - timedelta(days=difference))
        return self.search_date

    # function returns most recent weekday with an option to manually override
    def date_to_search(self, year, subtract_days = 1):
        if len(str(year)) != 4:
            return Exception('year format must conform to XXXX')
        else:
            pass
        self.input_year = year
        if self.input_year == self.current_year:
            self.search_date = (self.current_day - timedelta(days=subtract_days))
            return self._most_recent_workday(self.search_date)
        else:
            self.search_date = (datetime(self.input_year, 12, 31) - timedelta(days=(subtract_days - 1)))
            return self._most_recent_workday(self.search_date)