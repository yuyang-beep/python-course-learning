# 部署指南 - Emperor's New Clothes Settlement System

## 📋 前置条件

- GitHub 账号
- Supabase 账号 (https://supabase.com)
- Render 账号 (https://render.com)

---

## 🔧 Step 1: Supabase 设置

### 1.1 创建项目

1. 访问 [Supabase](https://supabase.com)
2. 点击 "New Project"
3. 填写项目信息：
   - **Project Name**: `emperor-game`
   - **Database Password**: 设置强密码
   - **Region**: 选择离你最近的地区（如 `ap-northeast-1` for 东京）
   - **Plan**: Free 计划足够开发

### 1.2 获取 API 凭证

部署后，进入 Project Settings → API，复制：
- `Project URL` → 设为 `SUPABASE_URL`
- `anon public` key → 设为 `VITE_SUPABASE_ANON_KEY`
- `service_role` secret key → 设为 `SUPABASE_SERVICE_ROLE_KEY`

### 1.3 创建数据库表

1. 在 Supabase 中打开 SQL Editor
2. 复制 `backend/docs/database-schema.sql` 中的所有 SQL
3. 执行 SQL 创建表和函数

---

## 🐙 Step 2: GitHub 设置

### 2.1 创建仓库

```bash
# 在你的 emperor-game 目录中
cd D:/Vibe_Coding/emperor-game

# 添加远程仓库 (替换 YOUR_USERNAME 为你的 GitHub 用户名)
git remote add origin https://github.com/YOUR_USERNAME/emperor-game.git
git branch -M main
git push -u origin main
```

### 2.2 配置 GitHub Secrets (可选)

如果后续要使用 GitHub Actions，在 GitHub 仓库的 Settings → Secrets and variables → Actions 中添加：

```
SUPABASE_URL=<你的Supabase URL>
SUPABASE_SERVICE_ROLE_KEY=<你的Service Role Key>
VITE_SUPABASE_URL=<你的Supabase URL>
VITE_SUPABASE_ANON_KEY=<你的Anon Key>
```

---

## 🚀 Step 3: Render 部署

### 3.1 连接 GitHub

1. 访问 [Render Dashboard](https://dashboard.render.com)
2. 点击 "New +" → "Web Service"
3. 选择 "Connect a repository" → 授权 GitHub
4. 搜索并选择 `emperor-game` 仓库

### 3.2 配置后端服务

**Service 信息**:
- **Name**: `emperor-game-api`
- **Environment**: `Node`
- **Build Command**: `cd backend && npm install && npm run build`
- **Start Command**: `cd backend && npm run start`
- **Plan**: Free

**环境变量**:
```
NODE_ENV=production
PORT=3000
SUPABASE_URL=<你的Supabase URL>
SUPABASE_SERVICE_ROLE_KEY=<你的Service Role Key>
```

点击 "Deploy"

### 3.3 配置前端服务

1. 点击 "New +" → "Static Site"
2. 选择同一个 GitHub 仓库

**Service 信息**:
- **Name**: `emperor-game-web`
- **Build Command**: `cd frontend && npm install && npm run build`
- **Publish directory**: `frontend/dist`
- **Plan**: Free

**环境变量**:
```
VITE_SUPABASE_URL=<你的Supabase URL>
VITE_SUPABASE_ANON_KEY=<你的Anon Key>
```

点击 "Deploy"

---

## 🔗 Step 4: 连接后端和前端

### 4.1 获取后端 URL

部署后，Render 会为后端生成一个 URL，例如：
```
https://emperor-game-api.onrender.com
```

### 4.2 更新前端代理配置

编辑 `frontend/vite.config.ts`：

```typescript
server: {
  proxy: {
    '/api': {
      target: 'https://emperor-game-api.onrender.com',
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/api/, '/api'),
    },
  },
},
```

### 4.3 Render 前端重定向规则

在 Render 前端服务的 Redirects/Rewrites 中添加：

```
Source: /api/*
Destination: https://emperor-game-api.onrender.com/api/*
```

---

## ✅ 部署检查清单

- [ ] Supabase 项目创建且 API 凭证已获取
- [ ] 数据库 Schema 已执行
- [ ] GitHub 仓库已创建并推送代码
- [ ] Render 后端服务已部署
- [ ] Render 前端服务已部署
- [ ] 环境变量已配置
- [ ] 后端和前端已连接
- [ ] 访问前端 URL，检查是否正常加载

---

## 🧪 测试部署

### 测试 API 健康检查

```bash
curl https://emperor-game-api.onrender.com/health
```

预期响应：
```json
{
  "status": "ok",
  "timestamp": "2026-06-23T00:00:00.000Z"
}
```

### 访问前端

打开浏览器访问前端 URL（Render 会为前端生成一个类似 `https://emperor-game-web.onrender.com` 的地址）

---

## 📝 常见问题

### Q: 前端无法连接到后端
**A**: 检查：
1. 后端服务是否正在运行
2. CORS 配置是否正确
3. API 代理规则是否配置正确

### Q: 数据库连接失败
**A**: 检查：
1. `SUPABASE_URL` 和 `SUPABASE_SERVICE_ROLE_KEY` 是否正确
2. Supabase 项目是否已激活
3. 防火墙/VPN 是否阻止连接

### Q: 环境变量显示为 undefined
**A**: 
1. Render 中重新部署服务以应用新的环境变量
2. 检查拼写是否正确
3. 等待 1-2 分钟，变量生效可能有延迟

---

## 🔄 后续更新

每当推送新代码到 GitHub 时，Render 会自动触发部署：

```bash
# 开发
git add .
git commit -m "fix: ..."
git push origin main

# Render 会自动部署
```

---

## 📱 生产环境建议

在正式上线前，考虑：

1. **配置自定义域名**
   - Render 支持添加自定义域名
   - 可配置 SSL 证书

2. **增加实例类型**
   - Free 计划有自动休眠，考虑升级到 Standard

3. **数据库备份**
   - Supabase 自动备份，但建议定期手动导出

4. **监控和日志**
   - 在 Render 中配置日志聚合
   - 设置错误告警

5. **认证和授权**
   - 实现用户认证机制
   - 将 RLS 策略从 public 改为基于用户

---

**部署成功！🎉**

你现在有了一个可访问的游戏结算系统，管理员和玩家可以通过浏览器访问。
