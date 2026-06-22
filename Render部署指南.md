# Render 部署完整指南

## 📋 部署概述

本指南将帮助你将"皇帝的新装"游戏系统部署到 Render 云平台。

**部署方式**：直接从 GitHub 仓库部署  
**预计部署时间**：5-10分钟  
**成本**：免费（Render 免费层）

---

## 🔑 所需的所有信息汇总

### 基本信息
```
GitHub 仓库 URL: https://github.com/wuyuyang/emperor-game
分支: master
Render 地区: Singapore（新加坡）或 Oregon（美国）
```

### 部署信息
```
构建命令: npm install
启动命令: npm start
环境: Node.js
```

### 环境变量
```
NODE_ENV: production
PORT: 3000
```

### 域名信息
```
子域名: emperor-game-server（或任意名称）
完整 URL: https://emperor-game-server.onrender.com
```

---

## 第1步：访问 Render 官网

1. 打开 [Render 官网](https://render.com)
2. 点击右上角 **"Sign Up"** 或 **"Sign In"**
3. 使用 GitHub 账号登录（推荐）

---

## 第2步：连接 GitHub

### 授权 Render 访问你的 GitHub

1. 登录 Render 后，进入 **Dashboard**
2. 点击 **"New +"** 按钮
3. 选择 **"Web Service"**

4. 在 "Connect a repository" 部分：
   - 点击 **"Connect account"**
   - 选择 **GitHub**
   - 授权 Render 访问你的账号

5. 在列表中选择你的仓库：
   ```
   emperor-game
   ```

---

## 第3步：配置部署设置

### 填写以下信息

| 字段 | 填入值 | 说明 |
|------|--------|------|
| **Name** | `emperor-game-server` | 服务名称（显示在 Render 控制面板） |
| **Environment** | `Node` | 运行环境 |
| **Region** | `Singapore` 或 `Oregon` | 服务器地区（新加坡或美国） |
| **Branch** | `master` | 要部署的分支 |
| **Build Command** | `npm install` | 构建命令 |
| **Start Command** | `npm start` | 启动命令 |
| **Plan** | `Free` | 免费层 |

---

## 第4步：设置环境变量

在 "Environment" 部分，添加以下环境变量：

### 环境变量 1
```
Key:   NODE_ENV
Value: production
```

### 环境变量 2
```
Key:   PORT
Value: 3000
```

---

## 第5步：配置选项

### Auto-Deploy
- ✅ **启用自动部署**（推荐）
  - 选择：Enable auto-deploy from git
  - 这样 GitHub 有更新时会自动重新部署

### Pull Request Preview
- ✅ **启用 PR 预览**（可选）
  - 这样每个 PR 都会生成预览链接

---

## 第6步：部署

1. 检查所有配置是否正确
2. 点击 **"Create Web Service"**
3. Render 开始构建和部署

### 部署进度

在 Dashboard 中可以看到：
```
✅ Building...
✅ Uploading...
✅ Deploying...
✅ Live
```

完整部署通常需要 5-10 分钟。

---

## 完整配置检查清单

### 基本设置
- [ ] GitHub 仓库已连接
- [ ] 仓库选择正确：`emperor-game`
- [ ] 分支选择：`master`

### 环境设置
- [ ] Environment: `Node`
- [ ] Region: `Singapore` 或 `Oregon`
- [ ] Plan: `Free`

### 命令设置
- [ ] Build Command: `npm install`
- [ ] Start Command: `npm start`

### 环境变量
- [ ] NODE_ENV: `production`
- [ ] PORT: `3000`

### 其他设置
- [ ] Auto-deploy: 已启用
- [ ] Name: `emperor-game-server`

---

## 🎯 部署完成后

### 访问你的应用

部署完成后，你的应用将在以下地址可访问：

```
https://emperor-game-server.onrender.com
```

### 验证服务器运行

在浏览器访问：
```
https://emperor-game-server.onrender.com/health
```

应该看到：
```json
{
  "status": "ok",
  "activeRooms": 0,
  "timestamp": "2026-06-22T..."
}
```

✅ 服务器正常运行！

---

## 🎮 使用部署的服务器

### 修改客户端配置

将客户端中的服务器地址从：
```
http://localhost:3000
```

改为：
```
https://emperor-game-server.onrender.com
```

### 在 game-admin-server.html 中
找到这一行：
```html
<input type="text" id="serverUrl" class="form-group__input" value="http://localhost:3000" placeholder="http://localhost:3000">
```

改为：
```html
<input type="text" id="serverUrl" class="form-group__input" value="https://emperor-game-server.onrender.com" placeholder="https://emperor-game-server.onrender.com">
```

### 在 game-player-server.html 中
同样修改服务器地址为完整的 Render URL。

---

## 📊 Render 仪表板

部署后，你可以在 Render Dashboard 中：

- ✅ 查看实时日志
- ✅ 监控应用性能
- ✅ 管理环境变量
- ✅ 手动重新部署
- ✅ 查看部署历史

---

## 🔧 常见问题

### Q: 部署失败怎么办？

**检查日志**：
1. 进入 Render Dashboard
2. 点击你的服务
3. 进入 "Logs" 标签
4. 查看错误信息

常见错误：
- `npm not found` → Node.js 未正确安装
- `Build failed` → package.json 有问题
- `Port already in use` → 检查 PORT 环境变量

### Q: 应用在线但无法连接？

检查：
1. 防火墙规则
2. Socket.io 跨域设置
3. 环境变量是否正确

### Q: 想要自定义域名？

1. 购买域名（如 godaddy.com）
2. 在 Render 中添加自定义域名
3. 更新 DNS 记录

### Q: 免费层有限制吗？

是的：
- 15分钟无活动后进入休眠
- 共享 CPU 和内存
- 每月 750 小时免费

升级到付费计划可以移除限制。

### Q: 如何更新代码？

三种方式：

**方式 1：自动部署（推荐）**
```bash
git push origin master
# Render 自动检测并重新部署
```

**方式 2：手动部署**
1. 进入 Render Dashboard
2. 点击 "Manual Deploy"
3. 选择分支
4. 点击 "Deploy"

**方式 3：Render CLI**
```bash
npm install -g @render/render-cli
render deploy
```

---

## 📈 优化性能

### 启用缓存
在 render.yaml 中添加：
```yaml
buildCache: enabled
```

### 增加内存
```yaml
plan: standard
```

### 增加 Worker 数量
修改 server.js 中的并发连接限制：
```javascript
const server = http.createServer(app);
server.maxConnections = 1000;
```

---

## 🔒 安全建议

### 生产环境必做

1. **启用 HTTPS**（Render 自动）✅

2. **设置环境变量**（而不是硬编码）
   ```javascript
   const PORT = process.env.PORT || 3000;
   const NODE_ENV = process.env.NODE_ENV || 'development';
   ```

3. **限制 CORS**
   ```javascript
   const cors = require('cors');
   app.use(cors({
     origin: 'https://your-frontend-domain.com'
   }));
   ```

4. **添加速率限制**
   ```javascript
   const rateLimit = require('express-rate-limit');
   const limiter = rateLimit({
     windowMs: 15 * 60 * 1000,
     max: 100
   });
   app.use(limiter);
   ```

5. **添加日志记录**
   ```javascript
   console.log(`[${new Date().toISOString()}] Event: ${message}`);
   ```

---

## 📞 部署遇到问题？

### 获取帮助

1. **Render 文档**: https://render.com/docs
2. **Render 支持**: https://render.com/support
3. **Node.js 部署**: https://nodejs.org/en/docs/guides/nodejs-docker-webapp/

### 检查清单

- [ ] GitHub 仓库已连接
- [ ] render.yaml 配置正确
- [ ] package.json 存在并有效
- [ ] npm start 命令能本地运行
- [ ] 所有环境变量已设置
- [ ] 防火墙允许端口 3000

---

## 🎉 部署完成！

现在你的游戏服务器已在线：

```
🌐 https://emperor-game-server.onrender.com

📱 管理者端: 打开 game-admin-server.html，输入服务器地址
🎮 玩家端: 打开 game-player-server.html，输入服务器地址

✅ 开始游戏！
```

---

**祝部署顺利！🚀**
