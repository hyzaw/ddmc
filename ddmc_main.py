import ddmc_dailysignin
import requests
import ddmc_yutang
import ddmc_farm
import time
import json

proxies = {
    "http": None,
    "https": None,
}
cookie = []
count = 1
token = ""
username = ""
password = ""
if username == "" or password == "":
    f = open("/ql/config/auth.json")
    auth = f.read()
    auth = json.loads(auth)
    username = auth["username"]
    password = auth["password"]
    token = auth["token"]
    f.close()


def getPhone(ck):
    url = "https://maicai.api.ddxq.mobi/user/info?api_version=9.7.3&app_version=1.0.0&app_client_id=3"
    headers = {
        "Host": "maicai.api.ddxq.mobi",
        "Origin": "https://activity.m.ddxq.mobi",
        "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; vmos Build/LMY48G; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045714 Mobile Safari/537.36 xzone/9.29.0 station_id/5b1f75e806752e5f408b5f70",
        "Referer": "https://activity.m.ddxq.mobi/",
        "Cookie": ck
    }
    r = requests.get(url, headers=headers, proxies=proxies).text
    return json.loads(r)["data"]["mobile"]


def gettimestamp():
    return str(int(time.time() * 1000))


def login(username, password):
    url = "http://127.0.0.1:5700/api/login?t=%s" % gettimestamp()
    data = {"username": username, "password": password}
    r = s.post(url, data)
    s.headers.update({"authorization": "Bearer " + json.loads(r.text)["data"]["token"]})


def getitem(key):
    url = "http://127.0.0.1:5700/api/envs?searchValue=%s&t=%s" % (key, gettimestamp())
    r = s.get(url)
    item = json.loads(r.text)["data"]
    return item


if __name__ == '__main__':
    s = requests.session()
    if token == "":
        login(username, password)
    else:
        s.headers.update({"authorization": "Bearer " + token})
    cookie = getitem("DDMC_COOKIE")
    for i in cookie:
        print("开始执行第%s个账号" % count)
        ck=i["value"]
        try:
            mobile = getPhone(ck)
            print("当前账号手机号码为：" + mobile)
            ddmc_dailysignin.main(ck)
            time.sleep(20)
            ddmc_yutang.main(ck)
            time.sleep(20)
            ddmc_farm.main(ck)
            print("\n\n\n")
            count += 1
        except:
            print("发生错误！")
            count += 1
