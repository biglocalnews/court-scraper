from datetime import datetime, timedelta
from court_scraper.configs import Configs


def dates_for_range(start_date, end_date, input_format="%Y-%m-%d", output_format=None):
    start = datetime.strptime(start_date, input_format)
    end = datetime.strptime(end_date, input_format)
    dates = []
    number_of_days = (end - start).days + 1
    for num in range(number_of_days):
        dt = start + timedelta(num)
        try:
            dates.append(dt.strftime(output_format))
        except TypeError:
            dates.append(dt)
    return dates


def get_captcha_service_api_key():
    configs = Configs()
    return configs.captcha_service_api_key
