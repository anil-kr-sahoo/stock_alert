import contextlib
import os
import json
import csv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from plyer import notification

options = Options()
options.headless = True
options.add_argument('--remote-debugging-port=61625')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)


def send_notifications(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=2
    )

    # For ubuntu, as it has not any sound on desktop notification
    # "sudo apt install sox"
    with contextlib.suppress(Exception):
        os.system('spd-say "hey, you got notification from stock alert" ')


def get_two_decimal_val(decimal_num):
    return float('%.2f' % decimal_num)


def get_float_val(string_num):
    try:
        return float(string_num)
    except Exception:
        return 0


def get_current_stock_price():
    raw_html = driver.find_element(By.CLASS_NAME, "lpu38Pri").get_attribute('innerHTML').split('hidden;">')[1:]
    raw_amount = ''.join(all_raw.split('</span>')[0] for all_raw in raw_html)
    try:
        return get_two_decimal_val(get_float_val(raw_amount) / 100)
    except Exception:
        return 0


def get_to_be_credit_dividend(stock_price, dividend_ratio):
    try:
        return get_two_decimal_val(get_float_val(stock_price) * get_float_val(dividend_ratio) / 100)
    except Exception as e:
        return 0


def get_stock_details(all_data):
    divident_ratio_percentage = 0
    url = all_data[0]
    stock_qty = all_data[1]
    driver.get(url)
    name = driver.find_element(By.CLASS_NAME, "lpu38Head").text
    current_price = get_current_stock_price()
    multiplier = 1
    check_negative_multiplier = driver.find_element(By.CLASS_NAME, "lpu38Day").text[0] == '-'
    if check_negative_multiplier:
        multiplier *= -1
    day_returns = get_float_val(
        driver.find_element(By.CLASS_NAME, "lpu38Day").text.split('(')[1].split(')')[0][:-1]) * multiplier
    all_details = driver.find_element(By.CLASS_NAME, "ft785TableContainer").text
    stock_details = {"Name": name, "Current Price": current_price, "Day Returns": day_returns}
    for each in all_details.split('\n'):
        if 'Dividend' in each or 'ROE' in each:
            if 'Dividend' in each:
                divident_ratio_percentage = get_float_val(each.split(" ")[-1][:-1])
            stock_details[(' ').join(each.split(" ")[:-1])] = get_float_val(each.split(" ")[-1][:-1])
        elif 'Market' in each:
            stock_details[(' ').join(each.split(" ")[:-1])] = get_float_val(each.split(" ")[-1][1:-2].replace(',', ''))
        else:
            stock_details[(' ').join(each.split(" ")[:-1])] = get_float_val(each.split(" ")[-1])
    stock_details["Credit Dividend"] = get_to_be_credit_dividend(current_price, divident_ratio_percentage)
    stock_details["To Be Credit Dividend"] = get_two_decimal_val(
        get_to_be_credit_dividend(current_price, divident_ratio_percentage) * stock_qty)
    stock_details["Qty"] = stock_qty

    print(json.dumps(stock_details, indent=2))
    send_notifications("Stok Details", str(stock_details))
    return stock_details


urls = [
    ['https://groww.in/stocks/equitas-small-finance-bank-ltd', 1],
    ['https://groww.in/stocks/dcb-bank-ltd', 1],
    ['https://groww.in/stocks/fertilisers-chemicals-travancore-ltd', 1],
    ['https://groww.in/stocks/canara-bank', 2],
    ['https://groww.in/stocks/itc-ltd', 2],
    ['https://groww.in/stocks/timken-india-ltd', 1],
    ['https://groww.in/stocks/idfc-ltd', 3],
    ['https://groww.in/stocks/yes-bank-ltd', 1],
    ['https://groww.in/stocks/divis-laboratories-ltd', 1],
    ['https://groww.in/stocks/uco-bank', 1],
    ['https://groww.in/stocks/jb-chemicals-pharmaceuticals-ltd', 1],
    ['https://groww.in/stocks/coal-india-ltd', 4],
    ['https://groww.in/stocks/oil-india-ltd', 3],
    ['https://groww.in/stocks/jsw-steel-ltd', 1],
    ['https://groww.in/stocks/shilpa-medicare-ltd', 2],
    ['https://groww.in/stocks/wipro-ltd', 3],
    ['https://groww.in/stocks/marico-ltd', 1],
    ['https://groww.in/stocks/marico-ltd', 3],
    ['https://groww.in/stocks/hindalco-industries-ltd', 1],
    ['https://groww.in/stocks/indian-overseas-bank', 1],
    ['https://groww.in/stocks/nmdc-ltd', 4],
    ['https://groww.in/stocks/zomato-ltd', 7],
    ['https://groww.in/stocks/bank-of-india', 2],
    ['https://groww.in/stocks/vedanta-ltd', 4],
    ['https://groww.in/stocks/adani-enterprises-ltd', 1],
    ['https://groww.in/stocks/bank-of-maharashtra', 1],
    ['https://groww.in/stocks/spicejet-ltd', 1],
    ['https://groww.in/stocks/delta-corp-ltd', 1],
    ['https://groww.in/stocks/indian-oil-corporation-ltd', 1],
    ['https://groww.in/stocks/ntpc-ltd', 3],
    ['https://groww.in/stocks/irb-infrastructure-developers-ltd', 1],
    ['https://groww.in/stocks/lodha-developers-ltd', 1],
    ['https://groww.in/stocks/rail-vikas-nigam-ltd', 1],
    ['https://groww.in/stocks/cg-power-industrial-solutions-ltd', 2],
    ['https://groww.in/stocks/power-grid-corporation-of-india-ltd', 1],
    ['https://groww.in/stocks/dlf-ltd', 1],
    ['https://groww.in/stocks/axis-bank-ltd', 1],
    ['https://groww.in/stocks/sun-pharma-advanced-research-company-ltd', 1],
    ['https://groww.in/stocks/bharti-airtel-ltd', 1],
    ['https://groww.in/stocks/schneider-electric-infrastructure-ltd', 1],
    ['https://groww.in/stocks/infosys-ltd', 1],
]
all_data = list()
for data in urls:
    driver.execute_script("window.open('about:blank', 'secondtab');")

    # It is switching to second tab now
    driver.switch_to.window("secondtab")
    all_data.append(get_stock_details(data))
driver.quit()

# Calculate total dividend to get from stocks
total = get_two_decimal_val(sum(data["To Be Credit Dividend"] for data in all_data))
print(f"Total evident to be credit is {total}/-")

with open("stock_data.json", "w") as twitter_data_file:
    json.dump(all_data, twitter_data_file, indent=4, sort_keys=True)


file = open('stock_details.csv', 'w')
writer = csv.writer(file)
heading = [list(all_data[0].keys())]
stock_details = [list(data.values()) for data in all_data]
writer.writerows(heading + stock_details)
file.close()
