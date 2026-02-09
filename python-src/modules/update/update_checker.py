"""封装 GitHub 最新版本查询与版本号比较逻辑。"""

from __future__ import annotations

import html
import re
from dataclasses import dataclass
from functools import lru_cache

import requests

_SEMVER_PATTERN = re.compile(r"v?(?P<version>\d+(?:\.\d+)*)", re.IGNORECASE)
_G_EMOJI_PATTERN = re.compile(
    r"<g-emoji\b(?P<attrs>[^>]*)>(?P<content>.*?)</g-emoji>",
    re.IGNORECASE | re.DOTALL,
)
_EMOJI_SHORTCODE_PATTERN = re.compile(r":(?P<name>[a-z0-9_+-]+):", re.IGNORECASE)
_IMG_TAG_PATTERN = re.compile(r"<img\b(?P<attrs>[^>]*?)\s*/?>", re.IGNORECASE | re.DOTALL)


@dataclass(slots=True)
class HtmlFontOptions:
    family: str | None = None
    size: int | None = None
    weight: str | None = None


@dataclass(slots=True)
class RenderContext:
    repo: str
    timeout: int = 10
    user_agent: str | None = None
    font: HtmlFontOptions | None = None
    session: requests.Session | None = None


@dataclass(slots=True)
class ReleaseInfo:
    """GitHub 最新发行版的核心信息。"""

    version_label: str | None
    release_notes: str
    release_url: str


def render_markdown_via_github_api(
    markdown_text: str | None,
    *,
    context: RenderContext,
) -> str:
    """调用 GitHub /markdown API 渲染 Markdown 为 HTML。

    说明：
    - 该接口返回的是 HTML 片段；这里会包装成一个完整 HTML 文档，便于 GUI 直接 load_html。
    - 可选注入仅与字体相关的最小 CSS（用于沿用 GUI 的全局字体设置）。
    - 渲染失败时会降级为 <pre> 纯文本。
    """
    # safe_source = _replace_emoji_shortcodes_with_img(
    #     markdown_text or "",
    #     timeout=timeout,
    #     user_agent=user_agent,
    # )
    safe_source = markdown_text or ""

    font_family = context.font.family if context.font else None
    font_size = context.font.size if context.font else None
    font_weight = context.font.weight if context.font else None

    escaped_family = (font_family or "").replace('"', r"\"").strip()
    font_stack = (
        f'"{escaped_family}", "Maple Mono NF CN", "Microsoft YaHei UI", "Microsoft YaHei", '
        '"PingFang SC", "Hiragino Sans GB", "Segoe UI", "Arial", sans-serif'
        if escaped_family
        else '"Maple Mono NF CN", "Microsoft YaHei UI", "Microsoft YaHei", "PingFang SC", '
        '"Hiragino Sans GB", "Segoe UI", "Arial", sans-serif'
    )
    css_rules: list[str] = []
    if font_family:
        css_rules.append(f"font-family: {font_stack};")
    if font_size:
        css_rules.append(f"font-size: {int(font_size)}px;")
    if font_weight:
        css_rules.append(f"font-weight: {font_weight};")
    style_chunks: list[str] = []
    if css_rules:
        style_chunks.append(f"body{{{''.join(css_rules)}}}")
    style_chunks.append("img.g-emoji{height:1em;width:1em;}")
    base_style = f"<style>{''.join(style_chunks)}</style>" if style_chunks else ""
    headers = {
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
    }
    if context.user_agent:
        headers["User-Agent"] = context.user_agent

    client = context.session or requests
    try:
        response = client.post(
            "https://api.github.com/markdown",
            json={"text": safe_source, "mode": "gfm", "context": context.repo},
            timeout=context.timeout,
            headers=headers,
        )
        if response.status_code == requests.codes.ok:  # type: ignore[attr-defined]
            rendered_fragment = response.text or ""
            # rendered_fragment = _replace_g_emoji_with_img(rendered_fragment)
            # rendered_fragment = _style_emoji_images(rendered_fragment)
            return "".join(
                (
                    "<html><head><meta charset='utf-8'>",
                    base_style,
                    "</head><body>",
                    rendered_fragment,
                    "</body></html>",
                )
            )
    except requests.RequestException:
        pass

    return "".join(
        (
            "<html><head><meta charset='utf-8'>",
            base_style,
            "</head><body><pre>",
            html.escape(safe_source),
            "</pre></body></html>",
        )
    )


def _replace_g_emoji_with_img(rendered_html: str) -> str:
    """将 GitHub 的 <g-emoji> 转为 <img>，避免字体缺失导致空白。"""

    def _extract_attr(attrs: str, name: str) -> str | None:
        match = re.search(rf'{name}=(["\'])(?P<value>.*?)\1', attrs, re.IGNORECASE)
        if not match:
            return None
        return match.group("value")

    def _replace(match: re.Match[str]) -> str:
        attrs = match.group("attrs")
        content = match.group("content").strip()
        fallback_src = _extract_attr(attrs, "fallback-src")
        if not fallback_src:
            return match.group(0)
        alias = _extract_attr(attrs, "alias")
        alt_text = html.escape((alias or content or "").strip(), quote=True)
        return f'<img src="{fallback_src}" alt="{alt_text}" class="g-emoji">'

    return _G_EMOJI_PATTERN.sub(_replace, rendered_html)


def _style_emoji_images(rendered_html: str) -> str:
    """为 emoji 图片补齐尺寸与对齐样式，保持与 GitHub 接近的显示效果。"""

    def _extract_attr(attrs: str, name: str) -> str | None:
        match = re.search(rf'{name}=(["\'])(?P<value>.*?)\1', attrs, re.IGNORECASE)
        if not match:
            return None
        return match.group("value")

    def _replace_or_add_attr(attrs: str, name: str, value: str) -> str:
        if re.search(rf'{name}=(["\'])', attrs, re.IGNORECASE):
            return re.sub(
                rf'{name}=(["\'])(?P<value>.*?)\1',
                f'{name}="{value}"',
                attrs,
                flags=re.IGNORECASE | re.DOTALL,
            )
        return f"{attrs} {name}=\"{value}\""

    def _is_github_emoji(attrs: str) -> bool:
        data_canonical_src = _extract_attr(attrs, "data-canonical-src")
        src = _extract_attr(attrs, "src")
        if data_canonical_src and "/images/icons/emoji/" in data_canonical_src:
            return True
        if src and "/images/icons/emoji/" in src:
            return True
        if src and "camo.githubusercontent.com" in src:
            return bool(data_canonical_src and "/images/icons/emoji/" in data_canonical_src)
        return False

    def _replace(match: re.Match[str]) -> str:
        attrs = match.group("attrs").strip()
        if not _is_github_emoji(attrs):
            return match.group(0)
        style_value = _extract_attr(attrs, "style") or ""
        style_value = re.sub(
            r"vertical-align\s*:\s*[^;]+;?",
            "",
            style_value,
            flags=re.IGNORECASE,
        )
        style_suffix = "height:1em;width:1em;"
        if style_suffix not in style_value:
            style_value = f"{style_value.rstrip(';')};{style_suffix}".lstrip(";")
        new_attrs = _replace_or_add_attr(attrs, "style", style_value)
        return f"<img {new_attrs}>"

    return _IMG_TAG_PATTERN.sub(_replace, rendered_html)


def _replace_emoji_shortcodes_with_img(
    markdown_text: str,
    *,
    timeout: int,
    user_agent: str | None,
) -> str:
    """将 :shortcode: 替换为 <img>，避免 emoji 字体缺失。"""
    emoji_urls = _get_emoji_urls(timeout=timeout, user_agent=user_agent)
    if not emoji_urls:
        return markdown_text

    def _replace(match: re.Match[str]) -> str:
        name = match.group("name")
        url = emoji_urls.get(name)
        if not url:
            return match.group(0)
        alt_text = f":{name}:"
        return f'<img src="{url}" alt="{alt_text}" class="g-emoji">'

    return _EMOJI_SHORTCODE_PATTERN.sub(_replace, markdown_text)


@lru_cache(maxsize=8)
def _get_emoji_urls(*, timeout: int, user_agent: str | None) -> dict[str, str]:
    headers = {"Accept": "application/vnd.github+json"}
    if user_agent:
        headers["User-Agent"] = user_agent

    try:
        response = requests.get(
            "https://api.github.com/emojis",
            timeout=timeout,
            headers=headers,
        )
        if response.status_code == requests.codes.ok:  # type: ignore[attr-defined]
            data = response.json()
            if isinstance(data, dict):
                return {str(k): str(v) for k, v in data.items()}
    except requests.RequestException:
        pass

    return {}


def _normalize_version_tuple(version_text: str | None) -> tuple[int, ...]:
    """Convert 版本字符串为整数元组，便于比较。"""
    if not version_text:
        return ()
    match = _SEMVER_PATTERN.search(version_text.strip())
    if not match:
        return ()
    numeric_part = match.group("version").split("-")[0]
    tokens: list[int] = []
    for chunk in numeric_part.split("."):
        digits = re.match(r"\d+", chunk)
        if not digits:
            continue
        tokens.append(int(digits.group()))
    return tuple(tokens)


def extract_version_label(text: str | None) -> str | None:
    """从标题或标签中抓取形如 vX.Y.Z 的片段。"""
    if not text:
        return None
    match = _SEMVER_PATTERN.search(text.strip())
    if not match:
        return None
    version = match.group(0)
    if not version.lower().startswith("v"):
        version = f"v{match.group('version')}"
    return version


def is_remote_version_newer(remote_version: str | None, local_version: str | None) -> bool:
    """比较远程与本地版本号，先看主版本，若相同则比较次版本。"""
    remote_tuple = _normalize_version_tuple(remote_version)
    local_tuple = _normalize_version_tuple(local_version)
    if not remote_tuple:
        return False
    if not local_tuple:
        return True
    major_remote = remote_tuple[0]
    major_local = local_tuple[0]
    if major_remote == major_local:
        return remote_tuple > local_tuple
    return major_remote > major_local


def fetch_latest_release(
    repo: str,
    *,
    timeout: int = 10,
    user_agent: str | None = None,
    font: HtmlFontOptions | None = None,
    session: requests.Session | None = None,
) -> ReleaseInfo:
    """从 GitHub API 获取 latest 发行版信息。"""
    if not repo:
        raise ValueError("repo 不能为空")
    api_url = f"https://api.github.com/repos/{repo}/releases/latest"
    headers = {"Accept": "application/vnd.github+json"}
    if user_agent:
        headers["User-Agent"] = user_agent

    client = session or requests
    response = client.get(api_url, timeout=timeout, headers=headers)
    if response.status_code != requests.codes.ok:  # type: ignore[attr-defined]
        raise RuntimeError(f"GitHub 返回 {response.status_code}")

    data = response.json()
    version_label = extract_version_label(data.get("name")) or extract_version_label(
        data.get("tag_name")
    )
    release_notes = render_markdown_via_github_api(
        data.get("body") or "",
        context=RenderContext(
            repo=repo,
            timeout=timeout,
            user_agent=user_agent,
            font=font,
            session=session,
        ),
    )
    release_url = data.get("html_url") or ""
    return ReleaseInfo(
        version_label=version_label,
        release_notes=release_notes,
        release_url=release_url,
    )


__all__ = [
    "HtmlFontOptions",
    "ReleaseInfo",
    "extract_version_label",
    "is_remote_version_newer",
    "fetch_latest_release",
    "render_markdown_via_github_api",
]
