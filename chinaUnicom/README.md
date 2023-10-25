# 拉文件

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/c00b6590-947f-4e3d-b337-88da03061681/Untitled.png)

### 发送短信验证码

`ql raw https://github.com/ChinaTelecomOperators/ChinaUnicom/releases/download/Prerelease-Alpha/10010_send_sms.js`

### 短信验证码登录

`ql raw https://github.com/ChinaTelecomOperators/ChinaUnicom/releases/download/Prerelease-Alpha/10010_sms_sign.js`

<aside>
⚠️ 默认操作如果无法进行短信验证码登录, 请尝试带 `(方式2)` 的操作

</aside>

<aside>
⚠️ 经群友提醒 如果登录不了可以尝试用官方营业厅app获取短信验证码 然后进行下一步

</aside>

### 发送短信验证码(方式2)

`ql raw https://github.com/ChinaTelecomOperators/ChinaUnicom/releases/download/Prerelease-Alpha/10010_send_sms2.js`

### 短信验证码登录(方式2)

`ql raw https://github.com/ChinaTelecomOperators/ChinaUnicom/releases/download/Prerelease-Alpha/10010_sms_sign2.js`   
设置环境变量：

名称：【ChinaUnicom_10010v4_mobile】 值：1XXXXXXXXX(手机号)

【这一步填写完后，运行上面第一个文件，会发送一个验证码到你手机号，验证码输入到下面的这个值里】

名称：【ChinaUnicom_10010v4_code】 值：（这里填的是上面运行后收到的短信验证码）

【然后运行上面的第二个文件】

运行完后，查看第二个文件的日志，里面往下翻就能找到我们需要的token_online
