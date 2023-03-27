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
# List details
# Grow url of stock, quantity you have, average price of your stocks
urls = [
    ['https://www.moneycontrol.com/india/stockpricequote/bank-private/equitassmallfinancebank/ESF', 1, 67.40],
    ['https://www.moneycontrol.com/india/stockpricequote/banks-private-sector/dcbbank/DCB01', 1, 119.95],
    ['https://www.moneycontrol.com/india/stockpricequote/fertilisers/fertiliserschemicalstravancore/FCT', 1, 237.25],
    ['https://www.moneycontrol.com/india/stockpricequote/banks-public-sector/canarabank/CB06', 2, 302.28],
    ['https://www.moneycontrol.com/india/stockpricequote/diversified/itc/ITC', 2, 354.43],
    ['https://www.moneycontrol.com/india/stockpricequote/bearings/timkenindia/TI23', 1, 3084.60],
    ['https://www.moneycontrol.com/india/stockpricequote/finance-term-lending-institutions/idfc/IDF', 3, 81.92],
    ['https://www.moneycontrol.com/india/stockpricequote/banks-private-sector/yesbank/YB', 1, 18],
    ['https://www.moneycontrol.com/india/stockpricequote/pharmaceuticals/divislaboratories/DL03', 1, 3425],
    ['https://www.moneycontrol.com/india/stockpricequote/banks-public-sector/ucobank/UCO', 1, 31],
    ['https://www.moneycontrol.com/india/stockpricequote/pharmaceuticals/jbchemicalspharmaceuticals/JBC01', 1, 1974.95],
    ['https://www.moneycontrol.com/india/stockpricequote/miningminerals/coalindia/CI11', 4, 204.74],
    ['https://www.moneycontrol.com/india/stockpricequote/oil-drillingexploration/oilindia/OI13', 3, 248.53, -3],
    ['https://www.moneycontrol.com/india/stockpricequote/steel-large/jswsteel/JSW01', 1, 749.65],
    ['https://www.moneycontrol.com/india/stockpricequote/pharmaceuticals/shilpamedicare/SM19', 2, 270.85],
    ['https://www.moneycontrol.com/india/stockpricequote/computers-software/wipro/W', 3, 605.28],
    ['https://www.moneycontrol.com/india/stockpricequote/personal-care/marico/M13', 1, 526.60],
    ['https://www.moneycontrol.com/india/stockpricequote/banks-public-sector/punjabnationalbank/PNB05', 3, 54.67],
    ['https://www.moneycontrol.com/india/stockpricequote/ironsteel/hindalcoindustries/HI', 1, 430.45],
    ['https://www.moneycontrol.com/india/stockpricequote/banks-public-sector/indianoverseasbank/IOB', 1, 31.40],
    ['https://www.moneycontrol.com/india/stockpricequote/miningminerals/nmdc/NMD02', 4, 114.81],
    ['https://www.moneycontrol.com/india/stockpricequote/online-services/zomato/Z', 7, 79.01],
    ['https://www.moneycontrol.com/india/stockpricequote/banks-public-sector/bankindia/BOI', 15, 72.12, -5],
    ['https://www.moneycontrol.com/india/stockpricequote/miningminerals/vedanta/SG', 4, 273],
    ['https://www.moneycontrol.com/india/stockpricequote/trading/adanienterprises/AE13', 1, 1945.90],
    ['https://www.moneycontrol.com/india/stockpricequote/banks-public-sector/bankmaharashtra/BM05', 3, 26.45, -3],
    ['https://www.moneycontrol.com/india/stockpricequote/transportlogistics/spicejet/SJ01', 1, 44.80],
    ['https://www.moneycontrol.com/india/stockpricequote/constructioncontracting-real-estate/deltacorp/DC11', 1,
     202.50],
    ['https://www.moneycontrol.com/india/stockpricequote/refineries/indianoilcorporation/IOC', 1, 81.75],
    ['https://www.moneycontrol.com/india/stockpricequote/power-generationdistribution/ntpc/NTP', 3, 168.22],
    ['https://www.moneycontrol.com/india/stockpricequote/infrastructure-general/irbinfrastructuredevelopers/IID01', 1,
     29.65],
    [
        'https://www.moneycontrol.com/india/stockpricequote/construction-residentialcommercial-complexes/macrotechdevelopers/MD03',
        1, 1001.40],
    ['https://www.moneycontrol.com/india/stockpricequote/miscellaneous/railvikasnigam/RVN', 1, 73.70],
    ['https://www.moneycontrol.com/india/stockpricequote/electric-equipment/cgpowerindustrialsolutions/CG', 2, 313.10],
    ['https://www.moneycontrol.com/india/stockpricequote/power-generationdistribution/powergridcorporationindia/PGC', 1,
     210],
    ['https://www.moneycontrol.com/india/stockpricequote/constructioncontracting-real-estate/dlf/D04', 1, 406],
    ['https://www.moneycontrol.com/india/stockpricequote/banks-private-sector/axisbank/AB16', 1, 880.50],
    ['https://www.moneycontrol.com/india/stockpricequote/pharmaceuticals/sunpharmaadvancedresearchcompany/SPA', 1,
     212.10],
    ['https://www.moneycontrol.com/india/stockpricequote/telecommunications-service/bhartiairtel/BA08', 1, 815],
    [
        'https://www.moneycontrol.com/india/stockpricequote/power-generationdistribution/schneiderelectricinfrastructure/SEI04',
        1, 193.95],
    ['https://www.moneycontrol.com/india/stockpricequote/computers-software/infosys/IT', 1, 1542.65],
    ['https://www.moneycontrol.com/india/stockpricequote/auto-23-wheelers/bajajauto/BA10', 0, 0],
    ['https://www.moneycontrol.com/india/stockpricequote/oil-drillingexploration/oilnaturalgascorporation/ONG', 0, 0],
    ['https://www.moneycontrol.com/india/stockpricequote/computers-software/hcltechnologies/HCL02', 0, 0],
    ['https://www.moneycontrol.com/india/stockpricequote/ironsteel/tatasteel/TIS', 0, 0],
    ['https://www.moneycontrol.com/india/stockpricequote/refineries/bharatpetroleumcorporation/BPC', 0, 0],
    ['https://www.moneycontrol.com/india/stockpricequote/auto-23-wheelers/heromotocorp/HHM', 0, 0],
    ['https://www.moneycontrol.com/india/stockpricequote/personal-care/colgatepalmoliveindia/CPI', 0, 0],
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
    driver.get(url)
    name = driver.find_element(By.ID, 'stockName').text.split('\n')[0]
    try:
        lowest_day_limit = all_data[3]
        print(f"Manually limit provided on {name}")
    except Exception as e:
        lowest_day_limit = -2
    current_price = get_float_val(
        driver.find_element(By.ID, 'nsecp').get_attribute('data-numberanimate-value').replace(',', ''))
    day_returns = get_float_val(driver.find_element(By.ID, 'nsechange').text.split('(')[1].split(')')[0][:-1])
    all_details_list = driver.find_element(By.ID, 'stk_overview').text.split('\n')
    roe = get_float_val(driver.find_element(By.CLASS_NAME, 'peer_tbl').text.split('\n')[1].split(' ')[6])
    individual_stock_details = {"Time": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), "Name": name,
                                "Current Price": current_price,
                                "Day Returns": day_returns,
                                "Stock Average Value": stock_average_val,
                                "ROE": roe}
    for each in all_details_list:
        if 'Mkt Cap' in each:
            individual_stock_details["Market Cap"] = get_float_val(each.split(' ')[-1].replace(',', ''))
        if 'Dividend Yield' in each:
            dividend_ratio_percentage = get_float_val(each.split(' ')[-1])
            individual_stock_details["Dividend Yield"] = dividend_ratio_percentage

    individual_stock_details["Credit Dividend"] = get_to_be_credit_dividend(current_price, dividend_ratio_percentage)
    individual_stock_details["To Be Credit Dividend"] = get_two_decimal_val(
        get_to_be_credit_dividend(current_price, dividend_ratio_percentage) * stock_qty)
    individual_stock_details["Qty"] = stock_qty
    notify_details_1 = f"Name : {name}\nCurrent Price : {current_price}\n"
    notify_details_2 = f"Day Returns : {day_returns}\nDividend : {dividend_ratio_percentage}\n" \
                       f"Current Stock QTY : {stock_qty}"
    if stock_qty:
        notify_details = f"{notify_details_1}Average Value : {stock_average_val}\n{notify_details_2}"
    else:
        notify_details = notify_details_1 + notify_details_2
    if day_returns <= lowest_day_limit and dividend_ratio_percentage > 2:
        global_notifier(
            "Buy Stocks",
            notify_details,
            buy_stock_list,
            individual_stock_details,
        )
    if stock_qty and target_stock_val < current_price and dividend_ratio_percentage < 2:
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


sleep_time = 120

while True:
    all_stocks_data = []

    options = Options()
    options.headless = True
    options.add_argument("window-size=1400,600")
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
                driver.find_element(By.ID, "qtip-5-content").get_attribute('innerHTML').split('<b>')[1].split('</b>')[
                    0][:-1]
            print(battery_level)
            with contextlib.suppress(Exception):
                if int(battery_level) <= 15:
                    send_notifications(title=f"{battery_level}% Battery Left",
                                       message="Wifi modem is going to be shut down soon\nPlease plug in charger")
    driver.quit()

    # Calculate total dividend to get from stocks
    total = get_two_decimal_val(sum(data["To Be Credit Dividend"] for data in all_stocks_data))
    print(f"Total dividend to be credit is {total}/-")

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
        break

    sleep(sleep_time)
