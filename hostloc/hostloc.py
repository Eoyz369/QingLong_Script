# -*- coding: utf-8 -*-
"""
//更新时间：2023/11/12
//作者：wdvipa 
//来源: https://github.com/wdvipa/hostloc_getPoints
//支持青龙和actions定时执行
//使用方法：创建变量 名字：HostLoc 内容的写法：账号,密码  多个账号用回车键隔开
//例如: 
abcd,11111
bbbb,22222
//更新内容：支持青龙执行
//如需推送将需要的推送写入变量HostLoc_fs即可多个用&隔开
如:变量内输入push需再添加HostLoc_push变量 内容是push的token即可
cron: 2 0,9 * * *
"""
import random
import textwrap

import requests
import os
import time
import re
import json

from pyaes import AESModeOfOperationCBC
from requests import Session as req_Session

requests.urllib3.disable_warnings()

# ------------------设置-------------------
UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26'

# 初始化环境变量开头
cs = 0
ZData = "5"
ttoken = ""
tuserid = ""
push_token = ""
SKey = ""
QKey = ""
ktkey = ""
msgs = ""
datas = ""
message = ""
# 检测推送
if cs == 1:
    if "cs_HostLoc" in os.environ:
        datas = os.environ.get("cs_HostLoc")
    else:
        print('您没有输入任何信息')
        exit()
elif cs == 2:
    datas = ""
else:
    if "HostLoc_fs" in os.environ:
        fs = os.environ.get('HostLoc_fs')
        fss = fs.split("&")
        if ("tel" in fss):
            if "HostLoc_telkey" in os.environ:
                telekey = os.environ.get("HostLoc_telkey")
                telekeys = telekey.split('\n')
                ttoken = telekeys[0]
                tuserid = telekeys[1]
        if ("qm" in fss):
            if "HostLoc_qkey" in os.environ:
                QKey = os.environ.get("HostLoc_qkey")
        if ("stb" in fss):
            if "HostLoc_skey" in os.environ:
                SKey = os.environ.get("HostLoc_skey")
        if ("push" in fss):
            if "HostLoc_push" in os.environ:
                push_token = os.environ.get("HostLoc_push")
        if ("kt" in fss):
            if "HostLoc_ktkey" in os.environ:
                ktkey = os.environ.get("HostLoc_ktkey")
    if "HostLoc" in os.environ:
        datas = os.environ.get("HostLoc")
    else:
        print('您没有输入任何信息')
        exit
groups = datas.split('\n')


# 初始化环境变量结尾

class HostLocanelQd(object):
    def __init__(self, username, password, n_num):
        # Authorization
        self.username = username
        self.password = password
        self.n_num = n_num
        ##############推送渠道配置区###############
        # 酷推qq推送
        # self.ktkey = ktkey
        # Telegram私聊推送
        self.tele_api_url = 'https://api.telegram.org'
        self.tele_bot_token = ttoken
        self.tele_user_id = tuserid
        ##########################################

    # 随机生成用户空间链接
    def randomly_gen_uspace_url(self) -> list:
        url_list = []
        # 访问小黑屋用户空间不会获得积分、生成的随机数可能会重复，这里多生成两个链接用作冗余
        for i in range(12):
            uid = random.randint(10000, 50000)
            url = "https://hostloc.com/space-uid-{}.html".format(str(uid))
            url_list.append(url)
        return url_list

    # 使用Python实现防CC验证页面中JS写的的toNumbers函数
    def toNumbers(self, secret: str) -> list:
        text = []
        for value in textwrap.wrap(secret, 2):
            text.append(int(value, 16))
        return text

    # 不带Cookies访问论坛首页，检查是否开启了防CC机制，将开启状态、AES计算所需的参数全部放在一个字典中返回
    def check_anti_cc(self) -> dict:
        result_dict = {}
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        }
        home_page = "https://hostloc.com/forum.php"
        res = requests.get(home_page, headers=headers)
        aes_keys = re.findall('toNumbers\("(.*?)"\)', res.text)
        cookie_name = re.findall('cookie="(.*?)="', res.text)

        if len(aes_keys) != 0:  # 开启了防CC机制
            print("检测到防 CC 机制开启！")
            if len(aes_keys) != 3 or len(cookie_name) != 1:  # 正则表达式匹配到了参数，但是参数个数不对（不正常的情况）
                result_dict["ok"] = 0
            else:  # 匹配正常时将参数存到result_dict中
                result_dict["ok"] = 1
                result_dict["cookie_name"] = cookie_name[0]
                result_dict["a"] = aes_keys[0]
                result_dict["b"] = aes_keys[1]
                result_dict["c"] = aes_keys[2]
        else:
            pass

        return result_dict

    # 在开启了防CC机制时使用获取到的数据进行AES解密计算生成一条Cookie（未开启防CC机制时返回空Cookies）
    def gen_anti_cc_cookies(self) -> dict:
        cookies = {}
        anti_cc_status = self.check_anti_cc()

        if anti_cc_status:  # 不为空，代表开启了防CC机制
            if anti_cc_status["ok"] == 0:
                print("防 CC 验证过程所需参数不符合要求，页面可能存在错误！")
            else:  # 使用获取到的三个值进行AES Cipher-Block Chaining解密计算以生成特定的Cookie值用于通过防CC验证
                print("自动模拟计尝试通过防 CC 验证")
                a = bytes(self.toNumbers(anti_cc_status["a"]))
                b = bytes(self.toNumbers(anti_cc_status["b"]))
                c = bytes(self.toNumbers(anti_cc_status["c"]))
                cbc_mode = AESModeOfOperationCBC(a, b)
                result = cbc_mode.decrypt(c)

                name = anti_cc_status["cookie_name"]
                cookies[name] = result.hex()
        else:
            pass

        return cookies

    # 登录帐户
    def login(self, username: str, password: str) -> req_Session:
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            "origin": "https://hostloc.com",
            "referer": "https://hostloc.com/forum.php",
        }
        login_url = "https://hostloc.com/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1"
        login_data = {
            "fastloginfield": "username",
            "username": username,
            "password": password,
            "quickforward": "yes",
            "handlekey": "ls",
        }

        s = req_Session()
        s.headers.update(headers)
        s.cookies.update(self.gen_anti_cc_cookies())
        res = s.post(url=login_url, data=login_data)
        res.raise_for_status()
        return s

    # 通过抓取用户设置页面的标题检查是否登录成功
    def check_login_status(self, s: req_Session, number_c: int) -> bool:
        test_url = "https://hostloc.com/home.php?mod=spacecp"
        res = s.get(test_url)
        res.raise_for_status()
        res.encoding = "utf-8"
        test_title = re.findall("<title>(.*?)<\/title>", res.text)

        if len(test_title) != 0:  # 确保正则匹配到了内容，防止出现数组索引越界的情况
            if test_title[0] != "个人资料 -  全球主机交流论坛 -  Powered by Discuz!":
                print("第", number_c, "个帐户登录失败！")
                return False
            else:
                print("第", number_c, "个帐户登录成功！")
                return True
        else:
            print("无法在用户设置页面找到标题，该页面存在错误或被防 CC 机制拦截！")
            return False

    # 抓取并打印输出帐户当前积分
    def print_current_points(self, s: req_Session):
        test_url = "https://hostloc.com/forum.php"
        res = s.get(test_url)
        res.raise_for_status()
        res.encoding = "utf-8"
        points = re.findall("积分: (\d+)", res.text)

        if len(points) != 0:  # 确保正则匹配到了内容，防止出现数组索引越界的情况
            print("帐户当前积分：" + points[0])
            return points[0]
        else:
            print("无法获取帐户积分，可能页面存在错误或者未登录！")
        time.sleep(5)

    # 依次访问随机生成的用户空间链接获取积分
    def get_points(self, s: req_Session, number_c: int):
        if self.check_login_status(s, number_c):
            point_a = self.print_current_points(s)  # 打印账户当前积分
            url_list = self.randomly_gen_uspace_url()
            # 依次访问用户空间链接获取积分，出现错误时不中断程序继续尝试访问下一个链接
            for i in range(len(url_list)):
                url = url_list[i]
                try:
                    res = s.get(url)
                    res.raise_for_status()
                    print("访问第", i + 1, "个用户空间成功")
                    time.sleep(5)  # 每访问一个链接后休眠5秒，以避免触发论坛的防CC机制
                except Exception as e:
                    print("链接访问异常：" + str(e))
                continue
            point_b = self.print_current_points(s)  # 再次打印账户当前积分
            return "完成前积分：" + point_a + "\n    完成后积分：" + point_b + "\n    总获得积分：" + str(int(point_b) - int(point_a))
        else:
            print("请检查你的帐户是否正确！")
            return "请检查你的帐户是否正确！"

    # 打印输出当前ip地址
    def print_my_ip(self):
        api_url = "https://api.ipify.org/"
        try:
            res = requests.get(url=api_url)
            res.raise_for_status()
            res.encoding = "utf-8"
            print("当前使用 ip 地址：" + res.text)
        except Exception as e:
            print("获取当前 ip 地址失败：" + str(e))

    # Qmsg私聊推送
    def Qmsg_send(msg):
        if QKey == '':
            return
        qmsg_url = 'https://qmsg.zendee.cn/send/' + str(QKey)
        data = {
            'msg': msg,
        }
        requests.post(qmsg_url, data=data)

    # Server酱推送
    def server_send(self, msg):
        if SKey == '':
            return
        server_url = "https://sctapi.ftqq.com/" + str(SKey) + ".send"
        data = {
            'text': self.name + "HostLoc任务通知",
            'desp': msg
        }
        requests.post(server_url, data=data)

    # 酷推QQ推送
    def kt_send(msg):
        if ktkey == '':
            return
        kt_url = 'https://push.xuthus.cc/send/' + str(ktkey)
        data = ('HostLoc任务完成，点击查看详细信息~\n' + str(msg)).encode("utf-8")
        requests.post(kt_url, data=data)

    # Telegram私聊推送
    def tele_send(self, msg: str):
        if self.tele_bot_token == '':
            return
        tele_url = f"{self.tele_api_url}/bot{self.tele_bot_token}/sendMessage"
        data = {
            'chat_id': self.tele_user_id,
            'parse_mode': "Markdown",
            'text': msg
        }
        requests.post(tele_url, data=data)

    # Pushplus推送
    def pushplus_send(msg):
        if push_token == '':
            return
        token = push_token
        title = 'HostLoc任务通知'
        content = msg
        url = 'http://www.pushplus.plus/send'
        data = {
            "token": token,
            "title": title,
            "content": content
        }
        body = json.dumps(data).encode(encoding='utf-8')
        headers = {'Content-Type': 'application/json'}
        re = requests.post(url, data=body, headers=headers)
        print(re.status_code)

    def main(self):
        global msgs
        # 更新Authorization
        s = self.login(self.username, self.password)
        self.Result = self.get_points(s, self.n_num)
        message = '''⏰当前时间：{} 
        HostLoc任务通知
    ####################
    {}
    ####################
    祝您过上美好的一天！'''.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + 28800)),
                                  self.Result)
        print(message)
        msgs = msgs + '\n' + message
        return message


if __name__ == '__main__':  # 直接运行和青龙入口
    i = 0
    n = 0
    print("已设置不显示账号密码等信息")
    while i < len(groups):
        n = n + 1
        group = groups[i]
        profile = group.split(',')
        username = profile[0]
        password = profile[1]
        msgs = msgs + "第" + str(n) + "用户的签到结果"
        print("第" + str(n) + "个用户开始签到")
        session = requests.session()
        # --------------------以下非特殊情况不要动---------------------
        session.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            "origin": "https://hostloc.com",
            "referer": "https://hostloc.com/forum.php"
        }
        # --------------------以上非特殊情况不要动---------------------
        try:
            run = HostLocanelQd(username, password, n)
            run.main()
            time.sleep(5)
            i += 1
        except Exception as e:
            print("程序执行异常：" + str(e))
            print("*" * 30)
        continue
    else:
        # HostLocanelQd.server_send( msgs )
        HostLocanelQd.kt_send(msgs)
        # HostLocanelQd.Qmsg_send(HostLocanelQd.name+"\n"+HostLocanelQd.email+"\n"+ msgs)
        # HostLocanelQd.tele_send(HostLocanelQd.name+"\n"+HostLocanelQd.email+"\n"+ msgs)
        HostLocanelQd.pushplus_send(msgs)
