import contextlib
import json
import os
from datetime import datetime
import socket
import platform

import pywhatkit
from plyer import notification

from user_stocks_input_file import ALLOWED_DEVICE_ACCESS, THANK_YOU_MESSAGE
from weekly_update import stocks_dict

system_name = socket.gethostname()


def check_weekly_stock_details():
    if (stocks_dict["trigger_date"] != datetime.now().date().strftime("%d/%m/%Y") or
            not (len(stocks_dict['newly_added_stocks']) or len(stocks_dict['removed_stocks']))):
        return
    weekly_stock_msg = "Weekly update for AK Stock Monitoring"
    weekly_stock_msg += f"\n\nRemoved Stocks :-\n\n"
    if stocks_dict['removed_stocks']:
        weekly_stock_msg += '\n'.join(stocks_dict['removed_stocks'])
    else:
        weekly_stock_msg += "NA"
    weekly_stock_msg += f"\n\nAdded Stocks :-\n\n"
    if stocks_dict['newly_added_stocks']:
        weekly_stock_msg += '\n'.join(stocks_dict['newly_added_stocks'])
    else:
        weekly_stock_msg += "NA"
    weekly_stock_msg += "\n\nNote:- The monitoring stocks are present in group description." \
                        "\nIf you invested any other stocks which not being monitoring, " \
                        "please message personally to admin, about the stock and it's average value."
    return weekly_stock_msg


def send_whatsapp_notification(message):
    pywhatkit.sendwhatmsg_to_group_instantly(group_id="KbFKSNqUkWs8RGVhiPpw4U", message=message, tab_close=True)


def send_notifications(title, message, wp_message=None):
    if system_name in ALLOWED_DEVICE_ACCESS:
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
            if 'over' in title:
                os.system('spd-say "Hi Sir, Trading over for today, please run wi-fi battery checker" ')
            else:
                os.system('spd-say "Hi Sir, Weekly stock portfolio updated" ')


weekly_update_msg = check_weekly_stock_details()
if weekly_update_msg:
    send_notifications(title="Weekly Update", message="Weekly Stocks update details", wp_message=weekly_update_msg)

file = open('stock_data.json')
data = json.load(file)

heighest_day_returns = data[0]['Day Returns']
heighest_stock_name =  data[0]['Name']
lowest_day_returns =  data[0]['Day Returns']
lowest_stock_name =  data[0]['Name']
for each_stock in data[1:]:
    if each_stock['Day Returns'] > heighest_day_returns:
        heighest_day_returns = each_stock['Day Returns']
        heighest_stock_name =  each_stock['Name']

    if each_stock['Day Returns'] < lowest_day_returns:
        lowest_day_returns = each_stock['Day Returns']
        lowest_stock_name =  each_stock['Name']

file.close()
eod_message = THANK_YOU_MESSAGE + (f'\n\nToday\'s Top Gainer Stock in AK Stock Monitoring\n{heighest_stock_name} ({heighest_day_returns}%)'
                                   f'\n\nToday\'s Top Loser Stock in AK Stock Monitoring\n{lowest_stock_name} ({lowest_day_returns}%)')

print(eod_message)
send_notifications(title=eod_message,
                   message="Please run wifi battery checker")