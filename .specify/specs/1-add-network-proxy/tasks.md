# 任务清单：添加网络代理模块

## 依赖顺序
- US1（代理配置与保存） → US2（重启回填与兼容） → US3（出站代理生效）

## 并行示例
- US1：T005 与 T006 可并行（前后端状态与 UI 分离）
- US3：T010 与 T015 可并行（代理逻辑与依赖更新）

## 实施策略
- MVP 优先完成 US1
- 每个用户故事都能独立验证
- 先保障配置读写链路，再接入出站请求

## Phase 1：Setup
- [X] T001 更新配置数据结构定义于 app/composables/mtgaTypes.ts
- [X] T002 准备前端默认值与本地状态于 app/composables/useMtgaStore.ts

## Phase 2：Foundational
- [X] T003 扩展配置读写逻辑于 python-src/modules/services/config_service.py
- [X] T004 扩展 load_config/save_config 负载于 python-src/mtga_app/__init__.py

## Phase 3：US1 代理配置与保存
- [X] T005 [P] [US1] 扩展前端状态读写代理字段于 app/composables/useMtgaStore.ts
- [X] T006 [P] [US1] 新增网络代理配置面板于 app/components/tabs/ProxyTab.vue
- [X] T007 [US1] 启用代理时校验 host/port 必填并提示于 app/components/tabs/ProxyTab.vue

## Phase 4：US2 重启回填与兼容
- [X] T008 [US2] 处理旧配置缺省值并回填于 python-src/modules/services/config_service.py
- [X] T009 [US2] 确保重启后加载与回填于 app/composables/useMtgaStore.ts

## Phase 5：US3 出站代理生效
- [X] T010 [P] [US3] 新增代理会话构造器于 python-src/modules/network/outbound_proxy.py
- [X] T011 [US3] 代理转发上游接入代理会话于 python-src/modules/proxy/proxy_transport.py
- [X] T012 [US3] 模型测活与拉模型接入代理会话于 python-src/modules/actions/model_tests.py
- [X] T013 [US3] 更新检查接入代理会话于 python-src/modules/services/update_service.py
- [X] T014 [US3] 更新渲染入口接入代理会话于 python-src/modules/update/update_checker.py
- [X] T015 [P] [US3] 增加 SOCKS 依赖于 python-src/pyproject.toml
- [X] T016 [US3] 确保代理密码不出现在日志于 python-src/modules/network/outbound_proxy.py

## Final Phase：Polish & Cross-Cutting
- [X] T017 执行前端检查命令并记录于 .specify/specs/1-add-network-proxy/quickstart.md
- [X] T018 执行 Python 检查命令并记录于 .specify/specs/1-add-network-proxy/quickstart.md
- [X] T019 补充手动验证结果于 .specify/specs/1-add-network-proxy/quickstart.md
