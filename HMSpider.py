import os
import time
import json
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from config import MERCHANTS_CONFIG
from utils.utils import split, generete_cookies


class HMSpider(object):
    def __init__(self, visible=None):
        option = None
        option = webdriver.ChromeOptions()
        if visible == '0':
            option.add_argument('--headless')
            option.add_argument('window-size=1920,1080')
        self.driver = webdriver.Chrome("./bin/chromedriver.exe", chrome_options=option)
        self.driver.implicitly_wait(30)
        self.cookies_file_p = "./config/cookies_final.txt"
        self.merchant_config_p = "./config/merchants.json"
        # self.merchants_config = self._load_merchants_config()
        self.merchants_config = MERCHANTS_CONFIG
        print(self.merchants_config)
        self._setup_driver()
    
    def _setup_driver(self):
        self.driver.set_page_load_timeout(3000)
        self.driver.set_script_timeout(3000)
    
    def login(self, url, cookies_file_p=None):
        if cookies_file_p:
            self.cookies_file_p = cookies_file_p

        if not os.path.exists(cookies_file_p):
            generete_cookies(self.driver, url, self.cookies_file_p)
        
        print("===> get_cookies")
        self.driver.get(url)
        with open(self.cookies_file_p, "r") as cookies_f:
            cookieslist = json.load(cookies_f)
            for cookie in cookieslist:
                if isinstance(cookie.get('expiry'), float):
                    cookie['expiry'] = int(cookie['expiry'])
                self.driver.add_cookie(cookie)
        self.driver.get(url)
    
    def select_merchant(self, name):
        selector = self.by_xpath_with_sleep('//*[@class="portal-switcher-trigger"]')
        selector.click()
        time.sleep(1)
        self.driver.switch_to_frame('iFrameResizer0')
        merchant_selector = self.by_xpath_with_sleep('//*[@id="container"]/div/div/div/div/div[1]/form/div[1]/div[2]/span/span[1]')
        merchant_selector.click()
        merchant = self.by_xpath_with_sleep('/html/body/div[4]/ul/li[@title="{}"]'.format(name))
        merchant.click()
        yes_button = self.by_xpath_with_sleep('//*[@id="container"]/div/div/div/div/div[1]/form/div[7]/button[1]')
        yes_button.click()
        self.driver.switch_to_default_content()
    
    def menu_search(self, name):
        menu_search = self.by_xpath_with_sleep('//*[@id="header-info"]/div/div[1]', 1)
        menu_search.click()
        input_button = self.by_xpath_with_sleep('/html/body/div[5]/div[2]/div/span/input', 1)
        input_button.clear()
        input_button.send_keys(name)
        dashbaord_selector = self.by_xpath_with_sleep('/html/body/div[5]/div[2]/ul/li[@title="{}"]'.format(name), 1)
        dashbaord_selector.click()

    def select_distribution_station(self, name):
        print("==> select station", name)
        info = {'basic': None, 'larger_than_35': None}
        iframe = self.by_xpath_with_sleep('//*[@id="wrapBody"]/div[2]/div/iframe', 1)
        self.driver.switch_to_frame(iframe)
        station_input = self.by_xpath_with_sleep('//*[@id="dockCode"]/span/input', 1)
        station_input.clear()
        station_input.send_keys(name)
        station = self.by_xpath_with_sleep('/html/body/div[2]/div/div/ul', 2)
        if station.text:
            station.click()
            # find = self.by_xpath_with_sleep('//*[@id="container"]/div/div[2]/div/div/form/div[2]/div[2]/button[1]', 1)
            find = self.by_xpath_with_sleep('//*[@id="container"]/div/div[1]/div/div/form/div[2]/div[2]/button[1]', 1)
            find.click()
            # item = self.by_xpath_with_sleep('//*[@id="container"]/div/div[3]/div[2]/div/div[2]/div[2]/div[4]/div[2]', 2)
            item = self.by_xpath_with_sleep('//*[@id="container"]/div/div[2]/div[2]/div/div[2]/div[2]/div[4]/div[2]', 2)

            info['basic'] = item.text.split("\n")
            if info['basic'][-1] != '0':
                try:
                    info['larger_than_35'] = self.analysis_timeout_order()
                except:
                    print("===> analysis timeout order failed!")
                    info['larger_than_35'] = 0
            else:
                info['larger_than_35'] = 0
        else:
            print("didn't exist", station)
        self.driver.switch_to_default_content()
        return info

    def analysis_timeout_order(self):
        print("===> analysis timeout order")
        item = self.by_xpath('//*[@id="container"]/div/div[2]/div[2]/div/div[2]/div[2]/div[4]/div[2]/div[7]/div[2]')
        item.click()
        try:
            orders = []
            time.sleep(5)
            curr_orders, count = [], 0
            while len(curr_orders) < 8 and count < 30:
                time.sleep(2)
                timeout_orders = self.by_xpath('/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[2]/table/tbody')
                curr_orders = timeout_orders.text.split("\n")
                count += 1
            
            page_orders = split(curr_orders, 8)
            orders += page_orders
            next_button = self.by_xpath('/html/body/div[2]/div/div[2]/div[2]/div[3]/div/button[2]')
            while next_button.is_enabled():
                next_button.click()
                curr_orders = [], 0
                while len(curr_orders) < 8 and count < 30:
                    time.sleep(2)
                    timeout_orders = self.by_xpath('/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[2]/table/tbody')
                    curr_orders = timeout_orders.text.split("\n")
                    count += 1

                page_odrers = split(curr_orders, 8)
                orders += page_orders
            larger_than_35 = len([item for item in orders if item != '-' and int(item) >= 35])
        except:
            print("===> can't find such orders!")
            larger_than_35 = 0
        close_button = self.by_xpath_with_sleep('/html/body/div[2]/div/div[2]/a/i', 1)
        close_button.click()
        return larger_than_35

    def by_xpath(self, path):
        element = self.driver.find_element_by_xpath(path)
        return element
    
    def by_xpath_with_sleep(self, path, peroid=1, count_num=60):
        element, count = None, 0
        while element is None and count < count_num:
            count += 1
            try:
                time.sleep(peroid)
                element = self.by_xpath(path)
            except:
                print("can't get element with XPath", path)
                element = None
        return element

    def _load_merchants_config(self):
        with open(self.merchant_config_p, "r", encoding="GB18030") as f:
            merchants_config = json.load(f)
            print(merchants_config)
        return merchants_config
        

if __name__ == "__main__":
    spider = HMSpider()