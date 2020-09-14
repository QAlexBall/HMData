import os
import time
import json
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from config import MERCHANTS_CONFIG
from utils.utils import split


class HMSpider(object):
    def __init__(self):
        self.driver = webdriver.Chrome("./bin/chromedriver.exe")
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
        time.sleep(3)
        selector = self.by_xpath('//*[@class="portal-switcher-trigger"]')
        selector.click()
        time.sleep(1)
        self.driver.switch_to_frame('iFrameResizer0')
        merchant_selector = self.by_xpath('//*[@id="container"]/div/div/div/div/div[1]/form/div[1]/div[2]/span/span[1]')
        merchant_selector.click()
        time.sleep(1)
        merchant = self.by_xpath('/html/body/div[4]/ul/li[@title="{}"]'.format(name))
        merchant.click()
        yes_button = self.by_xpath('//*[@id="container"]/div/div/div/div/div[1]/form/div[7]/button[1]')
        yes_button.click()
        self.driver.switch_to_default_content()
        time.sleep(5)
    
    def menu_search(self, name):
        menu_search = self.by_xpath('//*[@id="header-info"]/div/div[1]')
        menu_search.click()
        time.sleep(1)
        input_button = self.by_xpath('/html/body/div[5]/div[2]/div/span/input')
        input_button.clear()
        input_button.send_keys(name)
        time.sleep(1)
        dashbaord_selector = self.by_xpath('/html/body/div[5]/div[2]/ul/li[@title="{}"]'.format(name))
        dashbaord_selector.click()
        time.sleep(5)

    def select_distribution_station(self, name):
        iframe = self.by_xpath('//*[@id="wrapBody"]/div[2]/div/iframe')
        self.driver.switch_to_frame(iframe)
        station_input = self.by_xpath('//*[@id="dockCode"]/span/input')
        station_input.clear()
        station_input.send_keys(name)
        time.sleep(2)
        # station = self.by_xpath('/html/body/div[3]/div/div/ul/li')
        info = {}
        try:
            station = self.by_xpath('/html/body/div[2]/div/div/ul')
            station.click()
            find = self.by_xpath('//*[@id="container"]/div/div[2]/div/div/form/div[2]/div[2]/button[1]')
            find.click()
            time.sleep(5)
            item = self.by_xpath('//*[@id="container"]/div/div[3]/div[2]/div/div[2]/div[2]/div[4]/div[2]')
            info['basic'] = item.text.split("\n")
            time.sleep(3)
            if info['basic'][-1] != '0':
                info['larger_than_35'] = self.analysis_timeout_order()
            else:
                info['larger_than_35'] = 0
        except:
            info = {'basic': None, 'larger_than_35': None}
        self.driver.switch_to_default_content()
        return info

    def analysis_timeout_order(self):
        item = self.by_xpath('//*[@id="container"]/div/div[3]/div[2]/div/div[2]/div[2]/div[4]/div[2]/div[7]/div[2]')
        item.click()
        time.sleep(10)
        orders = []
        timeout_orders = self.by_xpath('/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[2]/table/tbody')
        page_orders = split(timeout_orders.text.split("\n"), 8)
        orders += page_orders
        next_button = self.by_xpath('/html/body/div[2]/div/div[2]/div[2]/div[3]/div/button[2]')
        while next_button.is_enabled():
            next_button.click()
            time.sleep(5)
            timeout_orders = self.by_xpath('/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[2]/table/tbody')
            page_orders = split(timeout_orders.text.split("\n"), 8)
            orders += page_orders
        larger_than_35 = len([item for item in orders if item != '-' and int(item) >= 35])
        close_button = self.by_xpath('/html/body/div[2]/div/div[2]/a/i')
        close_button.click()
        return larger_than_35

    def by_xpath(self, path):
        return self.driver.find_element_by_xpath(path)

    def _load_merchants_config(self):
        with open(self.merchant_config_p, "r", encoding="GB18030") as f:
            merchants_config = json.load(f)
            print(merchants_config)
        return merchants_config
        

if __name__ == "__main__":
    spider = HMSpider()