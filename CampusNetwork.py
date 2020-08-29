from requests import post
from requests import get
from win10toast import ToastNotifier
from re import findall
from enum import Enum
import requests
import win10toast


class StatusCode(Enum):
    Complete = u'登陆成功'
    E1 = u'无需重复登陆'
    E2 = u'登陆失败'


class operators(Enum):
    CMCC = '@cmcc'
    ChinaNet = '@njxy'
    School = ''


class campusNetwork:

    def __init__(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/84.0.4147.135 Safari/537.36 '
        }
        get_ip_url = 'http://10.10.244.11/'
        r = get(get_ip_url, headers=headers)
        self.ipaddress = str(findall(r"v46ip='(.+?)'", r.text)[0])
        self.statusCode = StatusCode.E2

    def login(self, username: str, passwd: str, operator: operators):
        url = 'http://10.10.244.11:801/eportal/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/84.0.4147.135 Safari/537.36 '
        }
        # 网页参数
        url_params = {
            'c': 'ACSetting',
            'a': 'Login',
            'protocol': 'http:',
            'hostname': '10.10.244.11',
            'iTermType': '1',
            # 分配给你的ip
            'wlanuserip': self.ipaddress,
            'wlanacip': '10.255.252.150',
            'wlanacname': 'XL-BRAS-SR8806-X',
            'mac': '00-00-00-00-00-00',
            # 分配给你的ip
            'ip': self.ipaddress,
            'enAdvert': '0',
            'queryACIP': '0',
            'loginMethod': '1'
        }
        # 表单信息 登陆方式取决于后缀
        # 电信：   @njxy
        # 移动：   @cmcc
        # 校园网： 无需后缀
        datas = {
            # 第三项为账号
            'DDDDD': ',0,' + username + operator.value,
            # 密码
            'upass': passwd,
            'R1': '0',
            'R2': '0',
            'R3': '0',
            'R6': '0',
            'para': '00',
            '0MKKey': '123456'
        }
        # 请求登陆
        r = post(url, data=datas, params=url_params, headers=headers)
        msg = r.url
        judge = msg.find('ErrorMsg=')
        if judge == -1:
            self.statusCode = StatusCode.Complete
        elif msg.find('ErrorMsg=Mg') >= 0:
            self.statusCode = StatusCode.E1
        else:
            self.statusCode = StatusCode.E2
            print(msg)

    def showtoast(self):
        toaster = ToastNotifier()
        try:
            toaster.show_toast(u'校园网登陆', self.statusCode.value, icon_path='D:/llq.ico', duration=-1)
        except ValueError:
            pass
