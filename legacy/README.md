# Legacy 旧代码

## 说明

本目录用于说明旧项目代码的位置和状态。

## 旧文件位置（项目根目录）

旧项目原型代码仍保留在项目根目录，**未被删除**：

| 文件 | 说明 |
|------|------|
| `index.html` | 旧前端页面（单页应用，包含 CSS + JS） |
| `server.py` | Python HTTP 服务器 |
| `config.py` | Python 配置文件 |
| `notification_scraper.py` | 通知抓取器 |
| `requirements.txt` | Python 依赖 |
| `start.bat` | Windows 启动脚本 |
| `start.sh` | Linux/Mac 启动脚本 |

## 启动旧项目的方式

```bash
# 安装依赖
pip install -r requirements.txt

# 启动（默认监听 127.0.0.1:8787）
python server.py
```

启动后访问 http://127.0.0.1:8787 即可使用旧的矩阵发布面板。

## 代码状态

- 旧代码功能完整可用
- 新工程结构建立后，旧代码不受影响
- 后续将由专门任务将业务逻辑迁移到新的 apps/desktop、apps/web 和 backend-java 中
- 迁移完成后，旧代码可逐步废弃

## 已复制到 uploader-python/

旧 Python 文件已复制到 `uploader-python/` 目录，作为未来 Java 后端通过 ProcessBuilder 调用的目标。
