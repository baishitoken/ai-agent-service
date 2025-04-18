import { ChainClient } from '@gala-chain/api';
import { LocalWallet } from '@gala-chain/connect';
import galaConfig from '../config/galaConfig.json';

const { rpcUrl, chainId, privateKey } = galaConfig;

export default async function configureNetwork() {
  const client = new ChainClient({ rpcUrl, chainId });

  const wallet = new LocalWallet(privateKey);
  client.setSigner(wallet);

  const address = await wallet.getAddress();
  const balance = await client.getBalance(address);
  console.log(`🔗 Connected to GalaChain ${rpcUrl} (chainId=${chainId})`);
  console.log(`👤 Using address ${address} with balance ${balance}`);

  return client;
}