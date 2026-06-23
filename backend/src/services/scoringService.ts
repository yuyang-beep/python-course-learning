import { Vote, ScoreEvent, Round, Player } from '../types/index';
import { db } from './supabaseClient';

/**
 * Scoring Service - Core game logic for calculating scores
 *
 * Rule Summary:
 * - Quality Success: Challenge players +3, Agree players -1
 * - Child Challenge Bonus: If child challenged successfully, Agree players get additional -3
 * - Challenge Failed: Challenge players -1, Agree players +3
 * - Silent players: Always +0 (no change)
 */

export class ScoringService {
  /**
   * Calculate all scores for a given round
   */
  async calculateRoundScores(
    roundId: string,
    round: Round,
    players: Player[],
    votes: Vote[]
  ): Promise<ScoreEvent[]> {
    // Count votes by type
    const challengeCount = votes.filter((v) => v.choice === 'challenge').length;
    const agreeCount = votes.filter((v) => v.choice === 'agree').length;

    // Determine success
    const success = challengeCount >= round.effective_threshold;

    // Calculate scores
    const scoreEvents: ScoreEvent[] = [];

    if (success) {
      // === CHALLENGE SUCCESS ===
      // Challenge players: +3
      const challengeVotes = votes.filter((v) => v.choice === 'challenge');
      for (const vote of challengeVotes) {
        scoreEvents.push({
          id: '',
          round_id: roundId,
          player_id: vote.player_id,
          score_change: 3,
          reason: 'challenge_success',
          created_at: new Date().toISOString(),
        });
      }

      // Agree players: -1 (base)
      const agreeVotes = votes.filter((v) => v.choice === 'agree');
      for (const vote of agreeVotes) {
        scoreEvents.push({
          id: '',
          round_id: roundId,
          player_id: vote.player_id,
          score_change: -1,
          reason: 'agree_failed',
          created_at: new Date().toISOString(),
        });

        // Child challenge bonus: additional -3 if child questioned successfully
        if (round.child_questioned) {
          scoreEvents.push({
            id: '',
            round_id: roundId,
            player_id: vote.player_id,
            score_change: -3,
            reason: 'child_challenge_bonus',
            created_at: new Date().toISOString(),
          });
        }
      }
    } else {
      // === CHALLENGE FAILED ===
      // Challenge players: -1
      const challengeVotes = votes.filter((v) => v.choice === 'challenge');
      for (const vote of challengeVotes) {
        scoreEvents.push({
          id: '',
          round_id: roundId,
          player_id: vote.player_id,
          score_change: -1,
          reason: 'challenge_failed',
          created_at: new Date().toISOString(),
        });
      }

      // Agree players: +3
      const agreeVotes = votes.filter((v) => v.choice === 'agree');
      for (const vote of agreeVotes) {
        scoreEvents.push({
          id: '',
          round_id: roundId,
          player_id: vote.player_id,
          score_change: 3,
          reason: 'agree_success',
          created_at: new Date().toISOString(),
        });
      }
    }

    return scoreEvents;
  }

  /**
   * Record score events in database and update player total scores
   */
  async applyScores(
    roundId: string,
    scoreEvents: ScoreEvent[],
    players: Player[]
  ): Promise<void> {
    // Create a map of player scores
    const playerScoreMap = new Map<string, number>();
    for (const player of players) {
      playerScoreMap.set(player.id, player.final_score);
    }

    // Process each score event
    for (const event of scoreEvents) {
      // Record in database
      await db.recordScoreEvent(
        roundId,
        event.player_id,
        event.score_change,
        event.reason
      );

      // Update player total score
      const currentScore = playerScoreMap.get(event.player_id) || 0;
      const newScore = currentScore + event.score_change;
      playerScoreMap.set(event.player_id, newScore);
    }

    // Update all player scores in database
    for (const [playerId, newScore] of playerScoreMap) {
      await db.updatePlayerScore(playerId, newScore);
    }
  }

  /**
   * Calculate final rankings based on player scores
   */
  calculateRankings(players: Player[]): Player[] {
    // Sort by score (descending), then by name (for tie-breaking)
    const sorted = [...players].sort((a, b) => {
      if (b.final_score !== a.final_score) {
        return b.final_score - a.final_score;
      }
      return a.name.localeCompare(b.name);
    });

    // Assign ranks
    let rank = 1;
    for (let i = 0; i < sorted.length; i++) {
      if (i > 0 && sorted[i].final_score !== sorted[i - 1].final_score) {
        rank = i + 1;
      }
      sorted[i].rank = rank;
    }

    return sorted;
  }

  /**
   * Get game statistics
   */
  async getGameStats(gameId: string, rounds: Round[]): Promise<{
    stability: 'stable' | 'critical' | 'collapsed';
    challenge_success_rate: number;
    total_challenges: number;
    successful_challenges: number;
  }> {
    let totalChallenges = 0;
    let successfulChallenges = 0;

    for (const round of rounds) {
      if (round.success !== null) {
        const votes = await db.getRoundVotes(round.id);
        const challengeCount = votes.filter(
          (v) => v.choice === 'challenge'
        ).length;

        if (challengeCount > 0) {
          totalChallenges += challengeCount;
          if (round.success) {
            successfulChallenges += challengeCount;
          }
        }
      }
    }

    const successRate =
      totalChallenges > 0 ? (successfulChallenges / totalChallenges) * 100 : 0;

    // Determine stability
    let stability: 'stable' | 'critical' | 'collapsed';
    if (successRate < 30) {
      stability = 'stable';
    } else if (successRate < 70) {
      stability = 'critical';
    } else {
      stability = 'collapsed';
    }

    return {
      stability,
      challenge_success_rate: successRate,
      total_challenges: totalChallenges,
      successful_challenges: successfulChallenges,
    };
  }
}

export const scoringService = new ScoringService();
