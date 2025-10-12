/**
 * SBC Payment Utility
 * Handles gasless blockchain payments using ERC20 permit signatures
 */

import { parseUnits, encodeFunctionData, getAddress, createPublicClient, http } from 'viem';
import { base } from 'viem/chains';

const SBC_TOKEN_ADDRESS = '0xfdcC3dd6671eaB0709A4C0f3F53De9a333d80798';
const SBC_DECIMALS = 18;

const erc20Abi = [
  {
    "inputs": [
      { "name": "owner", "type": "address" },
      { "name": "spender", "type": "address" },
      { "name": "value", "type": "uint256" },
      { "name": "deadline", "type": "uint256" },
      { "name": "v", "type": "uint8" },
      { "name": "r", "type": "bytes32" },
      { "name": "s", "type": "bytes32" }
    ],
    "name": "permit",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      { "name": "from", "type": "address" },
      { "name": "to", "type": "address" },
      { "name": "amount", "type": "uint256" }
    ],
    "name": "transferFrom",
    "outputs": [{ "name": "", "type": "bool" }],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [{ "name": "owner", "type": "address" }],
    "name": "nonces",
    "outputs": [{ "name": "", "type": "uint256" }],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "name",
    "outputs": [{ "name": "", "type": "string" }],
    "stateMutability": "view",
    "type": "function"
  }
];

/**
 * Process a gasless payment using SBC tokens
 * @param {Object} params Payment parameters
 * @param {number} params.amount - Amount in USD to pay
 * @param {string} params.ownerAddress - User's wallet address
 * @param {string} params.accountAddress - Smart account address
 * @param {Object} params.walletClient - Viem wallet client
 * @param {Function} params.sendUserOperation - SBC SDK function to send transaction
 * @param {string} params.recipientAddress - Platform address to receive payment
 * @returns {Promise<Object>} Transaction result
 */
export async function processPayment({
  amount,
  ownerAddress,
  accountAddress,
  walletClient,
  sendUserOperation,
  recipientAddress
}) {
  console.log('🚀 Processing payment:', { amount, from: ownerAddress, to: recipientAddress });

  const publicClient = createPublicClient({
    chain: base,
    transport: http(process.env.REACT_APP_RPC_URL || "https://base-rpc.publicnode.com")
  });

  const owner = getAddress(ownerAddress);
  const spender = getAddress(accountAddress);
  const recipient = getAddress(recipientAddress);
  const value = parseUnits(amount.toFixed(6), SBC_DECIMALS);
  const deadline = Math.floor(Date.now() / 1000) + 60 * 30; // 30 minutes

  console.log('📝 Payment details:', {
    owner,
    spender,
    recipient,
    value: value.toString(),
    deadline: new Date(deadline * 1000).toISOString()
  });

  // Step 1: Get current nonce for permit signature
  console.log('1️⃣ Getting nonce...');
  const nonce = await publicClient.readContract({
    address: SBC_TOKEN_ADDRESS,
    abi: erc20Abi,
    functionName: 'nonces',
    args: [owner],
  });
  console.log('✅ Nonce:', nonce.toString());

  // Step 2: Get token name for EIP-712 domain
  console.log('2️⃣ Getting token name...');
  const tokenName = await publicClient.readContract({
    address: SBC_TOKEN_ADDRESS,
    abi: erc20Abi,
    functionName: 'name',
  });
  console.log('✅ Token name:', tokenName);

  // Step 3: Create EIP-712 typed data for permit
  const domain = {
    name: tokenName,
    version: '1',
    chainId: BigInt(base.id),
    verifyingContract: SBC_TOKEN_ADDRESS,
  };

  const types = {
    Permit: [
      { name: 'owner', type: 'address' },
      { name: 'spender', type: 'address' },
      { name: 'value', type: 'uint256' },
      { name: 'nonce', type: 'uint256' },
      { name: 'deadline', type: 'uint256' },
    ],
  };

  const message = {
    owner,
    spender,
    value,
    nonce,
    deadline: BigInt(deadline),
  };

  // Step 4: Request signature from user's wallet
  console.log('3️⃣ Requesting permit signature from wallet...');
  const signature = await walletClient.signTypedData({
    account: owner,
    domain,
    types,
    primaryType: 'Permit',
    message,
  });
  console.log('✅ Signature received');

  // Step 5: Parse signature into r, s, v components
  const r = `0x${signature.slice(2, 66)}`;
  const s = `0x${signature.slice(66, 130)}`;
  const v = parseInt(signature.slice(130, 132), 16);

  // Step 6: Encode permit function call
  console.log('4️⃣ Encoding permit call...');
  const permitCallData = encodeFunctionData({
    abi: erc20Abi,
    functionName: 'permit',
    args: [owner, spender, value, deadline, v, r, s],
  });

  // Step 7: Encode transferFrom function call
  console.log('5️⃣ Encoding transferFrom call...');
  const transferCallData = encodeFunctionData({
    abi: erc20Abi,
    functionName: 'transferFrom',
    args: [owner, recipient, value],
  });

  // Step 8: Send gasless transaction (permit + transferFrom)
  console.log('6️⃣ Sending gasless transaction...');
  const result = await sendUserOperation({
    calls: [
      { to: SBC_TOKEN_ADDRESS, data: permitCallData },
      { to: SBC_TOKEN_ADDRESS, data: transferCallData },
    ],
  });

  console.log('✅ Payment successful!', result);
  return result;
}

/**
 * Convert USD amount to SBC token amount
 * Assumes 1 SBC = 1 USD for simplicity
 * @param {number} usdAmount - Amount in USD
 * @returns {bigint} Amount in SBC wei (18 decimals)
 */
export function usdToSbc(usdAmount) {
  return parseUnits(usdAmount.toFixed(6), SBC_DECIMALS);
}

/**
 * Format address for display (0x1234...5678)
 * @param {string} address - Full address
 * @returns {string} Formatted address
 */
export function formatAddress(address) {
  if (!address) return '';
  return `${address.slice(0, 6)}...${address.slice(-4)}`;
}
