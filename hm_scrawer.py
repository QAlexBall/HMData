import csv
import os
import time
import json
from selenium import webdriver
from HMSpider import HMSpider
from utils.records import create_csv

    
def main():
    url = "https://portalpro.hemaos.com/"
    cookies_file_p = "./config/cookies_final.txt"
    csv_path = create_csv()
    csv_f = open(csv_path, 'a+', newline='', encoding='utf-8-sig')
    csv_writer = csv.writer(csv_f)
    csv_writer.writerow(['站点', '强制妥投单', '二次妥投单', '物流超时单', '配送超时单'])
    spider = HMSpider()
    spider.login(url, cookies_file_p=cookies_file_p)
    # spider.select_merchant("大润发")
    # spider.menu_search("O2O实时看板")
    # print(spider.select_distribution_station("大润发宁波慈溪店配送站")['basic'])


    for merchant in spider.merchants_config["merchants"].keys():
        spider.select_merchant(merchant)
        spider.menu_search("O2O实时看板")
        for station in spider.merchants_config["merchants"][merchant]:
            station_info = spider.select_distribution_station(station)
            print(station_info)
            basic = station_info['basic']
            larger = station_info['larger_than_35']
            if basic:
                csv_writer.writerow([station, basic[9], basic[11], basic[13], larger])
            else:
                csv_writer.writerow([station])

        spider.driver.switch_to_default_content()

    csv_f.cose()
    time.sleep(10)
    spider.driver.close()


if __name__ == "__main__":
    main()