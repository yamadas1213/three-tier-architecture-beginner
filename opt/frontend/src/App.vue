<script setup>
import { ref, onMounted } from 'vue'

const todos = ref([])
const newTitle = ref('')
const loading = ref(false)
const errorMsg = ref('')

// 共通：API呼び出し
async function api(path, opts = {}) {
  const res = await fetch(path, { headers: { 'Content-Type': 'application/json' }, ...opts })
  if (!res.ok) {
    const t = await res.text().catch(() => '')
    throw new Error(`${res.status} ${res.statusText} ${t}`)
  }
  const text = await res.text()
  return text ? JSON.parse(text) : null
}

async function fetchTodos() {
  loading.value = true
  errorMsg.value = ''
  try {
    todos.value = await api('/api/todos')
  } catch (e) {
    errorMsg.value = '一覧の取得に失敗しました。' + (e?.message ? ` (${e.message})` : '')
  } finally {
    loading.value = false
  }
}

async function addTodo() {
  const title = newTitle.value.trim()
  if (!title) return
  errorMsg.value = ''
  try {
    await api('/api/todos', { method: 'POST', body: JSON.stringify({ title }) })
    newTitle.value = ''
    await fetchTodos()
  } catch (e) {
    errorMsg.value = '追加に失敗しました。' + (e?.message ? ` (${e.message})` : '')
  }
}

async function toggle(todo) {
  errorMsg.value = ''
  try {
    await api(`/api/todos/${todo.id}/toggle`, { method: 'POST' })
    await fetchTodos()
  } catch (e) {
    errorMsg.value = '更新に失敗しました。' + (e?.message ? ` (${e.message})` : '')
  }
}

function onKeydown(e) {
  if (e.key === 'Enter') addTodo()
}

onMounted(fetchTodos)
</script>

<template>
  <main class="container">
    <h1>TODO管理アプリ</h1>

    <section class="composer">
      <input
        v-model="newTitle"
        @keydown="onKeydown"
        placeholder="新規TODOを入力して Enter"
        aria-label="新規TODO入力"
      />
      <button @click="addTodo">追加</button>
    </section>

    <p v-if="loading" class="muted">読み込み中...</p>
    <p v-if="errorMsg" class="error">{{ errorMsg }}</p>

    <ul class="list">
      <li v-for="t in todos" :key="t.id" class="item">
        <label class="row">
          <input type="checkbox" :checked="t.done === 1 || t.done === true" @change="toggle(t)" />
          <span :class="{ done: t.done === 1 || t.done === true }">{{ t.title }}</span>
        </label>
        <time class="stamp" v-if="t.created_at">{{ new Date(t.created_at).toLocaleString() }}</time>
      </li>
      <li v-if="!loading && !todos.length" class="muted">まだTODOがありません</li>
    </ul>
  </main>
</template>

<style>
:root {
  --fg: #111;
  --muted: #666;
  --border: #e5e7eb;
  --accent: #0ea5e9;
  --bg: #fff;
}

* { box-sizing: border-box; }
html, body, #app { height: 100%; }
body {
  margin: 0;
  color: var(--fg);
  background: var(--bg);
  font-family: system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,Apple Color Emoji,Segoe UI Emoji;
}

.container {
  max-width: 720px;
  margin: 40px auto;
  padding: 16px;
}

h1 {
  font-size: 22px;
  margin: 0 0 16px;
}

.composer {
  display: flex;
  gap: 8px;
  margin: 12px 0 20px;
}

.composer input {
  flex: 1;
  padding: 10px 12px;
  border: 1px solid var(--border);
  border-radius: 8px;
  outline: none;
}

.composer input:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(14,165,233,0.12);
}

.composer button {
  padding: 10px 14px;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: #f8fafc;
  cursor: pointer;
}

.list { list-style: none; padding: 0; margin: 0; }
.item {
  padding: 10px 8px;
  border-top: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.item:first-child { border-top: none; }

.row { display: flex; align-items: center; gap: 10px; }

.done { text-decoration: line-through; color: var(--muted); }
.muted { color: var(--muted); margin: 8px 0; }
.error { color: #b91c1c; background: #fee2e2; border: 1px solid #fecaca; padding: 8px 10px; border-radius: 8px; }
.stamp { color: var(--muted); font-size: 12px; }
</style>

