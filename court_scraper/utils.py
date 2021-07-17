from datetime import datetime, timedelta


def dates_for_range(start_date, end_date, input_format="%Y-%m-%d", output_format=None):
    #[start + datetime.timedelta(n) for n in range(int ((today - start).days +1))]
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
