#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MTGA GUI - 图形界面工具
集成证书生成和代理服务器功能，自动获取管理员权限

功能:
1. 一键生成证书
2. 导入证书到系统信任存储
3. 修改hosts文件
4. 启动代理服务器
"""

import os
import sys
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext
import ctypes
import shutil
import io
import contextlib
from pathlib import Path
import json
import time
from queue import Queue, Empty

# 获取当前脚本的绝对路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# OpenSSL 路径
OPENSSL_DIR = os.path.join(SCRIPT_DIR, "openssl")
OPENSSL_EXE = os.path.join(OPENSSL_DIR, "openssl.exe")
# 虚拟环境路径
VENV_DIR = os.path.join(SCRIPT_DIR, ".venv")
VENV_PYTHON = os.path.join(VENV_DIR, "Scripts", "python.exe")
# 其他脚本路径
GENERATE_CERTS_PY = os.path.join(SCRIPT_DIR, "generate_certs.py")
TRAE_PROXY_PY = os.path.join(SCRIPT_DIR, "trae_proxy.py")
# hosts文件路径
HOSTS_FILE = r"C:\Windows\System32\drivers\etc\hosts" if os.name == 'nt' else "/etc/hosts"
# 证书目录
CA_DIR = os.path.join(SCRIPT_DIR, "ca")

# 定义配置文件路径
CONFIG_FILE = os.path.join(SCRIPT_DIR, "mtga_config.json")

# 全局变量，用于存储代理服务器进程
proxy_process = None

# 检查是否具有管理员权限
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# 请求管理员权限并重启脚本
def run_as_admin():
    if not is_admin():
        # 使用 sys.executable 获取当前 Python 解释器的路径
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit(0)

# 捕获输出的上下文管理器
@contextlib.contextmanager
def capture_output():
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    new_stdout = io.StringIO()
    new_stderr = io.StringIO()
    sys.stdout = new_stdout
    sys.stderr = new_stderr
    try:
        yield new_stdout, new_stderr
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr

# 运行命令并返回输出
def run_command(cmd, shell=False):
    try:
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True,
            shell=shell
        )
        stdout, stderr = process.communicate()
        return process.returncode, stdout, stderr
    except Exception as e:
        return -1, "", str(e)

# 检查环境
def check_environment():
    # 检查OpenSSL
    if not os.path.exists(OPENSSL_EXE):
        return False, f"OpenSSL不存在: {OPENSSL_EXE}"
    
    # 检查虚拟环境
    if not os.path.exists(VENV_PYTHON):
        return False, f"虚拟环境不存在: {VENV_PYTHON}"
    
    # 检查脚本文件
    if not os.path.exists(GENERATE_CERTS_PY):
        return False, f"证书生成脚本不存在: {GENERATE_CERTS_PY}"
    
    if not os.path.exists(TRAE_PROXY_PY):
        return False, f"代理服务器脚本不存在: {TRAE_PROXY_PY}"
    
    return True, "环境检查通过"

# 生成证书
def generate_certificates(log_func=print):
    log_func("开始生成证书...")
    
    # 设置环境变量，确保使用正确的OpenSSL
    env = os.environ.copy()
    env["PATH"] = OPENSSL_DIR + os.pathsep + env["PATH"]
    
    # 运行证书生成脚本
    cmd = [VENV_PYTHON, GENERATE_CERTS_PY]
    log_func(f"执行命令: {' '.join(cmd)}")
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            env=env
        )
        
        # 使用communicate获取输出
        stdout, _ = process.communicate()
        
        # 输出结果
        for line in stdout.splitlines():
            log_func(line)
        
        return_code = process.returncode
        
        if return_code == 0:
            log_func("证书生成成功！")
            return True
        else:
            log_func(f"证书生成失败，返回码: {return_code}")
            return False
    except Exception as e:
        log_func(f"执行证书生成脚本时出错: {e}")
        return False

# 导入证书到系统信任存储
def import_certificate(log_func=print):
    log_func("开始导入CA证书到系统信任存储...")
    
    ca_cert_path = os.path.join(CA_DIR, "ca.crt")
    if not os.path.exists(ca_cert_path):
        log_func(f"错误: CA证书不存在: {ca_cert_path}")
        return False
    
    # 使用certutil导入证书
    cmd = ["certutil", "-addstore", "ROOT", ca_cert_path]
    log_func(f"执行命令: {' '.join(cmd)}")
    
    return_code, stdout, stderr = run_command(cmd)
    log_func(stdout)
    if stderr:
        log_func(stderr)
    
    if return_code == 0:
        log_func("CA证书导入成功！")
        return True
    else:
        log_func(f"CA证书导入失败，返回码: {return_code}")
        return False

# 安装CA证书
def install_ca_cert(log_func=print):
    """
    安装CA证书
    
    参数:
    - log_func: 日志记录函数
    
    返回值:
    - 成功返回True，失败返回False
    """
    log_func("开始安装CA证书...")
    
    # 检查可能的CA证书文件名
    possible_cert_files = [
        os.path.join(CA_DIR, "rootCA.crt"),
        os.path.join(CA_DIR, "ca.crt"),
        os.path.join(CA_DIR, "ca.cer"),
        os.path.join(CA_DIR, "rootCA.cer")
    ]
    
    ca_cert_file = None
    for cert_file in possible_cert_files:
        if os.path.exists(cert_file):
            ca_cert_file = cert_file
            log_func(f"找到CA证书文件: {ca_cert_file}")
            break
    
    if ca_cert_file is None:
        log_func(f"错误: 未找到CA证书文件，已检查以下路径: {', '.join(possible_cert_files)}")
        return False
    
    # 安装CA证书
    try:
        # Windows系统
        if os.name == 'nt':
            cmd = f'certutil -addstore -f "ROOT" "{ca_cert_file}"'
            log_func(f"执行命令: {cmd}")
            return_code, stdout, stderr = run_command(cmd, shell=True)
            log_func(stdout)
            if stderr:
                log_func(stderr)
            
            if return_code != 0:
                log_func(f"证书安装失败，返回码: {return_code}")
                return False
        # Linux系统
        elif os.name == 'posix':
            # 复制证书到系统目录
            cmd = f'sudo cp "{ca_cert_file}" /usr/local/share/ca-certificates/'
            log_func(f"执行命令: {cmd}")
            return_code, stdout, stderr = run_command(cmd, shell=True)
            log_func(stdout)
            if stderr:
                log_func(stderr)
            
            if return_code != 0:
                log_func(f"复制证书失败，返回码: {return_code}")
                return False
            
            # 更新CA证书
            cmd = 'sudo update-ca-certificates'
            log_func(f"执行命令: {cmd}")
            return_code, stdout, stderr = run_command(cmd, shell=True)
            log_func(stdout)
            if stderr:
                log_func(stderr)
            
            if return_code != 0:
                log_func(f"更新证书失败，返回码: {return_code}")
                return False
        # Mac系统
        elif sys.platform == 'darwin':
            cmd = f'sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain "{ca_cert_file}"'
            log_func(f"执行命令: {cmd}")
            return_code, stdout, stderr = run_command(cmd, shell=True)
            log_func(stdout)
            if stderr:
                log_func(stderr)
            
            if return_code != 0:
                log_func(f"证书安装失败，返回码: {return_code}")
                return False
        else:
            log_func("错误: 不支持的操作系统")
            return False
        
        log_func("CA证书安装成功！")
        return True
    except Exception as e:
        log_func(f"安装CA证书失败: {e}")
        return False

# 修改hosts文件
def modify_hosts_file(log_func=print, action="add"):
    """
    修改hosts文件
    
    参数:
    - log_func: 日志记录函数
    - action: 操作类型，可选值: "add"(添加), "backup"(备份), "restore"(还原), "reset"(重置)
    
    返回值:
    - 成功返回True，失败返回False
    """
    log_func(f"开始{{'add': '修改', 'backup': '备份', 'restore': '还原', 'reset': '重置'}}[action] hosts文件...")
    
    if not os.path.exists(HOSTS_FILE):
        log_func(f"错误: hosts文件不存在: {HOSTS_FILE}")
        return False
    
    # 备份文件路径
    backup_file = os.path.join(SCRIPT_DIR, "hosts.backup")
    
    # 尝试确定文件编码
    def detect_encoding(file_path):
        encodings = ['utf-8', 'gbk', 'gb2312', 'latin1', 'utf-16']
        for enc in encodings:
            try:
                with open(file_path, 'r', encoding=enc) as f:
                    f.read()
                return enc
            except UnicodeDecodeError:
                continue
        # 如果所有编码都失败，返回一个安全的默认值
        return 'utf-8'
    
    # 根据不同操作类型执行不同操作
    if action == "backup":
        # 备份hosts文件
        try:
            shutil.copy2(HOSTS_FILE, backup_file)
            log_func(f"hosts文件已备份到: {backup_file}")
            return True
        except Exception as e:
            log_func(f"备份hosts文件失败: {e}")
            return False
            
    elif action == "restore":
        # 还原hosts文件
        if not os.path.exists(backup_file):
            log_func(f"错误: 备份文件不存在: {backup_file}")
            return False
        
        try:
            shutil.copy2(backup_file, HOSTS_FILE)
            log_func("hosts文件已还原")
            return True
        except Exception as e:
            log_func(f"还原hosts文件失败: {e}")
            return False
            
    elif action == "reset":
        # 重置hosts文件 (删除api.deepseek.com条目)
        try:
            # 检测文件编码
            encoding = detect_encoding(HOSTS_FILE)
            log_func(f"检测到hosts文件编码: {encoding}")
            
            with open(HOSTS_FILE, 'r', encoding=encoding, errors='replace') as f:
                content = f.read()
                
            # 查找并删除包含api.deepseek.com的行
            lines = content.splitlines()
            new_lines = []
            skip_next = False
            
            for line in lines:
                if "Added by MTGA GUI" in line:
                    skip_next = True
                    continue
                if skip_next and "api.deepseek.com" in line:
                    skip_next = False
                    continue
                new_lines.append(line)
                
            # 写回文件
            with open(HOSTS_FILE, 'w', encoding=encoding) as f:
                f.write('\n'.join(new_lines))
                
            log_func("hosts文件已重置，删除了api.deepseek.com条目")
            return True
        except Exception as e:
            log_func(f"重置hosts文件失败: {e}")
            return False
            
    else:  # action == "add"
        # 添加api.deepseek.com条目
        try:
            # 先备份
            if not os.path.exists(backup_file):
                shutil.copy2(HOSTS_FILE, backup_file)
                log_func(f"hosts文件已自动备份到: {backup_file}")
            
            # 检测文件编码
            encoding = detect_encoding(HOSTS_FILE)
            log_func(f"检测到hosts文件编码: {encoding}")
            
            # 读取hosts文件内容
            with open(HOSTS_FILE, 'r', encoding=encoding, errors='replace') as f:
                content = f.read()
            
            # 检查是否已经包含api.deepseek.com
            if "127.0.0.1 api.deepseek.com" in content:
                log_func("hosts文件已包含api.deepseek.com条目，无需修改")
                return True
            
            # 添加api.deepseek.com条目
            with open(HOSTS_FILE, 'a', encoding=encoding) as f:
                f.write("\n# Added by MTGA GUI\n127.0.0.1 api.deepseek.com\n")
            log_func("hosts文件修改成功！")
            return True
        except Exception as e:
            log_func(f"修改hosts文件失败: {e}")
            return False

# 保存配置
def save_config(api_url=None, model_id=None, log_func=print):
    """
    保存配置到配置文件
    
    参数:
    - api_url: API基础URL
    - model_id: 模型ID
    - log_func: 日志记录函数
    
    返回值:
    - 成功返回True，失败返回False
    """
    try:
        # 读取现有配置（如果存在）
        config = {}
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                try:
                    config = json.load(f)
                except json.JSONDecodeError:
                    log_func("警告: 配置文件格式错误，将创建新的配置文件")
        
        # 更新配置
        if api_url is not None:
            config['api_url'] = api_url
        if model_id is not None:
            config['model_id'] = model_id
        
        # 保存配置
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        
        log_func(f"配置已保存到: {CONFIG_FILE}")
        return True
    except Exception as e:
        log_func(f"保存配置失败: {e}")
        return False

# 加载配置
def load_config(log_func=print):
    """
    从配置文件加载配置
    
    参数:
    - log_func: 日志记录函数
    
    返回值:
    - 成功返回配置字典，失败返回空字典
    """
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                log_func(f"已加载配置: {CONFIG_FILE}")
                return config
        else:
            log_func(f"配置文件不存在: {CONFIG_FILE}，将使用默认配置")
            return {}
    except Exception as e:
        log_func(f"加载配置失败: {e}")
        return {}

# 启动代理服务器
def start_proxy_server(log_func=print, api_url=None, model_id=None):
    """
    启动代理服务器
    
    参数:
    - log_func: 日志记录函数
    - api_url: API基础URL，如果为None则使用配置文件中的值
    - model_id: 模型ID，如果为None则使用配置文件中的值
    
    返回值:
    - 成功返回进程对象，失败返回None
    """
    global proxy_process
    
    log_func("开始启动代理服务器...")
    
    # 如果已经有代理服务器在运行，先停止它
    if proxy_process:
        try:
            log_func("检测到代理服务器已在运行，先停止它...")
            proxy_process.terminate()
            proxy_process = None
            # 等待一段时间确保端口释放
            time.sleep(1)
        except Exception as e:
            log_func(f"停止现有代理服务器时出错: {e}")
    
    # 检查证书文件
    possible_cert_files = [
        os.path.join(CA_DIR, "api.deepseek.com.crt"),
        os.path.join(CA_DIR, "server.crt")
    ]
    possible_key_files = [
        os.path.join(CA_DIR, "api.deepseek.com.key"),
        os.path.join(CA_DIR, "server.key")
    ]
    
    cert_file = None
    for f in possible_cert_files:
        if os.path.exists(f):
            cert_file = f
            log_func(f"找到服务器证书文件: {cert_file}")
            break
    
    key_file = None
    for f in possible_key_files:
        if os.path.exists(f):
            key_file = f
            log_func(f"找到服务器密钥文件: {key_file}")
            break
    
    if cert_file is None or key_file is None:
        log_func(f"错误: 未找到服务器证书或密钥文件")
        log_func(f"已检查的证书文件: {', '.join(possible_cert_files)}")
        log_func(f"已检查的密钥文件: {', '.join(possible_key_files)}")
        return None
    
    # 保存配置
    if api_url or model_id:
        save_config(api_url, model_id, log_func)
    
    # 创建临时代理脚本
    temp_proxy_file = os.path.join(SCRIPT_DIR, "temp_proxy.py")
    try:
        # 读取原始文件内容
        with open(TRAE_PROXY_PY, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 修改证书文件路径
        if os.path.basename(cert_file) != "api.deepseek.com.crt":
            content = content.replace(
                "CERT_FILE = os.path.join(CERT_DIR, 'api.deepseek.com.crt')",
                f"CERT_FILE = os.path.join(CERT_DIR, '{os.path.basename(cert_file)}')"
            )
        
        if os.path.basename(key_file) != "api.deepseek.com.key":
            content = content.replace(
                "KEY_FILE = os.path.join(CERT_DIR, 'api.deepseek.com.key')",
                f"KEY_FILE = os.path.join(CERT_DIR, '{os.path.basename(key_file)}')"
            )
        
        # 如果提供了API URL，替换它
        if api_url:
            # 替换常见的API URL模式
            patterns = [
                'TARGET_API_BASE_URL = "YOUR_REVERSE_ENGINEERED_API_ENDPOINT_BASE_URL"',
                'TARGET_API_BASE_URL = "https://new-api.bifangfang.top/v1"',
                'TARGET_API_BASE_URL = "https://api.example.com/v1"'
            ]
            
            for pattern in patterns:
                if pattern in content:
                    content = content.replace(pattern, f'TARGET_API_BASE_URL = "{api_url}"')
                    log_func(f"已设置API URL: {api_url}")
                    break
        
        # 如果提供了模型ID，替换它
        if model_id:
            # 替换常见的模型ID模式
            patterns = [
                'CUSTOM_MODEL_ID = "CUSTOM_MODEL_ID"',
                'CUSTOM_MODEL_ID = "glm-4-flash-250414"',
                'CUSTOM_MODEL_ID = "gpt-3.5-turbo"'
            ]
            
            for pattern in patterns:
                if pattern in content:
                    content = content.replace(pattern, f'CUSTOM_MODEL_ID = "{model_id}"')
                    log_func(f"已设置模型ID: {model_id}")
                    break
        
        # 修改脚本，确保输出使用UTF-8编码
        if "# -*- coding: utf-8 -*-" not in content:
            content = "# -*- coding: utf-8 -*-\n" + content
        
        # 写入临时文件
        with open(temp_proxy_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        log_func(f"已创建临时代理脚本: {temp_proxy_file}")
        
        # 删除可能存在的旧批处理文件
        run_proxy_bat = os.path.join(SCRIPT_DIR, "run_proxy.bat")
        if os.path.exists(run_proxy_bat):
            try:
                os.remove(run_proxy_bat)
                log_func("已删除旧的批处理文件")
            except Exception as e:
                log_func(f"删除旧批处理文件失败: {e}")
    except Exception as e:
        log_func(f"创建临时代理脚本失败: {e}")
        return None
    
    # 启动代理服务器，将输出重定向到日志
    try:
        log_func("正在启动代理服务器...")
        
        # 创建一个队列用于存储输出
        output_queue = Queue()
        
        # 定义一个尝试多种编码解码文本的函数
        def decode_with_fallback(byte_str):
            encodings = ['utf-8', 'gbk', 'gb2312', 'cp936', 'latin1']
            for encoding in encodings:
                try:
                    return byte_str.decode(encoding)
                except UnicodeDecodeError:
                    continue
            # 如果所有编码都失败，使用latin1（它不会失败，但可能有乱码）
            return byte_str.decode('latin1', errors='replace')
        
        # 定义一个读取输出的函数
        def enqueue_output(out, queue):
            for line in iter(out.readline, b''):
                queue.put(decode_with_fallback(line).strip())
            out.close()
        
        # 设置环境变量，确保子进程使用UTF-8编码
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        
        # 创建子进程
        process = subprocess.Popen(
            [VENV_PYTHON, temp_proxy_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            universal_newlines=False,
            env=env
        )
        
        # 保存到全局变量
        proxy_process = process
        
        # 创建线程来读取输出
        output_thread = threading.Thread(
            target=enqueue_output,
            args=(process.stdout, output_queue)
        )
        output_thread.daemon = True
        output_thread.start()
        
        # 创建线程来处理输出
        def process_output():
            global proxy_process
            while True:
                try:
                    # 检查进程是否还在运行
                    if process.poll() is not None:
                        # 进程已结束
                        returncode = process.poll()
                        log_func(f"代理服务器已停止，返回码: {returncode}")
                        if proxy_process == process:
                            proxy_process = None
                        break
                    
                    # 尝试从队列获取输出
                    try:
                        line = output_queue.get_nowait()
                        log_func(f"[代理] {line}")
                    except Empty:
                        # 队列为空，等待一段时间
                        time.sleep(0.1)
                        continue
                except Exception as e:
                    log_func(f"处理代理服务器输出时出错: {e}")
                    break
        
        # 启动处理输出的线程
        threading.Thread(target=process_output, daemon=True).start()
        
        log_func("代理服务器已启动！")
        return process
    except Exception as e:
        log_func(f"启动代理服务器失败: {e}")
        return None

# 检查并安装依赖
def check_and_install_dependencies(log_func=print):
    log_func("检查并安装依赖...")
    
    # 使用uv安装Flask和requests
    cmd = ["uv", "pip", "install", "Flask", "requests"]
    log_func(f"执行命令: {' '.join(cmd)}")
    
    return_code, stdout, stderr = run_command(cmd)
    log_func(stdout)
    if stderr:
        log_func(stderr)
    
    if return_code == 0:
        log_func("依赖安装成功！")
        return True
    else:
        log_func(f"依赖安装失败，返回码: {return_code}")
        return False

# 创建主窗口
def create_main_window():
    window = tk.Tk()
    window.title("MTGA GUI")
    window.geometry("650x700")  # 调整窗口高度
    window.resizable(True, True)
    
    # 设置窗口图标
    try:
        icon_path = os.path.join(SCRIPT_DIR, "icon.ico")
        if os.path.exists(icon_path):
            window.iconbitmap(icon_path)
    except Exception:
        pass
    
    # 创建主框架
    main_frame = ttk.Frame(window, padding=10)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # 添加标题
    title_label = ttk.Label(
        main_frame, 
        text="MTGA GUI - 代理服务器管理工具", 
        font=("Arial", 16, "bold")
    )
    title_label.pack(pady=10)
    
    # 创建日志文本框 - 先创建但放在底部
    log_frame = ttk.LabelFrame(main_frame, text="日志")
    log_text = scrolledtext.ScrolledText(log_frame, height=10)
    
    # 自定义日志函数
    def log(message):
        log_text.insert(tk.END, f"{message}\n")
        log_text.see(tk.END)
        print(message)
    
    # 加载配置
    config = load_config(log)
    default_api_url = config.get('api_url', "YOUR_REVERSE_ENGINEERED_API_ENDPOINT_BASE_URL")
    default_model_id = config.get('model_id', "CUSTOM_MODEL_ID")
    
    # 添加API URL和模型ID输入框 - 移到标签页上方
    config_frame = ttk.LabelFrame(main_frame, text="代理服务器配置")
    config_frame.pack(fill=tk.X, pady=5)
    
    # API URL输入框
    api_url_frame = ttk.Frame(config_frame)
    api_url_frame.pack(fill=tk.X, padx=5, pady=5)
    
    ttk.Label(api_url_frame, text="API URL:").pack(side=tk.LEFT, padx=5)
    api_url_var = tk.StringVar(value=default_api_url)
    api_url_entry = ttk.Entry(api_url_frame, textvariable=api_url_var, width=40)
    api_url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
    
    # 模型ID输入框
    model_id_frame = ttk.Frame(config_frame)
    model_id_frame.pack(fill=tk.X, padx=5, pady=5)
    
    ttk.Label(model_id_frame, text="模型ID:").pack(side=tk.LEFT, padx=5)
    model_id_var = tk.StringVar(value=default_model_id)
    model_id_entry = ttk.Entry(model_id_frame, textvariable=model_id_var, width=40)
    model_id_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
    
    # 添加保存配置按钮
    save_config_button = ttk.Button(
        config_frame,
        text="保存配置",
        command=lambda: threading.Thread(
            target=lambda: save_config(
                api_url=api_url_var.get() if api_url_var.get() else None,
                model_id=model_id_var.get() if model_id_var.get() else None,
                log_func=log
            )
        ).start()
    )
    save_config_button.pack(fill=tk.X, padx=5, pady=5)
    
    # 创建标签页控件
    notebook = ttk.Notebook(main_frame)
    notebook.pack(fill=tk.BOTH, expand=False, pady=5)
    
    # --------- 标签页1: 证书管理 ---------
    cert_tab = ttk.Frame(notebook)
    notebook.add(cert_tab, text="证书管理")
    
    # 创建证书管理按钮
    cert_button = ttk.Button(
        cert_tab, 
        text="生成CA和服务器证书", 
        command=lambda: threading.Thread(target=lambda: generate_certificates(log)).start()
    )
    cert_button.pack(fill=tk.X, padx=5, pady=5)
    
    install_cert_button = ttk.Button(
        cert_tab, 
        text="安装CA证书", 
        command=lambda: threading.Thread(target=lambda: install_ca_cert(log)).start()
    )
    install_cert_button.pack(fill=tk.X, padx=5, pady=5)
    
    # --------- 标签页2: hosts文件管理 ---------
    hosts_tab = ttk.Frame(notebook)
    notebook.add(hosts_tab, text="hosts文件管理")
    
    # 创建hosts文件管理按钮
    hosts_button = ttk.Button(
        hosts_tab, 
        text="修改hosts文件", 
        command=lambda: threading.Thread(target=lambda: modify_hosts_file(log)).start()
    )
    hosts_button.pack(fill=tk.X, padx=5, pady=5)
    
    # 添加hosts文件备份、还原和重置按钮
    hosts_buttons_frame = ttk.Frame(hosts_tab)
    hosts_buttons_frame.pack(fill=tk.X, padx=5, pady=5)
    
    hosts_backup_button = ttk.Button(
        hosts_buttons_frame, 
        text="备份hosts", 
        command=lambda: threading.Thread(target=lambda: modify_hosts_file(log, action="backup")).start()
    )
    hosts_backup_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
    
    hosts_restore_button = ttk.Button(
        hosts_buttons_frame, 
        text="还原hosts", 
        command=lambda: threading.Thread(target=lambda: modify_hosts_file(log, action="restore")).start()
    )
    hosts_restore_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
    
    hosts_reset_button = ttk.Button(
        hosts_buttons_frame, 
        text="重置hosts", 
        command=lambda: threading.Thread(target=lambda: modify_hosts_file(log, action="reset")).start()
    )
    hosts_reset_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
    
    # --------- 标签页3: 代理服务器操作 ---------
    proxy_tab = ttk.Frame(notebook)
    notebook.add(proxy_tab, text="代理服务器操作")
    
    # 创建代理服务器按钮
    proxy_button = ttk.Button(
        proxy_tab, 
        text="启动代理服务器", 
        command=lambda: threading.Thread(
            target=lambda: start_proxy_server(
                log, 
                api_url=api_url_var.get() if api_url_var.get() and api_url_var.get() != "YOUR_REVERSE_ENGINEERED_API_ENDPOINT_BASE_URL" else None,
                model_id=model_id_var.get() if model_id_var.get() and model_id_var.get() != "CUSTOM_MODEL_ID" else None
            )
        ).start()
    )
    proxy_button.pack(fill=tk.X, padx=5, pady=5)
    
    # 添加停止代理服务器按钮
    proxy_stop_button = ttk.Button(
        proxy_tab, 
        text="停止代理服务器", 
        command=lambda: threading.Thread(target=lambda: stop_proxy_server(log)).start()
    )
    proxy_stop_button.pack(fill=tk.X, padx=5, pady=5)
    
    # --------- 标签页4: 关于 ---------
    about_tab = ttk.Frame(notebook)
    notebook.add(about_tab, text="关于")
    
    # 创建关于标签
    about_text = "MTGA GUI v1.0\n\n"
    about_text += "本工具用于自动生成CA和服务器证书，修改hosts文件，启动代理服务器。\n\n"
    about_text += "使用方法：\n"
    about_text += "1. 在\"证书管理\"标签页中生成并安装CA证书\n"
    about_text += "2. 在\"hosts文件管理\"标签页中修改hosts文件\n"
    about_text += "3. 在上方配置区域设置API URL和模型ID，点击\"保存配置\"保存\n"
    about_text += "4. 在\"代理服务器操作\"标签页中启动代理服务器\n"
    about_text += "5. 或者直接点击下方的\"一键启动全部服务\"按钮，一键完成以上所有操作\n"
    
    about_label = ttk.Label(about_tab, text=about_text, justify=tk.LEFT, wraplength=550)
    about_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    # 创建一键启动按钮（放在标签页外面）
    start_button = ttk.Button(
        main_frame, 
        text="一键启动全部服务", 
        command=lambda: threading.Thread(
            target=lambda: start_all_services(
                log,
                api_url=api_url_var.get() if api_url_var.get() and api_url_var.get() != "YOUR_REVERSE_ENGINEERED_API_ENDPOINT_BASE_URL" else None,
                model_id=model_id_var.get() if model_id_var.get() and model_id_var.get() != "CUSTOM_MODEL_ID" else None
            )
        ).start()
    )
    start_button.pack(fill=tk.X, pady=10)
    
    # 现在将日志框放在最下方
    log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
    log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    # 停止代理服务器函数
    def stop_proxy_server(log_func=print):
        global proxy_process
        if proxy_process:
            try:
                log_func("正在停止代理服务器...")
                proxy_process.terminate()
                proxy_process = None
                log_func("代理服务器已停止")
            except Exception as e:
                log_func(f"停止代理服务器时出错: {e}")
        else:
            log_func("代理服务器未运行")
    
    # 初始日志
    log("MTGA GUI已启动，请选择操作...")
    
    # 窗口关闭时停止代理服务器
    def on_closing():
        global proxy_process
        if proxy_process:
            try:
                log("正在停止代理服务器...")
                proxy_process.terminate()
                proxy_process = None
            except:
                pass
        window.destroy()
    
    window.protocol("WM_DELETE_WINDOW", on_closing)
    
    return window, log

# 一键启动全部服务
def start_all_services(log_func=print, api_url=None, model_id=None):
    log_func("开始一键启动全部服务...")
    
    # 生成证书
    if not generate_certificates(log_func):
        log_func("生成证书失败，无法继续！")
        return False
    
    # 安装CA证书
    if not install_ca_cert(log_func):
        log_func("安装CA证书失败，无法继续！")
        return False
    
    # 修改hosts文件
    if not modify_hosts_file(log_func):
        log_func("修改hosts文件失败，无法继续！")
        return False
    
    # 如果提供了API URL或模型ID，保存到配置文件
    if api_url or model_id:
        if not save_config(api_url, model_id, log_func):
            log_func("保存配置失败，但将继续启动代理服务器")
    
    # 启动代理服务器
    process = start_proxy_server(log_func, api_url, model_id)
    if not process:
        log_func("启动代理服务器失败，无法继续！")
        return False
    
    log_func("全部服务启动成功！")
    return True

def main():
    # 检查管理员权限，如果没有则请求
    if not is_admin():
        run_as_admin()
        return
    
    # 创建GUI
    root, log = create_main_window()
    root.mainloop()

if __name__ == "__main__":
    main() 