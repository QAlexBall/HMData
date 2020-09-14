import os
import time
import json


def generete_cookies(driver, url, cookies_file_p):
    print("===> generate cookies")
    driver.get(url)
    driver.get(url)
    time.sleep(120)
    print(driver.get_cookies())
    with open(cookies_file_p, 'w') as cookies_f:
        cookies_f.write(json.dumps(driver.get_cookies()))

def split(arr, size, index=3):
    arrs = []
    while len(arr) > size:
        pice = arr[:size]
        pice = pice[index]
        arrs.append(pice)
        arr = arr[size:]
    arrs.append(arr[index])
    return arrs