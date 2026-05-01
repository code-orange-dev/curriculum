# Payjoin Testnet Exercise

> Build and send a Payjoin transaction on regtest.

## Setup

### Prerequisites

- Bitcoin Core installed and running in regtest mode
- Rust toolchain installed (`rustup`)
- Payjoin Dev Kit cloned: `git clone https://github.com/payjoin/rust-payjoin`

### Start Your Regtest Environment

```bash
# Start bitcoind in regtest
bitcoind -regtest -daemon

# Create two wallets (sender and receiver)
bitcoin-cli -regtest createwallet "sender"
bitcoin-cli -regtest createwallet "receiver"

# Mine blocks to the sender (need 101 for maturity)
SENDER_ADDR=$(bitcoin-cli -regtest -rpcwallet=sender getnewaddress)
bitcoin-cli -regtest generatetoaddress 101 $SENDER_ADDR

# Check sender balance
bitcoin-cli -regtest -rpcwallet=sender getbalance
# Should show 50.00000000

# Fund the receiver too (they need a UTXO to contribute to the Payjoin)
RECEIVER_ADDR=$(bitcoin-cli -regtest -rpcwallet=receiver getnewaddress)
bitcoin-cli -regtest -rpcwallet=sender sendtoaddress $RECEIVER_ADDR 5.0
bitcoin-cli -regtest generatetoaddress 1 $SENDER_ADDR
```

---

## Exercise 1: Manual Payjoin (Step by Step)

### Step 1: Receiver Creates a Payment Request

```bash
# Receiver generates a fresh address for the payment
PAYMENT_ADDR=$(bitcoin-cli -regtest -rpcwallet=receiver getnewaddress)
echo "Payment address: $PAYMENT_ADDR"
```

### Step 2: Sender Creates the Original PSBT

```bash
# Sender creates a PSBT paying 1 BTC to the receiver
ORIG_PSBT=$(bitcoin-cli -regtest -rpcwallet=sender walletcreatefundedpsbt \
  '[]' "[{\"$PAYMENT_ADDR\": 1.0}]" 0 '{"includeWatching": true}' | jq -r '.psbt')

echo "Original PSBT: $ORIG_PSBT"

# Decode it to see the structure
bitcoin-cli -regtest decodepsbt $ORIG_PSBT
```

**YOUR TASK**: Examine the decoded PSBT. Answer:
- How many inputs does it have?
- How many outputs?
- Which output is the payment and which is change?
- If a chain analyst sees this, what can they deduce?

### Step 3: Sender Signs the Original PSBT

```bash
SIGNED_ORIG=$(bitcoin-cli -regtest -rpcwallet=sender walletprocesspsbt $ORIG_PSBT | jq -r '.psbt')
echo "Signed original PSBT: $SIGNED_ORIG"
```

### Step 4: Receiver Adds Their Input (The Payjoin Magic)

This is where Payjoin happens. The receiver contributes one of their own UTXOs.

```bash
# Receiver lists their UTXOs
bitcoin-cli -regtest -rpcwallet=receiver listunspent

# Pick one of the receiver's UTXOs (note the txid, vout, and amount)
# YOUR CODE: Fill in the UTXO details from the listunspent output
RECEIVER_UTXO_TXID="<fill in>"
RECEIVER_UTXO_VOUT=0  # fill in
RECEIVER_UTXO_AMOUNT=5.0  # fill in
```

**YOUR TASK**: Now manually construct the modified Payjoin PSBT.

The receiver needs to:
1. Add their UTXO as an additional input
2. Increase their payment output by the value of their added input
3. The change output from the sender stays the same

```bash
# Create the Payjoin PSBT with both sender's and receiver's inputs
# The receiver's output increases from 1.0 BTC to 1.0 + RECEIVER_UTXO_AMOUNT
# (minus the receiver's share of the fee)

# YOUR CODE HERE:
# Use walletcreatefundedpsbt or createpsbt to build the modified transaction
# Hint: You'll need to include:
#   - All inputs from the original PSBT
#   - The receiver's additional UTXO as a new input
#   - The payment output (now 1.0 + receiver's UTXO amount)
#   - The sender's change output (unchanged)
```

### Step 5: Both Sign the Payjoin PSBT

```bash
# Receiver signs their input
RECEIVER_SIGNED=$(bitcoin-cli -regtest -rpcwallet=receiver walletprocesspsbt $PAYJOIN_PSBT | jq -r '.psbt')

# Sender signs their input(s)
BOTH_SIGNED=$(bitcoin-cli -regtest -rpcwallet=sender walletprocesspsbt $RECEIVER_SIGNED | jq -r '.psbt')

# Finalize
FINAL_TX=$(bitcoin-cli -regtest finalizepsbt $BOTH_SIGNED | jq -r '.hex')
```

### Step 6: Broadcast and Analyze

```bash
# Broadcast
TXID=$(bitcoin-cli -regtest sendrawtransaction $FINAL_TX)
echo "Payjoin txid: $TXID"

# Mine a block
bitcoin-cli -regtest generatetoaddress 1 $SENDER_ADDR

# Decode the final transaction
bitcoin-cli -regtest getrawtransaction $TXID true
```

**YOUR TASK**: Analyze the final transaction:
1. How many inputs does it have?
2. Can you tell which input belongs to the sender and which to the receiver?
3. Apply the common-input-ownership heuristic — what would a chain analyst conclude?
4. Is that conclusion correct?

---

## Exercise 2: Compare Normal vs Payjoin

Create two transactions side by side:

1. A **normal transaction**: sender pays receiver 1 BTC (no Payjoin)
2. A **Payjoin transaction**: sender pays receiver 1 BTC (with receiver input)

For each transaction, document:

| Property | Normal TX | Payjoin TX |
|----------|-----------|------------|
| Number of inputs | | |
| Number of outputs | | |
| Can identify change output? | | |
| CIOH conclusion | | |
| CIOH accuracy | | |
| Identifiable as Payjoin? | | |

---

## Exercise 3: Discussion Questions

Write 2-3 paragraphs on each:

1. **What coin selection strategy should the receiver use when adding their input?** Should they add their largest UTXO? Smallest? Random? What are the privacy trade-offs?

2. **What checks must the sender perform on the receiver's modified PSBT?** List every verification step needed to prevent the receiver from stealing funds or degrading the sender's privacy.

3. **If you were integrating Payjoin into a mobile wallet, what UX decisions would you make?** Should it be automatic? Opt-in? How do you handle failures?

---

## Submission

Post your transaction analysis and discussion answers in the Discord `#privacy-track` channel before the next session.

---

*Code Orange Dev School | [codeorange.dev](https://codeorange.dev) | CC0 1.0 Universal*
