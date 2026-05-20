# Architecture

## 系统概述

Matrix Publisher 是一个多平台内容分发矩阵工具，核心能力是将一个视频/图文自动同步发布到小红书、抖音、视频号。

## 架构决策

### 技术栈

| 层 | 技术 | 说明 |
|---|------|------|
| 桌面端 | Electron + electron-vite + React + TypeScript | 桌面管理面板 |
| Web 端 | Next.js App Router | Web 管理后台 |
| 后端 | Java 21 + Spring Boot 3 | REST API 服务 |
| 数据库 | PostgreSQL 16 | 持久化存储 |
| 上传器 | Python (social-auto-upload) | 实际平台上传能力，通过 ProcessBuilder 调用 |
| 工程化 | pnpm workspace + Turborepo | 单体仓库管理 |

### 目录结构

```
matrix-publisher-panel/
├── apps/
│   ├── desktop/          # Electron 桌面端
│   └── web/              # Next.js Web 管理后台
├── packages/
│   ├── core/             # 共享类型、常量、API 封装
│   ├── ui/               # 通用 UI 组件
│   ├── views/            # 业务页面组件
│   └── config/           # 共享 tsconfig/eslint/tailwind 配置
├── backend-java/         # Spring Boot 3 后端
├── uploader-python/      # Python 上传器（保留原逻辑）
├── legacy/               # 旧项目说明
├── docs/
│   ├── architecture/     # 架构文档
│   └── migration/        # 迁移记录
├── docker-compose.yml    # PostgreSQL 本地开发环境
├── pnpm-workspace.yaml   # pnpm 工作区配置
├── turbo.json            # Turborepo 配置
└── package.json          # 根 package.json
```

### 数据流

```
前端 (Desktop/Web) → REST API → Java Backend → PostgreSQL
                                         ↓
                                  ProcessBuilder
                                         ↓
                                  Python Uploader
                                         ↓
                               social-auto-upload
                                         ↓
                          抖音 / 小红书 / 视频号 API
```

### 包依赖关系

```
apps/desktop → packages/views → packages/ui → packages/core
apps/web    → packages/views → packages/ui → packages/core
             packages/config (dev)
```

## 关键设计决策

1. **Python uploader 保留原样**：实际的平台上传能力由 `social-auto-upload` 提供。Java 后端通过 `ProcessBuilder` 调用 Python 脚本。这样避免重写已稳定的上传逻辑。

2. **前后端分离**：桌面端和 Web 端共享 `packages/` 中的类型和组件，通过 REST API 与 Java 后端通信。

3. **环境变量配置**：所有敏感信息（数据库密码、端口等）通过环境变量注入，不在代码中硬编码。
