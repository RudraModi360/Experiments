import { test } from "node:test";
import assert from "node:assert/strict";
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const app = require("../app.js");
function fakeStorage(){ const m=new Map(); return { getItem:k=>m.has(k)?m.get(k):null, setItem:(k,v)=>m.set(k,String(v)) }; }
test("save/load round-trip persists todos", () => {
  const s=fakeStorage(); let todos=[]; todos=app.addTodo(todos,"buy milk"); app.saveTodos(s,todos);
  const loaded=app.loadTodos(s); assert.equal(loaded.length,1); assert.equal(loaded[0].title,"buy milk");
});
test("delete uses event delegation on the container", () => {
  const calls=[]; const container={addEventListener:(ev,fn)=>calls.push(ev), querySelectorAll:()=>{throw new Error("per-item");}};
  const todos=app.addTodo([],"dynamic item"); app.bindEvents(container,todos,()=>{});
  assert.ok(calls.includes("click"),"delegated listener");
});
