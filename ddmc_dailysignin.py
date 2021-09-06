import requests
import json
import time

proxies = {
    "http": None,
    "https": None,
}

def main(cookie):
    try:
        url="https://sunquan.api.ddxq.mobi/api/v2/user/signin/"
        headers={
            "User-Agent":"Mozilla/5.0 (Linux; Android 5.1.1) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 xzone/9.29.0",
            "Referer":"https://activity.m.ddxq.mobi/",
            "cookie":cookie
        }
        data="api_version=9.7.3&app_version=1.0.0&app_client_id=3&native_version=9.29.0&city_number=0101"

        r=requests.post(url,data=data,headers=headers,proxies=proxies)
        r=json.loads(r.text)
        if r["success"]==1:
            print("签到成功")
    except:
        print("err")
