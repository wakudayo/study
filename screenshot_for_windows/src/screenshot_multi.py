import os
import time
import asyncio
from playwright.async_api import async_playwright
from config import SAMPLE_INSTANCE_PATH, EDGE_IMG_PATH, CHROME_IMG_PATH, LOGS_PATH
from get_html_files import get_html_files 

async def run_screenshot_parallel(html_files, browser_channel, label=""):
    import time
    t_start = time.time()

    worker_count = 2 # worker_count数を使って並列処理
    failed_urls = {}
    max_retries = 3

    class Worker:
        def __init__(self, name):
            self.name = name
            self.runner = FullPageScreenshotPlaywright(browser_channel)

        async def setup(self):
            await self.runner.create_browser()

        async def teardown(self):
            await self.runner.teardown()
            print(f"{self.name} のブラウザを閉じました")

        async def capture(self, url):
            retry_count = 0
            while retry_count < max_retries:
                success = await self.runner.capture_page(url)
                if success:
                    return None
                retry_count += 1
                print(f"{label} リトライ {retry_count}/{max_retries} : {url}")
                if retry_count < max_retries:
                    await self.runner.restart_browser()
            print(f"{label} 3回失敗: {url}")
            return url

    async def worker_task(queue, worker):
        while True:
            url = await queue.get() # queue.get()でURLをひとつ取り出す
            try:
                if url is None:
                    return
                result = await worker.capture(url) # ここで実際にスクリーンショット！
                if result:
                    failed_urls[result] = max_retries
            finally:
                queue.task_done()

    print("Workerの初期化を開始")
    workers = [Worker(f"Worker-{i}") for i in range(worker_count)] # Woker()をふたつ作ってworkers[]に格納
    await asyncio.gather(*[w.setup() for w in workers]) # 各Wokerに対して.setup()<ブラウザ起動>を並列実行
    print(f"Workerの初期化が完了（{time.time() - t_start:.2f}秒）")

    queue = asyncio.Queue() # これは順番待ちの箱、複数のWokerが交代で箱から取り出して処理する
    for url in html_files:
        queue.put_nowait(url) # 順番待ちの箱（queue）にスクショ対象URLを格納する
    for _ in range(worker_count):
        queue.put_nowait(None) # 各Wokerに「終了」の合図

    print("タスクの実行を開始")
    time_of_tasks = time.time()
    tasks = [asyncio.create_task(worker_task(queue, workers[i])) for i in range(worker_count)] # 2つのwoker_task()<スクショを撮る動作>をasyncio~で起動　
    await queue.join()  # すべてのタスク終了を待つ
    print(f"タスクの実行が完了（{time.time() - time_of_tasks:.2f}秒）")

    print("Workerの終了処理を開始")
    t_teardown = time.time()
    await asyncio.gather(*tasks)
    await asyncio.gather(*[w.teardown() for w in workers])
    print(f"Workerの終了処理が完了（{time.time() - t_teardown:.2f}秒）")

    print(f"run_screenshot_parallel 全体処理時間: {time.time() - t_start:.2f}秒")

    return failed_urls


class FullPageScreenshotPlaywright:

    def __init__(self, browser_name):
        self.browser_channel = browser_name  # "chrome" または "msedge"

        # ブラウザごとの保存先パスを設定
        if browser_name == "chrome":
            self.base_img_dir = CHROME_IMG_PATH
        elif browser_name == "msedge":
            self.base_img_dir = EDGE_IMG_PATH
        else:
            raise ValueError(f"未対応のブラウザ: {browser_name}")

    async def create_browser(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            channel=self.browser_channel, 
            headless=True
        )

    async def restart_browser(self):
        print("ブラウザを再起動します...")
        await self.teardown()
        await self.create_browser()

    async def create_save_directory(self, url):

        try:
            # URLを"/files/"で分割したものを配列partsに格納する
            # 例: "http://localhost:8000/files/01_開示府令/XBRL/AuditDoc/xxx.htm" の場合
            # 配列partsの中身はこんな感じ
            # [
            #     "http://localhost:8000",               # parts[0]
            #     "01_開示府令/XBRL/AuditDoc/xxx.htm"   # parts[1]
            # ]
            
            parts = url.split("/files/")
            
            # img以下に再現したいパス（"\01_開示府令-有価証券届出書\XBRL\AuditDoc\xxx.html"）を変数relative_pathに格納する
            relative_path = parts[1] 

            # os.path.dirname()はパスからディレクトリ部分だけを抜き出す関数
            # したがって、xxx.html部分が取り除かれ、dir_pathには\01_開示府令-有価証券届出書\XBRL\AuditDoc\までが代入される
            dir_path = os.path.dirname(relative_path)

            # 画像保存先ディレクトリを作成する
            # 第一引数:'c:\\Users\\synergy\\Desktop\\screenshot_for_windows\\img\\chrome'と
            # 第二引数:'01_開示府令-有価証券届出書\\XBRL\\AuditDoc'を結合して、
            # 保存先:'c:\Users\synergy\Desktop\screenshot_for_windows\img\chrome\01_開示府令-有価証券届出書\XBRL\AuditDoc'を作成する
            
            save_dir = os.path.join(self.base_img_dir, dir_path)

            # ディレクトリ作成
            os.makedirs(save_dir, exist_ok=True)
            return save_dir
        
        except Exception as e:
            print(f"フォルダ作成エラー: {e}")
            return self.base_img_dir  # 失敗した場合はデフォルトの `img` フォルダに保存

    async def capture_page(self, url):
        try:
            context = await self.browser.new_context()
            page = await context.new_page()

            # **フォルダを作成**
            save_dir = await self.create_save_directory(url)

            # **ファイル名を取得**
            filename = os.path.basename(url).replace(".html", "").replace(".htm", "") + ".jpeg"
            await page.goto(url, wait_until="load")
            
            # **スクリーンショットの保存先**
            screenshot_path = os.path.join(save_dir, filename)

            # **撮影**
            await page.screenshot(path=screenshot_path, full_page=True, type="jpeg")
            print(f"フルページスクリーンショットを保存しました: {screenshot_path}")

            await context.close()

        except Exception as e:
            print(f"ページ読み込みエラー: {url}")
            print(f"エラー詳細: {e}")
            return False
        return True

    async def teardown(self):
        await self.browser.close()
        await self.playwright.stop()


# =====================================メイン処理=====================================
async def main():
    html_files = get_html_files(SAMPLE_INSTANCE_PATH)
    print(f"📸 スクリーンショット対象のURL数: {len(html_files)}")

    # Chrome で撮影
    print("\n▶ Chromeで撮影開始...")
    failed_chrome = await run_screenshot_parallel(html_files, "chrome", label="Chrome")

    print("\n▶ Edgeで撮影開始...")
    failed_edge = await run_screenshot_parallel(html_files, "msedge", label="Edge")

    # 失敗URLのログ出力
    output_dir = LOGS_PATH
    os.makedirs(output_dir, exist_ok=True)

    if failed_chrome:
        chrome_log = os.path.join(output_dir, "failed_urls_chrome.txt")
        with open(chrome_log, "w", encoding="utf-8") as f:
            for url in failed_chrome:
                f.write(url + "\n")
        print(f"❌ Chromeで失敗したURLを {chrome_log} に保存しました")

    if failed_edge:
        edge_log = os.path.join(output_dir, "failed_urls_edge.txt")
        with open(edge_log, "w", encoding="utf-8") as f:
            for url in failed_edge:
                f.write(url + "\n")
        print(f"❌ Edgeで失敗したURLを {edge_log} に保存しました")

    if not failed_chrome and not failed_edge:
        print("🎉 すべてのスクリーンショットが成功しました！")
    
# 実行
asyncio.run(main())