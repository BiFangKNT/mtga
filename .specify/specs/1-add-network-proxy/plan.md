# 实施规划：添加网络代理模块

## 技术背景
- 前端：Nuxt + Tauri 前端，现有页面与组件保持风格一致
- 后端：Python 请求使用 requests，负责网络访问与代理转发
- 配置：用户配置写入 mtga_config.yaml
- 现有链路：load_config/save_config 负责前后端配置同步

## 需求与约束检查（宪章）
- 功能不回归：新增代理配置不影响现有功能入口与行为
- 配置单源与一致性：只写入 mtga_config.yaml，重启自动读取
- 代理协议与鉴权覆盖：支持 http/https/socks4/socks5 + 可选用户名密码
- 安全与隐私：不输出代理密码到日志
- 影响范围最小化：仅影响出站请求，不改变业务语义

## 风险与闸门
- 风险：代理配置遗漏导致请求未走代理
- 风险：代理密码泄露到日志
- 闸门：配置写入读取一致性（通过）
- 闸门：代理开启/关闭不影响原有功能（通过）

## Phase 0：调研与决策
- 研究结果输出到 research.md
- 关键决策：
  - 统一由 Python requests Session 注入代理配置
  - 关闭代理时禁用环境变量代理
  - SOCKS 依赖通过 PySocks 提供

## Phase 1：设计与契约
- 数据模型输出到 data-model.md
- 接口契约输出到 contracts/
- 快速验证输出到 quickstart.md

## Phase 2：实现规划
- 前端、后端、配置文件变更清单
- 测试与验证计划
- 前端：
  - 在“网络代理”页新增配置面板与保存操作
  - load_config/save_config 读写代理字段
- 后端：
  - 扩展 ConfigStore 读写代理字段
  - requests 出站统一注入代理配置
  - 代理转发上游保持现有逻辑，仅追加代理行为
- 配置文件：
  - mtga_config.yaml 新增代理字段，默认关闭，兼容旧配置
- 验证：
  - pnpm app:check
  - pnpm py:check
  - 手动验证代理开启/关闭与重启读取
