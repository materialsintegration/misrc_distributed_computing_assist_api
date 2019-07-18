#!python3.6
# -*- coding: utf-8 -*-

'''
MIシステム用に分散型計算環境を補助するAPI群
'''

from flask import Flask, request, render_template, redirect, url_for
import urllib.request
import json
import sys, os
import datetime
from mi_dicomapi_infomations import *

app = Flask(__name__)
 
calc_informations = []           # CalcInfomationを格納する

#-------------------- 対MIシステムのAPI --------------------
@app.route("add-calcinfo", method=['POST'])
def add_calcinfo():
    '''
    計算の登録
    
    '''

@app.route("allow-wait-calc", method=['POST'])
def allow_wait_calc():
    '''
    待ち受けを許可される。
    '''

@app.route("cancel-wait-calc", method=['POST'])
def cancel_wait_calc():
    '''
    待ち受けをキャンセルする
    '''

@app.route("status", method=['GET'])
def status():
    '''
    accept_idの計算の状況を返す。
    '''

@app.route("get-calc-result", method=['GET'])
def get_calc_result():
    '''
    accept_idの計算結果を返す。
    '''

#-------------------- 対遠隔計算環境のAPI --------------------
@app.route("calc-request", method=['GET'])
def calc_request():
    '''
    計算の有無、問い合わせ
    '''

@app.route("calc-params", method=['GET'])
def calc_params():
    '''
    パラメータの取得要求
    '''

@app.route("calc-params-comlete", method=['POST'])
def calc_params_complete():
    '''
    パラメータ取得完了通知
    '''

@app.route("calc-start", method=['POST'])
def calc_start():
    '''
    計算開始の通知
    '''

@app.route("calc=end", method=['POST'])
def calc_end():
    '''
    遠隔計算機から計算の終了通知
    '''

@app.route("send-results", method=['POST'])
def send_results():
    '''
    遠隔計算機から計算結果の送信
    '''

@app.route("end-send", method=['POST'])
def end_send():
    '''
    遠隔計算機からの計算結果送信終了通知
    '''

# パラメータ
param_len = len(sys.argv)
#print("paramlen = %d / params = %s"%(param_len, sys.argv))

# 開始点
if __name__ == "__main__":

    # パラメータ
    param_len = len(sys.argv)
    #print("paramlen = %d / params = %s"%(param_len, sys.argv))

    if param_len == 3:
        BASE_URL = sys.argv[1]
        docserver = sys.argv[2]
        print("%s: set BASE_URL to %s"%(datetime.datetime.now(), BASE_URL))
        print("%s: set document server name to %s"%(datetime.datetime.now(), docserver))
    else:
        print("%s: not define BASE_URL for sso server or document server name. exit"%datetime.datetime.now())
        sys.exit(1)

    app.jinja_env.add_extension('jinja2.ext.loopcontrols')
    app.debug = True
    app.run()
