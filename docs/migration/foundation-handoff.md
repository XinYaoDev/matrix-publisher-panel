# Foundation Handoff — 基础工程骨架建立

**日期**: 2026-05-20  
**执行者**: 架构师-Agent  
**任务**: [LEO-4](mention://issue/bab91761-4f74-4121-a02f-046c4d71dc35) — 建立 matrix-publisher 项目的基础工程骨架

---

## 一、本次建立了哪些结构

### 根目录工程化

| 文件 | 状态 |
|------|------|
| `pnpm-workspace.yaml` | 已创建 |
| `turbo.json` | 已创建 |
| `package.json` | 已创建，包含 dev:desktop, dev:web, build, typecheck, lint, test |
| `docker-compose.yml` | 已创建，PostgreSQL 16 |
| `.env.example` | 已创建 |
| `.gitignore` | 已更新，覆盖 Node/Java/Python |

### apps/

| 目录 | 状态 | 技术栈 |
|------|------|--------|
| `apps/desktop/` | 最小骨架 | Electron + electron-vite + React + TypeScript |
| `apps/web/` | 最小骨架 | Next.js App Router |

### packages/

| 目录 | 状态 | 内容 |
|------|------|------|
| `packages/core/` | 基础类型已定义 | Platform, PublishStatus, ErrorType, ApiResponse 等 |
| `packages/ui/` | 占位组件已创建 | Button, Card, Badge |
| `packages/views/` | 占位页面已创建 | 6 个业务页面占位组件 |
| `packages/config/` | 共享配置已创建 | tsconfig base, eslint base, tailwind base |

### backend-java/

| 项目 | 状态 |
|------|------|
| Spring Boot 3 + Java 21 + Maven | 已创建 |
| `/api/health` 接口 | 已实现 |
| `MatrixPublisherApplication.java` | 已创建 |
| `application.yml` (环境变量驱动) | 已创建 |
| 包结构 (controller/application/domain/infrastructure/common) | 已预留，含 .gitkeep |

### uploader-python/

| 文件 | 说明 |
|------|------|
| server.py, config.py, notification_scraper.py | 从根目录复制而来 |
| requirements.txt, start.bat, start.sh | 已复制 |
| README.md | 说明了文件来源和使用方式 |

### legacy/

| 内容 | 说明 |
|------|------|
| README.md | 说明旧项目文件位置和启动方式 |

### docs/

| 文件 | 说明 |
|------|------|
| docs/architecture/overview.md | 架构概述 |
| docs/migration/foundation-handoff.md | 本文件 |

---

## 二、哪些命令可用

| 命令 | 状态 | 说明 |
|------|------|------|
| `pnpm run dev:desktop` | 占位 | 需要先安装 pnpm 和依赖 |
| `pnpm run dev:web` | 占位 | 需要先安装 pnpm 和依赖 |
| `pnpm run build` | 占位 | 需要先安装依赖 |
| `pnpm run typecheck` | 占位 | 需要先安装依赖 |
| `pnpm run lint` | 占位 | 需要先安装依赖 |
| `pnpm run test` | 占位 | 输出 TODO 消息并 exit 0 |
| `docker compose up` | 可用 | 启动 PostgreSQL（需安装 Docker） |
| `python server.py` | 可用 | 启动旧 Python 后端（保留原方式） |
| `cd backend-java && mvnw spring-boot:run` | 占位 | 需要 Maven Wrapper 和 Java 21 |

---

## 三、哪些只是占位

1. **所有 `pnpm run` 命令**：依赖未安装，tsconfig/eslint 基础配置存在但未与具体工具集成
2. **apps/desktop**：Electron 主进程/预加载/Renderer 骨架可编译但未安装依赖，无法实际启动
3. **apps/web**：Next.js 骨架可编译但未安装依赖，无法实际启动
4. **packages/views 的所有页面**：仅输出占位文字，无业务逻辑
5. **packages/core 的 schemas/api/utils**：目录和空导出已预留，无实际实现
6. **packages/ui 的 hooks/lib**：空目录，无实现
7. **backend-java**：缺少 Maven Wrapper (`mvnw`)，pom.xml 正确但未安装 JDK 21，无法编译运行
8. **测试命令**：全部输出 TODO 消息，无实际测试

---

## 四、后续前端小队应该接什么任务

1. **安装 pnpm 依赖并验证骨架可构建**
   - 在根目录运行 `pnpm install`
   - 修复所有 TypeScript 编译错误
   - 确保 `pnpm run build` 至少能完成类型检查

2. **完善 apps/desktop 桌面端**
   - 接入 react-router 实现页面路由
   - 将 packages/views 的占位页面接入路由
   - 完善 Electron 主进程（窗口管理、菜单、托盘）
   - 完善 preload 安全桥接（IPC 通道定义）

3. **完善 apps/web Web 管理后台**
   - 接入 Next.js App Router 页面路由
   - 将 packages/views 的占位页面接入对应路由
   - 实现基础布局和导航

4. **完善 packages/ui 组件库**
   - 实现更多通用组件（Table, Modal, Form, Input 等）
   - 建立组件文档

5. **迁移旧前端业务逻辑**
   - 从旧 `index.html` 中提取业务逻辑到 React 组件
   - 账号管理、分组管理、作品管理、发布队列等功能

---

## 五、后续后端小队应该接什么任务

1. **配置 Java 开发环境**
   - 添加 Maven Wrapper (`mvnw`)
   - 确保 `mvnw spring-boot:run` 能成功启动

2. **设计数据库表结构**
   - 设计 accounts, groups, works, publish_tasks 等核心表
   - 创建 Flyway/Liquibase 迁移脚本

3. **实现核心 REST API**
   - CRUD 接口：账号/分组/作品/发布任务
   - 发布任务执行接口（调用 Python uploader）
   - 统一错误处理和 API 响应格式

4. **实现 ProcessBuilder 调用 Python uploader**
   - 封装对 `sau_cli.py` 的子进程调用
   - 处理超时、错误输出、命令构建
   - 异步任务执行

---

## 六、后续测试集成小队应该验证什么

1. **工程骨架验证**
   - `pnpm install` 在所有平台（Win/Mac/Linux）成功
   - `pnpm run typecheck` 通过
   - `pnpm run test` 退出码为 0（即使是 TODO）

2. **Docker 验证**
   - `docker compose up` 成功启动 PostgreSQL
   - 能用 `psql` 连接并操作数据库

3. **旧代码验证**
   - `python server.py` 仍可正常启动
   - 旧 `index.html` 页面仍可在浏览器使用

4. **CI/CD 骨架**
   - 为新项目设置基础的 GitHub Actions / 其他 CI
   - 包含 install → typecheck → lint → test 流水线

---

## 七、已知风险

1. **依赖未安装验证**：所有 TypeScript/Node 相关代码未经实际编译运行，可能存在拼写错误或类型不匹配
2. **electron-vite 版本兼容性**：electron-vite 2.x 与 electron 33.x 的搭配需要在安装依赖后实际验证
3. **Java 后端缺少 Maven Wrapper**：当前只有 pom.xml，没有 `mvnw` 脚本，无法直接 `mvnw spring-boot:run`
4. **旧项目 social-auto-upload 路径依赖**：`config.py` 中 `SAU_ROOT` 默认为 `../social-auto-upload`，新项目结构下可能需要调整
5. **packages 包名使用了 `@matrix-publisher/*`**：需要确保 pnpm 工作区能正确解析 workspace 依赖
6. **eslint 基础配置过于简单**：只包含 `eslint:recommended`，未配置 TypeScript 规则
7. **旧 `.gitignore` 被覆盖**：已将原有的 `.claude/` 和 Python 规则保留，新增加了 Node/Java 规则
