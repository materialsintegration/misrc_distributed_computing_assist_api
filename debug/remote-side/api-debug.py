#!python3.6
# -*- coding: utf-8 -*-

'''
MIシステム用に分散型計算環境を補助するAPI群へ登録を行うデバッグプログラム
'''

import requests
import json
import base64
from debug_gui import *


class api_debug(MIDistCompAPIDebugGUIForRemote):
    '''
    APIデバッグ、GUI版
    '''

    def __init__(self, parent):
        '''
        初期化
        '''

        MIDistCompAPIDebugGUIForRemote.__init__(self, parent)

        self.headers={'Authorization': 'Bearer 13bedfd69583faa62be240fcbcd0c0c0b542bc92e1352070f150f8a309f441ed', 'Content-Type': 'application/json'}
        self.data = {'calc-info': {
            'command': '/opt/mi-remote/abaqus.sh',
            'remote-site': 'nims-dev',
            'parameters':'',
            'parameter_files':{
                'XX.inp':'xxx',
                'XX.dat':'yyy'}}}
        self.session = requests.Session()

        self.base_url = "https://dev-u-tokyo.mintsys.jp/mi-distcomp-api"
        self.site_id = "nims-dev"
        self.accept_id = None

    def result_out(self, ret):
        '''
        レスポンスの表示
        '''

        print("status code:%d"%ret.status_code)
        if ret.status_code != 200 and ret.status_code != 201:
            print("error ?:%s"%ret.text)
        else:
            print(json.dumps(ret.json(), indent=2, ensure_ascii=False))

    def m_buttonCalcRequestOnButtonClick( self, event ):
        '''
        calc-request APIの実行
        '''

        ret = self.session.get("%s/calc-request?site_id=%s"%(self.base_url, self.site_id), headers=self.headers, json=self.data)

        self.result_out(ret)
        if ("code" in ret.json()) is True:
            if ret.json()["code"] == 200:
                self.accept_id = ret.json()["accept_id"]
                self.m_textCtrlCalcParams.SetValue(self.accept_id)

        event.Skip()
    
    def m_buttonCalcParamsOnButtonClick( self, event ):
        '''
        calc-params APIの実行
        '''

        accept_id = self.m_textCtrlCalcParams.GetValue()
        #if accept_id == "":
        #    return

        print("send request %s/calc-params?accept_id=%s&site_id=%s"%(self.base_url, accept_id, self.site_id))
        ret = self.session.get("%s/calc-params?accept_id=%s&site_id=%s"%(self.base_url, accept_id, self.site_id), headers=self.headers)

        self.result_out(ret)
        event.Skip()
    
    def m_buttonCalcParamsCompleteOnButtonClick( self, event ):
        '''
        calc-params-complete APIの実行
        '''

        accept_id = self.m_textCtrlCalcParamsComplete.GetValue()
        if accept_id == "":
            return

        data = {}
        data['accept_id'] = accept_id
        data['site_id'] = self.site_id

        ret = self.session.post("%s/calc-params-complete"%self.base_url, headers=self.headers, json=data)

        self.result_out(ret)
        event.Skip()
    
    def m_buttonCalcStartOnButtonClick( self, event ):
        '''
        calc-start APIの実行
        '''

        accept_id = self.m_textCtrlCalcStart.GetValue()
        if accept_id == "":
            return

        data = {}
        data['accept_id'] = accept_id
        data['site_id'] = self.site_id

        ret = self.session.post("%s/calc-start"%self.base_url, headers=self.headers, json=data)

        self.result_out(ret)
        event.Skip()
    
    def m_buttonCalcEndOnButtonClick( self, event ):
        '''
        calc-end APIの実行
        '''

        accept_id = self.m_textCtrlCalcEnd.GetValue()
        if accept_id == "":
            return

        data = {}
        data['accept_id'] = accept_id
        data['site_id'] = self.site_id
        data['result'] = "calc end"

        ret = self.session.post("%s/calc-end"%self.base_url, headers=self.headers, json=data)

        self.result_out(ret)
        event.Skip()
    
    def m_buttonSendResultOnButtonClick( self, event ):
        '''
        send-result APIの実行
        '''

        accept_id = self.m_textCtrlSendResult.GetValue()
        if accept_id == "":
            return

        data = {}
        data['accept_id'] = accept_id
        data['site_id'] = self.site_id
        data['result_files'] = {}
        data['result_files']["XX.dat"] = base64.b64encode(open("XX.dat", "rb").read()).decode('utf-8')

        ret = self.session.post("%s/send-results"%self.base_url, headers=self.headers, json=data)

        self.result_out(ret)
        event.Skip()
        
    def m_buttonEndSendOnButtonClick( self, event ):
        '''
        end-send APIの実行
        '''

        accept_id = self.m_textCtrlEndSend.GetValue()
        if accept_id == "":
            return

        data = {}
        data['accept_id'] = accept_id
        data['site_id'] = self.site_id
        data['result'] = "end send"

        ret = self.session.post("%s/end-send"%self.base_url, headers=self.headers, json=data)

        self.result_out(ret)

        event.Skip()
    
    def m_buttonClearOnButtonClick( self, event ):
        '''
        入力欄のクリア
        '''

        self.m_textCtrlCalcParams.SetValue("")
        self.m_textCtrlCalcParamsComplete.SetValue("")
        self.m_textCtrlCalcStart.SetValue("")
        self.m_textCtrlCalcEnd.SetValue("")
        self.m_textCtrlSendResult.SetValue("")
        self.m_textCtrlEndSend.SetValue("")
        event.Skip()

def main():
    '''
    開始点
    '''

    app = wx.App(False)
    org = api_debug(None)
    org.Show()

    app.MainLoop()

if __name__ == '__main__':
    main()
                               
