# 快速开始指南

## 本地开发环境设置

### 前置条件

- Node.js 18+ (下载: https://nodejs.org/)
- Supabase 账号 (可选，开发时也可以使用模拟数据)
- Git

### 第 1 步：安装依赖

```bash
# 后端依赖
cd backend
npm install

# 前端依赖
cd ../frontend
npm install
```

### 第 2 步：配置环境变量

```bash
# 在项目根目录
cp .env.example .env.local
```

编辑 `.env.local` (可选，如果要连接 Supabase)：

```env
# Supabase Configuration
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key

SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
PORT=3000
NODE_ENV=development
```

### 第 3 步：启动开发服务器

**终端 1 - 后端**:
```bash
cd backend
npm run dev
# 服务器运行在 http://localhost:3000
```

**终端 2 - 前端**:
```bash
cd frontend
npm run dev
# 开发服务器运行在 http://localhost:5173
```

### 第 4 步：打开浏览器

访问 http://localhost:5173

---

## 项目结构导览

```
emperor-game/
├── backend/
│  ├── src/
│  │  ├── index.ts              # Express 服务器入口
│  │  ├── routes/               # API 路由（待实现）
│  │  ├── services/
│  │  │  ├── supabaseClient.ts  # Supabase 连接
│  │  │  ├── gameService.ts     # 游戏逻辑
│  │  │  └── scoringService.ts  # 计分逻辑
│  │  └── types/
│  │     └── index.ts           # TypeScript 类型定义
│  └── package.json
│
├── frontend/
│  ├── src/
│  │  ├── App.tsx               # 主应用组件
│  │  ├── main.tsx              # 入口
│  │  ├── index.css             # HUMAN 3.0 样式
│  │  ├── pages/                # 页面组件（待实现）
│  │  ├── components/           # 可复用组件（待实现）
│  │  ├── stores/
│  │  │  └── gameStore.ts       # Zustand 状态管理
│  │  └── types/
│  │     └── index.ts           # TypeScript 类型定义
│  └── package.json
│
├── docs/
│  ├── deployment.md            # 部署指南
│  ├── quickstart.md            # 本指南
│  └── api.md                   # API 文档（待写）
│
└── README.md
```

---

## 核心文件说明

### 后端核心逻辑

#### `backend/src/types/index.ts`
定义所有 TypeScript 类型，包括：
- `Game`, `Player`, `Round`, `Vote` 数据实体
- `ScoringReason` 计分原因
- API 请求/响应类型

#### `backend/src/services/scoringService.ts`
**核心计分逻辑**：
```typescript
// 质疑成功 → 质疑者 +3，附和者 -1（再 -3 如果孩子质疑）
// 质疑失败 → 质疑者 -1，附和者 +3
// 沉默者：+0
```

#### `backend/src/services/gameService.ts`
游戏流程管理：
- 创建游戏
- 分配角色
- 推进轮次
- 计算最终排名

#### `backend/src/services/supabaseClient.ts`
数据库操作封装（`db` 对象）

### 前端核心文件

#### `frontend/src/types/index.ts`
前端类型定义

#### `frontend/src/stores/gameStore.ts`
Zustand 全局状态管理：
- `game_id`: 当前游戏 ID
- `player_id`: 当前玩家 ID
- `current_view`: 当前界面 ('join' | 'waiting' | 'voting' | 'result' | 'settlement')
- `game_session`: 游戏状态
- `settlement_data`: 结算页面数据

#### `frontend/src/App.tsx`
主应用，根据 `current_view` 显示不同页面

#### `frontend/src/index.css`
HUMAN 3.0 风格系统：
- 黑/灰/冷白色彩
- 等宽字体 (Courier New)
- 数据面板组件
- 按钮和表格样式
- 动画系统 (scoreFlow, pulseData)

---

## 开发流程

### 添加新的 API 端点

1. **定义类型** (`backend/src/types/index.ts`)
   ```typescript
   export interface CreateGameRequest {
     player_names: string[];
   }
   ```

2. **实现服务** (`backend/src/services/gameService.ts`)
   ```typescript
   async createGame(playerNames: string[]): Promise<Game> {
     // 实现逻辑
   }
   ```

3. **添加路由** (在 `backend/src/routes/` 中创建文件)
   ```typescript
   router.post('/games', async (req, res) => {
     const game = await gameService.createGame(req.body.player_names);
     res.json(game);
   });
   ```

4. **在 `backend/src/index.ts` 中注册路由**

### 添加新的前端页面

1. **在 `frontend/src/pages/` 创建组件**
   ```typescript
   export function MyPageView() {
     return <div>...</div>;
   }
   ```

2. **在 `frontend/src/App.tsx` 中使用**
   ```typescript
   {view === 'my_view' && <MyPageView />}
   ```

3. **使用 Zustand store 管理状态**
   ```typescript
   const { set_current_view } = useGameStore();
   set_current_view('my_view');
   ```

---

## HUMAN 3.0 UI 组件

前端已预定义了一套 HUMAN 3.0 风格组件，可在 CSS 中直接使用：

### 数据面板
```html
<div class="data-panel">
  <div class="data-panel-title">Round 1 Results</div>
  <!-- 内容 -->
</div>
```

### 数据表格
```html
<table class="data-table">
  <thead>
    <tr>
      <th>Player</th>
      <th>Score</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Player 1</td>
      <td class="data-value positive">+3</td>
    </tr>
  </tbody>
</table>
```

### 按钮
```html
<button class="btn btn-primary">Challenge</button>
<button class="btn btn-success">Agree</button>
<button class="btn btn-danger">Action</button>
```

### 时间轴
```html
<div class="timeline">
  <div class="timeline-item success">Round 1 - Success</div>
  <div class="timeline-item danger">Round 2 - Failed</div>
</div>
```

### 颜色值
- `human-black`: #0f0f0f
- `human-dark`: #1a1a1a
- `human-gray`: #333333
- `human-text`: #e0e0e0
- `human-blue`: #00d4ff
- `human-green`: #00ff88
- `human-red`: #ff4444

---

## 调试技巧

### 检查后端日志
```bash
# 后端服务会打印请求和错误
cd backend && npm run dev
```

### 检查前端日志
打开浏览器的开发者工具 (F12)，查看 Console 标签

### 使用 Zustand Devtools
添加到 `frontend/src/stores/gameStore.ts`：
```typescript
import { devtools } from 'zustand/middleware';

export const useGameStore = create<UIStore>(
  devtools((set) => ({
    // store logic
  }))
);
```

然后在浏览器中安装 Redux DevTools 扩展

---

## 常见问题

**Q: 访问 http://localhost:5173 显示空白？**
A: 检查前端终端是否有错误，可能是 Node 版本过低或依赖未安装

**Q: 后端无法连接到 Supabase？**
A: 
1. 检查 `.env.local` 中的 Supabase URL 和 Key
2. 确保网络连接正常
3. 检查 Supabase 项目是否已激活

**Q: TypeScript 报错？**
A: 运行 `npm install` 确保所有类型包已安装

---

## 下一步

- 查看 `docs/api.md` 了解 API 设计
- 查看 `docs/deployment.md` 了解如何部署到 Render
- 查看 `backend/docs/database-schema.sql` 了解数据库结构

---

**祝开发愉快！** 🚀
