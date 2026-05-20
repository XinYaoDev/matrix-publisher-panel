from __future__ import annotations

import json
import os
import subprocess
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

try:
    import httpx
except ImportError:
    httpx = None  # proxy won't work, but notifications and open-messages still will

from config import (
    ROOT,
    SAU_ROOT,
    SAU_ENTRY,
    SAU_VENV_PYTHON,
    SUPPORTED_PLATFORMS,
    PROXY_HOSTS,
    STRIP_HEADERS,
    COOKIES_DIR,
    DEFAULT_PORT,
    python_executable,
    account_file,
)


def json_response(handler: SimpleHTTPRequestHandler, status: int, payload: dict) -> None:
    data = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(data)))
    handler.end_headers()
    handler.wfile.write(data)


def read_json(handler: SimpleHTTPRequestHandler) -> dict:
    length = int(handler.headers.get("Content-Length", "0") or "0")
    if length <= 0:
        return {}
    raw = handler.rfile.read(length)
    if not raw:
        return {}
    return json.loads(raw.decode("utf-8"))



def run_sau(args: list[str], timeout: int = 900) -> dict:
    if not SAU_ENTRY.exists():
        return {
            "ok": False,
            "returncode": -1,
            "stdout": "",
            "stderr": f"找不到 social-auto-upload: {SAU_ENTRY}",
            "command": [],
        }

    command = [python_executable(), str(SAU_ENTRY), *args]
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    try:
        result = subprocess.run(
            command,
            cwd=str(SAU_ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            env=env,
        )
        return {
            "ok": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "command": command,
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "ok": False,
            "returncode": -2,
            "stdout": exc.stdout or "",
            "stderr": f"执行超时: {exc}",
            "command": command,
        }


def require_platform(payload: dict) -> str:
    platform = str(payload.get("platform") or "").strip()
    if platform not in SUPPORTED_PLATFORMS:
        raise ValueError(f"不支持该平台: {platform}，当前支持: {', '.join(sorted(SUPPORTED_PLATFORMS))}")
    return SUPPORTED_PLATFORMS[platform]


def require_account(payload: dict) -> str:
    account = str(payload.get("account") or "").strip()
    if not account:
        raise ValueError("缺少 account")
    return account


def clean_tags(raw: object) -> str:
    if isinstance(raw, list):
        return ",".join(str(item).strip().lstrip("#") for item in raw if str(item).strip())
    return str(raw or "").strip()


def existing_path(raw: object, field: str) -> str:
    value = str(raw or "").strip().strip('"')
    if not value:
        raise ValueError(f"缺少 {field}")
    path = Path(value)
    if not path.exists():
        raise ValueError(f"{field} 不存在: {value}")
    return str(path)


def load_cookies_from_storage(platform: str, account_name: str) -> dict[str, str]:
    """Read Playwright storage_state JSON and return cookies as name→value dict."""
    cookie_file = account_file(platform, account_name)
    if not cookie_file.exists():
        return {}
    try:
        data = json.loads(cookie_file.read_text(encoding="utf-8"))
        return {c["name"]: c["value"] for c in data.get("cookies", [])}
    except Exception:
        return {}


def proxy_request(platform: str, upstream_path: str, account_name: str, extra_qs: str = "") -> dict:
    """Forward a request through httpx with cookie injection; return (status, headers, body)."""
    if httpx is None:
        return {
            "status": 500,
            "headers": {"Content-Type": "text/html; charset=utf-8"},
            "body": "<p>代理功能需要安装 httpx 依赖</p>",
        }

    host = PROXY_HOSTS.get(platform)
    if not host:
        return {
            "status": 404,
            "headers": {"Content-Type": "text/html; charset=utf-8"},
            "body": f"<p>未知平台: {platform}</p>",
        }

    cookies = load_cookies_from_storage(platform, account_name)
    url = f"https://{host}{upstream_path}"
    if extra_qs:
        url = f"{url}?{extra_qs}"

    try:
        resp = httpx.get(
            url,
            cookies=cookies,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
            follow_redirects=True,
            timeout=30,
        )
        resp_headers = dict(resp.headers)
        # Strip headers that block iframe embedding
        for h in list(resp_headers.keys()):
            if h.lower() in STRIP_HEADERS:
                del resp_headers[h]

        return {
            "status": resp.status_code,
            "headers": resp_headers,
            "body": resp.text,
        }
    except Exception as exc:
        return {
            "status": 502,
            "headers": {"Content-Type": "text/html; charset=utf-8"},
            "body": f"<p>代理请求失败: {exc}</p>",
        }


def handle_notifications(handler: SimpleHTTPRequestHandler, payload: dict) -> None:
    """POST /api/notifications — scrape notification counts for given accounts."""
    accounts = payload.get("accounts", []) if isinstance(payload, dict) else []

    if not accounts:
        json_response(handler, 200, {"ok": True, "results": [], "message": "没有需要检查的账号"})
        return

    try:
        from notification_scraper import get_notifications_sync

        results = get_notifications_sync(accounts)
        json_response(handler, 200, {"ok": True, "results": results})
    except Exception as exc:
        json_response(handler, 500, {"ok": False, "error": str(exc)})


def handle_open_messages(handler: SimpleHTTPRequestHandler, payload: dict) -> None:
    """POST /api/open-messages — open messaging page in headed browser."""
    platform = str(payload.get("platform") or "").strip()
    account = str(payload.get("account") or "").strip()

    if not platform or not account:
        json_response(handler, 400, {"ok": False, "error": "缺少 platform 或 account"})
        return

    # Map shipinhao → tencent for cookie file lookup
    platform_key = "tencent" if platform == "shipinhao" else platform

    try:
        from notification_scraper import open_messaging_page_sync

        result = open_messaging_page_sync(platform_key, account)
        status = 200 if result.get("ok") else 400
        json_response(handler, status, result)
    except Exception as exc:
        json_response(handler, 500, {"ok": False, "error": str(exc)})


def handle_proxy(handler: SimpleHTTPRequestHandler) -> None:
    """GET /proxy/<platform>/<path> — reverse proxy with cookie injection."""
    parsed = urlparse(handler.path)
    # path looks like /proxy/douyin/creator-micro/message/notice
    parts = parsed.path.lstrip("/").split("/", 2)  # ['proxy', 'douyin', '...']
    if len(parts) < 2:
        json_response(handler, 400, {"ok": False, "error": "缺少平台参数"})
        return

    platform = parts[1]
    upstream_path = f"/{parts[2]}" if len(parts) > 2 else "/"

    qs = parse_qs(parsed.query)
    account_name = (qs.get("account", [""])[0]).strip()
    if not account_name:
        json_response(handler, 400, {"ok": False, "error": "缺少 account 参数"})
        return

    platform_key = "tencent" if platform == "shipinhao" else platform

    result = proxy_request(platform_key, upstream_path, account_name, parsed.query)

    # Send response
    body = result["body"]
    if isinstance(body, str):
        body_bytes = body.encode("utf-8")
    else:
        body_bytes = body

    handler.send_response(result["status"])
    for key, value in result["headers"].items():
        if key.lower() not in {"transfer-encoding", "content-length"}:
            handler.send_header(key, value)
    handler.send_header("Content-Length", str(len(body_bytes)))
    handler.end_headers()
    handler.wfile.write(body_bytes)


class Handler(SimpleHTTPRequestHandler):
    def translate_path(self, path: str) -> str:
        parsed = urlparse(path)
        clean = parsed.path.lstrip("/") or "index.html"
        return str((ROOT / clean).resolve())

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/status":
            json_response(self, 200, {
                "ok": True,
                "sauRoot": str(SAU_ROOT),
                "sauEntry": str(SAU_ENTRY),
                "python": python_executable(),
                "venvReady": SAU_VENV_PYTHON.exists(),
                "supportedPlatforms": sorted(SUPPORTED_PLATFORMS),
            })
            return

        if parsed.path.startswith("/proxy/"):
            handle_proxy(self)
            return

        return super().do_GET()

    def do_POST(self) -> None:
        try:
            payload = read_json(self)
            path = urlparse(self.path).path

            if path == "/api/check":
                platform = require_platform(payload)
                account = require_account(payload)
                result = run_sau([platform, "check", "--account", account], timeout=120)
                json_response(self, 200, result)
                return

            if path == "/api/login":
                platform = require_platform(payload)
                account = require_account(payload)
                mode = "--headed" if payload.get("headed", True) else "--headless"
                result = run_sau([platform, "login", "--account", account, mode], timeout=900)
                json_response(self, 200, result)
                return

            if path == "/api/upload-video":
                if payload.get("confirm") is not True:
                    raise ValueError("发布视频需要 confirm=true")
                platform = require_platform(payload)
                account = require_account(payload)
                file_path = existing_path(payload.get("file"), "视频文件")
                title = str(payload.get("title") or "").strip()
                if not title:
                    raise ValueError("缺少标题")
                args = [
                    platform,
                    "upload-video",
                    "--account",
                    account,
                    "--file",
                    file_path,
                    "--title",
                    title,
                    "--desc",
                    str(payload.get("desc") or ""),
                    "--headed",
                ]
                tags = clean_tags(payload.get("tags"))
                if tags:
                    args.extend(["--tags", tags])
                thumbnail = str(payload.get("thumbnail") or "").strip()
                if thumbnail:
                    args.extend(["--thumbnail", existing_path(thumbnail, "封面文件")])
                schedule = str(payload.get("schedule") or "").strip()
                if schedule:
                    args.extend(["--schedule", schedule])
                result = run_sau(args, timeout=1800)
                json_response(self, 200, result)
                return

            if path == "/api/notifications":
                handle_notifications(self, payload)
                return

            if path == "/api/open-messages":
                handle_open_messages(self, payload)
                return

            json_response(self, 404, {"ok": False, "stderr": "未知接口"})
        except Exception as exc:
            json_response(self, 400, {"ok": False, "stderr": str(exc)})


def main() -> None:
    os.chdir(str(ROOT))
    server = ThreadingHTTPServer(("127.0.0.1", DEFAULT_PORT), Handler)
    print(f"Matrix publisher panel: http://127.0.0.1:{DEFAULT_PORT}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
