#!python3.6
# -*- coding: utf-8 -*-

'''
MIシステム用に分散型計算環境を補助するAPI群
'''

#from flask import Flask, request, render_template, redirect, url_for, jsonify, make_response
import flask
import urllib.request
import json
import sys, os
import datetime
import uuid
from mi_dicomapi_infomations import *
import logging
from logging import config
import socket

logging.config.fileConfig("./logging.cfg")
logger = logging.getLogger("__name__")

app = flask.Flask(__name__)
 
calc_informations = {}           # CalcInfomationを格納する
remote_site_ids = ["u-tokyo-enokiLab", "uacj", "ihi", "kobelco"]
valid_commands = {}              # 遠隔側で実行可能なコマンドの辞書(遠隔サイトIDをキーに、コマンドのリスト)
BASE_URL = "mi-distcomp-api"     # ベースURL

#==================== 補助関数   ===========================
def check_dict():
    '''
    登録後30分以上経ったデータがあれば、削除する
    ToDo:現在はMIシステムからデータ受付時にここでチェックするが、定期的にしたほうがいいかも。
    '''

    delete_keys = []        # 削除対象のキーをリスト化
    for item in calc_informations:
        keikajikan = datetime.datetime.now() - calc_informations[item]["accept_time"]
        if keikajikan.total_seconds() > 1800:                   # 30分経過した
            if calc_informations[item]["wait_allow"] == "none": # 待ち受け許可発行していない
                log_print(3, "delete calc info(%s). no calc allow over 30 minutus after"%item)
                #del calc_informations[item]
                delete_keys.append(item)
                continue
            if calc_informations[item]["calc_start"] == "none": # 遠隔実行されていない
                log_print(3, "delete calc info(%s). no remote calc over 30 minutus after"%item)
                #del calc_informations[item]
                delete_keys.append(item)
                continue

    # リスト化されたキーを取り出して、辞書から削除
    for item in delete_keys:
        delete_cacl_information(item)

#---------------------------------------
def delete_calc_information(accept_id):
    '''
    accept_idの情報を削除する。
    '''

    del calc_informations[item]
    
#---------------------------------------
def log_print(loglevel, message):
    '''
    ログ出力
    '''

    try:
        loglevel = int(loglevel)
    except:
        loglevel = 0

    if loglevel == 0:           # critical
        logger.critical(message)
    elif loglevel == 1:         # error
        logger.error(message)
    elif loglevel == 2:         # warning
        logger.warning(message)
    elif loglevel == 3:         # info
        logger.info(message)
    elif loglevel == 4:         # debug
        logger.debug(message)

#---------------------------------------
def check_accept_id(api_url):
    '''
    内部データ内のaccept_idの確認を行う。
    '''
        
    # request bodyにaccept_idが無い
    if ("accept_id" in flask.request.get_json()) is False:
        log_print(1, "(/%s) There is no accept_id in request body."%api_url)
        response = {"message":"There is no accept id in equest body", "code":400}
        return False, response

    # 内部データにaccept_idの情報が無い（未登録か、30分ルールで削除されたか
    accept_id = flask.request.get_json().get("accept_id")
    log_print(3, calc_informations)
    if (accept_id in calc_informations) is False:
        log_print(1, "(/%s) There is no date related accept_id(%s) in internal dictionary."%(api_url, accept_id))
        response = {"message":"There is no data related accept id(%s) in internal dictionary"%accept_id, "code":400}
        return False, response

    return True, accept_id

#---------------------------------------
def return_api(response_text):
    '''
    api-gwへのresponseを作成して、返却する。
    '''

    response = flask.make_response(flask.jsonify(response_text))
    response.headers['Authorization'] = 'Bearer 13bedfd69583faa62be240fcbcd0c0c0b542bc92e1352070f150f8a309f441ed'

    return response

#==================== デバッグ用 ===========================
@app.route("/%s/get-calcinfo"%BASE_URL)
def get_calcinfo():
    '''
    登録済みの計算情報一覧
    '''

    #return flask.make_response(flask.jsonify(calc_informations))
    return_api(calc_informations)

#==================== 対MIシステムのAPI ====================
@app.route("/%s/add-calcinfo"%BASE_URL, methods=['POST'])
def add_calcinfo():
    '''
    計算の登録
    '''

    # JSONから取り出し。
    if ("calc-info" in flask.request.get_json()) is False:
        response = {"message":"no command entry", "code":400}
        log_print(1, "(/add-calcinfo)no command entry from MI system when calculation data regist.")
        return_api(response)
        #return flask.make_response(flask.jsonify(response), 400)

    calc_info = flask.request.get_json().get("calc-info")
    # 遠隔サイトの確認
    site_id = None
    if ("remote-site" in calc_info) is True:
        for site in remote_site_ids:
            if site == calc_info["remote-site"]:
                site_id = site
        if site_id is None:
            response = {"message":"missmatch remote-site id", "code":"400")
            log_print(1, "(/add-calcinfo)missmatch remote-site id")
            return_api( response )
    else:
        response = {"message":"no remote-site id", "code":400}
        log_print(1, "(/add-calcinfo)no remote-site id")
        return_api(response)

    # コマンドの確認
    command_name = None
    if ("command" in calc_info) is True:
        for site_command in valid_commands:
            for command in site_command[site_id]:
                if command == calc_info["command"]:
                    command_name = command
        if command_name is None:
            response = {"message":"invalid command name(%s)"%calc_info["command"], "code":401}
            log_print(1, "(/add-calcinfo)invalid command entry(%s)"%calc_info["command"])
            #return flask.make_response(flask.jsonify(response), 401)
            return_api(response)
    else:
        response = {"message":"no command entry", "code":400}
        log_print(1, "(/add-calcinfo)no command entry")
        #return flask.make_response(flask.jsonify(response),400)
        return_api(response)

    new_accept_id = str(uuid.uuid4())
    if (new_accept_id in calc_informations) is True:
        response = {"message":"duplicate uuid", "code":400}
        log_print(1, "(/add-calcinfo)duplicate accept_id has been established.")
        #return flask.make_response(flask.jsonify(response), 400)
        return_api(response)

    # 登録情報の確認（時間超過を判定）
    check_dict()

    calc_informations[new_accept_id] = flask.request.get_json().get("calc-info")
    calc_informations[new_accept_id]["accept_time"] = datetime.datetime.now()
    calc_informations[new_accept_id]["wait_allow"] = "not start"
    calc_informations[new_accept_id]["calc_start"] = "none"
    response = {"message":"calc info successfully added", "code":200, "accept_id":"%s"%new_accept_id}
    log_print(3, "(/add-calcinfo)registerd calc info with accept_id(%s)"%new_accept_id)

    #return flask.jsonify(response)
    return_api(response)

#---------------------------------------
@app.route("/%s/allow-wait-calc"%BASE_URL, methods=['POST'])
def allow_wait_calc():
    '''
    待ち受けを許可される。
    '''

    # accept_id他のチェック
    retval, accept_id = check_accept_id("allow-wait-calc")
    if retval is False:
        #return flask.make_response(flask.jsonify(accept_id), 400)
        return_api(accept_id)

    response = {"accept_id":accept_id}
    calc_start = calc_informations[accept_id]["calc_start"]
    wait_allow = calc_informations[accept_id]["wait_allow"]

    # 既に計算が開始している
    if calc_start != "not start":
        log_print(1, "(/allow-wait-calc) cannot wait allow. calcuration have been started at the remote. accept_id(%s)"%accept_id)
        response = {"message":"calcuration have been started at the remote. accept_id(%s)"%accept_id, "code":401}
        #return flask.make_response(flask.jsonify(response), 401)
        return_api(response)

    # すでにallow-wait-calcしている
    if wait_allow != "none":
        log_print(1, "(/allow-wait-calc) already wait calcurate. accept_id(%s)"%accept_id)
        response = {"message":"already wait calcurate. accept_id(%s)"%accept_id, "code":401}
        #return flask.make_response(flask.jsonify(response), 401)
        return_api(response)

    # Wait開始登録
    calc_informations[accept_id]["wait_allow"] = datetime.datetime.now()

    response = {"message":"successfully reqeust(start waiting calcurate)", "code":200}
    #return flask.jsonify(response)
    return_api(response)

#---------------------------------------
@app.route("/%s/cancel-wait-calc"%BASE_URL, methods=['POST'])
def cancel_wait_calc():
    '''
    待ち受けをキャンセルする
    '''

    # accept_id他のチェック
    retval, accept_id = check_accept_id("cancel-wait-calc")
    if retval is False:
        #return flask.make_response(flask.jsonify(accept_id), 400)
        return_api(accept_id)

    response = {"accept_id":accept_id}
    calc_start = calc_informations[accept_id]["calc_start"]
    wait_allow = calc_informations[accept_id]["wait_allow"]

    # 既に計算が開始している
    if calc_start != "not start":
        log_print(1, "(/cancel-wait-calc) cannot cancel. calcuration have been started at the remote. accept_id(%s)"%accept_id)
        response {"message":"calcuration have been started at the remote. accept_id(%s)"%accept_id, "code":401}
        #return flask.make_response(flask.jsonify(response), 401)
        return_api(response)

    # 指定されたaccept_idの情報を削除する。
    delete_calc_information(accept_id)

    response = {"message":"successfully cancel wait(delete calculation information for accept_id(%s))"%accept_id, "code":200}
    #return flask.jsonify(response)
    return_api(response)

#---------------------------------------
@app.route("/%s/status"%BASE_URL, methods=['GET'])
def status():
    '''
    accept_idの計算の状況を返す。
    '''

    # accept_id他のチェック
    retval, accept_id = check_accept_id("/status")
    if retval is False:
        #return flask.make_response(flask.jsonify(accept_id), 400)
        return_api(accept_id)

    status = {"message":"status:%s"%calc_informations[accept_id]["cacl_start"], "code":200}
    #return flask.jsonift(status)
    return_api(status)

#---------------------------------------
@app.route("/%s/get-calc-result"%BASE_URL, methods=['GET'])
def get_calc_result():
    '''
    accept_idの計算結果を返す。
    '''

#==================== 対遠隔計算環境のAPI ====================
@app.route("/%s/calc-request"%BASE_URL, methods=['GET'])
def calc_request():
    '''
    計算の有無、問い合わせ
    '''

#---------------------------------------
@app.route("/%s/calc-params"%BASE_URL, methods=['GET'])
def calc_params():
    '''
    パラメータの取得要求
    '''

#---------------------------------------
@app.route("/%s/calc-params-comlete"%BASE_URL, methods=['POST'])
def calc_params_complete():
    '''
    パラメータ取得完了通知
    '''

#---------------------------------------
@app.route("/%s/calc-start"%BASE_URL, methods=['POST'])
def calc_start():
    '''
    計算開始の通知
    '''

#---------------------------------------
@app.route("/%s/calc-end"%BASE_URL, methods=['POST'])
def calc_end():
    '''
    遠隔計算機から計算の終了通知
    '''

#---------------------------------------
@app.route("/%s/send-results"%BASE_URL, methods=['POST'])
def send_results():
    '''
    遠隔計算機から計算結果の送信
    '''

#---------------------------------------
@app.route("/%s/end-send"%BASE_URL, methods=['POST'])
def end_send():
    '''
    遠隔計算機からの計算結果送信終了通知
    '''

#==================== API 開始 ====================
# パラメータ
param_len = len(sys.argv)
#print("paramlen = %d / params = %s"%(param_len, sys.argv))

# 開始点
if __name__ == "__main__":

    # パラメータ
    param_len = len(sys.argv)
    #print("paramlen = %d / params = %s"%(param_len, sys.argv))

    ip_address = "127.0.0.1"
    port_num = "50000"
    if param_len == 3:
        ip_address = sys.argv[1]
        port_num = sys.argv[2]
        print("%s: set listen ip_address to %s"%(datetime.datetime.now(), ip_address))
        print("%s: set listen port number to %s"%(datetime.datetime.now(), port_num))
    else:
        print("%s: not define listen ip or port. exit"%datetime.datetime.now())
        sys.exit(1)

    app.jinja_env.add_extension('jinja2.ext.loopcontrols')
    app.debug = True
    app.run(host=ip_address, port=port_num)
