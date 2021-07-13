# 外部計算機資源の有効活用（API版）
このリポジトリには表題のAPIを実現するpythonベース、Flaskパッケージ使用のプロジェクトが格納されています。
## 概要
MIntシステムはローカルに構築された計算機のみを使用して計算を行います。行われる計算のうち商用コードなどがあった場合も同様に実行はローカルにまたはライセンスの許諾する場所の計算機を使用する。他方、共同研究利用などで企業などからNIMSへアクセスし、NIMSにない計算機または商用コードを含んだ計算を行いたいというニーズがある。このためMIntシステムの計算機からこれら外部の計算機または商用コードの計算を行う計算機を有機的に接続し、あたかもMIntシステムで計算するのと同じ状態を作り出すための仕組みを考える。その一つが本プロジェクトであり、APIを中心にポーリングシステムを構築して非同期ながらHTTPまたはHTTPSアクセスのみでこれら分散計算機環境に対応したMIntシステムとすることができる。

※ 分散環境で実行される商用コードはあくまでその分散環境と実行者の組織、場所などが同じまたはその商用コードのライセンス上許諾される範囲にあることが前提となる。ただし本プロジェクトはその前提条件を検証、担保するところは範囲外とする。

当リポジトリは外部計算機資源の有効活用に置ける、API実行のための資材のみが格納されている。
インストーラ、設計書などの根本的な情報はすべて「https://gitlab.mintsys.jp/midev/misrc_remote_workflow」リポジトリにて管理する方向である。

## 使用準備
ここから使用前の準備を記述する。

### rsyslogの設定
本APIはログをsyslog の機能を使用して/var/log/distcomp-api以下に記録するように作られている。そのための手順を記述する。

※ これはAPIサーバー上でのみ実施する項目である。

* rsyslog.confの変更と再起動   
  以下の手順を実行する。実行はrootまたはsudoなどで行う。
  ```
  # cd /etc
  # patch -b rsyslog.conf <directory name for this product>/syslogs/rsyslog.patch
  # cd rsyslog.d
  # cp <directory name for this product>/syslogs/distcomp-api.conf .
  # systemctl restart rsyslog(RHEL 7の場合)
  または
  # service rsyslog restart(RHEL 6の場合)
  ```

* ログファイルの場所とファイル名と機能
  + 場所：/var/log/dsitcom-api
  + distcomp-all.log：全てのログ
  + distcomp-notice.log：noticeレベルのログ
  + distcomp-error.log：Errorレベルのログ

### MIntシステムへの設定

※ これはAPIサーバー上でのみ実施する項目である。

* gatewayへの設定
  + /etc/httpd/conf.d/misystem.confファイルへの追記
    ```
    ProxyPass /mi-distcomp-api http://192.168.1.143/mi-distcomp-api
    ProxyPassReverse /mi-distcomp-api http://192.168.1.143/mi-distcomp-api
    ```
    の２行を、```<VirtualHost *:50443>```ディレクティブの  
    ```
    ProxyPass / http://192.168.1.143/
    ```
    の直前に追記します。
  + 再起動
    ```
    # systemctl restart httpd
    ```
* api-gwへの設定  
  * APIトークンの設定
    + api-gwへ設定を行い、MIntシステムのAPI認証システムを使用可能にします。
    + 設定方法（api-gwのpostgresqlへエントリを追加します。）
      ```
      $ psql -U postgres apigateway
      ユーザ postgres のパスワード: 
      psql (12.5)
      "help"でヘルプを表示します。
      
      apigateway=# insert into user_access_control values ('1100001100000xxx', 'mi-distcomp-api');
      INSERT 0 1
      apigateway=# select * from user_access_control where user_id='1100001100000xxx';
           user_id      |    database_name     
      ------------------+----------------------
       1100001100000xxx | inventory-api
       1100001100000xxx | inventory-update-api
       1100001100000xxx | suggest-api
       1100001100000xxx | workflow-api
       1100001100000xxx | asset-api
       1100001100000xxx | mi-distcomp-api
      ```
  * 認証ユーティリティのURLリライトの設定
　　- urlrewriteファイルの変更。  
      「マテリアルインテグレーション システム管理者ガイド 1.1」の「13.8.2. 独自のWebAPIの追加」を参考にして、~/tomcat/conf/urlrewrite.xmlへapi-gw/urlrwrite.xmlの内容を追記します。
    ```
    <api name="mi-distcomp-api">
        <database>mi-distcomp-api</database>
        <requestPattern>/mi-distcomp-api</requestPattern>
        <endhost>http://192.168.1.231:8082</endhost>
        <limitcall>2147483647</limitcall>
    </api>
    - APIトークン
    ```

## リポジトリ構成

本プロジェクトは以下のようなディレクトリ構成となっている。
├── README.md  
├── debug  
│   ├── api_status.py  
│   ├── api_status_gui.py  
│   ├── api_status_gui.pyc  
│   ├── mi-system-side  
│   │   ├── XX.com  
│   │   ├── XX.dat  
│   │   ├── XX.inp  
│   │   ├── XX.msg  
│   │   ├── XX.prt  
│   │   ├── XX.sim  
│   │   ├── XX.sta  
│   │   ├── aaa.bin  
│   │   ├── add-calc.py  
│   │   ├── allow-wait-calc.py  
│   │   ├── api-debug.py  
│   │   ├── cancel-wait-calc.py  
│   │   ├── debug-gui.fbp  
│   │   ├── debug_gui.py  
│   │   ├── debug_gui.pyc  
│   │   ├── get-calc-info.py  
│   │   ├── mi-system-wf.py  
│   │   └── result_files  
│   └── remote-side  
│       ├── api-debug.py  
│       ├── debug_gui.py  
│       └── mi-system-remote.py  
├── logging.cfg  
├── mi_dicomapi.py  
├── mi_dicomapi_infomations.py  
└── syslogs  
    ├── rsyslog.conf.old  
    └── rsyslog.patch  

### リポジトリ内の説明

* README.md：このファイル
* logging.cfg：syslog追加設定ファイル
* mi_dicomapi.py：MIntシステム側で動作するポーリングシステムAPI本体。
* mi_dicomapi_informations.py：APIが管理する情報クラス
* debugディレクトリ：ワークフロー側、分散環境資源計算機側のプログラム、デバッグ用状態表示プログラム、テスト実行用のパラメータなどがある。
* debug/api_status.py : API 内部の計算情報の状態監視用プログラム。
* debug/api_status_gui.py : 同、GUI部品
* debug/mi-system-side：ワークフロー側プログラム。デバッグ用のパラメータファイル。
* debug/mi-system-side/api-debug.py : 予測モジュール動作をシミュレートするプログラム。計算情報はダミー。要wxPython。
* debug/mi-system-side/debug_gui.py : 同、GUI部品
* debug/remote-side：分散環境資源計算機側ポーリングシステムプログラム、デバッグ用状態表示プログラム。
* debug/remote-side/api-debug.py : 外部計算機資源側の動作をシミュレートするプログラム。計算情報はダミー。要wxPython。
* debug/remote-side/debug-gui.py : 同、GUI部品
* syslog：/etc/rsyslog.confの設定用差分ファイル。

## 使い方
本プログラムはMIntシステム本体、ワークフローの該当モジュール、分散環境資源側の3か所でプログラムが動作して機能を実現する。それぞれの使い方を説明する。

### 概要
本プロジェクトの中核をなすのが、MIntシステム上で動作するAPI群である。ここで以下の情報を管理する。
* ワークフローからの分散環境資源計算機宛の計算依頼
* 対応する分散環境資源計算機からの担当計算の要求
* 計算状況の管理（分散環境資源計算機からの通知による）
* ワークフローからの入力ファイルのアップロード、分散環境資源計算機からの入力ファイルのダウンロード。
* 分散環境資源計算機からの結果ファイルのアップロード、ワークフローからの結果ファイルのダウンロード。

※ 本プロジェクトはプロトタイプであり、計算依頼のプログラムの指定はあらかじめ取り決めたものだけとする。  
※ 本プロジェクトを使用可能な分散環境資源計算機は同様にあらかじめ決められたものだけとする。  
※ 計算依頼されて動作するプログラムはあらかじめ分散環境資源計算機にインストールされたスクリプトのみとする。  

### MIntシステム側
APIとして機能する。デーモンとして動作させる。用意するパラメータファイルはないが、このバージョンでは接続可能なサイト名、サイト毎に利用可能なプログラム名などの情報はプログラム内に直接記述する。
指定するパラメータはこのプログラムを実行する計算機のIPアドレスとポート番号を指定する。

* 設定ファイル（mi_distributed_computing_assist.ini）の編集
  + Serverセクション
    - 実行ホストとポートの設定
  + RemoteSitesセクション
    - 外部計算機の識別名
  + 識別名のセクション
    - 識別名毎の実行プログラム名（複数化/フルパスが望ましい）
  + 設定例
    ```
    [Server]
    ipaddress = 192.168.10.242
    portnumber = 8082
    
    [RemoteSites]
    remote_site_ids = nims-dev
                   u-tokyo327
                   rme-u-tokyo
                   uacj
                   ihi-abe
                   kobeloc
    [nims-dev]
    commands = /opt/Abaqus/Commands/abaqus
            /opt/fem-ccv/femccv
    [u-tokyo327]
    commands = /opt/Abaqus/Commands/abaqus
            /opt/fem-ccv/femccv
    [rme-u-tokyo]
    commands = create_inp_file.sh
    ```
* APIアプリケーションの実行
  + /etc/systemd/systemにdistcomp_api.serviceをコピー
  + 必要であればstart.sh/shutdown.shのパスを修正
  + 実行と永続化
    ```
    # systemctl start distcomp_api.service
    # systemctl status distcomp_api.service
    # systemctl status distcomp_api.service 
    ● distcomp_api.service - arbitration using python3 Web Application Container
       Loaded: loaded (/etc/systemd/system/distcomp_api.service; enabled; vendor preset: disabled)
       Active: active (running) since 火 2021-07-13 10:50:38 JST; 2h 15min ago
     Main PID: 28559 (python3.6)
        Tasks: 3
       CGroup: /system.slice/distcomp_api.service
               ├─28559 python3.6 mi_dicomapi.py
               └─28566 /usr/bin/python3.6 /home/misystem/misrc_distributed_computing_assist_api/mi_dicomapi.py
    
     7月 13 10:50:39 app start.sh[28558]: nims-dev : ['/opt/Abaqus/Commands/abaqus', '/opt/fem-ccv/femccv']
     7月 13 10:50:39 app start.sh[28558]: u-tokyo327 : ['/opt/Abaqus/Commands/abaqus', '/opt/fem-ccv/femccv']
     7月 13 10:50:39 app start.sh[28558]: rme-u-tokyo : ['create_inp_file.sh']
     7月 13 10:50:39 app start.sh[28558]: Waiting IPaddress / Port Number
     7月 13 10:50:39 app start.sh[28558]: 192.168.10.231 / 8082
     7月 13 10:50:39 app start.sh[28558]: * Serving Flask app "mi_dicomapi" (lazy loading)
     7月 13 10:50:39 app start.sh[28558]: * Environment: production
     7月 13 10:50:39 app start.sh[28558]: WARNING: This is a development server. Do not use it in a production deployment.
     7月 13 10:50:39 app start.sh[28558]: Use a production WSGI server instead.
     7月 13 10:50:39 app start.sh[28558]: * Debug mode: on
     # systemctl enable distcomp_api.service
     ```

### ワークフロー側
ワークフローは通常のソルバーの代わりに、mi-system-wf.pyを動作させる。必要なパラメータと共に実行すれば、MIntシステム側のAPIを経由した分散環境資源計算機との必要な工程を全て執り行う。終了コードで判断する。
分散環境資源計算機側で実行させるプログラムは、以下のように準備しておく。
* MIntシステム側のAPIプログラム内に分散環境資源名とともにスクリプト名を設定しておく。
* 分散環境資源計算機内に該当するソルバー実行用のスクリプトをインストールしておく。

### 分散環境資源計算機側
分散環境資源計算機側はポーリングプログラム（mi-system-remote.py）をデーモンとして動作させる。あらかじめ実行可能なソルバーを決めておき、それを実行するスクリプトをインストールしておく。

* 使い方
  ```
  python3.6 mi-system-remote.py <識別名> <APIサーバーホスト名> <token>
  ```
* テスト実行の例
  ```
  $ python3.6 mi-system-remote.py nims-dev https://nims.mintsys.jp <token>
  site id = nims-dev
  base url = https://nims.mintsys.jp:50443
   token = <token>の表示
  2021/07/13 13:02:21:send request https://nims.mintsys.jp:50443/mi-distcomp-api/calc-request?site_id=nims-dev
  code = 401 / message = There is no information about the your site id(nims-dev)
  ```
### 
## 参考文献
### FlaskのAPI利用法
本APIはpythonのFlaskパッケージを使用しています。このパッケージを使用したAPIの実装のための参考文献
* [さくらのレンタルサーバーでFlaskを利用した住所検索APIを構築してみました](https://day-journal.com/memo/try-019/)
* [Flaskを使ってAPIサーバーを公開する。](http://rennnosukesann.hatenablog.com/entry/2018/07/21/155401)
* [Flaskのrequest.argsでパラメータ処理について](https://qiita.com/uokada/items/7cc35fbe2f956615259b)

### ログ出力
本APIはsyslog機能を使用するのでその参考文献
* [pythonでのsyslogの使い方](https://qiita.com/Esfahan/items/7888914dca0e8d23eac3)
* [Python:mod_wsgiのログをrsyslogとlogrotateでローテーションする](https://blog.amedama.jp/entry/2015/09/13/000901)

### base64エンコード
本APIはJSON形式でデータやファイル内容の受け渡しを行うが、そのためにはbase64エンコードが必要である。そのための参考資料を以下に記述する。
* [base64によるエンコードとデコード](python.ambitious-engineer.com/archives/2066)
* [BASE64でファイルのエンコード・デコード](https://algorithm.joho.info/programming/python/base64-encode-decode-py/)

### デバッグ全般
* GUIはwxを使用し、GUIの作成はwxFormBuilderを使用。
* ステータス表示GUIのタイマー実行はwx.Timerを使用。
  + [wxPython wx.Timerを使ってみる](https://bty.sakura.ne.jp/wp/archives/76)
