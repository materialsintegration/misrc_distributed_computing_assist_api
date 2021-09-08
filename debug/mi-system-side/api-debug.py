#!python3.6
# -*- coding: utf-8 -*-

'''
MIシステム用に分散型計算環境を補助するAPI群へ登録を行うデバッグプログラム
'''

import sys, os
import requests
import json
import base64
import subprocess
from debug_gui import *


class api_debug(MIDistCompAPIDebugGUI):
    '''
    APIデバッグ、GUI版
    '''

    def __init__(self, parent, baseUrl, token):
        '''
        初期化
        '''

        MIDistCompAPIDebugGUI.__init__(self, parent)

        #self.headers={'Authorization': 'Bearer 13bedfd69583faa62be240fcbcd0c0c0b542bc92e1352070f150f8a309f441ed', 'Content-Type': 'application/json'}
        self.headers={'Authorization': 'Bearer %s'%token, 'Content-Type': 'application/json'}
        self.data = {
            'calc-info':{
                'command': '/opt/mi-remote/abaqus.sh',
                'remote-site': 'nims-dev',
                'parameters':'',
                'parameter_files':{
                    'XX.inp':['xxx','','']
                },
                'result_files':{
                    'XX.dat':['xxx','',''],
                    'XX.com':['','',''],
                    'XX.msg':['','',''],
                    'XX.sta':['','',''],
                    'XX.prt':['','',''],
                    'XX.sim':['','',''],
                 #   'XX.odb':['','','']
                }
            }
        }
        self.session = requests.Session()

        #self.base_url = "https://dev-u-tokyo.mintsys.jp/mi-distcomp-api"
        self.base_url = baseUrl
        self.token = token

    def result_out(self, ret):
        '''
        レスポンスの表示
        '''

        print("status code:%d"%ret.status_code)
        if ret.status_code != 200 and ret.status_code != 201:
            print("error ?:%s"%ret.text)
        else:
            items = ret.json()
            #print(items)
            for accept_id in items:
                if ("calc-info" in items[accept_id]) is False:
                    continue
                if ("parameter_files" in items[accept_id]["calc-info"]) is True:
                    for item in items[accept_id]["calc-info"]["parameter_files"]:
                        items[accept_id]["calc-info"]["parameter_files"][item][0] = "paramtere file contents..."
                if ("result_files" in items[accept_id]) is True:
                    for item in items[accept_id]["result_files"]:
                        items[accept_id]["result_files"][item] = "return file contents..."
                
            #print(json.dumps(ret.json(), indent=2, ensure_ascii=False))
            print(json.dumps(items, indent=2, ensure_ascii=False))

    def m_buttonAddCalcOnButtonClick( self, event ):
        '''
        add-calc APIの実行
        '''

        for filename in self.data["calc-info"]["parameter_files"]:
        #self.data["calc-info"]["parameter_files"]["XX.inp"][0] = base64.b64encode(open("XX.inp", "rb").read()).decode('utf-8')
            p = subprocess.Popen("file -i -b %s"%filename, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p.wait()
            stdout_data = p.stdout.read()
            result = stdout_data.decode('utf-8').split("\n")[0]
            results = result.split()
            mime_types = results[0].split("/")
            self.data["calc-info"]["parameter_files"][filename][0] = base64.b64encode(open(filename, "rb").read()).decode('utf-8')
            self.data["calc-info"]["parameter_files"][filename][1] = results[0]
            self.data["calc-info"]["parameter_files"][filename][2] = results[1]

        ret = self.session.post("%s/add-calcinfo"%self.base_url, headers=self.headers, json=self.data)

        print("status code:%d"%ret.status_code)
        if ret.status_code != 200 and ret.status_code != 201:
            print("error ?:%s"%ret.text)
        else:
            print("accept_id = %s"%ret.json()["accept_id"])
        #self.result_out(ret)
        event.Skip()
    
    def m_buttonAllowWaitCalcOnButtonClick( self, event ):
        '''
        allow-wait-calc APIの実行
        '''

        accept_id = self.m_textCtrlAllowWaitCalc.GetValue()
        data = {}
        data['accept_id'] = accept_id

        ret = self.session.post("%s/allow-wait-calc"%self.base_url, headers=self.headers, json=data)

        print("code = %s / message = %s"%(ret.json()["code"], ret.json()["message"]))
        #self.result_out(ret)
        event.Skip()
    
    def m_buttonCancelWaitCalcOnButtonClick( self, event ):
        '''
        cancel-wait-calc APIの実行
        '''

        accept_id = self.m_textCtrlCancelWaitCalc.GetValue()
        data = {}
        data['accept_id'] = accept_id

        ret = self.session.post("%s/cancel-wait-calc"%self.base_url, headers=self.headers, json=data)

        print("code = %s / message = %s"%(ret.json()["code"], ret.json()["message"]))
        #self.result_out(ret)
        event.Skip()
    
    def m_buttonGetCalcInfoOnButtonClick( self, event ):
        '''
        get-calc-info APIの実行
        '''

        ret = self.session.get("%s/get-calcinfo"%self.base_url, headers=self.headers)

        self.result_out(ret)
        event.Skip()
    
    def m_buttonStatusOnButtonClick( self, event ):
        '''
        status APIの実行
        '''

        accept_id = self.m_textCtrlStatus.GetValue()
        data = {}
        data['accept_id'] = accept_id

        ret = self.session.get("%s/calc-status?accept_id=%s"%(self.base_url, accept_id), headers=self.headers)

        print("code = %s / message = %s"%(ret.json()["code"], ret.json()["message"]))
        #self.result_out(ret)
        event.Skip()
    
    def m_buttonGetCalcResultOnButtonClick( self, event ):
        '''
        get-calc-result APIの実行
        '''

        accept_id = self.m_textCtrlGetCalcResult.GetValue()
        data = {}
        data['accept_id'] = accept_id

        ret = self.session.get("%s/get-calc-result?accept_id=%s"%(self.base_url, accept_id), headers=self.headers, json=data)

        result = ret.json()
        if ("result-info" in result) is True:
            for filename in result["result-info"]["result_files"]:
                mime_type0 = result["result-info"]["result_files"][filename][1]
                mime_type1 = result["result-info"]["result_files"][filename][2]
                print("result file = %s(%s; %s)"%(filename, mime_type0, mime_type1))
                if mime_type1 == "charset=utf-8" or mime_type1 == "charset=us-ascii":
                    outfile = open(filename, "w")
                    outfile.write(base64.b64decode(result["result-info"]["result_files"][filename][0]).decode("utf-8"))
                    outfile.close
                else:
                    outfile = open(filename, "bw")
                    outfile.write(base64.b64decode(result["result-info"]["result_files"][filename][0].encode()))
                    outfile.close

        #self.result_out(ret)
        event.Skip()

    def m_buttonClearOnButtonClick(self, event):
        '''
        入力欄のクリア
        '''

        self.m_textCtrlGetCalcResult.SetValue("")
        self.m_textCtrlStatus.SetValue("")
        self.m_textCtrlCancelWaitCalc.SetValue("")
        self.m_textCtrlAllowWaitCalc.SetValue("")
        self.m_textCtrlForceDelete.SetValue("")
        
        event.Skip()

    def m_buttonGetUUIDsOnButtonClick( self, event ):
        '''
        登録済みのUUIDの表示
        '''

        ret = self.session.get("%s/get-calcinfo"%self.base_url, headers=self.headers)

        print("status code:%d"%ret.status_code)
        if ret.status_code != 200 and ret.status_code != 201:
            print("error ?:%s"%ret.text)
        else:
            items = ret.json()
            for item in items:
                print(item)
        
        event.Skip()

    def m_buttonForceDeleteOnButtonClick( self, event ):
        '''
        cancel-wait-calc APIの実行(Force delete)
        '''

        accept_id = self.m_textCtrlForceDelete.GetValue()
        data = {}
        data['accept_id'] = accept_id
        data['delete'] = 'force'

        ret = self.session.post("%s/cancel-wait-calc"%self.base_url, headers=self.headers, json=data)

        print("code = %s / message = %s"%(ret.json()["code"], ret.json()["message"]))
        #self.result_out(ret)
        event.Skip()
    
def main():
    '''
    開始点
    '''

    if len(sys.argv) < 3:
        print("python %s <base url> <api token>")
        print("")
        print("Usage:")
        print("      base url    : MI system top URL(e.g. https://nims.mintsys.jp or https://dev-u-tokyo.mintsys.jp)")
        print("      api token   : valid token for api access.")
        print(len(sys.argv))
        sys.exit(1)

    baseUrl = "%s:50443"%sys.argv[1]
    token = sys.argv[2]

    app = wx.App(False)
    org = api_debug(None, baseUrl, token)
    org.Show()

    app.MainLoop()

if __name__ == '__main__':
    main()
