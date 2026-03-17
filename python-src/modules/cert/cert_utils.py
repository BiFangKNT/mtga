"""
证书工具函数（跨模块复用）
用于证书检查/清理等场景的日志输出与 certutil 解析。
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from datetime import UTC, datetime

from cryptography import x509
from cryptography.hazmat.primitives import hashes

type LogFunc = Callable[[str], None]

def log_lines(lines: str | None, log_func: LogFunc = print) -> None:
    """逐行输出日志，自动跳过空行。"""
    if not lines:
        return
    for line in lines.splitlines():
        if line.strip():
            log_func(line.strip())


def normalize_fingerprint(value: str | None) -> str | None:
    """规范化证书指纹（去空白/冒号，转小写）。"""
    if not value:
        return None
    return value.replace(":", "").replace(" ", "").strip().lower()


def parse_openssl_fingerprint(output: str | None) -> str | None:
    """解析 OpenSSL 指纹输出，返回规范化 SHA1 指纹。"""
    if not output:
        return None
    for line in output.splitlines():
        if "fingerprint=" in line.lower():
            return normalize_fingerprint(line.split("=", 1)[1])
    return None


def parse_openssl_enddate_to_unix(output: str | None) -> int | None:
    """解析 OpenSSL notAfter 输出并转换为 Unix 时间戳（秒）。"""
    if not output:
        return None
    for line in output.splitlines():
        lower = line.lower()
        if lower.startswith("notafter="):
            date_str = line.split("=", 1)[1].strip()
            if date_str.endswith(" GMT"):
                date_str = date_str[:-4].strip()
            normalized = " ".join(date_str.split())
            try:
                parsed = datetime.strptime(normalized, "%b %d %H:%M:%S %Y")
            except ValueError:
                return None
            return int(parsed.replace(tzinfo=UTC).timestamp())
    return None


def certificate_fingerprint_sha1(certificate: x509.Certificate) -> str:
    """提取证书 SHA1 指纹并规范化。"""
    return normalize_fingerprint(certificate.fingerprint(hashes.SHA1()).hex()) or ""


def certificate_not_after_unix(certificate: x509.Certificate) -> int:
    """将证书到期时间转换为 Unix 时间戳（秒）。"""
    not_after_utc = getattr(certificate, "not_valid_after_utc", None)
    if isinstance(not_after_utc, datetime):
        return int(not_after_utc.timestamp())
    return int(certificate.not_valid_after.replace(tzinfo=UTC).timestamp())


def certificate_name_to_text(name: x509.Name) -> str:
    """将 cryptography 的名称对象转换为可读字符串。"""
    return name.rfc4514_string()


def parse_certutil_store(output: str) -> list[dict[str, str]]:
    """解析 certutil -store 输出，提取 subject/issuer/thumbprint。"""
    entries: list[dict[str, str]] = []
    current: dict[str, str] = {}

    def flush() -> None:
        if current:
            entries.append(current.copy())
            current.clear()

    for raw_line in output.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        lower = line.lower()
        if lower.startswith("================"):
            flush()
            continue

        if lower.startswith(("使用者:", "subject:")):
            current["subject"] = line.split(":", 1)[1].strip()
            continue

        if lower.startswith(("颁发者:", "issuer:")):
            current["issuer"] = line.split(":", 1)[1].strip()
            continue

        if "证书哈希" in line or lower.startswith("certificate hash"):
            current["thumbprint"] = line.split(":", 1)[1].strip().replace(" ", "")
            continue

    flush()
    return entries


def filter_certs_by_name(
    entries: Iterable[dict[str, str]],
    ca_common_name: str,
) -> list[dict[str, str]]:
    """根据 CA common name 过滤证书条目。"""
    target = ca_common_name.lower()
    matched: list[dict[str, str]] = []
    for entry in entries:
        subject = entry.get("subject", "")
        issuer = entry.get("issuer", "")
        if target in subject.lower() or target in issuer.lower():
            matched.append(entry)
    return matched


__all__ = [
    "certificate_fingerprint_sha1",
    "certificate_name_to_text",
    "certificate_not_after_unix",
    "filter_certs_by_name",
    "log_lines",
    "normalize_fingerprint",
    "parse_certutil_store",
    "parse_openssl_enddate_to_unix",
    "parse_openssl_fingerprint",
]
