参考サイト
https://qiita.com/atmaru/items/1f66d20a16657e493ccd

***導入方法（コマンドラインで完結します）***
・wingetが有効かどうか確認する
winget -v

・wingetが有効ではない→　wingetを有効にする
Start-Process "ms-windows-store://pdp/?productid=9NBLGGH4NNS1"

・wingetが有効→　vscode とpythonをインストール
winget install --id Python.Python.3.13 -e --accept-package-agreements --accept-source-agreements
winget install --id Microsoft.VisualStudioCode -e --accept-package-agreements --accept-source-agreements

・諸々のライブラリをインストール
pip install fastapi uvicorn playwright
playwright install chromium chrome msedge

***使用方法***

- 撮影対象のサンプルインスタンスフォルダを以下のように設置する
screenshot_for_windows\サンプルインスタンス

- 上部メニュー"ターミナル"から新規ターミナルを実行
以下のコマンドを実行する

1. サーバーを実行する（screenshot_for_windows/src# に移動してから）
uvicorn html_player:app --host 0.0.0.0 --port 8000

2. もうひとつターミナルを起動してpython実行し、スクショ撮影する
python screenshot.py

スクリーンショットは以下のディレクトリに保存されます
C:\Users\synergy\Desktop\screenshot_for_windows\img

***使用している技術***
Python
本アプリケーションの主要な処理言語。スクリーンショット撮影やサーバー処理をPythonで実装。

FastAPI
Python製の軽量Webフレームワーク。ローカルサーバーを立ち上げ、HTMLファイルをブラウザ上で表示するために使用。

Uvicorn
FastAPIアプリを動作させるASGIサーバー（http通信を可能にする）。高速で非同期処理に対応。

Playwright
ヘッドレスブラウザ自動操作ライブラリ。ChromeやEdgeを操作してHTMLのスクリーンショットを撮影。
ヘッドレスブラウザ: GUIを持たないブラウザ、画面描画を行わずにブラウザの処理だけを行うので早い。

VS Code
開発用エディタ。Pythonコードの実行に使用します。

winget
Windows向けのパッケージマネージャー。VS CodeやPythonなどのインストールをコマンドで自動化。