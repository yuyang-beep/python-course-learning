/**
 * 皇帝的新装 - 后端服务器
 * Node.js + Express + Socket.io
 */

const express = require('express');
const http = require('http');
const socketIO = require('socket.io');
const cors = require('cors');
const path = require('path');

const app = express();
const server = http.createServer(app);
const io = socketIO(server, {
    cors: {
        origin: "*",
        methods: ["GET", "POST"]
    },
    transports: ['websocket', 'polling']
});

// 中间件
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// ==================== 根路由 ====================
app.get('/', (req, res) => {
    res.json({
        message: '皇帝的新装 - 游戏服务器',
        version: '1.0.0',
        status: 'running',
        endpoints: {
            health: '/health',
            room: '/api/room/:code',
            player: '/api/player/:roomCode/:playerId'
        },
        socketio: 'WebSocket connection available'
    });
});

// ==================== 数据存储 ====================
const rooms = new Map();      // 房间数据
const players = new Map();    // 玩家连接映射

// ==================== 辅助函数 ====================
function generateRoomCode() {
    return Math.random().toString(36).substring(2, 8).toUpperCase();
}

function createRoom() {
    const code = generateRoomCode();
    rooms.set(code, {
        code,
        createdAt: Date.now(),
        status: 'waiting',         // waiting | playing | round_active | round_completed
        currentRound: 1,
        players: new Map(),        // playerId -> player data
        assignments: new Map(),    // playerId -> role
        roundConfigs: {},          // round -> config
        rounds: {}                 // round -> { votes, results }
    });
    return code;
}

function getRoom(code) {
    return rooms.get(code);
}

function deleteRoom(code) {
    rooms.delete(code);
}

function addPlayer(roomCode, playerId, playerName) {
    const room = getRoom(roomCode);
    if (!room) return false;

    room.players.set(playerId, {
        id: playerId,
        name: playerName,
        role: null,
        totalScore: 0,
        joinedAt: Date.now()
    });
    return true;
}

function removePlayer(roomCode, playerId) {
    const room = getRoom(roomCode);
    if (!room) return false;

    room.players.delete(playerId);
    room.assignments.delete(playerId);
    return true;
}

function assignRole(roomCode, playerId, role) {
    const room = getRoom(roomCode);
    if (!room) return false;

    const player = room.players.get(playerId);
    if (!player) return false;

    room.assignments.set(playerId, role);
    player.role = role;
    return true;
}

// ==================== REST API ====================

// 获取房间状态
app.get('/api/room/:code', (req, res) => {
    const room = getRoom(req.params.code);
    if (!room) {
        return res.status(404).json({ error: 'Room not found' });
    }

    res.json({
        code: room.code,
        status: room.status,
        currentRound: room.currentRound,
        playerCount: room.players.size,
        players: Array.from(room.players.values()).map(p => ({
            id: p.id,
            name: p.name,
            role: room.assignments.get(p.id) || null,
            totalScore: p.totalScore
        }))
    });
});

// 获取玩家数据
app.get('/api/player/:roomCode/:playerId', (req, res) => {
    const room = getRoom(req.params.roomCode);
    if (!room) {
        return res.status(404).json({ error: 'Room not found' });
    }

    const player = room.players.get(req.params.playerId);
    if (!player) {
        return res.status(404).json({ error: 'Player not found' });
    }

    res.json({
        id: player.id,
        name: player.name,
        role: room.assignments.get(player.id) || null,
        totalScore: player.totalScore
    });
});

// 健康检查
app.get('/health', (req, res) => {
    res.json({
        status: 'ok',
        activeRooms: rooms.size,
        timestamp: new Date().toISOString()
    });
});

// ==================== Socket.io 事件 ====================

io.on('connection', (socket) => {
    console.log(`[连接] 玩家连接: ${socket.id}`);

    // 玩家加入房间
    socket.on('join_room', (data) => {
        const { roomCode, playerId, playerName } = data;

        if (!addPlayer(roomCode, playerId, playerName)) {
            socket.emit('error', { message: '房间不存在或加入失败' });
            return;
        }

        players.set(playerId, { roomCode, socketId: socket.id });
        socket.join(roomCode);

        console.log(`[加入] ${playerName} 加入房间 ${roomCode}`);

        // 通知房间内的管理者
        io.to(roomCode).emit('player_joined', {
            players: getRoom(roomCode).players
        });
    });

    // 管理者创建房间
    socket.on('create_room', (callback) => {
        const code = createRoom();
        players.set(socket.id, { roomCode: code, socketId: socket.id });
        socket.join(code);

        console.log(`[创建] 房间创建: ${code}`);
        callback({ code });
    });

    // 分配身份
    socket.on('assign_role', (data) => {
        const { roomCode, playerId, role } = data;

        if (!assignRole(roomCode, playerId, role)) {
            socket.emit('error', { message: '分配失败' });
            return;
        }

        console.log(`[分配] ${playerId} 分配角色 ${role}`);

        io.to(roomCode).emit('role_assigned', {
            playerId,
            role,
            assignments: Object.fromEntries(getRoom(roomCode).assignments)
        });
    });

    // 开始游戏
    socket.on('start_game', (data) => {
        const { roomCode } = data;
        const room = getRoom(roomCode);
        if (!room) return;

        room.status = 'playing';

        console.log(`[开始] 房间 ${roomCode} 游戏开始`);

        io.to(roomCode).emit('game_started', {
            status: 'playing',
            currentRound: 1
        });
    });

    // 开启轮数
    socket.on('start_round', (data) => {
        const { roomCode, round, config } = data;
        const room = getRoom(roomCode);
        if (!room) return;

        room.status = 'round_active';
        room.currentRound = round;
        room.roundConfigs[round] = config;

        // 初始化本轮数据
        if (!room.rounds[round]) {
            room.rounds[round] = { votes: {}, results: {} };
        }

        console.log(`[轮数] 房间 ${roomCode} 第 ${round} 轮开启`);

        io.to(roomCode).emit('round_started', {
            status: 'round_active',
            round,
            config
        });
    });

    // 接收投票
    socket.on('submit_vote', (data) => {
        const { roomCode, playerId, round, vote } = data;
        const room = getRoom(roomCode);
        if (!room) return;

        if (!room.rounds[round]) {
            room.rounds[round] = { votes: {}, results: {} };
        }

        room.rounds[round].votes[playerId] = vote;

        console.log(`[投票] 玩家 ${playerId} 投票: ${vote}`);

        // 统计投票
        const votes = room.rounds[round].votes;
        const stats = {
            '质疑': 0,
            '附和': 0,
            '沉默': 0,
            '未投': 0
        };

        room.players.forEach((player) => {
            const choice = votes[player.id];
            if (choice) {
                stats[choice]++;
            } else {
                stats['未投']++;
            }
        });

        // 通知所有人投票进度
        io.to(roomCode).emit('vote_stats_updated', {
            round,
            stats,
            totalPlayers: room.players.size
        });
    });

    // 结束轮数并计算结果
    socket.on('end_round', (data) => {
        const { roomCode, round } = data;
        const room = getRoom(roomCode);
        if (!room) return;

        const votes = room.rounds[round]?.votes || {};
        const config = room.roundConfigs[round] || {};

        // 计算结果
        const results = calculateResults(room, votes, config);

        // 更新玩家分数
        Object.keys(results).forEach(playerId => {
            const player = room.players.get(playerId);
            if (player) {
                player.totalScore += results[playerId].score;
            }
        });

        room.rounds[round].results = results;
        room.status = 'round_completed';

        console.log(`[结算] 房间 ${roomCode} 第 ${round} 轮结算完成`);

        // 发送结果给所有人
        io.to(roomCode).emit('round_ended', {
            round,
            results,
            players: Array.from(room.players.values()).map(p => ({
                id: p.id,
                name: p.name,
                role: room.assignments.get(p.id),
                totalScore: p.totalScore
            }))
        });
    });

    // 退出房间
    socket.on('exit_room', (data) => {
        const { roomCode, playerId } = data;

        if (playerId) {
            removePlayer(roomCode, playerId);
            players.delete(playerId);

            io.to(roomCode).emit('player_left', {
                playerId,
                players: getRoom(roomCode)?.players
            });

            console.log(`[退出] 玩家 ${playerId} 退出房间 ${roomCode}`);
        }

        // 如果房间没有玩家，删除房间
        const room = getRoom(roomCode);
        if (room && room.players.size === 0) {
            deleteRoom(roomCode);
            console.log(`[删除] 房间 ${roomCode} 已删除（无玩家）`);
        }
    });

    // 删除房间（管理者）
    socket.on('delete_room', (data) => {
        const { roomCode } = data;
        deleteRoom(roomCode);

        io.to(roomCode).emit('room_deleted');
        socket.leave(roomCode);

        console.log(`[删除] 房间 ${roomCode} 被删除`);
    });

    // 断开连接
    socket.on('disconnect', () => {
        const playerInfo = players.get(socket.id);
        if (playerInfo) {
            const { roomCode } = playerInfo;
            const room = getRoom(roomCode);

            if (room && room.players.size > 0) {
                io.to(roomCode).emit('player_disconnected', {
                    message: '某位玩家已离线'
                });
            }

            players.delete(socket.id);
        }

        console.log(`[断开] 玩家断开连接: ${socket.id}`);
    });
});

// ==================== 计分逻辑 ====================
function calculateResults(room, votes, config) {
    const results = {};
    const effective = config.base + config.m1 + config.m2;

    // 统计投票
    let challengeCount = 0;
    let supportCount = 0;
    let silenceCount = 0;
    const challengePlayers = [];
    const supportPlayers = [];

    Object.keys(votes).forEach(playerId => {
        const choice = votes[playerId];
        if (choice === '质疑') {
            challengeCount++;
            challengePlayers.push(playerId);
        } else if (choice === '附和') {
            supportCount++;
            supportPlayers.push(playerId);
        } else if (choice === '沉默') {
            silenceCount++;
        }
    });

    const success = challengeCount >= effective;

    // 初始化结果
    room.players.forEach((player, playerId) => {
        results[playerId] = { score: 0, vote: votes[playerId] || '未投' };
    });

    // 完整的计分规则
    if (success) {
        // 质疑成功
        const scoreValue = supportCount + silenceCount;
        challengePlayers.forEach(playerId => {
            results[playerId].score = scoreValue;
        });

        // 孩子特殊质疑额外奖励
        if (config.childSpecial) {
            const childId = Array.from(room.assignments.entries()).find(
                ([_, role]) => role === '孩子'
            )?.[0];
            if (childId && challengePlayers.includes(childId)) {
                results[childId].score += 3;
            }
        }

        // 扣分
        const deductValue = challengeCount;
        room.players.forEach((player, playerId) => {
            const role = room.assignments.get(playerId);
            if (role === '裁缝') {
                results[playerId].score -= deductValue;
            }
        });

        supportPlayers.forEach(playerId => {
            results[playerId].score -= deductValue;
            if (config.childSpecial) {
                results[playerId].score -= 3;
            }
        });
    } else {
        // 质疑失败
        const scoreValue = challengeCount + silenceCount;
        room.players.forEach((player, playerId) => {
            const role = room.assignments.get(playerId);
            if (role === '裁缝') {
                results[playerId].score = scoreValue;
            }
        });

        supportPlayers.forEach(playerId => {
            results[playerId].score = scoreValue;
        });

        // 扣分
        const deductValue = supportCount;
        challengePlayers.forEach(playerId => {
            const role = room.assignments.get(playerId);
            if (!(config.childSpecial && role === '孩子')) {
                results[playerId].score -= deductValue;
            }
        });
    }

    return results;
}

// ==================== 启动服务器 ====================
const PORT = process.env.PORT || 3000;

server.listen(PORT, () => {
    console.log(`
╔════════════════════════════════════════════╗
║   皇帝的新装 - 后端服务器已启动 🚀        ║
╠════════════════════════════════════════════╣
║ 服务器地址: http://localhost:${PORT}       ║
║ WebSocket: ws://localhost:${PORT}          ║
║ 健康检查: http://localhost:${PORT}/health  ║
╚════════════════════════════════════════════╝
    `);
});

module.exports = { app, server, io };
