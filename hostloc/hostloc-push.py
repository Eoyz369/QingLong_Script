# encoding=utf-8
# 修改适配青龙面板使用
# 修改作者：Eoyz369
# 开源代码: https://github.com/w2r/hostloc2tg
# license：Apache-2.0 license


import requests
import time
from urllib import parse
import telegram
from telegram import InputMediaPhoto
import os

# CHANNEL_ID为简洁模式，CHANNEL_ID_2为完整推送
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
CHANNEL_ID_2 = os.getenv("CHANNEL_ID_2")
bot = telegram.Bot(token=TOKEN)


hostloc_list = ["1", "2", "3", "4", "5", "6"]
hostloc_title = ["1", "2", "3", "4", "5", "6"]
url_1 = "https://www.hostloc.com/"
while True:
    try:
        with requests.get('https://hostloc.mjj.sale/', stream=True) as r:
            print(time.strftime("%m-%d %H:%M:%S", time.localtime()))
            for i in r.json()["new_data"][0][15:]:
                if i['主题ID'] in hostloc_list or i['主题'] in hostloc_title:
                    pass
                else:
                    hostloc_list = hostloc_list[1::]
                    hostloc_list.append(i['主题ID'])
                    hostloc_title = hostloc_title[1::]
                    hostloc_title.append(i['主题'])
                    a = "https://hostloc.com/thread-{0}-1-1.html"。format(i['主题ID'])
                    time_1 = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime())
                    # 发送内容
                    text_content = ''
                    img_url = []
                    if "论坛bug，此贴内容无法查看~" == i['主题内容']:
                        a = f"<s>{a}</s>"
                        text_content = i['主题内容']
                    elif "获取失败，请手动登陆查看！" == i['主题内容']:
                        a = a
                        text_content = i['主题内容']
                    elif type(i['主题内容']) == str:
                        text_content = i['主题内容']
                    else:
                        # 分辨图片和文字内容
                        if i['主题内容']:
                            for i1 in i['主题内容']:
                                if "trueimg" in i1:
                                    # 莫名其妙的图片
                                    if "/public/images/patch.gif" in i1 or "static/image/smiley/" in i1:
                                        pass
                                    else:
                                        img_url.append(i1.replace("trueimg", ''))
                                else:
                                    if i1 == '\r\n':
                                        pass
                                    else:
                                        text_content = text_content + i1 + '\r\n'
                        else:
                            text_content = "获取失败，请手动登陆查看！"
                        text_content = text_content[:-2]
                    # 判断是否含有图片
                    if img_url:
                        # 判断匿名贴
                        if i['发布者'] == "匿名":
                            auth = '''<a>{}</a>'''。format(i['发布者'])
                        else:
                            auth = '''<a href="{0}">{1}</a>'''。format(i['发布者链接'], i['发布者'])
                        text_tg = '主        题：' + "<b>{}</b>"。format(i['主题']。replace("&", "%26")。replace("<", "%26lt%3b")。replace(">"， "%26gt%3b")。replace("#", " ")) + '\n' + '发  布  者：' + auth + '\n' + '时        间：' + time_1 + '\n' + '内容预览：' + '''<b>{0}</b>'''.format(text_content[0:800].replace("&", "%26").replace("<", "%26lt%3b").replace(">", "%26gt%3b").replace("#", " ")) + "\n" + "直达链接： " + a
                        text_short = '主        题：' + "<b>{}</b>".format(i['主题'].replace("&", "%26").replace("<", "%26lt%3b").replace(">", "%26gt%3b")。replace("#", " ")) + '\n' + '发  布  者：' + auth + '\n' + '时        间：' + time_1 + '\n' + '内容预览：' + '''<b>{0}</b>'''.format(text_content[0:100].replace("&", "%26").replace("<", "%26lt%3b").replace(">", "%26gt%3b").replace("#", " ")) + "\n" + "直达链接： " + a
                        media_group = []
                        print(img_url)
                        for i2 in range(len(img_url)):
                            if i2 == 0:
                                media_group.append(InputMediaPhoto(img_url[i2], caption=text_tg, parse_mode=telegram.ParseMode.HTML))
                            else:
                                media_group.append(InputMediaPhoto(img_url[i2]))
                        print(text_content)
                        try:
                            bot.send_media_group(chat_id=CHANNEL_ID, media=media_group)
                            # 推送简洁内容
                            bot.send_message(chat_id=CHANNEL_ID_2, text=text_short, disable_web_page_preview=True, parse_mode=telegram.ParseMode.HTML)
                        except Exception:
                            bot.send_message(chat_id=CHANNEL_ID, text=text_tg, disable_web_page_preview=True, parse_mode=telegram.ParseMode.HTML)
                            bot.send_message(chat_id=CHANNEL_ID_2, text=text_short, disable_web_page_preview=True, parse_mode=telegram.ParseMode.HTML)

                    else:
                        if i['发布者'] == "匿名":
                            auth = '''<a>{}</a>'''.format(i['发布者'])
                        else:
                            auth = '''<a href="{0}">{1}</a>'''.format(i['发布者链接'], i['发布者'])
                        text_tg = '主        题：' + "<b>{}</b>".format(i['主题'].replace("&", "%26").replace("<", "%26lt%3b").replace(">", "%26gt%3b")。replace("#", " ")) + '\n' + '发  布  者：' + auth + '\n' + '时        间：' + time_1 + '\n' + '内容预览：' + '''<b>{0}</b>'''.format(text_content[0:800].replace("&", "%26").replace("<", "%26lt%3b").replace(">", "%26gt%3b").replace("#", " ")) + "\n" + "直达链接： " + a
                        text_short = '主        题：' + "<b>{}</b>".format(i['主题'].replace("&", "%26").replace("<", "%26lt%3b").replace(">", "%26gt%3b")。replace("#", " ")) + '\n' + '发  布  者：' + auth + '\n' + '时        间：' + time_1 + '\n' + '内容预览：' + '''<b>{0}</b>'''.format(text_content[0:100].replace("&", "%26").replace("<", "%26lt%3b").replace(">", "%26gt%3b").replace("#", " ")) + "\n" + "直达链接： " + a
                        # 推送全部内容
                        bot.send_message(chat_id=CHANNEL_ID, text=text_tg, disable_web_page_preview=True, parse_mode=telegram.ParseMode.HTML)
                        bot.send_message(chat_id=CHANNEL_ID_2, text=text_short, disable_web_page_preview=True, parse_mode=telegram.ParseMode.HTML)

    except Exception:
        print("网络错误，请稍后重试")
    time.sleep(5)
