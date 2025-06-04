# 智能房屋租赁系统 (House System)

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.0-green.svg)](https://flask.palletsprojects.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)](https://www.mysql.com/)
[![Redis](https://img.shields.io/badge/Redis-6.0+-red.svg)](https://redis.io/)
[![License](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](LICENSE)

## 🏠 项目介绍

基于Flask框架开发的智能房屋租赁系统，为房东、租客和管理员提供完整的房屋租赁解决方案。系统集成了AI智能助手、实时消息通讯、电子合同签订、维修管理等现代化功能，旨在简化传统租房流程，提升用户体验。

## 📋 目录

- [软件架构](#-软件架构)
- [技术栈](#️-技术栈)
- [核心功能](#-核心功能)
- [环境依赖](#-环境依赖)
- [安装教程](#-安装教程)
- [使用说明](#-使用说明)
- [项目结构](#-项目结构)
- [数据库设计](#-数据库设计)
- [API文档](#-api文档)
- [部署指南](#-部署指南)
- [贡献指南](#-贡献指南)

## 📚 API文档

系统提供完整的API接口，支持两种调用方式：

### 📄 接口类型

| 类型 | 说明 | 示例 |
|------|------|------|
| **模板渲染** | 返回HTML页面，用于Web界面展示 | `/house/` - 房源列表页面 |
| **JSON API** | 返回JSON数据，用于AJAX调用和第三方集成 | `/house/api/search` - 房源搜索API |

### 🔐 主要接口模块

| 模块 | 页面接口 | JSON API | 描述 |
|------|----------|----------|------|
| **👥 用户管理** | `/account/login`, `/account/register` | `/account/send_email_code` | 用户注册、登录、个人资料 |
| **🏠 房源管理** | `/house/`, `/house/{id}` | `/house/api/search`, `/house/api/cities` | 房源浏览、搜索、管理 |
| **💬 消息通讯** | `/feedback/messages`, `/feedback/chat/{id}` | `/feedback/send_message/{id}` | 实时聊天、投诉反馈 |
| **📋 合同管理** | `/contract/history`, `/contract/view_contract/{id}` | `/contract/cancel/{id}` | 合同签署、管理 |
| **🤖 AI助手** | `/ai_chat/` | `/ai_chat/send_message` | 智能问答、聊天历史 |
| **📁 文件管理** | - | `/oss/upload_house_image/{id}` | 图片上传、文件管理 |
| **💰 支付系统** | `/pay/good_list` | `/pay/contract_pay` | 支付宝集成、交易处理 |
| **📊 统计分析** | - | `/logging/api/logs`, `/account/api/rent_rate_history` | 系统日志、数据统计 |

### 🔑 认证方式

```bash
# Session认证 (大部分接口)
Cookie: session=your_session_id

# JWT Token认证 (AI聊天接口)
Authorization: Bearer your_jwt_token
```

### 📖 接口调用示例

```bash
# 房源搜索API
GET /house/api/search?region=朝阳区&rooms=2室1厅

# 发送消息API  
POST /feedback/send_message/1
Content-Type: application/json
{"content": "您好，我对这个房源很感兴趣"}

# AI聊天API (流式响应)
POST /ai_chat/send_message
Authorization: Bearer token
{"message": "请介绍一下租房注意事项"}
```

> 📖 **完整API文档**: [API接口文档](API.md) - 包含所有接口的详细说明、参数、响应格式和调用示例

### 🛠️ 开发工具

- **API调试**: 推荐使用 [Postman](https://www.postman.com/) 或 [curl](https://curl.se/) 进行接口测试
- **WebSocket测试**: 可使用浏览器开发者工具测试实时消息功能
- **文档生成**: 接口文档支持导出为OpenAPI格式

## 🏗️ 软件架构

<div align="center">

### 系统分层架构

| 层级 | 技术栈 | 描述 |
|------|--------|------|
| **🎨 前端展示层** | `HTML5` `CSS3` `JavaScript` `Bootstrap` | 用户界面和交互体验 |
| **⚡ 业务逻辑层** | `Flask Blueprint` `Service Layer` | 业务规则和流程控制 |
| **🗃️ 数据访问层** | `SQLAlchemy ORM` `MySQL` `Redis` | 数据持久化和缓存 |
| **🌐 外部服务层** | `阿里云OSS` `百度地图API` `DeepSeek AI` | 第三方服务集成 |

</div>

### 🔧 核心模块关系

```mermaid
graph TD
    A[用户界面] --> B[Flask路由]
    B --> C[业务服务层]
    C --> D[数据模型]
    D --> E[MySQL数据库]
    C --> F[Redis缓存]
    C --> G[外部服务]
    G --> H[阿里云OSS]
    G --> I[百度地图API]
    G --> J[DeepSeek AI]
```

## 🛠️ 技术栈

<details>
<summary><strong>🔧 后端框架</strong></summary>

| 技术 | 版本 | 描述 |
|------|------|------|
| **[Flask](https://flask.palletsprojects.com/)** | 3.1.0 | 轻量级Web框架 |
| **[SQLAlchemy](https://www.sqlalchemy.org/)** | 2.0.40 | Python SQL工具包和ORM |
| **[Flask-Migrate](https://flask-migrate.readthedocs.io/)** | 4.1.0 | 数据库迁移工具 |
| **[Flask-Mail](https://pythonhosted.org/Flask-Mail/)** | 0.10.0 | 邮件发送服务 |
| **[Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)** | 4.7.1 | JWT身份验证 |
| **[APScheduler](https://apscheduler.readthedocs.io/)** | 3.11.0 | 任务调度器 |

</details>

<details>
<summary><strong>🗄️ 数据库</strong></summary>

| 技术 | 版本 | 描述 |
|------|------|------|
| **[MySQL](https://www.mysql.com/)** | 8.0+ | 关系型数据库 |
| **[Redis](https://redis.io/)** | 6.2.0 | 内存数据库，用于缓存和会话 |
| **[PyMySQL](https://github.com/PyMySQL/PyMySQL)** | 1.1.1 | MySQL数据库连接器 |

</details>

<details>
<summary><strong>🎨 前端技术</strong></summary>

| 技术 | 版本 | 描述 |
|------|------|------|
| **HTML5 + CSS3 + JavaScript** | - | 基础前端技术栈 |
| **[Bootstrap](https://getbootstrap.com/)** | 5.x | 响应式UI框架 |
| **[Jinja2](https://jinja.palletsprojects.com/)** | 3.1.6 | 模板引擎 |

</details>

<details>
<summary><strong>🌐 外部服务</strong></summary>

| 服务 | 版本 | 描述 |
|------|------|------|
| **[阿里云OSS](https://www.aliyun.com/product/oss)** | alibabacloud-oss-v2 1.1.1 | 对象存储服务 |
| **[百度地图API](https://lbsyun.baidu.com/)** | - | 地图和位置服务 |
| **[DeepSeek AI](https://www.deepseek.com/)** | openai 1.82.0 | AI智能对话服务 |
| **[支付宝SDK](https://opendocs.alipay.com/)** | python-alipay-sdk 3.3.0 | 在线支付服务 |

</details>

<details>
<summary><strong>🔒 安全与认证</strong></summary>

| 技术 | 版本 | 描述 |
|------|------|------|
| **[cryptography](https://cryptography.io/)** | 44.0.2 | 加密库 |
| **[argon2-cffi](https://argon2-cffi.readthedocs.io/)** | 23.1.0 | 密码哈希 |
| **[Flask-WTF](https://flask-wtf.readthedocs.io/)** | 1.2.2 | 表单验证和CSRF保护 |

</details>

<details>
<summary><strong>📡 通信与网络</strong></summary>

| 技术 | 版本 | 描述 |
|------|------|------|
| **[python-socketio](https://python-socketio.readthedocs.io/)** | 5.13.0 | WebSocket实时通信 |
| **[requests](https://docs.python-requests.org/)** | 2.32.3 | HTTP请求库 |
| **[httpx](https://www.python-httpx.org/)** | 0.28.1 | 异步HTTP客户端 |

</details>

## 🔧 环境依赖

### 📦 Python包依赖

系统使用了**58个**精心选择的Python包，涵盖Web框架、数据库、安全认证、外部服务等各个方面：

| 依赖类型 | 包数量 | 主要包 |
|----------|--------|--------|
| **🌐 Web框架** | 8个 | Flask生态系统完整支持 |
| **🗄️ 数据库** | 6个 | MySQL + Redis + SQLAlchemy |
| **🔒 安全认证** | 7个 | JWT + Argon2 + 加密算法 |
| **☁️ 外部服务** | 5个 | 阿里云OSS + AI + 支付宝 |
| **🛠️ 开发工具** | 12个 | 任务调度 + 实时通信 + 邮件 |
| **📚 支持库** | 20个 | 工具库和底层依赖 |

### ⚙️ 系统要求

| 环境 | 最低版本 | 推荐版本 | 说明 |
|------|----------|----------|------|
| **Python** | 3.11+ | 3.13+ | 使用最新特性和性能优化 |
| **MySQL** | 8.0+ | 8.0.35+ | 支持JSON字段和新特性 |
| **Redis** | 6.0+ | 7.0+ | 用于缓存和会话存储 |
| **内存** | 2GB+ | 4GB+ | 依赖包较多，需要足够内存 |

### 🔍 依赖亮点

- **现代化技术栈**: 使用Flask 3.x + SQLAlchemy 2.x最新版本
- **安全优先**: Argon2密码哈希 + 多层加密保护
- **云原生**: 阿里云OSS + AI服务无缝集成  
- **实时通信**: WebSocket + SocketIO支持
- **异步支持**: 现代异步HTTP客户端
- **支付集成**: 支付宝SDK完整支持

> 📖 **详细依赖文档**: [项目依赖说明](requirements.md) - 包含所有58个依赖包的详细说明、版本信息、安装指南和故障排除

## 🚀 安装教程

### 1. 环境要求

**基础环境**:
```bash
Python 3.13+  # 推荐使用最新版本
MySQL 8.0+    # 关系型数据库
Redis 6.0+    # 缓存和会话存储
```

**系统要求**:
- 内存: 4GB+ (推荐8GB)
- 磁盘: 10GB+ 可用空间
- 网络: 稳定的互联网连接

### 2. 克隆项目
```bash
git clone https://gitee.com/central-south-university_25/house-system.git
cd house-system
```

### 3. 创建虚拟环境
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 4. 安装依赖

**快速安装（推荐）**:
```bash
# 升级pip到最新版本
python -m pip install --upgrade pip

# 安装所有依赖（共58个包）
pip install -r requirements.txt
```

**分类安装**:
```bash
# 核心Web框架
pip install Flask==3.1.0 Flask-SQLAlchemy==3.1.1 Flask-Migrate==4.1.0

# 数据库驱动
pip install PyMySQL==1.1.1 redis==6.2.0

# 安全认证
pip install Flask-JWT-Extended==4.7.1 argon2-cffi==23.1.0 cryptography==44.0.2

# 外部服务
pip install alibabacloud-oss-v2==1.1.1 openai==1.82.0 python-alipay-sdk==3.3.0

# 实时通信
pip install python-socketio==5.13.0
```

**镜像源安装**（解决网络问题）:
```bash
# 使用清华大学镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 5. 配置数据库
```bash
# 创建MySQL数据库
mysql -u root -p
CREATE DATABASE house_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 导入数据库结构
mysql -u root -p house_system < flask_house.sql
```

### 6. 配置环境变量
创建 `.env` 文件：
```bash
# 数据库配置
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/house_system

# Redis配置
REDIS_URL=redis://localhost:6379/0

# 邮件配置
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-password

# 阿里云OSS配置
ALIBABA_CLOUD_ACCESS_KEY_ID=your-access-key
ALIBABA_CLOUD_ACCESS_KEY_SECRET=your-secret-key
OSS_BUCKET_NAME=your-bucket-name
OSS_ENDPOINT=your-endpoint

# AI服务配置
DEEPSEEK_API_KEY=your-deepseek-api-key

# 百度地图API
BAIDU_MAP_API_KEY=your-baidu-map-key
```

### 7. 初始化数据库
```bash
flask db upgrade
```

### 8. 启动服务
```bash
python app.py
# 访问 http://localhost:5000
```

### 🔧 故障排除

**依赖安装失败**:
```bash
# 安装编译工具
# Windows: 安装 Visual Studio Build Tools
# Ubuntu/Debian: sudo apt-get install build-essential python3-dev
# CentOS/RHEL: sudo yum install gcc python3-devel

# 清理pip缓存
pip cache purge

# 逐个安装失败的包
pip install package_name --no-cache-dir
```

**版本冲突问题**:
```bash
# 检查依赖冲突
pip check

# 使用pip-tools管理依赖
pip install pip-tools
pip-compile requirements.in
```

> 💡 **提示**: 详细的安装问题解决方案请参考 [依赖说明文档](requirements.md#故障排除)

## 📖 使用说明

### 房东用户
1. 注册账号并选择"房东"角色
2. 完善个人信息和联系方式
3. 发布房源信息（包括图片、价格、位置等）
4. 管理预约看房申请
5. 处理租客维修申请
6. 在线签订电子合同
7. 发布房屋相关新闻

### 租客用户  
1. 注册账号并选择"租客"角色
2. 浏览和搜索心仪房源
3. 预约看房时间
4. 与房东在线沟通
5. 签订电子租赁合同
6. 提交维修申请
7. 使用AI助手咨询问题

### 管理员用户
1. 管理系统用户和权限
2. 监控系统运行状态
3. 处理用户投诉建议
4. 查看系统统计报表
5. 维护系统数据

## 📂 项目结构

<details>
<summary><strong>📁 点击展开完整目录结构</strong></summary>

```
house-system/
│
├── 📄 应用核心文件
│   ├── app.py                 # Flask应用入口
│   ├── config.py             # 配置文件
│   ├── models.py             # 数据模型定义
│   ├── decorators.py         # 装饰器函数
│   └── exts.py               # 扩展初始化
│
├── 📁 业务模块 (blueprints/)
│   ├── account.py            # 👤 用户账户管理
│   ├── house.py              # 🏠 房源管理
│   ├── feedback.py           # 💬 消息反馈
│   └── ai_chat_bp.py         # 🤖 AI聊天助手
│
├── 📁 服务层 (service/)
│   ├── house_service.py      # 🏠 房源业务逻辑
│   ├── oss_service.py        # ☁️ 对象存储服务
│   └── logging.py            # 📝 日志服务
│
├── 📁 静态资源 (static/)
│   ├── css/                  # 🎨 样式文件
│   │   ├── style.css
│   │   └── bootstrap.min.css
│   ├── js/                   # ⚡ JavaScript文件
│   │   ├── common/
│   │   ├── house/
│   │   └── feedback/
│   └── images/               # 🖼️ 图片资源
│
├── 📁 模板文件 (templates/)
│   ├── base.html             # 📄 基础模板
│   ├── index.html            # 🏠 首页模板
│   ├── house/                # 🏠 房源相关页面
│   │   ├── house_list.html
│   │   ├── house_detail.html
│   │   └── publish_house.html
│   ├── account/              # 👤 用户相关页面
│   │   ├── login.html
│   │   ├── register.html
│   │   └── profile.html
│   └── feedback/             # 💬 消息相关页面
│       ├── message.html
│       └── complaint.html
│
├── 📁 数据库 (migrations/)   # 🗃️ 数据库迁移文件
├── 📄 flask_house.sql        # 🗄️ 数据库初始化文件
├── 📄 requirements.txt       # 📋 依赖包列表
└── 📄 README.md              # 📖 项目说明文档
```

</details>

### 🔧 核心文件说明

| 文件/目录 | 功能描述 |
|-----------|----------|
| `app.py` | Flask应用主入口，包含应用初始化和路由注册 |
| `models.py` | 数据库模型定义，包含所有表结构 |
| `config.py` | 应用配置文件，包含数据库、Redis等配置 |
| `blueprints/` | Flask蓝图模块，按功能模块划分 |
| `service/` | 业务逻辑层，处理复杂的业务逻辑 |
| `static/` | 静态资源目录，包含CSS、JS、图片等 |
| `templates/` | Jinja2模板文件，渲染HTML页面 |

## 🗄️ 数据库设计

系统采用MySQL 8.0作为主数据库，使用SQLAlchemy ORM进行数据建模。数据库设计遵循第三范式，包含20张核心表，涵盖用户管理、房源管理、消息通讯、租赁管理等模块。

### 📊 核心表结构概览

| 模块 | 表数量 | 主要表 |
|------|--------|--------|
| **👥 用户管理** | 4张表 | `login`, `landlord`, `tenant`, `user_email` |
| **🏠 房源管理** | 4张表 | `house_info`, `house_status`, `house_listing_audit`, `comment` |
| **💬 消息通讯** | 3张表 | `private_channel`, `message`, `complaint` |
| **📋 租赁管理** | 4张表 | `appointment`, `rental_contract`, `contract_info`, `repair_request` |
| **📰 内容管理** | 2张表 | `news`, `comment` |
| **📊 统计分析** | 3张表 | `daily_rent_rate`, `visit_stats`, `operation_log` |

### 🔗 关键关系设计

- **用户角色扩展**: `login` → `landlord/tenant` 一对一扩展
- **房源状态管理**: `house_info` ↔ `house_status` 一对一关联
- **私信频道**: 基于 `(tenant, landlord, house)` 三元组建立唯一频道
- **合同体系**: `rental_contract` ↔ `contract_info` 核心合同与详细条款分离

> 📖 **详细文档**: [数据库设计文档](database.md) - 包含完整的表结构、关系图谱、索引策略和性能优化指南

## 🌐 部署指南

### 🐳 Docker部署
```bash
# 构建镜像
docker build -t house-system .

# 运行容器
docker run -p 5000:5000 -d house-system
```

### 🌐 Nginx配置
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /static {
        alias /path/to/house-system/static;
    }
}
```

### 🚀 生产环境配置
- 使用 **[Gunicorn](https://gunicorn.org/)** 作为WSGI服务器
- 配置 **[Supervisor](http://supervisord.org/)** 进程管理
- 设置 **[Nginx](https://nginx.org/)** 反向代理
- 配置 SSL/TLS 证书

## 🧪 测试

### 运行测试
```bash
python -m pytest tests/
```

### 运行覆盖率测试
```bash
pytest --cov=app tests/
```

## 🔧 核心技术特性

| 特性 | 描述 |
|------|------|
| **🎨 响应式设计** | 支持PC端和移动端访问 |
| **⚡ 实时通讯** | WebSocket实现实时消息推送 |
| **☁️ 文件上传** | 集成阿里云OSS对象存储 |
| **🗺️ 地图服务** | 百度地图API显示房源位置 |
| **🤖 AI集成** | DeepSeek AI提供智能问答 |
| **🔒 安全防护** | SQL注入防护、XSS防护、CSRF保护 |
| **⚡ 性能优化** | Redis缓存、数据库查询优化 |
| **📊 日志监控** | 完整的操作日志和错误追踪 |

## 📊 系统要求

| 指标 | 要求 |
|------|------|
| **⏱️ 响应时间** | ≤ 2秒 |
| **👥 并发支持** | 1000+ 用户同时在线 |
| **🌐 浏览器兼容** | Chrome、Firefox、Safari、Edge |
| **📱 设备支持** | PC、手机、平板 |
| **🔐 数据安全** | SSL/TLS加密传输 |

## 🤝 贡献指南

### 📝 代码贡献流程
1. **Fork** 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 **Pull Request**

### 📋 开发规范
- 遵循 **[PEP 8](https://www.python.org/dev/peps/pep-0008/)** 代码规范
- 编写单元测试
- 更新文档
- 提交信息使用英文

### 🐛 问题反馈
如发现bug或有功能建议，请通过以下方式反馈：
- **[Gitee Issues](https://gitee.com/central-south-university_25/house-system/issues)**
- **[项目讨论区](https://gitee.com/central-south-university_25/house-system)**

## 📄 许可证

本项目采用 **[GNU Affero General Public License v3.0](LICENSE)** 许可证

[![AGPL License](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

### ⚠️ 重要说明
- 本项目为 **开源软件**，允许自由使用、修改和分发
- 如果您在网络服务中使用本软件的修改版本，必须向用户提供源代码
- 商业使用时需要遵循 AGPL-3.0 许可证条款

## 📞 联系方式

<div align="center">

| 联系方式 | 链接 |
|----------|------|
| 📧 **邮箱** | contact@house-system.com |
| 🌐 **项目主页** | [Gitee Repository](https://gitee.com/central-south-university_25/house-system) |
| 🐛 **问题反馈** | [Issues](https://gitee.com/central-south-university_25/house-system/issues) |
| 💬 **技术交流** | [Gitee 讨论区](https://gitee.com/central-south-university_25/house-system) |

</div>

## 🙏 致谢

感谢以下开源项目和服务提供商的支持：

<div align="center">

| 类别 | 技术 | 描述 |
|------|------|------|
| **🌐 Web框架** | [Flask](https://flask.palletsprojects.com/) | 灵活的Python Web框架 |
| **🗃️ ORM** | [SQLAlchemy](https://www.sqlalchemy.org/) | Python SQL工具包 |
| **🗄️ 数据库** | [MySQL](https://www.mysql.com/) | 可靠的关系型数据库 |
| **⚡ 缓存** | [Redis](https://redis.io/) | 高性能内存数据库 |
| **🎨 前端框架** | [Bootstrap](https://getbootstrap.com/) | 现代响应式UI框架 |
| **🗺️ 地图服务** | [百度地图API](https://lbsyun.baidu.com/) | 专业的地图服务 |
| **☁️ 云存储** | [阿里云OSS](https://www.aliyun.com/product/oss) | 安全可靠的对象存储 |
| **🤖 AI服务** | [DeepSeek](https://www.deepseek.com/) | 智能对话AI平台 |

</div>

---

<div align="center">

**💡 提示**: 本项目持续更新中，欢迎关注项目动态。如有任何问题或建议，请随时联系我们！

**⚠️ 注意**: 本项目仅用于学习和演示目的，如需商业使用请确保遵循 AGPL-3.0 许可证条款。

## ⭐ 项目支持

**如果这个项目对您有帮助，请在 [Gitee](https://gitee.com/central-south-university_25/house-system) 给我们点个 ⭐！**

[![Gitee Stars](https://gitee.com/central-south-university_25/house-system/badge/star.svg?theme=dark)](https://gitee.com/central-south-university_25/house-system/stargazers)
[![Gitee Forks](https://gitee.com/central-south-university_25/house-system/badge/fork.svg?theme=dark)](https://gitee.com/central-south-university_25/house-system/members)

### 📈 项目统计

<div align="center">

![Gitee Stats](https://gitee.com/central-south-university_25/house-system/widgets/widget_card.svg?colors=4183c4,ffffff,ffffff,e3e9ed,666666,9b9b9b)

</div>

</div>