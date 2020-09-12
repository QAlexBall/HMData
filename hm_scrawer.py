import os
import time
import json
from selenium import webdriver
from HMSpider import HMSpider

    
def main():
    url = "https://portalpro.hemaos.com/"
    cookies_file_p = "./config/cookies_final.txt"
    spider = HMSpider()
    spider.login(url, cookies_file_p=cookies_file_p)
    spider.select_merchant("大润发")
    spider.menu_search("O2O实时看板")
    print(spider.select_distribution_station("大润发宁波慈溪店配送站"))
    # for merchant in spider.merchants_config["merchants"].keys():
    #     spider.select_merchant(merchant)
    #     spider.menu_search("O2O实时看板")
    #     for station in spider.merchants_config["merchants"][merchant]:
    #         print(station, spider.select_distribution_station(station))
    #     spider.driver.switch_to_default_content()
    time.sleep(300)
    spider.driver.close()


if __name__ == "__main__":
    main()