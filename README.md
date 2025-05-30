# MTGA
<picture>
    <img alt="MTGA" src="https://github.com/user-attachments/assets/420a736a-7812-4821-847d-63dc8995c476">
</picture>

## 简介

 MTGA 是一个基于本地代理的 IDE 固定模型服务商解决方案，适用于 windows。

1) clone，2) 运行！

 <details>
  <summary>你什么也看不见~~</summary>
  <br>
  <p>MTGA 即 Make T Great Again !</p>
 </details>

---

**目录**

* [快速开始（一键启动方式）](#快速开始GUI一键启动方式)
* [从脚本启动](#从脚本启动)
  * [第 0 步：环境准备](#第-0-步环境准备)
  * [第 1 步：生成自签名证书](#第-1-步生成自签名证书)
  * [第 2 步：让 Windows 信任你的 CA 证书](#第-2-步让-windows-信任你的-ca-证书)
  * [第 3 步：修改 Hosts 文件](#第-3-步修改-hosts-文件)
  * [第 4 步：运行本地代理服务器 (Python)](#第-4-步运行本地代理服务器-python)
  * [第 5 步：配置 Trae IDE](#第-5-步配置-trae-ide)

---

## 快速开始（GUI一键启动方式）

1. 双击运行 `MTGA_GUI.exe`（需要管理员权限）
2. 在打开的图形界面中，填写 API URL 和模型 ID
3. 点击"一键启动全部服务"按钮
4. 等待程序自动完成以下操作：
   - 生成并安装证书
   - 修改hosts文件
   - 启动代理服务器
5. 完成后，按照[第 5 步：配置 Trae IDE](#第-5-步配置-trae-ide)进行IDE配置

> 注意：首次运行可能需要允许防火墙访问权限

---

## 从脚本启动

### 第 0 步：环境准备

- 系统为 windows 10 以上
- 拥有管理员权限
- 安装 python 环境，推荐 python 3.10 以上
- 安装 git

### 第 1 步：生成自签名证书

打开 Git Bash:

```bash
# 切换到 ca 目录
cd "mtga/ca"

# 1. 生成 CA 证书 (ca.crt 和 ca.key)
./genca.sh
```

执行 `./genca.sh` 时，它会问你 "Do you want to generate ca cert and key? [yes/no]"，输入 `y` 并按回车。之后会要求填写一些信息：
*   `Country Name (2 letter code) []`: 填 `CN` (或其他国家代码)
*   其他字段（如 State, Locality, Organization, Common Name for CA）可以按需填写或留空，建议填`X`。Common Name 可以填 `MyLocalCA` 之类的。邮箱可以留空。

```bash
# 2. 生成 api.deepseek.com 的服务器证书 (api.deepseek.com.crt 和 api.deepseek.com.key)
# 这个脚本会使用同目录下的 api.deepseek.com.subj 和 api.deepseek.com.cnf 配置文件
./gencrt.sh api.deepseek.com
```

执行完毕后，在 `mtga\ca` 目录下你会找到以下重要文件：
*   `ca.crt` (你的自定义 CA 证书)
*   `ca.key` (你的自定义 CA 私钥 - **请勿泄露**)
*   `api.deepseek.com.crt` (用于本地代理服务器的 SSL 证书)
*   `api.deepseek.com.key` (用于本地代理服务器的 SSL 私钥 - **请勿泄露**)

### 第 2 步：让 Windows 信任你的 CA 证书

1.  找到 `mtga\ca\ca.crt` 文件。
2.  双击 `ca.crt` 文件，打开证书查看器。
3.  点击"安装证书..."按钮。
4.  选择"当前用户"或"本地计算机"。推荐选择"本地计算机"（这需要管理员权限），这样对所有用户生效。
5.  在下一个对话框中，选择"将所有的证书都放入下列存储"，然后点击"浏览..."。
6.  选择"受信任的根证书颁发机构"，然后点击"确定"。
7.  点击"下一步"，然后"完成"。如果弹出安全警告，选择"是"。

### 第 3 步：修改 Hosts 文件

**⚠️警告：执行这一步之后，你将无法访问原来的 deepseek 的api。网页使用不影响。**

你需要用管理员权限修改 Hosts 文件，将 `api.deepseek.com` 指向你的本地机器。

1.  Hosts 文件路径: `C:\Windows\System32\drivers\etc\hosts`
2.  以管理员身份，使用记事本（或其他文本编辑器）打开此文件。
3.  在文件末尾添加一行：
    ```
    127.0.0.1 api.deepseek.com
    ```
4.  保存文件。  

### 第 4 步：运行本地代理服务器 (Python)

**运行代理服务器之前：**

1.  **安装依赖**:
    ```bash
    pip install Flask requests
    ```
2.  **配置脚本**:
    *   打开 `trae_proxy.py` 文件。
    *   **修改 `TARGET_API_BASE_URL`**: 将其替换为你实际要连接的那个站点的 OpenAI 格式 API 的基础 URL (例如: `"https://your-api.example.com/v1"`)。
    *   **确认证书路径**: 脚本默认会从 `mtga\ca` 读取 `api.deepseek.com.crt` 和 `api.deepseek.com.key`。如果你的证书不在此路径，请修改 `CERT_FILE` 和 `KEY_FILE` 的值，或者将这两个文件复制到脚本指定的 `CERT_DIR`。

**运行代理服务器：**

打开命令提示符 (cmd) 或 PowerShell **以管理员身份运行** (因为要监听 443 端口)，然后执行：

```bash
python trae_proxy.py
```

如果一切顺利，你应该会看到服务器启动的日志。

### 第 5 步：配置 Trae IDE

1.  打开并登录 Trae IDE。
2.  在 AI 对话框中，点击右下角的模型图标，选择末尾的"添加模型"。
3.  **服务商**：选择 `DeepSeek`。
4.  **模型**：选择"自定义模型"。
5.  **模型 ID**：填写你在 Python 脚本中 `CUSTOM_MODEL_ID` 定义的值 (例如: `my-custom-local-model`)。
6.  **API 密钥**：
    *   如果你的目标 API 需要 API 密钥，并且 Trae 会将其通过 `Authorization: Bearer <key>` 传递，那么这里填写的密钥会被 Python 代理转发。
    *   Trae 配置 DeepSeek 时，API 密钥与 `remove_reasoning_content` 配置相关。我们的 Python 代理不处理这个逻辑，它只是简单地转发 Authorization 头部。你可以尝试填写你的目标 API 所需的密钥，或者一个任意的 `sk-xxxx` 格式的密钥。

7.  点击"添加模型"。
8.  回到 AI 聊天框，右下角选择你刚刚添加的自定义模型。

现在，当你通过 Trae 与这个自定义模型交互时，请求应该会经过你的本地 Python 代理，并被转发到你配置的 `TARGET_API_BASE_URL`。

**故障排除提示：**
*   **端口冲突**：如果 443 端口已被占用 (例如被 IIS、Skype 或其他服务占用)，Python 脚本会启动失败。你需要停止占用该端口的服务，或者修改 Python 脚本和 Nginx (如果使用) 监听其他端口 (但这会更复杂，因为 Trae 硬编码访问 `https://api.deepseek.com` 的 443 端口)。
*   **防火墙**：确保 Windows 防火墙允许 Python 监听 443 端口的入站连接 (尽管是本地连接 `127.0.0.1`，通常不需要特别配置防火墙，但值得检查)。
*   **证书问题**：如果 Trae 报错 SSL/TLS 相关错误，请仔细检查 CA 证书是否已正确安装到"受信任的根证书颁发机构"，以及 Python 代理是否正确加载了 `api.deepseek.com.crt` 和 `.key`。
*   **代理日志**：Python 脚本会打印一些日志，可以帮助你诊断问题。

这个方案比直接使用 vproxy + nginx 的方式更集成一些，将 TLS 终止和代理逻辑都放在了一个 Python 脚本中，更适合快速在 Windows 上进行原型验证。

---

## 引用

`ca`目录引用自`wkgcass/vproxy`仓库，感谢大佬！
