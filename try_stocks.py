import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument('--remote-debugging-port=61625')
options.add_argument('--no-sandbox')
options.add_argument('--headless=new')
url = "https://www.google.com/finance/quote/VEDL:NSE"
# url = "https://www.nseindia.com/get-quotes/equity?symbol=AJANTPHARM"
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.execute_script("window.open('about:blank', 'secondtab');")
driver.switch_to.window("secondtab")
driver.get(url)
# all_details = driver.find_element(By.CLASS_NAME, "ft785TableContainer").text
# print(all_details)
all_data = driver.find_element(By.CLASS_NAME, "rPF6Lc").text.split('\n')
price = all_data[0][1:]
day_returns = float(all_data[1][:-1]) *-1 if all_data[2][0] == "-" else float(all_data[1][:-1])
print(price, day_returns)
