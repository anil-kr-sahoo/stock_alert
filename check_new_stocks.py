import json
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

filter_url = "https://groww.in/stocks/filter?closePriceHigh=100000&closePriceLow=0&index=Nifty%20Next%2050," \
             "Nifty%20Midcap%20100,Nifty%2050,Nifty%20100,BSE%20100&marketCapHigh=2000000&marketCapLow=0&page=0&size=1000&sortType=ASC"
driver = None


def get_float_val(string_num):
    try:
        return float(string_num)
    except Exception:
        return 0


def get_two_decimal_val(decimal_num):
    return float('%.2f' % decimal_num)


def get_current_stock_price():
    raw_html = driver.find_element(By.CLASS_NAME, "lpu38Pri").get_attribute('innerHTML').split('hidden;">')[1:]
    raw_amount = ''.join(all_raw.split('</span>')[0] for all_raw in raw_html)
    try:
        return get_two_decimal_val(get_float_val(raw_amount) / 100)
    except Exception:
        return 0


def get_stock_details(url, sleep_timer=False):
    driver.get(url)
    if sleep_timer:
        sleep(5)
    name = driver.find_element(By.CLASS_NAME, "lpu38Head").text
    all_details = driver.find_element(By.CLASS_NAME, "ft785TableContainer").text
    current_price = get_current_stock_price()
    if not current_price:
        get_stock_details(url, True)
    individual_stock_details = {"Name": name,
                                "Current Price": current_price,
                                "Url": url
                                }
    for each in all_details.split('\n'):
        if 'Dividend' in each:
            dividend = get_float_val(each.split(" ")[-1][:-1])
            if dividend < 2:
                return
            individual_stock_details[' '.join(each.split(" ")[:-1])] = dividend
        elif 'ROE' in each:
            roe = get_float_val(each.split(" ")[-1][:-1])
            if roe < 2:
                return
            individual_stock_details[' '.join(each.split(" ")[:-1])] = roe
        elif 'Market' in each:
            individual_stock_details[' '.join(each.split(" ")[:-1])] = get_float_val(
                each.split(" ")[-1][1:-2].replace(',', ''))
        else:
            individual_stock_details[' '.join(each.split(" ")[:-1])] = get_float_val(each.split(" ")[-1])

    return individual_stock_details


def check_details():
    global driver
    try:
        options = Options()
        options.headless = True
        options.add_argument('--remote-debugging-port=61625')
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
        driver.get(filter_url)
        table = driver.find_element(By.CLASS_NAME, 'tb10Table')
        soup = BeautifulSoup(table.get_attribute('outerHTML'), "html.parser")
        table_data = list()
        eligible_stocks = list()
        for row in soup.find_all('tr'):
            urls = row.find_all('a')
            if urls:
                raw_link = str(urls[0]).split('href="')[1].split('" target')[0]
                link = f'https://groww.in{raw_link}'
                table_data.append(link)

        for each_stock_url in table_data:
            details = get_stock_details(each_stock_url)
            if details and details['ROE'] >= 10 and details['Dividend Yield'] >= 2:
                eligible_stocks.append(
                    {
                        "Name": details['Name'],
                        "Url": details['Url'],
                    }
                )

        print(json.dumps(sorted(eligible_stocks, key=lambda i: i['Url']), indent=2))
        print(len(eligible_stocks))
        if driver:
            driver.quit()
    except Exception as e:
        print(e)
        if driver:
            driver.quit()


check_details()
