// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "./RewardEngine.sol";
import "./PlayerProfile.sol";

contract GameRouter is Ownable {
    struct Match {
        address playerA;
        address playerB;
        uint8  scoreA;
        uint8  scoreB;
        bool   active;
    }

    uint256 public entryFee;
    RewardEngine    public rewardEngine;
    PlayerProfile   public profileContract;
    mapping(uint256 => Match) public matches;
    mapping(address => bool)  public hasDeposited;
    uint256 public nextMatchId;

    event Deposited(address indexed player, uint256 amount);
    event MatchStarted(uint256 indexed matchId, address playerA, address playerB);
    event MatchEnded(uint256 indexed matchId, address winner, uint8 scoreA, uint8 scoreB);

    constructor(
        uint256 _entryFee,
        address _rewardEngine,
        address _profileContract
    ) {
        entryFee        = _entryFee;
        rewardEngine    = RewardEngine(_rewardEngine);
        profileContract = PlayerProfile(_profileContract);
    }

    /// @notice Player deposits the entry fee to participate in the next match
    function deposit() external payable {
        require(msg.value == entryFee,           "GameRouter: incorrect entry fee");
        require(!hasDeposited[msg.sender],       "GameRouter: already deposited");
        hasDeposited[msg.sender] = true;
        emit Deposited(msg.sender, msg.value);
    }

    /// @notice Owner pairs two deposited players and starts the match
    function startMatch(address _playerA, address _playerB)
        external
        onlyOwner
        returns (uint256)
    {
        require(
            hasDeposited[_playerA] && hasDeposited[_playerB],
            "GameRouter: both players must deposit"
        );

        uint256 matchId = nextMatchId++;
        matches[matchId] = Match({
            playerA: _playerA,
            playerB: _playerB,
            scoreA:  0,
            scoreB:  0,
            active:  true
        });

        // reset deposit flags so they have to re-deposit for next match
        hasDeposited[_playerA] = false;
        hasDeposited[_playerB] = false;

        emit MatchStarted(matchId, _playerA, _playerB);
        return matchId;
    }

    /// @notice Owner ends a match, records result, updates profiles, and triggers payouts
    function endMatch(
        uint256 _matchId,
        uint8   _scoreA,
        uint8   _scoreB
    ) external onlyOwner {
        Match storage m = matches[_matchId];
        require(m.active, "GameRouter: match not active");

        m.scoreA = _scoreA;
        m.scoreB = _scoreB;
        m.active = false;

        // determine winner (ties go to playerA by default)
        address winner = _scoreA >= _scoreB ? m.playerA : m.playerB;

        // update on‐chain player stats
        profileContract.recordResult(
            m.playerA,
            m.playerB,
            _scoreA,
            _scoreB
        );

        // payout entry‐fee pool to winner
        // Assumes contract balance == 2 * entryFee
        rewardEngine.payout{ value: address(this).balance }(winner);

        emit MatchEnded(_matchId, winner, _scoreA, _scoreB);
    }

    /// @notice Allow receiving ETH refunds or forced sends
    receive() external payable {}
}