import { db } from './supabaseClient';
import { scoringService } from './scoringService';
import type {
  Game,
  Player,
  Round,
  Vote,
  GameResultResponse,
  SettlementData,
} from '../types/index';

/**
 * Game Service - High-level game management operations
 */

export class GameService {
  /**
   * Create a new game session
   */
  async createGame(playerNames: string[]): Promise<Game> {
    if (playerNames.length !== 8) {
      throw new Error('Game must have exactly 8 players');
    }

    const game = await db.createGame();

    // Add players (initially unassigned)
    for (const name of playerNames) {
      await db.addPlayer(game.id, name, 'citizen'); // Default role
    }

    return game;
  }

  /**
   * Get full game state
   */
  async getGameState(gameId: string) {
    const game = await db.getGame(gameId);
    const players = await db.getGamePlayers(gameId);

    return {
      game,
      players,
    };
  }

  /**
   * Assign role to a player
   */
  async assignPlayerRole(playerId: string, role: string): Promise<Player> {
    return await db.updatePlayerRole(playerId, role);
  }

  /**
   * Start a game
   */
  async startGame(gameId: string): Promise<Game> {
    return await db.updateGameStatus(gameId, 'in_progress');
  }

  /**
   * Create a new round with parameters
   */
  async createRound(
    gameId: string,
    roundNumber: number,
    baseThreshold: number,
    minister1Adjustment: number,
    minister2Adjustment: number
  ): Promise<Round> {
    return await db.createRound(
      gameId,
      roundNumber,
      baseThreshold,
      minister1Adjustment,
      minister2Adjustment
    );
  }

  /**
   * Process votes for a round
   */
  async processRoundVotes(roundId: string): Promise<void> {
    const round = await db.getRoundDetails(roundId);
    const votes = await db.getRoundVotes(roundId);
    const gameId = round.game_id;
    const players = await db.getGamePlayers(gameId);

    // Determine if challenge succeeded
    const challengeCount = votes.filter(
      (v) => v.choice === 'challenge'
    ).length;
    const success = challengeCount >= round.effective_threshold;

    // Update round with result
    await db.updateRound(roundId, { success });

    // Calculate and apply scores
    const scoreEvents = await scoringService.calculateRoundScores(
      roundId,
      round,
      players,
      votes
    );
    await scoringService.applyScores(roundId, scoreEvents, players);
  }

  /**
   * Finish a game and calculate final rankings
   */
  async finishGame(gameId: string): Promise<GameResultResponse> {
    const game = await db.getGame(gameId);
    let players = await db.getGamePlayers(gameId);

    // Calculate final rankings
    players = scoringService.calculateRankings(players);

    // Update database with ranks
    for (const player of players) {
      await db.updatePlayerScore(player.id, player.final_score);
    }

    // Update game status
    await db.updateGameStatus(gameId, 'finished');

    // Fetch all rounds for response
    const rounds = await Promise.all(
      Array.from({ length: 5 }, async (_, i) => {
        const round = await db.getRoundDetails(
          (
            await db.getGameScoreEvents(gameId)
          )[i]?.id || ''
        );
        if (!round) return null;

        const votes = await db.getRoundVotes(round.id);
        const scoreEvents = await db.getRoundScoreEvents(round.id);

        return {
          round,
          votes,
          score_events: scoreEvents,
          vote_distribution: {
            challenge_count: votes.filter(
              (v) => v.choice === 'challenge'
            ).length,
            agree_count: votes.filter((v) => v.choice === 'agree').length,
            silent_count: votes.filter((v) => v.choice === 'silent').length,
          },
        };
      })
    ).then((rounds) => rounds.filter((r) => r !== null));

    return {
      game,
      players,
      rounds: rounds as any,
      final_rankings: players.map((p) => ({
        ...p,
        total_score: p.final_score,
      })),
    };
  }

  /**
   * Get settlement page data
   */
  async getSettlementData(gameId: string): Promise<SettlementData> {
    const game = await db.getGame(gameId);
    const players = await db.getGamePlayers(gameId);

    // Get all rounds info
    const roundDataPromises = Array.from({ length: 5 }, async (_, i) => {
      // This is a simplified version - in real implementation, you'd fetch actual rounds
      return null;
    });

    const roundsData = await Promise.all(roundDataPromises);

    const stats = await scoringService.getGameStats(
      gameId,
      roundsData.filter((r) => r !== null)
    );

    return {
      game_info: {
        id: game.id,
        status: game.status,
        total_rounds: 5,
      },
      overview: {
        stability: stats.stability,
        challenge_success_rate: stats.challenge_success_rate,
        total_challenge_attempts: stats.total_challenges,
        successful_challenges: stats.successful_challenges,
      },
      rounds: [], // To be populated
      final_rankings: scoringService.calculateRankings(players).map((p) => ({
        player_id: p.id,
        rank: p.rank || 0,
        name: p.name,
        role: p.role,
        total_score: p.final_score,
        round_scores: [0, 0, 0, 0, 0], // To be calculated
      })),
      role_reveals: players.map((p) => ({
        player_id: p.id,
        player_name: p.name,
        role: p.role,
        final_score: p.final_score,
        rank: p.rank || 0,
      })),
    };
  }
}

export const gameService = new GameService();
