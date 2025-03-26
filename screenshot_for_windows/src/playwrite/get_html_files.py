import os

def adjust_url(url):
    """
    取得したURLのうち、/XBRL/ を削除してアクセス可能なURLに変換する
    :param url: 変換前のURL（文字列）
    :return: 変換後のURL（文字列）
    """
    return url.replace("/XBRL/", "/")  # `/XBRL/` を `/` に置換

def get_html_files(directory):
    """
    指定したディレクトリ内のすべてのHTMLファイルを取得し、適切なURLに変換する
    :param directory: 検索対象のディレクトリ
    :return: 変換済みのHTMLファイルのURLリスト
    """
    html_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".html") or file.endswith(".htm"):  # HTMLファイルのみ取得
                relative_path = os.path.relpath(os.path.join(root, file), directory)
                full_url = f"http://localhost:8000/files/{relative_path}"
                # adjusted_url = adjust_url(full_url)  # /XBRL/ を削除して変換
                html_files.append(full_url)

    return html_files

# 例: /workspaces/screenshot/サンプルインスタンス からHTMLファイルを取得
if __name__ == "__main__":
    html_directory = r"C:\Users\synergy\Desktop\screenshot_for_windows\サンプルインスタンス"
    html_files = get_html_files(html_directory)

    # 取得したHTMLファイル一覧を表示
    for url in html_files:
        print(url)
