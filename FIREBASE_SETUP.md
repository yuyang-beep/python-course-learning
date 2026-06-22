# Firebase 配置指南

## 快速开始

管理者端和玩家端使用 Firebase Realtime Database 来实现多人游戏同步。按以下步骤配置：

### 步骤 1: 创建 Firebase 项目

1. 访问 [Firebase Console](https://console.firebase.google.com/)
2. 点击"创建项目"或"添加项目"
3. 输入项目名称（如 `emperor-game`）
4. 点击"创建项目"

### 步骤 2: 获取 Firebase 配置

1. 在 Firebase 项目中，点击左上角的齿轮图标 ⚙️
2. 进入"项目设置"
3. 在"您的应用"部分，点击"</>"（Web）
4. 复制显示的配置对象，格式如下：

```javascript
const firebaseConfig = {
    apiKey: "YOUR_API_KEY",
    authDomain: "YOUR_AUTH_DOMAIN",
    databaseURL: "YOUR_DATABASE_URL",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_STORAGE_BUCKET",
    messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
    appId: "YOUR_APP_ID"
};
```

### 步骤 3: 设置 Realtime Database

1. 在 Firebase 控制台左侧菜单，点击"Realtime Database"
2. 点击"创建数据库"
3. 选择地区（建议选择离用户最近的）
4. **重要**: 选择"以测试模式启动"（允许所有读写，仅用于开发）
   - 生产环境应使用安全规则：
   ```json
   {
     "rules": {
       "rooms": {
         "$roomCode": {
           ".read": true,
           ".write": true,
           "players": {
             "$playerId": {
               ".read": true,
               ".write": true
             }
           },
           "rounds": {
             ".read": true,
             ".write": true
           },
           "results": {
             ".read": true,
             ".write": true
           }
         }
       }
     }
   }
   ```

### 步骤 4: 填入配置

1. 打开 `game-admin.html`
2. 找到以下代码（约在第 380 行）：
   ```javascript
   const firebaseConfig = {
       apiKey: "YOUR_API_KEY",
       // ... 其他字段
   };
   ```
3. 将你的 Firebase 配置替换占位符值

4. 打开 `game-player.html`
5. 找到相同位置的 `firebaseConfig`
6. 用同样的配置替换占位符值

### 步骤 5: 测试

1. **打开管理者端**: 在浏览器中打开 `game-admin.html`
2. **创建房间**: 点击"创建新房间"，记下房间代码（如 `AB12CD`）
3. **打开玩家端**: 在新标签页或另一浏览器打开 `game-player.html`
4. **加入房间**: 输入房间代码、玩家名称、选择身份，点击"加入房间"
5. **开启轮数**: 在管理者端配置参数，点击"开启本轮"
6. **投票**: 在玩家端点击投票按钮（质疑/附和/沉默），提交投票
7. **查看结果**: 在管理者端点击"结束本轮"，查看投票统计和结果

## 常见问题

### Q: 如何允许多个设备访问？
**A**: Firebase 云端数据库可以被任何有网络连接的设备访问。只需要在不同设备上使用相同的 Firebase 配置。

### Q: 房间代码是什么？
**A**: 房间代码是 6 位字母数字组合（如 `AB12CD`），由管理者创建。玩家使用此代码加入同一游戏房间。

### Q: 可以同时有多少个房间？
**A**: Firebase Realtime Database 的免费版本支持无限数量的房间，但并发连接数有限制。对于小规模游戏测试应该没问题。

### Q: 游戏数据会保留多久？
**A**: 数据存储在 Firebase 中，直到手动删除。管理者可以在 Firebase 控制台中清理旧数据。

### Q: 如何为生产环境做准备？
**A**: 
1. 配置安全规则（参见步骤 3）
2. 启用身份验证（可选）
3. 设置数据库备份
4. 监控使用量，可能需要升级到付费计划

## 数据结构

```
rooms/
  {roomCode}/
    status: "waiting" | "round_active" | "round_completed"
    currentRound: 1-5
    players/
      {playerId}/
        name: "玩家名"
        role: "裁缝" | "大臣" | "百姓" | "孩子"
        totalScore: 0
        joinedAt: timestamp
    roundConfigs/
      {roundNum}/
        base: 3
        m1: 0
        m2: 0
        childSpecial: false
    rounds/
      {roundNum}/
        votes/
          {playerId}: "质疑" | "附和" | "沉默"
        results/
          {playerId}: { score: 5, vote: "质疑" }
```

## 故障排除

如果玩家端无法连接到管理者端的房间：

1. **检查 Firebase 配置**: 确保两个文件中的配置完全相同
2. **检查房间代码**: 确保大小写正确（自动转换为大写）
3. **检查网络**: 两个设备应该都能访问 Firebase（`firebaseio.com`）
4. **查看浏览器控制台**: 按 F12 打开开发者工具，查看错误信息
5. **重启应用**: 刷新页面或重新加载应用

## 下一步

- 根据实际使用情况调整轮数（目前固定为 5 轮）
- 添加身份验证，确保只有授权用户可以创建房间
- 实现游戏结束时的排名分享功能
- 添加聊天或实时消息功能
