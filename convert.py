from bs4 import BeautifulSoup
from decimal import *
import requests


def convert(amount, cur_from, cur_to, date='', requests=requests):
    response = requests.get(f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={date}")
    soup = BeautifulSoup(response.content, "xml")
    if cur_from != 'RUR' and cur_to != 'RUR':
        from_ = Decimal((soup.find('CharCode', text=cur_from).find_next_sibling('Value').string).replace(',', '.'))
        Nominal_from = Decimal((soup.find('CharCode', text=cur_from).find_next_sibling('Nominal').string).replace(',', '.'))
        to_ = Decimal((soup.find('CharCode', text=cur_to).find_next_sibling('Value').string).replace(',', '.'))
        Nominal_to = Decimal((soup.find('CharCode', text=cur_to).find_next_sibling('Nominal').string).replace(',', '.'))
        result = Decimal((amount*(from_/Nominal_from))/(to_/Nominal_to))
        result = round(result, 4)
    elif cur_from == 'RUR' and cur_to != 'RUR':
        to_ = Decimal((soup.find('CharCode', text=cur_to).find_next_sibling('Value').string).replace(',', '.'))
        Nominal_to = Decimal((soup.find('CharCode', text=cur_to).find_next_sibling('Nominal').string).replace(',', '.'))
        result = Decimal(amount/(to_/Nominal_to))
        result = round(result, 4)
    elif cur_from != 'RUR' and cur_to == 'RUR':
        from_ = Decimal((soup.find('CharCode', text=cur_from).find_next_sibling('Value').string).replace(',', '.'))
        Nominal_from = Decimal((soup.find('CharCode', text=cur_from).find_next_sibling('Nominal').string).replace(',', '.'))
        result = Decimal((amount*(from_/Nominal_from)))
        result = round(result, 4)
    else:
        result = amount
        result = round(result, 4)
    return result
