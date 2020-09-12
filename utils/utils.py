import os
import time
import json

TEST_COOKIES = {
    "cna": "ujM4F/eXgzACASe9K17Xwsza",
    "_ati": "63909201298",
    "WDK_USER_OPEN_ACCOUNT_ID": "4398987157280",
    "WDKSESSID": "em8FNY4iS5q8__ARWmZWQaCAaCA",
    "X-XSRF-TOKEN": "b41fc30b-7a97-446a-bc11-174a1842f9b0",
    "WDK_SECRET": "099fa1748f7ca11e80d007fbb068283e",
    "WDK_UA": "5D5554460924E99584DED4FB40CA6CAD",
    "WDK_WAREHOUSE_CODE": "SJ083",
    "isg": "BP__ineYnGrFjJhyThWpsoPWjtOJ5FOGIrWBYZHMm671oB8imbTj1n224nhe-Cv-"
}


def generete_cookies(driver, url, cookies_file_p):
    print("===> generate cookies")
    driver.get(url)
    driver.get(url)
    time.sleep(120)
    print(driver.get_cookies())
    with open(cookies_file_p, 'w') as cookies_f:
        cookies_f.write(json.dumps(driver.get_cookies()))

