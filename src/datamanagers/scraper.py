import argparse

from bs4 import BeautifulSoup
import requests
from typing import Dict, List


def get_all_daily_data() -> Dict[str, List[str]]:
    html = requests.get("https://www.worldometers.info/coronavirus/")
    soup = BeautifulSoup(html.text, "html.parser")

    table = soup.find("table")
    tbody = table.find("tbody")
    results = {}
    for tr in tbody.find_all("tr"):
        res = [td.text for td in tr.find_all("td")]
        country_key = res[1].replace("\n", "")
        cases_info = res[2:15]
        results[country_key] = cases_info
    return results


def get_daily_data_for_country(country: str) -> List[str]:
    results = get_all_daily_data()
    try:
        country_data = results[country]
    except KeyError:
        raise KeyError
    return country_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--country", help="select a country to get covid data on")
    args = parser.parse_args()
