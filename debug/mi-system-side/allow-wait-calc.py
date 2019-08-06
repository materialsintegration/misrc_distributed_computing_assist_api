#!python3.6
# -*- coding: utf-8 -*-

'''
MIシステム用に分散型計算環境を補助するAPI群へ登録を行うデバッグプログラム
'''

import requests
import json
import sys, os

print(len(sys.argv))
if len(sys.argv) == 1:
    print("python3.6 %s <accept_id>"%sys.argv[0])
    sys.exit(1)

accept_id = sys.argv[1]
headers={'Authorization': 'Bearer 13bedfd69583faa62be240fcbcd0c0c0b542bc92e1352070f150f8a309f441ed', 'Content-Type': 'application/json'}

data = {}
data['accept_id'] = accept_id

session = requests.Session()
ret = session.post("https://dev-u-tokyo.mintsys.jp/mi-distcomp-api/allow-wait-calc", headers=headers, json=data)

print("status code:%d"%ret.status_code)
if ret.status_code != 200 and ret.status_code != 201:
    print("error ?:%s"%ret.text)
else:
    print(json.dumps(ret.json(), indent=2, ensure_ascii=False))
