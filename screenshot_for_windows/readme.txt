参考サイト
https://qiita.com/atmaru/items/1f66d20a16657e493ccd

※screenshot_for_windowsはDesktopに直接配置して使用してください

- 撮影対象のサンプルインスタンスフォルダを以下のように設置する
C:\Users\synergy\Desktop\screenshot_for_windows\サンプルインスタンス

- 上部メニュー"ターミナル"から新規ターミナルを実行
以下のコマンドを実行する

1. サーバーを実行する（screenshot_for_windows/src# に移動してから）
uvicorn html_player:app --host 0.0.0.0 --port 8000

2. もうひとつターミナルを起動してpython実行し、スクショ撮影する
cd C:\Users\synergy\Desktop\screenshot_for_windows\src\playwrite
python screenshot.py

スクリーンショットは以下のディレクトリに保存されます
C:\Users\synergy\Desktop\screenshot_for_windows\img

