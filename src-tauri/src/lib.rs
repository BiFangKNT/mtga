use std::ffi::CString;
use std::path::{Path, PathBuf};
use std::sync::{
    atomic::{AtomicBool, Ordering},
    Arc, OnceLock,
};
use std::time::Duration;

use pyo3::prelude::*;
use pyo3::types::PyDict;
use serde::{Deserialize, Serialize};
use tauri::{ipc::Channel, webview::PageLoadEvent, AppHandle, Emitter, Manager};
use tauri_plugin_autostart::MacosLauncher;

// 检查是否包含静默启动参数
fn has_minimized_arg() -> bool {
    std::env::args().any(|arg| arg == "--minimized")
}

fn resolve_python_home() -> Option<PathBuf> {
    if let Some(home) = std::env::var_os("PYTHONHOME") {
        return Some(PathBuf::from(home));
    }

    if let Ok(exe) = std::env::current_exe() {
        if let Some(exe_dir) = exe.parent() {
            // Check 1: Direct path (Windows standard bundle structure)
            let direct_candidate = exe_dir.join("pyembed").join("python");
            if direct_candidate.exists() {
                return Some(direct_candidate);
            }
            // Check 2: resources/pyembed/python (Maybe for dev or legacy structure)
            let candidate = exe_dir.join("resources").join("pyembed").join("python");
            if candidate.exists() {
                return Some(candidate);
            }
            // Check 3: Resources/pyembed/python (macOS standard)
            let mac_candidate = exe_dir.join("Resources").join("pyembed").join("python");
            if mac_candidate.exists() {
                return Some(mac_candidate);
            }
        }
    }

    if let Ok(manifest_dir) = std::env::var("CARGO_MANIFEST_DIR") {
        let manifest_path = PathBuf::from(&manifest_dir);
        let candidate = manifest_path.join("pyembed").join("python");
        if candidate.exists() {
            return Some(candidate);
        }
    }

    None
}

static PY_WARMUP: OnceLock<PyObject> = OnceLock::new();
static BACKEND_READY: AtomicBool = AtomicBool::new(false);
static MAIN_PAGE_READY: AtomicBool = AtomicBool::new(false);
static MAIN_WINDOW_SHOWN: AtomicBool = AtomicBool::new(false);
static LOG_STREAM_STARTED: AtomicBool = AtomicBool::new(false);

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

fn try_show_main(app_handle: &AppHandle) {
    if !BACKEND_READY.load(Ordering::SeqCst) || !MAIN_PAGE_READY.load(Ordering::SeqCst) {
        return;
    }
    let Some(main) = app_handle.get_webview_window("main") else {
        log::warn!(target: "boot", "label=main_window_missing");
        return;
    };
    if MAIN_WINDOW_SHOWN.swap(true, Ordering::SeqCst) {
        return;
    }

    // 检查是否是静默启动（开机自启动）
    // 注意：如果配置中窗口可见性为 false，且 setup 中没有显示窗口，这里需要确保显示
    // 但我们的逻辑是 setup 中已经处理了显示，这里主要负责通知后端就绪
    // 不过为了保险起见，如果非静默启动且窗口未显示，这里可以再次确保显示

    if let Err(error) = main.eval("window.__MTGA_BACKEND_READY__ = true;") {
        log::warn!(
            target: "boot",
            "label=backend_ready_eval_failed error={}",
            error
        );
    }
    let _ = main.emit("mtga:backend-ready", ());
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

fn resolve_python_paths(python_home: &Path) -> Vec<PathBuf> {
    let mut paths = Vec::new();

    if cfg!(windows) {
        let dlls = python_home.join("DLLs");
        if dlls.exists() {
            paths.push(dlls);
        }

        // For Anaconda/Miniconda: DLLs might be in Library/bin
        let library_bin = python_home.join("Library").join("bin");
        if library_bin.exists() {
            paths.push(library_bin);
        }
    }

    // Explicitly add base python paths if we are in a venv
    // This handles the case where python_home is the venv, but we need the base python's DLLs/Lib
    // However, our get_venv_home logic tries to return the base home.
    // If python_home IS the base home (e.g. miniconda), we need to make sure we get everything.

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

fn get_venv_home(venv_path: &Path) -> Option<PathBuf> {
    let cfg_path = venv_path.join("pyvenv.cfg");
    if !cfg_path.exists() {
        return None;
    }
    let content = std::fs::read_to_string(cfg_path).ok()?;
    for line in content.lines() {
        if let Some(rest) = line.trim().strip_prefix("home = ") {
            return Some(PathBuf::from(rest.trim()));
        }
    }
    None
}

fn ensure_python_env() -> Option<PathBuf> {
    // 1. Check for dev venv
    let mut dev_venv_path = None;
    if let Ok(manifest_dir) = std::env::var("CARGO_MANIFEST_DIR") {
        let manifest_path = PathBuf::from(&manifest_dir);
        if let Some(project_root) = manifest_path.parent() {
            let venv = project_root.join("python-src").join(".venv");
            if venv.exists() {
                dev_venv_path = Some(venv);
            }
        }
    }

    let mut home_path = resolve_python_home();

    // If dev venv exists and we didn't find a bundled python, use the venv's base home
    if home_path.is_none() {
        if let Some(venv) = &dev_venv_path {
            if let Some(real_home) = get_venv_home(venv) {
                home_path = Some(real_home);
            }
        }
    }

    if let Some(ref home) = home_path {
        if std::env::var_os("PYTHONHOME").is_none() {
            std::env::set_var("PYTHONHOME", home);
        }
    }

    if std::env::var_os("PYTHONPATH").is_none() {
        let mut paths = Vec::new();

        // Add standard libs from home if available
        if let Some(ref home) = home_path {
            paths.extend(resolve_python_paths(home));
        }

        // Add dev venv site-packages
        if let Some(venv) = &dev_venv_path {
            let site_packages = venv.join("Lib").join("site-packages");
            if site_packages.exists() {
                paths.insert(0, site_packages);
            }

            // Add python-src root
            if let Some(parent) = venv.parent() {
                paths.insert(0, parent.to_path_buf());
            }
        } else if let Ok(manifest_dir) = std::env::var("CARGO_MANIFEST_DIR") {
            // Fallback for non-venv dev environment (if any)
            let manifest_path = PathBuf::from(&manifest_dir);
            if let Some(project_root) = manifest_path.parent() {
                let python_src = project_root.join("python-src");
                if python_src.exists() {
                    paths.push(python_src);
                }
            }
        }

        if !paths.is_empty() {
            let separator = if cfg!(windows) { ";" } else { ":" };
            let joined = paths
                .iter()
                .map(|path| path.to_string_lossy())
                .collect::<Vec<_>>()
                .join(separator);
            std::env::set_var("PYTHONPATH", joined);
        }
    }

    if std::env::var_os("MTGA_ENV_FILE").is_none() {
        if let Some(ref home) = home_path {
            if let Some(env_file) = resolve_env_file(home) {
                std::env::set_var("MTGA_ENV_FILE", env_file);
            }
        }
    }

    home_path
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
import sys
import os
import traceback
import importlib

# Explicitly add Miniconda Library/bin to DLL search path
if sys.platform == "win32":
    # Common locations for Miniconda/Anaconda
    possible_prefixes = [
        sys.prefix,
        r"C:\ProgramData\miniconda3",
        os.environ.get("CONDA_PREFIX", "")
    ]
    
    for prefix in possible_prefixes:
        if not prefix: continue
        lib_bin = os.path.join(prefix, "Library", "bin")
        if os.path.exists(lib_bin):
            try:
                os.add_dll_directory(lib_bin)
            except Exception:
                pass
            # Also add to PATH
            if lib_bin not in os.environ["PATH"]:
                os.environ["PATH"] = lib_bin + os.pathsep + os.environ["PATH"]

# Debug logging for boot
try:
    with open("python_boot.log", "w", encoding="utf-8") as f:
        f.write(f"sys.path: {sys.path}\n")
        f.write(f"os.environ: {os.environ}\n")
        if sys.platform == "win32":
             f.write(f"PATH: {os.environ.get('PATH', '')}\n")
except:
    pass

_handler = None

def _ensure_handler():
    global _handler
    if _handler is None:
        try:
            module = importlib.import_module("mtga_app")
            _handler = module.get_py_invoke_handler()
        except Exception:
            with open("python_error.log", "w", encoding="utf-8") as f:
                f.write(traceback.format_exc())
            raise
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
    start_log_event_stream(app_handle.clone());
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

fn start_log_event_stream(app_handle: AppHandle) {
    if LOG_STREAM_STARTED.swap(true, Ordering::SeqCst) {
        return;
    }
    std::thread::spawn(move || {
        let mut after_id: Option<i64> = None;
        loop {
            let result = Python::with_gil(|py| -> PyResult<(Vec<String>, Option<i64>)> {
                let module = PyModule::import(py, "modules.runtime.log_bus")?;
                let pull_logs = module.getattr("pull_logs")?;
                let kwargs = PyDict::new(py);
                kwargs.set_item("after_id", after_id)?;
                kwargs.set_item("timeout_ms", 1000)?;
                kwargs.set_item("max_items", 200)?;
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
            });

            match result {
                Ok((items, next_id)) => {
                    if let Some(value) = next_id {
                        after_id = Some(value);
                    }
                    if !items.is_empty() {
                        let payload = LogEventPayload {
                            items,
                            next_id: after_id.unwrap_or(0),
                        };
                        if let Err(error) = app_handle.emit("mtga:logs", payload) {
                            log::warn!(
                                target: "boot",
                                "label=log_stream_emit_failed error={}",
                                error
                            );
                        }
                    }
                }
                Err(error) => {
                    log::warn!(
                        target: "boot",
                        "label=log_stream_pull_failed error={}",
                        error
                    );
                    std::thread::sleep(Duration::from_millis(200));
                }
            }
        }
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

#[tauri::command]
fn check_minimized_arg() -> bool {
    has_minimized_arg()
}

#[tauri::command]
fn quit_app(app_handle: AppHandle) {
    app_handle.exit(0);
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    if !cfg!(debug_assertions) && std::env::var("MTGA_RUNTIME").is_err() {
        std::env::set_var("MTGA_RUNTIME", "tauri");
    }

    if std::env::var("MTGA_VERSION").is_err() {
        std::env::set_var("MTGA_VERSION", env!("CARGO_PKG_VERSION"));
    }

    init_python_runtime();
    let py_invoke_handler =
        build_py_invoke_handler().expect("Failed to initialize Python invoke handler");

    let backend_init_started = Arc::new(AtomicBool::new(false));

    let app = tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            proxy_step_channel,
            check_minimized_arg,
            quit_app
        ])
        .plugin(tauri_plugin_pytauri::init(py_invoke_handler))
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_shell::init())
        .plugin(tauri_plugin_autostart::init(
            MacosLauncher::LaunchAgent,
            Some(vec!["--minimized"]), // 启动参数：最小化启动
        ))
        .plugin(tauri_plugin_single_instance::init(|app, _args, _cwd| {
            if let Some(window) = app.get_webview_window("main") {
                let _ = window.unminimize();
                let _ = window.show();
                let _ = window.set_focus();
            }
        }))
        .on_page_load({
            let backend_init_started = Arc::clone(&backend_init_started);
            move |webview, payload| {
                if payload.event() == PageLoadEvent::Finished {
                    // Main window loaded
                    MAIN_PAGE_READY.store(true, Ordering::SeqCst);
                    let app_handle = webview.app_handle().clone();
                    try_show_main(&app_handle);

                    // Start backend init if not already started (fallback)
                    start_backend_init(app_handle, Arc::clone(&backend_init_started));
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

                // Start backend init immediately
                start_backend_init(app.handle().clone(), Arc::clone(&backend_init_started));

                if let Some(window) = app.get_webview_window("main") {
                    inject_runtime_tag(&window);

                    // Show main window immediately if not silent startup
                    if !has_minimized_arg() {
                        let _ = window.show();
                        let _ = window.set_focus();
                    }
                }
                Ok(())
            }
        })
        .setup(|_app| {
            // 系统托盘将在应用启动后通过前端JavaScript创建
            // 这样我们可以使用前端API来控制托盘行为
            // Tauri v2 的系统托盘API需要在前端JavaScript中初始化
            // 我们将在app.vue或专门的组件中创建系统托盘

            Ok(())
        })
        .on_window_event({
            move |_window, _event| {
                // 窗口事件处理逻辑移交前端，保持状态同步
            }
        })
        .build(tauri::generate_context!())
        .expect("error while building tauri application");

    app.run(move |_app_handle, _event| {});
}
