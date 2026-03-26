# MTGA v2.4.0 Provider 支持说明

## 定位

`v2.4.0` 把 LiteLLM 作为后端执行层引入，当前下游统一暴露 **OpenAI Chat Completions API**。

- 前端配置模型时通过 `提供商` 字段显式声明上游类型。
- `/models` 仍由 MTGA 本地代理返回当前映射模型，不直接透出 LiteLLM 原生对象。
- 系统提示词采集与增量覆盖链路对下游 `messages` 生效；当上游使用 `openai_response` 时，MTGA 会在代理层转换为 Responses 所需的 `input`。

## Provider 选择规则

MTGA 不再通过模型名前缀或 `API URL` 域名推断 provider，而是直接使用配置组中的 `提供商` 字段。

当前支持值：

- `openai_chat_completion`
- `openai_response`
- `anthropic`
- `gemini`

旧配置如果仍写成 `openai`，会自动兼容为 `openai_chat_completion`。

## 配置字段到 LiteLLM 的映射

| MTGA 配置字段 | LiteLLM 调用参数                      | 说明                                                                                              |
| ------------- | ------------------------------------- | ------------------------------------------------------------------------------------------------- |
| `提供商`      | `custom_llm_provider` / 请求 API 类型 | 决定 MTGA 是调用上游 `/chat/completions` 还是 `/responses`，以及 LiteLLM 使用哪个 provider 适配器 |
| `API URL`     | `base_url`                            | 作为上游基础地址传入 LiteLLM                                                                      |
| `实际模型 ID` | `model`                               | OpenAI 两类 provider 保持原值；Anthropic / Gemini 会组装成 `provider/model_id`                    |
| `API Key`     | `api_key`                             | 优先使用配置组里的 key                                                                            |
| `中间路由`    | 上游基路径前缀                        | `chat` 与 `models` 分开构造；Gemini 未显式填写时默认使用 `/v1beta`                                |
| `映射模型 ID` | 不直接传给 LiteLLM                    | 继续作为 MTGA 对外暴露的稳定模型名                                                                |

## 当前最小支持范围

### OpenAI Chat Completion

- `提供商`：`openai_chat_completion`
- 上游按 Chat Completions 语义调用。
- MTGA 下游直接输出 Chat Completions JSON / SSE。
- `中间路由` 会自动拼到 `base_url` 上。

### OpenAI Response

- `提供商`：`openai_response`
- 上游直接按 Responses API 语义调用。
- MTGA 会把下游 `messages` 请求转换成 Responses `input`，再把上游结果转换回 Chat Completions JSON / SSE。
- `中间路由` 会自动拼到 `base_url` 上。

### Anthropic

- `提供商`：`anthropic`
- 推荐 `API URL`：`https://api.anthropic.com`
- 推荐 `实际模型 ID`：`claude-...`
- 默认 `中间路由`：`/v1`
- 实际请求会在该基路径后补 `/messages`

### Gemini

- `提供商`：`gemini`
- 推荐 `API URL`：`https://generativelanguage.googleapis.com`
- 推荐 `实际模型 ID`：`gemini-...`
- 默认 `中间路由`：`/v1beta`
- 实际请求会在该基路径后补 `/models/{model}:generateContent`

## 流式与非流式语义

- 当客户端请求流式，且上游 provider 走 Chat Completions 时，MTGA 会向 LiteLLM 发起流式调用，并向下游输出 Chat Completions SSE。
- 当客户端请求非流式时，MTGA 返回普通 Chat Completions JSON。
- 当上游 provider 为 `openai_response`，或运行时配置强制 `stream=false` 时，MTGA 会拿到最终结果后在代理侧模拟 Chat Completions SSE，再返回给客户端。

## 已知限制

- 当前版本只解决“单当前映射”模式下的多 provider 转发，不包含多发布模型、故障转移、LiteLLM Proxy 管理能力或新的配置 schema。

## 建议配置示例

### OpenAI Chat Completion

```yaml
provider: openai_chat_completion
api_url: https://example.com
model_id: gpt-4o-mini
api_key: sk-...
middle_route: /v1
```

### OpenAI Response

```yaml
provider: openai_response
api_url: https://api.openai.com
model_id: gpt-5
api_key: sk-...
middle_route: /v1
```

### Anthropic

```yaml
provider: anthropic
api_url: https://api.anthropic.com
model_id: claude-3-7-sonnet-latest
api_key: sk-ant-...
middle_route: /v1
```

### Gemini

```yaml
provider: gemini
api_url: https://generativelanguage.googleapis.com
model_id: gemini-2.5-pro
api_key: AIza...
middle_route: /v1beta
```
