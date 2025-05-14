from flask import Flask, request, jsonify, Response
import requests
import ssl
import os
import logging

app = Flask(__name__)

# --- 用户配置 START ---
# 你实际的目标 OpenAI 格式 API 的基础 URL
# 例如: "https://your-reverse-api.com/v1"
TARGET_API_BASE_URL = "YOUR_REVERSE_ENGINEERED_API_ENDPOINT_BASE_URL"

# 你将在 Trae IDE 中配置的模型 ID，这个随意填，Trae 里的模型 ID 与之对应
CUSTOM_MODEL_ID = "CUSTOM_MODEL_ID"

# SSL 证书和私钥文件的路径
# 脚本会尝试从 c:\github\mtga\misc\ca\ 读取，如果找不到，你需要将它们复制到脚本同目录
# 或者修改这里的路径
# 获取脚本文件所在的绝对路径
# __file__ 是 Python 中的一个内置变量，表示当前脚本的文件名
SCRIPT_FILE_PATH = os.path.abspath(__file__)
# 使用 os.path.dirname 获取脚本文件所在的目录
SCRIPT_PARENT_DIR = os.path.dirname(SCRIPT_FILE_PATH)
# 定义 ca 目录的路径，使其相对于脚本文件位置 (假设 ca 目录与脚本在同一目录下)
CERT_DIR = os.path.join(SCRIPT_PARENT_DIR, "ca")

CERT_FILE = os.path.join(CERT_DIR, 'api.deepseek.com.crt')
KEY_FILE = os.path.join(CERT_DIR, 'api.deepseek.com.key')
# --- 用户配置 END ---

# 设置日志记录
logging.basicConfig(level=logging.INFO)

@app.route('/models', methods=['GET'])
def get_models():
    """
    处理到 /models 的 GET 请求，返回 Trae IDE 期望的模型列表格式。
    这里我们只返回一个自定义模型。
    """
    app.logger.info(f"Received request for /models")
    # Trae 会检查这些字段，特别是 'id' 和 'owned_by'
    model_data = {
        "object": "list",
        "data": [
            {
                "id": CUSTOM_MODEL_ID, # 使用 CUSTOM_MODEL_ID 变量
                "object": "model",
                "owned_by": "deepseek", # 模型所有者，确保这个字段存在
            }
        ]
    }
    app.logger.info(f"Responding to /models with: {model_data}")
    return jsonify(model_data)





# ------------------------------------------- 下面一般来说不需要修改 ---------------------------------------------------




@app.route('/chat/completions', methods=['POST'])
def chat_completions():
    """
    处理到 /chat/completions 的 POST 请求。
    它会验证请求是否为有效的 JSON，然后将请求转发到配置的目标 API 地址。
    支持流式和非流式响应。
    """
    app.logger.info(f"Received request for /chat/completions")
    app.logger.debug(f"Request headers: {request.headers}")

    # 尝试获取 JSON 数据
    # request.get_json(silent=True) 会在 mimetype 不正确或 JSON 解析失败时返回 None
    request_data = request.get_json(silent=True)

    if request_data is None:
        app.logger.error("Failed to parse JSON from request or request is not JSON.")
        app.logger.error("Content-Type: %s", request.headers.get("Content-Type"))
        # 记录原始请求数据以帮助调试，注意数据大小可能很大
        try:
            raw_data_sample = request.get_data(as_text=True)
            if len(raw_data_sample) > 500: # 只记录一部分，避免日志过长
                raw_data_sample = raw_data_sample[:500] + "..."
            app.logger.error("Request data sample: %s", raw_data_sample)
        except Exception as e:
            app.logger.error("Error getting raw request data: %s", e)
            
        return jsonify({
            "error": "Invalid JSON or Content-Type",
            "message": "The request body must be valid JSON and the Content-Type header must be 'application/json'."
        }), 400

    app.logger.debug(f"Request JSON: {request_data}")

    # 从 Trae 的请求中获取 Authorization header (通常包含 API Key)
    auth_header = request.headers.get('Authorization')
    forward_headers = {'Content-Type': 'application/json'}
    if auth_header:
        forward_headers['Authorization'] = auth_header

    try:
        target_url = f"{TARGET_API_BASE_URL.rstrip('/')}/chat/completions"
        app.logger.info(f"Forwarding request to: {target_url}")

        # 从解析后的 request_data 中获取 stream 参数
        is_stream = request_data.get('stream', False)
        app.logger.info(f"Stream mode: {is_stream}")

        response_from_target = requests.post(
            target_url,
            json=request_data, # 使用解析后的 request_data
            headers=forward_headers,
            stream=is_stream,
            timeout=300  # 为大模型响应设置较长超时
        )
        response_from_target.raise_for_status()  # 如果目标 API 返回错误，则抛出异常

        if is_stream:
            app.logger.info("Streaming response back to client.")
            def generate_stream():
                for chunk in response_from_target.iter_content(chunk_size=None): # 直接透传原始字节块
                    yield chunk
            return Response(generate_stream(), content_type=response_from_target.headers.get('content-type', 'text/event-stream'))
        else:
            app.logger.info("Returning non-streamed JSON response.")
            return jsonify(response_from_target.json()), response_from_target.status_code

    except requests.exceptions.HTTPError as e:
        app.logger.error(f"HTTP error from target API: {e.response.status_code} - {e.response.text}")
        return jsonify({"error": f"Target API error: {e.response.status_code}", "details": e.response.text}), e.response.status_code
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Request exception while contacting target API: {e}")
        return jsonify({"error": f"Error contacting target API: {str(e)}"}), 503 # Service Unavailable
    except Exception as e:
        app.logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        return jsonify({"error": "An internal server error occurred"}), 500

if __name__ == '__main__':
    if TARGET_API_BASE_URL == "YOUR_REVERSE_ENGINEERED_API_ENDPOINT_BASE_URL":
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!! 请务必修改脚本中的 'TARGET_API_BASE_URL' 为你实际的 API 地址 !!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        exit(1)

    if not (os.path.exists(CERT_FILE) and os.path.exists(KEY_FILE)):
        print(f"错误: 证书文件 {CERT_FILE} 或私钥文件 {KEY_FILE} 未找到。")
        print(f"请确保这些文件存在于 '{CERT_DIR}' 目录中，")
        print(f"或者将它们从 'c:\\github\\mtga\\misc\\ca' 复制到脚本期望的位置，")
        print("或者直接在脚本中修改 CERT_FILE 和 KEY_FILE 的路径。")
        exit(1)

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(CERT_FILE, KEY_FILE)

    print(f"启动代理服务器，监听 https://0.0.0.0:443")
    print(f"确保你的 hosts 文件已将 api.deepseek.com 指向 127.0.0.1")
    print(f"目标 LLM API 地址: {TARGET_API_BASE_URL}")
    print(f"为 Trae 配置的模型 ID: {CUSTOM_MODEL_ID}")
    print("注意: 监听 443 端口通常需要管理员权限运行此脚本。")
    
    try:
        app.run(host='0.0.0.0', port=443, ssl_context=ssl_context, debug=False)
    except PermissionError:
        print("错误: 权限不足，无法监听 443 端口。请尝试以管理员身份运行此脚本。")
    except OSError as e:
        if "address already in use" in str(e).lower():
            print("错误: 端口 443 已被占用。请检查是否有其他服务（如 IIS, Skype 等）占用了该端口。")
        else:
            print(f"启动服务器时发生 OS 错误: {e}")