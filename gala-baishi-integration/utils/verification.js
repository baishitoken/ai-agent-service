import { ethers } from 'ethers';

/**
 * Verifies that a given signature was produced by the holder of `expectedAddress`.
 *
 * @param {string} message      - The original message that was signed.
 * @param {string} signature    - The signature string.
 * @param {string} expectedAddress - The address you expect signed it.
 * @returns {boolean}           - True if valid, false otherwise.
 */
export function verifySignature(message, signature, expectedAddress) {
  // Recreate the message hash that was signed
  const messageHash = ethers.utils.hashMessage(message);
  // Recover the address that signed this message
  const recoveredAddress = ethers.utils.recoverAddress(messageHash, signature);
  return recoveredAddress.toLowerCase() === expectedAddress.toLowerCase();
}

/**
 * Ensures a transaction receipt indicates success.
 *
 * @param {object} receipt - A transaction receipt object.
 * @throws {Error}         - If the status is not 1 (success).
 */
export function assertTxSuccess(receipt) {
  if (receipt.status !== 1) {
    throw new Error(`Transaction failed (status=${receipt.status}).`);
  }
}