// ============================================================================
// GAME STATUS & ROLES
// ============================================================================

export type GameStatus = 'waiting' | 'in_progress' | 'finished';
export type PlayerRole = 'tailor' | 'minister' | 'citizen' | 'child';
export type VoteChoice = 'challenge' | 'agree' | 'silent';
export type ScoringReason =
  | 'challenge_success'
  | 'agree_failed'
  | 'child_challenge_bonus'
  | 'challenge_failed'
  | 'agree_success';

// ============================================================================
// GAME ENTITIES
// ============================================================================

export interface Game {
  id: string;
  status: GameStatus;
  current_round: number;
  created_at: string;
  finished_at: string | null;
}

export interface Player {
  id: string;
  game_id: string;
  name: string;
  role: PlayerRole;
  final_score: number;
  rank: number | null;
  created_at: string;
}

export interface Round {
  id: string;
  game_id: string;
  round_number: number; // 1-5
  base_threshold: number; // 2-6
  minister1_adjustment: number; // -1, 0, 1
  minister2_adjustment: number; // -1, 0, 1
  effective_threshold: number; // 计算出来
  child_questioned: boolean;
  success: boolean | null;
  created_at: string;
}

export interface Vote {
  id: string;
  round_id: string;
  player_id: string;
  choice: VoteChoice;
  created_at: string;
}

export interface ScoreEvent {
  id: string;
  round_id: string;
  player_id: string;
  score_change: number;
  reason: ScoringReason;
  created_at: string;
}

// ============================================================================
// API REQUEST/RESPONSE
// ============================================================================

export interface CreateGameRequest {
  player_names: string[];
}

export interface AssignRoleRequest {
  player_id: string;
  role: PlayerRole;
}

export interface SetRoundParamsRequest {
  base_threshold: number;
  minister1_adjustment: number;
  minister2_adjustment: number;
}

export interface SubmitVoteRequest {
  player_id: string;
  choice: VoteChoice;
}

export interface GameResultResponse {
  game: Game;
  players: Player[];
  rounds: RoundDetail[];
  final_rankings: PlayerWithScore[];
}

export interface RoundDetail {
  round: Round;
  votes: Vote[];
  score_events: ScoreEvent[];
  vote_distribution: {
    challenge_count: number;
    agree_count: number;
    silent_count: number;
  };
}

export interface PlayerWithScore extends Player {
  total_score: number;
}

// ============================================================================
// SETTLEMENT PAGE DATA
// ============================================================================

export interface SettlementData {
  game_info: {
    id: string;
    status: GameStatus;
    total_rounds: number;
  };
  overview: {
    stability: 'stable' | 'critical' | 'collapsed';
    challenge_success_rate: number; // 0-100
    total_challenge_attempts: number;
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
  score_changes: {
    player_id: string;
    player_name: string;
    change: number;
    reason: ScoringReason;
  }[];
}

export interface SettlementPlayer {
  player_id: string;
  rank: number;
  name: string;
  role: PlayerRole;
  total_score: number;
  round_scores: number[];
}

export interface RoleReveal {
  player_id: string;
  player_name: string;
  role: PlayerRole;
  final_score: number;
  rank: number;
}

// ============================================================================
// INTERNAL LOGIC
// ============================================================================

export interface RoundState {
  base_threshold?: number;
  minister1_adjustment?: number;
  minister2_adjustment?: number;
  effective_threshold?: number;
  votes?: Map<string, VoteChoice>;
  challenge_count?: number;
  success?: boolean;
}
