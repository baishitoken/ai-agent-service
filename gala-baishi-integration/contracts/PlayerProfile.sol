// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";

contract PlayerProfile is Ownable {
    struct Stats {
        uint256 wins;
        uint256 losses;
        uint256 draws;
        uint256 totalMatches;
    }

    mapping(address => Stats) public stats;

    event ProfileUpdated(
        address indexed player,
        uint256 wins,
        uint256 losses,
        uint256 draws,
        uint256 totalMatches
    );

    /// @notice Called by GameRouter (owner) to record the outcome of a match
    function recordResult(
        address playerA,
        address playerB,
        uint8   scoreA,
        uint8   scoreB
    ) external onlyOwner {
        Stats storage a = stats[playerA];
        Stats storage b = stats[playerB];

        if (scoreA > scoreB) {
            a.wins++;
            b.losses++;
        } else if (scoreB > scoreA) {
            b.wins++;
            a.losses++;
        } else {
            a.draws++;
            b.draws++;
        }

        a.totalMatches++;
        b.totalMatches++;

        emit ProfileUpdated(
            playerA,
            a.wins,
            a.losses,
            a.draws,
            a.totalMatches
        );
        emit ProfileUpdated(
            playerB,
            b.wins,
            b.losses,
            b.draws,
            b.totalMatches
        );
    }

    /// @notice Fetch a player’s stats in one call
    function getStats(address player)
        external
        view
        returns (
            uint256 wins,
            uint256 losses,
            uint256 draws,
            uint256 totalMatches
        )
    {
        Stats storage s = stats[player];
        return (s.wins, s.losses, s.draws, s.totalMatches);
    }
}