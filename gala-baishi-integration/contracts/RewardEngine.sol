// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";

contract RewardEngine is Ownable {
    event Payout(address indexed winner, uint256 amount);

    /// @notice Pays out the full contract balance (sent as msg.value) to the winner
    /// @param winner The address to receive the rewards
    function payout(address winner) external payable onlyOwner {
        require(msg.value > 0, "RewardEngine: zero payout");

        (bool success, ) = winner.call{ value: msg.value }("");
        require(success, "RewardEngine: payout failed");

        emit Payout(winner, msg.value);
    }
}