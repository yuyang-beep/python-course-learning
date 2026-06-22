# Render 部署 - 快速参考卡

## 📋 需要填写的所有信息

### 1️⃣ 连接 GitHub
```
GitHub 账号: wuyuyang
仓库: emperor-game
分支: master
```

---

### 2️⃣ 基本设置

| 字段 | 值 |
|------|-----|
| **Service Name** | `emperor-game-server` |
| **Environment** | `Node` |
| **Region** | `Singapore` 或 `Oregon` |
| **Plan** | `Free` |

---

### 3️⃣ 构建和启动命令

```
构建命令 (Build Command):
npm install

启动命令 (Start Command):
npm start
```

---

### 4️⃣ 环境变量

**变量 1:**
```
Key:   NODE_ENV
Value: production
```

**变量 2:**
```
Key:   PORT
Value: 3000
```

---

### 5️⃣ 部署设置

- ✅ 启用自动部署 (Auto-deploy from git)
- ✅ 启用 PR 预览 (Pull Request previews)

---

## 🎯 部署步骤速查

| 步骤 | 操作 |
|------|------|
| 1 | 访问 https://render.com |
| 2 | 使用 GitHub 账号登录 |
| 3 | 点击 "New +" → "Web Service" |
| 4 | 连接 GitHub 账号 |
| 5 | 选择 emperor-game 仓库 |
| 6 | 填写上述所有信息 |
| 7 | 点击 "Create Web Service" |
| 8 | 等待部署完成（5-10分钟） |

---

## ✅ 配置确认清单

在点击部署前，确保以下全部正确：

### 仓库设置
- [ ] 选择的分支是 `master`
- [ ] GitHub 仓库正确连接

### 环境设置
- [ ] Environment: `Node`
- [ ] Region: 已选择（Singapore 或 Oregon）
- [ ] Plan: `Free`

### 命令设置
- [ ] Build Command: `npm install`
- [ ] Start Command: `npm start`

### 环境变量
- [ ] NODE_ENV = `production`
- [ ] PORT = `3000`

### 其他
- [ ] Service Name: `emperor-game-server`
- [ ] Auto-deploy: 已启用

---

## 🌐 部署完成后

### 访问地址
```
https://emperor-game-server.onrender.com
```

### 验证服务器
访问健康检查：
```
https://emperor-game-server.onrender.com/health
```

应返回：
```json
{"status": "ok", "activeRooms": 0}
```

### 更新客户端

在 game-admin-server.html 和 game-player-server.html 中，将服务器地址改为：
```
https://emperor-game-server.onrender.com
```

---

## 📊 实时监控

部署后可在 Render Dashboard 中：
- 查看实时日志
- 监控 CPU/内存使用
- 手动重新部署
- 管理环境变量

---

## ⚠️ 常见问题速解

| 问题 | 解决方案 |
|------|---------|
| 部署失败 | 查看日志 (Logs tab) |
| 应用休眠 | 免费层 15分钟无活动会休眠 |
| 无法连接 | 检查防火墙和 Socket.io 设置 |
| 需要自定义域名 | 进入 Settings → Custom Domain |
| 需要更新代码 | Push 到 master（自动部署） |

---

## 🚀 快速总结

1. **GitHub**: https://github.com/wuyuyang/emperor-game ✅
2. **分支**: master ✅
3. **构建**: `npm install` ✅
4. **启动**: `npm start` ✅
5. **环境变量**: NODE_ENV=production, PORT=3000 ✅
6. **点击**: Create Web Service ✅
7. **等待**: 5-10分钟 ⏳
8. **访问**: https://emperor-game-server.onrender.com 🌐

---

**祝部署成功！**
