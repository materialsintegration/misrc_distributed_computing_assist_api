#!python3.6
# -*- coding: utf-8 -*-

'''
MIシステム用に分散型計算環境を補助するAPI群へ登録を行うデバッグプログラム
'''

import requests
import json

headers={'Authorization': 'Bearer 13bedfd69583faa62be240fcbcd0c0c0b542bc92e1352070f150f8a309f441ed', 'Content-Type': 'application/json'}

data = {'calc-info': {'command': '/opt/mi-remote/abaqus.sh', 'remote-site': 'nims-dev'}}

session = requests.Session()
ret = session.get("https://dev-u-tokyo.mintsys.jp/mi-distcomp-api/get-calcinfo", headers=headers)

print("status code:%d"%ret.status_code)
if ret.status_code != 200 and ret.status_code != 201:
    print("error ?:%s"%ret.text)
else:
    print(json.dumps(ret.json(), indent=2, ensure_ascii=False))
