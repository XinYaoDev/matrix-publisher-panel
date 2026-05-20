# Matrix Publisher

多平台内容分发矩阵工具。当前项目保留 Python 原型服务和上传器逻辑，同时保留 Web/Desktop 前端工程骨架用于后续迁移。

## 当前状态

- 可运行主链路：`server.py` + `index.html`
- Python 上传器副本：`uploader-python/`
- 前端工程骨架：`apps/web`、`apps/desktop`、`packages/*`
- 后端方向：Python 服务

## 项目结构

```text
matrix-publisher-panel/
├── server.py                  # Python HTTP 服务
├── index.html                 # 旧单页前端
├── config.py                  # Python 配置
├── notification_scraper.py    # 通知抓取器
├── requirements.txt           # Python 依赖
├── uploader-python/           # Python 上传器副本
├── apps/
│   ├── desktop/               # Electron 桌面端骨架
│   └── web/                   # Next.js Web 管理后台骨架
├── packages/                  # 前端共享包
├── legacy/                    # 旧项目说明
└── docs/                      # 架构和迁移文档
```

## 快速开始

### Python 原型

```bash
pip install -r requirements.txt
python server.py
```

启动后访问：

```text
http://127.0.0.1:8787
```

### Web 骨架

```bash
pnpm install
pnpm run dev:web
```

启动后访问：

```text
http://127.0.0.1:3000
```

### Desktop 骨架

```bash
pnpm install
pnpm run dev:desktop
```

## 可用命令

| 命令 | 说明 |
| --- | --- |
| `python server.py` | 启动当前可用的 Python 原型服务 |
| `pnpm run dev:web` | 启动 Web 骨架 |
| `pnpm run dev:desktop` | 启动 Desktop 骨架 |
| `pnpm run build` | 构建前端 workspace |
| `pnpm run typecheck` | 前端类型检查 |
| `pnpm run lint` | 前端 lint |
| `pnpm run test` | 测试占位命令 |

## Python 代码

根目录 Python 文件仍是当前业务主入口：

| 文件 | 说明 |
| --- | --- |
| `server.py` | Python HTTP 服务，提供页面和 API |
| `index.html` | 当前可用的单页界面 |
| `config.py` | 路径、端口、平台和上传器配置 |
| `notification_scraper.py` | 平台通知抓取逻辑 |
| `requirements.txt` | Python 依赖 |

`uploader-python/` 保留了同一批 Python 文件的副本，方便后续将上传能力独立成模块。

## 后续方向

1. 继续以 Python 服务作为后端主线。
2. 将 `index.html` 中的业务界面逐步迁移到 `apps/web` 或 `apps/desktop`。
3. 前端通过 HTTP/API 调用 Python 服务。
4. 如需持久化，优先在 Python 服务内选择轻量方案，再根据实际复杂度决定是否引入数据库。

## 文档

- [架构概览](docs/architecture/overview.md)
- [基础骨架 Handoff](docs/migration/foundation-handoff.md)
- [旧代码说明](legacy/README.md)
- [Python Uploader 说明](uploader-python/README.md)
