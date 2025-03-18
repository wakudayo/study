function TodoItem({ todo, onToggleCompletion, onDelete }) {
    return (
        <div className="todo-item">
            <input
                type="checkbox"
                checked={todo.completed}
                onChange={() => onToggleCompletion(todo.id)}
                className="form-check-input"
            />
            <span className={`todo-text ${todo.completed ? 'completed' : ''}`}>
                {todo.text}
            </span>
            <button
                onClick={() => onDelete(todo.id)}
                className="btn btn-sm btn-danger"
                aria-label="削除"
            >
                削除
            </button>
        </div>
    );
}
