# TODOリスト管理アプリ

タスクの追加・削除・完了管理ができるシンプルなTODOリスト管理アプリです。

## 技術スタック

- フロントエンド: React（CDNから読み込み）
- バックエンド: Python Flask
- データ保存: JSONファイル

## セットアップ手順

### バックエンドのセットアップ

1. Pythonがインストールされていることを確認してください（Python 3.6以上推奨）
2. 仮想環境を作成し、有効化します

```bash
# 仮想環境の作成
cd todo-app/backend
python -m venv venv

# 仮想環境の有効化（Windows）
venv\Scripts\activate

# 仮想環境の有効化（macOS/Linux）
# source venv/bin/activate
```

3. 必要なパッケージをインストールします

```bash
pip install -r requirements.txt
```

4. バックエンドサーバーを起動します

```bash
python app.py
```

これで、バックエンドサーバーが http://localhost:5000 で起動します。

### フロントエンドの実行

フロントエンドは単純なHTMLとJavaScriptファイルで構成されているため、特別なビルド手順は必要ありません。以下の2つの方法でフロントエンドを実行できます：

#### 方法1: プロジェクトルートディレクトリでHTTPサーバーを起動（推奨）

```bash
# プロジェクトのルートディレクトリで実行
cd todo-app
python -m http.server 8000
```

ブラウザで http://localhost:8000/frontend/ にアクセスします。

#### 方法2: フロントエンドディレクトリでHTTPサーバーを起動

```bash
# フロントエンドディレクトリで実行
cd todo-app/frontend
python -m http.server 8000
```

ブラウザで http://localhost:8000 にアクセスします。

#### 方法3: HTMLファイルを直接開く

`todo-app/frontend/index.html` をブラウザで直接開くこともできますが、この方法ではCORSポリシーによりJavaScriptファイルの読み込みがブロックされる場合があります。その場合は、上記の方法1または方法2を使用してください。

## 使用方法

1. テキストボックスに新しいタスクを入力し、「追加」ボタンをクリックしてタスクを追加します。
2. タスクの左側のチェックボックスをクリックすると、タスクを完了としてマークできます。
3. 「削除」ボタンをクリックすると、タスクを削除できます。

## 注意事項

- バックエンドサーバーが起動していない場合、フロントエンドはエラーメッセージを表示します。
- データはバックエンドの `todos.json` ファイルに保存されます。日本語などの非ASCII文字も人間が読める形式で保存されます。
- フロントエンドとバックエンドは別々のサーバーで実行されるため、両方のサーバーが起動している必要があります。
- ブラウザの開発者ツール（F12）を開くと、コンソールログでエラーメッセージを確認できます。

## トラブルシューティング

### タスクが追加されない場合

1. バックエンドサーバーが正常に起動しているか確認してください。
2. ブラウザの開発者ツール（F12）を開き、コンソールタブでエラーメッセージを確認してください。
3. バックエンドサーバーのURLが正しく設定されているか確認してください（デフォルトは `http://localhost:5000/api`）。

### CORSエラーが発生する場合

1. フロントエンドをHTTPサーバーを使用して実行してください（方法1または方法2）。
2. バックエンドサーバーが正常に起動しているか確認してください。
3. ブラウザのキャッシュをクリアしてみてください。
