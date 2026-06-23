import { create } from 'zustand';
import type {
  UIStore,
  GameSession,
  SettlementData,
  Player,
} from '../types/index';

export const useGameStore = create<UIStore>((set) => ({
  game_id: null,
  player_id: null,
  current_view: 'join',
  game_session: null,
  settlement_data: null,

  set_game_id: (id: string) => set({ game_id: id }),
  set_player_id: (id: string) => set({ player_id: id }),
  set_current_view: (view: string) =>
    set({ current_view: view as any }),
  set_game_session: (session: GameSession) =>
    set({ game_session: session }),
  set_settlement_data: (data: SettlementData) =>
    set({ settlement_data: data }),
}));

// Helper functions
export const getPlayerRole = (players: Player[], playerId: string) => {
  return players.find((p) => p.id === playerId)?.role;
};

export const isChild = (players: Player[], playerId: string) => {
  return getPlayerRole(players, playerId) === 'child';
};

export const isTailor = (players: Player[], playerId: string) => {
  return getPlayerRole(players, playerId) === 'tailor';
};
