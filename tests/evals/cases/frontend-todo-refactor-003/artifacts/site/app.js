const SAVE_KEY = "todos";
const LOAD_KEY = "todo-items"; // BUG
function loadTodos(storage){ try { return JSON.parse(storage.getItem(LOAD_KEY)) || []; } catch { return []; } }
function saveTodos(storage, todos){ storage.setItem(SAVE_KEY, JSON.stringify(todos)); }
function addTodo(todos, title){ todos.push({ id: Date.now()+Math.random(), title, done:false }); return todos; }
function bindEvents(container, todos, rerender){
  container.querySelectorAll("button.delete").forEach(btn => {
    btn.addEventListener("click", () => {
      const id = btn.dataset.id;
      const next = todos.filter(t => String(t.id)!==id);
      todos.length=0; todos.push(...next); rerender();
    });
  });
}
