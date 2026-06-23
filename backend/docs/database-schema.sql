-- ============================================================================
-- HUMAN 3.0 - Emperor's New Clothes
-- Supabase PostgreSQL Schema
-- ============================================================================

-- ============================================================================
-- ENUMS
-- ============================================================================

CREATE TYPE game_status AS ENUM ('waiting', 'in_progress', 'finished');
CREATE TYPE player_role AS ENUM ('tailor', 'minister', 'citizen', 'child');
CREATE TYPE vote_choice AS ENUM ('challenge', 'agree', 'silent');
CREATE TYPE scoring_reason AS ENUM (
  'challenge_success',
  'agree_failed',
  'child_challenge_bonus',
  'challenge_failed',
  'agree_success'
);

-- ============================================================================
-- TABLES
-- ============================================================================

-- Games Table
CREATE TABLE games (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  status game_status NOT NULL DEFAULT 'waiting',
  current_round INT NOT NULL DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  finished_at TIMESTAMP WITH TIME ZONE,
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- Players Table
CREATE TABLE players (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  game_id UUID NOT NULL REFERENCES games(id) ON DELETE CASCADE,
  name VARCHAR(100) NOT NULL,
  role player_role NOT NULL,
  final_score INT NOT NULL DEFAULT 0,
  rank INT,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- Rounds Table (5 rounds per game)
CREATE TABLE rounds (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  game_id UUID NOT NULL REFERENCES games(id) ON DELETE CASCADE,
  round_number INT NOT NULL CHECK (round_number >= 1 AND round_number <= 5),
  base_threshold INT NOT NULL CHECK (base_threshold >= 2 AND base_threshold <= 6),
  minister1_adjustment INT NOT NULL CHECK (minister1_adjustment IN (-1, 0, 1)),
  minister2_adjustment INT NOT NULL CHECK (minister2_adjustment IN (-1, 0, 1)),
  effective_threshold INT NOT NULL,
  child_questioned BOOLEAN NOT NULL DEFAULT FALSE,
  success BOOLEAN,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  UNIQUE(game_id, round_number)
);

-- Votes Table
CREATE TABLE votes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  round_id UUID NOT NULL REFERENCES rounds(id) ON DELETE CASCADE,
  player_id UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
  choice vote_choice NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  UNIQUE(round_id, player_id)
);

-- Score Events Table (detailed scoring records)
CREATE TABLE score_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  round_id UUID NOT NULL REFERENCES rounds(id) ON DELETE CASCADE,
  player_id UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
  score_change INT NOT NULL,
  reason scoring_reason NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- ============================================================================
-- INDEXES
-- ============================================================================

CREATE INDEX idx_players_game_id ON players(game_id);
CREATE INDEX idx_rounds_game_id ON rounds(game_id);
CREATE INDEX idx_votes_round_id ON votes(round_id);
CREATE INDEX idx_votes_player_id ON votes(player_id);
CREATE INDEX idx_score_events_round_id ON score_events(round_id);
CREATE INDEX idx_score_events_player_id ON score_events(player_id);

-- ============================================================================
-- FUNCTIONS & TRIGGERS
-- ============================================================================

-- Update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers for updated_at
CREATE TRIGGER update_games_updated_at
  BEFORE UPDATE ON games
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_players_updated_at
  BEFORE UPDATE ON players
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_rounds_updated_at
  BEFORE UPDATE ON rounds
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();

-- ============================================================================
-- POLICIES (RLS - Row Level Security)
-- ============================================================================

-- Enable RLS
ALTER TABLE games ENABLE ROW LEVEL SECURITY;
ALTER TABLE players ENABLE ROW LEVEL SECURITY;
ALTER TABLE rounds ENABLE ROW LEVEL SECURITY;
ALTER TABLE votes ENABLE ROW LEVEL SECURITY;
ALTER TABLE score_events ENABLE ROW LEVEL SECURITY;

-- Allow public read on games
CREATE POLICY "Allow public read games"
  ON games FOR SELECT
  USING (true);

-- Allow public read on players
CREATE POLICY "Allow public read players"
  ON players FOR SELECT
  USING (true);

-- Allow public read on rounds
CREATE POLICY "Allow public read rounds"
  ON rounds FOR SELECT
  USING (true);

-- Allow public read on votes
CREATE POLICY "Allow public read votes"
  ON votes FOR SELECT
  USING (true);

-- Allow public read on score_events
CREATE POLICY "Allow public read score_events"
  ON score_events FOR SELECT
  USING (true);

-- Allow public insert (for development - consider restricting in production)
CREATE POLICY "Allow public insert games"
  ON games FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Allow public insert players"
  ON players FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Allow public insert rounds"
  ON rounds FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Allow public insert votes"
  ON votes FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Allow public insert score_events"
  ON score_events FOR INSERT
  WITH CHECK (true);

-- Allow public update
CREATE POLICY "Allow public update games"
  ON games FOR UPDATE
  USING (true);

CREATE POLICY "Allow public update players"
  ON players FOR UPDATE
  USING (true);

CREATE POLICY "Allow public update rounds"
  ON rounds FOR UPDATE
  USING (true);

-- ============================================================================
-- SEED DATA (Optional - Remove for production)
-- ============================================================================

-- INSERT INTO games (status) VALUES ('waiting');
-- This will be populated by the application

-- ============================================================================
-- NOTES
-- ============================================================================
-- 1. All timestamps are in UTC (WITH TIME ZONE)
-- 2. RLS is enabled but policies allow public access (development mode)
-- 3. Consider adding authentication/authorization in production
-- 4. Score calculations are done in the application layer
-- 5. The effective_threshold is pre-calculated before storing in the DB
