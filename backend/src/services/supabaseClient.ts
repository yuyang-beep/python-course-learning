import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseServiceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

if (!supabaseUrl || !supabaseServiceRoleKey) {
  throw new Error(
    'Missing Supabase environment variables: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY'
  );
}

/**
 * Supabase client for server-side operations
 * Uses service role key for full access
 */
export const supabase = createClient(supabaseUrl, supabaseServiceRoleKey);

/**
 * Database queries helpers
 */
export const db = {
  // Games
  async getGame(gameId: string) {
    const { data, error } = await supabase
      .from('games')
      .select('*')
      .eq('id', gameId)
      .single();
    if (error) throw error;
    return data;
  },

  async createGame() {
    const { data, error } = await supabase
      .from('games')
      .insert({ status: 'waiting', current_round: 0 })
      .select()
      .single();
    if (error) throw error;
    return data;
  },

  async updateGameStatus(gameId: string, status: string) {
    const { data, error } = await supabase
      .from('games')
      .update({ status })
      .eq('id', gameId)
      .select()
      .single();
    if (error) throw error;
    return data;
  },

  // Players
  async getGamePlayers(gameId: string) {
    const { data, error } = await supabase
      .from('players')
      .select('*')
      .eq('game_id', gameId);
    if (error) throw error;
    return data;
  },

  async addPlayer(gameId: string, name: string, role: string) {
    const { data, error } = await supabase
      .from('players')
      .insert({
        game_id: gameId,
        name,
        role,
        final_score: 0,
      })
      .select()
      .single();
    if (error) throw error;
    return data;
  },

  async updatePlayerRole(playerId: string, role: string) {
    const { data, error } = await supabase
      .from('players')
      .update({ role })
      .eq('id', playerId)
      .select()
      .single();
    if (error) throw error;
    return data;
  },

  async updatePlayerScore(playerId: string, score: number) {
    const { data, error } = await supabase
      .from('players')
      .update({ final_score: score })
      .eq('id', playerId)
      .select()
      .single();
    if (error) throw error;
    return data;
  },

  // Rounds
  async createRound(
    gameId: string,
    roundNumber: number,
    baseThreshold: number,
    minister1Adjustment: number,
    minister2Adjustment: number
  ) {
    const effectiveThreshold =
      baseThreshold + minister1Adjustment + minister2Adjustment;

    const { data, error } = await supabase
      .from('rounds')
      .insert({
        game_id: gameId,
        round_number: roundNumber,
        base_threshold: baseThreshold,
        minister1_adjustment: minister1Adjustment,
        minister2_adjustment: minister2Adjustment,
        effective_threshold: effectiveThreshold,
      })
      .select()
      .single();
    if (error) throw error;
    return data;
  },

  async getRoundDetails(roundId: string) {
    const { data, error } = await supabase
      .from('rounds')
      .select('*')
      .eq('id', roundId)
      .single();
    if (error) throw error;
    return data;
  },

  async updateRound(roundId: string, updates: any) {
    const { data, error } = await supabase
      .from('rounds')
      .update(updates)
      .eq('id', roundId)
      .select()
      .single();
    if (error) throw error;
    return data;
  },

  // Votes
  async submitVote(roundId: string, playerId: string, choice: string) {
    const { data, error } = await supabase
      .from('votes')
      .upsert({
        round_id: roundId,
        player_id: playerId,
        choice,
      })
      .select()
      .single();
    if (error) throw error;
    return data;
  },

  async getRoundVotes(roundId: string) {
    const { data, error } = await supabase
      .from('votes')
      .select('*')
      .eq('round_id', roundId);
    if (error) throw error;
    return data;
  },

  // Score Events
  async recordScoreEvent(
    roundId: string,
    playerId: string,
    scoreChange: number,
    reason: string
  ) {
    const { data, error } = await supabase
      .from('score_events')
      .insert({
        round_id: roundId,
        player_id: playerId,
        score_change: scoreChange,
        reason,
      })
      .select()
      .single();
    if (error) throw error;
    return data;
  },

  async getRoundScoreEvents(roundId: string) {
    const { data, error } = await supabase
      .from('score_events')
      .select('*')
      .eq('round_id', roundId);
    if (error) throw error;
    return data;
  },

  async getGameScoreEvents(gameId: string) {
    const { data, error } = await supabase
      .from('score_events')
      .select('*')
      .eq('rounds.game_id', gameId)
      .order('created_at', { ascending: false });
    if (error) throw error;
    return data;
  },
};
