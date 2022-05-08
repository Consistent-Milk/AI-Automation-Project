from datetime import date, timedelta
import pandas as pd


def date_list(s_year, s_month, s_date, e_year, e_month, e_date):
    sdate = date(s_year, s_month, s_date)  # start date
    edate = date(e_year, e_month, e_date)  # end date
    dates1 = pd.date_range(sdate, edate - timedelta(days=1), freq='d')
    dates2 = dates1.date
    allowed_dates = []

    for i in range(len(dates2)):
        allowed_dates.append(dates2[i].isoformat())

    return allowed_dates
