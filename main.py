import ctypes
import json
import os
import sys

from PyQt5.QtCore import Qt, QCoreApplication, QThread
from PyQt5.QtWidgets import QMainWindow, QApplication
from win32com import client

import interface
from CampusNetwork import campusNetwork, LoginError, FileError, Operators, UserInfo


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


class LoginInfo:
    def __init__(self, user_info: UserInfo, self_start: bool, save_passwd: bool, auto_login: bool):
        self.user_info = user_info
        self.self_start = self_start
        self.save_passwd = save_passwd
        self.auto_login = auto_login


class loginThread(QThread):
    def __init__(self, login_info: LoginInfo):
        super(loginThread, self).__init__()
        self.login_info = login_info

    def run(self):
        login(self.login_info.user_info)


class loginWindow(QMainWindow, interface.Ui_Login):
    def __init__(self, login_info: LoginInfo, parent=None):
        super(loginWindow, self).__init__(parent)
        self.setupUi(self)
        self.login_info = login_info

        if self.login_info.user_info.operator == Operators.CMCC:
            self.CMCC.setChecked(Qt.Checked)
        elif self.login_info.user_info.operator == Operators.ChinaNet:
            self.ChinaNet.setChecked(Qt.Checked)
        elif self.login_info.user_info.operator == Operators.School:
            self.School.setChecked(Qt.Checked)
        else:
            raise LoginError

        self.lineEdit_username.setText(self.login_info.user_info.username)
        if self.login_info.self_start:
            self.checkBox_selfstart.setCheckState(Qt.Checked)
        if self.login_info.save_passwd:
            self.checkBox_savepasswd.setCheckState(Qt.Checked)
            self.lineEdit_passed.setText(self.login_info.user_info.passwd)
        if self.login_info.auto_login:
            self.checkBox_autologin.setCheckState(Qt.Checked)

        if not is_admin():
            self.checkBox_selfstart.setText('开机自启(请以管\n理员身份运行)')
            self.checkBox_selfstart.setEnabled(False)

        self.checkBox_selfstart.stateChanged.connect(self.self_start_changed)
        self.checkBox_savepasswd.stateChanged.connect(self.save_passed_changed)
        self.checkBox_autologin.stateChanged.connect(self.auto_login_changed)

        self.CMCC.clicked.connect(lambda: self.chose_operator(Operators.CMCC))
        self.ChinaNet.clicked.connect(lambda: self.chose_operator(Operators.ChinaNet))
        self.School.clicked.connect(lambda: self.chose_operator(Operators.School))

        self.pushButton_yes.clicked.connect(self.passwd_changed)
        self.pushButton_yes.clicked.connect(self.username_changed)
        self.pushButton_yes.clicked.connect(lambda: save_data(self.login_info))
        self.login_thread = loginThread(self.login_info)
        self.pushButton_yes.clicked.connect(self.login_thread.start)
        self.pushButton_yes.clicked.connect(lambda: self.setVisible(False))
        self.login_thread.finished.connect(QCoreApplication.instance().quit)
        self.pushButton_cancle.clicked.connect(QCoreApplication.instance().quit)

    def start_thread(self):
        self.login_thread.start()

    def auto_login_changed(self):
        self.login_info.auto_login = not self.login_info.auto_login

    def self_start_changed(self):
        self.login_info.self_start = not self.login_info.self_start
        if self.login_info.self_start:
            try:
                file_name = sys.argv[0]
                link_name = r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\CampusNetworkAutoLogin.lnk'
                shortcut = client.Dispatch("WScript.Shell").CreateShortCut(link_name)
                shortcut.TargetPath = file_name
                shortcut.save()
            except Exception as e:
                print(e.args)
        else:
            if os.path.exists(r'C:\ProgramData\Microsoft\Windows\Start '
                              r'Menu\Programs\StartUp\CampusNetworkAutoLogin.lnk'):
                os.remove(r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\CampusNetworkAutoLogin.lnk')

    def save_passed_changed(self):
        self.login_info.save_passwd = not self.login_info.save_passwd

    def passwd_changed(self):
        self.login_info.user_info.passwd = self.lineEdit_passed.text()

    def username_changed(self):
        self.login_info.user_info.username = self.lineEdit_username.text()

    def chose_operator(self, operator: Operators):
        if operator == Operators.School:
            self.login_info.user_info.operator = Operators.School
        elif operator == Operators.CMCC:
            self.login_info.user_info.operator = Operators.CMCC
        elif operator == Operators.ChinaNet:
            self.login_info.user_info.operator = Operators.ChinaNet
        else:
            raise LoginError


def save_data(login_info: LoginInfo):
    user_data = {
        'username': login_info.user_info.username,
        'passwd': login_info.user_info.passwd,
        'operator': str(login_info.user_info.operator.name),
        'self_start': login_info.self_start,
        'save_passwd': login_info.save_passwd,
        'auto_login': login_info.auto_login
    }
    with open('./setting.json', 'w') as file:
        json.dump(user_data, file, indent=4)


def login(user_info: UserInfo):
    c = campusNetwork()
    try:
        if user_info.operator == Operators.ChinaNet:
            c.login(user_info.username, user_info.passwd, Operators.ChinaNet)
        elif user_info.operator == Operators.CMCC:
            c.login(user_info.username, user_info.passwd, Operators.CMCC)
        elif user_info.operator == Operators.School:
            c.login(user_info.username, user_info.passwd, Operators.School)
        else:
            print('setting.json error')
        c.showtoast()
    except LoginError:
        c.showtoast()


def showWindow(login_info: LoginInfo):
    main_window = loginWindow(login_info)
    main_window.setVisible(True)
    main_window.show()


def str_to_operators(s: str):
    if s == 'ChinaNet':
        return Operators.ChinaNet
    elif s == 'CMCC':
        return Operators.CMCC
    elif s == 'School':
        return Operators.School
    else:
        raise FileError


if __name__ == '__main__':
    app = QApplication(sys.argv)
    if not os.path.exists('./setting.json'):
        user = {'username': '', 'passwd': '', 'operator': '', 'self_start: ': False, 'save_passwd': False,
                'auto_login': False}
        with open('./setting.json', 'w') as f:
            json.dump(user, f, indent=4)
        showWindow(LoginInfo(UserInfo('', '', Operators.School), False, False, False))
    else:
        with open('./setting.json', 'r') as f:
            user = json.load(f)
            try:
                if user['auto_login']:
                    login(UserInfo(user['username'], user['passwd'], str_to_operators(user['operator'])))
                    sys.exit(0)
                else:
                    showWindow(LoginInfo(UserInfo(user['username'], user['passwd'], str_to_operators(user['operator'])),
                                         user['self_start'], user['save_passwd'], False))
            except LoginError:
                pass
            except FileError:
                showWindow(LoginInfo(UserInfo('', '', Operators.School), False, False, False))
    sys.exit(app.exec_())
