# 开发路线图

## Phase 1 ✅ 完成
- [x] 项目结构初始化
- [x] 后端 (Express + TypeScript) 基础设置
- [x] 前端 (React + Vite + TailwindCSS) 基础设置
- [x] Supabase 数据库 Schema 设计
- [x] 核心类型定义
- [x] 核心服务实现 (ScoringService, GameService, SupabaseClient)
- [x] HUMAN 3.0 UI 样式系统
- [x] 部署文档

---

## Phase 2 🚧 后端 API 实现 (预计 2-3 天)

### 2.1 游戏管理 API
- [ ] `POST /api/games` - 创建游戏
  - 输入: 8 个玩家名字
  - 输出: 游戏 ID
- [ ] `GET /api/games/:id` - 获取游戏信息
  - 输出: 游戏状态、玩家列表、当前轮次
- [ ] `PATCH /api/games/:id/start` - 开始游戏
  - 将游戏状态从 'waiting' 改为 'in_progress'
- [ ] `PATCH /api/games/:id/finish` - 结束游戏
  - 计算最终排名
  - 返回结算数据

### 2.2 玩家管理 API
- [ ] `POST /api/games/:id/players` - 添加玩家到游戏
  - 输入: 玩家名字
  - 输出: 玩家 ID
- [ ] `PATCH /api/games/:id/players/:playerId/role` - 分配角色
  - 输入: 角色 (tailor, minister, citizen, child)
  - 输出: 更新后的玩家信息

### 2.3 轮次管理 API
- [ ] `POST /api/games/:id/rounds` - 创建新一轮
  - 输入: base_threshold, minister1_adjustment, minister2_adjustment
  - 输出: 轮次 ID
- [ ] `GET /api/games/:id/rounds/:roundNumber` - 获取轮次信息
- [ ] `POST /api/games/:id/rounds/:roundId/votes` - 提交投票
  - 输入: playerId, choice (challenge/agree/silent)
  - 输出: 投票确认
- [ ] `POST /api/games/:id/rounds/:roundId/finalize` - 提交轮次
  - 计算质疑是否成功
  - 计分并更新玩家总分
  - 标记孩子是否触发质疑

### 2.4 结算数据 API
- [ ] `GET /api/games/:id/settlement` - 获取结算页面数据
  - 输出: SettlementData (包含所有 5 轮的详细信息)
- [ ] `GET /api/games/:id/summary` - 获取游戏摘要
  - 输出: 最终排名、总体统计

### 2.5 错误处理和验证
- [ ] 输入验证 (参数类型、范围)
- [ ] 错误响应标准化
  - { success: false, error: "Error message", code: "ERROR_CODE" }
- [ ] 日志系统

---

## Phase 3 🎯 前端页面实现 (预计 2-3 天)

### 3.1 页面结构
```
/game/:gameId/
├── JoinGame          # 输入 gameId 加入
├── WaitingRoom       # 等待游戏开始或分配身份
├── VotingUI          # 投票界面
│  ├── NormalView     # 普通玩家: 质疑/附和/沉默
│  ├── ChildView      # 孩子: 首轮只有质疑
│  └── TailorView     # 裁缝: 无投票按钮
├── RoundResult       # 每轮结果展示
└── Settlement        # 结算页面

/manager/
├── GameCreate        # 新建游戏
├── GameControl       # 分配身份 + 控制流程
└── GameResult        # 查看结算结果
```

### 3.2 JoinGame 组件
- [ ] 游戏 ID 输入框
- [ ] 玩家名字输入框
- [ ] 加入按钮
- [ ] 错误提示

### 3.3 WaitingRoom 组件
- [ ] 显示已加入的 8 个玩家
- [ ] 等待通知
- [ ] 显示当前游戏状态
- [ ] 自动刷新（轮询或 WebSocket）

### 3.4 VotingUI 组件
**NormalView**:
- [ ] 三个大按钮：质疑 / 附和 / 沉默
- [ ] 按钮禁用状态（已投票后禁用）
- [ ] 投票确认动画

**ChildView**:
- [ ] 首轮：只显示"质疑"按钮
- [ ] 后续轮次：显示全部 3 个按钮
- [ ] 特殊样式标记"孩子"

**TailorView**:
- [ ] 显示"等待玩家投票"
- [ ] 实时投票进度条
- [ ] 无投票按钮

### 3.5 RoundResult 组件
- [ ] 显示该轮的结果：成功/失败
- [ ] 显示投票分布：质疑 / 附和 / 沉默
- [ ] 显示得分变化表
  - 每个玩家的分数变化
  - 分数来源说明
- [ ] "下一轮"按钮（或自动跳转）

### 3.6 Settlement 组件（核心，见 Phase 3.2）
详见下一章

---

## Phase 3.2 🌟 结算页面 - HUMAN 3.0 系统 (预计 2-3 天)

### 3.6.1 OverviewPanel
- [ ] 游戏稳定性评分
  - Stable (质疑成功率 < 30%)
  - Critical (30-70%)
  - Collapsed (> 70%)
- [ ] 质疑成功率百分比
- [ ] 总质疑次数 vs 成功次数

### 3.6.2 Timeline 时间轴
- [ ] 5 轮可展开/折叠
- [ ] 每轮显示：
  - 轮次编号
  - 基础阈值 + 两个大臣调整 = 有效阈值
  - 投票分布饼图或条形图
  - 质疑成功/失败标记
  
### 3.6.3 ScoreMatrix 分数矩阵
- [ ] 表格：8 个玩家 × 5 轮
- [ ] 每个单元格显示该轮得分 (+3, -1, 0, 等)
- [ ] 右侧列显示总分
- [ ] 可排序（按总分、按轮次等）
- [ ] 特殊标记孩子质疑的 -3 分

### 3.6.4 分数流动动画
- [ ] SVG 动画：分数从玩家头像流向总分区域
- [ ] 颜色代码：
  - 绿色 (+3): 质疑成功
  - 红色 (-1/-3): 失败或孩子惩罚
  - 蓝色 (+0): 沉默
- [ ] 每个分数独立动画，持续约 1 秒

### 3.6.5 FinalRank 最终排名
- [ ] 排名表：1-8 名
- [ ] 每个玩家显示：
  - 排名
  - 名字
  - 总分
  - 身份（裁缝/大臣/百姓/孩子）
- [ ] 排名动画：从底部逐个滑入
- [ ] 冠军高亮

### 3.6.6 RoleReveal 身份揭示
- [ ] 8 个卡片，每个显示：
  - 玩家名字
  - 身份
  - 最终排名
  - 总分
  - 小头像或标记
- [ ] 卡片展示动画（翻转或淡入）
- [ ] 可按身份分组显示

### 3.6.7 代理导出
- [ ] "导出为 JSON" 按钮
- [ ] "打印" 按钮
- [ ] "分享结果链接" 按钮（可选）

---

## Phase 4 🎮 管理端页面 (预计 1-2 天)

### 4.1 GameCreate 页面
- [ ] 输入 8 个玩家名字
- [ ] "创建游戏"按钮
- [ ] 成功后显示 Game ID
- [ ] 复制按钮

### 4.2 GameControl 页面
- [ ] 显示游戏 ID
- [ ] 显示 8 个玩家列表（可分配身份）
  - 选择玩家 → 选择身份 → 确认
  - 支持拖拽分配（可选）
- [ ] "开始游戏"按钮
- [ ] 当前轮次显示
- [ ] 逐轮控制面板：
  - 输入 base_threshold (2-6)
  - 输入 minister1_adjustment (-1/0/1)
  - 输入 minister2_adjustment (-1/0/1)
  - "标记孩子质疑"复选框（如果该轮孩子质疑了）
  - "提交轮次"按钮
- [ ] 实时投票进度条（正在投票的玩家数）
- [ ] "结束游戏"按钮

### 4.3 GameResult 页面
- [ ] 与玩家端的 Settlement 页面相同
- [ ] 额外的"后台数据"面板：
  - 原始投票日志
  - 得分事件日志
  - 数据导出

---

## Phase 5 🧪 集成与测试 (预计 1-2 天)

### 5.1 端到端流程测试
- [ ] 创建游戏
- [ ] 分配身份
- [ ] 开始游戏
- [ ] 完成 5 轮游戏
- [ ] 查看结算结果

### 5.2 边界情况测试
- [ ] 孩子特殊质疑逻辑
- [ ] 裁缝无投票
- [ ] 质疑人数恰好等于阈值
- [ ] 所有玩家沉默
- [ ] 计分累积正确性

### 5.3 UI/UX 测试
- [ ] 响应式设计（手机/平板/桌面）
- [ ] HUMAN 3.0 风格一致性
- [ ] 动画流畅度
- [ ] 按钮可用性

### 5.4 性能优化
- [ ] 前端打包体积
- [ ] API 响应时间
- [ ] 数据库查询性能

---

## Phase 6 🚀 部署上线 (预计 1 天)

### 6.1 Supabase 最终配置
- [ ] 执行数据库 Schema
- [ ] 配置行级安全 (RLS)
- [ ] 测试数据库连接

### 6.2 GitHub 推送
- [ ] 所有代码提交到 main 分支
- [ ] 添加标签 (v1.0.0)

### 6.3 Render 部署
- [ ] 连接 GitHub 仓库
- [ ] 配置环境变量
- [ ] 后端和前端分别部署
- [ ] 配置自定义域名（可选）

### 6.4 上线前检查
- [ ] 测试所有功能
- [ ] 检查错误日志
- [ ] 验证数据一致性
- [ ] 性能基准测试

---

## 时间估计总结

| Phase | 工作量 | 预计时间 |
|-------|--------|---------|
| 1     | 项目初始化 | 1 天 ✅ |
| 2     | 后端 API | 2-3 天 |
| 3.1   | 前端基础页面 | 2-3 天 |
| 3.2   | 结算页面 | 2-3 天 |
| 4     | 管理端 | 1-2 天 |
| 5     | 集成测试 | 1-2 天 |
| 6     | 部署上线 | 1 天 |
| **总计** | | **11-16 天** |

---

## 优先级优化

如果时间紧张，可按以下优先级：

**MVP (必须，~1 周)**:
- Phase 2: 后端 API
- Phase 3.1: 前端基础
- Phase 3.2: 结算页面

**增强 (可选)**:
- Phase 4: 管理端
- Phase 5: 测试
- Phase 6: 部署

---

## 代码质量检查清单

每个 Phase 完成前：

- [ ] 所有 TypeScript 类型正确，无 `any`
- [ ] 所有函数有 JSDoc 注释
- [ ] 代码通过 linter (如有)
- [ ] 没有 console.log 调试代码
- [ ] 错误处理完整
- [ ] 提交信息遵循 Conventional Commits

---

## 参考资源

- [Express.js 文档](https://expressjs.com/)
- [React 文档](https://react.dev/)
- [Supabase 文档](https://supabase.com/docs)
- [Zustand 文档](https://github.com/pmndrs/zustand)
- [Tailwind CSS 文档](https://tailwindcss.com/)

---

**下一步**: 开始 Phase 2 后端 API 实现 🚀
