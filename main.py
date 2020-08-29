from CampusNetwork import campusNetwork
from CampusNetwork import operators
import json
import os

c = campusNetwork()
if not os.path.exists('./setting.json'):
    user = {'username': '', 'passwd': ''}
    with open('./setting.json', 'w') as f:
        json.dump(user, f, indent=4)
with open('./setting.json', 'r') as f:
    user = json.load(f)
    c.login(user['username'], user['passwd'], operators.ChinaNet)
    c.showtoast()
