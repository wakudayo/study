from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from config import SAMPLE_INSTANCE_PATH

app = FastAPI()

# フロントエンドと通信できるように CORS を設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # すべてのオリジンを許可
    allow_methods=["*"],
    allow_headers=["*"],
)

# フォルダ内のファイルを提供
app.mount("/files", StaticFiles(directory=SAMPLE_INSTANCE_PATH), name="files")
