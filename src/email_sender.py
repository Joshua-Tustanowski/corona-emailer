import argparse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import smtplib

from db import config
from datamanagers import get_daily_data_for_country

DEBUG = False


def main(country):
    email_client = CoronavirusEmailer()
    covid_data = get_daily_covid_data(country)
    email_client.send_email(country, **covid_data)


def extract_data_fields(row):
    columns = [
        "total_cases",
        "new_cases",
        "total_deaths",
        "new_deaths",
        "active_cases",
        "total_recovered",
        "serious_critical",
    ]
    return {column: row[i] for i, column in enumerate(columns)}


def get_daily_covid_data(country):
    return extract_data_fields(get_daily_data_for_country(country))


class CoronavirusEmailer:
    def __init__(self):
        self.options = Options()
        self.options.headless = True
        self.driver = webdriver.Chrome(options=self.options)
        self.user = config.EMAIL_ADDRESS
        self.password = config.PASSWORD

    def get_data(self, country: str):
        try:
            self.driver.get("https://www.worldometers.info/coronavirus/")
            table = self.driver.find_element_by_xpath(
                '//*[@id="main_table_countries_today"]/tbody[1]'
            )
            country_element = table.find_element_by_xpath(
                f"//a[contains(text(), '{country}')]/./.././.."
            )
            country_data = extract_data_fields(country_element.text.split(" ")[1:])
            self.driver.close()
            return country_data
        except Exception as ex:
            print(f"[Error] Failed to scrape the page {ex}")
            self.driver.quit()
            return {}

    def send_email(
        self,
        country_code,
        total_cases,
        new_cases,
        total_deaths,
        new_deaths,
        active_cases,
        total_recovered,
        serious_critical,
    ):
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(self.user, self.password)
            url = "https://www.worldometers.info/coronavirus"
            if country_code != "World":
                url = f"{url}/country/{country_code}/"
            subject = "Coronavirus statistics in your country today!"

            body = f"Today in {country_code}\n"
            body += "There is new data on the coronavirus:\n"
            body += f"Total cases: {total_cases}\n"
            body += f"New cases: {new_cases}\n"
            body += f"Total deaths: {total_deaths}\n"
            body += f"New deaths: {new_deaths}\n"
            body += f"Active cases: {active_cases}\n"
            body += f"Total recovered: {total_recovered}\n"
            body += f"Serious, critical cases: {serious_critical}\n"
            body += f"Check the link: {url}\n"

            message = "Subject: {0}\n\n{1}".format(subject, body)
            if DEBUG:
                print(body)

            server.sendmail(self.user, self.user, message)
            print("Email has been sent!")
            server.quit()
        except Exception as ex:
            print("[ERROR] couldn't email")
            raise ex


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--country", help="select a country to get covid data on")
    args = parser.parse_args()
    main(args.country)
