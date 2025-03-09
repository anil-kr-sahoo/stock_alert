import json
from tqdm import tqdm
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from user_stocks_input_file import user_stocks

filter_url = "https://groww.in/stocks/filter?closePriceHigh=100000&closePriceLow=0&index=Nifty%20100,Nifty%2050,BSE%20100&marketCapHigh=2000000&marketCapLow=0&page=0&size=1000&sortType=ASC"
driver = None


def get_float_val(string_num):
    try:
        return float(string_num)
    except Exception:
        return 0


def get_two_decimal_val(decimal_num):
    return float('%.2f' % decimal_num)


def get_current_stock_price():
    try:
        raw_html = driver.find_element(By.CLASS_NAME, "lpu38Pri").get_attribute('innerHTML').split('">')[-1]
        raw_amount = raw_html.split('</span>')[0]
        return get_two_decimal_val(get_float_val(raw_amount) / 100)
    except Exception:
        return 0


def check_stocks_eligibility(sort_listed_stocks):
    risky_urls = list()
    all_urls = list()
    for k, v in user_stocks.items():
        all_urls += [data[0] for data in v]
        stock_urls = [data[0] for data in v if not data[1] and not data[2]]
        risky_urls += stock_urls
    stock_details = {
        "Add Stocks": [
            url for url in sort_listed_stocks if url not in all_urls
        ],
        "Remove Stocks": [
            url for url in risky_urls if url not in sort_listed_stocks
        ],
    }
    return stock_details


def get_stock_details(url, sleep_timer=False):
    try:
        driver.get(url)
        if sleep_timer:
            sleep(5)
        try:
            name = driver.find_element(By.CLASS_NAME, "lpu38Head").text
            if not name:
                return get_stock_details(url, sleep_timer=True)
        except Exception as e:
            return get_stock_details(url, sleep_timer=True)
        all_details = driver.find_element(By.CLASS_NAME, "ft785TableContainer").text
        individual_stock_details = {"Name": name,
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
                if roe < 15:
                    return
                individual_stock_details[' '.join(each.split(" ")[:-1])] = roe
            elif 'Debt to Equity' in each:
                debt_to_equity = get_float_val(each.split(" ")[-1])
                if debt_to_equity > 1:
                    return
                individual_stock_details[' '.join(each.split(" ")[:-1])] = debt_to_equity
            elif 'Market' in each:
                individual_stock_details[' '.join(each.split(" ")[:-1])] = get_float_val(
                    each.split(" ")[-1][1:-2].replace(',', ''))
            else:
                individual_stock_details[' '.join(each.split(" ")[:-1])] = get_float_val(each.split(" ")[-1])

        return individual_stock_details
    except Exception as e:
        print(e)
        print(f"\nProblem in fetching details{'-' * 20}{url}")
        return


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

        for each_stock_url in tqdm(table_data, desc="Stock Scanned", unit='stocks'):
            details = get_stock_details(each_stock_url)
            if details and details['ROE'] >= 10 and details['Dividend Yield'] >= 2:
                eligible_stocks.append(
                    {
                        "Name": details['Name'],
                        "Url": details['Url'],
                    }
                )
        # print(json.dumps(sorted(eligible_stocks, key=lambda i: i['Url']), indent=2))
        print("Total Eligible Stocks - ", len(eligible_stocks))
        print("Total Eligible Stocks - ", '\n'.join([data['Url'] for data in eligible_stocks]))
        stock_details = check_stocks_eligibility([data['Url'] for data in eligible_stocks])
        print(json.dumps(stock_details, indent=2))
        if driver:
            driver.quit()
    except Exception as e:
        print(e)
        if driver:
            driver.quit()


check_details()
