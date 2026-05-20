"""
Centralized configuration for matrix-publisher-panel.
All paths, platform mappings, and defaults live here so they can be
adjusted in one place or overridden via environment variables.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

ROOT = Path(__file__).parent.resolve()
WORKSPACE = ROOT.parent
SAU_ROOT = Path(os.environ.get("SAU_ROOT", str(WORKSPACE / "social-auto-upload")))
SAU_ENTRY = SAU_ROOT / "sau_cli.py"
SAU_VENV_PYTHON = Path(
    os.environ.get(
        "SAU_PYTHON",
        str(SAU_ROOT / ".venv" / "Scripts" / "python.exe"),
    )
)
COOKIES_DIR = SAU_ROOT / "cookies"

# ---------------------------------------------------------------------------
# Network / server
# ---------------------------------------------------------------------------

DEFAULT_PORT = int(os.environ.get("MATRIX_PANEL_PORT", "8787"))

# ---------------------------------------------------------------------------
# Platform registry
# ---------------------------------------------------------------------------

SUPPORTED_PLATFORMS: dict[str, str] = {
    "douyin": "douyin",
    "xiaohongshu": "xiaohongshu",
    "shipinhao": "tencent",
}

PLATFORM_LABELS: dict[str, str] = {
    "douyin": "抖音",
    "xiaohongshu": "小红书",
    "shipinhao": "视频号",
    "tencent": "视频号",
}

# Reverse-proxy target hosts (platform key → real domain)
PROXY_HOSTS: dict[str, str] = {
    "douyin": "creator.douyin.com",
    "xiaohongshu": "creator.xiaohongshu.com",
    "shipinhao": "channels.weixin.qq.com",
}

# Headers to strip from proxied responses so pages can be iframed
STRIP_HEADERS: set[str] = {"x-frame-options", "content-security-policy"}

# Target URLs for "open messaging page in headed browser"
MESSAGING_URLS: dict[str, str] = {
    "douyin": "https://creator.douyin.com/creator-micro/home",
    "xiaohongshu": "https://creator.xiaohongshu.com",
    "shipinhao": "https://channels.weixin.qq.com/platform/post/list",
    "tencent": "https://channels.weixin.qq.com/platform/post/list",
}

# ---------------------------------------------------------------------------
# Browser
# ---------------------------------------------------------------------------

PREFERRED_BROWSER = os.environ.get("PREFERRED_BROWSER", "").lower()

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def account_file(platform: str, account_name: str) -> Path:
    """Path to a platform's Playwright storage_state cookie JSON."""
    return COOKIES_DIR / f"{platform}_{account_name}.json"


def python_executable() -> str:
    if SAU_VENV_PYTHON.exists():
        return str(SAU_VENV_PYTHON)
    return sys.executable


def launch_kwargs(headless: bool = True) -> dict:
    """Build Playwright launch args for the user's preferred browser."""
    kwargs: dict = {"headless": headless}

    if PREFERRED_BROWSER in ("chrome", "msedge", "chromium"):
        kwargs["channel"] = PREFERRED_BROWSER
    else:
        kwargs["channel"] = "msedge" if sys.platform == "win32" else "chrome"
    return kwargs
