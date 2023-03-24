import contextlib
import os
from sys import platform
from time import sleep

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from plyer import notification

# Use Airtel Wi-Fi battery indicator as well
modem_url = "http://192.168.1.1/index.html"


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
                os.system('spd-say "HURRY!!! Buy a Stock" ')
            elif 'Sell' in title:
                os.system('spd-say "HURRY!!! Sell a Stock" ')
            else:
                os.system('spd-say "Upps!! Your Wi-Fi Battery Low" ')


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
        if int(wifi_battery_percentage) <= 15:
            send_notifications(title=f"{wifi_battery_percentage}% Battery Left",
                               message="Wifi modem is going to be shut down soon\nPlease plug in charger")
    wifi_driver.quit()
    sleep(60)
