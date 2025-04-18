# Gala-Baishi Integration

This module integrates our 8-ball-pool AI agent with Gala Chain, handling match routing, player profiles, rewards and on-chain bridging.

## 📦 Folder Structure

Gala-Baishi-Integration/
├── config/
│ └── galaConfig.json ← RPC URL, chain ID, keys
├── contracts/ ← Solidity sources
├── scripts/ ← JS deploy/configure/simulation
├── tests/ ← Contract test suite
├── abi/ ← Generated ABIs
├── mockdata/ ← Fake players & match history
└── utils/ ← Logging, randomizers, verifiers

## 🚀 Getting Started

1. **Install dependencies**
   ```bash
   cd Gala-Baishi-Integration
   npm install @gala-chain/api @gala-chain/connect ethers
   ```
