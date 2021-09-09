#!python3.6
# Copyright (c) The University of Tokyo and
# National Institute for Materials Science (NIMS). All rights reserved.
# This document may not be reproduced or transmitted in any form,
# in whole or in part, without the express written permission of
# the copyright owners.
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
import logging.config
import socket
if sys.version_info[0] <= 2:
    import ConfigParser
    #from urlparse import urlparse
else:
    import configparser
    #from urllib.parse import urlparse
import threading

logging.config.fileConfig("./logging.conf")
#logger = logging.getLogger("__name__")
logfile = logging.getLogger("apis")             # 通常のログファイル
execlogfile = logging.getLogger("exec")         # 実行情報ログファイル

app = flask.Flask(__name__)
 
lock = threading.Lock()          # セマフォ
calc_informations = {}           # CalcInfomationを格納する
#remote_site_ids = ["nims-dev", "u-tokyo-enokiLab", "uacj", "ihi", "kobelco"]
remote_site_ids = []
# 遠隔側で実行可能なコマンドの辞書(遠隔サイトIDをキーに、コマンドのリスト)
#valid_commands = {"nims-dev":["/opt/mi-remote/abaqus.sh",],
#                  "u-tokyo-enokiLab":[],
#                  "uacj":[],
#                  "ihi":[],
#                  "kobelco":[]}
valid_commands = {}
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
                log_print(3, flask.request.remote_addr, "[check_dict] delete calc info(%s). no calc allow over 30 minutus after"%item)
                #del calc_informations[item]
                delete_keys.append(item)
                continue
            if calc_informations[item]["calc_status"] == "not start": # 遠隔実行されていない
                log_print(3, flask.request.remote_addr, "[check_dict] delete calc info(%s). no remote calc over 30 minutus after"%item)
                #del calc_informations[item]
                delete_keys.append(item)
                continue

    # リスト化されたキーを取り出して、辞書から削除
    for item in delete_keys:
        delete_calc_information(item)

#---------------------------------------
def delete_calc_information(accept_id):
    '''
    accept_idの情報を削除する。
    '''

    del calc_informations[accept_id]
    
#---------------------------------------
def log_print(loglevel, from_url, mes):
    '''
    ログ出力
    '''

    #print(message)
    try:
        loglevel = int(loglevel)
    except:
        loglevel = 4

    if loglevel == 0:           # critical
        message = "%s CRITICAL [%s] %s"%(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), from_url, mes)
        logfile.critical(message)
    elif loglevel == 1:         # error
        message = "%s ERROR [%s] %s"%(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), from_url, mes)
        logfile.error(message)
    elif loglevel == 2:         # warning
        message = "%s WARNING [%s] %s"%(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), from_url, mes)
        logfile.warning(message)
    elif loglevel == 3:         # info
        message = "%s INFO [%s] %s"%(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), from_url, mes)
        logfile.info(message)
    elif loglevel == 4:         # debug
        message = "%s DEBUG [%s] %s"%(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), from_url, mes)
        logfile.debug(message)

    logfile.handlers[0].flush()

#---------------------------------------
def check_accept_id_in_requestbody(api_url):
    '''
    request body内のaccept_idのチェックを行う
    '''
        
    log_print(4, flask.request.remote_addr, "[/%s] checking accept_id key in requestbody."%api_url)
    #print("start check_accept_id function")
    #print(flask.request.data)
    # request bodyにaccept_idが無い
    if flask.request.is_json is False:
        log_print(1, flask.request.remote_addr, "[/%s] is not json (checking requestbody)."%api_url)
        message = {"message":"The Request body is not json format?", "code":400}
        return False, response
    if ("accept_id" in flask.request.get_json(force=True)) is False:
        log_print(1, flask.request.remote_addr, "[/%s] There is no accept_id key in request body."%api_url)
        response = {"message":"There is no accept id_key in equest body", "code":400}
        return False, response
    else:

        log_print(4, flask.request.remote_addr, "[/%s] found accept_id key in requestbody ok."%api_url)
        accept_id = flask.request.get_json().get("accept_id")
    log_print(4, flask.request.remote_addr, "[/%s] check accept_id key in requestbody ok."%api_url)

    return True, accept_id

#---------------------------------------
def check_id_in_requestargs(key, api_url):
    '''
    request args内のaccept_idのチェックを行う
    '''
        
    log_print(4, flask.request.remote_addr, "[/%s] checking %s in request args."%(api_url, key))
    # request bodyにkeyが無い
    key_id = flask.request.args.get(key)
    if key_id is None:
        log_print(1, flask.request.remote_addr, "[/%s] There is no key(%s) in request args."%(api_url, key))
        response = {"message":"There is no key(%s) in equest args"%key, "code":400}
        return False, response

    # request bodyにkeyはあるが、からっぽ
    if key_id == "":
        log_print(1, flask.request.remote_addr, "[/%s] There is no value for key(%s) in request args."%(api_url, key))
        response = {"message":"There is no value for key(%s) in equest args"%key, "code":400}
        return False, response

    return True, key_id

#---------------------------------------
def check_accept_id(accept_id, api_url):
    '''
    内部データ内のaccept_idの確認を行う。
    '''

    # 内部データにaccept_idの情報が無い（未登録か、30分ルールで削除されたか
    log_print(4, flask.request.remote_addr, "[/%s] checking accept id."%api_url)
    if (accept_id in calc_informations) is False:
        log_print(1, flask.request.remote_addr, "[/%s] There is no date related accept_id(%s) in internal dictionary."%(api_url, accept_id))
        response = {"message":"There is no data related accept id(%s) in internal dictionary"%accept_id, "code":400}
        return False, response

    log_print(4, flask.request.remote_addr, "[/%s] check accept id qualified"%api_url)
    #print("end check_accept_id function")
    return True, accept_id

#---------------------------------------
def make_api_response(response_text, token="", status_code=200):
    '''
    api-gwへのresponseを作成して、返却する。
    '''

    response = flask.make_response(flask.jsonify(response_text), status_code)
    #response.headers['Authorization'] = 'Bearer %s'%token
    response.headers['Authorization'] = token

    return response

#---------------------------------------
def get_valid_commands():
    '''
    登録済みのコマンドであるかどうかの情報読み込み
    '''

    global remote_site_ids
    global valid_commands

    valid_commands = {}

    # iniファイルの読み込み
    parser = configparser.ConfigParser()
    inifilename = "./mi_distributed_computing_assist.ini"
    if os.path.exists(inifilename) is True:
        parser.read(inifilename)
    # 許可サイトの読み込み
    if parser.has_section("RemoteSites") is True:
        remote_site_ids = parser.get("RemoteSites", "remote_site_ids").split()
    print("remote servers")
    for server in remote_site_ids:
        print("  %s"%server)
        if parser.has_section(server) is True:
            valid_commands[server] = []
            commands = parser.get(server, "commands").split()
            for command in commands:
                valid_commands[server].append(command)

#==================== デバッグ用 ===========================
@app.route("/%s/get-calcinfo"%BASE_URL)
def get_calcinfo():
    '''
    登録済みの計算情報一覧
    '''

    # 登録情報の確認（時間超過を判定）
    check_dict()

    #return flask.make_response(flask.jsonify(calc_informations))
    return(make_api_response(calc_informations))

#==================== 対MIシステムのAPI ====================
@app.route("/%s/add-calcinfo"%BASE_URL, methods=['POST'])
def add_calcinfo():
    '''
    計算の登録
    '''

    global remote_site_ids
    global valid_commands

    # JSONから取り出し。
    #token = flask.request.headers.get("Authorization")
    #print(flask.request.headers)
    if ("calc-info" in flask.request.get_json()) is False:
        message = {"message":"no command entry", "code":400}
        log_print(1, flask.request.remote_addr, "[/add-calcinfo] no command entry from MI system when calculation data regist.")
        return(make_api_response(message, status_code=400))
        #return flask.make_response(flask.jsonify(response), 400)

    calc_info = flask.request.get_json().get("calc-info")
    # 遠隔サイトの確認
    site_id = None
    if ("remote-site" in calc_info) is True:
        for site in remote_site_ids:
            if site == calc_info["remote-site"]:
                site_id = site
        if site_id is None:
            message = {"message":"missmatch remote-site id", "code":"400"}
            log_print(1, flask.request.remote_addr, "[/add-calcinfo] missmatch remote-site id")
            return(make_api_response( message, status_code=400 ))
    else:
        message = {"message":"no remote-site id", "code":400}
        log_print(1, flask.request.remote_addr, "[/add-calcinfo] no remote-site id")
        return(make_api_response(message, status_code=400))

    # チェック中はvalid_commandsの作り直し禁止
    lock.acquire()
    # 最新の適正コマンドリストの読み込み
    get_valid_commands()

    # コマンドの確認
    command_name = None
    if ("command" in calc_info) is True:
        for site_command in valid_commands[site_id]:
            if site_command == calc_info["command"]:
                command_name = site_command
        if command_name is None:
            message = {"message":"invalid command name(%s)"%calc_info["command"], "code":401}
            log_print(1, flask.request.remote_addr, "[/add-calcinfo] invalid command entry(%s)"%calc_info["command"])
            #return flask.make_response(flask.jsonify(response), 401)
            lock.release()
            return(make_api_response(message, status_code=400))
    else:
        message = {"message":"no command entry", "code":400}
        log_print(1, flask.request.remote_addr, "[/add-calcinfo] no command entry")
        #return flask.make_response(flask.jsonify(response),400)
        lock.release()
        return(make_api_response(message, status_code=400))

    lock.release()

    # パラメータとファイルの確認
    # ToDO:

    # 登録
    new_accept_id = str(uuid.uuid4())
    if (new_accept_id in calc_informations) is True:
        message = {"message":"duplicate uuid", "code":400}
        log_print(1, flask.request.remote_addr, "[/add-calcinfo] duplicate accept_id has been established.")
        #return flask.make_response(flask.jsonify(response), 400)
        return(make_api_response(message, status_code=400))

    # 登録情報の確認（時間超過を判定）
    check_dict()

    calc_informations[new_accept_id] = {}
    calc_informations[new_accept_id]["calc-info"] = flask.request.get_json().get("calc-info")
    calc_informations[new_accept_id]["accept_time"] = datetime.datetime.now()
    calc_informations[new_accept_id]["wait_allow"] = "none"
    calc_informations[new_accept_id]["calc_status"] = "not start"
    #calc_informations[new_accept_id]["result_files"] = {}
    message = {"message":"calc info successfully added", "code":200, "accept_id":"%s"%new_accept_id}
    log_print(3, flask.request.remote_addr, "[/add-calcinfo] registerd calc info with accept_id(%s)"%new_accept_id)

    #return flask.jsonify(response)
    return(make_api_response(message))

#---------------------------------------
@app.route("/%s/allow-wait-calc"%BASE_URL, methods=['POST'])
def allow_wait_calc():
    '''
    待ち受けを許可される。
    '''

    # accept_id他のチェック
    retval, accept_id = check_accept_id_in_requestbody("allow-wait-calc")
    if retval is False:
        #return flask.make_response(flask.jsonify(accept_id), 400)
        return(make_api_response(accept_id, status_code=400))

    retval, message = check_accept_id(accept_id, "aalow-wait-calc")
    if retval is False:
        return(make_api_response(message, status_code=400))

    message = {"accept_id":accept_id}
    calc_status = calc_informations[accept_id]["calc_status"]
    wait_allow = calc_informations[accept_id]["wait_allow"]

    # 既に計算が開始している
    if calc_status != "not start":
        log_print(1, flask.request.remote_addr, "[/allow-wait-calc] cannot wait allow. calcuration have been started at the remote. accept_id(%s)"%accept_id)
        message = {"message":"calcuration have been started at the remote. accept_id(%s)"%accept_id, "code":401}
        #return flask.make_response(flask.jsonify(response), 401)
        return(make_api_response(message, status_code=400))

    # すでにallow-wait-calcしている
    if wait_allow != "none":
        log_print(1, flask.request.remote_addr, "[/allow-wait-calc] already wait calcurate. accept_id(%s)"%accept_id)
        message = {"message":"already wait calcurate. accept_id(%s)"%accept_id, "code":401}
        #return flask.make_response(flask.jsonify(response), 401)
        return(make_api_response(message, status_code=400))

    # Wait開始登録
    calc_informations[accept_id]["wait_allow"] = datetime.datetime.now()

    message = {"message":"successfully reqeust(start waiting calcurate)", "code":200}
    #return flask.jsonify(response)
    return(make_api_response(message))

#---------------------------------------
@app.route("/%s/cancel-wait-calc"%BASE_URL, methods=['POST'])
def cancel_wait_calc():
    '''
    待ち受けをキャンセルする
    '''

    # accept_id他のチェック
    retval, accept_id = check_accept_id_in_requestbody("cancel-wait-calc")
    if retval is False:
        return(make_api_response(accept_id, status_code=400))

    retval, message = check_accept_id(accept_id, "cancel-wait-calc")
    if retval is False:
        return(make_api_response(accept_id, status_code=400))

    message = {"accept_id":accept_id}
    calc_status = calc_informations[accept_id]["calc_status"]
    wait_allow = calc_informations[accept_id]["wait_allow"]

    # Force Deleteかどうかの判定
    force_delete = False
    if ("delete" in flask.request.get_json()) is True:
        if flask.request.get_json().get("delete") == "force":
            force_delete = True

    if force_delete is False:
        # 既に計算が開始しているまたは計算が終了して、結果も取得済み(got return)
        if calc_status != "not start" and calc_start != "got return" and calc_start != "abnormal-end":
            log_print(1, flask.request.remote_addr, "[/cancel-wait-calc] cannot cancel. calcuration have been started at the remote. (status = %s / accept_id = %s)"%(calc_status, accept_id))
            message = {"message":"calcuration have been started at the remote. (status = %s / accept_id = %s)"%(calc_status, accept_id), "code":401}
            #return flask.make_response(flask.jsonify(response), 401)
            return(make_api_response(message, status_code=400))
    
        # まだallow waitしていない
        if wait_allow == "none":
            log_print(1, flask.request.remote_addr, "[/cancel-wait-calc] cannot cancel. calcuration have not been allow-wait. accept_id(%s)"%accept_id)
            message = {"message":"calcuration have not been allow-wait. accept_id(%s)"%accept_id, "code":401}
            #return flask.make_response(flask.jsonify(response), 401)
            return(make_api_response(message, status_code=400))

    # 指定されたaccept_idの情報を削除する。
    delete_calc_information(accept_id)

    message = {"message":"successfully cancel wait(delete calculation information for accept_id(%s))"%accept_id, "code":200}
    #return flask.jsonify(response)
    return(make_api_response(message))

#---------------------------------------
@app.route("/%s/calc-status"%BASE_URL, methods=['GET'])
def calc_status():
    '''
    accept_idの計算の状況を返す。
    '''

    # accept_id他のチェック
    retval, accept_id = check_id_in_requestargs("accept_id", "calc-status")
    if retval is False:
        return(make_api_response(accept_id, status_code=400))

    # accept_idのデータがあるか？
    if (accept_id in calc_informations) is False:
        log_print(1, flask.request.remote_addr, "[/status] There is no information about the id(%s)"%accept_id)
        message = {"message":"There is no information about the id(%s)"%accept_id, "code":400}
        return(make_api_response(message))

    log_print(3, flask.request.remote_addr, "[/status] status:%s"%calc_informations[accept_id]["calc_status"])
    status = {"message":"status:%s"%calc_informations[accept_id]["calc_status"], "code":200}
    #return flask.jsonift(status)
    return(make_api_response(status))

#---------------------------------------
@app.route("/%s/get-calc-result"%BASE_URL, methods=['GET'])
def get_calc_result():
    '''
    accept_idの計算結果を返す。
    '''

    # accept_id他のチェック
    retval, accept_id = check_id_in_requestargs("accept_id", "get-calc-result")
    if retval is False:
        return(make_api_response(accept_id, status_code=400))

    # accept_idのデータがあるか？
    if (accept_id in calc_informations) is False:
        log_print(3, flask.request.remote_addr, "[/status] There is no information about the id(%s)"%accept_id)
        message = {"message":"There is no information about the id(%s)"%accept_id, "code":400}
        return(make_api_response(message))

    infor = calc_informations[accept_id]

    # デーが返却可能かの個別チェック
    calc_status = calc_informations[accept_id]["calc_status"]
    # 計算が終わって、ファイルが戻ってきていない。
    if calc_status == "got return":
        pass
    else:
        log_print(2, flask.request.remote_addr, "[/get-calc-result] calc can not return(status = %s / accept_id = %s)"%(calc_status, accept_id))
        message = {"message":"calc can not return(status = %s / accept_id = %s)"%(calc_status, accept_id), "code":400}
        return(make_api_response(message, status_code=400))

    # 指定されたaccept_idの情報を削除する。
    delete_calc_information(accept_id)

    # 返却データの組み立て
    result = {}
    result["result-info"] = {}
    result["result-info"]["result_files"] = infor["calc-info"]["result_files"]

    message = {"message":"", "code":200, "result-info":result["result-info"]}
    return(make_api_response(message))

#==================== 対遠隔計算環境のAPI ====================
def check_accept_remote_side_id(accept_id, site_id, url_id):
    '''
    遠隔側の要求確認（accept id)
    '''

    global remote_site_ids

    # site_idの確認
    is_site_id = (site_id in remote_site_ids)

    # 識別子未登録
    if is_site_id is False:
        log_print(1, flask.request.remote_addr, "[/%s] Your site-id(%s) does not match in the list that acceptable to."%(url_id, site_id))
        message = {"message":"Your site-id(%s) does not match in the list that acceptable to."%site_id, "code":"400"}
        return False, message

    # accept_idの確認
    if (accept_id in calc_informations) is False:
        log_print(2, flask.request.remote_addr, "[/%s] There is no information for accept_id(%s), about the your site-id(%s)"%(url_id, accept_id, site_id))
        message = {"errors":[{"code":"0400","message":"There is no information for accept_id(%s), about the your site id(%s)"%(accept_id, site_id)}]}
        return False, message

    # 待ち受け開始していない
    if calc_informations[accept_id]["wait_allow"] == "none":
        log_print(2, flask.request.remote_addr, "[/%s] There is no information which can calc(no wait allow), about the your site-id(%s)"%(url_id, site_id))
        message = {"message":"There is no information which can calc(no wait allow), about the your site id(%s)"%site_id, "code":"400"}
        return False, message

    return True, None

#---------------------------------------
def check_site_id_in_requestbody(api_url):
    '''
    site_idの確認
    '''
    if ("site_id" in flask.request.get_json()) is False:
        log_print(1, flask.request.remote_addr, "[/%s] There is no site_id in request body."%api_url)
        response = {"message":"There is no site id in equest body", "code":400}
        return False, response
    else:
        site_id = flask.request.get_json().get("site_id")

    return True, site_id

#---------------------------------------
@app.route("/%s/calc-request"%BASE_URL, methods=['GET'])
def calc_request():
    '''
    計算の有無、問い合わせ
    '''

    # site_id他のチェック
    retval, site_id = check_id_in_requestargs("site_id", "calc-request")
    if retval is False:
        return(make_api_response(site_id, status_code=400))

    # site_idのデータがあるか？
    accept_id = None
    for item in calc_informations:
        if calc_informations[item]["calc-info"]["remote-site"] == site_id:
            if calc_informations[item]["calc_status"] == "not start":
                accept_id = item
                break;                              # 最初の一つ目を返す

    # site_id/accept_idのチェック 
    ret, message = check_accept_remote_side_id(accept_id, site_id, "calc-request")
    if ret is False:
        return(make_api_response(message, status_code=400))

    # 計算未登録
    if accept_id is None:
        log_print(1, flask.request.remote_addr, "[/calc-request] There is no information about the your site-id(%s)"%site_id)
        message = {"message":"There is no information about the your site id(%s)"%site_id, "code":401}
        return(make_api_response(message))


    infor = {}
    infor[accept_id] = calc_informations[accept_id]["calc-info"]
    log_print(3, flask.request.remote_addr, "[/calc-request] return information")
    message = {"message":"There is information that can calc", "code":200, "accept_id":accept_id}
    return(make_api_response(message))

#---------------------------------------
@app.route("/%s/calc-params"%BASE_URL, methods=['GET'])
def calc_params():
    '''
    パラメータの取得要求
    '''

    # site_id他のチェック
    retval, site_id = check_id_in_requestargs("site_id", "calc-params")
    if retval is False:
        message = site_id
        return(make_api_response(message, status_code=400))

    retval, accept_id = check_id_in_requestargs("accept_id", "calc-params")
    if retval is False:
        message = accept_id
        return(make_api_response(message, status_code=400))

    ret, message = check_accept_remote_side_id(accept_id, site_id, "calc-params")

    if ret is False:
        return(make_api_response(message, status_code=400))

    # 待ち受け中かの確認
    url_id = "calc-params"
    if calc_informations[accept_id]["calc_status"] == "not start":
        pass
    else:
        log_print(3, flask.request.remote_addr, "[/%s] There is no information which can calc(no calc wating), about the your site-id(%s)"%(url_id, site_id))
        message = {"message":"There is no information which can calc(no calc wating), about the your site id(%s)"%site_id, "code":200}
        return(make_api_response(message))

    log_print(3, flask.request.remote_addr, "[/calc-params] return information")
    #message = {"message":"There is information that can calc", "code":200, "accept_id":accept_id}
    message = {}
    message["calc-info"] = calc_informations[accept_id]["calc-info"]
    calc_informations[accept_id]["calc_status"] = "sending params"
    return(make_api_response(message))

#---------------------------------------
@app.route("/%s/calc-params-complete"%BASE_URL, methods=['POST'])
def calc_params_complete():
    '''
    パラメータ取得完了通知
    '''

    # accept_id他のチェック
    retval, accept_id = check_accept_id_in_requestbody("calc-params-complete")
    if retval is False:
        #return flask.make_response(flask.jsonify(accept_id), 400)
        return(make_api_response(accept_id, status_code=400))

    # site_id
    ret, site_id = check_site_id_in_requestbody("calc-params-complet")
    if ret is False:
        message = site_id
        return(make_api_response(message, status_code=400))

    # 対象か？
    ret, message = check_accept_remote_side_id(accept_id, site_id, "calc-params-complete")
    if ret is False:
        return(make_api_response(message, status_code=400))

    # パラメータ送信中かの確認
    url_id = "calc-params-complete"
    if calc_informations[accept_id]["calc_status"] == "sending params":
        pass
    else:
        log_print(3, flask.request.remote_addr, "[/%s] There is no information which can calc(no params sending), about the your site-id(%s)"%(url_id, site_id))
        message = {"message":"There is no information which can calc(no params sending), about the your site id(%s)"%site_id, "code":200}
        return(make_api_response(message))

    calc_informations[accept_id]["calc_status"] = "complete send"
    message = {"message":"ok", "code":200}
    return(make_api_response(message))

#---------------------------------------
@app.route("/%s/calc-start"%BASE_URL, methods=['POST'])
def calc_start():
    '''
    計算開始の通知
    '''

    # accept_id他のチェック
    retval, accept_id = check_accept_id_in_requestbody("calc-start")
    if retval is False:
        #return flask.make_response(flask.jsonify(accept_id), 400)
        return(make_api_response(accept_id, status_code=400))

    # site_id
    ret, site_id = check_site_id_in_requestbody("calc-start")
    if ret is False:
        message = site_id
        return(make_api_response(message, status_code=400))

    ret, message = check_accept_remote_side_id(accept_id, site_id, "calc-start")

    if ret is False:
        return(make_api_response(message, status_code=400))

    # パラメータ送信完了しているかの確認
    url_id = "calc-start"
    if calc_informations[accept_id]["calc_status"] == "complete send":
        pass
    else:
        log_print(1, flask.request.remote_addr, "[/%s] There is no information which can calc(no complete send), about the your site-id(%s)"%(url_id, site_id))
        message = {"message":"There is no information which can calc(no complete send), about the your site id(%s)"%site_id, "code":400}
        return(make_api_response(message))

    calc_informations[accept_id]["calc_status"] = "running"
    message = {"message":"ok", "code":200}
    return(make_api_response(message))

#---------------------------------------
@app.route("/%s/calc-end"%BASE_URL, methods=['POST'])
def calc_end():
    '''
    遠隔計算機から計算の終了通知
    '''

    # accept_id他のチェック
    retval, accept_id = check_accept_id_in_requestbody("calc-end")
    if retval is False:
        #return flask.make_response(flask.jsonify(accept_id), 400)
        return(make_api_response(accept_id, status_code=400))

    # site_id
    ret, site_id = check_site_id_in_requestbody("calc-end")
    if ret is False:
        message = site_id
        return(make_api_response(message, status_code=400))

    ret, message = check_accept_remote_side_id(accept_id, site_id, "calc-end")

    if ret is False:
        return(make_api_response(message, status_code=400))

    url_id = "calc-end"

    # 計算実行開始しているかの確認
    if calc_informations[accept_id]["calc_status"] == "running":
        pass
    else:
        log_print(3, flask.request.remote_addr, "[/%s] There is no information which can calc(no calc running), about the your site-id(%s)"%(url_id, site_id))
        message = {"message":"There is no information which can calc(no calc running), about the your site id(%s)"%site_id, "code":200}
        return(make_api_response(message))

    # bodyのresultキーの確認
    if ("result" in flask.request.get_json()) is False:
        log_print(1, flask.request.remote_addr, "[/%s] There is no 'result' key in request body"%url_id)
        message = {"message":"There is no 'result' key in request body", "code":401}
        return(make_api_response(message, status_code=400))

    result = flask.request.get_json()['result']

    if result != "calc end" and result != "abnormal":
        log_print(1, flask.request.remote_addr, "[/%s] unknown calc status(%s)"%(url_id, result))
        message = {"message":"unknown calc status(%s)"%result, "code":402}
        return(make_api_response(message, status_code=400))

    calc_informations[accept_id]["calc_status"] = result
    message = {"message":"ok", "code":200}
    return(make_api_response(message))

#---------------------------------------
@app.route("/%s/send-results"%BASE_URL, methods=['POST'])
def send_results():
    '''
    遠隔計算機から計算結果の送信
    '''

    log_print(3, flask.request.remote_addr, "[/send-results] recirving result file(s)")
    # accept_id他のチェック
    retval, accept_id = check_accept_id_in_requestbody("send-results")
    if retval is False:
        #return flask.make_response(flask.jsonify(accept_id), 400)
        return(make_api_response(accept_id, status_code=401))

    log_print(4, flask.request.remote_addr, "リクエストボディ内のaccept_id check ok")

    # site_id
    ret, site_id = check_site_id_in_requestbody("send-results")
    if ret is False:
        message = site_id
        return(make_api_response(message, status_code=401))

    log_print(4, flask.request.remote_addr, "リクエストボディ内のsite_id check ok")

    ret, message = check_accept_remote_side_id(accept_id, site_id, "send-results")
    if ret is False:
        return(make_api_response(message, status_code=401))

    log_print(4, flask.request.remote_addr, "site_id 受付check ok")

    url_id = "calc-end"

    # 計算終了、計算結果返送待ちか？
    if calc_informations[accept_id]["calc_status"] == "calc end":
        pass
    else:
        log_print(1, flask.request.remote_addr, "[/%s] There is no information which can recieve(no calc end), about the your site-id(%s)"%(url_id, site_id))
        message = {"message":"There is no information which can recieve(no calc end), about the your site id(%s)"%site_id, "code":401}
        return(make_api_response(message))

    log_print(4, flask.request.remote_addr, "計算終了して返送まちのチェックOK")
    # bodyのresult_filesキーの確認
    if ("result_files" in flask.request.get_json()) is False:
        log_print(1, flask.request.remote_addr, "[/%s] There is no 'result_files' key in request body"%url_id)
        message = {"message":"There is no 'result_files' key in request body", "code":401}
        return(make_api_response(message, status_code=401))

    result_files = flask.request.get_json()['result_files']

    calc_informations[accept_id]['calc-info']["result_files"] = result_files
    calc_informations[accept_id]["calc_status"] = "getting return"
    message = {"message":"ok", "code":200}
    log_print(3, flask.request.remote_addr, "[/send-results] recirved result file(s)")
    return(make_api_response(message))
    
#---------------------------------------
@app.route("/%s/end-send"%BASE_URL, methods=['POST'])
def end_send():
    '''
    遠隔計算機からの計算結果送信終了通知
    '''

    # accept_id他のチェック
    retval, accept_id = check_accept_id_in_requestbody("end-send")
    if retval is False:
        #return flask.make_response(flask.jsonify(accept_id), 400)
        return(make_api_response(accept_id, status_code=400))

    # site_id
    ret, site_id = check_site_id_in_requestbody("end-send")
    if ret is False:
        message = site_id
        return(make_api_response(message, status_code=400))

    ret, message = check_accept_remote_side_id(accept_id, site_id, "end-send")
    if ret is False:
        return(make_api_response(message, status_code=400))

    url_id = "calc-end"

    # 計算終了、計算結果返送待ちか？
    calc_status = calc_informations[accept_id]["calc_status"]
    if calc_status == "calc end" or calc_status == "getting return":
        pass
    else:
        log_print(1, flask.request.remote_addr, "[/%s] There is no information which can recieve end(no calc end or recieving), about the your site-id(%s)"%(url_id, site_id))
        message = {"message":"There is no information which can recieve end(no calc end or recieving), about the your site id(%s)"%site_id, "code":401}
        return(make_api_response(message))

    # bodyのresultキーの確認
    if ("result" in flask.request.get_json()) is False:
        log_print(1, flask.request.remote_addr, "[/%s] There is no 'result' key in request body"%url_id)
        message = {"message":"There is no 'result' key in request body", "code":401}
        return(make_api_response(message, status_code=400))

    result = flask.request.get_json()['result']

    if result != "end send":
        log_print(1, flask.request.remote_addr, "[/%s] unknown string in end-send body"%url_id)
        message = {"message":"unknown string(%s) in end-send body"%result}
        return(make_api_response(message, status_code=401))

    calc_informations[accept_id]["calc_status"] = "got return"
    message = {"message":"ok", "code":200}
    return(make_api_response(message))

#==================== API 開始 ====================
# パラメータ
param_len = len(sys.argv)
#print("paramlen = %d / params = %s"%(param_len, sys.argv))

# 開始点
if __name__ == "__main__":

    # パラメータ
    param_len = len(sys.argv)
    #print("paramlen = %d / params = %s"%(param_len, sys.argv))

    ipaddress = "127.0.0.1"
    port_num = "50000"
    #if param_len == 3:
    #    ipaddress = sys.argv[1]
    #    port_num = sys.argv[2]
    #    print("%s: set listen ipaddress to %s"%(datetime.datetime.now(), ipaddress))
    #    print("%s: set listen port number to %s"%(datetime.datetime.now(), port_num))
    #else:
    #    print("%s: not define listen ip or port. exit"%datetime.datetime.now())
    #    sys.exit(1)

    # iniファイルの読み込み
    parser = configparser.ConfigParser()
    inifilename = "./mi_distributed_computing_assist.ini"
    if os.path.exists(inifilename) is True:
        parser.read(inifilename)
#    # 許可サイトの読み込み
    get_valid_commands()                           # 初回読み込み
#    if parser.has_section("RemoteSites") is True:
#        remote_site_ids = parser.get("RemoteSites", "remote_site_ids").split()
#    print("remote servers")
#    for server in remote_site_ids:
#        print("  %s"%server)
#        if parser.has_section(server) is True:
#            valid_commands[server] = []
#            commands = parser.get(server, "commands").split()
#            for command in commands:
#                valid_commands[server].append(command)
#
#    print("%15s : commands"%"server")
#    for item in valid_commands:
#        print("%15s : %s"%(item, valid_commands[item]))
    # 待ち受けアドレスとポート番号
    if parser.has_section("Server") is True:
        if parser.has_option("Server", "ipaddress") is True:
            ipaddress = parser.get("Server", "ipaddress")
        if parser.has_option("Server", "portnumber") is True:
            port_num = parser.get("Server", "portnumber")

    print("Waiting IPaddress / Port Number")
    print("      %s / %s"%(ipaddress, port_num))
    app.config["JSON_AS_ASCII"] = False
    for item in app.config:
        print("%s : %s"%(item, app.config[item]))
    app.jinja_env.add_extension('jinja2.ext.loopcontrols')
    app.debug = True
    app.run(host=ipaddress, port=port_num, threaded=True)
