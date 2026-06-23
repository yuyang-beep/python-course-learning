import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// ============================================================================
// MIDDLEWARE
// ============================================================================

app.use(cors());
app.use(express.json());

// ============================================================================
// HEALTH CHECK
// ============================================================================

app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// ============================================================================
// API ROUTES (To be implemented)
// ============================================================================

// Game routes
app.get('/api/games/:id', (req, res) => {
  res.json({ message: 'Get game details - TODO' });
});

app.post('/api/games', (req, res) => {
  res.json({ message: 'Create game - TODO' });
});

// Players routes
app.post('/api/games/:id/join', (req, res) => {
  res.json({ message: 'Join game - TODO' });
});

// Rounds routes
app.get('/api/games/:id/rounds', (req, res) => {
  res.json({ message: 'Get rounds - TODO' });
});

// Settlement routes
app.get('/api/games/:id/settlement', (req, res) => {
  res.json({ message: 'Get settlement - TODO' });
});

// ============================================================================
// ERROR HANDLING
// ============================================================================

app.use((err: any, req: express.Request, res: express.Response, next: express.NextFunction) => {
  console.error(err);
  res.status(err.status || 500).json({
    error: err.message || 'Internal Server Error',
  });
});

app.use((req: express.Request, res: express.Response) => {
  res.status(404).json({ error: 'Not Found' });
});

// ============================================================================
// START SERVER
// ============================================================================

app.listen(PORT, () => {
  console.log(`🚀 Server running at http://localhost:${PORT}`);
  console.log(`📚 API ready for implementation`);
});
