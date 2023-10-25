# 获取token_online
参考文章[[查看](https://chinatelecomoperators.notion.site/chinatelecomoperators/ChinaUnicom-5959008dfc2a477baf90471682f770fd)]   
作者[[ChinaTelecomOperators](https://github.com/ChinaTelecomOperators/ChinaUnicom)]   

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


## 使用短信验证码登录

<aside>
⚠️ 默认操作如果无法进行短信验证码登录, 请尝试 `方式2`, 见上方 `拉文件` 中带 `方式2` 的文件

</aside>

1. 配置手机号的环境变量 `ChinaUnicom_10010v4_mobile`
2. 执行 `发送短信登录验证码`
3. 配置短信登录验证码的环境变量 `ChinaUnicom_10010v4_code`
4. 执行 `短信登录验证码登录`

运行`短信登录验证码登录`完后，查看文件的日志，里面往下翻就能找到我们需要的`token_online`   

    
## 温馨提示
<aside>
🤔 如果你要更换当前使用的账号 请自行清空所有数据(青龙清除环境变量和.dat文件) 保证无脏数据后 再使用

</aside>
