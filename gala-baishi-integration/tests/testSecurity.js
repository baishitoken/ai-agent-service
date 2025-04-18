const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("GameRouter Security & Access Control", function () {
  let GameRouter, RewardEngine, PlayerProfile;
  let router, reward, profile;
  let owner, playerA, playerB, other;
  const ENTRY_FEE = ethers.utils.parseEther("0.01");

  beforeEach(async function () {
    [owner, playerA, playerB, other] = await ethers.getSigners();

    // Deploy RewardEngine & PlayerProfile
    RewardEngine = await ethers.getContractFactory("RewardEngine");
    reward = await RewardEngine.connect(owner).deploy();
    await reward.deployed();

    PlayerProfile = await ethers.getContractFactory("PlayerProfile");
    profile = await PlayerProfile.connect(owner).deploy();
    await profile.deployed();

    // Deploy GameRouter
    GameRouter = await ethers.getContractFactory("GameRouter");
    router = await GameRouter.connect(owner).deploy(
      ENTRY_FEE,
      reward.address,
      profile.address
    );
    await router.deployed();

    // Fund router so it can payout
    await owner.sendTransaction({ to: router.address, value: ENTRY_FEE.mul(2) });
  });

  it("reverts deposit when incorrect fee is sent", async function () {
    await expect(
      router.connect(playerA).deposit({ value: ENTRY_FEE.div(2) })
    ).to.be.revertedWith("GameRouter: incorrect entry fee");
  });

  it("reverts on double deposit by same player", async function () {
    await router.connect(playerA).deposit({ value: ENTRY_FEE });
    await expect(
      router.connect(playerA).deposit({ value: ENTRY_FEE })
    ).to.be.revertedWith("GameRouter: already deposited");
  });

  it("reverts startMatch if players haven't deposited", async function () {
    // No deposits at all
    await expect(
      router.connect(owner).startMatch(playerA.address, playerB.address)
    ).to.be.revertedWith("GameRouter: both players must deposit");
  });

  it("reverts startMatch when called by non-owner", async function () {
    await router.connect(playerA).deposit({ value: ENTRY_FEE });
    await router.connect(playerB).deposit({ value: ENTRY_FEE });
    await expect(
      router.connect(other).startMatch(playerA.address, playerB.address)
    ).to.be.revertedWith("Ownable: caller is not the owner");
  });

  it("reverts endMatch when match is not active", async function () {
    // Start and immediately end a match
    await router.connect(playerA).deposit({ value: ENTRY_FEE });
    await router.connect(playerB).deposit({ value: ENTRY_FEE });
    await router.connect(owner).startMatch(playerA.address, playerB.address);
    await router.connect(owner).endMatch(0, 5, 8);

    // Attempting to end again should revert
    await expect(
      router.connect(owner).endMatch(0, 6, 7)
    ).to.be.revertedWith("GameRouter: match not active");
  });

  it("reverts endMatch when called by non-owner", async function () {
    await router.connect(playerA).deposit({ value: ENTRY_FEE });
    await router.connect(playerB).deposit({ value: ENTRY_FEE });
    await router.connect(owner).startMatch(playerA.address, playerB.address);
    await expect(
      router.connect(other).endMatch(0, 8, 3)
    ).to.be.revertedWith("Ownable: caller is not the owner");
  });
});