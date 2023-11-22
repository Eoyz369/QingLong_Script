
# PikPak会员奖励隐藏任务
# Source: @纸鸢花的花语 https://www.bilibili.com/video/BV1x8411r7nk/
# 请勿用于商业用途！

# 修改说明：在原项目上简单适配青龙使用
# 变量 pikpakNAME（邮箱）,pikpakPWD（密码）
# cron: 30 1 * * *
# const $ = new Env("PikPak会员奖励隐藏任务");

# coding:utf-8
import time

import requests
import json
import uuid
import hashlib
import random
import os

# 创建随机UA
def get_user_agent():
    tmp1 = random.randrange(90, 120)
    tmp2 = random.randrange(5200, 5500)
    tmp3 = random.randrange(90, 180)
    tmp_version = str(tmp1) + ".0." + str(tmp2) + "." + str(tmp3)
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/' + tmp_version + ' Safari/537.36'
    print(ua)
    return ua


# md5加密字符串
def get_hash(str):
    obj = hashlib.md5()
    obj.update(str.encode("utf-8"))
    result = obj.hexdigest()
    return result


# 仿制captcha_sign
def get_sign(begin_str):
    salts = [
        {'alg': 'md5', 'salt': '6ov9AjGrStwPh+Dy9CSYcJ+QesOX'},
        {'alg': 'md5', 'salt': ''},
        {'alg': 'md5', 'salt': 'tpn69xYajl9QCoDcBquNmW'},
        {'alg': 'md5', 'salt': 'IEFNmRWeu6bbHQG'},
        {'alg': 'md5', 'salt': 'DPmuDzz1EDfKSWvj4QrkawjOaSuVBR/Wpb8AuERPCJH/pwDn9R78'},
        {'alg': 'md5', 'salt': 'nfGllh2kOXm/2KqpHHAeAa9X5B4GjGL4tZ'},
        {'alg': 'md5', 'salt': '7PaOcGq2REG9IGlMvdz2H1DhS1bO9uQY/fAUw2y766iQ+l'},
        {'alg': 'md5', 'salt': 'BLs1AD/VKU/6M23HzJcna'},
        {'alg': 'md5', 'salt': '6lS6PzMP'},
        {'alg': 'md5', 'salt': 'iO36B4qMPNAqjt3JAR8KGddkY'},
    ]

    # print("Salts：" + str(salts))
    hex_str = begin_str
    for salt in salts:
        hex_str = get_hash(hex_str + salt["salt"])
    print("Sign：", hex_str)
    return hex_str


# 安全验证-登录
def login_init(client_id, device_id, email, user_agent):
    url = "https://user.mypikpak.com/v1/shield/captcha/init"

    payload = {
        "client_id": client_id,
        "action": "POST:/v1/auth/signin",
        "device_id": device_id,
        "captcha_token": "",
        "meta": {"email": email}
    }
    headers = {
        "sec-ch-ua": '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        "x-provider-name": "NONE",
        "x-sdk-version": "6.0.0",
        "x-device-sign": "wdi10." + device_id + "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "accept-language": "zh-CN",
        "x-os-version": "Win32",
        "x-net-work-type": "NONE",
        "sec-ch-ua-platform": '"Windows"',
        "x-platform-version": "1",
        "x-protocol-version": "301",
        "x-client-version": "1.0.0",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": user_agent,
        "content-type": "application/json",
        "Referer": "https://mypikpak.com/",
        "x-client-id": client_id,
        "x-device-model": "chrome/117.0.0.0",
        "x-device-id": device_id,
        "x-device-name": "PC-Chrome",
        "Accept-Encoding": "deflate, gzip"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)
    return json.loads(response.text);


# 登录
def get_login(username, password, client_id, device_id, user_agent, captcha_token):
    url = "https://user.mypikpak.com/v1/auth/signin"

    payload = {
        "username": username,
        "password": password,
        "client_id": client_id
    }
    headers = {
        "sec-ch-ua": '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        "x-captcha-token": captcha_token,
        "x-provider-name": "NONE",
        "x-sdk-version": "6.0.0",
        "x-device-sign": "wdi10." + device_id + "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "accept-language": "zh-CN",
        "x-os-version": "Win32",
        "x-net-work-type": "NONE",
        "sec-ch-ua-platform": '"Windows"',
        "x-platform-version": "1",
        "x-protocol-version": "301",
        "x-client-version": "1.0.0",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": user_agent,
        "content-type": "application/json",
        "Referer": "https://mypikpak.com/",
        "x-client-id": client_id,
        "x-device-model": "chrome/117.0.0.0",
        "x-device-id": device_id,
        "x-device-name": "PC-Chrome",
        "Accept-Encoding": "deflate, gzip"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)
    return json.loads(response.text);


# 获取验证CODE
def get_authorize(client_id, device_id, access_token, user_agent):
    url = "https://user.mypikpak.com/v1/user/authorize"

    payload = {
        "client_id": client_id,
        "state": "ignored",
        "scope": "user+pan+offline",
        "response_type": "code",
        "redirect_uri": "chrome-extension://jkmnnedinolbhjcibbfpdlkmmibkcbgf"
    }
    headers = {
        "sec-ch-ua": '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        "x-provider-name": "NONE",
        "x-sdk-version": "6.0.0",
        "x-device-sign": "wdi10." + device_id + "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "accept-language": "zh-CN",
        "Authorization": "Bearer " + access_token,
        "x-os-version": "Win32",
        "x-net-work-type": "NONE",
        "sec-ch-ua-platform": '"Windows"',
        "x-platform-version": "1",
        "x-protocol-version": "301",
        "x-client-version": "1.0.0",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": user_agent,
        "content-type": "application/json",
        "Referer": "https://mypikpak.com/",
        "x-client-id": client_id,
        "x-device-model": "chrome/117.0.0.0",
        "x-device-id": device_id,
        "x-device-name": "PC-Chrome",
        "Accept-Encoding": "deflate, gzip"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)
    return json.loads(response.text);


# 获取真正access_token
def get_token(code, client_id, user_agent):
    url = "https://user.mypikpak.com/v1/auth/token"

    payload = {
        "code": code,
        "grant_type": "authorization_code",
        "client_id": client_id
    }
    headers = {
        "authority": "user.mypikpak.com",
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5",
        "content-type": "application/json",
        "origin": "chrome-extension://jkmnnedinolbhjcibbfpdlkmmibkcbgf",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "none",
        "user-agent": user_agent,
        "x-client-id": client_id,
        "x-protocol-version": "301",
        "x-sdk-version": "5.2.0",
        "Accept-Encoding": "deflate, gzip"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)
    return json.loads(response.text);


# 安全验证-领取奖励
def reward_init(device_id, captcha_token, captcha_sign, timestamp, aliyungf_tc, user_agent, client_id):
    url = "https://user.mypikpak.com/v1/shield/captcha/init"

    payload = {
        "client_id": client_id,
        "action": "POST:/vip/v1/activity/rewardVip",
        "device_id": device_id,
        "captcha_token": captcha_token,
        "meta": {
            "captcha_sign": "1." + captcha_sign,
            "client_version": "1.4.6",
            "package_name": "mypikpak.com",
            "timestamp": timestamp
        }
    }
    headers = {
        "authority": "user.mypikpak.com",
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5",
        "content-type": "application/json",
        "cookie": "aliyungf_tc=" + aliyungf_tc,
        "origin": "chrome-extension://jkmnnedinolbhjcibbfpdlkmmibkcbgf",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "none",
        "user-agent": user_agent,
        "x-client-id": client_id,
        "x-protocol-version": "301",
        "x-sdk-version": "5.2.0",
        "Accept-Encoding": "deflate, gzip"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)
    return json.loads(response.text);


# 领取奖励
def reward(access_token, aliyungf_tc, user_agent, device_id, captcha_token):
    url = "https://api-drive.mypikpak.com/vip/v1/activity/rewardVip"

    payload = {
        "type": "install_web_pikpak_extension",
        "data": {}
    }
    headers = {
        "authority": "api-drive.mypikpak.com",
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5",
        "authorization": "Bearer " + access_token,
        "content-type": "application/json",
        "cookie": "aliyungf_tc=" + aliyungf_tc,
        "origin": "chrome-extension://jkmnnedinolbhjcibbfpdlkmmibkcbgf",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "none",
        "user-agent": user_agent,
        "x-captcha-token": captcha_token,
        "x-device-id": device_id,
        "Accept-Encoding": "deflate, gzip"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)


# 运行程序
def start(email, password):
    # 模拟设备基本配置
    client_id1 = "YUMx5nI8ZU8Ap8pm"
    client_id2 = "Ypcug64Odf8hwuKB"
    device_id = str(uuid.uuid4()).replace("-", "")
    user_agent = get_user_agent()
    # 开始模拟请求
    captcha_token = login_init(client_id1, device_id, email, user_agent)["captcha_token"]
    login_data = get_login(email, password, client_id1, device_id, user_agent, captcha_token)
    access_token = login_data["access_token"]
    code = get_authorize(client_id2, device_id, access_token, user_agent)["code"]
    token = get_token(code, client_id2, user_agent)
    access_token = token['access_token']
    aliyungf_tc = str(uuid.uuid4()).replace("-", "") + str(uuid.uuid4()).replace("-", "")
    timestamp = "1694680977127"
    # timestamp = str(int(time.time()) * 1000)
    str1 = client_id2 + "1.4.6mypikpak.com" + device_id + timestamp
    captcha_sign = get_sign(str1)
    captcha_token = reward_init(device_id, captcha_token, captcha_sign, timestamp, aliyungf_tc, user_agent, client_id2)[
        'captcha_token']
    reward(access_token, aliyungf_tc, user_agent, device_id, captcha_token)


if __name__ == "__main__":
    
    print("COPYRIGHT@纸鸢花的花语，程序仅供交流学习，请勿用于商业用途。")
    print("@Eoyz369 | 适配青龙使用 ")
    print("该程序为自动完成PIKPAK安装拓展任务而写，所以每个账号只有一次机会，但不掉。")
    
    while 1:
        email =os.getenv("pikpakNAME")        
        password = os.getenv("pikpakPWD")
        start(email, password)
        break
