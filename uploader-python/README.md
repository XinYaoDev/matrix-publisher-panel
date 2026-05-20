# Python Uploader

本目录保存了从旧项目根目录复制的 Python 上传相关代码。

## 文件来源

所有文件从旧版 `matrix-publisher-panel` 根目录复制而来，原始文件仍保留在项目根目录中，未被删除。

## 文件说明

| 文件 | 说明 |
|------|------|
| `server.py` | HTTP 服务器，提供 API 和前端静态文件服务 |
| `config.py` | 集中配置（路径、平台映射、网络设置） |
| `notification_scraper.py` | 平台通知抓取器 |
| `requirements.txt` | Python 依赖（patchright, httpx） |
| `start.bat` / `start.sh` | Windows / Linux 启动脚本 |

## 依赖的外部项目

- **social-auto-upload** (`SAU_ROOT`): 实际的平台上传能力由 `social-auto-upload` 项目提供，通过子进程调用 `sau_cli.py`
- 路径通过环境变量 `SAU_ROOT` 配置，默认为 `../social-auto-upload`

## 使用方式

```bash
# 安装依赖
pip install -r requirements.txt

# 启动（确保 SAU_ROOT 指向正确的 social-auto-upload 路径）
python server.py

# 或指定 social-auto-upload 路径
export SAU_ROOT=/path/to/social-auto-upload
python server.py
```

## 后续计划

1. 本目录中的代码保留原样，不重写上传逻辑
2. 未来 Java 后端将通过 `ProcessBuilder` 调用此 Python uploader
3. 原有 `index.html` 前端页面保留在 `legacy/` 和项目根目录
4. social-auto-upload 项目不在本仓库中，需单独克隆到工作区

## 重要说明

- **不要重写 social-auto-upload**
- **不要改变现有上传逻辑**
- 本目录为副本，根目录原文件仍然可用
