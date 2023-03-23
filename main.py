from time import sleep
import json
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

def send_notificaations(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=2
    )
def get_two_decimal_val(decimal_num):
    return float('%.2f' % decimal_num)

def get_current_stock_price():
    raw_html = driver.find_element(By.CLASS_NAME, "lpu38Pri").get_attribute('innerHTML').split('hidden;">')[1:]
    raw_amount = ''.join(all_raw.split('</span>')[0] for all_raw in raw_html)
    try:
        return get_two_decimal_val(float(raw_amount)/100)
    except Exception:
        return 0

def get_to_be_credit_dividend(stock_price, dividend_ratio):
    try:
        return get_two_decimal_val(float(stock_price)*float(dividend_ratio)/100)
    except Exception as e:
        return 0

def get_stock_details(all_data):
    divident_ratio_percentage = 0
    url = all_data[0]
    stock_qty = all_data[1]
    driver.get(url)
    name = driver.find_element(By.CLASS_NAME, "lpu38Head").text
    current_price = get_current_stock_price()
    day_returns = driver.find_element(By.CLASS_NAME, "lpu38Day").text.split('(')[1].split(')')[0][:-1]
    all_details = driver.find_element(By.CLASS_NAME, "ft785TableContainer").text
    stock_details = {"Name": name, "Current Price": current_price, "Day Returns": day_returns}
    ls = {"Name": name, "Current Price": current_price}
    for each in all_details.split('\n'):
        if 'Dividend' in each or 'ROE' in each:
            if 'Dividend' in each:
                divident_ratio_percentage = each.split(" ")[-1][:-1]
            stock_details[(' ').join(each.split(" ")[:-1])] = each.split(" ")[-1][:-1]
            ls[(' ').join(each.split(" ")[:-1])] = each.split(" ")[-1][:-1]
        elif 'Market' in each:
            stock_details[(' ').join(each.split(" ")[:-1])] = each.split(" ")[-1][1:-2].replace(',', '')
        else:
            stock_details[(' ').join(each.split(" ")[:-1])] = each.split(" ")[-1]
    ls["Credit Dividend"] = get_to_be_credit_dividend(current_price, divident_ratio_percentage)
    ls["To Be Credit Dividend"] = get_two_decimal_val(get_to_be_credit_dividend(current_price, divident_ratio_percentage) * stock_qty)
    ls["Qty"] = stock_qty

    print(json.dumps(ls, indent=2))
    send_notificaations("Stok Details", str(ls))
    return ls


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
nm = [
    ['https://groww.in/stocks/tata-steel-ltd', 130],
    ['https://groww.in/stocks/one-communications-ltd', 1],
    ['https://groww.in/stocks/pb-fintech-ltd', 3],
    ['https://groww.in/stocks/larsen-toubro-infotech-ltd', 5],
    ['https://groww.in/stocks/indian-railway-catering-tourism-corpn-ltd', 10],
    ['https://groww.in/stocks/hdfc-bank-ltd', 3],
    ['https://groww.in/stocks/happiest-minds-technologies-ltd', 19],
    ['https://groww.in/stocks/avenue-supermarts-ltd', 1],
]
all_data = list()
for data in urls:
    if 'idfc' not in data[0]:
        continue
    driver.execute_script("window.open('about:blank', 'secondtab');")

    # It is switching to second tab now
    driver.switch_to.window("secondtab")
    all_data.append(get_stock_details(data))
driver.quit()
total = sum(data["To Be Credit Dividend"] for data in all_data)
print(f"Total devident to be credit is {total}/-")

with open("stock_data.json", "w") as twitter_data_file:
    json.dump(all_data, twitter_data_file, indent=4, sort_keys=True)
