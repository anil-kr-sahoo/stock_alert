import platform
import json
import csv
import os
import contextlib
import pywhatkit
import socket

from plyer import notification
from datetime import datetime
from collections import defaultdict

from user_stocks_input_file import *
from weekly_update import stocks_dict


def check_weekly_stock_details():
    """
    This helper function used to check weekly data and send weekly notifications
    :return: weekly stock message
    """
    if (stocks_dict["trigger_date"] != datetime.now().date().strftime("%d/%m/%Y") or
            not (len(stocks_dict['newly_added_stocks']) or len(stocks_dict['removed_stocks']))):
        return
    weekly_stock_msg = "Weekly update for AK Stock Monitoring"
    weekly_stock_msg += f"\n\nRemoved Stocks ({len(stocks_dict['removed_stocks'])}):-\n\n"
    if stocks_dict['removed_stocks']:
        weekly_stock_msg += '\n'.join(stocks_dict['removed_stocks'])
    else:
        weekly_stock_msg += "NA"
    weekly_stock_msg += f"\n\nAdded Stocks ({len(stocks_dict['newly_added_stocks'])}):-\n\n"
    if stocks_dict['newly_added_stocks']:
        weekly_stock_msg += '\n'.join(stocks_dict['newly_added_stocks'])
    else:
        weekly_stock_msg += "NA"
    weekly_stock_msg += "\n\nNote:- The monitoring stocks are present in group description."
    return weekly_stock_msg


def send_whatsapp_notification(message):
    """
    This helper function used to send notifications in whatsapp group or individual phone numbers
    :param message:
    :return:
    """
    if any(data in message for data in ['Buy', 'Sell', 'Thank', 'Weekly']):
        for group_id in GROUP_LIST:
            pywhatkit.sendwhatmsg_to_group_instantly(group_id=group_id, message=message, tab_close=True)
    else:
        for phone_no in PHONE_NO_LIST:
            pywhatkit.sendwhatmsg_instantly(phone_no=phone_no, message=message, tab_close=True)


def send_notifications(title, message, wp_message=None):
    """
    This helper function used to send notification in devices not in whatsapp.
    It's triggered to whatsapp notification after checking conditions.
    :param title:
    :param message:
    :param wp_message:
    :return:
    """
    system_name = socket.gethostname()
    if ALLOW_NOTIFICATION and system_name in ALLOWED_DEVICE_ACCESS:
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
                elif 'Weekly' in title:
                    os.system('spd-say "Hi Sir, Weekly stock portfolio updated" ')
                else:
                    os.system('spd-say "Hi Sir, Your wifi battery is low, Please plug in Charger" ')


def get_two_decimal_val(decimal_num):
    """
    This helper function used to return two decimal values
    :param decimal_num:
    :return:
    """
    return float('%.2f' % decimal_num)


def get_float_val(string_num):
    """
    This helper function used to get float value
    :param string_num:
    :return:
    """
    try:
        return float(string_num)
    except Exception:
        return 0


def get_to_be_credit_dividend(stock_price, dividend_ratio):
    """
    This helper function used to calculate the dividend going to receive in future
    """
    try:
        return get_two_decimal_val(get_float_val(stock_price) * get_float_val(dividend_ratio) / 100)
    except Exception:
        return 0


def generate_files(file_name, file_data, only_json=False):
    """
    This helper function used to generate files as json and csv.
    :param file_name:
    :param file_data:
    :param only_json:
    :return:
    """
    with open(f"{file_name}.json", "w") as stock_data:
        json.dump(file_data, stock_data, indent=2 if only_json else 4, sort_keys=True)
    if not only_json:
        with open(f'{file_name}.csv', 'w') as file:
            writer = csv.writer(file)
            heading = [list(file_data[0].keys())]
            stock_details = [list(element.values()) for element in file_data]
            writer.writerows(heading + stock_details)

def generate_portfolio_data(data):
    """
    This helper function used to get combined or unique portfolio data
    :param data:
    :return:
    """

    def get_two_decimal_val(value):
        """Returns value rounded to two decimal places."""
        return round(value, 2)

    # File path
    file_path = 'portfolio.json'

    # Load existing portfolio data safely
    try:
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            with open(file_path, 'r') as file:
                old_portfolio_data = json.load(file)
        else:
            old_portfolio_data = {}
    except (json.JSONDecodeError, FileNotFoundError):
        old_portfolio_data = {}

    # Extract old analytics data if available
    analytics_data = old_portfolio_data.get('datewise_returns', {})
    dividend_data = old_portfolio_data.get('datewise_dividends', {})
    today_date_str = datetime.now().strftime("%d %b, %Y")
    today_date_key = datetime.now().strftime("%m/%d/%Y")  # Format for storage

    # Dictionary to store consolidated stock data
    stocks = defaultdict(lambda: {
        "name":'',
        "total_stock_value": 0,
        "total_qty": 0,
        "total_returns": 0,
        "total_investment": 0,
        "current_price": 0
    })

    # Process each stock entry
    for stock in data:
        if not stock["Qty"]:
            continue
        url = stock["Url"]
        name = stock["Name"]
        qty = stock["Qty"]
        stock_avg_value = stock["Stock Average Value"]

        stocks[url]["name"] = name
        stocks[url]["total_stock_value"] += stock_avg_value * qty
        stocks[url]["total_qty"] += qty
        stocks[url]["total_returns"] += stock["Total Returns"]
        stocks[url]["total_investment"] += stock_avg_value * qty
        stocks[url]["current_price"] = stock["Current Price"]

        # Handle upcoming dividend tracking
        if stock.get("Upcoming Dividend Amount") and stock.get("Upcoming Dividend Date") == today_date_str:
            dividend_amount = qty * stock["Upcoming Dividend Amount"]

            if today_date_key not in dividend_data:
                dividend_data[today_date_key] = []
            all_urls = [details['url'] for details in dividend_data[today_date_key] if details.get('url')]
            if url not in all_urls:
                dividend_data[today_date_key].append({
                    'name': name,
                    'url': url,
                    'dividend_amount': get_two_decimal_val(dividend_amount),
                    'declared_dividend': stock["Upcoming Dividend Amount"]
                })
            if url in all_urls:
                amounts = [details['dividend_amount'] for details in dividend_data[today_date_key] if details.get('url') == url]
                if dividend_amount not in amounts:
                    dividend_data[today_date_key].append({
                        'name': name,
                        'url': url,
                        'dividend_amount': get_two_decimal_val(dividend_amount),
                        'declared_dividend': stock["Upcoming Dividend Amount"]
                    })
    # Compute final results
    result = []
    total_profit_loss = 0
    total_overall_investment = 0

    for url, values in stocks.items():
        avg_stock_value = values["total_stock_value"] / values["total_qty"]
        total_profit_loss += values["total_returns"]
        total_overall_investment += values["total_investment"]

        result.append({
            "Name": values["name"],
            "Url": url,
            "Avg Stock Average Value": get_two_decimal_val(avg_stock_value),
            "Total Returns": get_two_decimal_val(values["total_returns"]),
            "Total Qty": values["total_qty"],
            "Current Price": get_two_decimal_val(values["current_price"])
        })

    # Update analytics data
    analytics_data[today_date_key] = {
        'total_investment': get_two_decimal_val(total_overall_investment),
        'total_profit_loss': get_two_decimal_val(total_profit_loss),
    }

    # Construct final portfolio data
    portfolio_data = {
        'datewise_returns': analytics_data,
        'current_stock_data': result,
        'datewise_dividends': dividend_data
    }

    generate_files('portfolio', portfolio_data, True)
