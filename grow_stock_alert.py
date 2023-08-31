import contextlib
import os
import json
import csv
import pywhatkit
import platform
import socket

from datetime import datetime
from time import sleep

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from plyer import notification

# Use Airtel Wi-Fi battery indicator as well
USE_WIFI_INDICATOR = True
system_name = socket.gethostname()
modem_url = "http://192.168.1.1/index.html"

# 10% minimum profit added
required_min_percentage = .1
buy_stock_list = []
sell_stock_list = []
start_time = datetime.now()
# List details
# [Grow url of stock, quantity you have, average price of your stocks, max threshold %]
urls = [
    ['https://groww.in/stocks/bajaj-auto-ltd', 1, 4720.20],
    ['https://groww.in/stocks/bank-of-baroda', 11, 195.01],
    ['https://groww.in/stocks/bosch-ltd', 0, 0],
    ['https://groww.in/stocks/britannia-industries-ltd', 3, 4813.13],
    ['https://groww.in/stocks/canara-bank', 12, 309.88],
    ['https://groww.in/stocks/coal-india-ltd', 11, 221.22],
    ['https://groww.in/stocks/colgatepalmolive-india-ltd', 0, 0],
    ['https://groww.in/stocks/general-insurance-corporation-of-india-ltd', 3, 199.43],
    ['https://groww.in/stocks/hcl-technologies-ltd', 9, 1093.63],
    ['https://groww.in/stocks/hero-motocorp-ltd', 9, 2815.93],
    ['https://groww.in/stocks/hindalco-industries-ltd', 1, 430.45],
    ['https://groww.in/stocks/hindustan-zinc-ltd', 5, 324.93],
    ['https://groww.in/stocks/infosys-ltd', 7, 1365.07],
    ['https://groww.in/stocks/itc-ltd', 7, 418.33],
    ['https://groww.in/stocks/nmdc-ltd', 7, 113.22],
    ['https://groww.in/stocks/oil-india-ltd', 21, 256.97],
    ['https://groww.in/stocks/oil-natural-gas-corporation-ltd', 7, 154.79],
    ['https://groww.in/stocks/oracle-financial-services-software-ltd', 0, 0],
    ['https://groww.in/stocks/piramal-enterprises-ltd', 13, 1004.86],
    ['https://groww.in/stocks/power-grid-corporation-of-india-ltd', 22, 243.85],
    ['https://groww.in/stocks/tata-consultancy-services-ltd', 0, 0],
    ['https://groww.in/stocks/tech-mahindra-ltd', 9, 1083.39],
    ['https://groww.in/stocks/vedanta-ltd', 15, 268.96],
    ['https://groww.in/stocks/wipro-ltd', 3, 605.28],
]


def send_whatsapp_notification(message):
    if any(data in message for data in ['Buy', 'Sell', 'Thank']):
        pywhatkit.sendwhatmsg_to_group_instantly(group_id="KbFKSNqUkWs8RGVhiPpw4U", message=message, tab_close=True)
    else:
        pywhatkit.sendwhatmsg_instantly(phone_no="+917749984274", message=message, tab_close=True)


def send_notifications(title, message, wp_message=None):
    if system_name in ["anil-ubuntu"]:
        if wp_message:
            send_whatsapp_notification(wp_message)
        else:
            send_whatsapp_notification(title)

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
    except Exception:
        return 0


def get_stock_details(all_data):
    global buy_stock_list, sell_stock_list
    url = all_data[0]
    stock_qty = all_data[1]
    stock_average_val = all_data[2]
    target_stock_val = stock_average_val + stock_average_val * required_min_percentage
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
    individual_stock_details = {"Time": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                                "Name": name,
                                "Stock Average Value": stock_average_val,
                                "Day Returns": day_returns,
                                "Current Price": current_price,
                                "Url": url
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
            and dividend_ratio_percentage >= 2
    ):
        global_notifier(
            f"Buy {round(day_returns * -1)} Stocks",
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
            "Sell All Stocks",
            notify_details,
            sell_stock_list,
            individual_stock_details,
        )
    return individual_stock_details


def global_notifier(notification_title, notify_details, stock_list_type, individual_stock_details):
    if 'Sell' in notification_title:
        least_sell_amount = get_two_decimal_val(individual_stock_details['Current Price'] - individual_stock_details[
            'Current Price'] * required_min_percentage)
        whatsapp_message = f"{notification_title} of {individual_stock_details['Name']}\n{individual_stock_details['Url']}\n" \
                           f"If the purchased amount is less than {least_sell_amount}/-"
    else:
        whatsapp_message = f"{notification_title} of {individual_stock_details['Name']}\n" \
                           f"{individual_stock_details['Url']}\n" \
                           f"Day Returns {individual_stock_details['Day Returns']}\n" \
                           f"Current Value for a single stock is {individual_stock_details['Current Price']}/-"
    send_notifications(notification_title, notify_details, whatsapp_message)
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
    while True:
        all_stocks_data = []

        options = Options()
        options.headless = True
        options.add_argument('--remote-debugging-port=61625')
        options.add_argument('--no-sandbox')
        try:
            driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
        except Exception:
            driver = webdriver.Chrome(executable_path=ChromeDriverManager(version="114.0.5735.90").install(),
                                      options=options)
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
                        send_notifications(title=f"Wifi running low, {battery_level}% Battery Left",
                                           message="Wifi modem is going to be shut down soon\nPlease plug in charger")
        driver.quit()

        # Calculate total dividend to get from stocks
        total_units = get_two_decimal_val(sum(data["Qty"] for data in all_stocks_data))
        print(f"{int(total_units)} units purchased till now.")
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
            send_notifications(title="Thank you for trade with AK. \nToday's trade is over",
                               message="Please run wifi battery checker")

            break

except Exception as e:
    title = "Restart Server\n"
    hour = int((datetime.now() - start_time).seconds / 60 / 60)
    minute = int((datetime.now() - start_time).seconds / 60) % 60
    seconds = int((datetime.now() - start_time).seconds % 60)
    title += f"Server ran for {hour} hour{'s' if hour > 1 else ''}," \
             f" {minute} minute{'s' if minute > 1 else ''}," \
             f" {seconds} second{'s' if seconds > 1 else ''}"

    send_notifications(title=title, message="Server crashed due low internet connection")
    if driver:
        driver.quit()
        driver.close()
