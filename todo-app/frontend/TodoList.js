function TodoList({ todos, onToggleCompletion, onDelete }) {
    if (todos.length === 0) {
        return (
            <div className="text-center py-3">
                <p className="text-muted">タスクがありません。新しいタスクを追加してください。</p>
            </div>
        );
    }

    return (
        <div>
            <h2 className="h5 mb-3">タスク一覧</h2>
            <div className="todo-list">
                {todos.map(todo => (
                    <TodoItem
                        key={todo.id}
                        todo={todo}
                        onToggleCompletion={onToggleCompletion}
                        onDelete={onDelete}
                    />
                ))}
            </div>
            <div className="mt-3">
                <p className="text-muted">
                    合計: {todos.length} タスク、
                    完了: {todos.filter(todo => todo.completed).length} タスク
                </p>
            </div>
        </div>
    );
}
