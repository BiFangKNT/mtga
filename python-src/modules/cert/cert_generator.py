"""
证书生成模块
使用 Python cryptography 直接生成 CA 与服务器证书。
"""

from __future__ import annotations

import configparser
import ipaddress
import os
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any, cast

from cryptography import __version__ as cryptography_version
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID, ObjectIdentifier

from modules.cert.ca_metadata import save_ca_info
from modules.cert.cert_utils import (
    certificate_fingerprint_sha1,
    certificate_not_after_unix,
)
from modules.runtime.resource_manager import ResourceManager

type LogFunc = Callable[[str], None]
type SubjectName = x509.Name
type SubjectAttribute = x509.NameAttribute[Any]


@dataclass(frozen=True)
class ServerCertificateExtensions:
    subject_alt_names: list[x509.GeneralName]
    subject_alt_name_critical: bool
    basic_constraints: x509.BasicConstraints
    basic_constraints_critical: bool
    key_usage: x509.KeyUsage
    key_usage_critical: bool
    extended_key_usage: x509.ExtendedKeyUsage | None
    extended_key_usage_critical: bool


@dataclass(frozen=True)
class ServerCertContext:
    subject: SubjectName
    extensions: ServerCertificateExtensions
    ca_certificate: x509.Certificate
    ca_private_key: rsa.RSAPrivateKey

_SUBJECT_OIDS: dict[str, ObjectIdentifier] = {
    "C": NameOID.COUNTRY_NAME,
    "ST": NameOID.STATE_OR_PROVINCE_NAME,
    "L": NameOID.LOCALITY_NAME,
    "O": NameOID.ORGANIZATION_NAME,
    "OU": NameOID.ORGANIZATIONAL_UNIT_NAME,
    "CN": NameOID.COMMON_NAME,
    "E": NameOID.EMAIL_ADDRESS,
    "EMAILADDRESS": NameOID.EMAIL_ADDRESS,
}

_V3_REQ_SUPPORTED_KEYS = {
    "basicconstraints",
    "extendedkeyusage",
    "keyusage",
    "subjectaltname",
}
_KEY_USAGE_FLAGS = {
    "contentcommitment": "content_commitment",
    "crlsign": "crl_sign",
    "dataencipherment": "data_encipherment",
    "decipheronly": "decipher_only",
    "digitalsignature": "digital_signature",
    "encipheronly": "encipher_only",
    "keyagreement": "key_agreement",
    "keycertsign": "key_cert_sign",
    "keyencipherment": "key_encipherment",
    "nonrepudiation": "content_commitment",
}
_EXTENDED_KEY_USAGE_OIDS: dict[str, ObjectIdentifier] = {
    "anyextendedkeyusage": ObjectIdentifier("2.5.29.37.0"),
    "clientauth": ExtendedKeyUsageOID.CLIENT_AUTH,
    "codesigning": ExtendedKeyUsageOID.CODE_SIGNING,
    "emailprotection": ExtendedKeyUsageOID.EMAIL_PROTECTION,
    "ocspsigning": ExtendedKeyUsageOID.OCSP_SIGNING,
    "serverauth": ExtendedKeyUsageOID.SERVER_AUTH,
    "timestamping": ExtendedKeyUsageOID.TIME_STAMPING,
}


def _utc_now() -> datetime:
    return datetime.now(UTC)


def _write_bytes(path: str, payload: bytes, description: str, log_func: LogFunc = print) -> bool:
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as handle:
            handle.write(payload)
        log_func(f"{description}: {path}")
        return True
    except Exception as exc:  # noqa: BLE001
        log_func(f"写入 {description} 失败: {exc}")
        return False


def _read_text_file(path: str, description: str, log_func: LogFunc = print) -> str | None:
    try:
        with open(path, encoding="utf-8") as handle:
            return handle.read()
    except Exception as exc:  # noqa: BLE001
        log_func(f"读取{description}失败: {exc}")
        return None


def _split_subject_components(subject_info: str) -> list[str]:
    stripped = subject_info.strip()
    if stripped.startswith("/"):
        stripped = stripped[1:]

    components: list[str] = []
    current: list[str] = []
    escaped = False
    for char in stripped:
        if escaped:
            current.append(char)
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == "/":
            segment = "".join(current).strip()
            if segment:
                components.append(segment)
            current = []
            continue
        current.append(char)

    tail = "".join(current).strip()
    if tail:
        components.append(tail)
    return components


def _build_name_attribute(
    key: str,
    value: str,
    *,
    log_func: LogFunc = print,
) -> SubjectAttribute | None:
    oid = _SUBJECT_OIDS.get(key)
    if oid is None:
        log_func(f"不支持的主题字段: {key}")
        return None

    try:
        return cast(SubjectAttribute, x509.NameAttribute(oid, value))
    except Exception as exc:  # noqa: BLE001
        log_func(f"主题字段写入失败 ({key}): {exc}")
        return None


def _parse_subject(subject_info: str, log_func: LogFunc = print) -> SubjectName | None:
    attributes: list[SubjectAttribute] = []
    for component in _split_subject_components(subject_info):
        if "=" not in component:
            log_func(f"主题字段格式无效: {component}")
            return None
        key, value = component.split("=", 1)
        normalized_key = key.strip().upper()
        normalized_value = value.strip()
        if not normalized_value:
            log_func(f"主题字段为空: {normalized_key}")
            return None

        attribute = _build_name_attribute(
            normalized_key,
            normalized_value,
            log_func=log_func,
        )
        if attribute is None:
            return None
        attributes.append(attribute)

    if not attributes:
        log_func("主题信息为空")
        return None
    return x509.Name(attributes)


class _CaseSensitiveConfigParser(configparser.ConfigParser):
    def optionxform(self, optionstr: str) -> str:
        return optionstr


def _find_section_name(parser: configparser.ConfigParser, section_name: str) -> str | None:
    normalized_target = section_name.strip().lower()
    for candidate in parser.sections():
        if candidate.strip().lower() == normalized_target:
            return candidate
    return None


def _split_extension_tokens(raw_value: str) -> tuple[bool, list[str]]:
    tokens = [token.strip() for token in raw_value.split(",") if token.strip()]
    if tokens and tokens[0].lower() == "critical":
        return True, tokens[1:]
    return False, tokens


def _parse_general_name_value(
    name_type: str,
    value: str,
    *,
    log_func: LogFunc = print,
) -> x509.GeneralName | None:
    normalized_type = name_type.strip().upper()
    try:
        if normalized_type == "DNS":
            return x509.DNSName(value)
        if normalized_type == "IP":
            return x509.IPAddress(ipaddress.ip_address(value))
        if normalized_type == "EMAIL":
            return x509.RFC822Name(value)
        if normalized_type == "URI":
            return x509.UniformResourceIdentifier(value)
    except ValueError as exc:
        log_func(f"无效 SAN 项: {name_type}:{value} ({exc})")
        return None

    log_func(f"不支持的 SAN 类型: {name_type}:{value}")
    return None


def _parse_alt_names_section(
    parser: configparser.ConfigParser,
    section_name: str,
    *,
    log_func: LogFunc = print,
) -> list[x509.GeneralName] | None:
    actual_section = _find_section_name(parser, section_name)
    if actual_section is None:
        log_func(f"SAN 引用的节不存在: {section_name}")
        return None

    general_names: list[x509.GeneralName] = []
    for key, raw_value in parser.items(actual_section):
        value = raw_value.strip()
        if not value:
            log_func(f"SAN 项为空: {key}")
            return None
        name_type = key.split(".", 1)[0].strip()
        general_name = _parse_general_name_value(name_type, value, log_func=log_func)
        if general_name is None:
            return None
        general_names.append(general_name)
    return general_names


def _parse_inline_subject_alt_names(
    tokens: Sequence[str],
    *,
    log_func: LogFunc = print,
) -> list[x509.GeneralName] | None:
    general_names: list[x509.GeneralName] = []
    for token in tokens:
        if ":" not in token:
            log_func(f"不支持的 subjectAltName 配置: {token}")
            return None
        name_type, value = token.split(":", 1)
        general_name = _parse_general_name_value(
            name_type,
            value.strip(),
            log_func=log_func,
        )
        if general_name is None:
            return None
        general_names.append(general_name)
    return general_names


def _parse_subject_alt_name_value(
    parser: configparser.ConfigParser,
    raw_value: str,
    *,
    log_func: LogFunc = print,
) -> tuple[list[x509.GeneralName], bool] | None:
    critical, tokens = _split_extension_tokens(raw_value)
    if not tokens:
        log_func("subjectAltName 为空")
        return None

    if len(tokens) == 1 and tokens[0].startswith("@"):
        section_name = tokens[0][1:].strip()
        section_general_names = _parse_alt_names_section(parser, section_name, log_func=log_func)
        if section_general_names is None:
            return None
        if not section_general_names:
            log_func("subjectAltName 引用的节为空")
            return None
        return section_general_names, critical

    inline_general_names = _parse_inline_subject_alt_names(tokens, log_func=log_func)
    if not inline_general_names:
        log_func("subjectAltName 未解析到任何 SAN")
        return None
    return inline_general_names, critical


def _apply_basic_constraints_token(
    token: str,
    *,
    current_ca: bool | None,
    current_path_length: int | None,
    log_func: LogFunc = print,
) -> tuple[bool | None, int | None] | None:
    result: tuple[bool | None, int | None] | None = None
    if ":" not in token:
        log_func(f"不支持的 basicConstraints 配置: {token}")
    else:
        key, value = token.split(":", 1)
        normalized_key = key.strip().lower()
        normalized_value = value.strip()
        if normalized_key == "ca":
            if normalized_value.upper() == "TRUE":
                result = (True, current_path_length)
            elif normalized_value.upper() == "FALSE":
                result = (False, current_path_length)
            else:
                log_func(f"无效的 basicConstraints CA 值: {normalized_value}")
            return result
        if normalized_key == "pathlen":
            try:
                result = (current_ca, int(normalized_value))
            except ValueError:
                log_func(f"无效的 basicConstraints pathlen 值: {normalized_value}")
            return result

        log_func(f"不支持的 basicConstraints 键: {key}")

    return result


def _parse_basic_constraints(
    raw_value: str,
    *,
    log_func: LogFunc = print,
) -> tuple[x509.BasicConstraints, bool] | None:
    critical, tokens = _split_extension_tokens(raw_value)
    is_ca: bool | None = None
    path_length: int | None = None

    for token in tokens:
        updated = _apply_basic_constraints_token(
            token,
            current_ca=is_ca,
            current_path_length=path_length,
            log_func=log_func,
        )
        if updated is None:
            return None
        is_ca, path_length = updated

    if is_ca is None:
        log_func("basicConstraints 缺少 CA 标志")
        return None
    if not is_ca and path_length is not None:
        log_func("basicConstraints 在 CA:FALSE 时不允许 pathlen")
        return None
    return x509.BasicConstraints(ca=is_ca, path_length=path_length), critical


def _parse_key_usage(
    raw_value: str,
    *,
    log_func: LogFunc = print,
) -> tuple[x509.KeyUsage, bool] | None:
    critical, tokens = _split_extension_tokens(raw_value)
    if not tokens:
        log_func("keyUsage 为空")
        return None
    flags = {
        "content_commitment": False,
        "crl_sign": False,
        "data_encipherment": False,
        "decipher_only": False,
        "digital_signature": False,
        "encipher_only": False,
        "key_agreement": False,
        "key_cert_sign": False,
        "key_encipherment": False,
    }

    for token in tokens:
        normalized = token.replace(" ", "").lower()
        flag_name = _KEY_USAGE_FLAGS.get(normalized)
        if flag_name is None:
            log_func(f"不支持的 keyUsage 项: {token}")
            return None
        flags[flag_name] = True

    if (flags["encipher_only"] or flags["decipher_only"]) and not flags["key_agreement"]:
        log_func("keyUsage 中 encipherOnly/decipherOnly 需要同时启用 keyAgreement")
        return None

    return (
        x509.KeyUsage(
            digital_signature=flags["digital_signature"],
            content_commitment=flags["content_commitment"],
            key_encipherment=flags["key_encipherment"],
            data_encipherment=flags["data_encipherment"],
            key_agreement=flags["key_agreement"],
            key_cert_sign=flags["key_cert_sign"],
            crl_sign=flags["crl_sign"],
            encipher_only=flags["encipher_only"],
            decipher_only=flags["decipher_only"],
        ),
        critical,
    )


def _parse_extended_key_usage(
    raw_value: str,
    *,
    log_func: LogFunc = print,
) -> tuple[x509.ExtendedKeyUsage, bool] | None:
    critical, tokens = _split_extension_tokens(raw_value)
    if not tokens:
        log_func("extendedKeyUsage 为空")
        return None

    oids: list[ObjectIdentifier] = []
    for token in tokens:
        normalized = token.replace(" ", "").lower()
        oid = _EXTENDED_KEY_USAGE_OIDS.get(normalized)
        if oid is None:
            if all(part.isdigit() for part in normalized.split(".")) and "." in normalized:
                oid = ObjectIdentifier(normalized)
            else:
                log_func(f"不支持的 extendedKeyUsage 项: {token}")
                return None
        oids.append(oid)

    return x509.ExtendedKeyUsage(oids), critical


def _load_server_extension_parser(
    v3_req_config_text: str,
    domain_config_text: str,
    *,
    log_func: LogFunc = print,
) -> configparser.ConfigParser | None:
    parser = _CaseSensitiveConfigParser(interpolation=None, strict=False)
    try:
        parser.read_string(v3_req_config_text)
        parser.read_string(domain_config_text)
    except configparser.Error as exc:
        log_func(f"解析证书扩展配置失败: {exc}")
        return None
    return parser


def _load_v3_req_section_items(
    parser: configparser.ConfigParser,
    *,
    log_func: LogFunc = print,
) -> dict[str, str] | None:
    v3_req_section = _find_section_name(parser, "v3_req")
    if v3_req_section is None:
        log_func("缺少 v3_req 扩展配置节")
        return None

    section_items = {key.strip(): value.strip() for key, value in parser.items(v3_req_section)}
    for key in section_items:
        if key.replace(" ", "").lower() not in _V3_REQ_SUPPORTED_KEYS:
            log_func(f"不支持的 v3_req 配置项: {key}")
            return None
    return section_items


def _parse_optional_extended_key_usage(
    raw_value: str | None,
    *,
    log_func: LogFunc = print,
) -> tuple[x509.ExtendedKeyUsage | None, bool] | None:
    if not raw_value:
        return None, False
    return _parse_extended_key_usage(raw_value, log_func=log_func)


def _parse_server_extensions(
    v3_req_config_text: str,
    domain_config_text: str,
    *,
    log_func: LogFunc = print,
) -> ServerCertificateExtensions | None:
    parser = _load_server_extension_parser(
        v3_req_config_text,
        domain_config_text,
        log_func=log_func,
    )
    if parser is None:
        return None

    section_items = _load_v3_req_section_items(parser, log_func=log_func)
    if section_items is None:
        return None

    subject_alt_name_value = section_items.get("subjectAltName")
    if not subject_alt_name_value:
        log_func("v3_req 缺少 subjectAltName 配置")
        return None
    parsed_subject_alt_names = _parse_subject_alt_name_value(
        parser,
        subject_alt_name_value,
        log_func=log_func,
    )

    basic_constraints_value = section_items.get("basicConstraints", "CA:FALSE")
    parsed_basic_constraints = _parse_basic_constraints(
        basic_constraints_value,
        log_func=log_func,
    )

    key_usage_value = section_items.get("keyUsage")
    if not key_usage_value:
        log_func("v3_req 缺少 keyUsage 配置")
        return None
    parsed_key_usage = _parse_key_usage(key_usage_value, log_func=log_func)

    parsed_extended_key_usage = _parse_optional_extended_key_usage(
        section_items.get("extendedKeyUsage"),
        log_func=log_func,
    )
    if (
        parsed_subject_alt_names is None
        or parsed_basic_constraints is None
        or parsed_key_usage is None
        or parsed_extended_key_usage is None
    ):
        return None

    subject_alt_names, subject_alt_name_critical = parsed_subject_alt_names
    basic_constraints, basic_constraints_critical = parsed_basic_constraints
    key_usage, key_usage_critical = parsed_key_usage
    extended_key_usage, extended_key_usage_critical = parsed_extended_key_usage

    return ServerCertificateExtensions(
        subject_alt_names=subject_alt_names,
        subject_alt_name_critical=subject_alt_name_critical,
        basic_constraints=basic_constraints,
        basic_constraints_critical=basic_constraints_critical,
        key_usage=key_usage,
        key_usage_critical=key_usage_critical,
        extended_key_usage=extended_key_usage,
        extended_key_usage_critical=extended_key_usage_critical,
    )


def _serialize_private_key(private_key: rsa.RSAPrivateKey) -> bytes:
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )


def _serialize_certificate(certificate: x509.Certificate) -> bytes:
    return certificate.public_bytes(serialization.Encoding.PEM)


def _serialize_csr(csr: x509.CertificateSigningRequest) -> bytes:
    return csr.public_bytes(serialization.Encoding.PEM)


def _missing_required_file(paths: Sequence[str]) -> str | None:
    for path in paths:
        if not os.path.exists(path):
            return path
    return None


def _record_ca_cert_metadata(
    resource_manager: ResourceManager,
    certificate: x509.Certificate,
    log_func: LogFunc = print,
) -> bool:
    return save_ca_info(
        resource_manager,
        fingerprint_sha1=certificate_fingerprint_sha1(certificate),
        not_after_unix=certificate_not_after_unix(certificate),
        log_func=log_func,
    )


def create_default_config_files(
    resource_manager: ResourceManager, log_func: LogFunc = print
) -> bool:
    """创建默认配置文件（如果不存在）"""
    ca_dir = resource_manager.ca_path

    if not os.path.exists(ca_dir):
        try:
            os.makedirs(ca_dir)
            log_func(f"创建目录: {ca_dir}")
        except Exception as exc:  # noqa: BLE001
            log_func(f"无法创建ca目录: {exc}")
            return False

    config_files = {
        "openssl.cnf": """[ req ]
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
""",
        "v3_ca.cnf": """[ v3_ca ]
subjectKeyIdentifier=hash
authorityKeyIdentifier=keyid:always,issuer
basicConstraints = critical, CA:TRUE, pathlen:3
keyUsage = critical, cRLSign, keyCertSign
nsCertType = sslCA, emailCA
""",
        "v3_req.cnf": """[ v3_req ]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
subjectAltName = @alt_names
""",
        "api.openai.com.cnf": """
[ v3_req ]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = api.openai.com
""",
        "api.openai.com.subj": "/C=CN/ST=State/L=City/O=Organization/OU=Unit/CN=api.openai.com",
    }

    for filename, content in config_files.items():
        file_path = resource_manager.get_config_file(filename)
        if not os.path.exists(file_path):
            try:
                with open(file_path, "w", encoding="utf-8") as handle:
                    handle.write(content)
                log_func(f"创建配置文件: {file_path}")
            except Exception as exc:  # noqa: BLE001
                log_func(f"无法创建文件 {file_path}: {exc}")
                return False
        else:
            log_func(f"配置文件已存在: {file_path}")

    return True


def _build_ca_certificate(
    private_key: rsa.RSAPrivateKey,
    *,
    ca_common_name: str,
) -> x509.Certificate:
    subject = x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, "CN"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "X"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "X"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "X"),
            x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, "X"),
            x509.NameAttribute(NameOID.COMMON_NAME, ca_common_name),
        ]
    )
    now = _utc_now()
    return (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(subject)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - timedelta(days=1))
        .not_valid_after(now + timedelta(days=36500))
        .add_extension(x509.BasicConstraints(ca=True, path_length=3), critical=True)
        .add_extension(
            x509.KeyUsage(
                digital_signature=False,
                content_commitment=False,
                key_encipherment=False,
                data_encipherment=False,
                key_agreement=False,
                key_cert_sign=True,
                crl_sign=True,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        )
        .add_extension(
            x509.SubjectKeyIdentifier.from_public_key(private_key.public_key()),
            critical=False,
        )
        .add_extension(
            x509.AuthorityKeyIdentifier.from_issuer_public_key(private_key.public_key()),
            critical=False,
        )
        .sign(private_key, hashes.SHA256())
    )


def generate_ca_cert(
    resource_manager: ResourceManager, log_func: LogFunc = print, *, ca_common_name: str = "MTGA_CA"
) -> bool:
    """生成 CA 证书和私钥"""
    log_func("开始生成CA证书和私钥...")

    ca_key_path = resource_manager.get_ca_key_file()
    ca_crt_path = resource_manager.get_ca_cert_file()

    try:
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        certificate = _build_ca_certificate(private_key, ca_common_name=ca_common_name)
    except Exception as exc:  # noqa: BLE001
        log_func(f"生成 CA 证书材料失败: {exc}")
        return False

    if not _write_bytes(ca_key_path, _serialize_private_key(private_key), "CA私钥已生成", log_func):
        return False
    if not _write_bytes(ca_crt_path, _serialize_certificate(certificate), "CA证书已生成", log_func):
        return False
    if not _record_ca_cert_metadata(resource_manager, certificate, log_func):
        log_func("CA 证书元数据写入失败")
        return False
    return True


def _load_ca_certificate(ca_cert_path: str, log_func: LogFunc = print) -> x509.Certificate | None:
    payload = _read_text_file(ca_cert_path, "CA证书文件", log_func)
    if payload is None:
        return None
    try:
        return x509.load_pem_x509_certificate(payload.encode("utf-8"))
    except Exception as exc:  # noqa: BLE001
        log_func(f"加载 CA 证书失败: {exc}")
        return None


def _load_ca_private_key(ca_key_path: str, log_func: LogFunc = print) -> rsa.RSAPrivateKey | None:
    payload = _read_text_file(ca_key_path, "CA私钥文件", log_func)
    if payload is None:
        return None
    try:
        private_key = serialization.load_pem_private_key(payload.encode("utf-8"), password=None)
    except Exception as exc:  # noqa: BLE001
        log_func(f"加载 CA 私钥失败: {exc}")
        return None

    if not isinstance(private_key, rsa.RSAPrivateKey):
        log_func("CA 私钥类型无效：仅支持 RSA")
        return None
    return private_key


def _certificate_matches_private_key(
    certificate: x509.Certificate,
    private_key: rsa.RSAPrivateKey,
    *,
    log_func: LogFunc = print,
) -> bool:
    cert_public_key = certificate.public_key()
    private_public_key = private_key.public_key()
    try:
        cert_public_bytes = cert_public_key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        private_public_bytes = private_public_key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    except Exception as exc:  # noqa: BLE001
        log_func(f"校验 CA 证书与私钥匹配失败: {exc}")
        return False
    return cert_public_bytes == private_public_bytes


def _build_server_certificate(
    *,
    subject: SubjectName,
    extensions: ServerCertificateExtensions,
    ca_certificate: x509.Certificate,
    ca_private_key: rsa.RSAPrivateKey,
    server_private_key: rsa.RSAPrivateKey,
) -> x509.Certificate:
    now = _utc_now()
    builder = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(ca_certificate.subject)
        .public_key(server_private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - timedelta(days=1))
        .not_valid_after(now + timedelta(days=365))
        .add_extension(
            extensions.basic_constraints,
            critical=extensions.basic_constraints_critical,
        )
        .add_extension(
            extensions.key_usage,
            critical=extensions.key_usage_critical,
        )
        .add_extension(
            x509.SubjectKeyIdentifier.from_public_key(server_private_key.public_key()),
            critical=False,
        )
        .add_extension(
            x509.AuthorityKeyIdentifier.from_issuer_public_key(ca_private_key.public_key()),
            critical=False,
        )
    )
    if extensions.extended_key_usage is not None:
        builder = builder.add_extension(
            extensions.extended_key_usage,
            critical=extensions.extended_key_usage_critical,
        )
    if extensions.subject_alt_names:
        builder = builder.add_extension(
            x509.SubjectAlternativeName(list(extensions.subject_alt_names)),
            critical=extensions.subject_alt_name_critical,
        )
    return builder.sign(ca_private_key, hashes.SHA256())


def _load_server_subject_and_extensions(
    resource_manager: ResourceManager,
    domain: str,
    *,
    log_func: LogFunc = print,
) -> tuple[SubjectName, ServerCertificateExtensions] | None:
    subject_path = resource_manager.get_config_file(f"{domain}.subj")
    v3_req_path = resource_manager.get_config_file("v3_req.cnf")
    san_config_path = resource_manager.get_config_file(f"{domain}.cnf")

    required_files = [subject_path, v3_req_path, san_config_path]
    missing_file = _missing_required_file(required_files)
    if missing_file is not None:
        log_func(f"必需文件不存在: {missing_file}")
        return None

    subject_info = _read_text_file(subject_path, f"{domain}.subj", log_func)
    v3_req_config = _read_text_file(v3_req_path, "v3_req.cnf", log_func)
    san_config = _read_text_file(san_config_path, f"{domain}.cnf", log_func)
    if subject_info is None or v3_req_config is None or san_config is None:
        return None

    subject = _parse_subject(subject_info.strip(), log_func)
    extensions = _parse_server_extensions(
        v3_req_config,
        san_config,
        log_func=log_func,
    )
    if subject is None or extensions is None:
        return None
    return subject, extensions


def _load_ca_materials(
    resource_manager: ResourceManager,
    *,
    log_func: LogFunc = print,
) -> tuple[x509.Certificate, rsa.RSAPrivateKey] | None:
    ca_key_path = resource_manager.get_ca_key_file()
    ca_crt_path = resource_manager.get_ca_cert_file()
    missing_file = _missing_required_file([ca_crt_path, ca_key_path])
    if missing_file is not None:
        log_func(f"必需文件不存在: {missing_file}")
        return None

    ca_certificate = _load_ca_certificate(ca_crt_path, log_func)
    ca_private_key = _load_ca_private_key(ca_key_path, log_func)
    if ca_certificate is None or ca_private_key is None:
        return None
    if not _certificate_matches_private_key(
        ca_certificate,
        ca_private_key,
        log_func=log_func,
    ):
        log_func("CA 证书与私钥不匹配")
        return None
    return ca_certificate, ca_private_key


def _load_server_cert_context(
    resource_manager: ResourceManager,
    domain: str,
    log_func: LogFunc = print,
) -> ServerCertContext | None:
    subject_and_extensions = _load_server_subject_and_extensions(
        resource_manager,
        domain,
        log_func=log_func,
    )
    ca_materials = _load_ca_materials(resource_manager, log_func=log_func)
    if subject_and_extensions is None or ca_materials is None:
        return None

    subject, extensions = subject_and_extensions
    ca_certificate, ca_private_key = ca_materials

    return ServerCertContext(
        subject=subject,
        extensions=extensions,
        ca_certificate=ca_certificate,
        ca_private_key=ca_private_key,
    )


def _write_server_key_and_csr(
    resource_manager: ResourceManager,
    domain: str,
    *,
    context: ServerCertContext,
    server_private_key: rsa.RSAPrivateKey,
    log_func: LogFunc = print,
) -> bool:
    server_key_path = resource_manager.get_key_file(domain)
    if not _write_bytes(
        server_key_path,
        _serialize_private_key(server_private_key),
        f"私钥 {domain}.key 生成成功",
        log_func,
    ):
        return False

    try:
        csr = (
            x509.CertificateSigningRequestBuilder()
            .subject_name(context.subject)
            .add_extension(
                x509.SubjectAlternativeName(list(context.extensions.subject_alt_names)),
                critical=context.extensions.subject_alt_name_critical,
            )
            .sign(server_private_key, hashes.SHA256())
        )
    except Exception as exc:  # noqa: BLE001
        log_func(f"生成 CSR 失败: {exc}")
        return False

    server_csr_path = os.path.join(resource_manager.ca_path, f"{domain}.csr")
    return _write_bytes(
        server_csr_path,
        _serialize_csr(csr),
        f"CSR {domain}.csr 生成成功",
        log_func,
    )


def _write_server_certificate(
    resource_manager: ResourceManager,
    domain: str,
    *,
    context: ServerCertContext,
    server_private_key: rsa.RSAPrivateKey,
    log_func: LogFunc = print,
) -> bool:
    try:
        server_certificate = _build_server_certificate(
            subject=context.subject,
            extensions=context.extensions,
            ca_certificate=context.ca_certificate,
            ca_private_key=context.ca_private_key,
            server_private_key=server_private_key,
        )
    except Exception as exc:  # noqa: BLE001
        log_func(f"签署服务器证书失败: {exc}")
        return False

    server_crt_path = resource_manager.get_cert_file(domain)
    if not _write_bytes(
        server_crt_path,
        _serialize_certificate(server_certificate),
        f"证书 {domain}.crt 生成成功",
        log_func,
    ):
        return False

    file_size = os.path.getsize(server_crt_path)
    if file_size == 0:
        log_func(f"错误: 证书文件 {server_crt_path} 为空文件")
        return False

    log_func(f"证书 {domain}.crt 文件大小: {file_size} bytes")
    return True


def generate_server_cert(
    resource_manager: ResourceManager, domain: str = "api.openai.com", log_func: LogFunc = print
) -> bool:
    """生成服务器证书"""
    log_func(f"开始为 {domain} 生成服务器证书...")

    context = _load_server_cert_context(resource_manager, domain, log_func)
    if context is None:
        return False

    try:
        server_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    except Exception as exc:  # noqa: BLE001
        log_func(f"生成服务器私钥失败: {exc}")
        return False

    if not _write_server_key_and_csr(
        resource_manager,
        domain,
        context=context,
        server_private_key=server_private_key,
        log_func=log_func,
    ):
        return False

    if not _write_server_certificate(
        resource_manager,
        domain,
        context=context,
        server_private_key=server_private_key,
        log_func=log_func,
    ):
        return False

    log_func("")
    log_func("=== 服务器证书生成完成 ===")
    return True


def generate_certificates(
    domain: str = "api.openai.com", *, ca_common_name: str = "MTGA_CA", log_func: LogFunc = print
) -> bool:
    """
    一键生成 CA 证书和服务器证书

    参数:
        domain: 服务器证书的域名
        log_func: 日志输出函数

    返回:
        成功返回 True，失败返回 False
    """
    log_func("=" * 60)
    log_func("证书生成工具 - 一键生成CA证书和服务器证书")
    log_func("=" * 60)
    log_func(f"使用 Python cryptography 生成证书: {cryptography_version}")

    resource_manager = ResourceManager()

    if not create_default_config_files(resource_manager, log_func):
        return False

    if not generate_ca_cert(resource_manager, log_func, ca_common_name=ca_common_name):
        return False

    if not generate_server_cert(resource_manager, domain, log_func):
        return False

    log_func("=" * 60)
    log_func("证书生成完成！")
    log_func("=" * 60)
    log_func(f"CA 证书: {resource_manager.get_ca_cert_file()}")
    log_func(f"CA 私钥: {resource_manager.get_ca_key_file()} (请妥善保管，勿泄露)")
    log_func(f"服务器证书: {resource_manager.get_cert_file(domain)}")
    log_func(f"服务器私钥: {resource_manager.get_key_file(domain)} (请妥善保管，勿泄露)")
    log_func("")
    log_func("后续步骤:")
    log_func("1. 将CA证书 (ca.crt) 导入到Windows的受信任的根证书颁发机构存储中")
    log_func("2. 修改hosts文件，将api.openai.com指向127.0.0.1")
    log_func("3. 配置并运行代理服务器")
    log_func("=" * 60)

    return True
