from datetime import datetime, timedelta
import requests

Y_CRV = "0xfcc5c47be19d06bf83eb04298b026f81069ff65b"
SD_CRV = "0xd1b5651e55d4ceed36251c61c50c889b36f6abb5"
CVX_CRV = "0x62b9c7356a2dc64a1969e19c23e4f579f9810aa7"
PERIOD = 365 # in days

def iso_dates():
    # Current date with fixed hour at 11:00:00
    now = datetime.now().replace(hour=11, minute=0, second=0, microsecond=0)

    # Date from 1 year ago with fixed hour at 11:00:00
    one_year_ago = (now - timedelta(days=PERIOD)).replace(hour=11, minute=0, second=0, microsecond=0)

    # Format dates into ISO format with milliseconds
    iso_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    now_str = now.strftime(iso_format)[:-3] + "Z"
    one_year_ago_str = one_year_ago.strftime(iso_format)[:-3] + "Z"

    return now_str, one_year_ago_str

def build_link(token):
    today, year_before = iso_dates()
    start = "https://www.defiwars.xyz/api/peg-history?fromToken="+token+"&toToken=0xd533a949740bb3306d119cc777fa900ba034cd52&"
    start += "startDate=" + year_before + "&endDate=" + today + "&precision=all"
    return start

def get_json(link):
    response = requests.get(link)

    if response.status_code == 200:
        data_json = response.json()
        return data_json["dataPoints"]
    else:
        print("Erreur:", response.status_code)

def get_average(json):
    sum = 0
    for i in range(len(json)):
        sum += float(json[i]["pegPercentage"])
    return sum / len(json)

def get_all_pegs():
    return get_average(get_json(build_link(Y_CRV))), get_average(get_json(build_link(CVX_CRV))), get_average(get_json(build_link(SD_CRV)))

def print_all_pegs():
    y_crv, cvx_crv, sd_crv = get_all_pegs()
    print("Y_CRV:\t", "{:.2f}".format(y_crv * 100),"%")
    print("SD_CRV:\t", "{:.2f}".format(sd_crv * 100),"%")
    print("CVX_CRV:", "{:.2f}".format(cvx_crv * 100),"%")

print_all_pegs()
