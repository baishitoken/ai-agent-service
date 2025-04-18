import configureNetwork from './configureNetwork.js';
import GameRouterArtifact from '../abi/GameRouter.json';

async function deploy() {
  const client = await configureNetwork();

  const { abi, bytecode } = GameRouterArtifact;
  const factory = new client.ContractFactory(abi, bytecode);
  
  const contract = await factory.deploy();
  console.log(`🚀 Deployed GameRouter at ${contract.address}`);
}

deploy().catch(err => {
  console.error('❌ Deployment failed:', err);
  process.exit(1);
});