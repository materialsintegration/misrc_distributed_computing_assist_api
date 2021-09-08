#!python3.6
# -*- coding: utf-8 -*-

'''
MIシステム用に分散型計算環境を補助するAPI群へ登録を行うWF側プログラム
'''

import requests
import json
import base64
import subprocess
import time
import sys, os

class mi_workflow(object):
    '''
    API WF側
    '''

    def __init__(self, siteId, baseUrl, token, command, param_files, result_files, parameters):
        '''
        初期化
        remote-site nims-dev
        command /opt/mi-remote/abaqus.sh
        '''

        #self.headers={'Authorization': 'Bearer 13bedfd69583faa62be240fcbcd0c0c0b542bc92e1352070f150f8a309f441ed', 'Content-Type': 'application/json'}
        self.headers={'Authorization': 'Bearer %s'%token, 'Content-Type': 'application/json'}
        self.data = {
            'calc-info':{
                'command': '%s'%command,
                'remote-site': '%s'%siteId,
                'parameters':'%s'%parameters,
                'parameter_files':{},
                'result_files':{}
            }
        }
        for item in param_files:
            self.data['calc-info']['parameter_files'][item] = ['','','']

        print("出力ファイルを登録します。")
        for item in result_files:
            print("ファイル名(%s)を追加します。"%item)
            self.data['calc-info']['result_files'][item] = ['','','']

        # 標準出力と標準エラーの戻り用のエントリをセットする
        self.data['calc-info']['result_files']["計算標準出力.txt"] = ['','','']
        self.data['calc-info']['result_files']["計算標準エラー出力.txt"] = ['','','']

        self.session = requests.Session()

        #self.base_url = "https://dev-u-tokyo.mintsys.jp/mi-distcomp-api"
        self.base_url = "%s/mi-distcomp-api"%baseUrl
        self.accept_id = None

    def __del__(self):
        '''
        '''

        if self.accept_id is not None:
            self.miDistApiForceDelete()

    def result_out(self, ret):
        '''
        レスポンスの表示
        '''

        print("status code:%d"%ret.status_code, flush=True)
        if ret.status_code != 200 and ret.status_code != 201:
            print("error ?:%s"%ret.text, flush=True)
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
            print(json.dumps(items, indent=2, ensure_ascii=False), flush=True)

    def miDistApiAddCalc(self):
        '''
        add-calc APIの実行
        '''

        for filename in self.data["calc-info"]["parameter_files"]:
            p = subprocess.Popen('file -i -b "%s"'%filename, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p.wait()
            stdout_data = p.stdout.read()
            result = stdout_data.decode('utf-8').split("\n")[0]
            results = result.split()
            mime_types = results[0].split("/")
            self.data["calc-info"]["parameter_files"][filename][0] = base64.b64encode(open(filename, "rb").read()).decode('utf-8')
            self.data["calc-info"]["parameter_files"][filename][1] = results[0]
            self.data["calc-info"]["parameter_files"][filename][2] = results[1]

        ret = self.session.post("%s/add-calcinfo"%self.base_url, headers=self.headers, json=self.data)

        print("status code:%d"%ret.status_code, flush=True)
        print("return contents:%s"%ret.text, flush=True)
        if ret.status_code != 200 and ret.status_code != 201:
            print("error ?:%s"%ret.text, flush=True)
            return False
        else:
            self.accept_id = ret.json()["accept_id"]
            print("accept_id = %s"%self.accept_id, flush=True)

        return True
    
    def miDistApiAllowWaitCalc(self):
        '''
        allow-wait-calc APIの実行
        '''

        data = {}
        data['accept_id'] = self.accept_id

        ret = self.session.post("%s/allow-wait-calc"%self.base_url, headers=self.headers, json=data)
        if ret.status_code != 200 and ret.status_code != 201:
            print("error ?:%s"%ret.text, flush=True)
            return False, ret.text

        code = ret.json()["code"]
        message = ret.json()["message"]
        print("code = %s / message = %s"%(code, message), flush=True)

        if code != 200:
            return False, message

        return True, message
    
    def miDistApiCancelWaitCalc(self):
        '''
        cancel-wait-calc APIの実行
        '''

        data = {}
        data['accept_id'] = self.accept_id

        ret = self.session.post("%s/cancel-wait-calc"%self.base_url, headers=self.headers, json=data)
        if ret.status_code != 200 and ret.status_code != 201:
            print("error ?:%s"%ret.text, flush=True)
            return False, ret.text

        code = ret.json()["code"]
        message = ret.json()["message"]
        print("code = %s / message = %s"%(code, message), flush=True)

        if code != 200:
            return False, message

        return True, message
    
    def miDistApiGetCalcInfo(self):
        '''
        get-calc-info APIの実行
        '''

        ret = self.session.get("%s/get-calcinfo"%self.base_url, headers=self.headers)
        if ret.status_code != 200 and ret.status_code != 201:
            print("error ?:%s"%ret.text, flush=True)
            return False, ret.text

        code = ret.json()["code"]
        message = ret.json()["message"]
        print("code = %s / message = %s"%(code, message), flush=True)

        if code != 200:
            return False, message

        return True, message
    
    def miDistApiStatus(self):
        '''
        status APIの実行
        '''

        ret = self.session.get("%s/calc-status?accept_id=%s"%(self.base_url, self.accept_id), headers=self.headers)
        if ret.status_code != 200 and ret.status_code != 201:
            print("error ?:%s"%ret.text, flush=True)
            return False, ret.text

        #print("code = %s / message = %s"%(ret.json()["code"], ret.json()["message"]))

        code = ret.json()["code"]
        message = ret.json()["message"]
        print("code = %s / message = %s"%(code, message), flush=True)
        if message == "status:abnormal":
            return False, message

        if code != 200:
            return False, message

        return True, message
    
    def miDistApiGetCalcResult(self):
        '''
        get-calc-result APIの実行
        '''

        data = {}
        data['accept_id'] = self.accept_id

        ret = self.session.get("%s/get-calc-result?accept_id=%s"%(self.base_url, self.accept_id), headers=self.headers, json=data)
        if ret.status_code != 200 and ret.status_code != 201:
            print("error ?:%s"%ret.text, flush=True)
            return False, ret.text

        code = ret.json()["code"]
        message = ret.json()["message"]
        if code != 200:
            return False, message

        result = ret.json()
        if ("result-info" in result) is True:
            for filename in result["result-info"]["result_files"]:
                filesize = len(result["result-info"]["result_files"][filename][0])
                mime_type0 = result["result-info"]["result_files"][filename][1]
                mime_type1 = result["result-info"]["result_files"][filename][2]
                if mime_type1 == "charset=utf-8;" or mime_type1 == "charset=us-ascii;":
                    outfile = open(filename, "w")
                    outfile.write(base64.b64decode(result["result-info"]["result_files"][filename][0]).decode("utf-8"))
                    outfile.close
                elif mime_type1 == "Error":
                    print(mime_type2)
                else:
                    outfile = open(filename, "bw")
                    outfile.write(base64.b64decode(result["result-info"]["result_files"][filename][0].encode()))
                    outfile.close
                print("result file = %s(size=%d / mime_type0(%s); mime_type1(%s))"%(filename, filesize, mime_type0, mime_type1), flush=True)

        #self.result_out(ret)
        #event.Skip()
        return True, message

    def miDistApiGetUUIDs(self):
        '''
        登録済みのUUIDの表示
        '''

        ret = self.session.get("%s/get-calcinfo"%self.base_url, headers=self.headers)
        if ret.status_code != 200 and ret.status_code != 201:
            print("error ?:%s"%ret.text, flush=True)
            return False, ret.text

        print("status code:%d"%ret.status_code, flush=True)
        if ret.status_code != 200 and ret.status_code != 201:
            print("error ?:%s"%ret.text, flush=True)
            return None
        else:
            items = ret.json()
            #for item in items:
            #    print(item)
            return items
        
    def miDistApiForceDelete(self):
        '''
        cancel-wait-calc APIの実行(Force delete)
        '''

        data = {}
        data['accept_id'] = self.accept_id
        data['delete'] = 'force'

        ret = self.session.post("%s/cancel-wait-calc"%self.base_url, headers=self.headers, json=data)
        if ret.status_code != 200 and ret.status_code != 201:
            print("error ?:%s"%ret.text, flush=True)
            return False, ret.text

        print("code = %s / message = %s"%(ret.json()["code"], ret.json()["message"]), flush=True)

        code = ret.json()["code"]
        message = ret.json()["message"]
        print("code = %s / message = %s"%(code, message), flush=True)

        if code != 200:
            return False, message

        return True, message
    
def main():
    '''
    開始点
    '''

    print(len(sys.argv), flush=True)
    if sys.version[0] != "3":
        print("Please run under the python version 3.6 or later. now you are executing this under the python version %s"%sys.version[0], flush=True)
        sys.exit(1)

    if len(sys.argv) < 7:
        print("python %s <base url> <site id> <api token> <command> <infile(s)> <result file(s)> [parameter]", flush=True)
        print("")
        print("Usage:")
        print("      site id     : 'nims-dev', 'u-tokyo-enokiLab', 'uacj', 'ihi' and 'kobelco' の様な識別名")
        print("      base url    : MIntシステムのURL(e.g. https://nims.mintsys.jp or https://dev-u-tokyo.mintsys.jp)")
        print("      api token   : ワークフロー実行者のAPIトークン")
        print("      command     : 外部計算機側で実行するコマンドまたはプログラム名")
        print("      infiles     : commandに必要なパラメータを : でつなげて記述(e.g. infile1:infile2:...:infilen")
        print("      result files: 外部計算機側で出力されたファイルのうち必要なファイルを : でつなげて記述(e.g. result1:result2:...:resultn")
        print('      paramere    : commandに必要なファイル以外のパラメータ。複数ある場合は"で囲って指定する。', flush=True)
        sys.exit(1)

    baseUrl = "%s:50443"%sys.argv[1]
    siteId = sys.argv[2]
    token = sys.argv[3]
    command = sys.argv[4]
    infiles = sys.argv[5].split(":")
    result_files = sys.argv[6].split(":")
    params = ""
    if len(sys.argv) == 8:
        params = sys.argv[7]

    print("base url = %s"%baseUrl, flush=True)
    print("site id = %s"%siteId, flush=True)

    api_prog = mi_workflow(siteId, baseUrl, token, command, infiles, result_files, params)

    print("regist calc", flush=True)
    if api_prog.miDistApiAddCalc() is False:
        print("error?", flush=True)
        sys.exit(1)
    time.sleep(2.0)
    print("allow calc", flush=True)
    ret, message = api_prog.miDistApiAllowWaitCalc()
    if ret is False:
        print(message, flush=True)
        sys.exit(1)

    print("wait untill end", flush=True)
    time.sleep(2.0)
    priv_message = "unknown"
    while True:         # 計算終了になるまでループ
        ret, messages = api_prog.miDistApiStatus()
        if ret is False:
            print(messages, flush=True)
            sys.exit(1)

        message = messages.split(":")[1]
        if priv_message != message:
            print("status change from %s to %s"%(priv_message, message), flush=True)
            priv_message = message

        if message == "got return":
            break
        time.sleep(10.0)

    print("get results", flush=True)
    time.sleep(2.0)
    ret, message = api_prog.miDistApiGetCalcResult()
    if ret is False:
        print(message, flush=True)
        sys.exit(1)

    print("calc end", flush=True)
    api_prog.accept_id = None
    sys.exit(0)

if __name__ == '__main__':
    main()
                               
