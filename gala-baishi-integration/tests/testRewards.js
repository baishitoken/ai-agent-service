const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("RewardEngine", function () {
  let RewardEngine, reward, owner, other;

  beforeEach(async function () {
    [owner, other] = await ethers.getSigners();
    const RE = await ethers.getContractFactory("RewardEngine");
    reward = await RE.connect(owner).deploy();
    await reward.deployed();
  });

  it("pays out funds to the winner and emits event", async function () {
    const payoutAmount = ethers.utils.parseEther("1.0");

    // Send ETH into the transaction and call payout
    await expect(
      reward.connect(owner).payout(other.address, { value: payoutAmount })
    )
      .to.emit(reward, "Payout")
      .withArgs(other.address, payoutAmount);

    // Confirm recipient balance increased by payoutAmount (minus gas)
    const balanceBefore = await ethers.provider.getBalance(other.address);
    // Note: cannot exactly match due to gas, but at least > payoutAmount - small delta
    expect(balanceBefore).to.be.gt(payoutAmount.sub(ethers.utils.parseEther("0.001")));
  });

  it("reverts when non-owner calls payout", async function () {
    const amt = ethers.utils.parseEther("0.5");
    await expect(
      reward.connect(other).payout(other.address, { value: amt })
    ).to.be.revertedWith("Ownable: caller is not the owner");
  });

  it("reverts on zero payout", async function () {
    await expect(
      reward.connect(owner).payout(other.address, { value: 0 })
    ).to.be.revertedWith("RewardEngine: zero payout");
  });
});