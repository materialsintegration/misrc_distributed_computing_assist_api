# MIシステム用に分散計算機環境用の補助を行うAPI群
このリポジトリには表題のAPIを実現するpythonベース、Flaskパッケージ使用のプロジェクトが格納されています。
## 概要
MIシステムはローカルに構築された計算機のみを使用して計算を行います。行われる計算のうち商用コードなどがあった場合も同様に実行はローカルにまたはライセンスの許諾する場所の計算機を使用する。他方、共同研究利用などで企業などからNIMSへアクセスし、NIMSにない計算機または商用コードを含んだ計算を行いたいというニーズがある。このためMIシステムの計算機からこれら外部の計算機または商用コードの計算を行う計算機を有機的に接続し、あたかもMIシステムで計算するのと同じ状態を作り出すための仕組みを考える。その一つが本プロジェクトであり、APIを中心にポーリングシステムを構築して非同期ながらHTTPまたはHTTPSアクセスのみでこれら分散計算機環境に対応したMIシステムとすることができる。

※ 分散環境で実行される商用コードはあくまでその分散環境と実行者の組織、場所などが同じまたはその商用コードのライセンス上許諾される範囲にあることが前提となる。ただし本プロジェクトはその前提条件を検証、担保するところは範囲外とする。

## 使用準備
ここから使用前の準備を記述する。

### rsyslogの設定
本APIはログをsyslog の機能を使用して/var/log/distcomp-api以下に記録するように作られている。そのための手順を記述する。

* rsyslog.confの変更と再起動   
  以下の手順を実行する。実行はrootまたはsudoなどで行う。
  ```
  # cd /etc
  # patch -b rsyslog.conf <directory name for this product>/syslogs/rsyslog.patch
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

## 参考文献
### FlaskのAPI利用法
本APIはpythonのFlaskパッケージを使用しています。このパッケージを使用したAPIの実装のための参考文献
* ![さくらのレンタルサーバーでFlaskを利用した住所検索APIを構築してみました](https://day-journal.com/memo/try-019/)

### ログ出力
本APIはsyslog機能を使用するのでその参考文献
* ![pythonでのsyslogの使い方](https://qiita.com/Esfahan/items/7888914dca0e8d23eac3)
* ![Python:mod_wsgiのログをrsyslogとlogrotateでローテーションする](https://blog.amedama.jp/entry/2015/09/13/000901)

