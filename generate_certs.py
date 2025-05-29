#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
证书生成工具 - 用于生成CA证书和服务器证书
替代 genca.sh 和 gencrt.sh 的功能

使用方法:
1. 运行脚本一键生成CA证书和服务器证书: python generate_certs.py
2. 所有证书信息使用默认值，无需用户输入
"""

import os
import sys
import subprocess
import tempfile
import atexit
import argparse

# 颜色输出
class Colors:
    INFO = '\033[94m'  # 蓝色
    SUCCESS = '\033[92m'  # 绿色
    WARNING = '\033[93m'  # 黄色
    ERROR = '\033[91m'  # 红色
    ENDC = '\033[0m'  # 结束颜色

def print_colored(message, color):
    """打印彩色文本"""
    print(f"{color}{message}{Colors.ENDC}")

def info(message):
    """打印信息消息"""
    print_colored(f"[INFO] {message}", Colors.INFO)

def success(message):
    """打印成功消息"""
    print_colored(f"[成功] {message}", Colors.SUCCESS)

def warning(message):
    """打印警告消息"""
    print_colored(f"[警告] {message}", Colors.WARNING)

def error(message):
    """打印错误消息并退出"""
    print_colored(f"[错误] {message}", Colors.ERROR)
    sys.exit(1)

def check_openssl():
    """检查OpenSSL是否已安装"""
    try:
        result = subprocess.run(["openssl", "version"], capture_output=True, text=True)
        if result.returncode == 0:
            info(f"检测到OpenSSL: {result.stdout.strip()}")
            return True
        else:
            error("OpenSSL命令执行失败。请确保OpenSSL已安装并添加到PATH中。")
    except FileNotFoundError:
        error("未找到OpenSSL。请安装OpenSSL并确保它在系统PATH中。")

def create_temp_file(content, suffix=".cnf"):
    """创建临时文件并写入内容"""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    temp_file.write(content.encode('utf-8'))
    temp_file.close()
    # 注册脚本退出时删除临时文件
    atexit.register(lambda: os.remove(temp_file.name) if os.path.exists(temp_file.name) else None)
    return temp_file.name

def run_command(command, error_message):
    """运行命令并检查结果"""
    info(f"执行命令: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        error(f"{error_message}\n错误输出: {result.stderr}")
    return result

def create_default_config_files():
    """创建默认配置文件（如果不存在）"""
    ca_dir = "ca"
    
    # 确保ca目录存在
    if not os.path.exists(ca_dir):
        try:
            os.makedirs(ca_dir)
            info(f"创建目录: {ca_dir}")
        except Exception as e:
            error(f"无法创建ca目录: {e}")
    
    # 创建 openssl.cnf
    openssl_cnf = """[ req ]
default_bits		= 2048
default_md		= sha256
distinguished_name	= req_distinguished_name
attributes		= req_attributes

[ req_distinguished_name ]
countryName			= Country Name (2 letter code)
countryName_min			= 2
countryName_max			= 2
stateOrProvinceName		= State or Province Name (full name)
localityName			= Locality Name (eg, city)
0.organizationName		= Organization Name (eg, company)
organizationalUnitName		= Organizational Unit Name (eg, section)
commonName			= Common Name (eg, fully qualified host name)
commonName_max			= 64
emailAddress			= Email Address
emailAddress_max		= 64

[ req_attributes ]
challengePassword		= A challenge password
challengePassword_min		= 4
challengePassword_max		= 20
"""

    # 创建 v3_ca.cnf
    v3_ca_cnf = """[ v3_ca ]
subjectKeyIdentifier=hash
authorityKeyIdentifier=keyid:always,issuer
basicConstraints = critical, CA:TRUE, pathlen:3
keyUsage = critical, cRLSign, keyCertSign
nsCertType = sslCA, emailCA
"""

    # 创建 v3_req.cnf
    v3_req_cnf = """[ v3_req ]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
subjectAltName = @alt_names
"""

    # 创建 api.deepseek.com.cnf
    api_deepseek_cnf = """
[ v3_req ]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = api.deepseek.com
"""

    # 创建 api.deepseek.com.subj
    api_deepseek_subj = "/C=CN/ST=State/L=City/O=Organization/OU=Unit/CN=api.deepseek.com"

    # 定义要创建的文件及其内容
    files_to_create = {
        os.path.join(ca_dir, "openssl.cnf"): openssl_cnf,
        os.path.join(ca_dir, "v3_ca.cnf"): v3_ca_cnf,
        os.path.join(ca_dir, "v3_req.cnf"): v3_req_cnf,
        os.path.join(ca_dir, "api.deepseek.com.cnf"): api_deepseek_cnf,
        os.path.join(ca_dir, "api.deepseek.com.subj"): api_deepseek_subj
    }

    # 创建文件（如果不存在）
    for file_path, content in files_to_create.items():
        if not os.path.exists(file_path):
            try:
                with open(file_path, 'w') as f:
                    f.write(content)
                info(f"创建配置文件: {file_path}")
            except Exception as e:
                error(f"无法创建文件 {file_path}: {e}")
        else:
            info(f"配置文件已存在: {file_path}")

def generate_ca_cert():
    """生成CA证书和私钥"""
    info("开始生成CA证书和私钥...")
    
    # 读取并合并配置文件
    openssl_cnf_path = os.path.join("ca", "openssl.cnf")
    v3_ca_cnf_path = os.path.join("ca", "v3_ca.cnf")
    
    if not os.path.exists(openssl_cnf_path):
        error(f"配置文件不存在: {openssl_cnf_path}")
    if not os.path.exists(v3_ca_cnf_path):
        error(f"配置文件不存在: {v3_ca_cnf_path}")
    
    with open(openssl_cnf_path, 'r') as f:
        openssl_cnf = f.read()
    with open(v3_ca_cnf_path, 'r') as f:
        v3_ca_cnf = f.read()
    
    # 合并配置文件
    combined_config = openssl_cnf + "\n" + v3_ca_cnf
    temp_config_file = create_temp_file(combined_config)
    info(f"临时配置文件已创建: {temp_config_file}")
    
    # 生成CA私钥
    ca_key_path = os.path.join("ca", "ca.key")
    info("正在生成CA私钥 (ca.key)...")
    run_command(
        ["openssl", "genrsa", "-out", ca_key_path, "2048"],
        "生成CA私钥失败"
    )
    success("CA私钥已生成: ca.key")
    
    # 生成CA证书
    ca_crt_path = os.path.join("ca", "ca.crt")
    info("正在生成CA证书 (ca.crt)...")
    
    # 使用默认值
    country = "CN"
    state = "X"
    locality = "X"
    organization = "X"
    org_unit = "X"
    common_name = "MyLocalCA"
    email = ""
    
    # 构建主题字符串
    subject = f"/C={country}/ST={state}/L={locality}/O={organization}/OU={org_unit}/CN={common_name}"
    if email:
        subject += f"/emailAddress={email}"
    
    info(f"使用默认证书信息: {subject}")
    
    # 生成CA证书
    run_command(
        [
            "openssl", "req", "-new", "-x509", "-extensions", "v3_ca",
            "-days", "36500", "-key", ca_key_path, "-out", ca_crt_path,
            "-config", temp_config_file, "-subj", subject
        ],
        "生成CA证书失败"
    )
    success("CA证书已生成: ca.crt")
    
    return ca_key_path, ca_crt_path

def generate_server_cert(ca_key_path, ca_crt_path, domain="api.deepseek.com"):
    """生成服务器证书"""
    info(f"开始为 {domain} 生成服务器证书...")
    
    # 检查必要文件是否存在
    required_files = [
        os.path.join("ca", "openssl.cnf"),
        os.path.join("ca", "v3_req.cnf"),
        os.path.join("ca", f"{domain}.cnf"),
        os.path.join("ca", f"{domain}.subj"),
        ca_crt_path,
        ca_key_path
    ]
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            error(f"必需文件不存在: {file_path}")
    
    # 读取配置文件
    with open(os.path.join("ca", "openssl.cnf"), 'r') as f:
        openssl_cnf = f.read()
    with open(os.path.join("ca", "v3_req.cnf"), 'r') as f:
        v3_req_cnf = f.read()
    with open(os.path.join("ca", f"{domain}.cnf"), 'r') as f:
        domain_cnf = f.read()
    
    # 合并配置文件
    combined_config = openssl_cnf + "\n" + v3_req_cnf + "\n" + domain_cnf
    temp_config_file = create_temp_file(combined_config)
    info(f"临时配置文件已创建: {temp_config_file}")
    
    # 读取主题信息
    with open(os.path.join("ca", f"{domain}.subj"), 'r') as f:
        subject_info = f.read().strip()
    
    if not subject_info:
        error(f"主题文件 {domain}.subj 为空或无法读取")
    
    info(f"从 {domain}.subj 读取的主题信息: {subject_info}")
    
    # 生成服务器私钥
    server_key_path = os.path.join("ca", f"{domain}.key")
    info(f"正在生成私钥 {domain}.key (2048位 RSA)...")
    run_command(
        ["openssl", "genrsa", "-out", server_key_path, "2048"],
        f"生成私钥 {domain}.key 失败"
    )
    
    # 将私钥转换为PKCS#8格式
    info(f"正在将私钥 {domain}.key 转换为 PKCS#8 格式...")
    server_key_pk8_path = os.path.join("ca", f"{domain}.key.pk8")
    run_command(
        [
            "openssl", "pkcs8", "-topk8", "-nocrypt",
            "-in", server_key_path, "-out", server_key_pk8_path
        ],
        f"将私钥 {domain}.key 转换为 PKCS#8 格式失败"
    )
    
    # 删除原始私钥并重命名PKCS#8格式的私钥
    os.remove(server_key_path)
    os.rename(server_key_pk8_path, server_key_path)
    info(f"私钥 {domain}.key 处理完成")
    
    # 生成CSR
    server_csr_path = os.path.join("ca", f"{domain}.csr")
    info(f"正在生成证书签名请求 (CSR) {domain}.csr...")
    run_command(
        [
            "openssl", "req", "-reqexts", "v3_req", "-sha256", "-new",
            "-key", server_key_path, "-out", server_csr_path,
            "-config", temp_config_file, "-subj", subject_info
        ],
        f"生成 CSR {domain}.csr 失败"
    )
    info(f"CSR {domain}.csr 生成成功")
    
    # 使用CA签署证书
    server_crt_path = os.path.join("ca", f"{domain}.crt")
    info(f"正在使用 CA 签署证书 {domain}.crt...")
    run_command(
        [
            "openssl", "x509", "-req", "-extensions", "v3_req",
            "-days", "365", "-sha256", "-in", server_csr_path,
            "-CA", ca_crt_path, "-CAkey", ca_key_path, "-CAcreateserial",
            "-out", server_crt_path, "-extfile", temp_config_file
        ],
        f"签署证书 {domain}.crt 失败"
    )
    
    success(f"证书 {domain}.crt 生成成功")
    # CSR文件保留，如果不需要可以取消下面一行的注释来删除它
    # os.remove(server_csr_path)
    
    return server_key_path, server_crt_path

def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='一键生成CA证书和服务器证书')
    parser.add_argument('--domain', default='api.deepseek.com', help='服务器证书的域名 (默认: api.deepseek.com)')
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("证书生成工具 - 一键生成CA证书和服务器证书")
    print("="*60 + "\n")
    
    # 检查OpenSSL
    check_openssl()
    
    # 创建默认配置文件（如果不存在）
    create_default_config_files()
    
    # 生成CA证书
    ca_key_path, ca_crt_path = generate_ca_cert()
    
    # 生成服务器证书
    domain = args.domain
    server_key_path, server_crt_path = generate_server_cert(ca_key_path, ca_crt_path, domain)
    
    # 输出结果摘要
    print("\n" + "="*60)
    print("证书生成完成！")
    print("="*60)
    print(f"CA 证书: {ca_crt_path}")
    print(f"CA 私钥: {ca_key_path} (请妥善保管，勿泄露)")
    print(f"服务器证书: {server_crt_path}")
    print(f"服务器私钥: {server_key_path} (请妥善保管，勿泄露)")
    print("\n后续步骤:")
    print("1. 将CA证书 (ca.crt) 导入到Windows的受信任的根证书颁发机构存储中")
    print("2. 修改hosts文件，将api.deepseek.com指向127.0.0.1")
    print("3. 配置并运行trae_proxy.py")
    print("="*60 + "\n")

if __name__ == "__main__":
    main() 