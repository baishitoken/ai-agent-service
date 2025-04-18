const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("GameRouter – full game flow", function () {
  let GameRouter, RewardEngine, PlayerProfile;
  let router, reward, profile;
  let owner, playerA, playerB;

  const ENTRY_FEE = ethers.utils.parseEther("0.01");

  beforeEach(async function () {
    [owner, playerA, playerB, ...addrs] = await ethers.getSigners();

    // Deploy RewardEngine and PlayerProfile
    const RE = await ethers.getContractFactory("RewardEngine");
    reward = await RE.connect(owner).deploy();
    await reward.deployed();

    const PP = await ethers.getContractFactory("PlayerProfile");
    profile = await PP.connect(owner).deploy();
    await profile.deployed();

    // Deploy GameRouter with entry fee and addresses
    const GR = await ethers.getContractFactory("GameRouter");
    router = await GR.connect(owner).deploy(
      ENTRY_FEE,
      reward.address,
      profile.address
    );
    await router.deployed();

    // fund router so it can forward ETH
    await owner.sendTransaction({ to: router.address, value: ENTRY_FEE.mul(2) });
  });

  it("allows two players to deposit and start/end a match with correct payout", async function () {
    // Players deposit
    await router.connect(playerA).deposit({ value: ENTRY_FEE });
    await router.connect(playerB).deposit({ value: ENTRY_FEE });

    // Check deposit flags
    expect(await router.hasDeposited(playerA.address)).to.be.true;
    expect(await router.hasDeposited(playerB.address)).to.be.true;

    // Start match
    await expect(router.connect(owner).startMatch(playerA.address, playerB.address))
      .to.emit(router, "MatchStarted")
      .withArgs(0, playerA.address, playerB.address);

    // End match with A as winner (scoreA >= scoreB)
    await expect(router.connect(owner).endMatch(0, 8, 5))
      .to.emit(router, "MatchEnded")
      .withArgs(0, playerA.address, 8, 5);

    // Verify profiles updated
    const statsA = await profile.getStats(playerA.address);
    const statsB = await profile.getStats(playerB.address);
    expect(statsA.wins).to.equal(1);
    expect(statsB.losses).to.equal(1);
  });

  it("reverts if non-owner tries to start or end a match", async function () {
    await router.connect(playerA).deposit({ value: ENTRY_FEE });
    await router.connect(playerB).deposit({ value: ENTRY_FEE });

    await expect(
      router.connect(playerA).startMatch(playerA.address, playerB.address)
    ).to.be.revertedWith("Ownable: caller is not the owner");

    // fund, start match properly, then test endMatch revert
    await router.connect(owner).startMatch(playerA.address, playerB.address);
    await expect(
      router.connect(playerA).endMatch(0, 7, 8)
    ).to.be.revertedWith("Ownable: caller is not the owner");
  });
});
js
Kopiér
Rediger
