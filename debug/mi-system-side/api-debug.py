#!python3.6
# -*- coding: utf-8 -*-

'''
MIシステム用に分散型計算環境を補助するAPI群へ登録を行うデバッグプログラム
'''

import requests
import json
from debug_gui import *


class api_debug(MIDistCompAPIDebugGUI):
    '''
    APIデバッグ、GUI版
    '''

    def __init__(self, parent):
        '''
        初期化
        '''

        MIDistCompAPIDebugGUI.__init__(self, parent)

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

    def result_out(self, ret):
        '''
        レスポンスの表示
        '''

        print("status code:%d"%ret.status_code)
        if ret.status_code != 200 and ret.status_code != 201:
            print("error ?:%s"%ret.text)
        else:
            print(json.dumps(ret.json(), indent=2, ensure_ascii=False))

    def m_buttonAddCalcOnButtonClick( self, event ):
        '''
        add-calc APIの実行
        '''

        ret = self.session.post("%s/add-calcinfo"%self.base_url, headers=self.headers, json=self.data)

        self.result_out(ret)
        event.Skip()
    
    def m_buttonAllowWaitCalcOnButtonClick( self, event ):
        '''
        allow-wait-calc APIの実行
        '''

        accept_id = self.m_textCtrlAllowWaitCalc.GetValue()
        data = {}
        data['accept_id'] = accept_id

        ret = self.session.post("%s/allow-wait-calc"%self.base_url, headers=self.headers, json=data)

        self.result_out(ret)
        event.Skip()
    
    def m_buttonCancelWaitCalcOnButtonClick( self, event ):
        '''
        cancel-wait-calc APIの実行
        '''

        accept_id = self.m_textCtrlCancelWaitCalc.GetValue()
        data = {}
        data['accept_id'] = accept_id

        ret = self.session.post("%s/cancel-wait-calc"%self.base_url, headers=self.headers, json=data)

        self.result_out(ret)
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

        self.result_out(ret)
        event.Skip()
    
    def m_buttonGetCalcResultOnButtonClick( self, event ):
        '''
        get-calc-result APIの実行
        '''

        accept_id = self.m_textCtrlGetCalcResult.GetValue()
        data = {}
        data['accept_id'] = accept_id

        ret = self.session.get("%s/get-calc-result?accept_id=%s"%(self.base_url, accept_id), headers=self.headers, json=data)

        self.result_out(ret)
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
                               
