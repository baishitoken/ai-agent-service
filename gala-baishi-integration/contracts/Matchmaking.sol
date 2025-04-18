// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";

contract Matchmaking is Ownable {
    address[] private queue;
    mapping(address => bool) public inQueue;

    event PlayerEnqueued(address indexed player);
    event PlayersMatched(address indexed playerA, address indexed playerB);

    /// @notice Join the matchmaking queue
    function joinQueue() external {
        require(!inQueue[msg.sender], "Matchmaking: already in queue");
        queue.push(msg.sender);
        inQueue[msg.sender] = true;
        emit PlayerEnqueued(msg.sender);

        // Auto-match when at least two players are waiting
        if (queue.length >= 2) {
            address playerA = queue[0];
            address playerB = queue[1];
            _removeAtIndex(1);
            _removeAtIndex(0);
            emit PlayersMatched(playerA, playerB);
        }
    }

    /// @notice View current queue
    function getQueue() external view returns (address[] memory) {
        return queue;
    }

    /// @dev Remove a player from queue by index (order: remove higher index first)
    function _removeAtIndex(uint256 index) internal {
        address toRemove = queue[index];
        inQueue[toRemove] = false;

        // Move last element into the slot to delete and pop
        queue[index] = queue[queue.length - 1];
        queue.pop();
    }
}
solidity
Kopiér
Rediger
// contracts/GalaBaishiBridge.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract GalaBaishiBridge is Ownable {
    IERC20 public immutable token;

    event GameAssetBridged(address indexed user, uint256 indexed gameId, uint256 amount);

    /// @param _token Address of the ERC-20 token used for in-game assets or fees
    constructor(address _token) {
        token = IERC20(_token);
    }

    /// @notice Locks tokens on this chain and emits an event for an off-chain relayer
    /// @param gameId  The ID of the game or asset being bridged
    /// @param amount  The amount of tokens to bridge
    function bridgeAsset(uint256 gameId, uint256 amount) external {
        require(amount > 0, "GalaBaishiBridge: amount must be > 0");
        require(token.transferFrom(msg.sender, address(this), amount), "GalaBaishiBridge: transfer failed");
        emit GameAssetBridged(msg.sender, gameId, amount);
    }

    /// @notice Allows the owner (relayer) to withdraw tokens back out
    function withdrawTokens(address to, uint256 amount) external onlyOwner {
        require(token.transfer(to, amount), "GalaBaishiBridge: withdraw failed");
    }
}