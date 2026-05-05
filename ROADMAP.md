# 路线图

## 文档定位

这份文档用于定义 `v2.4.0` 到 `v2.6.0` 的产品方向、版本边界和协作规则。

- 目标是先固定里程碑与约束，再让 Admin 任务、issue 或 Contributor PR 在明确边界内推进。
- 这不是完整设计文档；实现细节应在具体 issue、设计讨论、Admin 任务或 Contributor PR 中展开。
- 如路线图与临时实现方案冲突，以路线图约束为准。

## 状态约定

- `Planned`：已确认方向，未开始实现。
- `In Design`：正在补齐设计边界，暂不建议直接编码。
- `In Progress`：已有实现工作进行中。
- `Done`：里程碑目标已完成并发布。

## 路线图总览

| 版本     | 核心主题             | 主要产出                                                              | 状态        |
| -------- | -------------------- | --------------------------------------------------------------------- | ----------- |
| `v2.4.0` | 多供应商上游适配     | MLiteLLM 执行层、上游适配层、非 OpenAI 上游转发能力                   | `Done`      |
| `v2.5.0` | 结构化代理日志与并发 | `trace` 体系、代理日志页、单模型并发处理                              | `Done`      |
| `v2.6.0` | 模型路由重构         | `published_model / target / failover_pool` 配置模型、动态路由、热切换 | `In Design` |

## 规划原则

- 不继续扩展旧的“单当前映射 + 配置组兼任路由对象”心智模型。
- 每个版本只解决一个主问题，避免跨里程碑混合提交。
- 新能力优先服务后续版本演进，避免一次性做完整大重构。
- 路由、日志、并发等基础能力应按版本顺序渐进落地。

## MLiteLLM 使用边界

- MLiteLLM 是项目内置维护的精简执行层模块，负责多 provider 调用、请求归一化、响应归一化和 provider 兼容补丁。
- MTGA 自己维护“产品层配置模型”，前端仍以用户可理解的对象暴露配置，不直接把 MLiteLLM 内部调用参数作为主要心智模型。
- `trace`、代理日志页、查询接口、清理策略、热应用、路由、fallback、retry、cooldown 等产品语义属于 MTGA 自有能力，不由 MLiteLLM 反向决定配置模型。
- 当 MLiteLLM 能覆盖 provider 适配细节时，应优先复用 MLiteLLM 能力，而不是在代理主流程里重复实现 provider 调用细节。
- 当 MTGA 的产品语义强于执行层调用语义时，应由 MTGA 配置 schema 编译为 MLiteLLM 调用参数，而不是反过来用执行层参数倒逼前端设计。

## 当前主要代码落点

- 后端主入口：[python-src/modules/proxy/proxy_app.py](./python-src/modules/proxy/proxy_app.py)
- 传输层：[python-src/modules/proxy/proxy_transport.py](./python-src/modules/proxy/proxy_transport.py)
- 代理运行时：[python-src/modules/proxy/proxy_runtime.py](./python-src/modules/proxy/proxy_runtime.py)
- 配置读写：[python-src/modules/services/config_service.py](./python-src/modules/services/config_service.py)
- 前端状态：[app/composables/useMtgaStore.ts](./app/composables/useMtgaStore.ts)
- 现有配置页：[app/components/panels/ConfigGroupPanel.vue](./app/components/panels/ConfigGroupPanel.vue)
- 现有全局页：[app/components/panels/GlobalConfigPanel.vue](./app/components/panels/GlobalConfigPanel.vue)
- 现有日志区：[app/components/LogPanel.vue](./app/components/LogPanel.vue)
- 左侧导航：[app/app.vue](./app/app.vue)

## 里程碑

### `v2.4.0` 多供应商上游适配

**目标**

- 在 `proxy_app` 中引入 MLiteLLM 执行层，使 OpenAI Chat Completions 请求可以转发到 Anthropic、Google 等上游。
- 保持当前 UI、配置格式和 `/models` 语义基本不变。
- 为后续 `trace` 与动态路由改造预留清晰的上游适配接口。
- 将 MLiteLLM 接入定位为“后端执行层改造”，而不是前端配置模型改造。

**范围**

- 抽出“上游调用适配层”，把供应商差异从 `proxy_app` 主流程中隔离。
- 保持现有“单当前映射”模式。
- 兼容流式与非流式请求。
- 保留现有系统提示词处理链路。
- 保留当前“用户配置 -> 运行时配置”转换关系，不把 MLiteLLM 内部调用参数直接暴露到 UI。

**本版本不做**

- 不做多发布模型。
- 不做新的配置 schema。
- 不做通用请求体改写规则，不新增配置组级请求变换 schema。
- 不做故障转移。
- 不做日志页重构。
- 不接入执行层的用户、预算、virtual key 等代理管理能力。
- 不把 MLiteLLM 内部配置或管理 API 直接变成用户配置面。

**预期交付物**

- MLiteLLM 内置执行层接入。
- 统一的上游请求构造与响应归一化入口。
- 至少 2 个非 OpenAI provider 的最小可用适配。
- MTGA 运行时配置到 MLiteLLM 调用参数的映射约束说明。
- 对流式、非流式和异常响应的回归测试。
- provider 支持范围与限制说明文档。

**建议任务拆分**

1. 后端基础设施：引入 MLiteLLM，建立上游适配入口，并补齐 MTGA 运行时配置到 MLiteLLM 调用参数的映射层。
2. 后端 provider 打通：接入至少 2 个非 OpenAI provider，并统一流式、非流式响应归一化行为。
3. 测试补强：覆盖流式、非流式、异常响应回归，确保现有请求链路不回退。
4. 文档收口：补充 provider 支持范围、已知限制和配置映射约束。

**完成标准**

- 在不改现有配置页的前提下，至少支持 2 个非 OpenAI 上游的对话转发。
- SSE 与非 SSE 行为不回退。
- `pnpm py:check` 通过。

### `v2.5.0` 结构化代理日志与并发

**目标**

- 将代理日志从普通字符串升级为结构化 `trace`。
- 新增“代理日志”页，用于查看请求列表与详情。
- 验证并加固当前单模型映射架构下的并发请求处理。
- 将右侧日志区收敛为摘要日志，而不是完整代理详情。
- 明确 `trace` 是 MTGA 自有的数据模型与产品能力，不随执行层选型外包出去。

**范围**

- 后端新增 trace 总线或 trace 存储，不再复用纯字符串 `log_bus` 作为代理详情载体。
- 前端新增“代理日志”页，交互可参考现有“系统提示词”页的列表区。
- 右侧运行日志区只记录一行摘要，例如“收到代理请求”或“已转发到上游”。
- 对现有代理运行时做并发安全审计和必要加固，重点保证并发请求下的 trace 完整性。
- 并发范围仅限“当前单映射模型下的并发处理”，不提前引入多发布模型路由。
- 如 MLiteLLM 提供 raw request/response 或 provider 事件，只作为 trace 打点的数据来源之一，不作为日志页主存储模型。
- trace 存储必须独立于纯字符串 `log_bus`，`log_bus` 只保留面向右侧运行日志的摘要文本。
- 请求体、响应体和错误详情必须有脱敏、截断与保留策略，不保存可泄露的鉴权信息。
- 流式请求以生成器结束、上游异常或客户端断开作为 trace 结束点，不以 Flask handler 返回 `Response` 作为结束点。
- 清空代理日志不应破坏正在进行中的 trace；清空语义必须明确 active trace 的处理方式。

**本版本不做**

- 不改配置 schema。
- 不做通用请求体改写规则。
- 不做 `published_model`、`target`、`failover_pool`。
- 不让 `/models` 返回多个模型。
- 不把 PR #79 当前的“配置组轮询”语义直接合入主线。
- 不用执行层 callback 或第三方 observability 页面直接替代“代理日志”页。

**预期交付物**

- `ProxyTrace` 数据结构与生命周期定义。
- trace 查询接口，至少包含列表、详情、清空。
- `proxy_app` 请求处理全链路 trace 打点。
- 并发代理运行时。
- “代理日志”页列表与详情视图。
- MLiteLLM provider 事件与 `ProxyTrace` 的字段映射策略说明。
- 请求体、响应体、鉴权信息脱敏、截断与保留策略。
- 并发请求、trace 完整性、清理逻辑测试。
- trace 字段、并发边界、清空语义与内存保留策略说明文档。

**建议任务拆分**

1. 后端 trace 基础：定义 `ProxyTrace` 数据结构、生命周期和存储保留策略，并提供列表、详情、清空接口。
2. 后端 trace 打点：把 `proxy_app` 全链路请求处理接入 trace，并明确 MLiteLLM provider 事件到 `ProxyTrace` 的字段映射边界。
3. 后端并发安全：审计并加固现有代理运行时，确保并发场景下 trace 完整性不丢失。
4. 前端日志页：新增“代理日志”页的列表与详情视图，支持查看请求体、响应体、状态码、耗时和错误。
5. 前端日志收敛：调整右侧日志区，仅保留代理摘要日志，避免与 trace 详情重复。
6. 测试与文档：补充并发请求、流式结束、客户端断开、trace 完整性、清理逻辑测试，并说明 trace 字段、并发边界与内存保留策略。

**完成标准**

- 同一模型可同时处理多个请求，不互相阻塞。
- 并发请求可在“代理日志”页中独立追踪。
- 日志页能定位单次请求的完整请求体与响应体。
- 流式请求在完成、异常或客户端断开时都能落到明确的 trace 终态。
- 清空代理日志不会导致正在处理中的请求 trace 丢失或结束回写失败。
- `pnpm py:check` 与 `pnpm app:check` 通过。

### `v2.6.0` 模型路由重构

**目标**

- 引入新的路由架构：`published_model + primary_target + optional failover_pool`。
- `/models` 返回全部启用的发布模型。
- 请求按 `request.model` 动态路由，不再依赖线程内固定单一映射。
- 将“代理配置组”页和“全局配置”页统一为“模型路由”。
- 配置保存后可热切换到运行中代理，无需重启线程。
- 在不牺牲 MTGA 配置语义的前提下，尽量复用 MLiteLLM provider 调用与兼容能力；路由、fallback、cooldown 由 MTGA 路由层定义。

**范围**

- 后端配置 schema 从旧的 `config_groups + current_config_index + mapped_model_id` 迁移到新结构。
- 前端“模型路由”页负责管理：
  - `targets`
  - `failover_pools`
  - `published_models`
- 请求体变换规则应在新模型路由下重新设计，不继续挂在旧 `config_group` 上：
  - `published_model` 级：用于定义对外暴露模型的稳定请求改写行为。
  - `target` 级：用于定义特定上游目标的兼容性请求改写行为。
- 每个 `published_model` 只能绑定一个 `primary_target_id`。
- 每个 `published_model` 可选一个 `failover_pool_id`。
- 故障转移第一阶段只要求支持 `429` 冷却切换。
- 冷却状态应以 `target_id` 为键，而不是 pool member 局部状态。
- `/models` 只返回启用的 `published_model.name`。
- 允许同一 `target` 被多个模型、多个故障转移池复用。
- 路由配置保存后应直接热应用到运行中代理，仅影响后续新请求；已在处理中的请求继续沿用请求开始时解析出的路由。
- 后端可以把 `target / failover_pool / published_model` 编译为 MTGA 路由层的执行计划，再下发为 MLiteLLM provider 调用参数，但不把执行层对象直接上浮为前端配置对象。

**本版本不做**

- 不做模型能力自动探测。
- 不做无限级故障转移链。
- 不做复杂流量调度策略。
- 不做“主目标多成员”的另一套语义。
- 不接受继续扩展旧 `config_group` 语义来模拟新模型路由。
- 不直接把执行层的 `model_list`、`fallbacks`、virtual key、access group 等对象作为前端配置模型。

**预期交付物**

- 新配置 schema 与类型定义。
- 旧 schema 到新 schema 的迁移逻辑。
- `request.model -> published_model -> primary_target/failover_pool` 解析器。
- `published_model / target / failover_pool -> MTGA 路由执行计划 -> MLiteLLM 调用参数` 编译层或适配层。
- `published_model` / `target` 级请求体变换规则设计与落地。
- 路由配置热切换能力。
- `/models` 返回全部启用发布模型。
- 基于 `target_id` 的 `429` 冷却状态管理。
- 故障转移池按顺序尝试执行器。
- 前端“模型路由”页及旧入口迁移。
- 迁移、动态路由、热切换、`429` 故障转移和 target 复用测试。
- 术语、迁移说明和故障转移风险说明文档。

**建议任务拆分**

1. 配置模型重构：定义新 schema 与类型，并实现旧 schema 到新 schema 的迁移逻辑。
2. 路由解析主链路：实现 `request.model -> published_model -> primary_target/failover_pool` 解析器，并让 `/models` 返回全部启用发布模型。
3. 执行层接线：实现 MTGA 路由对象到路由执行计划和 MLiteLLM 调用参数的编译层，并支持运行中配置热应用。
4. 故障转移内核：实现基于 `target_id` 的 `429` 冷却状态管理和故障转移池顺序执行器。
5. 前端路由页：完成“模型路由”页信息架构与 `targets`、`failover_pools`、`published_models` 三类对象管理。
6. 旧入口迁移：移除旧“代理配置组”页与“全局配置”页入口，并完成新旧交互路径切换。
7. 测试与文档：覆盖迁移、动态路由、热切换、`429` 故障转移、target 复用等行为，并补充术语、迁移说明和风险说明。

**完成标准**

- 用户无需重启代理，即可通过不同发布模型命中不同上游目标。
- 编辑并保存运行中的“模型路由”配置后，无需重启代理线程即可对后续请求生效。
- `/models` 可列出全部启用发布模型。
- 主目标返回 `429` 时，可按配置切换到故障转移池中的下一个可用目标。
- 同一 `target` 复用于多个模型和多个池时行为一致。
- `pnpm py:check` 与 `pnpm app:check` 通过。

## 跨版本依赖关系

- `v2.4.0` 提供统一的上游适配接口，为 `v2.5.0` 和 `v2.6.0` 提供稳定调用边界。
- `v2.5.0` 提供结构化 trace 和并发基础设施，为 `v2.6.0` 的动态路由调试提供可观测性。
- `v2.6.0` 才是新的稳定路由模型，不建议在 `v2.4.0` 或 `v2.5.0` 提前做部分 schema 重构。
- 通用请求体改写规则应依附 `v2.6.0` 的新对象模型设计，不应继续叠加到旧 `config_group`。
- MLiteLLM 的引入顺序应是先适配 provider，再补 trace，最终由 `v2.6.0` 的 MTGA 路由层统一接管动态路由与故障转移语义。

## `v2.6.0` 目标状态

### 目标对象模型

```yaml
targets:
  - id: claude-main
    provider: anthropic
    api_base: https://example.com
    api_key: xxx
    middle_route: /v1
    upstream_model: claude-3-7-sonnet

failover_pools:
  - id: claude-failover
    trigger_statuses: [429]
    cooldown_seconds: 10
    members:
      - target_id: claude-backup-1
      - target_id: claude-backup-2

published_models:
  - name: sonnet-proxy
    enabled: true
    primary_target_id: claude-main
    failover_pool_id: claude-failover
```

### 稳定约束

- 同一个 `target` 可被多个 `published_model`、多个 `failover_pool` 复用。
- “多对一”的真实需求收敛为“主目标 + 故障转移池”，不单独设计主池多成员语义。
- 不做模型能力自动识别与兼容性校验，风险由用户自行承担。

### 与 MLiteLLM 的概念映射

- `target` 对应一个可复用的上游目标定义，可编译为 MLiteLLM provider 调用参数。
- `published_model` 是 MTGA 对用户暴露的稳定模型名，不要求与 MLiteLLM 请求中的 `model` 一一同名，但可在执行层映射到同一上游模型。
- `failover_pool` 是 MTGA 的产品语义对象，由 MTGA 路由层映射为 fallback、retry、cooldown 执行计划。
- `target_id` 仍是 MTGA 内部稳定标识；即使底层调用经过 MLiteLLM，也不放弃以 `target_id` 为键的产品语义与调试语义。

## 附录 A：`v2.5.0` trace 草案

```ts
type ProxyTraceStatus = "active" | "completed" | "failed" | "cancelled";

type ProxyTraceEvent = {
  at: string;
  kind: string;
  message?: string;
  data?: Record<string, unknown>;
};

type ProxyTraceBodyCapture = {
  value?: unknown;
  bytes?: number;
  truncated?: boolean;
  truncated_reason?: "size_limit" | "stream_limit" | "unsupported_type";
  redacted?: boolean;
};

type ProxyTrace = {
  trace_id: string;
  request_id: string;
  status: ProxyTraceStatus;
  method: string;
  request_path: string;
  route_mode?: "reverse_hosts" | "trae_native" | "trae_official_base_url";
  provider?: string;
  request_api?: "chat_completions" | "responses";
  request_model?: string;
  client_model?: string;
  resolved_target_label?: string;
  target_api_base_url?: string;
  upstream_model?: string;
  target_model?: string;
  is_stream: boolean;
  status_code?: number;
  started_at: string;
  first_chunk_at?: string;
  ended_at?: string;
  duration_ms?: number;
  chunk_count?: number;
  finish_reason?: string;
  request_body?: ProxyTraceBodyCapture;
  response_body?: ProxyTraceBodyCapture;
  error?: string;
  events: ProxyTraceEvent[];
};
```

## 协作与合并规则

- Contributor 贡献默认通过 PR；Admin 可按同样任务边界直接提交或合并，不受 PR 流程约束。
- Contributor 单个 PR 只覆盖一个里程碑，不跨 `v2.4.0`、`v2.5.0`、`v2.6.0`；Admin 直接提交也应避免跨里程碑混合改动。
- Contributor 设计型 PR 必须先在 issue 中确认术语和边界，再进入实现；Admin 直接推进设计时也应先在 issue、设计讨论或路线图中固定边界。
- 涉及 Python 的变更必须运行 `pnpm py:check`。
- 涉及 JS/TS/Vue 的变更必须运行 `pnpm app:check`。
- 涉及配置 schema 的变更必须写迁移说明。
- 涉及日志或 trace 的变更必须说明数据保留策略和内存上限。
- 涉及代理并发的变更必须提供至少一个并发行为测试。
- 涉及 UI 的 Contributor PR 必须附截图或录屏；Admin 直接提交 UI 变更时也应在交付说明中说明验证方式。

## 对现有 PR 的处理建议

- PR #79 不建议按当前“配置组轮询 / 全局开关”语义直接合并。
- 可复用部分可以拆出后按里程碑分别贡献：
  - `429` 冷却内核
  - 目标切换执行逻辑
  - 每目标独立 `middle_route` 支持
- 若扩展 MLiteLLM 路由相关能力，应优先拆成“执行层能力”而不是直接引入执行层对象到 UI。
- 上述能力应服务 `v2.6.0` 的 `target + failover_pool` 模型，而不是继续强化旧 `config_group`。

## 暂不接受的贡献方向

- 继续把 `config_group` 扩展成多模型路由核心对象。
- 继续向旧 `config_group` 追加通用请求体改写规则、路由规则等长期产品语义。
- 在 `v2.5.0` 之后仍把代理详情日志做成纯字符串拼接。
- 未完成并发 trace 设计就先做复杂日志 UI。
- 在安全边界未明确前，仅做“允许空鉴权 key”的放宽而不讨论监听策略。
- 未经设计确认就把 MLiteLLM 内部调用术语直接暴露为最终用户配置面。

## 对外发布建议

- 新增一份 GitHub Projects Roadmap。
- 为 `v2.4.0`、`v2.5.0`、`v2.6.0` 分别建立 milestone。
- 所有相关 issue 使用统一标签，例如：
  - `roadmap:v2.4.0`
  - `roadmap:v2.5.0`
  - `roadmap:v2.6.0`
  - `area:proxy`
  - `area:frontend`
  - `area:config`
  - `area:trace`
  - `needs-design`
