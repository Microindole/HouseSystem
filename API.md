# API 接口文档

[![Flask](https://img.shields.io/badge/Flask-3.1.0-green.svg)](https://flask.palletsprojects.com/)
[![API](https://img.shields.io/badge/API-RESTful-blue.svg)](https://restfulapi.net/)

## 📋 目录

- [概述](#概述)
- [认证机制](#认证机制)
- [用户管理 API](#用户管理-api)
- [房源管理 API](#房源管理-api)
- [消息通讯 API](#消息通讯-api)
- [合同管理 API](#合同管理-api)
- [AI聊天 API](#ai聊天-api)
- [文件上传 API](#文件上传-api)
- [支付系统 API](#支付系统-api)
- [日志统计 API](#日志统计-api)
- [错误码说明](#错误码说明)
- [请求示例](#请求示例)

## 🔐 概述

智能房屋租赁系统提供完整的API接口，包含RESTful API和模板渲染两种方式。所有JSON API接口均采用JSON格式进行数据交换，页面渲染接口返回HTML页面。

### 基础信息

| 项目 | 值 |
|------|-----|
| **Base URL** | `http://localhost:5000` |
| **Content-Type** | `application/json` (API) / `text/html` (页面) |
| **字符编码** | `UTF-8` |
| **时间格式** | `ISO 8601` (例: `2025-06-04T12:00:00Z`) |

## 🔑 认证机制

系统使用基于Session的身份验证机制和JWT Token双重认证方式。

### 登录状态检查

大多数API需要在请求头中包含有效的Session信息或Token：

```http
# Session认证
GET /api/endpoint
Cookie: session=your_session_id

# JWT Token认证 (AI聊天等接口)
GET /ai_chat/endpoint
Authorization: Bearer your_jwt_token
```

### 权限级别

| 权限级别 | 用户类型 | 说明 |
|----------|----------|------|
| **0** | 管理员 | 系统最高权限，可访问所有功能 |
| **1** | 租客 | 可浏览房源、发起聊天、签署合同等 |
| **2** | 房东 | 可发布房源、管理租赁、处理维修等 |

## 👥 用户管理 API

### 用户登录页面
```http
GET /account/login
```
**类型**: 模板渲染
**返回**: HTML登录页面

### 用户登录 (JSON API)
```http
POST /account/login
Content-Type: application/json

{
  "username": "用户名",
  "password": "密码",
  "role": "tenant"  // tenant, landlord, admin
}
```

**响应示例**:
```json
{
  "success": true,
  "message": "登录成功",
  "user_type": 1,
  "redirect_url": "/house/house_list"
}
```

### 管理员登录
```http
POST /account/admin/login
Content-Type: application/json

{
  "username": "管理员用户名",
  "password": "管理员密码"
}
```

### 用户注册页面
```http
GET /account/register
```
**类型**: 模板渲染
**返回**: HTML注册页面

### 用户注册 (JSON API)
```http
POST /account/register
Content-Type: application/json

{
  "username": "用户名",
  "password": "密码",
  "confirm_password": "确认密码", 
  "email": "邮箱地址",
  "phone": "联系方式",
  "address": "完整地址",
  "user_type": "1"  // 1-租客, 2-房东
}
```

### 发送邮箱验证码 (JSON API)
```http
POST /account/send_email_code
Content-Type: application/json

{
  "email": "user@example.com"
}
```

### 发送密码重置验证码 (JSON API)
```http
POST /account/send_reset_code
Content-Type: application/json

{
  "email": "user@example.com"
}
```

### 验证重置验证码 (JSON API)
```http
POST /account/verify_reset_code
Content-Type: application/json

{
  "email": "user@example.com",
  "code": "123456"
}
```

### 用户个人资料页面
```http
GET /account/profile
```
**类型**: 模板渲染
**返回**: HTML个人资料页面

### 用户登出
```http
GET|POST /account/logout
```
**类型**: 重定向到登录页面

### 租客首页
```http
GET /account/tenant/home
```
**类型**: 模板渲染
**权限**: 租客 (user_type=1)

### 房东首页  
```http
GET /account/landlord/home
```
**类型**: 模板渲染
**权限**: 房东 (user_type=2)

### 管理员仪表板
```http
GET /account/admin/dashboard
```
**类型**: 模板渲染
**权限**: 管理员 (user_type=0)

### 手动更新出租率 (JSON API)
```http
GET /account/admin/manual_rent_rate_update
```
**权限**: 管理员

**响应示例**:
```json
{
  "message": "已更新今日出租率记录",
  "total_count": 100,
  "rented_count": 75,
  "rent_rate": 75.0
}
```

### 出租率历史数据 (JSON API)
```http
GET /account/api/rent_rate_history?start_date=2025-01-01&end_date=2025-06-04
```

**响应示例**:
```json
{
  "dates": ["2025-01-01", "2025-01-02"],
  "rates": [75.0, 76.5]
}
```

## 🏠 房源管理 API

### 房源列表页面
```http
GET /house
Query Parameters:
- page: 页码 (默认: 1)
- search: 搜索关键词
- region: 地区筛选
- rooms: 户型筛选
```
**类型**: 模板渲染
**返回**: HTML房源列表页面

### 房源详情页面
```http
GET /house/{house_id}
```
**类型**: 模板渲染
**返回**: HTML房源详情页面

### 发布房源页面
```http
GET /house/add
```
**类型**: 模板渲染
**权限**: 房东

### 发布房源 (表单提交)
```http
POST /house/add
Content-Type: multipart/form-data

{
  "house_name": "房源名称",
  "rooms": "2室1厅",
  "region": "朝阳区", 
  "addr": "详细地址",
  "price": "3500.00",
  "deposit": "3500.00",
  "situation": "装修情况",
  "highlight": "房源亮点"
}
```

### 编辑房源页面
```http
GET /house/edit/{house_id}
```
**类型**: 模板渲染
**权限**: 房东

### 编辑房源 (表单提交)
```http
POST /house/edit/{house_id}
```

### 删除房源 (JSON API)
```http
POST /house/delete/{house_id}
```
**权限**: 房东

### 批量房源操作 (JSON API)
```http
POST /house/batch/action
Content-Type: application/json

{
  "action": "delete",
  "house_ids": [1, 2, 3]
}
```

### 房源搜索 (JSON API)
```http
GET /house/api/search
Query Parameters:
- region: 地区
- rooms: 户型
- price_min: 最低价格
- price_max: 最高价格
- keyword: 关键词
```

**响应示例**:
```json
{
  "houses": [
    {
      "house_id": 1,
      "house_name": "精装两居室",
      "price": 3500.00,
      "region": "朝阳区",
      "rooms": "2室1厅",
      "image": "http://example.com/image.jpg",
      "status": 0
    }
  ],
  "total_count": 120
}
```

### 获取城市数据 (JSON API)
```http
GET /house/api/cities
```

### 导出房源数据 (JSON API)
```http
GET /house/api/export/csv
```
**权限**: 管理员

### 热门房源页面
```http
GET /house/popular
```
**类型**: 模板渲染

### 浏览历史页面
```http
GET /house/browse-history
```
**类型**: 模板渲染
**权限**: 租客

### 新闻列表页面
```http
GET /house/news
```
**类型**: 模板渲染

### 新闻详情页面
```http
GET /house/news/{news_id}
```
**类型**: 模板渲染

### 发布新闻页面
```http
GET /house/news/add
```
**类型**: 模板渲染
**权限**: 房东

### 发布新闻 (表单提交)
```http
POST /house/news/add
```

### 管理新闻页面
```http
GET /house/news/manage
```
**类型**: 模板渲染
**权限**: 房东

### 预约看房 (JSON API)
```http
POST /house/appointment
Content-Type: application/json

{
  "house_id": 1,
  "appointment_time": "2025-06-05T14:00:00"
}
```

### 维修申请 (JSON API)
```http
POST /house/repair_request
Content-Type: application/json

{
  "house_id": 1,
  "content": "维修问题描述"
}
```

## 💬 消息通讯 API

### 开始聊天/获取聊天频道
```http
GET /feedback/start_chat/{house_id}
```
**类型**: 重定向到聊天页面

### 聊天页面
```http
GET /feedback/chat/{channel_id}
```
**类型**: 模板渲染

### 发送消息 (JSON API)
```http
POST /feedback/send_message/{channel_id}
Content-Type: application/json

{
  "content": "消息内容"
}
```

**响应示例**:
```json
{
  "success": true,
  "message": {
    "message_id": 123,
    "channel_id": 1,
    "sender_username": "user123",
    "content": "消息内容",
    "timestamp": "2025-06-04T12:00:00Z"
  }
}
```

### 获取聊天数据 (JSON API)
```http
GET /feedback/get_chat_data/{channel_id}
```

**响应示例**:
```json
{
  "success": true,
  "channel": {
    "channel_id": 1,
    "tenant_username": "tenant123",
    "landlord_username": "landlord456",
    "house_id": 1,
    "house_status": 0
  },
  "house": {
    "house_id": 1,
    "house_name": "精装两居室",
    "price": 3500.00,
    "deposit": 3500.00
  },
  "messages": [
    {
      "message_id": 1,
      "sender_username": "tenant123",
      "content": "您好，我想了解一下这个房子",
      "timestamp": "2025-06-04T12:00:00Z",
      "is_read": true
    }
  ]
}
```

### 消息列表页面
```http
GET /feedback/messages
```
**类型**: 模板渲染

### 标记消息已读 (JSON API)
```http
POST /feedback/set_read/{channel_id}
```

### 投诉建议页面
```http
GET /feedback/complaint
```
**类型**: 模板渲染

### 提交投诉/反馈 (表单提交)
```http
POST /feedback/complaint
Content-Type: multipart/form-data

{
  "receiver": "被投诉人用户名",
  "content": "投诉内容",
  "type": "投诉"  // 或 "反馈"
}
```

### 管理投诉页面
```http
GET /feedback/manage_complaints
```
**类型**: 模板渲染
**权限**: 管理员或相关用户

### 更新投诉状态 (JSON API)
```http
POST /feedback/update_complaint_status/{complaint_id}
Content-Type: application/json

{
  "status": "已解决"  // 待处理/处理中/已解决/已关闭
}
```

### 我的投诉页面
```http
GET /feedback/my_complaints
```
**类型**: 模板渲染

### 根据房东获取房源 (JSON API)
```http
GET /feedback/get_houses_by_landlord?landlord={landlord_name}
```

### 发送合同 (JSON API)
```http
POST /feedback/send_contract
Content-Type: application/json

{
  "channel_id": 1,
  "start_date": "2025-06-01",
  "end_date": "2026-06-01",
  "total_amount": "3500.00",
  "receiver_username": "tenant123",
  "deposit_amount_numeric": "3500.00",
  "rent_payment_frequency": "月付",
  "lease_purpose_text": "居住",
  "other_agreements_text": "其他约定"
}
```

## 📋 合同管理 API

### 合同历史页面
```http
GET /contract/history?page=1
```
**类型**: 模板渲染

### 查看合同文档页面
```http
GET /contract/view_contract/{contract_id}
```
**类型**: 模板渲染

### 租客签署合同页面
```http
GET /contract/sign_contract_page/{contract_id}
```
**类型**: 模板渲染
**权限**: 租客

### 租客签署合同 (JSON API)
```http
POST /contract/sign_contract/{contract_id}
```
**权限**: 租客

**响应示例**:
```json
{
  "success": true,
  "message": "合同已成功签署！您现在可以进行支付。"
}
```

### 房东编辑合同页面
```http
GET /contract/upload_contract_page/{contract_id}
```
**类型**: 模板渲染
**权限**: 房东

### 取消合同 (JSON API)
```http
POST /contract/cancel/{contract_id}
```

### 房屋归还 (JSON API)
```http
POST /contract/return/{contract_id}
```

### 创建新合同
```http
GET /contract/create_new_contract?house_id={house_id}&tenant={tenant_name}
```
**类型**: 重定向
**权限**: 房东

### 取消签署页面
```http
GET /contract/cancel_signing/{contract_id}
```
**类型**: 模板渲染

### 访问统计 (JSON API)
```http
GET /contract/api/visit/stats
```

### 收入取消统计 (JSON API)
```http
GET /contract/api/income/cancel_stats
```

## 🤖 AI聊天 API

### AI聊天页面
```http
GET /ai_chat/
```
**类型**: 模板渲染
**认证**: 需要JWT Token

### 获取聊天历史 (JSON API)
```http
GET /ai_chat/get_history
```
**认证**: 需要JWT Token

**响应示例**:
```json
{
  "history": [
    {
      "role": "user",
      "content": "用户消息"
    },
    {
      "role": "assistant", 
      "content": "AI回复"
    }
  ]
}
```

### 发送AI消息 (流式响应)
```http
POST /ai_chat/send_message
Content-Type: application/json
Authorization: Bearer your_jwt_token

{
  "message": "用户输入的消息",
  "pageContent": "当前页面内容(可选)"
}
```

**响应类型**: Server-Sent Events (流式)
```
data: {"content": "AI回复片段", "done": false}

data: {"content": "", "done": true}
```

### 清除聊天历史 (JSON API)
```http
POST /ai_chat/clear_history
```
**认证**: 需要JWT Token

## 📁 文件上传 API

### 上传房源图片 (JSON API)
```http
POST /oss/upload_house_image/{house_id}
Content-Type: multipart/form-data

file: 图片文件
```

**响应示例**:
```json
{
  "success": true,
  "message": "图片上传成功",
  "image_url": "https://example.com/house_images/1/uuid.jpg"
}
```

## 💰 支付系统 API

### 商品列表页面
```http
GET /pay/good_list
```
**类型**: 模板渲染

### 发起合同支付 (重定向到支付宝)
```http
POST /pay/contract_pay
Content-Type: multipart/form-data

{
  "contract_id": "合同ID"
}
```
**权限**: 租客
**类型**: 重定向到支付宝支付页面

### 支付成功回调
```http
GET|POST /pay/alipay/success_result/
```
**类型**: 处理支付宝回调，重定向到用户首页

### 支付失败回调
```http
GET|POST /pay/alipay/fail_result/
```

## 📊 日志统计 API

### 获取系统日志 (JSON API)
```http
GET /logging/api/logs?limit=100&search=关键词
```

**响应示例**:
```json
{
  "logs": [
    {
      "username": "user123",
      "user_type": "租客",
      "message": "用户登录系统",
      "timestamp": "2025-06-04 12:00:00"
    }
  ]
}
```

## ❌ 错误码说明

| HTTP状态码 | 错误类型 | 说明 |
|------------|----------|------|
| **200** | 成功 | 请求成功处理 |
| **400** | 请求错误 | 参数错误或格式不正确 |
| **401** | 未授权 | 需要登录或Token无效 |
| **403** | 禁止访问 | 权限不足 |
| **404** | 未找到 | 资源不存在 |
| **500** | 服务器错误 | 内部服务器错误 |

### 标准错误响应格式

```json
{
  "success": false,
  "error": "错误描述",
  "code": "ERROR_CODE"
}
```

## 📝 请求示例

### 用户登录示例

```bash
# 获取登录页面
curl -X GET http://localhost:5000/account/login

# 提交登录请求
curl -X POST http://localhost:5000/account/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123",
    "role": "tenant"
  }'
```

### 房源搜索示例

```bash
# 搜索房源
curl -X GET "http://localhost:5000/house/api/search?region=朝阳区&rooms=2室1厅&price_max=5000"
```

### AI聊天示例

```bash
# 发送AI消息 (需要JWT Token)
curl -X POST http://localhost:5000/ai_chat/send_message \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_jwt_token" \
  -d '{
    "message": "请介绍一下这个房源的特点",
    "pageContent": "<html>页面内容...</html>"
  }'
```

### 发送消息示例

```bash
# 发送私信
curl -X POST http://localhost:5000/feedback/send_message/1 \
  -H "Content-Type: application/json" \
  -H "Cookie: session=your_session_id" \
  -d '{
    "content": "您好，我对这个房源很感兴趣"
  }'
```

## 🔗 相关文档

- [数据库设计文档](database.md) - 数据库表结构和关系设计
- [部署指南](README.md#部署指南) - 系统部署和配置说明
- [Flask官方文档](https://flask.palletsprojects.com/) - Flask框架文档

---

**注意**: 
- 所有需要身份验证的接口都需要有效的Session或JWT Token
- 文件上传接口需要使用 `multipart/form-data` 格式
- 流式响应接口(如AI聊天)使用Server-Sent Events格式
- 页面渲染接口返回HTML，JSON API接口返回JSON数据