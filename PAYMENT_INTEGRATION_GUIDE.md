# 💰 SBC Payment Integration Guide

## 🎯 Goal
Add blockchain payment functionality from the gasless-transaction repo to your CodeCollab Swarm app.

---

## ⚡ Quick Start (30 Minutes)

### Step 1: Fix npm Permissions (1 minute)

Run this command in your terminal:
```bash
sudo chown -R $(id -u):$(id -g) "$HOME/.npm"
```

Enter your password when prompted.

---

### Step 2: Install Dependencies (2 minutes)

```bash
cd /Users/nithinkamavaram/Desktop/Hackathon/frontend

# Install SBC blockchain payment dependencies
npm install @stablecoin.xyz/core@^1.3.0 \
            @stablecoin.xyz/react@^0.5.1 \
            viem@^2.38.0 \
            --legacy-peer-deps
```

**What these do:**
- `@stablecoin.xyz/core`: Core SBC SDK for gasless transactions
- `@stablecoin.xyz/react`: React hooks for wallet connection
- `viem`: Ethereum library for blockchain interactions

---

### Step 3: Create Environment Variables (1 minute)

Create `frontend/.env`:
```bash
cd /Users/nithinkamavaram/Desktop/Hackathon/frontend
cat > .env << 'EOF'
# SBC Payment Configuration
REACT_APP_SBC_API_KEY=sbc-73d2b0b2ffa7117d6fdd4c5282a95f7c
REACT_APP_PAYMENT_RECIPIENT=0x97fd851453E04e70D290E922e6A72D34a28AC331
REACT_APP_RPC_URL=https://base-rpc.publicnode.com

# Base Chain Explorer
REACT_APP_CHAIN_EXPLORER=https://basescan.org
EOF
```

**What these mean:**
- `SBC_API_KEY`: Your SBC SDK key for gasless transactions
- `PAYMENT_RECIPIENT`: Platform wallet address that receives payments
- `RPC_URL`: Base blockchain RPC endpoint
- `CHAIN_EXPLORER`: Block explorer for viewing transactions

---

### Step 4: Copy Payment Integration Files (5 minutes)

I'll create the payment integration files for you. These add:
- ✅ Wallet connection (MetaMask)
- ✅ Automatic payment after task completion
- ✅ Gasless transactions using SBC tokens
- ✅ ERC20 permit signatures

The files will be created in the next step.

---

### Step 5: Update Your Current App (20 minutes)

#### A. Update `frontend/src/App.jsx`

Your current App.jsx needs minimal changes:

1. **Add imports at the top:**
```javascript
import { SbcProvider, WalletButton, useSbcApp, useUserOperation } from '@stablecoin.xyz/react';
import { base } from 'viem/chains';
import { createPublicClient, http, parseUnits, encodeFunctionData } from 'viem';
```

2. **Wrap your app with SbcProvider** (in the default export):
```javascript
import React from 'react';
import { SbcProvider } from '@stablecoin.xyz/react';
import { base } from 'viem/chains';

// Your existing imports and components...

function App() {
  // Your existing app code
  return (
    <div className="app">
      {/* Your existing JSX */}
    </div>
  );
}

// Wrap with payment provider
export default function AppWithPayments() {
  const sbcConfig = {
    apiKey: process.env.REACT_APP_SBC_API_KEY || 'sbc-73d2b0b2ffa7117d6fdd4c5282a95f7c',
    chain: base,
    rpcUrl: process.env.REACT_APP_RPC_URL,
    wallet: 'auto',
    debug: true,
    walletOptions: { autoConnect: false },
  };

  return (
    <SbcProvider config={sbcConfig}>
      <App />
    </SbcProvider>
  );
}
```

3. **Add wallet connection button** (in your header):
```javascript
import { WalletButton, useSbcApp } from '@stablecoin.xyz/react';

function App() {
  const { ownerAddress, disconnectWallet } = useSbcApp();

  return (
    <header className="app-header">
      <h1>CodeCollab Swarm</h1>

      {/* Add this wallet button */}
      {!ownerAddress ? (
        <WalletButton
          walletType="auto"
          render={({ onClick, isConnecting }) => (
            <button onClick={onClick} disabled={isConnecting}>
              {isConnecting ? 'Connecting...' : 'Connect Wallet'}
            </button>
          )}
        />
      ) : (
        <div>
          <span>Connected: {ownerAddress.slice(0, 6)}...{ownerAddress.slice(-4)}</span>
          <button onClick={disconnectWallet}>Disconnect</button>
        </div>
      )}
    </header>
  );
}
```

4. **Add automatic payment logic** (as a useEffect):
```javascript
import { useUserOperation } from '@stablecoin.xyz/react';
import { parseUnits, encodeFunctionData } from 'viem';

function App() {
  const { ownerAddress, account, sbcAppKit } = useSbcApp();
  const { sendUserOperation, isLoading: isPaymentLoading, isSuccess: isPaymentSuccess } = useUserOperation();

  const [currentResult, setCurrentResult] = useState(null);
  const paymentTriggeredRef = useRef(null);

  // Auto-trigger payment when result with payment info appears
  useEffect(() => {
    if (!currentResult?.payment || currentResult.payment.amount <= 0) return;
    if (!ownerAddress || !account) return;

    const resultId = `${currentResult.task_description}_${currentResult.payment.amount}`;
    if (paymentTriggeredRef.current === resultId) return;

    paymentTriggeredRef.current = resultId;

    // Trigger payment after 1 second
    setTimeout(() => {
      handlePayment(currentResult.payment.amount);
    }, 1000);
  }, [currentResult, ownerAddress, account]);

  const handlePayment = async (amount) => {
    // Payment implementation (see next section)
  };

  // Your existing code...
}
```

---

## 🔐 Payment Implementation

Create a new file `frontend/src/utils/payment.js`:

```javascript
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

export async function processPayment({
  amount,
  ownerAddress,
  accountAddress,
  walletClient,
  sendUserOperation,
  recipientAddress
}) {
  const publicClient = createPublicClient({
    chain: base,
    transport: http(process.env.REACT_APP_RPC_URL || "https://base-rpc.publicnode.com")
  });

  const owner = getAddress(ownerAddress);
  const spender = getAddress(accountAddress);
  const recipient = getAddress(recipientAddress);
  const value = parseUnits(amount.toFixed(6), SBC_DECIMALS);
  const deadline = Math.floor(Date.now() / 1000) + 60 * 30; // 30 minutes

  // Step 1: Get nonce
  const nonce = await publicClient.readContract({
    address: SBC_TOKEN_ADDRESS,
    abi: erc20Abi,
    functionName: 'nonces',
    args: [owner],
  });

  // Step 2: Get token name
  const tokenName = await publicClient.readContract({
    address: SBC_TOKEN_ADDRESS,
    abi: erc20Abi,
    functionName: 'name',
  });

  // Step 3: Create EIP-712 signature
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
  const signature = await walletClient.signTypedData({
    account: owner,
    domain,
    types,
    primaryType: 'Permit',
    message,
  });

  // Step 5: Parse signature
  const r = `0x${signature.slice(2, 66)}`;
  const s = `0x${signature.slice(66, 130)}`;
  const v = parseInt(signature.slice(130, 132), 16);

  // Step 6: Create permit call
  const permitCallData = encodeFunctionData({
    abi: erc20Abi,
    functionName: 'permit',
    args: [owner, spender, value, deadline, v, r, s],
  });

  // Step 7: Create transferFrom call
  const transferCallData = encodeFunctionData({
    abi: erc20Abi,
    functionName: 'transferFrom',
    args: [owner, recipient, value],
  });

  // Step 8: Send gasless transaction
  const result = await sendUserOperation({
    calls: [
      { to: SBC_TOKEN_ADDRESS, data: permitCallData },
      { to: SBC_TOKEN_ADDRESS, data: transferCallData },
    ],
  });

  return result;
}
```

---

## 📦 What You Get

After integration, your app will have:

1. **🔐 Wallet Connection**
   - MetaMask integration
   - Shows connected address
   - Disconnect functionality

2. **💰 Automatic Payments**
   - After AI completes task → MetaMask opens automatically
   - User signs permit (no gas needed)
   - Platform receives SBC tokens

3. **⛽ Gasless Transactions**
   - Users don't need ETH for gas
   - SBC SDK covers gas fees
   - ERC-2612 permit signatures

4. **🔍 Transaction Tracking**
   - Transaction hashes displayed
   - Links to BaseScan explorer
   - Payment status feedback

---

## 🧪 Testing

1. **Start the app:**
```bash
cd /Users/nithinkamavaram/Desktop/Hackathon/frontend
npm start
```

2. **Connect wallet:**
   - Click "Connect Wallet"
   - Approve in MetaMask
   - Should show connected address

3. **Submit AI task:**
   - Enter task description
   - Submit
   - Wait for result with payment info

4. **Payment flow:**
   - After 1 second → MetaMask opens
   - Sign permit
   - Transaction sends
   - See confirmation + TX hash

---

## 🎬 For Video Demo

When recording, highlight:

1. **Show wallet connection**
   - "First I connect my MetaMask wallet"
   - Point to connected address

2. **Submit task**
   - "I submit an LRU Cache implementation task"

3. **Automatic payment**
   - "When results appear, payment triggers automatically"
   - "MetaMask opens for signature"
   - "No gas fees needed!"

4. **Transaction confirmation**
   - "Payment sent! Here's the transaction hash"
   - Click link to BaseScan

---

## 🚨 Troubleshooting

### Issue: npm install fails
**Solution:**
```bash
sudo chown -R $(id -u):$(id -g) "$HOME/.npm"
npm cache clean --force
npm install --legacy-peer-deps
```

### Issue: Wallet doesn't connect
**Solution:**
- Make sure MetaMask is installed
- Switch to Base Mainnet in MetaMask
- Check console for errors

### Issue: Payment doesn't trigger
**Solution:**
- Check wallet is connected (`ownerAddress` exists)
- Check `currentResult.payment.amount > 0`
- Check console logs for errors

### Issue: Signature fails
**Solution:**
- Make sure user has SBC tokens
- Check deadline hasn't expired
- Verify network is Base Mainnet (chain ID 8453)

---

## 📝 Commit & Push

After integration works:

```bash
cd /Users/nithinkamavaram/Desktop/Hackathon

# Add all changes
git add .

# Commit
git commit -m "feat: integrate SBC blockchain payment system

- Added @stablecoin.xyz SDK for gasless transactions
- Implemented automatic payment after AI task completion
- Added MetaMask wallet connection
- Integrated ERC20 permit signatures for gasless payments
- Payment flows automatically when results display
- Supports Base Mainnet with BaseScan explorer links

This completes the payment integration from gasless-transaction repo"

# Push to feature branch
git push origin feature/codecollab-swarm-implementation

# Merge to main
git checkout main
git merge feature/codecollab-swarm-implementation
git push origin main
```

---

## ✅ Done!

Your app now has:
- ✅ Blockchain wallet connection
- ✅ Automatic micropayments
- ✅ Gasless transactions
- ✅ Transaction explorer links
- ✅ Ready for hackathon demo!

**Next:** Record your video and submit! 🎥🚀
