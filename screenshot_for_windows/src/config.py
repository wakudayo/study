import os

# このファイル（config.py）の親ディレクトリを基準にする
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# パスを定義（偉い）
SAMPLE_INSTANCE_PATH = os.path.join(BASE_DIR, "サンプルインスタンス")
IMG_PATH = os.path.join(BASE_DIR, "img")
LOGS_PATH = os.path.join(BASE_DIR, "logs")

# こちらのパスは枝葉になる。偉いパスの変更の影響を受ける範囲であることに注意する。
EDGE_IMG_PATH = os.path.join(IMG_PATH, "msedge")
CHROME_IMG_PATH = os.path.join(IMG_PATH, "chrome")
OTAMESHI_IMG_PATH = os.path.join(IMG_PATH, "otameshi")
