# ⚡ Quick Start: Add Payments in 5 Steps

## ✅ What's Ready
- ✅ Payment utility created (`frontend/src/utils/payment.js`)
- ✅ Integration guide written (`PAYMENT_INTEGRATION_GUIDE.md`)
- ✅ Timeout changes committed

---

## 🚀 Next Steps (20 Minutes)

### 1. Fix npm & Install Dependencies (3 min)

Open your terminal and run:

```bash
# Fix npm permissions
sudo chown -R $(id -u):$(id -g) "$HOME/.npm"

# Install blockchain payment dependencies
cd /Users/nithinkamavaram/Desktop/Hackathon/frontend
npm install @stablecoin.xyz/core@^1.3.0 \
            @stablecoin.xyz/react@^0.5.1 \
            viem@^2.38.0 \
            --legacy-peer-deps
```

---

### 2. Create Environment File (1 min)

```bash
cd /Users/nithinkamavaram/Desktop/Hackathon/frontend
cat > .env << 'EOF'
REACT_APP_SBC_API_KEY=sbc-73d2b0b2ffa7117d6fdd4c5282a95f7c
REACT_APP_PAYMENT_RECIPIENT=0x97fd851453E04e70D290E922e6A72D34a28AC331
REACT_APP_RPC_URL=https://base-rpc.publicnode.com
REACT_APP_CHAIN_EXPLORER=https://basescan.org
EOF
```

---

### 3. Update App.jsx with Wallet Integration (10 min)

Open `frontend/src/App.jsx` and add these changes:

#### At the top of the file:
```javascript
import { SbcProvider, WalletButton, useSbcApp, useUserOperation } from '@stablecoin.xyz/react';
import { base } from 'viem/chains';
import { processPayment } from './utils/payment';
import { useRef } from 'react';
```

#### Inside your App component:
```javascript
function App() {
  const { ownerAddress, account, sbcAppKit, disconnectWallet } = useSbcApp();
  const { sendUserOperation, isLoading: isPaymentLoading, isSuccess: isPaymentSuccess, data: paymentData } = useUserOperation();
  const paymentTriggeredRef = useRef(null);

  // Your existing state...
  const [currentResult, setCurrentResult] = useState(null);
  const [paymentStatus, setPaymentStatus] = useState('');

  // Add payment handler
  const handlePayment = async (amount) => {
    if (!account || !ownerAddress || !sbcAppKit?.walletClient) {
      setPaymentStatus('❌ Wallet not connected');
      return;
    }

    try {
      setPaymentStatus('💳 Preparing payment...');

      await processPayment({
        amount,
        ownerAddress,
        accountAddress: account.address,
        walletClient: sbcAppKit.walletClient,
        sendUserOperation,
        recipientAddress: process.env.REACT_APP_PAYMENT_RECIPIENT
      });

      setPaymentStatus('✅ Payment successful!');
    } catch (err) {
      console.error('Payment failed:', err);
      setPaymentStatus(`❌ Payment failed: ${err.message}`);
    }
  };

  // Auto-trigger payment when result appears
  useEffect(() => {
    if (!currentResult?.payment || currentResult.payment.amount <= 0) return;
    if (!ownerAddress || !account) return;

    const resultId = `${currentResult.task_description}_${currentResult.payment.amount}`;
    if (paymentTriggeredRef.current === resultId) return;

    paymentTriggeredRef.current = resultId;
    setTimeout(() => handlePayment(currentResult.payment.amount), 1000);
  }, [currentResult, ownerAddress, account]);

  // Your existing code...
}
```

#### Add wallet button in your header:
```javascript
<header className="app-header">
  <h1>🤖 CodeCollab Swarm</h1>

  {/* Add wallet button */}
  {!ownerAddress ? (
    <WalletButton
      walletType="auto"
      render={({ onClick, isConnecting }) => (
        <button
          onClick={onClick}
          disabled={isConnecting}
          style={{
            padding: '10px 20px',
            borderRadius: '8px',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            border: 'none',
            cursor: 'pointer'
          }}
        >
          {isConnecting ? 'Connecting...' : '🔗 Connect Wallet'}
        </button>
      )}
    />
  ) : (
    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
      <span style={{
        padding: '8px 16px',
        background: '#10b981',
        borderRadius: '6px',
        color: 'white'
      }}>
        ✓ {ownerAddress.slice(0, 6)}...{ownerAddress.slice(-4)}
      </span>
      <button onClick={disconnectWallet}>Disconnect</button>
    </div>
  )}
</header>
```

#### Show payment status banner:
```javascript
{paymentStatus && (
  <div style={{
    padding: '15px',
    background: paymentStatus.includes('✅') ? '#d1fae5' : '#fee2e2',
    borderRadius: '8px',
    margin: '10px 0'
  }}>
    {paymentStatus}
    {isPaymentSuccess && paymentData && (
      <a
        href={`https://basescan.org/tx/${paymentData.transactionHash}`}
        target="_blank"
        rel="noopener noreferrer"
        style={{ marginLeft: '10px', color: '#3b82f6' }}
      >
        View Transaction →
      </a>
    )}
  </div>
)}
```

#### Wrap your export with SbcProvider:
```javascript
export default function AppWithPayments() {
  const sbcConfig = {
    apiKey: process.env.REACT_APP_SBC_API_KEY,
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

---

### 4. Test It! (5 min)

```bash
# Start the app
cd /Users/nithinkamavaram/Desktop/Hackathon/frontend
npm start
```

**Test flow:**
1. Open http://localhost:3000
2. Click "Connect Wallet"
3. Approve in MetaMask
4. Submit an AI task
5. When results appear → MetaMask should open automatically
6. Sign the transaction
7. See payment confirmation!

---

### 5. Commit & Merge (2 min)

```bash
cd /Users/nithinkamavaram/Desktop/Hackathon

# Add all changes
git add .

# Commit
git commit -m "feat: integrate SBC blockchain payment system

- Added gasless transaction support with @stablecoin.xyz SDK
- Implemented automatic payment after AI task completion
- Added MetaMask wallet connection
- Created payment utility for ERC20 permit signatures
- Payment flows automatically when results display
- Supports Base Mainnet with BaseScan explorer links"

# Push to feature branch
git push origin feature/codecollab-swarm-implementation

# Merge to main
git checkout main
git merge feature/codecollab-swarm-implementation
git push origin main
```

---

## 🎬 For Your Demo Video

When recording, show:

1. **"First, I connect my MetaMask wallet"**
   - Click Connect Wallet button
   - Show connected address

2. **"I submit an AI task - let's do an LRU Cache"**
   - Enter task description
   - Click submit

3. **"Watch the 5 agents collaborate"**
   - Point to each agent as they work

4. **"When results appear, payment happens automatically!"**
   - Show MetaMask popup
   - "No gas fees needed - it's gasless!"

5. **"I sign the transaction and boom - 6 cents paid in SBC tokens"**
   - Show transaction confirmation
   - Click "View Transaction" link
   - Show on BaseScan

---

## 📚 Full Documentation

For detailed info, see `PAYMENT_INTEGRATION_GUIDE.md`

---

## 🐛 If Something Breaks

### npm install fails?
```bash
sudo chown -R $(id -u):$(id -g) "$HOME/.npm"
npm cache clean --force
cd frontend
npm install --legacy-peer-deps
```

### Wallet won't connect?
- Install MetaMask extension
- Switch to Base Mainnet in MetaMask
- Refresh the page

### Payment doesn't trigger?
- Check console for errors (F12)
- Make sure wallet is connected
- Verify `currentResult.payment.amount > 0`

---

## ✅ Done!

**You now have:**
- ✅ Blockchain wallet integration
- ✅ Automatic micropayments after AI tasks
- ✅ Gasless transactions (no ETH needed for gas)
- ✅ Transaction explorer links
- ✅ Ready to record your demo video! 🎥

**Time to demo and win! 🏆🚀**
