# 皇帝的新装 V1.1 - 结算系统（HUMAN 3.0）

一个多人博弈游戏的完整结算与分析系统。

## 项目概述

这不是一个普通的游戏结果页面，而是一个**"人类行为在不确定条件下信任机制的结构化重建系统"**。

属于 HUMAN 3.0 世界观：冷静、系统化、哲学化、去情绪化叙事。

## 技术栈

- **Frontend**: React 18 + TypeScript + Vite + TailwindCSS
- **Backend**: Node.js + Express + TypeScript
- **Database**: Supabase (PostgreSQL)
- **Deploy**: Render + GitHub

## 项目结构

```
emperor-game/
├── backend/          # Node.js + Express 后端
│  └── src/
│     ├── routes/     # API 路由
│     ├── services/   # 业务逻辑
│     └── types/      # TypeScript 类型定义
├── frontend/         # React 前端
│  └── src/
│     ├── pages/      # 页面组件
│     ├── components/ # 可复用组件
│     ├── stores/     # Zustand 状态管理
│     └── types/      # TypeScript 类型定义
└── .github/
   └── workflows/     # CI/CD 配置
```

## 快速开始

### 前置条件

- Node.js 18+
- Supabase 账号
- GitHub 账号

### 安装依赖

```bash
# 后端
cd backend && npm install

# 前端
cd frontend && npm install
```

### 环境配置

```bash
cp .env.example .env.local
# 编辑 .env.local，添加 Supabase 凭证
```

### 启动开发服务器

```bash
# 终端 1 - 后端
cd backend && npm run dev

# 终端 2 - 前端
cd frontend && npm run dev
```

## 核心特性

- ✅ 管理端游戏控制
- ✅ 玩家实时投票
- ✅ 5轮行为轨迹回放
- ✅ 分数矩阵可视化
- ✅ 角色真相揭示
- ✅ HUMAN 3.0 风格 UI

## API 文档

详见 `backend/docs/api.md`

## 游戏规则

详见 `docs/rules.md`

## 部署

详见 `docs/deployment.md`

## 开发进度

- [x] Phase 1: 项目初始化
- [ ] Phase 2: 后端 API
- [ ] Phase 3: 前端界面
- [ ] Phase 4: 结算页面
- [ ] Phase 5: 部署上线

---

**作者**: Claude Code  
**许可证**: MIT
