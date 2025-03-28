import os
from config import SAMPLE_INSTANCE_PATH

def get_html_files(directory):
    """
    指定したディレクトリ内のすべてのHTMLファイルを取得し、適切なURLに変換する
    :param directory: 検索対象のディレクトリ
    :return: 変換済みのHTMLファイルのURLリスト
    """
    html_files = []
    for root, _, files in os.walk(directory): # os.walkで再帰的にサンプルインスタンス以下のファイルすべてを探索する
        for file in files:
            if file.endswith(".html") or file.endswith(".htm"):  # 見つけたファイルの拡張子がHTMLファイルのみ取得
                relative_path = os.path.relpath(os.path.join(root, file), directory)
                full_url = f"http://localhost:8000/files/{relative_path}" # urlを組み立てる
                html_files.append(full_url)

    return html_files

if __name__ == "__main__":

    html_files = get_html_files(SAMPLE_INSTANCE_PATH)

    # 取得したHTMLファイル一覧を表示
    for url in html_files:
        print(url)
