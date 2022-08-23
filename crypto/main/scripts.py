import requests
import os
import pandas as pd
import csv
import argparse
from .models import Crypto, Detail

base_url = 'https://www.alphavantage.co/query?'
function = 'DIGITAL_CURRENCY_DAILY'


def get_raw_response(symbol, market, base_url=base_url, function=function):
    """ Cryptocurrency data is received from the provided source """
    return requests.get(
        f'{base_url}function={function}&symbol={symbol}&market={market}&apikey={None}&datatype=csv')


def parse_response(response):
    """ Data is prepared and divided into a table """
    csv_string = response.content.decode('utf-8')
    splitting_to_lines = csv_string.splitlines()
    reader = csv.reader(splitting_to_lines)
    return list(reader)


def upload_to_database(data, market, symbol):
    """ The user selects a currency, if it is not available, it is written to the database as new.
    If the currency is found, the data is transferred to the database """
    list_of_ds_objects = []
    crypto = Crypto.objects.filter(crypto=symbol).first()

    if not crypto:
        crypto = Crypto(crypto=symbol).save()

    existing_dates = list(Detail.objects.filter(currency_name_id=crypto.id,
                                                currency=market).values_list('time_stamp', flat=True))
    for row in data[1:]:
        if row[0] not in existing_dates:
            crypto_row = Detail(time_stamp=row[0], open=row[1], high=row[2], low=row[3], close=row[4], volume=row[5],
                                market_cap=row[6], created_at=row[7], currency=market,
                                currency_name_id=crypto.id)
            list_of_ds_objects.append(crypto_row)

    Detail.objects.bulk_create(list_of_ds_objects)


def run_script(symbol, market):
    """ The market and symbol are submitted and command is called for transfer data """
    response = get_raw_response(symbol, market)
    data = parse_response(response)
    upload_to_database(data, market, symbol)
