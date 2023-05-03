import contextlib
import os
import json
import csv
import platform
from datetime import datetime
from time import sleep

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from plyer import notification

# Use Airtel Wi-Fi battery indicator as well
USE_WIFI_INDICATOR = True
modem_url = "http://192.168.1.1/index.html"
buy_stock_list = []
sell_stock_list = []
unaffordable_stocks = []
# List details
# [Grow url of stock, quantity you have, average price of your stocks, max threshold %]
urls = [
    ['https://groww.in/stocks/adani-enterprises-ltd', 1, 1945.9],
    ['https://groww.in/stocks/axis-bank-ltd', 1, 880.5],
    ['https://groww.in/stocks/bajaj-auto-ltd', 0, 0],
    ['https://groww.in/stocks/bharat-petroleum-corporation-ltd', 7, 332.96],
    ['https://groww.in/stocks/bharti-airtel-ltd', 1, 815],
    ['https://groww.in/stocks/britannia-industries-ltd', 0, 0],
    ['https://groww.in/stocks/canara-bank', 2, 302.28],
    ['https://groww.in/stocks/cg-power-industrial-solutions-ltd', 2, 313.1],
    ['https://groww.in/stocks/coal-india-ltd', 4, 204.74],
    ['https://groww.in/stocks/colgatepalmolive-india-ltd', 0, 0],
    ['https://groww.in/stocks/dcb-bank-ltd', 1, 119.95],
    ['https://groww.in/stocks/delta-corp-ltd', 1, 202.5],
    ['https://groww.in/stocks/divis-laboratories-ltd', 1, 3425],
    ['https://groww.in/stocks/dlf-ltd', 1, 406],
    ['https://groww.in/stocks/equitas-small-finance-bank-ltd', 1, 67.4],
    ['https://groww.in/stocks/hcl-technologies-ltd', 3, 1070.93],
    ['https://groww.in/stocks/hdfc-asset-management-company-ltd', 0, 0],
    ['https://groww.in/stocks/hindustan-zinc-ltd', 0, 0],
    ['https://groww.in/stocks/hero-motocorp-ltd', 3, 2338.31],
    ['https://groww.in/stocks/hindalco-industries-ltd', 1, 430.45],
    ['https://groww.in/stocks/hindustan-petroleum-corporation-ltd', 6, 227.30],
    ['https://groww.in/stocks/indian-oil-corporation-ltd', 1, 81.75],
    ['https://groww.in/stocks/indian-overseas-bank', 1, 31.4],
    ['https://groww.in/stocks/infosys-ltd', 2, 1384.32],
    ['https://groww.in/stocks/irb-infrastructure-developers-ltd', 1, 29.65],
    ['https://groww.in/stocks/itc-ltd', 2, 354.43],
    ['https://groww.in/stocks/jsw-steel-ltd', 1, 749.65],
    ['https://groww.in/stocks/lodha-developers-ltd', 1, 1001.4],
    ['https://groww.in/stocks/marico-ltd', 1, 526.6],
    ['https://groww.in/stocks/nhpc-ltd', 7, 40.89],
    ['https://groww.in/stocks/nmdc-ltd', 5, 113.66],
    ['https://groww.in/stocks/ntpc-ltd', 5, 168.77],
    ['https://groww.in/stocks/oil-india-ltd', 15, 252.53],
    ['https://groww.in/stocks/oil-natural-gas-corporation-ltd', 2, 147.3],
    ['https://groww.in/stocks/oracle-financial-services-software-ltd', 0, 0],
    ['https://groww.in/stocks/power-finance-corporation-ltd', 4, 161.55],
    ['https://groww.in/stocks/power-grid-corporation-of-india-ltd', 3, 224.03],
    ['https://groww.in/stocks/punjab-national-bank', 3, 54.67],
    ['https://groww.in/stocks/schneider-electric-infrastructure-ltd', 1, 193.95],
    ['https://groww.in/stocks/shilpa-medicare-ltd', 2, 270.85],
    ['https://groww.in/stocks/shriram-transport-finance-company-ltd', 0, 0],
    ['https://groww.in/stocks/spicejet-ltd', 1, 44.8],
    ['https://groww.in/stocks/sun-pharma-advanced-research-company-ltd', 1, 212.1],
    ['https://groww.in/stocks/tata-steel-ltd', 0, 0],
    ['https://groww.in/stocks/timken-india-ltd', 1, 3084.6],
    ['https://groww.in/stocks/uco-bank', 1, 31.5],
    ['https://groww.in/stocks/vedanta-ltd', 4, 274.05],
    ['https://groww.in/stocks/wipro-ltd', 3, 605.28],
    ['https://groww.in/stocks/yes-bank-ltd', 1, 18],
    ['https://groww.in/stocks/zomato-ltd', 7, 79.01],
]


def send_notifications(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=2
    )
    if platform.system() == "Linux":
        # For ubuntu, as it has not any sound on desktop notification
        # "sudo apt install sox"
        with contextlib.suppress(Exception):
            if 'Buy' in title:
                os.system('spd-say "Hi Sir, A stock is ready to Buy" ')
            elif 'Sell' in title:
                os.system('spd-say "Hi Sir, A stock is ready to Sell" ')
            elif 'over' in title:
                os.system('spd-say "Hi Sir, Trading over for today, please run wi-fi battery checker" ')
            elif 'Restart' in title:
                os.system('spd-say "Hi Sir, Please restart server, its crashed due to low internet" ')
            else:
                os.system('spd-say "Hi Sir, Your wifi battery is low, Please plug in Charger" ')


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
    global buy_stock_list, sell_stock_list
    url = all_data[0]
    stock_qty = all_data[1]
    stock_average_val = all_data[2]

    target_stock_val = stock_average_val + stock_average_val * .1
    dividend_ratio_percentage = 0
    roe = 0
    driver.get(url)
    if (
            datetime.now().hour >= 15 and datetime.now().minute > 20) or datetime.now().hour > 15 or datetime.now().weekday() > 4:
        sleep(5)
    name = driver.find_element(By.CLASS_NAME, "lpu38Head").text
    current_price = get_current_stock_price()
    multiplier = 1
    check_negative_multiplier = driver.find_element(By.CLASS_NAME, "lpu38Day").text[0] == '-'
    if check_negative_multiplier:
        multiplier *= -1
    try:
        lowest_day_limit = all_data[3]
        print(f"Manually limit provided on -------- {name}")
    except Exception as e:
        lowest_day_limit = -2
    day_returns = get_float_val(
        driver.find_element(By.CLASS_NAME, "lpu38Day").text.split('(')[1].split(')')[0][:-1]) * multiplier
    all_details = driver.find_element(By.CLASS_NAME, "ft785TableContainer").text
    individual_stock_details = {"Time": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), "Name": name,
                                "Stock Average Value": stock_average_val,
                                "Day Returns": day_returns,
                                "Current Price": current_price
                                }
    for each in all_details.split('\n'):
        if 'Dividend' in each:
            dividend_ratio_percentage = get_float_val(each.split(" ")[-1][:-1])
            individual_stock_details[' '.join(each.split(" ")[:-1])] = get_float_val(each.split(" ")[-1][:-1])
        elif 'ROE' in each:
            roe = get_float_val(each.split(" ")[-1][:-1])
            individual_stock_details[' '.join(each.split(" ")[:-1])] = roe
        elif 'Market' in each:
            individual_stock_details[' '.join(each.split(" ")[:-1])] = get_float_val(
                each.split(" ")[-1][1:-2].replace(',', ''))
        else:
            individual_stock_details[' '.join(each.split(" ")[:-1])] = get_float_val(each.split(" ")[-1])
    individual_stock_details["Credit Dividend"] = get_to_be_credit_dividend(current_price, dividend_ratio_percentage)
    individual_stock_details["To Be Credit Dividend"] = get_two_decimal_val(
        get_to_be_credit_dividend(current_price, dividend_ratio_percentage) * stock_qty)
    individual_stock_details["Qty"] = stock_qty
    individual_stock_details["Total Returns"] = (current_price - stock_average_val) * stock_qty
    notify_details_1 = f"Name : {name}\nCurrent Price : {current_price}\n"
    notify_details_2 = f"Day Returns : {day_returns}\nDividend : {dividend_ratio_percentage}\n" \
                       f"Current Stock QTY : {stock_qty}"
    if stock_qty:
        notify_details = f"{notify_details_1}Average Value : {stock_average_val}\n{notify_details_2}"
    else:
        notify_details = notify_details_1 + notify_details_2
    if (
            current_price != 0
            and day_returns != -100
            and day_returns <= lowest_day_limit
            and roe >= 10
            and all(key not in url for key in unaffordable_stocks)
            and dividend_ratio_percentage >= 2
    ):
        global_notifier(
            "Buy Stocks",
            notify_details,
            buy_stock_list,
            individual_stock_details,
        )
    if (
            stock_qty
            and target_stock_val < current_price
            and (dividend_ratio_percentage < 2 or roe < 10)
    ):
        global_notifier(
            "Sell Stocks",
            notify_details,
            sell_stock_list,
            individual_stock_details,
        )
    return individual_stock_details


def global_notifier(notification_title, notify_details, stock_list_type, individual_stock_details):
    send_notifications(notification_title, notify_details)
    stock_list_type.append(individual_stock_details)
    print(json.dumps(individual_stock_details, indent=2))


def generate_files(file_name, file_data):
    with open(f"{file_name}.json", "w") as stock_data:
        json.dump(file_data, stock_data, indent=4, sort_keys=True)

    with open(f'{file_name}.csv', 'w') as file:
        writer = csv.writer(file)
        heading = [list(file_data[0].keys())]
        stock_details = [list(element.values()) for element in file_data]
        writer.writerows(heading + stock_details)


driver = None
try:
    sleep_time = 120

    while True:
        all_stocks_data = []

        options = Options()
        options.headless = True
        options.add_argument('--remote-debugging-port=61625')
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
        for data in urls:
            driver.execute_script("window.open('about:blank', 'secondtab');")

            # It is switching to second tab now
            driver.switch_to.window("secondtab")
            all_stocks_data.append(get_stock_details(data))

        if USE_WIFI_INDICATOR:
            with contextlib.suppress(Exception):
                # Get airtel wi-fi modem battery health
                # ------------------------------------------------------------------------------------------------------------------
                driver.execute_script("window.open('about:blank', 'secondtab');")
                driver.switch_to.window("secondtab")
                driver.get(modem_url)
                battery_level = \
                    driver.find_element(By.ID, "qtip-5-content").get_attribute('innerHTML').split('<b>')[1].split(
                        '</b>')[
                        0][:-1]
                print(battery_level)
                with contextlib.suppress(Exception):
                    if int(battery_level) <= 15:
                        send_notifications(title=f"{battery_level}% Battery Left",
                                           message="Wifi modem is going to be shut down soon\nPlease plug in charger")
        driver.quit()

        # Calculate total dividend to get from stocks
        total_dividend = get_two_decimal_val(sum(data["To Be Credit Dividend"] for data in all_stocks_data))
        print(f"Total dividend to be credit is {total_dividend}/-")
        total = get_two_decimal_val(sum(data["Total Returns"] for data in all_stocks_data))
        print(f"Total returns is {total}/-")

        if buy_stock_list:
            file = 'buy_stock_details'
            data = buy_stock_list
            generate_files(file, data)
        if sell_stock_list:
            file = 'sell_stock_details'
            data = sell_stock_list
            generate_files(file, data)
        if (
                datetime.now().hour >= 15 and datetime.now().minute > 20) or datetime.now().hour > 15 or datetime.now().weekday() > 4:
            file = 'stock_data'
            data = all_stocks_data
            generate_files(file, data)
            send_notifications(title="Today's trade over",
                               message="Please run wifi battery checker")

            break

        sleep(sleep_time)
except Exception as e:
    send_notifications(title="Restart Server", message="Server crashed due low internet connection")
    if driver:
        driver.quit()
        driver.close()
