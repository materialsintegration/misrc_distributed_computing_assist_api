#!python3.6
# -*- coding: utf-8 -*-

'''
MIシステム用に分散型計算環境を補助するAPI群から計算を取得するプログラム
'''

import requests
import json
import base64
import time
import datetime
import subprocess
import sys, os
import signal
import urllib3

# トークン取得のためのログイン
def getToken(baseurl):
    '''
    @param baseurl(string) e.g. nims.mintsys.jp
    @retval token(string)
    '''

    if ("AUTHENTICATION_OPERATOR" in os.environ) is False:
        print("ログイン用ライブラリのインストール先を設定する環境変数（AUTHENTICATION_OPERATOR）の定義がありません。")
        sys.exit(1)
    if os.path.exists(os.environ["AUTHENTICATION_OPERATOR"]) is False:
        print("ログイン用ライブラリがありません（%s）"%os.environ["AUTHENTICATION_OPERATOR"])
        sys.exit(1)
    sys.path.append(os.environ["AUTHENTICATION_OPERATOR"])
    from openam_operator import openam_operator

    uid, token = openam_operator.miLogin(baseurl)

    if uid is None:
        print("ログインに失敗しました")
        sys.exit(1)

    return token


class timeout_object(object):
    '''
    タイムアウト時にrequestsのレスポンスオブジェクトと似たような振る舞いをするオブジェクト
    '''

    def __init__(self):
        '''
        コンストラクタ

        '''
        self.status_code = None
        self.text = "Timeout"

class connection_error_object(object):
    '''
    接続エラーのための擬似応答オブジェクト
    '''

    def __init__(self):
        '''
        コンストラクタ

        '''
        self.status_code = 500
        self.text = ""


class mi_remote(object):
    '''
    APIデバッグ、GUI版
    '''

    def __init__(self, siteId, baseUrl, token, retry_count=5, retry_interval=10, timeout=None):
        '''
        初期化
        @param siteId (string)
        @param baseUrl (string)
        @param token (string) APIアクセストークン（MIntシステム発行）
        @param retry_count (int) APIアクセス失敗時のリトライ回数
        @param retry_interval (float) APIアクセス失敗時のリトライ間隔
        '''

        #self.headers={'Authorization': 'Bearer 13bedfd69583faa62be240fcbcd0c0c0b542bc92e1352070f150f8a309f441ed', 'Content-Type': 'application/json'}
        self.headers={'Authorization': 'Bearer %s'%token, 'Content-Type': 'application/json', 'Accept': 'application/json'}
        self.session = requests.Session()

        #self.base_url = "https://dev-u-tokyo.mintsys.jp/mi-distcomp-api"
        self.base_url = baseUrl + "/mi-distcomp-api"
        self.site_id = siteId
        self.accept_id = None
        self.command_result = None
        self.calc_info = None
        self.stop_flag = False
        self.debug_print = False
        self.retry_count = retry_count
        self.retry_interval = retry_interval
        self.timeout = timeout
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, signum, frame):
        '''
        '''

        if signum == 2:         # ctrl + C
            print("Ctrl + C スクリプト停止要求受付。。。")
            self.stop_flag = True

    def apiAccess(self, method, weburl, headers=None, json=None):
        '''
        APIアクセスを一括で管理（アクセス失敗をリトライカウントとリトライ間隔で）
        @param weburl (string)
        @param headers (dict/json) リクエストヘッダ
        @param json (dict/json) リクエストボディ
        @retval 応答ボディ(requests.response)
        '''

        retry_count = self.retry_count
        retry_interval = self.retry_interval
        invdata = params = None
        timeout = self.timeout
        session = self.session
        while True:
            sessionError = True
            if self.stop_flag is True:
                break
            if method == "get":
                try:
                    res = session.get(weburl, data=invdata, headers=headers, timeout=timeout)
                    sessionError = False
                except requests.ConnectTimeout:
                    res = timeout_object()
                    res.text = "サーバーに接続できませんでした（timeout = %s秒)"%timeout[0]
                except requests.ReadTimeout:
                    res = timeout_object()
                    res.text = "サーバーから応答がありませんでした（timeout = %s秒)"%timeout[1]
                except requests.ConnectionError as e:
                    res = connection_error_object()
                    res.text = "%sによりURL(%s)に接続できませんでした。"%(e, weburl)
                except urllib3.exceptions.MaxRetryError as e:
                    res = connection_error_object()
                    res.text = "%sによりURL(%s)に接続できませんでした。"%(e, weburl)
            elif method == "post":
                try:
                    res = session.post(weburl, headers=headers, json=json, timeout=timeout)
                    sessionError = False
                except requests.ConnectTimeout:
                    res = timeout_object()
                    res.text = "サーバーに接続できませんでした（timeout = %s秒)"%timeout[0]
                except requests.ReadTimeout:
                    res = timeout_object()
                    res.text = "サーバーから応答がありませんでした（timeout = %s秒)"%timeout[1]
                except requests.ConnectionError as e:
                    res = connection_error_object()
                    res.text = "%sによりURL(%s)に接続できませんでした。"%(e, weburl)
                except urllib3.exceptions.MaxRetryError as e:
                    res = connection_error_object()
                    res.text = "%sによりURL(%s)に接続できませんでした。"%(e, weburl)
            elif method == "put":
                try:
                    res = session.put(weburl, headers=headers, json=json, timeout=timeout)
                    sessionError = False
                except requests.ConnectTimeout:
                    res = timeout_object()
                    res.text = "サーバーに接続できませんでした（timeout = %s秒)"%timeout[0]
                except requests.ReadTimeout:
                    res = timeout_object()
                    res.text = "サーバーから応答がありませんでした（timeout = %s秒)"%timeout[1]
                except requests.ConnectionError as e:
                    res = connection_error_object()
                    res.text = "%sによりURL(%s)に接続できませんでした。"%(e, weburl)
                except urllib3.exceptions.MaxRetryError as e:
                    res = connection_error_object()
                    res.text = "%sによりURL(%s)に接続できませんでした。"%(e, weburl)
            if sessionError is True:
                if retry_count != 0:
                    sys.stderr.write("%s:%s%s 秒後に再接続します。(リトライ回数（%d))\n"%(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), res.text, retry_interval, retry_count))
                    sys.stderr.flush()
                else:
                    sys.stderr.write("%s:%s%d 回の再接続に失敗しました。終了します。\n"%(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), res.text, retry_count))
                    sys.stderr.flush()
                    if res.status_code is not None:
                        res.status_code = 500
                    break
                retry_count -= 1
                time.sleep(self.retry_interval)
            else:
                break

        return res

    def check_directory_in_filename(self, filename):
        '''
        ファイル名に含まれるディレクトリの確認。なければ作る。
        @param filename(string)
        @retval なし
        '''

        items = filename.split("/")
        if len(items) == 1:             # ディレクトリ指定は無と判断
            return

        current = os.getcwd()
        item_len = len(items) - 1
        for i in range(item_len):

            if os.path.exists(items[i]) is False:
                os.mkdir(items[i])
                os.chdir(items[i])

        os.chdir(current)

    def result_out(self, ret):
        '''
        レスポンスの表示
        '''

        if self.debug_print is False:
            return

        print("status code:%d"%ret.status_code)
        if ret.status_code != 200 and ret.status_code != 201:
            print("error ?:%s"%ret.text)
        else:
            items = ret.json()
            if ("calc-info" in items) is True:
                if ("parameter_files" in items["calc-info"]) is True:
                    for item in items["calc-info"]["parameter_files"]:
                        items["calc-info"]["parameter_files"][item][0] = "paramtere file contents..."

            #print(json.dumps(ret.json(), indent=2, ensure_ascii=False))
            print(json.dumps(items, indent=2, ensure_ascii=False))

    def apiCalcRequest(self):
        '''
        calc-request APIの実行
        '''

        if self.request_status is not False:
            print("%s:send request %s/calc-request?site_id=%s"%(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), self.base_url, self.site_id))
        if self.debug_print is True:
            print("%s:header = %s"%(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), str(self.headers)))
        #ret = self.session.get("%s/calc-request?site_id=%s"%(self.base_url, self.site_id), headers=self.headers)
        ret = self.apiAccess("get", "%s/calc-request?site_id=%s"%(self.base_url, self.site_id), headers=self.headers)

        if ret.status_code >= 400:
            print("%s:status code = %s / reason = %s"%(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), ret.status_code, ret.text))
            self.accept_id = None
            return False

        #print("status_code = %s(%s)"%(ret.status_code, ret.text))
        if self.request_status is not False:
            print("code = %s / message = %s"%(ret.json()["errors"][0]["code"], ret.json()["errors"][0]["message"]))
        #self.result_out(ret)
        if ("errors" in ret.json()) is True:
            if ret.json()["errors"][0]["code"] == 200:
                self.accept_id = ret.json()["errors"][0]["accept_id"]
        
        if self.accept_id is None:
            return False

        return True
    
    def apiCalcParams(self):
        '''
        calc-params APIの実行
        '''

        print("%s:send request %s/calc-params?accept_id=%s&site_id=%s"%(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), self.base_url, self.accept_id, self.site_id))
        #ret = self.session.get("%s/calc-params?accept_id=%s&site_id=%s"%(self.base_url, self.accept_id, self.site_id), headers=self.headers)
        ret = self.apiAccess("get", "%s/calc-params?accept_id=%s&site_id=%s"%(self.base_url, self.accept_id, self.site_id), headers=self.headers)

        #print("code = %s / message = %s"%(ret.json()["code"], ret.json()["message"]))
        if self.debug_print is True:
            self.result_out(ret)
        if ("errors" in ret.json()) is True:
            if ret.json()["errors"][0]["code"] != 200:
                self.accept_id = None
                return False

        self.calc_info = ret.json()
        return True
    
    def apiCalcParamsComplete(self):
        '''
        calc-params-complete APIの実行
        '''

        data = {}
        data['accept_id'] = self.accept_id
        data['site_id'] = self.site_id

        print("%s:send request %s/calc-params-complete"%(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), self.base_url))
        #ret = self.session.post("%s/calc-params-complete"%self.base_url, headers=self.headers, json=data)
        ret = self.apiAccess("post", "%s/calc-params-complete"%self.base_url, headers=self.headers, json=data)

        print("code = %s / message = %s"%(ret.json()["errors"][0]["code"], ret.json()["errors"][0]["message"]))
        #self.result_out(ret)
        if ("errors" in ret.json()) is True:
            if ret.json()["errors"][0]["code"] != 200:
                self.accept_id = None
                return False

        return True
    
    def apiCalcStart(self):
        '''
        calc-start APIの実行
        '''

        data = {}
        data['accept_id'] = self.accept_id
        data['site_id'] = self.site_id

        print("%s:send request %s/calc-start"%(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), self.base_url))
        #ret = self.session.post("%s/calc-start"%self.base_url, headers=self.headers, json=data)
        ret = self.apiAccess("post", "%s/calc-start"%self.base_url, headers=self.headers, json=data)

        print("code = %s / message = %s"%(ret.json()["errors"][0]["code"], ret.json()["errors"][0]["message"]))
        #self.result_out(ret)
        if ("errors" in ret.json()) is True:
            if ret.json()["errors"][0]["code"] != 200:
                self.accept_id = None
                return False

        # 計算ディレクトリの変更
        os.mkdir("/tmp/%s"%self.accept_id)
        os.chdir("/tmp/%s"%self.accept_id)

        # ファイルの取り出し
        for filename in self.calc_info["calc-info"]["parameter_files"]:
            #self.check_directory_in_filename(filename)
            filename = filename.split("/")[-1]              # ディレクトリ名を取り払ったファイル名のみ取り出し
            mime_type0 = self.calc_info["calc-info"]["parameter_files"][filename][1]
            mime_type1 = self.calc_info["calc-info"]["parameter_files"][filename][2]
            if mime_type1 == "charset=utf-8" or mime_type1 == "charset=us-ascii":
                print("ファイル名(%s) をアスキーファイルとして取り出し、保存しました"%filename)
                try:
                    outfile = open(filename, "w")
                except:
                    print("ファイル生成に失敗しました(ファイル名：%s）"%filename)
                    return False

                outfile.write(base64.b64decode(self.calc_info["calc-info"]["parameter_files"][filename][0]).decode("utf-8"))
                outfile.close()
            else:
                print("ファイル名(%s) をバイナリファイルとして取り出し、保存しました"%filename)
                try:
                    outfile = open(filename, "bw")
                except:
                    print("ファイル生成に失敗しました(ファイル名：%s）"%filename)
                    return False

                outfile.write(base64.b64decode(self.calc_info["calc-info"]["parameter_files"][filename][0].encode()))
                outfile.close()

        # コマンド名取り出し
        command_name = self.calc_info["calc-info"]["command"]
        parameters = self.calc_info["calc-info"]["parameters"]

        print("計算中...")
        # コマンド実行
        p = subprocess.Popen(command_name, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        stdout_data = p.stdout.read().decode("utf-8").split("\n")
        stderr_data = p.stderr.read().decode("utf-8").split("\n")

        # 標準出力
        outfile = open("計算標準出力.txt", "w")
        for item in stdout_data:
            outfile.write("%s\n"%item)
        outfile.close()
        # 標準エラー
        outfile = open("計算標準エラー出力.txt", "w")
        for item in stderr_data:
            outfile.write("%s\n"%item)
        outfile.close()

        #print(stdout_data)
        #result = stdout_data.decode("utf-8").split("\n")[0]
        result = p.returncode
        print("実行結果（%s）"%result)
        if result != 0:
            print("コマンド異常終了？")
            self.command_result = 1
            return False
        else:
            self.command_result = 0

        return True
    
    def apiCalcEnd(self, status="calc end"):
        '''
        calc-end APIの実行
        '''

        data = {}
        data['accept_id'] = self.accept_id
        data['site_id'] = self.site_id
        if self.command_result != 0:
            data['result'] = "abnormal"
            # 標準出力
            #if os.path.exists("計算標準出力.txt", "rb") is True:
            #    infile = open("計算標準出力.txt", "rb")
            #    contents = infile.read()
            #    data['stdout'] = {'exists':'yes'}
            #    data['stdout']["content"] = base64.b64encode(contents).decode('utf-8')
            #    infile.close()
            #else:
            #    data['stdout'] = {'exists':'no'}
            # 標準出力
            #if os.path.exists("計算標準エラー出力.txt") is True:
            #    infile = open("計算標準エラー出力.txt", "rb")
            #    contents = infile.read()
            #    data['stdout'] = {'exists':'yes'}
            #    data['stderr']["content"] = base64.b64encode(contents).decode('utf-8')
            #    infile.close()
            #else:
            #    data['stderr'] = {'exists':'no'}
        else:
            data['result'] = status
            #data['stdout'] = {'exists':'no'}
            #data['stderr'] = {'exists':'no'}

        print("%s:send request %s/calc-end"%(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), self.base_url))
        ret = self.session.post("%s/calc-end"%self.base_url, headers=self.headers, json=data)
        ret = self.apiAccess("post", "%s/calc-end"%self.base_url, headers=self.headers, json=data)

        #self.result_out(ret)
        if ("errors" in ret.json()) is True:
            print("code = %s / message = %s"%(ret.json()["errors"][0]["code"], ret.json()["errors"][0]["message"]))
            if ret.json()["errors"][0]["code"] != 200:
                self.accept_id = None
                return False

        return True
    
    def apiSendResult(self):
        '''
        send-result APIの実行
        '''

        data = {}
        data['accept_id'] = self.accept_id
        data['site_id'] = self.site_id
        data['result_files'] = {}

        # 計算ディレクトリ
        os.chdir("/tmp/%s"%self.accept_id)
        
        # 返すべきファイルの取得
        for filename in self.calc_info["calc-info"]["result_files"]:
            # ファイルの種類を特定
            data['result_files'][filename] = self.calc_info["calc-info"]["result_files"][filename]
            if os.path.exists(filename) is False:
                print("出力指定ファイル(%s)がありませんでした。"%filename)
                data['result_files'][filename]["mimetype1"] = "Error"
                data['result_files'][filename]["mimetype2"] = "出力指定ファイル(%s)がありませんでした。"%filename

            else:
                p = subprocess.Popen("file -b -i %s"%filename, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                p.wait()
                stdout_data = p.stdout.read()
                print("filename(%s) is %s"%(filename, stdout_data))
                result = stdout_data.decode("utf-8").split("\n")[0]
                results = result.split()
                mime_types = results[0].split("/")
    
                infile = open(filename, "rb")
                contents = infile.read()
                data['result_files'][filename]["content"] = base64.b64encode(contents).decode('utf-8')
                data['result_files'][filename]["mimetype1"] = results[0]
                data['result_files'][filename]["mimetype2"] = results[1]
                print("filename(%s) size is %d"%(filename, len(base64.b64encode(contents).decode('utf-8'))))
             
                infile.close()

        #data['result_files']["XX.dat"] = "yyy"
        if self.debug_print is True:
            print(json.dumps(data, indent=2, ensure_ascii=False))

        print("%s:send request %s/send-results"%(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), self.base_url))
        #ret = self.session.post("%s/send-results"%self.base_url, headers=self.headers, json=data)
        ret = self.apiAccess("post", "%s/send-results"%self.base_url, headers=self.headers, json=data)

        if ret.status_code >= 500 or ret.status_code == 400 or ret.status_code == 401:
            print("%s:status code = %s / reason = %s"%(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), ret.status_code, ret.text))
            #self.accept_id = None
            return False

        #self.result_out(ret)
        try:
            if ("errors" in ret.json()) is True:
                print("code = %s / message = %s"%(ret.json()["errors"][0]["code"], ret.json()["errors"][0]["message"]))
                if ret.json()["errors"][0]["code"] != 200:
                    #self.accept_id = None
                    return False
        except:
            print("%s:status code = %s / reason = %s"%(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), ret.status_code, ret.text))
            return False

        return True
        
    def apiEndSend(self):
        '''
        end-send APIの実行
        '''

        data = {}
        data['accept_id'] = self.accept_id
        data['site_id'] = self.site_id
        data['result'] = "end send"

        print("%s:send request %s/end-send"%(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), self.base_url))
        #ret = self.session.post("%s/end-send"%self.base_url, headers=self.headers, json=data)
        ret = self.apiAccess("post", "%s/end-send"%self.base_url, headers=self.headers, json=data)

        #self.result_out(ret)
        if ("errors" in ret.json()) is True:
            print("code = %s / message = %s"%(ret.json()["errors"][0]["code"], ret.json()["errors"][0]["message"]))
            if ret.json()["errors"][0]["code"] != 200:
                self.accept_id = None
                return False

        return True

    def go_calc_sequence(self):
        '''
        遠隔実行のシーケンス
        '''

        print("計算情報を取得します。")
        if self.apiCalcParams() is False:
            print("エラーが発生したので、待ち受け状態に遷移します。")
            self.accept_id = None
            return
        time.sleep(10)
        print("計算情報が取得できました。")
        if self.apiCalcParamsComplete() is False:
            print("エラーが発生したので、待ち受け状態に遷移します。")
            self.accept_id = None
            return
        time.sleep(10)
        print("計算を開始します。")
        if self.apiCalcStart() is False:
            print("エラーが発生したので、送信できるファイルを送信して、待ち受け状態に遷移します。")
            self.apiCalcEnd()
            time.sleep(2.0)
            self.apiSendResult()
            time.sleep(2.0)
            self.apiEndSend()
            self.accept_id = None
            return
        print("計算終了。計算終了を通知します")
        if self.apiCalcEnd() is False:
            print("エラーが発生したので、待ち受け状態に遷移します。")
            self.accept_id = None
            return
        if self.command_result != 0:            # 異常終了時
            print("エラーが発生したので、待ち受け状態に遷移します。")
            self.accept_id = None
            return
        time.sleep(10)
        print("結果をアップロードします。")
        if self.apiSendResult() is False:
            print("エラーが発生したので、待ち受け状態に遷移します。")
            self.apiEndSend()
            time.sleep(2.0)
            self.accept_id = None
            return
        time.sleep(10)
        print("アップロード終了")
        self.apiEndSend()

        print("全行程が終了したので、待ち受け状態に遷移します。")
        self.accept_id = None
        return

def main():
    '''
    開始点
    '''

    if sys.version[0] != "3":
        print("Please run under the python version 3.6 or later. now you are executing this under the python version %s"%sys.version[0])
        sys.exit(1)

    if len(sys.argv) <= 2:
        print("python %s <site id> <base url> <token>")
        print("")
        print("Usage:")
        print("      site id : 'nims-dev', 'rme-u-tokyo', 'uacj', 'ihi' and 'kobelco'の様な識別子")
        print("      base url: MIntシステムのtop URL(e.g. https://nims.mintsys.jp or https://dev-u-tokyo.mintsys.jp)")
        print("        token : 64文字のMIntシステムのAPIへアクセスするためのトークン")
        print(len(sys.argv))
        sys.exit(1)

    debug_print = False
    retry_count = 5
    retry_interval = 60.0
    siteid = None
    token = None
    baseUrl = None
    for i in range(len(sys.argv)):
        if i == 1:
            print("site id = %s"%sys.argv[1])
            siteid = sys.argv[1]
        elif i == 2:
            print("base url = %s:50443"%sys.argv[2])
            baseUrl = sys.argv[2]
        elif i == 3:
            if sys.argv[3] == "login":
                token = getToken(baseUrl.split("//")[1])
            else:
                token = sys.argv[3]
            print(" token = %s"%token)
        elif i >= 4:
            if sys.argv[i] == "debug":
                print("debug print: yes")
                debug_print = True
            if sys.argv[i].startswith("retry") is True:
                try:
                    items = sys.argv[i].split(":")
                    items = items.split(",")
                    retry_count = int(items[0])
                    retry_interval = float(items[1])
                except:
                    pass

    api_prog = mi_remote(siteid, "%s:50443"%baseUrl, token, retry_count=retry_count, retry_interval=retry_interval)

    api_prog.request_status = None
    api_prog.debug_print = debug_print
    while True:
        if api_prog.stop_flag is True:
            break
        if api_prog.apiCalcRequest() is True:
            time.sleep(10)
            print("There is calc in MI-system by accept_id(%s)"%api_prog.accept_id)
            api_prog.go_calc_sequence()
            api_prog.request_status = None

        else:
            api_prog.request_status = False

        time.sleep(30)

if __name__ == '__main__':
    main()
