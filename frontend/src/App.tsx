import React from 'react';
import { useGameStore } from './stores/gameStore';

export function App() {
  const view = useGameStore((state) => state.current_view);

  return (
    <div className="min-h-screen bg-human-black text-human-text font-mono">
      {/* Header */}
      <header className="border-b border-human-gray p-4">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-2xl font-bold tracking-wide text-human-blue">
            HUMAN 3.0 → Emperor's New Clothes Settlement System
          </h1>
          <p className="text-human-gray text-xs mt-2">
            Behavioral Reconstruction Under Uncertainty
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto p-4">
        <div className="border border-human-gray bg-human-dark p-6">
          {view === 'join' && <JoinGameView />}
          {view === 'waiting' && <WaitingRoomView />}
          {view === 'voting' && <VotingView />}
          {view === 'result' && <RoundResultView />}
          {view === 'settlement' && <SettlementView />}
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-human-gray p-4 mt-8">
        <div className="max-w-7xl mx-auto text-center text-human-gray text-xs">
          <p>System v1.0 | 2026-06-23</p>
          <p className="mt-2">
            This is not a game. This is a system audit of human trust mechanisms.
          </p>
        </div>
      </footer>
    </div>
  );
}

// Placeholder Components
function JoinGameView() {
  return (
    <div className="text-center py-12">
      <p className="text-human-blue mb-4">→ Join Game View</p>
      <p className="text-human-gray text-sm">Placeholder - To be implemented</p>
    </div>
  );
}

function WaitingRoomView() {
  return (
    <div className="text-center py-12">
      <p className="text-human-blue mb-4">→ Waiting Room View</p>
      <p className="text-human-gray text-sm">Placeholder - To be implemented</p>
    </div>
  );
}

function VotingView() {
  return (
    <div className="text-center py-12">
      <p className="text-human-blue mb-4">→ Voting View</p>
      <p className="text-human-gray text-sm">Placeholder - To be implemented</p>
    </div>
  );
}

function RoundResultView() {
  return (
    <div className="text-center py-12">
      <p className="text-human-blue mb-4">→ Round Result View</p>
      <p className="text-human-gray text-sm">Placeholder - To be implemented</p>
    </div>
  );
}

function SettlementView() {
  return (
    <div className="text-center py-12">
      <p className="text-human-blue mb-4">→ Settlement View</p>
      <p className="text-human-gray text-sm">Placeholder - To be implemented</p>
    </div>
  );
}

export default App;
