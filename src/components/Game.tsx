import React, { useEffect, useRef, useState } from 'react';
import { GameState, Player } from '../types/game';

const INITIAL_PLAYER: Player = {
  id: 'player',
  x: 100,
  y: 100,
  width: 32,
  height: 32,
  health: 100,
  speed: 5
};

const Game: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [gameState, setGameState] = useState<GameState>({
    player: INITIAL_PLAYER,
    objects: [],
    isPaused: false
  });

  // Handle keyboard input
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const { player } = gameState;
      const newPlayer = { ...player };

      switch (e.key) {
        case 'ArrowUp':
          newPlayer.y -= player.speed;
          break;
        case 'ArrowDown':
          newPlayer.y += player.speed;
          break;
        case 'ArrowLeft':
          newPlayer.x -= player.speed;
          break;
        case 'ArrowRight':
          newPlayer.x += player.speed;
          break;
      }

      setGameState(prev => ({
        ...prev,
        player: newPlayer
      }));
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [gameState]);

  // Game loop
  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas?.getContext('2d');
    
    if (!canvas || !ctx) return;

    const gameLoop = () => {
      if (!gameState.isPaused) {
        // Clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw player
        ctx.fillStyle = 'red';
        ctx.fillRect(
          gameState.player.x,
          gameState.player.y,
          gameState.player.width,
          gameState.player.height
        );

        // Draw other objects
        gameState.objects.forEach(obj => {
          ctx.fillStyle = 'blue';
          ctx.fillRect(obj.x, obj.y, obj.width, obj.height);
        });
      }

      requestAnimationFrame(gameLoop);
    };

    gameLoop();
  }, [gameState]);

  return (
    <div className="game-container">
      <canvas
        ref={canvasRef}
        width={800}
        height={600}
        style={{ border: '1px solid black' }}
      />
    </div>
  );
};

export default Game;