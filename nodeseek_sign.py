# Source: https://github.com/YYWO/NodeSeek-Signin
# 修改多账号（ 
import requests
import os


random = "true"  # 随机签到1-x鸡腿为true，固定鸡腿*5为false
Cookie = os.environ.get("NodeSeek","").split("#")  # 多个 Cookie 用 # 分隔

# Cookie = os.environ。get("NodeSeek","colorscheme=light; sortBy=postTime; session=b7763de25b59c79f2e9db0f1012a3eb2; smac=1713689135-1RDbwWQILGvESTcAzyijjj-JJXmAnu0Rgf7CzI5SwBE; cf_clearance=Jsu9DDG_vZ1F2J_g2RqKgHgZUsLsErBFOieK3DZx0aY-1715178018-1.0.1.1-pZ_6gB_m._BdzJ1.cDXYDwzN7HjYF4DppUMHO0mbww2N6cadTweqRKl8g3YRMnw6xwM3wqF3ylWPvAF4eh7PhA; hmti_=1716266953-Yv8CCoXTN0sCa-cryfDSdJTE_UzU_O7zY9UPqKVPDvoz; cf_chl_rc_m=1; cf_clearance=1ay1KsRqogBJ7VBeGvRMXXWpB6v4dBnqvOv_Ke3zLyA-1716278547-1.0.1.1-aqAk3aQ_j9RUSDYE44nOFVmtQn3FqGxbbSIRREKHkACUg5q0_igEl_rZeKhkfSiH1IRQKvRaAYB67EpRuW4Z1A")
pushplus_token = os.environ.get("PUSHPLUS_TOKEN")
telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN","")
chat_id = os.environ.get("CHAT_ID","")
telegram_api_url = os.environ.get("TELEGRAM_API_URL","https://api.telegram.org") # 代理api,可以使用自己的反代
def telegram_Bot(token,chat_id,message):
    url = f'{telegram_api_url}/bot{token}/sendMessage'
    data = {
        'chat_id': chat_id,
        'text': message
    }
    r = requests.post(url, json=data,verify=False)
    response_data = r.json()
    msg = response_data['ok']
    print(f"telegram推送结果：{msg}\n")
def pushplus_ts(token, rw, msg):
    url = 'https://www.pushplus.plus/send/'
    data = {
        "token": token,
        "title": rw,
        "content": msg
    }
    r = requests.post(url, json=data,verify=False)
    msg = r.json().get('msg', None)
    print(f'pushplus推送结果：{msg}\n')

if Cookie:
    url = f"https://www.nodeseek.com/api/attendance?random={random}"
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
        'sec-ch-ua': "\"Not A(Brand\";v=\"99\", \"Microsoft Edge\";v=\"121\", \"Chromium\";v=\"121\"",
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': "\"Windows\"",
        'origin': "https://www.nodeseek.com",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://www.nodeseek.com/board",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        'Cookie': Cookie
    }

    try:
        response = requests.post(url, headers=headers,verify=False)
        response_data = response.json()
        print(response_data)
        message = response_data.get('message')
        success = response_data.get('success')
        
        if success == "true":
            print(message)
            if telegram_bot_token and chat_id:
                telegram_Bot(telegram_bot_token, chat_id, message)
        else:
            print(message)
            if telegram_bot_token and chat_id:
                telegram_Bot(telegram_bot_token, chat_id, message)
            if pushplus_token:
                pushplus_ts(pushplus_token, "nodeseek签到", message)
    except Exception as e:
        print("发生异常:", e)
        print("实际响应内容:", response.text)
else:
    print("请先设置Cookie")
