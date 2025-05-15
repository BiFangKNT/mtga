#!/bin/bash

# 循环提示用户确认是否生成 CA 证书和密钥
while true; do
    read -p "Do you want to generate ca cert and key? [yes/no] " yn
    case $yn in
        [Yy]* ) break;; # 如果用户输入 Y 或 y，则跳出循环继续执行
        [Nn]* ) exit 1;; # 如果用户输入 N 或 n，则退出脚本
        * ) echo "Please answer yes or no.";; # 其他输入则提示用户重新输入
    esac
done

# 定义临时配置文件名
TEMP_CONF_FILE="_genca_temp_config.cnf"
# 设置 trap，确保脚本退出时（无论是正常结束还是出错）都尝试删除临时文件
trap 'rm -f "$TEMP_CONF_FILE"' EXIT

echo "Combining openssl.cnf and v3_ca.cnf into $TEMP_CONF_FILE..."
# 将 openssl.cnf 和 v3_ca.cnf 的内容合并到临时配置文件中
cat openssl.cnf v3_ca.cnf > "$TEMP_CONF_FILE"
# 检查上一个命令是否成功执行
if [ $? -ne 0 ]; then
    echo "Error: Failed to create temporary config file '$TEMP_CONF_FILE'."
    exit 1 # 如果创建失败，则输出错误信息并退出
fi
echo "Temporary config file created successfully."

echo "Generating CA private key (ca.key)..."
# 生成 2048 位的 RSA CA 私钥
openssl genrsa -out ca.key 2048
if [ $? -ne 0 ]; then
    echo "Error: Failed to generate CA key."
    exit 1
fi
echo "CA key generated."

echo "Generating CA certificate (ca.crt) using $TEMP_CONF_FILE..."
# 使用生成的 CA 私钥和临时配置文件创建自签名的 CA 证书
# -new: 创建新的证书请求（虽然这里直接生成证书）
# -x509: 输出自签名证书而不是证书请求
# -extensions v3_ca: 使用 v3_ca 段中定义的扩展
# -days 36500: 证书有效期（约100年）
# -key ca.key: 指定私钥文件
# -out ca.crt: 指定输出的证书文件
# -config "$TEMP_CONF_FILE": 指定 OpenSSL 配置文件
openssl req -new -x509 -extensions v3_ca -days 36500 -key ca.key -out ca.crt -config "$TEMP_CONF_FILE"
if [ $? -ne 0 ]; then
    echo "Error: Failed to generate CA certificate."
    exit 1
fi
echo "CA certificate generated successfully: ca.crt"
echo "Script finished."
# trap 会在脚本结束时自动清理 $TEMP_CONF_FILE
