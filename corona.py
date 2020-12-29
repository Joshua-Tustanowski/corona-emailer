from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import smtplib
import config

DEBUG = True

class coronavirus():
    def __init__(self) :
        self.options = Options()
        self.options.headless = True
        self.driver = webdriver.Chrome(options=self.options)
        self.user = config.EMAIL_ADDRESS
        self.password = config.PASSWORD

    def get_data(self):
        try:
            self.driver.get('https://www.worldometers.info/coronavirus/')
            table = self.driver.find_element_by_xpath('//*[@id="main_table_countries_today"]/tbody[1]')
            country_element = table.find_element_by_xpath('//a[contains(text(), "Bhutan")]/./.././..')

            data = table.text.split(" ")

            country_element = data[0]
            total_cases = data[1]
            new_cases = data[2]
            total_deaths = data[3]
            new_deaths = data[4]
            active_cases = data[5]
            total_recovered = data[6]
            serious_critical = data[7]
            self.driver.close()
            if DEBUG:
                print("Sucessfully scraped")
                print("Country: " + country_element)
                print("Total cases: " + total_cases)
                print("New cases: " + new_cases)
                print("Total deaths: " + total_deaths)
                print("New deaths: " + new_deaths)
                print("Active cases: " + active_cases)
                print("Total recovered: " + total_recovered)
                print("Serious, critical cases: " + serious_critical)

            return {
                'country_element': country_element,
                'total_cases': total_cases,
                'new_cases': new_cases,
                'total_deaths': total_deaths,
                'new_deaths': new_deaths,
                'active_cases': active_cases,
                'total_recovered': total_recovered,
                'serious_critical': serious_critical
            }
        except Exception as ex:
            print("something went wrong")
            self.driver.quit()
            raise ex

    def send_email(self, country_element, total_cases, new_cases, total_deaths, new_deaths, active_cases, total_recovered, serious_critical):
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(self.user, self.password)
            print('Login details: {self.user} \t {self.password}')

            subject = 'Coronavirus statistics in your country today!'

            body = f'Today in {country_element}\n'
            body += 'There is new data on the coronavirus:\n'
            body += f'Total cases: {total_cases}\n'
            body += f'New cases: {new_cases}\n'
            body += f'Total deaths: {total_deaths}\n'
            body += f'New deaths: {new_deaths}\n'
            body += f'Active cases: {active_cases}\n'
            body += f'Total recovered: {total_recovered}\n'
            body += f'Serious, critical cases: {serious_critical}\n'
            body += "Check the link: https://www.worldometer.info/coronavirus/\n"

            message = 'Subject: {0}\n\n{1}'.format(subject, body)
            if DEBUG:
                print(body)

            server.sendmail(self.user, self.user, message)
            print("Email has been sent!")
            server.quit()
        except Exception as ex:
            print("[ERROR] couldn't email")
            raise ex

if __name__ == '__main__':
    corona_email_client = coronavirus()
    data = corona_email_client.get_data()
    corona_email_client.send_email(**data)
