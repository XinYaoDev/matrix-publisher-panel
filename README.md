# Matrix Publisher

多平台内容分发矩阵工具 — 将视频/图文自动同步发布到抖音、小红书、视频号。

## 当前状态

本项目正在进行工程化重构。基础工程骨架已建立，业务功能正在逐步迁移中。

## 项目结构

```
├── apps/
│   ├── desktop/              # Electron 桌面端 (React + TypeScript)
│   └── web/                  # Next.js Web 管理后台
├── packages/
│   ├── core/                 # 共享类型、常量、API 封装
│   ├── ui/                   # 通用 UI 组件库
│   ├── views/                # 业务页面组件
│   └── config/               # 共享 tsconfig / eslint / tailwind 配置
├── backend-java/             # Java 21 + Spring Boot 3 后端
├── uploader-python/          # Python 上传器（保留原有逻辑）
├── legacy/                   # 旧项目代码状态说明
├── docs/
│   ├── architecture/         # 架构文档
│   └── migration/            # 迁移记录
├── docker-compose.yml        # PostgreSQL 本地开发环境
├── pnpm-workspace.yaml       # pnpm 工作区配置
├── turbo.json                # Turborepo 任务编排
└── .env.example              # 环境变量模板
```

## 快速开始

### 前置依赖

- Node.js >= 18
- pnpm >= 8
- Java 21 (用于后端开发)
- Docker (用于 PostgreSQL)
- Python 3 (用于旧上传器)

### 1. 安装 pnpm 依赖

```bash
pnpm install
```

### 2. 启动 PostgreSQL

```bash
docker compose up -d
```

### 3. 启动 Java 后端

```bash
cd backend-java
./mvnw spring-boot:run
```

> 注意：`mvnw` Maven Wrapper 尚未添加，后续由后端小队配置。

后端启动后访问 http://localhost:8080/api/health 验证。

### 4. 启动 Desktop 桌面端

```bash
pnpm run dev:desktop
```

### 5. 启动 Web 管理后台

```bash
pnpm run dev:web
```

启动后访问 http://localhost:3000。

### 6. 启动旧 Python 原型

旧 Python 原型仍可直接使用：

```bash
pip install -r requirements.txt
python server.py
```

启动后访问 http://127.0.0.1:8787。

## 可用命令

| 命令 | 说明 |
|------|------|
| `pnpm run dev:desktop` | 启动桌面端开发服务器 |
| `pnpm run dev:web` | 启动 Web 端开发服务器 |
| `pnpm run build` | 构建所有项目 |
| `pnpm run typecheck` | 类型检查 |
| `pnpm run lint` | 代码检查 |
| `pnpm run test` | 运行测试 |

> 部分命令当前为占位状态，需先安装依赖。详见 `docs/migration/foundation-handoff.md`。

## 旧项目文件位置

旧 Python 原型和前端代码保留在项目根目录，未被删除：

| 文件 | 说明 |
|------|------|
| `index.html` | 旧前端页面（单页应用） |
| `server.py` | Python HTTP 服务器 |
| `config.py` | Python 配置 |
| `notification_scraper.py` | 通知抓取器 |

这些文件已复制到 `uploader-python/` 目录。详见 `legacy/README.md`。

## 尚未迁移的业务功能

以下功能仍仅在旧 `index.html` + `server.py` 中可用，尚未迁移到新结构：

1. 账号管理（增删改查、平台绑定）
2. 账号分组管理
3. 作品库管理（视频/图文）
4. 发布队列生成
5. 发布命令构建和预览
6. 实际视频上传到平台
7. 平台登录态检查
8. 消息中心（通知抓取、iframe 代理）
9. 配置导入/导出

## 后续建议创建的 Issue

1. **安装 pnpm 依赖并修复编译错误** — 前端
2. **添加 Maven Wrapper 并验证 Java 后端启动** — 后端
3. **设计并创建数据库表结构** — 后端
4. **实现账号管理 CRUD REST API** — 后端
5. **实现作品管理 CRUD REST API** — 后端
6. **实现发布任务系统（创建、执行、状态追踪）** — 后端
7. **ProcessBuilder 封装 Python uploader 调用** — 后端
8. **完善 Electron 桌面端主进程功能** — 前端
9. **实现桌面端页面路由和导航** — 前端
10. **迁移账号管理页面到新前端** — 前端
11. **迁移作品管理页面到新前端** — 前端
12. **迁移发布队列页面到新前端** — 前端
13. **Web 管理后台路由和页面实现** — 前端
14. **CI/CD 流水线搭建** — 测试/集成
15. **端到端测试：发布流程验证** — 测试/集成

## 技术栈

| 层 | 技术 |
|---|------|
| 桌面端 | Electron + electron-vite + React 18 + TypeScript |
| Web 端 | Next.js 15 + React 18 + TypeScript |
| 后端 | Java 21 + Spring Boot 3 + Maven |
| 数据库 | PostgreSQL 16 |
| 上传器 | Python (social-auto-upload) |
| 工程化 | pnpm workspace + Turborepo |

## 文档

- [架构概述](docs/architecture/overview.md)
- [基础骨架 Handoff](docs/migration/foundation-handoff.md)
- [旧代码说明](legacy/README.md)
- [Python Uploader 说明](uploader-python/README.md)
