# 南京邮电大学校园网自动登陆程序

## setting.json

1. 设置自己的账号密码
2. 设置运营商，选项：
  - ChinaNet
  - CMCC
  - School

Example:
```json
{
    "username": "Bxxxxxxxx",
    "passwd": "xxxxxx",
    "operators": "ChinaNet"
}
```

## error.log

  - 发生登录失败，打开error.log则可以查看错误日志
  - error.log中复制打开发生错误时的网址，即可查看发生错误的具体原因
  - 这些网址属于校园内网，在物理连接没有问题的情况下，可以直接打开

你可以将main.exe创建快捷方式后，将快捷方式复制到 C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp 目录下使其开机自动启动
