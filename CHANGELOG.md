# CHANGELOG

## v2.4.0 - 2026-04-03

### :sparkles: 新功能

- 引入 LiteLLM 支持多提供商模型转发 ([8b4ee6d](https://github.com/BiFangKNT/mtga/commit/8b4ee6d8bd819b76dee153f9d57a2f6527d46120))

- 支持模型发现策略缓存与上游鉴权分离 ([996cfde](https://github.com/BiFangKNT/mtga/commit/996cfde370b0a18272d3c1fc3737166cdb82537f))

- 添加双栈 IPv4/IPv6 监听支持与优雅回退 ([6b376fd](https://github.com/BiFangKNT/mtga/commit/6b376fd07816be274e0e5f1f458caaf7fb551540))

- 为上游 API 调用增加建连阶段故障重试机制 ([33abc66](https://github.com/BiFangKNT/mtga/commit/33abc66087dd358861d4003703b219eff6f59e8e))

- 添加 pyembed 裁剪脚本以减小应用体积 ([b288a5d](https://github.com/BiFangKNT/mtga/commit/b288a5de236eda3420a247932be3971664b14404))

- 改进上游错误处理与日志格式化 ([c500c2d](https://github.com/BiFangKNT/mtga/commit/c500c2dd0f5323fc5979d10a45e2e8a792e9ac63))

- 添加前端诊断插件并改进日志目录管理 ([ca2d81d](https://github.com/BiFangKNT/mtga/commit/ca2d81d36ecc099aaff3f0cb351235a898260ceb))

- 添加上游参数自愈机制以临时处理不兼容参数 ([7ded897](https://github.com/BiFangKNT/mtga/commit/7ded8979a4294ee18b5c3ebc7bf3040e7069cf65))

- 重构参数自愈信号提取逻辑并支持litellm本地验证错误 ([2a55f87](https://github.com/BiFangKNT/mtga/commit/2a55f8715e4031c6a69b7c7070fd7bddb6a6871d))

### :bug: 修复

- 修复上游适配器中模型发现策略对路由构建的影响 ([610ddcf](https://github.com/BiFangKNT/mtga/commit/610ddcfd488739a1987092733ff06f6f38239dd3))

- 延迟应用 Gemini 兼容补丁至实际请求时 ([a96e96f](https://github.com/BiFangKNT/mtga/commit/a96e96f0313447e4be2314f2489a649784f75100))

- 移除模型测试中不必要的temperature参数 ([633f63b](https://github.com/BiFangKNT/mtga/commit/633f63b6332fa6cb82ac99d01f829b962ac5e85c))

- 修复上游适配器中不兼容参数过滤逻辑 ([e25cf1c](https://github.com/BiFangKNT/mtga/commit/e25cf1ced4beba55f2b819bb1846e3a5f4f09446))

- 修复 shell 转义问题以正确忽略标签 ([d5459e9](https://github.com/BiFangKNT/mtga/commit/d5459e907c470faaa83c87fe0938d2eaca23318a))

- 修复日志路径处理并改进错误处理 ([5b7fcd7](https://github.com/BiFangKNT/mtga/commit/5b7fcd7cd388e9f0e34f14d75c2a660cd9046850))

## v2.3.3 - 2026-03-19









### :bug: 修复

- 在Windows上移除SSLKEYLOGFILE环境变量以避免OpenSSL_Applink崩溃 ([0b64307](https://github.com/BiFangKNT/mtga/commit/0b6430720e04ddddad87eacabc483eb29284e0fe))





### :sparkles: 新功能

- 使用 cryptography 库替代 OpenSSL 进行证书解析 ([444cfc1](https://github.com/BiFangKNT/mtga/commit/444cfc1524359b932e2f9993dec35561111deabb))












## v2.3.2 - 2026-03-14





### :sparkles: 新功能

- 支持 prerelease 版本的 SemVer 比较 ([264f724](https://github.com/BiFangKNT/mtga/commit/264f724bc3dba6e50a368cd231730190c5b2c467))






### :bug: 修复

- 修复合并视图编辑器溢出和面板定位问题 ([fb973af](https://github.com/BiFangKNT/mtga/commit/fb973afdecbe6db8e68fb2b0e0e7b11881fe1db6))








## v2.3.1 - 2026-03-12


### :sparkles: 新功能

- 支持批量删除系统提示词记录 ([e6f7861](https://github.com/BiFangKNT/mtga/commit/e6f78614dcaa528015731c2a6a6b7bfc2cafeb6e))

- 使edited_text字段可选并优化编辑时间显示 ([533cc66](https://github.com/BiFangKNT/mtga/commit/533cc6653dee4fa283d97de8f75efa7e5b9927f0))



## v2.3.0 - 2026-03-10


### :art: 界面样式

- 为日志面板添加自定义滚动条样式 ([ec40204](https://github.com/BiFangKNT/mtga/commit/ec402040a94cfae63c2e5ecf3526f063c58fd1a5))



### :bug: 修复

- 修复合并视图表头宽度与编辑器不一致的问题 ([6af76e3](https://github.com/BiFangKNT/mtga/commit/6af76e34fd1c4d6cdf2ba701421caeef075ca2ac))



### :sparkles: 新功能

- 为按钮操作添加防重复点击和加载状态 ([a6de4b8](https://github.com/BiFangKNT/mtga/commit/a6de4b8b3b4e7427f99cce3dd86d056e55942a62))

- 允许在无法获取系统字体时手动输入字体 ([922568e](https://github.com/BiFangKNT/mtga/commit/922568ed5f9ab3e2f89ed2e8e8fdfa107c4548d5))

- 改进 MtgaSelect 下拉面板的定位和滚动行为 ([0a0c317](https://github.com/BiFangKNT/mtga/commit/0a0c3177b9a15a20586e078edc9e944cf7aba778))

- 新增系统提示词管理功能 ([2d726b8](https://github.com/BiFangKNT/mtga/commit/2d726b84b47433cdf6e9c4cd5c68ff934520ee73))

- 升级编辑器并支持差异对比模式 ([fb43f1b](https://github.com/BiFangKNT/mtga/commit/fb43f1b84a3d3a95b9ee84aa97448a1895bfb9af))

- 添加清空日志功能 ([3038202](https://github.com/BiFangKNT/mtga/commit/30382024a663509976696f994865b2687a3f300f))



## v2.2.0
### :sparkles: 新功能
- feat(proxy): 支持运行时热更新代理配置 (3587ada37488acdabc0f56393069b82377fdf5e1)
### :bug: 修复
- 暂无修复
### :art: 界面样式
- 暂无界面样式

## v2.1.0
### :sparkles: 新功能
- feat(proxy): 添加配置缺失时的自动面板导航 (cf6d81dfafba699e4344b7a09f79db10d9b01c7a)
### :bug: 修复
- fix(gitflow): 执行 release finish 后自动签回开发分支 (b8ed6e5d05cd474926903afa80ddad8302d88681)
### :art: 界面样式
- 暂无界面样式

## v2.0.1
### :sparkles: 新功能
- 暂无新功能
### :bug: 修复
- fix: 仅在未指定stdin和input时设置stdin为DEVNULL (0662356818131976af11100fe0300c9c5c12429a)
- fix: 修复非 Windows 平台加载 WinDLL 时的类型检查错误 (7a7604ee5d57fe1e700946f65c0220460d6741e9)
### :art: 界面样式
- 暂无界面样式

## v2.0.0
### :sparkles: 新功能
- feat: 初始化Tauri项目基础配置和文件结构 (1edafe6bb8ed012a3176171899affaf4bf79e78b)
- feat(tauri): 更新应用配置和权限设置 (c78eb8eb0827b9b873721839d6be8ebde598c327)
- feat: 添加Tauri Python后端基础结构 (40a9ae0530450cba63b351da735cc6659e360870)
- feat: 添加mtga-app模块的初始实现 (2025cac672669254ebd10453d95d297497a8896c)
- feat: 实现基础UI框架并添加组件库 (01025bd83f264dd69a740fbc31645251c18bf49f)
- feat(ui): 初始化主标签页组件并优化nuxt配置 (660f5c8ad3c8efb27098bc77ad4e2fb79ea28412)
- feat: 实现MTGA前端核心功能与状态管理 (cbf6b8434ddffdd5efbd5f8398c79ef362c2436b)
- feat(commands): 添加配置管理和应用信息命令 (29d8c1af5edf295382c4d0ca171fd36c7af7092a)
- feat(hosts): 实现hosts文件操作功能 (5c2387d8c287d4dfe514b2983a4d83cbb7c2e467)
- feat: 实现后端功能并替换前端占位逻辑 (232dafcebfe57aa325edf989772e7b49c04c03f3)
- feat(icons): 添加多平台应用图标资源 (db74547c69104d4ecbe59a2acae80669671b670e)
- feat(模块加载): 实现模块来源控制功能 (008c71be4a7592c92e0023e3e7fdbd5e3e00b404)
- feat(tauri): 实现模块和资源路径的统一配置管理 (4b1db38c08f746ca922103661226ce8d611b8c4f)
- feat: 在非调试模式下设置默认MTGA_RUNTIME环境变量 (fe3fa197357f7908dd1eff53aa7fd0830e6dc78b)
- feat(启动): 添加启动状态检查和日志系统 (dbe121c3b5d4ee920086dca80818b44690ea4c84)
- feat: 添加shell插件支持并优化UI界面 (5546996c31b0220092ebf48d1721aefe7a8b4eba)
- feat(logs): 实现日志总线功能及前端日志流式拉取 (cc643367c7facfe115d76a9f2042ca0006df8eb9)
- feat(runtime): 实现平台感知的日志总线模块 (706d3593bd9ffa033e3202a4ee6e9e54f278cfaa)
- feat(proxy): 添加应用关闭时的代理清理功能 (b80d3e8566ec66a135793706355c4a3616d1b875)
- feat: 添加工具提示功能并优化UI交互 (7bd33eebb70f460f66c142a87cf1fc88f94df63a)
- feat(更新): 添加应用启动时自动检查更新功能 (83e00b40a02fdf482be14035e1ddefa54f1a0473)
- feat(tooltip): 实现全局悬浮提示代理以逃逸容器剪裁 (8de7201c194275f6f849b85a88218b066b621fac)
- feat(build): 添加Windows应用清单并更新构建配置 (9bbed4688d86f1b08accbb9621fa6532234bd83b)
- feat(运行时): 添加运行时环境检测功能 (83ae2ba09f259dcc03b4b6b2f4bd8baffdb1be9a)
- feat: 添加原生启动页并修复后端并发初始化问题 (5d88b2e1ad51b3a2364619733be85c8b93ff2478)
- feat(logs): 添加日志事件流支持以替代轮询机制 (04b54fb20b0e398106296169f6b58c464dc7fcb4)
- feat(标签页): 为标签页切换添加过渡动画效果 (e481a24f5fbcb74294de19c6e79bd6ae0237a013)
- feat(version): 重构应用版本号注入机制 (a6b1168e90042adb259ed5c1b837b41d7199a0a0)
- feat(proxy): 实现代理启动步骤事件流与自动导航 (e9cb13681791fc0ed135ed21865eb376368c46e0)
- feat(ui): 为输入框添加带清空按钮的标准样式组件 (f5783bfabc0ba41d395ea798ec6b487d91b21632)
- feat(ui): 新增可复用输入框组件并重构配置面板 (42cb421b5cbf5590677a1eb0e2a937c33cde1192)
- feat(ui): 引入 MtgaSelect 组件并替换 ProxyTab 中的原生 select (647ae84a6511cb67507e2218937c7cb6fb30da48)
- feat(配置组): 添加获取模型列表功能并优化下拉组件 (ad8ade74eae42a775a6e631915788edff8413388)
- feat(ui): 添加新版本更新提醒徽章 (bc30f5070d344489486a122f5524231eb94a004c)
- feat(cert): 增强CA证书检查逻辑并记录元数据 (b8f5299c3c4a83b0da6510f32defd46af81ff701)
- feat(cert): 为清除 CA 证书添加二次确认弹窗 (193fb828e34c6986f6aa803d001141bbd2ee44c1)
- feat(ui): 重构对话框组件并新增通用弹窗基础组件 (bb0f1107e1fca78c35d772cfd3a34dd1251032dd)
- feat(theme): 添加主题自定义功能 (e840e3f4cad0891bbd6575f914d13061f522ccf7)
### :bug: 修复
- fix(security): 添加 DOMPurify 以净化更新对话框中的 HTML 内容 (3e78b366aaa2d7a570dd3672806dabf252650cfa)
- fix: 修复Python后端核心功能及依赖配置 (4f69d6339362f92387d24e973397572b75ea8e0c)
- fix(python集成): 添加Python环境配置及调用处理功能 (6fe07bcc448d28940e9797aefabf1418d972ec85)
- fix(proxy): 补上停止代理时添加hosts文件清理失败日志的功能 (71141b02efead607ef6d0b7a60b261c994a47c0e)
- fix(macos_privileged_helper): 改进Python可执行文件路径检测逻辑 (ff0cbcdaa8d5adcf5391a2439b67bfe8fbbe5df7)
- fix(tooltip): 修复不支持CSS锚点定位时的工具提示位置问题 (c9ae9ec8f3d70e759cd440937a6186bbbc5e87e7)
- fix(app): 修复类型断言和事件目标检查问题 (a33572944e2c80d567db52b52c931e76225b430a)
- fix(hosts): 在非Windows系统跳过hosts预检 (6284ce7c6118a20df3cd4237be6c3cb0e3a786a1)
- fix(tauri配置): 后端改进开发服务器配置以确保主窗口在开发模式下可见 (9cce6c1e1034328cc9f62d3da2869bf9028ba5b1)
- fix(nuxt.config): 开发期禁用缓存避免 Tauri WebView 读取损坏缓存 (aeb2081f5d2fbc1dbdcd6f457be8a98c5738ed1e)
- fix: 添加日志流和代理步骤监听器的清理逻辑 (a65a6f8fd20cbfcf740f0048818a261e7b33666e)
- fix(proxy): 改进代理服务器停止逻辑，修复重启时残留实例问题 (df19b0ba44e631fa9bcb4dcdbc68fb03dfddad93)
### :art: 界面样式
- style(MainTabs): 为标签页添加悬停效果和过渡动画 (f24020680e8525c9b129b2a7d86418414384c54a)
- style(AboutTab): 居中显示页脚文本 (a5565118c45115316441eedc46a8805b968f4895)
- style: 优化配置编辑面板布局与中间路由样式 (f50d24f2a4dcae613652c2a7dd8637cfc95b2569)
- style(ui): 更新主题颜色为琥珀色并统一按钮样式 (fa51e815e7dcb37ab4d66f0831ceebd745efc686)
- style(RuntimeOptionsPanel): 为选项标签添加悬停效果和交互样式 (9addcdf54076b4ff8fc9d99b0a22cf52eaa0ce08)
- style(AppShell): 调整页面布局和底部导航样式 (54fb08a25587e2186959deeb0dba382e0723aeb3)
- style(ui): 优化应用布局和导航菜单样式 (49146f1423480488d71f9ebb1f1538c2ff4c51bc)
- style(ui): 移除冗余卡片容器并优化布局结构 (c2203a9381b5771a19b18d54cc986d84bc9c0de4)
- style(components): 移除AppShell.vue中多余的背景色类 (6598a6e8a2535435697fe37070f9e6c48be58131)
- style(ui): 重构应用布局和样式以简化结构 (4e72819ad2d3a2610adb0840721de5b0258ff1be)
- style(ConfigGroupPanel): 调整表格最大高度以显示更多内容 (2ee381f02133b513ddfc78b0e1c127ece842f14a)
- style(css): 添加自定义滚动条样式以提升用户体验 (2be8a427272bb5a6524132b7e7d3e554f57c5744)
- style(ui): 调整多个组件的透明度和背景模糊效果 (c2a1dc6b1b379cf6b9ee074ef142aa3485cd1af5)
- style(ConfigGroupPanel): 优化配置组面板的视觉反馈和过渡效果 (6a957b5e06909c0c7e3734aa118786f6d9a83769)
- style(UpdateDialog): 优化更新对话框的UI和交互逻辑 (4c0a401514baa02434f4c3b2da5b7cb5fb6db499)
- style(ui): 移除独立的关于页并将功能移至主界面 (825754ed67e1dadae24a617cc4db0ca4e1fc4776)
- style(LogPanel): 调整日志面板的边框和背景样式以提升视觉效果 (cc69346a5cbd0942c655853fe91733ae331f5031)
- style(UI): 调整界面背景和组件透明度以增强视觉效果 (b1bcee912d650d13d180713cf23c318fe414b16e)
- style(ui): 重构导航面板和设置功能 (c110edc14ff50f0041a0d1e9a70c78ec116efaee)
- style(tailwind): 重构样式配置以适配 Tailwind CSS 4 并添加工具类 (3f64e38d734169b7721460fa9a5fb460d59a99f0)
- style: 更新应用标题与副标题文本 (d7c31503c2eee7964bc70b309850207fa0ee03e0)

## v1.7.1
### :sparkles: 新功能
- 暂无新功能
### :bug: 修复
- fix(macos_privileged_helper): 修正模块搜索路径的父级目录层级 (b7737e9c918bd68260fbaa55bdd13e20b36990b4)
- fix(proxy_orchestration): 修改hosts文件失败时继续启动代理服务器 (72a115d0d020a51abdf2ab512b3c487e885d8cdf)

## v1.7.0
### :sparkles: 新功能
- feat(gui): 启动后自动检查更新 (2c9b233ee6636b7fc35b30714943cd1e1066924d)
- feat(update_checker): 添加对GitHub表情符号的渲染支持 (3e5e3b1acd612181bf70ae10acd108706131b8fd)
- feat(runtime): 引入错误码枚举并重构错误处理逻辑 (953fbb69fe8328ae76b4f967a3e0106993ffe6e6)
- feat: 统一使用describe_result处理操作结果消息 (65b5a889d48fa65afa348b7d147a57b30965bbae)
- feat(proxy): 添加中间路由支持并更新相关测试和UI (37db2643f22117ae29109a60f120844bed7f6b6b)
### :bug: 修复
- fix(actions): 用 /v1/models 列表校验模型并修正文案 (2e34fae2a4b9b8b582b4224b8c35f11bc91a6dde)
- fix(ui): 修复macOS下Notebook标签切换时的焦点问题 (eaf8d2d8b6cc1f0ed269750b6bb8ea4d10ae7f0d)

## v1.6.0
### :sparkles: 新功能
- feat(hosts_manager): 添加 hosts 文件写入预检和受限模式支持 (47c2b8f14d3e9e7126b08c45df153e7435f24983)
- feat(网络检查): 添加网络环境检测功能以识别显式代理配置 (ae3e5042d1b700105bbce7f093c533f75b42fbc8)
- feat(界面): 为映射模型和MTGA鉴权字段添加工具提示 (9081116e0703be23e6e243f78a9fdcbc4921cd7d)
- feat(资源管理): 使用platformdirs库改进跨平台用户数据目录处理 (3a280966edbfb1cd2696db65c9e5c14c1bba3c56)
- feat(update_checker): 使用 GitHub API 渲染 Markdown 并移除本地渲染模块 (97765d2efcc2fbc9054a9cbcc7b9cfb7eae3dc5c)
- feat(tk字体管理): 提取字体管理逻辑到独立模块并支持更新检查器字体配置 (fb2b1ace1405c1838fab51fca71665e88c7ee998)
### :bug: 修复
- fix(hosts_manager): 改进 Windows 系统下 hosts 文件路径获取逻辑 (7794f157861691e17b2870274970786d95d20a51)
- fix(hosts): 原子写入失败时回退为追加写入 (71016307e726accbf6155e185021fb03705f4688)

## v1.5.0
### :sparkles: 新功能
- feat(proxy): 添加关闭SSL严格模式的选项 (8bf706b75f2b3909003d3d18b6b58a717e4a4536)
- feat(proxy_server): 添加SSE流式响应日志记录功能 (154a694f0e06fd3ca866ae878f688e981e90b10c)
- feat(proxy_server): 添加请求ID和详细日志记录功能 (286fee26e675c2eb56c4a0be7026b11bef8f53cb)
- feat(proxy_server): 实现 SSE 事件流处理与 OpenAI 格式规范化 (78d44e0569f563dd46ceb74d8a9316c1eb3054d8)
### :bug: 修复
- fix(proxy_server): 修复服务器关闭时可能的属性错误并添加端口占用检查 (cc3c116dd11c73e1bc82ce1261361f9dbbac9466)

## v1.4.0
### :sparkles: 新功能
- feat(proxy): 启动代理时自动修改hosts (187ddfc513f9666a646620dde666203b833314f7)
- feat(macos): 简化macOS证书安装流程并自动设置信任 (b5cf97e0e81685dfbfbcdfc222f9cf5920660c4e)
- feat(证书管理): 添加清除系统CA证书功能 (05994def0e0daa8b7a7c57f78e690b3d82dd1385)
- feat(cert): 添加证书存在性检查功能避免重复生成 (ccbfbee547629a1636b56db7adb249910fe16896)
- feat(更新检查): 优化更新对话框布局并添加前往发布页按钮 (11c812337bdd44cfdcd1a945b0b9fc5cf5abda33)
- feat(gui): 清除CA证书添加确认对话框以可修改变量及避免误操作风险 (3b98f1ecb4527067b70119e2155fdd7bed8fbed8)
- feat(gui): 居中显示对话框以提升用户体验 (170f73c0b30f99116566a54a5033ed971fd88f50)
- feat(gui): 添加全局配置必填项检查功能 (0e35fd3732f1c7e0eb213db9c4b32735646e2a06)
### :bug: 修复
- fix(process): 创建子进程工具模块以避免win端继承无效的stdin句柄 (4fcc18507f90e647fc39f08c8a379f6f656c31d2)
- fix(build): macOS端修复tkhtml库导入失败问题并添加动态库到构建脚本 (6e5fbc5b48ae83a2ee1eef32b35019b651e7a616)
- fix(gui): 提取窗口居中逻辑到独立函数避免macOS闪屏问题 (16d15a2e1ab98353f8dbe43fe0f103959e973704)

## v1.3.1
### :sparkles: 新功能
- 暂无新功能
### :bug: 修复
- fix(process): 创建子进程工具模块以避免win端继承无效的stdin句柄 (4fcc18507f90e647fc39f08c8a379f6f656c31d2)

## v1.3.0
### :sparkles: 新功能
- feat(hosts): hosts 文件支持同时写入 IPv4 与 IPv6 映射 (c62d87cfd1c1057266e688c572c443a4d6f89aa2)
- feat(gui): 引入统一线程管理并强化代码规范 (37cec8d1c38d5daf93fb341ba222e4263c59ad98)
- feat(gui): 停止代理时同步还原 hosts (cf23d939ec03f83380596ab554395541c0b95013)
- feat(gui): 适配 macOS 深色模式悬浮提示 (b7f93d8cd760185ebab6f730874a3144ce28e7b0)
- feat(hosts管理): 修复程序退出时hosts记录未清理的问题 (7249afb730b3b3aa7a634db0577a0b63d283b16a)
- feat(macos): 添加持久化提权模块用于 macOS 管理员权限操作 (d935b8b757abc2751684d1eedc4dc896f2c2a5af)
- feat(gui): 添加版本更新检查功能和Markdown渲染器 (15aec5a8fb5e9c16fdd0f62827129a6e17081f61)
- feat(version): 添加构建时版本注入和错误日志记录 (0c0c4fb44b46a84e19853f0353ca9f5e91fc6015)
- feat(字体): 统一应用字体设置并支持自定义渲染字体 (2546b8e2abd87951ddec81fd68d3feab712a293c)
- feat(界面): 调整主窗口布局并添加关于页脚 (c55c30376084052b9e3e1a2c3d73beaa783300db)
### :bug: 修复
- fix(界面): 调整窗口高度并优化关于标签页样式 (99ae59c1530fdcc52c6522c1bb8578c42e120e28)
- fix(resources): 恢复 Windows 打包后的资源路径回退逻辑 (b087d5c50834fe3e633bb83e838b15ac596d069e)
- fix(proxy): 改进代理服务器的启动和关闭逻辑 (5fc9f935e8a346d508babd2721a41bc4a1235051)
- fix(gui): 增强字体选择避免打包后崩溃 (8f3cdb0b8d38d53564a4c8451388c005c64a7c27)
- fix(tkhtml): 修复tkinterweb资源打包和运行时加载问题 (c071f3bc753bb1598a87ccbc79ef0b9062b6efc8)
- fix(ui): 修复macOS上字体显示过小和DPI缩放问题 (9bac52baec9aa597d7aab99e5d880f02bb5b538d)
- fix(mtga_gui): 重构左侧面板布局以使用网格管理 (0e16c93f756dea8a1069bb817a152751a2af2e1b)

## v1.2.1
此版本主要是合并双端，并跑通自动化发版流程

- feat(mac): 添加macOS应用沙箱权限配置和启动优化 (008c04fb55e3e79b5a362c6573063471d3cbd1a6)
- feat(ci): 添加预发布版本的构建工作流 (7e68b706bec0aea0f272cbc2c6d3739b86736a40)
- fix(macos): 修复打包应用的中文编码和启动问题 (47dbeb68cc6a4aad8bdfc05dfca2327b4e7c556f)

## v1.2.0
- 🔄 **重构模型映射架构** - 从"一对一映射"改为"统一映射模型"架构
  - trae端使用统一的映射模型ID，MTGA通过配置组切换实际后端模型
  - 代理服务器支持模型ID映射和MTGA鉴权验证
  - 全局配置支持映射模型ID和MTGA鉴权Key设置
- ⚡ **配置组管理优化** - 重构配置组字段和验证逻辑
  - 配置组名称改为可选，API URL、实际模型ID、API Key改为必填
  - 移除目标模型ID字段，改为全局映射配置
  - 配置组表头重命名，向下兼容旧配置文件
- 🧪 **新增自动化测试功能** - 完整的模型连接测试体系
  - 保存配置后自动测试模型连接 (GET `/v1/models/{模型id}`)
  - 手动测活功能，支持聊天补全测试 (POST `/v1/chat/completions`)
  - 详细测试日志输出，包括响应内容和token消耗统计
- 🎯 **增强用户体验** - 新增测活按钮和详细提示
  - 测活按钮支持tooltip提示，说明token消耗风险
  - 异步测试避免UI阻塞，完善的错误处理机制
  - API Key安全显示（掩码处理）

## v1.1.1
- 🐛 **修复 hosts 修改功能的问题** - 解决 hosts 文件修改时换行符异常的问题

## v1.1.0
- ✨ **新增用户数据管理功能** - 单文件版本支持用户数据持久化存储
  - 数据存储位置：Windows `%APPDATA%\MTGA\`，macOS/Linux `~/.mtga/`
  - 支持备份、还原、清除用户数据
  - 配置文件、SSL证书、hosts备份自动持久化
- 🔧 **优化单文件构建** - 改进 `build_onefile.bat`，支持版本号变量化
- 🎯 **改进用户界面** - 添加配置组列表刷新按钮，优化界面布局
- 📖 **完善文档** - 新增单文件构建指南，更新项目文档

## v1.0.0
- ✅ **适配 Mac OS 端** - 支持 macOS 应用程序安装方式
- 🔄 **默认服务商变更** - 从 DeepSeek 变更为 OpenAI
- 📦 **文件重构** - ds 相关文件重命名为 `*_ds.*` 格式存档
- 🌐 **API URL 格式变更** - 从 `https://your-api.example.com/v1` 变更为 `https://your-api.example.com`
