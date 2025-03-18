const { useState, useEffect } = React;

function App() {
    const [todos, setTodos] = useState([]);
    const [newTodoText, setNewTodoText] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // APIのベースURL
    const API_URL = 'http://localhost:5000/api';

    // 全てのTODOを取得
    const fetchTodos = async () => {
        try {
            setLoading(true);
            const response = await fetch(`${API_URL}/todos`);
            if (!response.ok) {
                throw new Error('TODOの取得に失敗しました');
            }
            const data = await response.json();
            setTodos(data);
            setError(null);
        } catch (err) {
            setError('サーバーとの通信に失敗しました。バックエンドが起動しているか確認してください。');
            console.error('Error fetching todos:', err);
        } finally {
            setLoading(false);
        }
    };

    // 新しいTODOを追加
    const addTodo = async (e) => {
        e.preventDefault();
        if (!newTodoText.trim()) return;

        try {
            const response = await fetch(`${API_URL}/todos`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: newTodoText }),
            });

            if (!response.ok) {
                throw new Error('TODOの追加に失敗しました');
            }

            const newTodo = await response.json();
            setTodos([...todos, newTodo]);
            setNewTodoText('');
        } catch (err) {
            setError('TODOの追加に失敗しました');
            console.error('Error adding todo:', err);
        }
    };

    // TODOの完了状態を更新
    const toggleTodoCompletion = async (id) => {
        try {
            const todo = todos.find(t => t.id === id);
            const updatedCompleted = !todo.completed;

            const response = await fetch(`${API_URL}/todos/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ completed: updatedCompleted }),
            });

            if (!response.ok) {
                throw new Error('TODOの更新に失敗しました');
            }

            setTodos(todos.map(todo => 
                todo.id === id ? { ...todo, completed: updatedCompleted } : todo
            ));
        } catch (err) {
            setError('TODOの更新に失敗しました');
            console.error('Error updating todo:', err);
        }
    };

    // TODOを削除
    const deleteTodo = async (id) => {
        try {
            const response = await fetch(`${API_URL}/todos/${id}`, {
                method: 'DELETE',
            });

            if (!response.ok) {
                throw new Error('TODOの削除に失敗しました');
            }

            setTodos(todos.filter(todo => todo.id !== id));
        } catch (err) {
            setError('TODOの削除に失敗しました');
            console.error('Error deleting todo:', err);
        }
    };

    // コンポーネントがマウントされたときにTODOを取得
    useEffect(() => {
        fetchTodos();
    }, []);

    return (
        <div className="row">
            <div className="col-md-8 offset-md-2">
                <div className="card">
                    <div className="card-header bg-primary text-white">
                        <h1 className="h4 mb-0">TODOリスト管理アプリ</h1>
                    </div>
                    <div className="card-body">
                        {error && (
                            <div className="alert alert-danger" role="alert">
                                {error}
                            </div>
                        )}

                        <form onSubmit={addTodo} className="mb-4">
                            <div className="input-group">
                                <input
                                    type="text"
                                    className="form-control"
                                    placeholder="新しいタスクを入力..."
                                    value={newTodoText}
                                    onChange={(e) => setNewTodoText(e.target.value)}
                                />
                                <button type="submit" className="btn btn-primary">
                                    追加
                                </button>
                            </div>
                        </form>

                        {loading ? (
                            <div className="text-center">
                                <div className="spinner-border text-primary" role="status">
                                    <span className="visually-hidden">読み込み中...</span>
                                </div>
                            </div>
                        ) : (
                            <TodoList
                                todos={todos}
                                onToggleCompletion={toggleTodoCompletion}
                                onDelete={deleteTodo}
                            />
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
