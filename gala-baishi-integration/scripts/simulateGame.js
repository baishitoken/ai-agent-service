import configureNetwork from './configureNetwork.js';
import { pickTwoPlayers, pickWinner, randomScore } from '../utils/randomUtils.js';
import fakePlayers from '../mockdata/fakePlayers.json';
import GameRouterArtifact from '../abi/GameRouter.json';
import RewardEngineArtifact from '../abi/RewardEngine.json';

async function simulateGame() {
  const client = await configureNetwork();

  const { abi: routerAbi, bytecode: routerBytecode } = GameRouterArtifact;
  const { abi: rewardAbi } = RewardEngineArtifact;

  const routerAddress = process.env.GAMEROUTER_ADDRESS;
  const rewardAddress = process.env.REWARDENGINE_ADDRESS;

  const gameRouter = new client.Contract(routerAbi, routerAddress);
  const rewardEngine = new client.Contract(rewardAbi, rewardAddress);

  const [playerA, playerB] = pickTwoPlayers(fakePlayers);
  console.log(`🎮 Matching: ${playerA.address} vs ${playerB.address}`);

  const entryFee = client.utils.parseUnits('0.1', 'ether');
  await gameRouter.connect(playerA.signer).deposit({ value: entryFee });
  await gameRouter.connect(playerB.signer).deposit({ value: entryFee });

  const txStart = await gameRouter.startMatch(playerA.address, playerB.address);
  await txStart.wait();
  console.log('🏁 Match started');

  const [scoreA, scoreB] = [randomScore(), randomScore()];
  const winner = pickWinner(playerA, playerB, scoreA, scoreB);
  console.log(`🏆 Winner: ${winner.address} (${scoreA}–${scoreB})`);

  const txEnd = await gameRouter.endMatch(
    playerA.address,
    playerB.address,
    scoreA,
    scoreB
  );
  await txEnd.wait();

  const txReward = await rewardEngine
    .connect(client.signer)
    .payout(winner.address);
  await txReward.wait();
  console.log(`💰 Reward paid out to ${winner.address}`);
}

simulateGame().catch(err => {
  console.error('❌ Simulation failed:', err);
  process.exit(1);
});