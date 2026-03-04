# 命令通信与状态管理

## 最小命令闭环

Rust 端注册命令：

```rust
#[tauri::command]
fn greet(name: String) -> String {
    format!("Hello, {name}!")
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![greet])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

前端调用：

```ts
import { invoke } from "@tauri-apps/api/core";

const msg = await invoke<string>("greet", { name: "world" });
console.log(msg);
```

## 异步与错误处理

优先返回 `Result<T, E>`，让前端以 `try/catch` 处理失败分支：

```rust
#[tauri::command]
async fn divide(a: f64, b: f64) -> Result<f64, String> {
    if b == 0.0 {
        return Err("Cannot divide by zero".into());
    }
    Ok(a / b)
}
```

## 状态注入

在 `Builder` 中 `manage`，在命令参数中注入 `State`：

```rust
use std::sync::Mutex;
use tauri::State;

struct AppState {
    counter: u32,
}

#[tauri::command]
fn increment(state: State<'_, Mutex<AppState>>) -> Result<u32, String> {
    let mut guard = state.lock().map_err(|e| e.to_string())?;
    guard.counter += 1;
    Ok(guard.counter)
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .manage(Mutex::new(AppState { counter: 0 }))
        .invoke_handler(tauri::generate_handler![increment])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

## 验收清单

1. 命令已在 `generate_handler![]` 注册。
2. 前端参数名与 Rust 参数名一致。
3. 返回错误时前端能看到明确报错。
4. 状态访问无死锁、无跨线程所有权错误。
