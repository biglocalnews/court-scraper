from datetime import datetime, timedelta, date

yesterday = date.today() - timedelta(days=1)
print(yesterday.weekday())