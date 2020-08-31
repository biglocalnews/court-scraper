from datetime import datetime, timedelta, date

class LastDate:
    
    def __init__(self):
        now = date.today()
        self.current_year = now.year
        self.current_day = now

    def _most_recent_workday(self, last_day):
        #.weekday returns a 0 - 4 for Monday - Friday
        if last_day.weekday() < 5:
            return last_day
        else:
            difference = (last_day.weekday() - 4)
            other_day = (last_day - timedelta(days=difference))
            return other_day

    # function returns most recent weekday
    def date_to_search(self, year, subtract_days=1):
        if len(str(year)) != 4:
            return Exception('year format must conform to XXXX')
        else:
            pass
        if year == self.current_year:
            yesterday = (date.today() - timedelta(days=subtract_days))
            return self._most_recent_workday(yesterday)
        else:
            last_day = (date.fromisoformat(f'{year}-12-31') - timedelta(days=(subtract_days - 1)))
            return self._most_recent_workday(last_day)