const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("GalaBaishiBridge", function () {
  let token, bridge;
  let owner, user, other;
  const initialSupply = ethers.utils.parseEther("1000");
  const bridgeAmount = ethers.utils.parseEther("50");

  beforeEach(async function () {
    [owner, user, other] = await ethers.getSigners();

    // Deploy an ERC20 preset so we can mint & transfer
    const ERC20 = await ethers.getContractFactory("ERC20PresetMinterPauser");
    token = await ERC20.connect(owner).deploy("TestToken", "TTK");
    await token.deployed();

    // Mint tokens to owner, then transfer to user
    await token.connect(owner).mint(owner.address, initialSupply);
    await token.connect(owner).transfer(user.address, bridgeAmount);

    // Deploy the bridge contract
    const Bridge = await ethers.getContractFactory("GalaBaishiBridge");
    bridge = await Bridge.connect(owner).deploy(token.address);
    await bridge.deployed();

    // User approves the bridge contract
    await token.connect(user).approve(bridge.address, bridgeAmount);
  });

  it("bridges assets and emits GameAssetBridged", async function () {
    const gameId = 42;
    await expect(
      bridge.connect(user).bridgeAsset(gameId, bridgeAmount)
    )
      .to.emit(bridge, "GameAssetBridged")
      .withArgs(user.address, gameId, bridgeAmount);

    // Bridge contract should hold the tokens
    const bal = await token.balanceOf(bridge.address);
    expect(bal).to.equal(bridgeAmount);
  });

  it("reverts when trying to bridge zero amount", async function () {
    await expect(
      bridge.connect(user).bridgeAsset(1, 0)
    ).to.be.revertedWith("GalaBaishiBridge: amount must be > 0");
  });

  it("allows owner to withdraw tokens", async function () {
    // First bridge some tokens
    await bridge.connect(user).bridgeAsset(7, bridgeAmount);
    // Owner withdraws to `other`
    await expect(
      bridge.connect(owner).withdrawTokens(other.address, bridgeAmount)
    ).to.not.be.reverted;

    // `other` now has the tokens
    expect(await token.balanceOf(other.address)).to.equal(bridgeAmount);
  });

  it("reverts withdrawTokens when called by non-owner", async function () {
    await bridge.connect(user).bridgeAsset(3, bridgeAmount);
    await expect(
      bridge.connect(user).withdrawTokens(user.address, bridgeAmount)
    ).to.be.revertedWith("Ownable: caller is not the owner");
  });
});