from datetime import datetime, timedelta
from decimal import Decimal

from numpy import double

from .models import Detail, Crypto


def get_date_range(numdays):
    """ """
    date_now = datetime.now()
    days = [date_now - timedelta(days=day) for day in range(numdays)]
    days_string = [date.strftime('%Y-%m-%d') for date in sorted(days)]
    return days_string



def get_moving_average(date, numdays, crypto, currency):
    """ The moving average is calculated"""
    date_start = datetime.strptime(date, '%Y-%m-%d') - timedelta(days=numdays)

    crypto = Crypto.objects.filter(crypto=crypto).first()
    close_prices = list(
        Detail.objects.filter(
            currency_name_id=crypto.id, currency=currency, time_stamp__gte=date_start
        ).values('close')
    )

    ma = sum([double(row.get('close')) for row in close_prices]) / len(close_prices)
    return ma
