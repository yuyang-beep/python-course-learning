// ============================================================================
// ENUMS & TYPES
// ============================================================================

export type GameStatus = 'waiting' | 'in_progress' | 'finished';
export type PlayerRole = 'tailor' | 'minister' | 'citizen' | 'child';
export type VoteChoice = 'challenge' | 'agree' | 'silent';

// ============================================================================
// GAME STATE
// ============================================================================

export interface Player {
  id: string;
  name: string;
  role: PlayerRole;
  final_score: number;
  rank: number | null;
}

export interface GameSession {
  id: string;
  status: GameStatus;
  current_round: number;
  players: Player[];
  created_at: string;
}

export interface RoundInfo {
  round_number: number;
  base_threshold: number;
  minister_adjustments: [number, number];
  effective_threshold: number;
  success: boolean;
  vote_distribution: {
    challenge: number;
    agree: number;
    silent: number;
  };
}

// ============================================================================
// SETTLEMENT PAGE
// ============================================================================

export interface SettlementData {
  game_id: string;
  status: GameStatus;
  overview: {
    stability: 'stable' | 'critical' | 'collapsed';
    challenge_success_rate: number;
    total_challenges: number;
    successful_challenges: number;
  };
  rounds: SettlementRound[];
  final_rankings: SettlementPlayer[];
  role_reveals: RoleReveal[];
}

export interface SettlementRound {
  round_number: number;
  base_threshold: number;
  minister_adjustments: [number, number];
  effective_threshold: number;
  vote_distribution: {
    challenge: number;
    agree: number;
    silent: number;
  };
  success: boolean;
  score_events: ScoreEvent[];
}

export interface SettlementPlayer {
  player_id: string;
  name: string;
  role: PlayerRole;
  rank: number;
  total_score: number;
  round_scores: number[];
}

export interface RoleReveal {
  player_id: string;
  name: string;
  role: PlayerRole;
  final_score: number;
  rank: number;
}

export interface ScoreEvent {
  player_name: string;
  score_change: number;
  reason: string;
}

// ============================================================================
// UI STATE
// ============================================================================

export interface UIStore {
  game_id: string | null;
  player_id: string | null;
  current_view: 'join' | 'waiting' | 'voting' | 'result' | 'settlement';
  game_session: GameSession | null;
  settlement_data: SettlementData | null;
  set_game_id: (id: string) => void;
  set_player_id: (id: string) => void;
  set_current_view: (view: string) => void;
  set_game_session: (session: GameSession) => void;
  set_settlement_data: (data: SettlementData) => void;
}

// ============================================================================
// API RESPONSES
// ============================================================================

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}
