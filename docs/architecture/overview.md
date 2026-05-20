# Architecture

## 系统概览

Matrix Publisher 是一个多平台内容分发矩阵工具，目标是将视频、图文等内容发布到抖音、小红书、视频号等平台。

当前架构保留 Python 服务作为业务主线。前端工程仍保留 Web/Desktop 骨架，后续可以逐步接入 Python API。

## 技术栈

| 层 | 技术 | 说明 |
| --- | --- | --- |
| 当前服务 | Python `http.server` | `server.py` 提供页面、配置和发布相关 API |
| 当前页面 | HTML + 浏览器原生 JS | `index.html` 是现阶段可用界面 |
| 上传器 | Python | 调用或承载平台上传逻辑 |
| 桌面端骨架 | Electron + React + TypeScript | 后续可迁移业务页面 |
| Web 骨架 | Next.js App Router | 后续可作为管理后台 |
| 前端工程化 | pnpm workspace + Turborepo | 管理前端 workspace |

## 目录结构

```text
matrix-publisher-panel/
├── server.py              # Python HTTP 服务
├── index.html             # 当前可用单页界面
├── config.py              # Python 配置
├── notification_scraper.py
├── requirements.txt
├── uploader-python/       # Python 上传器副本
├── apps/
│   ├── desktop/           # Electron 骨架
│   └── web/               # Next.js 骨架
├── packages/              # 前端共享类型、组件和页面骨架
├── legacy/                # 旧项目说明
└── docs/                  # 文档
```

## 当前数据流

```text
Browser
  -> index.html
  -> Python server.py
  -> Python uploader / notification_scraper
  -> 平台上传或通知抓取能力
```

## 目标数据流

```text
Desktop/Web
  -> Python API
  -> Python uploader
  -> 抖音 / 小红书 / 视频号等平台
```

## 前端依赖关系

```text
apps/desktop -> packages/views -> packages/ui -> packages/core
apps/web     -> packages/views -> packages/ui -> packages/core
packages/config is used for shared frontend tooling config.
```

## 关键设计决策

1. **Python 优先**：实际业务和上传逻辑集中在 Python 侧。
2. **前端渐进迁移**：先保留可运行的 `index.html + server.py`，再逐步将页面迁移到 React/Next/Electron。
3. **轻量后端**：当前没有数据库强依赖。持久化方案应根据真实业务复杂度再决定。
4. **上传能力独立**：`uploader-python/` 可继续沉淀上传、登录态检测、通知抓取等平台能力。
