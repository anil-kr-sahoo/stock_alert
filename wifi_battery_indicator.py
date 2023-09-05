import contextlib
import os
import platform
from time import sleep

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from plyer import notification

# Use Airtel Wi-Fi battery indicator as well
modem_url = "http://192.168.1.1/index.html"
POWER_BANK_LOW_BATTERY = False


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
            if 'Charge' in title:
                os.system('spd-say "Hi Sir, Please Check your Power Bank Battery" ')
            elif 'Restart' in title:
                os.system('spd-say "Hi Sir, Please restart server, its crashed due to low internet" ')
            else:
                os.system('spd-say "Hi Sir, Your wifi running low, Please plug in Charger" ')


wifi_driver = None
try:
    while True:
        wifi_options = Options()
        wifi_options.headless = True
        wifi_options.add_argument('--remote-debugging-port=61625')
        wifi_options.add_argument('--no-sandbox')
        wifi_driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=wifi_options)
        wifi_driver.execute_script("window.open('about:blank', 'secondtab');")
        wifi_driver.switch_to.window("secondtab")
        wifi_driver.get(modem_url)
        wifi_battery_percentage = \
            wifi_driver.find_element(By.ID, "qtip-5-content").get_attribute('innerHTML').split('<b>')[1].split(
                '</b>')[0][:-1]
        print(wifi_battery_percentage)
        with contextlib.suppress(Exception):
            if POWER_BANK_LOW_BATTERY and 'Charging' not in wifi_battery_percentage:
                send_notifications(title="Charge your Power Bank", message="Power Bank Battery Low")
            elif int(wifi_battery_percentage) <= 15:
                send_notifications(title=f"{wifi_battery_percentage}% Battery Left",
                                   message="Wifi modem is going to be shut down soon\nPlease plug in charger")
        wifi_driver.quit()
        sleep(60)
except Exception as e:
    send_notifications(title="Restart Server", message="Server crashed due low internet connection")

    if wifi_driver:
        wifi_driver.quit()
        wifi_driver.close()
