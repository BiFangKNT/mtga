# 数据模型：网络代理配置

## 实体：ProxySettings
- enabled: boolean
- type: enum(http, https, socks4, socks5)
- host: string
- port: integer
- username: string
- password: string

## 约束与校验
- enabled 为 false 时，其余字段可为空
- enabled 为 true 时，host 与 port 必填
- port 为 1-65535 的整数
- username 与 password 可选且允许为空

## 关系
- ProxySettings 作为全局配置的一部分持久化
