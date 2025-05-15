#!/bin/bash

# 函数：记录错误信息并退出脚本
# 参数 $1: 错误信息字符串
error_exit() {
    echo "错误: $1" >&2 # 将错误信息输出到标准错误
    # 如果临时配置文件变量已设置且文件存在，则尝试删除
    if [ ! -z "$TEMP_CONF_FILE" ] && [ -f "$TEMP_CONF_FILE" ]; then
        rm -f "$TEMP_CONF_FILE"
    fi
    exit 1 # 以状态码 1 退出，表示错误
}

# --- 脚本主要逻辑开始 ---

# 从命令行第一个参数获取证书名称前缀 (例如 api.deepseek.com)
NAME="$1"
TEMP_CONF_FILE="" # 初始化临时配置文件变量，以防trap在未设置时出错

# 检查 NAME 参数是否已提供
if [ -z "$NAME" ]; then
    error_exit "必须提供 NAME 参数 (例如 api.deepseek.com)。用法: $0 <domain_name_prefix>"
fi

# 定义所需配置文件的名称
OPENSSL_CNF="openssl.cnf"
V3_REQ_CNF="v3_req.cnf"
NAME_CNF="$NAME.cnf"
NAME_SUBJ="$NAME.subj"
CA_CERT="ca.crt"
CA_KEY="ca.key"

# 检查所有必需的输入文件是否存在于当前目录
echo "INFO: 正在检查所需文件..."
for f in "$OPENSSL_CNF" "$V3_REQ_CNF" "$NAME_CNF" "$NAME_SUBJ" "$CA_CERT" "$CA_KEY"; do
    if [ ! -f "$f" ]; then
        error_exit "必需文件 '$f' 在当前目录 ($(pwd)) 未找到。"
    fi
done
echo "INFO: 所有必需文件均存在。"

# 创建一个唯一的临时配置文件名 (使用进程ID $$ 保证唯一性)
TEMP_CONF_FILE="_temp_openssl_config_$$.cnf"
# 设置 trap: 无论脚本如何退出 (正常结束、错误、中断)，都尝试删除临时文件
trap 'echo "INFO: 清理临时文件 $TEMP_CONF_FILE..."; rm -f "$TEMP_CONF_FILE"' EXIT

echo "INFO: 正在合并 '$OPENSSL_CNF', '$V3_REQ_CNF', 和 '$NAME_CNF' 到临时文件 '$TEMP_CONF_FILE'..."
# 将多个 OpenSSL 配置文件内容合并到一个临时文件中
cat "$OPENSSL_CNF" "$V3_REQ_CNF" "$NAME_CNF" > "$TEMP_CONF_FILE"
if [ $? -ne 0 ]; then # 检查上一个命令 (cat) 是否成功执行
    error_exit "创建临时配置文件 '$TEMP_CONF_FILE' 失败。"
fi
echo "INFO: 临时配置文件创建成功。"

# 从 $NAME.subj 文件读取证书主题信息
SUBJECT_INFO=$(cat "$NAME.subj")
if [ -z "$SUBJECT_INFO" ]; then # 检查是否成功读取到内容
    error_exit "主题文件 '$NAME.subj' 为空或无法读取。"
fi
echo "INFO: 从 '$NAME.subj' 读取的主题信息: $SUBJECT_INFO"

echo "INFO: 正在生成私钥 '$NAME.key' (2048位 RSA)..."
# 生成服务器私钥
openssl genrsa -out "$NAME.key" 2048
if [ $? -ne 0 ]; then error_exit "生成私钥 '$NAME.key' 失败。"; fi

echo "INFO: 正在将私钥 '$NAME.key' 转换为 PKCS#8 格式..."
# 将私钥转换为 PKCS#8 格式 (通常为了更好的兼容性)
openssl pkcs8 -topk8 -nocrypt -in "$NAME.key" -out "$NAME.key.pk8"
if [ $? -ne 0 ]; then error_exit "将私钥 '$NAME.key' 转换为 PKCS#8 格式失败。"; fi
rm "$NAME.key" # 删除原始格式的私钥
mv "$NAME.key.pk8" "$NAME.key" # 将 PKCS#8 格式的私钥重命名回原名
echo "INFO: 私钥 '$NAME.key' 处理完成。"

echo "INFO: 正在生成证书签名请求 (CSR) '$NAME.csr'..."
# 使用临时配置文件和读取的主题信息生成 CSR
# 添加 MSYS_NO_PATHCONV=1 来阻止 MinGW/MSYS 对 -subj 参数值进行不必要的路径转换
MSYS_NO_PATHCONV=1 openssl req -reqexts v3_req -sha256 -new -key "$NAME.key" -out "$NAME.csr" \
    -config "$TEMP_CONF_FILE" \
    -subj "$SUBJECT_INFO"
if [ $? -ne 0 ]; then error_exit "生成 CSR '$NAME.csr' 失败。"; fi
echo "INFO: CSR '$NAME.csr' 生成成功。"

echo "INFO: 正在使用 CA 签署证书 '$NAME.crt'..."
# 使用 CA 证书和 CA 私钥来签署 CSR，生成最终的服务器证书
# -extfile 参数也使用我们合并的临时配置文件
openssl x509 -req -extensions v3_req -days 365 -sha256 \
    -in "$NAME.csr" \
    -CA "$CA_CERT" \
    -CAkey "$CA_KEY" \
    -CAcreateserial \
    -out "$NAME.crt" \
    -extfile "$TEMP_CONF_FILE"
if [ $? -ne 0 ]; then error_exit "签署证书 '$NAME.crt' 失败。"; fi

echo "INFO: 证书 '$NAME.crt' 生成成功。"
# CSR 文件 ($NAME.csr) 默认会保留，如果不需要可以取消下面一行的注释来删除它
# echo "INFO: (可选) 清理 '$NAME.csr'..."
# rm -f "$NAME.csr"

# 临时配置文件 $TEMP_CONF_FILE 会由 trap 命令在脚本退出时自动清理
echo "INFO: 脚本为 '$NAME' 执行完毕。"
exit 0 # 以状态码 0 退出，表示成功
