import contextlib
import json
import time
import traceback
from datetime import datetime
from time import sleep

from selenium.common import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service
from tqdm import tqdm

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from user_stocks_input_file import user_stocks, GROUP_LIST, PHONE_NO_LIST, THANK_YOU_MESSAGE, ALLOW_NOTIFICATION, \
    ALLOWED_DEVICE_ACCESS, NOTIFIED_SELL_STOCK_URLS
from utils import *

# Use Airtel Wi-Fi battery indicator as well
USE_WIFI_INDICATOR = False
modem_url = "http://192.168.1.1/index.html"

# 10% minimum profit added
required_min_percentage = .13
urls = list()

# print(sorted(set([data[0] for data in urls])))
buy_stock_list = list()
sell_stock_list = list()
notified_stock_list = NOTIFIED_SELL_STOCK_URLS
in_memory_data = dict()
message_summary = dict()
start_time = datetime.now()


def get_current_stock_price():
    """
    This helper function used to get realtime current data from Groww
    :return:
    """
    try:
        raw_html = driver.find_element(By.CLASS_NAME, "lpu38Pri").get_attribute('innerHTML').split('">')[-1]
        raw_amount = raw_html.split('</span>')[0]
        return get_two_decimal_val(get_float_val(raw_amount))
    except Exception:
        return 0


def get_current_stock_data(source_url):
    """
    This helper function used to get realtime current data from Google finance
    :param source_url:
    :return:
    """
    try:
        mapping_stocks = json.load(open('stocks_mapping.json'))
        destination_url = mapping_stocks[source_url]
        driver.get(destination_url)
        all_data = driver.find_element(By.CLASS_NAME, "rPF6Lc").text.split('\n')
        price = get_float_val(all_data[0][1:].replace(',', ''))
        day_returns = get_float_val(all_data[1][:-1]) * -1 if all_data[2][0] == "-" else get_float_val(all_data[1][:-1])
        driver.execute_script("window.open('about:blank', 'secondtab');")
        driver.switch_to.window("secondtab")
        return price, day_returns
    except Exception as e:
        print("Error - ", e)
        driver.execute_script("window.open('about:blank', 'secondtab');")
        driver.switch_to.window("secondtab")
        return 0, 0


def get_stock_details(all_data, set_timer=False):
    global buy_stock_list, sell_stock_list, in_memory_data, notified_stock_list
    url = all_data[0]
    stock_qty = all_data[1]
    stock_average_val = all_data[2]
    target_stock_val = stock_average_val + stock_average_val * required_min_percentage
    dividend_ratio_percentage = 0
    upcoming_dividend_amount = 0
    upcoming_dividend_date = ''
    roe = 0
    debt_to_equity = 0
    current_price, day_returns = get_current_stock_data(url)
    driver.get(url)
    if set_timer: sleep(5)
    try:
        name = driver.find_element(By.CLASS_NAME, "lpu38Head").text
        if not name:
            return get_stock_details(all_data, set_timer=True)
    except Exception as e:
        return get_stock_details(all_data, set_timer=True)

    # current_price = get_current_stock_price()
    # if not current_price:
    #     return get_stock_details(all_data, set_timer=True)
    # name = driver.find_element(By.CLASS_NAME, "lpu38Head").text
    # check_negative_multiplier = driver.find_element(By.CLASS_NAME, "lpu38Day").text[0] == '-'
    # multiplier = 1
    # if check_negative_multiplier:
    #     multiplier *= -1
    # day_returns = get_float_val(
    #     driver.find_element(By.CLASS_NAME, "lpu38Day").text.split('(')[1].split(')')[0][:-1]) * multiplier

    if not in_memory_data.get(all_data[0]):
        try:
            in_memory_data[all_data[0]] = all_data[3]
            buy_stock_list = json.load(open('buy_stock_details.json'))
            if url not in notified_stock_list:
                notified_stock_list.append(url)
        except Exception:
            least_day_return = round(day_returns)
            if least_day_return >= -2 or url not in notified_stock_list:
                in_memory_data[all_data[0]] = -2
            else:
                in_memory_data[all_data[0]] = least_day_return

    lowest_day_limit = in_memory_data[all_data[0]]
    if lowest_day_limit != -2:
        print(f"\nManually limit provided on -------- {name} With value {lowest_day_limit}")

    all_details = driver.find_element(By.CLASS_NAME, "ft785TableContainer").text

    try:
        # Check future dividends
        dividend_message = ''
        driver.find_element(By.CLASS_NAME, "tabs8Parent").find_elements(By.XPATH, "./*")[2].click()
        sleep(.5)
        dividend_data = driver.find_element(By.CLASS_NAME, "corporateActions_container__UKS5a").text.split('\n')
        if 'loading' in dividend_data[0].lower():
            sleep(10)
            dividend_data = driver.find_element(By.CLASS_NAME, "corporateActions_container__UKS5a").text.split('\n')
        upcoming_dividend_date = ''
        upcoming_future_insights_list = ["Upcoming", "Today"]
        for index, stock_insight in enumerate(dividend_data):
            if stock_insight in upcoming_future_insights_list:
                if dividend_data[index - 1].strip() == "Dividend" and dividend_data[index].strip() in upcoming_future_insights_list and dividend_data[index + 1].strip() == "Ex date":
                    dividend_date = datetime.strptime(f"{dividend_data[0]}-{dividend_data[1]}-{dividend_data[2]}", "%Y-%d-%b").date()
                    current_date = datetime.today().date()
                    if dividend_date >= current_date:
                        upcoming_dividend_amount = 0
                        for index, event_data in enumerate(dividend_data):
                            if event_data.strip() in upcoming_future_insights_list and dividend_data[index + 1].strip() == 'Ex date':
                                if dividend_date == current_date:
                                    upcoming_dividend_amount += get_two_decimal_val(get_float_val(dividend_data[index + 2].strip()[1:]))
                                else:
                                    upcoming_dividend_amount = get_two_decimal_val(get_float_val(dividend_data[index + 2].strip()[1:]))
                                upcoming_dividend_date = f"{dividend_data[index - 3].strip() if len(dividend_data[index - 3].strip()) == 2 else '0' + dividend_data[index - 3].strip()} {dividend_data[index - 2].strip()}, {dividend_data[0].strip()}"
                        if not upcoming_dividend_date:
                            upcoming_dividend_date = f"{dividend_data[1].strip()} {dividend_data[2].strip()}, {dividend_data[0].strip()}"
                        if dividend_data[4].strip() == upcoming_future_insights_list[0]:
                            dividend_message = f"*Rs {upcoming_dividend_amount}/- dividend per share declared by {upcoming_dividend_date}*\n"
                            print("\n", dividend_message, name)
    except Exception:
        pass

    individual_stock_details = {"Time": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                                "Name": name,
                                "Stock Average Value": stock_average_val,
                                "Day Returns": day_returns,
                                "Current Price": current_price,
                                "Url": url,
                                "Upcoming Dividend Amount": upcoming_dividend_amount,
                                "Upcoming Dividend Date": upcoming_dividend_date
                                }
    for each in all_details.split('\n'):
        if 'Dividend' in each:
            dividend_ratio_percentage = get_float_val(each.split(" ")[-1][:-1])
            individual_stock_details[' '.join(each.split(" ")[:-1])] = get_float_val(each.split(" ")[-1][:-1])
        elif 'ROE' in each:
            roe = get_float_val(each.split(" ")[-1][:-1])
            individual_stock_details[' '.join(each.split(" ")[:-1])] = roe
        elif 'Debt to Equity' in each:
            debt_to_equity = get_float_val(each.split(" ")[-1])
            individual_stock_details[' '.join(each.split(" ")[:-1])] = debt_to_equity
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
    notify_details_2 = f"Day Returns : {day_returns}%\nDividend : {dividend_ratio_percentage}\n" \
                       f"Current Stock QTY : {stock_qty}"
    if stock_qty:
        notify_details = f"{notify_details_1}Average Value : {stock_average_val}\n{notify_details_2}"
    else:
        notify_details = notify_details_1 + notify_details_2
    if (
            current_price != 0
            and day_returns != -100
            and day_returns < lowest_day_limit
            and roe >= 15
            and dividend_ratio_percentage >= 2
            and debt_to_equity <= 1
    ):
        in_memory_data[all_data[0]] = int(day_returns) - 1

        if url not in notified_stock_list:
            notified_stock_list.append(url)
            buy_message = f"{dividend_message}Buy {round(day_returns * -1)} Stocks"
            individual_stock_details["Buy Units"] = round(day_returns * -1)
        else:
            buy_message = f"{dividend_message}Buy {int((day_returns - lowest_day_limit - 1) * -1)} more Stocks"
            individual_stock_details["Buy Units"] = int((day_returns - lowest_day_limit - 1) * -1)

        global_notifier(
            buy_message,
            notify_details,
            buy_stock_list,
            individual_stock_details,
        )
    if (
            target_stock_val
            and target_stock_val < current_price
            and (dividend_ratio_percentage < 2 or roe < 15 or debt_to_equity > 1)
            and url not in notified_stock_list
            and not upcoming_dividend_amount
    ):
        notified_stock_list.append(url)
        global_notifier(
            "Sell All Stocks",
            notify_details,
            sell_stock_list,
            individual_stock_details,
        )
    return individual_stock_details


def global_notifier(notification_title, notify_details, notified_buy_stock_list, individual_stock_details):
    """
    This function helps to generate realtime messages to send in notification
    :param notification_title:
    :param notify_details:
    :param notified_buy_stock_list:
    :param individual_stock_details:
    :return:
    """
    if 'Sell' in notification_title:
        least_sell_amount = get_two_decimal_val(individual_stock_details['Current Price'] / (1 + (required_min_percentage * 100) / 100))
        whatsapp_message = f"{notification_title} of {individual_stock_details['Name']}\n{individual_stock_details['Url']}\n" \
                           f"If the average amount is less than {least_sell_amount}/-"
    else:
        whatsapp_message = f"{notification_title} of {individual_stock_details['Name']}\n" \
                           f"{individual_stock_details['Url']}\n" \
                           f"Day Returns {individual_stock_details['Day Returns']}%\n" \
                           f"Current Value for a single stock is {individual_stock_details['Current Price']}/-"
    if ALLOW_NOTIFICATION:
        send_notifications(notification_title, notify_details, whatsapp_message)
    notified_buy_stock_list.append(individual_stock_details)
    print(json.dumps(individual_stock_details, indent=2))


driver = None
retries = 200
try:
    while retries > 0:
        try:
            all_stocks_data = []
            portfolio_data = []
            options = Options()
            options.add_argument('--remote-debugging-port=61625')
            options.add_argument('--no-sandbox')
            options.add_argument('--headless=new')
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            progress_bar = tqdm(total=sum(len(urls) for urls in user_stocks.values()), desc="Scanning Stocks", unit="stock")
            for user, urls in user_stocks.items():
                for data in urls:
                    progress_bar.set_postfix(stock=data[0].split('/')[-1][:7] + "...")
                    progress_bar.update(1)  # Increment progress

                    driver.execute_script("window.open('about:blank', 'secondtab');")

                    # It is switching to second tab now
                    driver.switch_to.window("secondtab")
                    stock_data = get_stock_details(data)
                    if user in ["my_stocks", "sp"]:
                        portfolio_data.append(stock_data)
                    all_stocks_data.append(stock_data)
            progress_bar.close()  # Close the progress bar when done
            generate_portfolio_data(portfolio_data)

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
            if driver:
                driver.quit()

            # Calculate total dividend to get from stocks
            total_units = get_two_decimal_val(sum(data["Qty"] for data in all_stocks_data))

            print(f"\n{datetime.now().strftime('%H:%M:%S')} - {int(total_units)} units purchased till now.")
            total = get_two_decimal_val(sum(data["Total Returns"] for data in all_stocks_data))
            print(f"Total returns is {total}/-")

            # Generate Files After Each Stock Bulk Scan
            file = 'stock_data'
            stocks_data = all_stocks_data
            generate_files(file, stocks_data)

            file = 'input_modified'
            modified_stocks = user_stocks.copy()
            for k, v in modified_stocks.items():
                user_stock_list = list()
                for new_data in v:
                    if in_memory_data[new_data[0]] != -2:
                        if len(new_data) == 4:
                            new_data[3] = in_memory_data[new_data[0]]
                        else:
                            new_data.append(in_memory_data[new_data[0]])
                        user_stock_list.append(new_data)
                    else:
                        user_stock_list.append(new_data)
                modified_stocks[k] = user_stock_list
            generate_files(file, modified_stocks, only_json=True)

            if buy_stock_list:
                file = 'buy_stock_details'
                data = buy_stock_list
                generate_files(file, data)
            if sell_stock_list:
                file = 'sell_stock_details'
                data = sell_stock_list
                generate_files(file, data)
            if (
                    datetime.now().hour >= 15 and datetime.now().minute > 30) or datetime.now().hour > 15 or datetime.now().weekday() > 4:
                weekly_update_msg = check_weekly_stock_details()
                if weekly_update_msg:
                    send_notifications(title="Weekly Update", message="Weekly Stocks update details",
                                       wp_message=weekly_update_msg)
                all_stock_name_list = [each_data['Name'] for each_data in stocks_data]
                all_stock_day_return_list = [each_data['Day Returns'] for each_data in stocks_data]
                most_grow_stock = max(all_stock_day_return_list)
                most_losser_stock = min(all_stock_day_return_list)
                eod_message = THANK_YOU_MESSAGE + (
                    f'\n\nToday\'s Top Gainer Stock in AK Stock Monitoring\n{all_stock_name_list[all_stock_day_return_list.index(most_grow_stock)]} ({most_grow_stock}%)'
                    f'\n\nToday\'s Top Loser Stock in AK Stock Monitoring\n{all_stock_name_list[all_stock_day_return_list.index(most_losser_stock)]} ({most_losser_stock}%)')
                if buy_stock_list:
                    for each_stock in buy_stock_list:
                        if each_stock['Url'] not in message_summary:
                            message_summary[each_stock['Url']] = {'name': each_stock['Name']}
                        to_be_purchase_unit = sum([individual_stock['Buy Units']
                                                   for individual_stock in buy_stock_list
                                                   if individual_stock['Url'] == each_stock['Url']])
                        message_summary[each_stock['Url']]['notified_units'] = to_be_purchase_unit
                        message_summary[each_stock['Url']]['triggered_price'] = each_stock['Current Price']
                        message_summary[each_stock['Url']]['current_price'] = [each_stock_details['Current Price']
                                                                               for each_stock_details in stocks_data
                                                                               if
                                                                               each_stock_details['Url'] == each_stock[
                                                                                   'Url']][-1]
                    eod_message += "\n\nToday's Summery:-\n\n"
                    for stock_url, stock_details in message_summary.items():
                        eod_message += (f"{stock_details['name']} - {stock_details['notified_units']} Units\n"
                                        f"Triggered Price - {stock_details['triggered_price']}/-\n"
                                        f"Current Price - {stock_details['current_price']}/-\n"
                                        f"{stock_url}\n\n")
                send_notifications(title=eod_message,
                                   message="Stock Monitoring Turning Off")
                break
        except (NoSuchElementException, TimeoutException, WebDriverException) as e:
            if retries > 0:
                if driver:
                    driver.quit()
                retries -= 1
                print(f"Retries left {retries}")
                time.sleep(5)
            else:
                raise Exception(e)
except Exception as e:
    print(e)
    print(traceback.format_exc())
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
