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

| 版本     | 核心主题             | 主要产出                                                              | 状态   |
| -------- | -------------------- | --------------------------------------------------------------------- | ------ |
| `v2.4.0` | 多供应商上游适配     | MLiteLLM 执行层、上游适配层、非 OpenAI 上游转发能力                   | `Done` |
| `v2.5.0` | 结构化代理日志与并发 | `trace` 体系、代理日志页、单模型并发处理                              | `Done` |
| `v2.6.0` | 模型路由重构         | `published_model / target / failover_pool` 配置模型、动态路由、热切换 | `Done` |

## 规划原则

- 不继续扩展旧的“单当前映射 + 配置组兼任路由对象”心智模型。
- 每个版本只解决一个主问题，避免跨里程碑混合提交。
- 新能力优先服务后续版本演进，避免一次性做完整大重构。
- 路由、日志、并发等基础能力应按版本顺序渐进落地。

## MLiteLLM 使用边界

- MLiteLLM 中的 `M` 指 MTGA；它是项目内置并由 MTGA 维护的精简执行层模块，不是外部产品或不可控第三方服务边界。
- MLiteLLM 负责多 provider 调用、请求归一化、响应归一化和 provider 兼容补丁。
- MLiteLLM 提供最终出站 JSON body patch 扩展点；该扩展点在 provider 适配之后、HTTP 请求发出之前执行，属于用户自定义高级能力。
- MTGA 自己维护“产品层配置模型”，前端仍以用户可理解的对象暴露配置，不直接把 MLiteLLM 内部调用参数作为主要心智模型。
- `trace`、代理日志页、查询接口、清理策略、热应用、路由、fallback、retry、cooldown 等产品语义属于 MTGA 自有能力，不由 MLiteLLM 反向决定配置模型。
- 当 MLiteLLM 能覆盖 provider 适配细节时，应优先复用 MLiteLLM 能力，而不是在代理主流程里重复实现 provider 调用细节。
- 当 MTGA 的产品语义强于执行层调用语义时，应由 MTGA 配置 schema 编译为 MLiteLLM 调用参数，而不是反过来用执行层参数倒逼前端设计。
- 文档中区分“MTGA 路由层”和“MLiteLLM 执行层”只是为了明确仓库内部职责边界：前者维护产品语义和路由状态，后者维护 provider 调用兼容性。

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
- MTGA 路由层只负责把 `published_model / target / failover_pool` 编译为 route plan 与 MLiteLLM 调用参数；provider 级请求体兼容、字段删除/补齐、响应归一化继续由 MLiteLLM 或现有 upstream adapter 负责。
- `target.request_body_patch` 可配置 MLiteLLM 出站 JSON Patch；它只传递到 MLiteLLM 执行层，不由 MTGA 路由层解释 provider 字段。
- 每个 `published_model` 只能绑定一个 `primary_target_id`。
- 每个 `published_model` 可选一个 `failover_pool_id`。
- 故障转移第一阶段只要求支持 `429` 冷却切换，以及 retry 机会耗尽后的可重试网络运输错误切换；只有 `429` 写入 target-level cooldown。
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
- 不在 MTGA 路由层重复实现 provider 级请求体兼容逻辑。
- 不在 MTGA 路由层实现任意请求体改写 DSL；用户自定义出站请求体补丁由 MLiteLLM 执行。
- 不直接把执行层的 `model_list`、`fallbacks`、virtual key、access group 等对象作为前端配置模型。

**预期交付物**

- 新配置 schema 与类型定义。
- 旧 schema 到新 schema 的迁移逻辑。
- `request.model -> published_model -> primary_target/failover_pool` 解析器。
- `published_model / target / failover_pool -> MTGA 路由执行计划 -> MLiteLLM 调用参数` 编译层或适配层。
- MTGA 路由层与 MLiteLLM/upstream adapter 的请求编译边界说明。
- 路由配置热切换能力。
- `/models` 返回全部启用发布模型。
- MLiteLLM 出站 JSON body patch 协议与 `target.request_body_patch` 配置入口。
- 基于 `target_id` 的 `429` 冷却状态管理。
- retry 机会耗尽后的可重试网络运输错误故障转移判断。
- 故障转移池按顺序尝试执行器。
- 前端“模型路由”页及旧入口迁移。
- 迁移、动态路由、热切换、`429` 故障转移、网络错误故障转移和 target 复用测试。
- 术语、迁移说明和故障转移风险说明文档。

**建议任务拆分**

> 可按以下任务分步设计、合并和验证；但 `v2.6.0` 对用户应作为一次完整模型路由切换发布，未达到完成标准前不标记 `Done`，不发布半迁移状态。

1. 配置模型重构：定义新 schema 与类型，并实现旧 schema 到新 schema 的迁移逻辑。
2. 路由解析主链路：实现 `request.model -> published_model -> primary_target/failover_pool` 解析器，并让 `/models` 返回全部启用发布模型。
3. 执行层接线：实现 MTGA 路由对象到路由执行计划和 MLiteLLM 调用参数的编译层，并支持运行中配置热应用。
4. 故障转移内核：实现基于 `target_id` 的 `429` 冷却状态管理、retry 耗尽后的网络错误故障转移入口和故障转移池顺序执行器。
5. 前端路由页：完成“模型路由”页信息架构与 `targets`、`failover_pools`、`published_models` 三类对象管理。
6. 旧入口迁移：移除旧“代理配置组”页与“全局配置”页入口，并完成新旧交互路径切换。
7. 测试与文档：覆盖迁移、动态路由、热切换、`429` 故障转移、网络错误故障转移、target 复用等行为，并补充术语、迁移说明和风险说明。

**完成标准**

- 用户无需重启代理，即可通过不同发布模型命中不同上游目标。
- 编辑并保存运行中的“模型路由”配置后，无需重启代理线程即可对后续请求生效。
- `/models` 可列出全部启用发布模型。
- 主目标返回 `429` 或 retry 耗尽后的可重试网络运输错误时，可按配置切换到故障转移池中的下一个可用目标。
- 同一 `target` 复用于多个模型和多个池时行为一致。
- 对外发布版本不暴露半迁移状态：用户不需要在旧“代理配置组 / 全局配置”和新“模型路由”之间来回切换才能完成配置。
- `pnpm py:check` 与 `pnpm app:check` 通过。

## 跨版本依赖关系

- `v2.4.0` 提供统一的上游适配接口，为 `v2.5.0` 和 `v2.6.0` 提供稳定调用边界。
- `v2.5.0` 提供结构化 trace 和并发基础设施，为 `v2.6.0` 的动态路由调试提供可观测性。
- `v2.6.0` 才是新的稳定路由模型，不建议在 `v2.4.0` 或 `v2.5.0` 提前做部分 schema 重构。
- 通用请求体改写不作为旧 `config_group` 的长期产品语义，也不作为 MTGA 路由层的 provider 兼容能力；`target.request_body_patch` 仅作为 MLiteLLM 最终出站 JSON Patch 扩展点存在。
- MLiteLLM 的引入顺序应是先适配 provider，再补 trace，最终由 `v2.6.0` 的 MTGA 路由层统一接管动态路由与故障转移语义。

## `v2.6.0` 目标状态

### 目标对象模型

```yaml
schema_version: 2
mtga_auth_key: ""

targets:
  - id: claude-main
    display_name: Claude Main
    provider: anthropic
    api_base: https://example.com
    api_key: xxx
    middle_route: /v1
    upstream_model: claude-3-7-sonnet
    request_body_patch:
      - op: add
        path: /thinking
        value:
          type: enabled
          budget_tokens: 2048

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

### 配置 schema 约束

- 新 schema 必须有显式版本字段，例如 `schema_version: 2`，用于区分旧 `config_groups` 配置和新模型路由配置。
- `target.id`、`failover_pool.id` 和 `published_model.name` 在各自集合内必须唯一。
- `mtga_auth_key` 是全局入站鉴权 key；为空字符串或缺失时表示 MTGA 入站代理不鉴权。
- `target.api_key` 只表示上游鉴权 key，不参与 MTGA 入站鉴权。
- `target.id` 是内部稳定引用键，用于 `published_model.primary_target_id`、`failover_pool.members[*].target_id`、trace、日志和热切换生命周期；不应作为可随意修改的前端显示名称。
- `target.display_name` 是前端显示名称，可由用户修改，不作为引用键；为空时前端可按 `target.id` 或序号生成展示文案。
- `published_model.name` 是对外暴露的模型名，也是 `request.model` 的精确匹配键；匹配规则第一阶段只做大小写敏感的全量匹配，不做别名、通配符或模糊匹配。
- `target.provider` 只能使用 MTGA 支持的 provider id；provider 归一化规则继续由 MTGA 控制，不能直接透传 MLiteLLM 内部 provider 名作为前端 schema。
- `target.api_base` 只保存上游 base URL，不包含 `middle_route`；实际请求 base URL 由 `api_base + middle_route` 归一化得到。
- `target.request_body_patch` 使用 JSON Patch 操作数组，应用于 MLiteLLM provider 适配后的最终上游 JSON body；它是高级自定义出口，不参与 provider 兼容保证。
- `failover_pool.members[*].target_id` 可以引用任意已存在 `target`；同一 pool 内不允许重复 `target_id`。
- `published_model.primary_target_id` 必须引用已存在 `target`。
- `published_model.failover_pool_id` 为空时只执行主目标；非空时必须引用已存在 `failover_pool`。

### 旧配置迁移规则

- 读取旧 schema 时，迁移层必须把每个有效 `config_groups[*]` 转成一个 `target`，并生成稳定 `target.id`。
- 迁移生成的 `target.id` 应使用不含敏感信息的稳定内部值，例如 `target-1`、`target-2`；冲突时追加后缀，不从 `api_url`、`api_key` 或上游模型名派生。
- 旧 `config_groups[*].name` 迁移为 `target.display_name`；为空时只自动生成展示文案，不影响 `target.id`。
- 旧全局 `mtga_auth_key` 迁移到新 schema 顶层 `mtga_auth_key`；缺失或空字符串表示入站不鉴权。
- 旧全局 `mapped_model_id` 迁移为一个默认 `published_model.name`。
- 旧 `current_config_index` 指向的配置组迁移为默认发布模型的 `primary_target_id`。
- 旧配置组的 `provider / api_url / model_id / api_key / middle_route / prompt_cache_enabled / model_discovery_strategy` 映射到 `target` 对应字段。
- 旧配置不会自动生成 `request_body_patch`。
- 旧未选中的配置组只迁移为 `target`，默认不自动发布为额外 `published_model`。
- 旧 schema 中已经不支持的 `config_groups[*].mapped_model_id` 不再恢复；迁移层只保留当前版本仍支持的旧字段。
- 迁移应在 load 阶段返回新结构；是否立即写回磁盘由保存动作触发，避免只打开应用就改写用户配置文件。

### 路由解析规则

1. 请求进入 Chat Completions handler 后，先从当前运行时路由快照读取不可变配置视图。
2. 解析 `request.model`：
   - 缺失、空字符串或非字符串时返回 `400 model_required`。
   - 找不到同名 `published_model` 时返回 `404 model_not_found`。
   - 找到但 `enabled=false` 时返回 `404 model_not_found`，不向调用方暴露禁用模型存在。
3. 根据 `published_model.primary_target_id` 解析主目标；引用缺失视为配置错误，返回 `500 route_config_invalid` 并写入 trace。
4. 若主目标未冷却，先尝试主目标。
5. 若主目标因匹配 `trigger_statuses` 的上游状态进入冷却，记录冷却截止时间后继续尝试 failover pool。
6. 若主目标在请求开始前已经处于冷却状态，直接跳过主目标并尝试 failover pool。
7. failover pool 按 `members` 顺序尝试目标；跳过当前仍处于冷却状态的 `target_id`。
8. 所有可尝试目标都失败后，返回最后一个上游错误；如果没有任何目标可尝试，返回 `503 route_unavailable`。
9. 每次请求的 route plan 在请求开始时固定；运行中热切换只影响后续新请求。
10. 代理自身错误响应应保持 OpenAI-compatible error body，不返回 MTGA 内部专用格式给下游客户端。

### 请求编译与 adapter 边界

- MTGA 路由层的职责是把 `request.model` 解析为 `published_model`，再解析为本次请求使用的 `target`，并生成 route plan。
- route plan 应包含 provider、上游 base URL、middle route、上游模型名、API key 引用、prompt cache 开关等执行参数。
- MTGA 路由层可以把请求中的对外模型名替换为选中 `target.upstream_model`，这是路由解析结果的一部分，不是通用请求体变换 schema。
- provider 级字段兼容、字段删除/补齐、Chat Completions 到 Responses 或其他 provider API 的语义映射，继续由 MLiteLLM 或现有 upstream adapter 负责。
- `target.request_body_patch` 在 MLiteLLM 完成 provider 适配后执行，优先级最高；patch 后不再做 provider 兼容修正。
- `target.request_body_patch` 不允许修改 `stream`，因为流式策略由代理服务器运行时选项统一控制。
- 用户自定义 patch 造成非法 body 时按上游或 MLiteLLM 错误返回，不由 MTGA 自动兜底。

### 故障转移规则

- 第一阶段只对上游返回或执行层归一化后的 HTTP `429`，以及 retry 机会耗尽后的可重试网络运输错误触发 failover。
- 可重试网络运输错误包括连接超时、读取超时、连接重置、DNS 解析失败、TLS 握手失败等未收到有效上游业务响应的 transport-level 错误。
- 网络运输错误应先走现有 retry 机制；只有 retry 机会耗尽后，才进入 failover pool。
- 普通 4xx/5xx、上游鉴权失败、模型不存在、参数错误、MTGA 配置错误不触发 failover。
- `429` 会触发 target-level cooldown；网络运输错误第一阶段只触发本次请求 failover，不自动写入 cooldown，除非后续设计明确需要 network cooldown。
- cooldown 键必须是全局 `target_id`，不是 `published_model`、pool member index 或请求局部状态。
- 同一 `target_id` 被多个 `published_model` 或多个 pool 复用时，共享同一 cooldown 状态。
- cooldown 到期后不需要显式恢复动作；后续新请求会重新尝试该 target。
- 非流式请求在收到上游 `429` 或 retry 耗尽后的可重试网络运输错误，且响应尚未返回下游前，可以切换到 failover target。
- 流式请求一旦已经向下游发送首个 chunk，不再切换 target；后续错误按当前流的失败处理并结束 trace。
- failover 只在同一次请求内顺序尝试当前 published model 绑定的 pool；不跨 published model 查找其他目标。
- 每个触发 cooldown、跳过冷却目标、尝试 failover target、最终失败或成功的节点都必须写入 trace event。

### 热切换与并发边界

- 路由配置保存成功后，运行中代理应通过 `apply_runtime_config` 或等价入口热应用新 route plan。
- 热应用必须原子替换运行时 route plan，不允许请求线程看到半更新结构。
- 请求开始时必须持有 route plan 快照；请求执行期间不得再次读取可变全局配置。
- 旧 route plan 如果持有 transport/client 资源，应沿用 v2.5.0 的引用计数或等价生命周期管理，确保进行中请求结束后再释放。
- 热切换失败时必须保留旧 route plan，不能让运行中代理进入无路由状态。
- 配置保存成功但运行中热应用失败时，不回滚磁盘配置；磁盘保留用户刚保存的新配置，运行中代理继续使用旧 route plan，并返回明确 warning/log。
- 用户修正配置后可再次保存并热应用；重启代理时应尝试加载磁盘上的最新 route plan。

### 稳定约束

- 同一个 `target` 可被多个 `published_model`、多个 `failover_pool` 复用。
- “多对一”的真实需求收敛为“主目标 + 故障转移池”，不单独设计主池多成员语义。
- 不做模型能力自动识别与兼容性校验；provider 或模型能力不匹配时按上游调用失败处理，并通过 trace 暴露诊断信息。
- 第一阶段不做路由优先级、权重、健康检查后台探测或自动摘除。

### 与 MLiteLLM 的概念映射

- `target` 对应一个可复用的上游目标定义，可编译为 MLiteLLM provider 调用参数。
- `target.request_body_patch` 对应 MLiteLLM 的最终出站 body patch 参数，不改变 MTGA 路由层职责。
- `published_model` 是 MTGA 对用户暴露的稳定模型名，不要求与 MLiteLLM 请求中的 `model` 一一同名，但可在执行层映射到同一上游模型。
- `failover_pool` 是 MTGA 的产品语义对象，由 MTGA 路由层映射为 fallback、retry、cooldown 执行计划。
- `target_id` 仍是 MTGA 内部稳定标识；即使底层调用经过 MLiteLLM，也不放弃以 `target_id` 为键的产品语义与调试语义。

### trace 字段要求

- v2.6.0 复用 `v2.5.0` 已有 `ProxyTrace` 与代理日志页，不新增独立路由日志系统。
- `ProxyTrace` 应补充路由 summary 字段：`published_model`、`target_id`、`target_display_name`、`failover_pool_id`。
- 路由 attempt 明细通过 `events` 承载，不在第一阶段新增顶层 `attempts` 聚合字段；`route_attempt` event 至少记录 `attempt_index`、`source`、`target_id`、`target_display_name`、`upstream_model`。
- `target_cooldown`、`transport_failover`、`route_resolved` event 分别记录 cooldown、网络故障转移入口和最终选中目标；代理日志页可基于 summary 标记显示 `has_route_attempts`、`has_failover`、`has_cooldown`。
- trace 中不得保存明文 `api_key`、Authorization header 或 provider token。
- trace 可记录 request body patch 的 `op/path/from/value` 摘要。

### 测试矩阵

- 旧 schema 迁移：单配置组、多配置组、缺失全局 `mapped_model_id`、越界 `current_config_index`、legacy group-level `mapped_model_id`。
- 动态路由：多个 enabled `published_model` 命中不同 `target`，disabled 模型不可访问，未知模型返回 `model_not_found`。
- `/models`：按 `published_models` 配置顺序返回 enabled `published_model.name`，不返回 disabled 模型或内部 `target.upstream_model`。
- 热切换：代理运行中保存新 route plan 后，新请求命中新配置，旧请求继续使用旧快照。
- 429 failover：主目标 429 后进入 target-level cooldown，同次请求可切换到 failover target；所有候选目标冷却时返回 `route_unavailable`。
- 网络错误 failover：retry 耗尽后的可重试网络运输错误可以进入 failover，但普通 4xx/5xx、上游鉴权失败和配置错误不触发；第一阶段以连接阶段错误为可重试运输错误边界。
- target 复用：同一 target 被多个 published model 和 pool 复用时，共享 cooldown 和一致的 trace 语义。
- 流式边界：首 chunk 前 429 可 failover；首 chunk 后异常不切换目标，只结束当前 trace。
- 请求体补丁：JSON Patch 应用于 provider 适配后的最终 body；`/stream` 和根节点 patch 被拒绝。

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
