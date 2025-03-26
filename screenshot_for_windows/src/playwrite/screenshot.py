import os
import sys
import asyncio
from playwright.async_api import async_playwright
# 現在のスクリプトのディレクトリを取得
current_dir = os.path.dirname(os.path.abspath(__file__))

# ここで `get_html_files` をインポート
from get_html_files import get_html_files  # src ディレクトリを指定

async def run_screenshot(html_files, browser_channel, label=""):
    test = FullPageScreenshotPlaywright(browser_name=browser_channel)
    await test.create_browser()

    failed_urls = {}
    max_retries = 3

    for url in html_files:
        retry_count = 0
        while retry_count < max_retries:
            success = await test.capture_page(url)
            if success:
                break
            else:
                retry_count += 1
                print(f"{label} リトライ {retry_count}/{max_retries} : {url}")
                if retry_count < max_retries:
                    await test.restart_browser()
                else:
                    print(f"{label} 3回失敗: {url}")
                    failed_urls[url] = retry_count

    await test.teardown()
    return failed_urls

class FullPageScreenshotPlaywright:

    def __init__(self, browser_name):
        base_dir = r"C:\Users\synergy\Desktop\screenshot_for_windows\img"
        self.base_img_dir = os.path.join(base_dir, browser_name)
        self.browser_channel = browser_name  # "chrome" または "msedge"

    async def create_browser(self):
        """ Playwright のブラウザインスタンスを作成（Google Chrome 使用） """
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            channel=self.browser_channel,  # ここでGoogle Chromeを指定！
            headless=True
        )

    async def restart_browser(self):
        """ Playwright のブラウザを再起動 """
        print("ブラウザを再起動します...")
        await self.teardown()
        await self.create_browser()

    async def create_save_directory(self, url):
        """
        URL からフォルダ名を取得し、存在しない場合は作成する
        :param url: スクリーンショット対象のURL
        :return: 作成したフォルダのパス
        """
        try:
            parts = url.split("/files/")
            folder_name = parts[1].split("/")[0]  # `22_特定有価証券府令-訂正有価証券報告書【みなし訂正有価証券届出書】`
            save_dir = os.path.join(self.base_img_dir, folder_name)

            # **フォルダを作成（存在しない場合のみ）**
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
    html_directory = r"C:\Users\synergy\Desktop\screenshot_for_windows\サンプルインスタンス"
    html_files = get_html_files(html_directory)

    print(f"📸 スクリーンショット対象のURL数: {len(html_files)}")

    # Chrome で撮影
    print("\n▶ Chromeで撮影開始...")
    failed_chrome = await run_screenshot(html_files, "chrome", label="Chrome")

    # Edge で撮影
    print("\n▶ Edgeで撮影開始...")
    failed_edge = await run_screenshot(html_files, "msedge", label="Edge")

    # 失敗URLのログ出力
    output_dir = r"C:\Users\synergy\Desktop\screenshot_for_windows\logs"
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