from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# フロントエンドと通信できるように CORS を設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # すべてのオリジンを許可
    allow_methods=["*"],
    allow_headers=["*"],
)

# Windows のパス（r をつけるとエスケープが不要）
html_directory = r"C:\Users\synergy\Desktop\screenshot_for_windows\サンプルインスタンス"

# フォルダ内のファイルを提供
app.mount("/files", StaticFiles(directory=html_directory), name="files")
