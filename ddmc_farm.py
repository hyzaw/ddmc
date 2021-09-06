import requests
import json
import re
import time

proxies = {
    "http": None,
    "https": None,
}


def catchWater(cookie):
    url = "https://farm.api.ddxq.mobi/api/v2/task/list-orchard?api_version=9.1.0&app_client_id=2&native_version=&app_version=9.29.0&reward=FEED&cityCode=0101"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 xzone/9.29.0",
        "Referer": "https://orchard-m.ddxq.mobi/?is_nav_hide=true&s=mine_orchard",
        "DDMC-GAME-TID": "2",
        "cookie": cookie
    }
    r = requests.get(url, headers=headers, proxies=proxies)
    list = re.findall(r'"taskCode":"(.*?)"', r.text)
    return list


def catchLogId(cookie):
    url = "https://farm.api.ddxq.mobi/api/v2/task/list?api_version=9.1.0&app_client_id=2&native_version=&app_version=9.29.0&gameId=1&cityCode=0101"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 xzone/9.29.0",
        "Referer": "https://game.m.ddxq.mobi/index.html",
        "DDMC-GAME-TID": "2",
        "cookie": cookie
    }
    r = requests.get(url, headers=headers, proxies=proxies)
    list = re.findall(r'"userTaskLogId":"(.*?)"', r.text)
    return list


def doTask(cookie, task):
    url = "https://farm.api.ddxq.mobi/api/v2/task/achieve?api_version=9.1.0&app_client_id=2&native_version=&app_version=9.29.0&gameId=1&taskCode=" + task
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 xzone/9.29.0",
        "Referer": "https://orchard-m.ddxq.mobi/?is_nav_hide=true&s=mine_orchard",
        "DDMC-GAME-TID": "2",
        "cookie": cookie
    }
    r = requests.get(url, headers=headers, proxies=proxies)
    r = json.loads(r.text)
    print(r["msg"])


def awardTask(cookie, logid):
    url = "https://farm.api.ddxq.mobi/api/v2/task/reward?api_version=9.1.0&app_client_id=2&native_version=&app_version=9.29.0&gameId=1&userTaskLogId=" + logid
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 xzone/9.29.0",
        "Referer": "https://game.m.ddxq.mobi/index.html",
        "DDMC-GAME-TID": "2",
        "cookie": cookie
    }
    r = requests.get(url, headers=headers, proxies=proxies)
    r = json.loads(r.text)
    print(r["msg"])


def fertilizer(cookie):
    url = "https://farm.api.ddxq.mobi/api/v2/task/list-orchard?api_version=9.1.0&app_client_id=2&native_version=&app_version=9.29.0&reward=FERTILIZER&cityCode=0101"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 xzone/9.29.0",
        "Referer": "https://orchard-m.ddxq.mobi/?is_nav_hide=true&s=mine_orchard",
        "DDMC-GAME-TID": "2",
        "cookie": cookie
    }
    r = requests.get(url, headers=headers, proxies=proxies)
    fertilizer = json.loads(r.text)["data"]["fertilizer"]["amount"]
    propsId = json.loads(r.text)["data"]["fertilizer"]["propsId"]
    if fertilizer >= 10:
        url = "https://farm.api.ddxq.mobi/api/v2/props/props-use?api_version=9.1.0&app_client_id=2&propsCode=FERTILIZER&propsId=%s&seedId=%s" % (
        propsId, propsId)
        r = requests.get(url, headers=headers, proxies=proxies)
        r = json.loads(r.text)
        print("施肥成功，剩余肥料：" + str(r["data"]["propsUse"]["amount"]) + "，当前肥料：" + str(
            r["data"]["propsUseResultVo"]["amount"]))


def water(cookie):
    url = "https://farm.api.ddxq.mobi/api/v2/userguide/detail?api_version=9.1.0&app_client_id=2&native_version=&app_version=9.29.0&gameId=1&guideCode=FISHPOND_NEW"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 xzone/9.29.0",
        "Referer": "https://orchard-m.ddxq.mobi/?is_nav_hide=true&s=mine_orchard",
        "DDMC-GAME-TID": "2",
        "cookie": cookie
    }
    r = requests.get(url, headers=headers, proxies=proxies).text
    amount = int(re.findall(r'"amount":(.*?)}', r)[0])
    seedid = re.findall(r'"seedId":"(.*?)"', r)[0]
    msg = json.loads(r)["data"]["baseSeed"]["msg"]
    url = "https://farm.api.ddxq.mobi/api/v2/props/feed?api_version=9.1.0&app_client_id=2&native_version=&app_version=9.29.0&gameId=1&propsId=%s&seedId=%s" % (
        seedid, seedid)
    if amount > 9:
        while True:
            r = requests.get(url, headers=headers, proxies=proxies)
            r = json.loads(r.text)
            if r["code"] == 0:
                print("浇水成功，剩余" + str(r["data"]["props"]["amount"]))
                if r["data"]["props"]["amount"] < 10:
                    print(msg)
                    break
            else:
                print("喂食失败")
            time.sleep(2)
    else:
        print(msg)


def main(cookie):
    try:
        WaterList = catchWater(cookie)
        for i in WaterList:
            if i != "POINT_EXCHANGE":
                doTask(cookie, i)
                time.sleep(2)
        loglist = catchLogId(cookie)
        for i in loglist:
            awardTask(cookie, i)
            time.sleep(2)
        fertilizer(cookie)
        water(cookie)
    except:
        pass
