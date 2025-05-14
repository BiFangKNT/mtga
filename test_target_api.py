import requests
import json

# --- 用户配置 START ---
# 目标 API 的基础 URL
TARGET_API_BASE_URL = ""
# 你的 API 密钥 (请务必替换成你的真实有效密钥)
API_KEY = "sk-xxx" # 根据你的实际 API_KEY 填写
# 你想测试的模型 ID (如果目标 API 需要指定模型)
MODEL_ID = "" # 根据你的 CUSTOM_MODEL_ID 或目标 API 支持的模型填写
# --- 用户配置 END ---

def test_chat_completions():
    """
    测试 /chat/completions 端点。
    发送一个 POST 请求到目标 API，并打印响应。
    """
    if API_KEY == "sk-YOUR_ACTUAL_API_KEY_HERE":
        print("错误：请在脚本中设置你的真实 API_KEY。")
        return

    target_url = f"{TARGET_API_BASE_URL.rstrip('/')}/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    # 一个简单的 OpenAI 格式的请求体
    payload = {
        "model": MODEL_ID,
        "messages": [
            {"role": "user", "content": "你好，你是谁？"}
        ],
        "temperature": 0.7,
        "stream": False # 设置为 False 以获取完整的 JSON 响应，方便调试
    }
    
    print(f"正在向 {target_url} 发送请求...")
    print(f"请求头: {headers}")
    print(f"请求体: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(target_url, headers=headers, json=payload, timeout=60)
        
        print("\n--- 响应 ---")
        print(f"状态码: {response.status_code}")
        print("响应头:")
        for key, value in response.headers.items():
            print(f"  {key}: {value}")
        
        print("\n响应体:")
        try:
            # 尝试以 JSON 格式解析和打印响应体
            response_json = response.json()
            print(json.dumps(response_json, indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            # 如果不是有效的 JSON，则直接打印文本内容
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"\n请求过程中发生错误: {e}")
    except Exception as e:
        print(f"\n发生未知错误: {e}")

if __name__ == "__main__":
    test_chat_completions()