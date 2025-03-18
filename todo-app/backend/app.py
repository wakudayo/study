from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # フロントエンドからのリクエストを許可

# JSONファイルのパス
TODOS_FILE = os.path.join(os.path.dirname(__file__), 'todos.json')

# JSONファイルが存在しない場合は作成
if not os.path.exists(TODOS_FILE):
    with open(TODOS_FILE, 'w') as f:
        json.dump([], f)

# TODOリストの取得
def get_todos():
    try:
        with open(TODOS_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

# TODOリストの保存
def save_todos(todos):
    with open(TODOS_FILE, 'w', encoding='utf-8') as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)

# 全てのTODOを取得
@app.route('/api/todos', methods=['GET'])
def get_all_todos():
    return jsonify(get_todos())

# 新しいTODOを追加
@app.route('/api/todos', methods=['POST'])
def add_todo():
    todos = get_todos()
    new_todo = request.json
    
    # IDの生成（既存のTODOがある場合は最大ID+1、なければ1）
    if todos:
        new_todo['id'] = max(todo['id'] for todo in todos) + 1
    else:
        new_todo['id'] = 1
    
    # 完了状態を初期化
    new_todo['completed'] = False
    
    todos.append(new_todo)
    save_todos(todos)
    return jsonify(new_todo), 201

# TODOの完了状態を更新
@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todos = get_todos()
    for todo in todos:
        if todo['id'] == todo_id:
            todo['completed'] = request.json.get('completed', todo['completed'])
            save_todos(todos)
            return jsonify(todo)
    return jsonify({"error": "Todo not found"}), 404

# TODOを削除
@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todos = get_todos()
    for i, todo in enumerate(todos):
        if todo['id'] == todo_id:
            del todos[i]
            save_todos(todos)
            return jsonify({"message": "Todo deleted"})
    return jsonify({"error": "Todo not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
