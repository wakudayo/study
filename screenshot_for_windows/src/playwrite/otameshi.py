import os
import asyncio
from playwright.async_api import async_playwright

class FullPageScreenshotPlaywright:
    def __init__(self, browser_channel):
        self.browser_channel = browser_channel  # "chrome" または "msedge"
        self.img_dir = r"C:\Users\synergy\Desktop\screenshot_for_windows\img\otameshi"
        os.makedirs(self.img_dir, exist_ok=True)

    async def get_used_fonts(self, page):
        script = """() => {
            let fonts = new Set();
            document.querySelectorAll('*').forEach(el => {
                let style = window.getComputedStyle(el);
                let font = style.fontFamily;
                if (font) {
                    fonts.add(font);
                }
            });
            return Array.from(fonts);
        }"""
        fonts = await page.evaluate(script)
        return fonts

    async def capture_page(self, url):
        async with async_playwright() as p:
            browser = await p.chromium.launch(channel=self.browser_channel, headless=True)
            page = await browser.new_page()

            try:
                # 元のファイル名を取得し、拡張子を.jpegに変換
                filename = os.path.basename(url).replace(".html", "").replace(".htm", "")
                filename = f"{self.browser_channel}_{filename}.jpeg"  # 先頭にブラウザ名を追加

                # ページを開く
                await page.goto(url, wait_until="load")

                # 使用フォントを取得
                fonts = await self.get_used_fonts(page)
                print(f"🖋️ 使用フォント（{self.browser_channel}）: {fonts}")

                # フルページスクリーンショットを保存
                screenshot_path = os.path.join(self.img_dir, filename)
                await page.screenshot(path=screenshot_path, full_page=True)

                print(f"✅ {self.browser_channel}で保存: {screenshot_path}")
            except Exception as e:
                print(f"❌ {self.browser_channel} ページ読み込みエラー: {url}")
                print(f"エラー詳細: {e}")
            finally:
                await browser.close()

# 実行処理
async def main():
    url = "http://localhost:8000/files/22_特定有価証券府令-訂正有価証券報告書【みなし訂正有価証券届出書】/PublicDoc/0000000_header.htm"

    for browser in ["chrome", "msedge"]:
        print(f"\n▶ {browser} で撮影開始...")
        test = FullPageScreenshotPlaywright(browser_channel=browser)
        await test.capture_page(url)

asyncio.run(main())
