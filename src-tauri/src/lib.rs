use std::ffi::CString;
use std::path::{Path, PathBuf};
use std::sync::{
    Arc, OnceLock,
    atomic::{AtomicBool, Ordering},
};
use std::time::Duration;

use pyo3::prelude::*;
use pyo3::types::PyDict;
use serde::{Deserialize, Serialize};
use tauri::{
    AppHandle, Emitter, Listener, Manager, RunEvent, Url, WindowEvent,
    ipc::Channel,
    menu::{Menu, MenuItem},
    tray::{MouseButton, MouseButtonState, TrayIconBuilder, TrayIconEvent},
    webview::PageLoadEvent,
};

const MAIN_WINDOW_LABEL: &str = "main";
const SPLASH_WINDOW_LABEL: &str = "splash";
const TRAY_ID: &str = "mtga-main-tray";
const TRAY_SHOW_MENU_ID: &str = "mtga-tray-show";
const TRAY_QUIT_MENU_ID: &str = "mtga-tray-quit";

fn resolve_python_home() -> Option<PathBuf> {
    if let Some(home) = std::env::var_os("PYTHONHOME") {
        return Some(PathBuf::from(home));
    }

    if let Ok(exe) = std::env::current_exe() {
        if let Some(exe_dir) = exe.parent() {
            let candidate = exe_dir.join("resources").join("pyembed").join("python");
            if candidate.exists() {
                return Some(candidate);
            }
            let mac_candidate = exe_dir.join("Resources").join("pyembed").join("python");
            if mac_candidate.exists() {
                return Some(mac_candidate);
            }
        }
    }

    if let Ok(manifest_dir) = std::env::var("CARGO_MANIFEST_DIR") {
        let candidate = PathBuf::from(manifest_dir).join("pyembed").join("python");
        if candidate.exists() {
            return Some(candidate);
        }
    }

    None
}

static PY_WARMUP: OnceLock<PyObject> = OnceLock::new();
static BACKEND_READY: AtomicBool = AtomicBool::new(false);
static MAIN_PAGE_READY: AtomicBool = AtomicBool::new(false);
static FRONTEND_READY: AtomicBool = AtomicBool::new(false);
static MAIN_WINDOW_SHOWN: AtomicBool = AtomicBool::new(false);

fn set_env_var_during_startup<K, V>(key: K, value: V)
where
    K: AsRef<std::ffi::OsStr>,
    V: AsRef<std::ffi::OsStr>,
{
    // SAFETY: 仅在应用启动早期主线程调用，尚未启动后台线程或 Python 运行时。
    unsafe {
        std::env::set_var(key, value);
    }
}

#[derive(Clone, Serialize)]
struct LogEventPayload {
    items: Vec<String>,
    next_id: i64,
}

#[derive(Deserialize)]
struct ProxyStepEvent {
    step: String,
    status: String,
}

fn is_splash_url(url: &Url) -> bool {
    url.path().ends_with("/splashscreen.html")
}

fn try_show_main(app_handle: &AppHandle) {
    if !BACKEND_READY.load(Ordering::SeqCst)
        || !MAIN_PAGE_READY.load(Ordering::SeqCst)
        || !FRONTEND_READY.load(Ordering::SeqCst)
    {
        return;
    }
    let Some(main) = app_handle.get_webview_window(MAIN_WINDOW_LABEL) else {
        log::warn!(target: "boot", "label=main_window_missing");
        return;
    };
    if MAIN_WINDOW_SHOWN.swap(true, Ordering::SeqCst) {
        return;
    }
    if let Some(splash) = app_handle.get_webview_window(SPLASH_WINDOW_LABEL) {
        if let Ok(pos) = splash.outer_position() {
            let _ = main.set_position(pos);
        }
        if let Ok(size) = splash.outer_size() {
            let _ = main.set_size(size);
        }
    }
    if let Err(error) = main.show() {
        log::warn!(
            target: "boot",
            "label=main_show_failed error={}",
            error
        );
    }
    let _ = main.set_focus();
    if let Err(error) = main.eval("window.__MTGA_BACKEND_READY__ = true;") {
        log::warn!(
            target: "boot",
            "label=backend_ready_eval_failed error={}",
            error
        );
    }
    let _ = main.emit("mtga:backend-ready", ());
    if let Some(splash) = app_handle.get_webview_window(SPLASH_WINDOW_LABEL) {
        if let Err(error) = splash.close() {
            log::warn!(
                target: "boot",
                "label=splash_close_failed error={}",
                error
            );
        }
    }
}

fn schedule_try_show_main(app_handle: AppHandle) {
    let app_handle_clone = app_handle.clone();
    if let Err(error) = app_handle.run_on_main_thread(move || {
        try_show_main(&app_handle_clone);
    }) {
        log::warn!(target: "boot", "label=run_on_main_thread_failed error={}", error);
        try_show_main(&app_handle);
    }
}

fn mark_frontend_ready(app_handle: &AppHandle) {
    FRONTEND_READY.store(true, Ordering::SeqCst);
    schedule_try_show_main(app_handle.clone());
}

fn resolve_python_paths(python_home: &Path) -> Vec<PathBuf> {
    let mut paths = Vec::new();
    let lib = python_home.join("Lib");
    if lib.exists() {
        paths.push(lib.clone());
        let site = lib.join("site-packages");
        if site.exists() {
            paths.push(site);
        }
        return paths;
    }

    let unix_lib = python_home.join("lib");
    if !unix_lib.exists() {
        return paths;
    }
    if let Ok(entries) = std::fs::read_dir(&unix_lib) {
        for entry in entries.flatten() {
            let path = entry.path();
            if !path.is_dir() {
                continue;
            }
            let name = path
                .file_name()
                .and_then(|value| value.to_str())
                .unwrap_or("");
            if !name.starts_with("python") {
                continue;
            }
            paths.push(path.clone());
            let site = path.join("site-packages");
            if site.exists() {
                paths.push(site);
            }
        }
    }
    paths
}

fn resolve_env_file(python_home: &Path) -> Option<PathBuf> {
    let windows_candidate = python_home.join("Lib").join(".env");
    if windows_candidate.exists() {
        return Some(windows_candidate);
    }

    let unix_lib = python_home.join("lib");
    if unix_lib.exists() {
        let direct = unix_lib.join(".env");
        if direct.exists() {
            return Some(direct);
        }
        if let Ok(entries) = std::fs::read_dir(&unix_lib) {
            for entry in entries.flatten() {
                let path = entry.path();
                if path.is_dir() {
                    let candidate = path.join(".env");
                    if candidate.exists() {
                        return Some(candidate);
                    }
                }
            }
        }
    }

    None
}

fn ensure_python_env() -> Option<PathBuf> {
    let home = resolve_python_home();
    let home_path = home.as_ref()?;

    if std::env::var_os("PYTHONHOME").is_none() {
        set_env_var_during_startup("PYTHONHOME", home_path);
    }

    if std::env::var_os("PYTHONPATH").is_none() {
        let paths = resolve_python_paths(home_path);
        if !paths.is_empty() {
            let separator = if cfg!(windows) { ";" } else { ":" };
            let joined = paths
                .iter()
                .map(|path| path.to_string_lossy())
                .collect::<Vec<_>>()
                .join(separator);
            set_env_var_during_startup("PYTHONPATH", joined);
        }
    }

    if std::env::var_os("MTGA_ENV_FILE").is_none() {
        if let Some(env_file) = resolve_env_file(home_path) {
            set_env_var_during_startup("MTGA_ENV_FILE", env_file);
        }
    }

    Some(home_path.clone())
}

fn init_python_runtime() -> Option<PathBuf> {
    let home = ensure_python_env();
    pyo3::prepare_freethreaded_python();
    if home.is_none() {
        log::warn!(target: "boot", "label=python_home_missing");
    }
    home
}

fn inject_app_version(version: &str) {
    let result = Python::with_gil(|py| -> PyResult<()> {
        let module = PyModule::import(py, "modules.services.app_version")?;
        let setter = module.getattr("set_app_version")?;
        setter.call1((version,))?;
        Ok(())
    });
    if let Err(error) = result {
        log::warn!(
            target: "boot",
            "label=app_version_inject_failed error={}",
            error
        );
    }
}

fn build_py_invoke_handler() -> PyResult<PyObject> {
    Python::with_gil(|py| {
        let bootstrap = r#"
import importlib

_handler = None

def _ensure_handler():
    global _handler
    if _handler is None:
        module = importlib.import_module("mtga_app")
        _handler = module.get_py_invoke_handler()
    return _handler

def py_invoke_handler(invoke):
    handler = _ensure_handler()
    return handler(invoke)

def warmup():
    _ensure_handler()
"#;
        let code = CString::new(bootstrap).expect("bootstrap contains null bytes");
        let filename = CString::new("mtga_lazy.py").expect("filename contains null bytes");
        let module_name = CString::new("mtga_lazy").expect("module name contains null bytes");
        let module = PyModule::from_code(py, &code, &filename, &module_name)?;
        let handler = module.getattr("py_invoke_handler")?.unbind();
        let warmup = module.getattr("warmup")?.unbind();
        let _ = PY_WARMUP.set(warmup);
        Ok(handler)
    })
}

fn warmup_py_invoke_handler() -> PyResult<()> {
    if let Some(warmup) = PY_WARMUP.get() {
        Python::with_gil(|py| -> PyResult<()> {
            warmup.bind(py).call0()?;
            Ok(())
        })?;
    }
    Ok(())
}

fn run_backend_warmup(app_handle: &AppHandle) {
    if let Err(error) = warmup_py_invoke_handler() {
        log::error!(target: "boot", "label=backend_init_error error={}", error);
    }
    BACKEND_READY.store(true, Ordering::SeqCst);
    schedule_try_show_main(app_handle.clone());
}

fn start_backend_init(app_handle: AppHandle, init_started: Arc<AtomicBool>) {
    if init_started.swap(true, Ordering::SeqCst) {
        return;
    }
    std::thread::spawn(move || {
        run_backend_warmup(&app_handle);
    });
}

fn should_stop_proxy_step(payload: &str) -> bool {
    let Ok(event) = serde_json::from_str::<ProxyStepEvent>(payload) else {
        return false;
    };
    if event.status == "failed" {
        return true;
    }
    event.step == "proxy"
}

fn pull_proxy_steps(
    after_id: Option<i64>,
    timeout_ms: i64,
    max_items: i64,
) -> PyResult<(Vec<String>, Option<i64>)> {
    Python::with_gil(|py| {
        let module = PyModule::import(py, "modules.runtime.proxy_step_bus")?;
        let pull_steps = module.getattr("pull_steps")?;
        let kwargs = PyDict::new(py);
        kwargs.set_item("after_id", after_id)?;
        kwargs.set_item("timeout_ms", timeout_ms)?;
        kwargs.set_item("max_items", max_items)?;
        let result = pull_steps.call((), Some(&kwargs))?;
        let dict = result.downcast::<PyDict>()?;
        let items = match dict.get_item("items")? {
            Some(value) => value.extract::<Vec<String>>()?,
            None => Vec::new(),
        };
        let next_id = match dict.get_item("next_id")? {
            Some(value) => value.extract::<Option<i64>>()?,
            None => None,
        };
        Ok((items, next_id))
    })
}

fn pull_logs(
    after_id: Option<i64>,
    timeout_ms: i64,
    max_items: i64,
) -> PyResult<(Vec<String>, Option<i64>)> {
    Python::with_gil(|py| {
        let module = PyModule::import(py, "modules.runtime.log_bus")?;
        let pull_logs = module.getattr("pull_logs")?;
        let kwargs = PyDict::new(py);
        kwargs.set_item("after_id", after_id)?;
        kwargs.set_item("timeout_ms", timeout_ms)?;
        kwargs.set_item("max_items", max_items)?;
        let result = pull_logs.call((), Some(&kwargs))?;
        let dict = result.downcast::<PyDict>()?;
        let items = match dict.get_item("items")? {
            Some(value) => value.extract::<Vec<String>>()?,
            None => Vec::new(),
        };
        let next_id = match dict.get_item("next_id")? {
            Some(value) => value.extract::<Option<i64>>()?,
            None => None,
        };
        Ok((items, next_id))
    })
}

fn ensure_proxy_status_watcher_started() -> PyResult<()> {
    Python::with_gil(|py| {
        let module = PyModule::import(py, "mtga_app.commands.proxy")?;
        let starter = module.getattr("ensure_proxy_status_watcher_started")?;
        starter.call0()?;
        Ok(())
    })
}

fn pull_proxy_status(
    after_id: Option<i64>,
    timeout_ms: i64,
    max_items: i64,
) -> PyResult<(Vec<String>, Option<i64>)> {
    Python::with_gil(|py| {
        let module = PyModule::import(py, "modules.runtime.proxy_status_bus")?;
        let pull_status = module.getattr("pull_status")?;
        let kwargs = PyDict::new(py);
        kwargs.set_item("after_id", after_id)?;
        kwargs.set_item("timeout_ms", timeout_ms)?;
        kwargs.set_item("max_items", max_items)?;
        let result = pull_status.call((), Some(&kwargs))?;
        let dict = result.downcast::<PyDict>()?;
        let items = match dict.get_item("items")? {
            Some(value) => value.extract::<Vec<String>>()?,
            None => Vec::new(),
        };
        let next_id = match dict.get_item("next_id")? {
            Some(value) => value.extract::<Option<i64>>()?,
            None => None,
        };
        Ok((items, next_id))
    })
}

#[tauri::command]
fn proxy_step_channel(channel: Channel<String>, start_from_latest: Option<bool>) {
    let start_from_latest = start_from_latest.unwrap_or(false);
    std::thread::spawn(move || {
        let mut after_id: Option<i64> = None;
        if start_from_latest {
            if let Ok((_, next_id)) = pull_proxy_steps(None, 0, 1) {
                after_id = next_id;
            }
        }
        loop {
            let result = pull_proxy_steps(after_id, 1000, 200);

            match result {
                Ok((items, next_id)) => {
                    if let Some(value) = next_id {
                        after_id = Some(value);
                    }
                    if items.is_empty() {
                        continue;
                    }
                    for item in items {
                        if channel.send(item.clone()).is_err() {
                            return;
                        }
                        if should_stop_proxy_step(&item) {
                            return;
                        }
                    }
                }
                Err(error) => {
                    log::warn!(
                        target: "boot",
                        "label=proxy_step_pull_failed error={}",
                        error
                    );
                    std::thread::sleep(Duration::from_millis(200));
                }
            }
        }
    });
}

#[tauri::command]
fn log_channel(channel: Channel<LogEventPayload>, after_id: Option<i64>) {
    std::thread::spawn(move || {
        let mut after_id = after_id;
        loop {
            let result = pull_logs(after_id, 1000, 200);

            match result {
                Ok((items, next_id)) => {
                    if let Some(value) = next_id {
                        after_id = Some(value);
                    }
                    if items.is_empty() {
                        continue;
                    }
                    let payload = LogEventPayload {
                        items,
                        next_id: after_id.unwrap_or(0),
                    };
                    if channel.send(payload).is_err() {
                        return;
                    }
                }
                Err(error) => {
                    log::warn!(
                        target: "boot",
                        "label=log_channel_pull_failed error={}",
                        error
                    );
                    std::thread::sleep(Duration::from_millis(200));
                }
            }
        }
    });
}

#[tauri::command]
fn proxy_status_channel(
    channel: Channel<String>,
    start_from_latest: Option<bool>,
) -> Result<(), String> {
    let start_from_latest = start_from_latest.unwrap_or(false);
    ensure_proxy_status_watcher_started().map_err(|error| {
        log::warn!(
            target: "boot",
            "label=proxy_status_watcher_start_failed error={}",
            error
        );
        error.to_string()
    })?;

    std::thread::spawn(move || {
        let mut after_id: Option<i64> = None;
        if start_from_latest {
            if let Ok((_, next_id)) = pull_proxy_status(None, 0, 1) {
                after_id = next_id;
            }
        }

        loop {
            let result = pull_proxy_status(after_id, 1000, 200);

            match result {
                Ok((items, next_id)) => {
                    if let Some(value) = next_id {
                        after_id = Some(value);
                    }
                    if items.is_empty() {
                        continue;
                    }
                    for item in items {
                        if channel.send(item).is_err() {
                            return;
                        }
                    }
                }
                Err(error) => {
                    log::warn!(
                        target: "boot",
                        "label=proxy_status_pull_failed error={}",
                        error
                    );
                    std::thread::sleep(Duration::from_millis(200));
                }
            }
        }
    });
    Ok(())
}

fn stop_proxy_on_close() {
    Python::with_gil(|py| {
        let module = PyModule::import(py, "mtga_app.commands.proxy")?;
        let handler = module.getattr("stop_proxy_for_shutdown")?;
        let _ = handler.call0();
        Ok::<(), PyErr>(())
    })
    .ok();
}

fn should_minimize_to_tray_on_close() -> bool {
    Python::with_gil(|py| -> PyResult<bool> {
        let module = PyModule::import(py, "mtga_app")?;
        let getter = module.getattr("should_minimize_to_tray_on_close")?;
        getter.call0()?.extract::<bool>()
    })
    .unwrap_or(false)
}

fn show_main_window(app_handle: &AppHandle) {
    let Some(main) = app_handle.get_webview_window(MAIN_WINDOW_LABEL) else {
        log::warn!(target: "tray", "label=main_window_missing");
        return;
    };
    let _ = main.set_skip_taskbar(false);
    if let Err(error) = main.show() {
        log::warn!(target: "tray", "label=main_show_failed error={}", error);
        return;
    }
    let _ = main.unminimize();
    let _ = main.set_focus();
    let _ = set_tray_visible(app_handle, false);
}

fn set_tray_visible(app_handle: &AppHandle, visible: bool) -> bool {
    let Some(tray) = app_handle.tray_by_id(TRAY_ID) else {
        log::warn!(target: "tray", "label=tray_icon_missing");
        return false;
    };
    if let Err(error) = tray.set_visible(visible) {
        log::warn!(target: "tray", "label=tray_visibility_failed error={}", error);
        return false;
    }
    true
}

fn request_shutdown(app_handle: AppHandle, shutdown_started: &AtomicBool) {
    if shutdown_started.swap(true, Ordering::SeqCst) {
        return;
    }
    spawn_shutdown(app_handle);
}

fn spawn_shutdown(app_handle: tauri::AppHandle) {
    std::thread::spawn(move || {
        stop_proxy_on_close();
        std::thread::sleep(Duration::from_millis(500));
        app_handle.exit(0);
    });
}

fn resolve_runtime_tag() -> String {
    std::env::var("MTGA_RUNTIME")
        .unwrap_or_else(|_| "dev".to_string())
        .trim()
        .to_lowercase()
}

fn inject_runtime_tag(window: &tauri::WebviewWindow) {
    let runtime = resolve_runtime_tag();
    let payload = serde_json::to_string(&runtime).unwrap_or_else(|_| "\"dev\"".to_string());
    let script = format!("window.__MTGA_RUNTIME__ = {payload};");
    if let Err(error) = window.eval(&script) {
        log::warn!("failed to inject MTGA runtime tag: {error}");
    }
}

fn setup_tray(app: &mut tauri::App, shutdown_started: Arc<AtomicBool>) -> tauri::Result<()> {
    let show_item = MenuItem::with_id(app, TRAY_SHOW_MENU_ID, "显示主窗口", true, None::<&str>)?;
    let quit_item = MenuItem::with_id(app, TRAY_QUIT_MENU_ID, "退出 MTGA", true, None::<&str>)?;
    let menu = Menu::with_items(app, &[&show_item, &quit_item])?;

    let mut tray_builder = TrayIconBuilder::with_id(TRAY_ID)
        .menu(&menu)
        .tooltip("MTGA")
        .show_menu_on_left_click(false);
    if let Some(icon) = app.default_window_icon().cloned() {
        tray_builder = tray_builder.icon(icon);
    }
    let tray = tray_builder.build(app)?;
    tray.set_visible(false)?;

    app.handle()
        .on_tray_icon_event(|app_handle, event| match event {
            TrayIconEvent::Click {
                button: MouseButton::Left,
                button_state: MouseButtonState::Up,
                ..
            }
            | TrayIconEvent::DoubleClick {
                button: MouseButton::Left,
                ..
            } => show_main_window(app_handle),
            _ => {}
        });

    app.handle().on_menu_event(move |app_handle, event| {
        let id: &str = event.id().as_ref();
        if id == TRAY_SHOW_MENU_ID {
            show_main_window(app_handle);
        } else if id == TRAY_QUIT_MENU_ID {
            request_shutdown(app_handle.clone(), &shutdown_started);
        }
    });

    Ok(())
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    if !cfg!(debug_assertions) && std::env::var("MTGA_RUNTIME").is_err() {
        set_env_var_during_startup("MTGA_RUNTIME", "tauri");
    }

    init_python_runtime();
    let py_invoke_handler =
        build_py_invoke_handler().expect("Failed to initialize Python invoke handler");
    let shutdown_started = Arc::new(AtomicBool::new(false));

    let backend_init_started = Arc::new(AtomicBool::new(false));
    let setup_shutdown_started = Arc::clone(&shutdown_started);

    let app = tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            log_channel,
            proxy_step_channel,
            proxy_status_channel
        ])
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_pytauri::init(py_invoke_handler))
        .plugin(tauri_plugin_shell::init())
        .on_page_load({
            let backend_init_started = Arc::clone(&backend_init_started);
            move |webview, payload| {
                if payload.event() == PageLoadEvent::Finished {
                    if !is_splash_url(payload.url()) {
                        MAIN_PAGE_READY.store(true, Ordering::SeqCst);
                        let app_handle = webview.app_handle().clone();
                        try_show_main(&app_handle);
                    }
                    let app_handle = webview.app_handle().clone();
                    let backend_init_started = Arc::clone(&backend_init_started);
                    std::thread::spawn(move || {
                        std::thread::sleep(Duration::from_millis(1200));
                        start_backend_init(app_handle, backend_init_started);
                    });
                }
            }
        })
        .setup({
            let backend_init_started = Arc::clone(&backend_init_started);
            move |app| {
                let version = app.package_info().version.to_string();
                inject_app_version(&version);
                if cfg!(debug_assertions) {
                    app.handle().plugin(
                        tauri_plugin_log::Builder::default()
                            .level(log::LevelFilter::Info)
                            .build(),
                    )?;
                }
                setup_tray(app, Arc::clone(&setup_shutdown_started))?;
                if let Some(window) = app.get_webview_window(MAIN_WINDOW_LABEL) {
                    inject_runtime_tag(&window);
                    let listener_handle = app.handle().clone();
                    window.listen("mtga:frontend-ready", move |_event| {
                        mark_frontend_ready(&listener_handle);
                    });
                }
                if let Some(splash) = app.get_webview_window(SPLASH_WINDOW_LABEL) {
                    let listener_handle = app.handle().clone();
                    splash.listen("mtga:overlay-ready", move |_event| {
                        start_backend_init(
                            listener_handle.clone(),
                            Arc::clone(&backend_init_started),
                        );
                    });
                }
                let frontend_fallback_handle = app.handle().clone();
                std::thread::spawn(move || {
                    std::thread::sleep(Duration::from_secs(8));
                    if !FRONTEND_READY.load(Ordering::SeqCst) {
                        log::warn!(
                            target: "boot",
                            "label=frontend_ready_timeout_fallback"
                        );
                        mark_frontend_ready(&frontend_fallback_handle);
                    }
                });
                Ok(())
            }
        })
        .on_window_event({
            let shutdown_started = Arc::clone(&shutdown_started);
            move |window, event| {
                if let WindowEvent::CloseRequested { api, .. } = event {
                    if window.label() == SPLASH_WINDOW_LABEL
                        && MAIN_WINDOW_SHOWN.load(Ordering::SeqCst)
                    {
                        return;
                    }
                    if window.label() == MAIN_WINDOW_LABEL
                        && MAIN_WINDOW_SHOWN.load(Ordering::SeqCst)
                        && should_minimize_to_tray_on_close()
                    {
                        api.prevent_close();
                        if !set_tray_visible(window.app_handle(), true) {
                            let app_handle = window.app_handle().clone();
                            request_shutdown(app_handle, &shutdown_started);
                            return;
                        }
                        if let Err(error) = window.hide() {
                            log::warn!(target: "tray", "label=main_hide_failed error={}", error);
                        }
                        let _ = window.set_skip_taskbar(true);
                        return;
                    }
                    api.prevent_close();
                    let app_handle = window.app_handle().clone();
                    request_shutdown(app_handle, &shutdown_started);
                }
            }
        })
        .build(tauri::generate_context!())
        .expect("error while building tauri application");

    let shutdown_started = Arc::clone(&shutdown_started);
    app.run(move |app_handle, event| match event {
        RunEvent::ExitRequested { api, .. } => {
            if !MAIN_WINDOW_SHOWN.load(Ordering::SeqCst) {
                api.prevent_exit();
                return;
            }
            if shutdown_started.swap(true, Ordering::SeqCst) {
                return;
            }
            api.prevent_exit();
            spawn_shutdown(app_handle.clone());
        }
        _ => {}
    });
}
