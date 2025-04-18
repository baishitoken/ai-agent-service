/**
 * Pick two distinct random players from an array.
 * Each player object should include { address, signer }.
 */
export function pickTwoPlayers(players) {
  if (players.length < 2) {
    throw new Error('Not enough players to pick a match');
  }
  const shuffled = players.sort(() => 0.5 - Math.random());
  return [shuffled[0], shuffled[1]];
}

/**
 * Generate a random 8-ball pool–style score (0–7).
 */
export function randomScore() {
  // In 8-ball, first to 8 wins; scores up to 7 for loser
  return Math.floor(Math.random() * 8);
}

/**
 * Determine winner based on scores; returns one of the two player objects.
 */
export function pickWinner(playerA, playerB, scoreA, scoreB) {
  if (scoreA === scoreB) {
    // Tie-breaker: random
    return Math.random() > 0.5 ? playerA : playerB;
  }
  return scoreA > scoreB ? playerA : playerB;
}