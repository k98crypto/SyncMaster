🚀 SyncMaster 

一个极简、安全、支持加密的自托管一键备份工具。专为独立开发者和服务器管理员设计。

✨ 核心特性
- **📦 一键打包**：自动将目标目录打包为 `.tar.gz`。
- **🔒 本地端到端加密**：使用 AES-256 (Fernet) 加密，网盘服务商也无法读取你的数据。
- **🐳 Docker 一键部署**：无需配置复杂的 Python 环境。
- **📢 Webhook 通知**：备份成功/失败第一时间推送到你的设备。

🛠 快速开始

1. 准备配置文件
克隆仓库后，修改 `src/config.yaml`，填入你需要备份的路径。

2. 使用 Docker 运行 (推荐)

```bash
docker build -t syncmaster .
# 将本地目录挂载到容器中进行备份
docker run -v /your/local/data:/app/data_to_backup \
           -v /your/local/backups:/app/backup_archives \
           syncmaster