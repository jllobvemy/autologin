# 南京邮电大学校园网自动登陆程序

- 如果需要设置开机自动启动，请以管理员身份运行程序
- 如果登录失败，则会打开错误窗口，并在error.log中存储错误链接
- 如果选中自动登录，则会根据setting.json中保存的信息直接登录，跳过图形化界面，如需要再次开启图形化界面，请将setting.json中的auto_login修改为false

## error.log
  - 发生登录失败，打开error.log则可以查看错误日志
  - error.log中复制打开发生错误时的网址，即可查看发生错误的具体原因
  - 这些网址属于校园内网，在物理连接没有问题的情况下，可以直接打开

## setting.json

> 非必要无需修改，可以在这里修改用户数据

1. 修改自己的账号密码
2. 修改运营商，选项：
  - ChinaNet
  - CMCC
  - School
3. 修改是否开机自启(true/false) 
    - 注意请在程序中修改此选项，在此处修改可能无效
4. 修改是否保存密码(true/false)
5. 修改是否自动登录(true/false)
Example:
```json
{
    "username": "Bxxxxxxxx",
    "passwd": "**********",
    "operator": "School",
    "self_start": false,
    "save_passwd": false,
    "auto_login": false
}
```
