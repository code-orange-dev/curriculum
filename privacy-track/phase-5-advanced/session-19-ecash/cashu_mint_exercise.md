# Cashu Mint Exercise: eCash Privacy on Bitcoin

## Overview

Chaumian eCash provides **perfect sender privacy** within a mint through blind signatures. Unlike on-chain transactions where all UTXOs are public, or Lightning where nodes see routing information, eCash transactions are completely opaque to the mint operator.

**Blind signatures** allow a user to obtain a cryptographic signature on a value that the signer (mint) never sees in plaintext. This means:
- The mint signs a blinded commitment
- The user unblinds the signature
- The mint cannot link the original request to the redemption
- Perfect privacy between user and mint

This exercise walks through setting up a Cashu mint, minting tokens, sending them peer-to-peer, and analyzing what information leaks at each step.

## Prerequisites

- Python 3.9 or higher
- `pip` package manager
- Docker (for Lightning backend)
- `git` for cloning repositories
- Basic command-line familiarity
- ~30 minutes for full exercise

## Part 1: Set Up a Cashu Mint

### Step 1a: Clone and Install Nutshell

```bash
# Clone the Nutshell Cashu mint reference implementation
git clone https://github.com/cashubtc/nutshell.git
cd nutshell

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
```

### Step 1b: Configure for Signet/Testnet

Create a `.env` file in the nutshell directory:

```bash
# .env configuration for Cashu mint on Bitcoin Signet
MINT_PRIVATE_KEY=your_generated_key_here
MINT_HOST=0.0.0.0
MINT_PORT=3338
MINT_NETWORK=signet
MINT_DATABASE_URL=sqlite:///./mint.db

# Lightning backend (LND, CLN, or LDK)
MINT_LIGHTNING_BACKEND=lnbits
MINT_LNBITS_URL=http://localhost:5000
MINT_LNBITS_KEY=your_lnbits_admin_key

# Optional: Postgres for production
# MINT_DATABASE_URL=postgresql://user:password@localhost/cashu_mint
```

### Step 1c: Start the Mint

```bash
# Run the Cashu mint
cashu mint

# The mint will be available at http://localhost:3338
# Check the API with: curl http://localhost:3338/v1/info
```

**Expected output:**
```json
{
  "name": "Nutshell",
  "version": "0.15.0",
  "pubkey": "02a1b2c3...",
  "keyset_id": "00a1b2c3...",
  "mint_url": "http://localhost:3338"
}
```

### Step 1d: Connect a Lightning Backend

For development, use **LNbits** (simple self-hosted Lightning wallet):

```bash
# In a new terminal, run LNbits
docker run -p 5000:5000 lnbits/lnbits:latest

# Visit http://localhost:5000
# Create a wallet, copy the admin key to your .env MINT_LNBITS_KEY
```

Alternatively, use:
- **LND** (Lightning Network Daemon): Full node with gRPC API
- **CLN** (Core Lightning): Minimal setup with REST API
- **LDK** (Rust Lightning implementation)

## Part 2: Mint Tokens

### Step 2a: Pay a Lightning Invoice

Get a Cashu token by paying an invoice:

```bash
# Request an invoice from the mint
curl -X POST http://localhost:3338/v1/mint/quote/lightning \
  -H "Content-Type: application/json" \
  -d '{"amount": 100, "unit": "sat"}'

# Response:
# {
#   "quote": "05d0c...",
#   "request": "lnbc1000n1pj...",
#   "paid": false,
#   "created_at": 1716129600,
#   "expiry": 1716216000
# }

# Pay the invoice with your Lightning wallet (e.g., LNbits)
# Then claim the tokens:
curl -X POST http://localhost:3338/v1/mint/bolt11 \
  -H "Content-Type: application/json" \
  -d '{"quote": "05d0c...", "outputs": [{"amount": 100, "blind_message": "..."}]}'
```

### Step 2b: Examine the Token Structure

A Cashu token is a JSON object:

```json
{
  "mint": "http://localhost:3338",
  "proofs": [
    {
      "amount": 100,
      "secret": "abcd1234...",
      "C": "02a1b2c3...",
      "id": "00a1b2c3..."
    }
  ]
}
```

**Decoding the token:**
- `amount`: Satoshi value
- `secret`: User's random secret (blinding input)
- `C`: Blind-signed commitment (mint's signature on blinded value)
- `id`: Keyset ID (which mint key was used)
- `mint`: Mint URL (where to redeem)

```bash
# Inspect a Cashu token
python3 -c "
import json
import base64
token = 'cashu...'  # Paste your token here
decoded = base64.urlsafe_b64decode(token + '==')
print(json.dumps(json.loads(decoded), indent=2))
"
```

### Step 2c: Understanding the Blind Signature

**What the mint signs vs what you receive:**

1. **User creates:** Secret `x`, computes public `Y = hash_to_curve(x)`
2. **User blinds:** Blinded commitment `B' = Y + r*G` (r = random blinding factor)
3. **User sends to mint:** Only `B'` (mint never sees `x` or `Y`)
4. **Mint signs:** `C' = k * B'` (k = mint's private key)
5. **User unblinds:** `C = C' - r*K` (K = k*G = mint's public key)
6. **Result:** `C = k*Y` (valid signature on `Y` that mint never explicitly signed)

**Why this provides privacy:**
- Mint receives `B'` at step 2, receives `C` at redemption
- But `B'` is mathematically unrelated to `C` (due to blinding)
- Mint cannot link the minting request to the redemption

```python
# Simplified blind signature example (elliptic curve)
from coincurve import PrivateKey, PublicKey
import hashlib
import secrets

# Setup
mint_privkey = PrivateKey(secrets.token_bytes(32))
mint_pubkey = mint_privkey.public_key

# User creates a secret and blinds it
user_secret = secrets.token_bytes(32)
Y = PrivateKey(hashlib.sha256(user_secret).digest()).public_key.point

# User blinds the commitment
r = secrets.randbelow(2**256)
blinding_factor = PrivateKey(r.to_bytes(32, 'big')).public_key.point
B_blind = Y.add(blinding_factor)

# Mint signs the blinded commitment
C_blind = mint_privkey.secret * B_blind  # scalar multiplication

# User unblinds
C_unblind = C_blind.add(blinding_factor.multiply(-r))

# Verify: C_unblind == mint_privkey.secret * Y
print("Signature valid:", C_unblind == mint_privkey.secret * Y)
```

## Part 3: Send Tokens Peer-to-Peer

### Step 3a: Send Tokens (No Mint Interaction)

One of Cashu's key features: **tokens can be transferred directly between users without the mint's knowledge.**

```bash
# User A has token and wants to send to User B

# Export token as string
TOKEN="cashu://..."

# User B imports token into their wallet
# (In reality, use Cashu wallet like ENuts, Minibits, or Cashu.me)

# The mint sees NOTHING during this transfer
```

### Step 3b: Receiver Redeems Tokens

When User B spends the token, they must "swap" it for fresh tokens (essential for double-spend prevention):

```bash
# User B calls /v1/swap endpoint
curl -X POST http://localhost:3338/v1/swap \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": [{"amount": 100, "secret": "abcd1234...", "C": "02a1b2c3..."}],
    "outputs": [{"amount": 100, "blind_message": "..."}]
  }'

# Response: New signed tokens (unlinked to original)
```

### Step 3c: Privacy Analysis - What the Mint Sees

| Operation | User Identity | Amount | Linking? | Comment |
|-----------|---------------|--------|----------|---------|
| Minting | Known (pays invoice) | Known | Yes | Linked to Lightning payment |
| P2P Send | Unknown | Known | No | Mint sees nothing |
| Redemption (Swap) | Unknown | Known | No | Blinded signature hides which token |
| Melting | Known (withdraws to LN) | Known | Yes | Linked to withdrawal invoice |

**Key insight:** Within a mint, the sender and receiver are perfectly private from the mint and each other (except for amounts). The mint only learns about users when they enter (via Lightning) or exit (via Lightning) the system.

## Part 4: Privacy Analysis

Create a detailed table showing information flow:

```
╔════════════════════╦═══════════════════╦══════════════╦═════════════════╗
║   Operation        ║  User Linked?     ║  Amounts     ║  Linking Data   ║
╠════════════════════╬═══════════════════╬══════════════╬═════════════════╣
║ Lightning Invoice  ║ Yes (payer)       ║ Visible      ║ Payment hash    ║
║ Mint (Keyset)      ║ No                ║ Visible      ║ Blind signature ║
║ P2P Token Transfer ║ No (off-chain)    ║ Visible      ║ None            ║
║ Swap/Redeem        ║ No                ║ Visible      ║ Blind signature ║
║ Melt (LN Payout)   ║ Yes (payee)       ║ Visible      ║ Payment hash    ║
╚════════════════════╩═══════════════════╩══════════════╩═════════════════╝
```

**Question:** Can a sophisticated mint operator link minting to redemption by analyzing timing or amounts?

**Answer:** Partially—if amounts and timing are unique, some correlation is possible. This is why:
- **Mixing/coinjoin-style protocols** combine tokens across users
- **Fedimint** uses distributed threshold signatures (no single operator)
- Users should **split and recombine** tokens to avoid fingerprinting

## Part 5: Double-Spend Prevention

### Step 5a: Attempt a Double-Spend

```bash
# Proof: attempt to swap the same token twice
TOKEN_SECRET="abcd1234..."
TOKEN_COMMITMENT="02a1b2c3..."

# First swap (succeeds)
curl -X POST http://localhost:3338/v1/swap \
  -H "Content-Type: application/json" \
  -d "{\"inputs\": [{\"secret\": \"$TOKEN_SECRET\", \"C\": \"$TOKEN_COMMITMENT\"}]}"
# Response: New token issued

# Second swap (same token, should fail)
curl -X POST http://localhost:3338/v1/swap \
  -H "Content-Type: application/json" \
  -d "{\"inputs\": [{\"secret\": \"$TOKEN_SECRET\", \"C\": \"$TOKEN_COMMITMENT\"}]}"
# Response: Error - token already redeemed
```

### Step 5b: How Double-Spend Prevention Works

1. **Storage:** Mint maintains a database of spent `(secret, C)` pairs
2. **Check:** Before issuing new tokens, mint verifies the input isn't in the spent set
3. **Record:** After successful swap, mint marks `(secret, C)` as spent
4. **Failure mode:** If honest participant redeems offline and syncs with conflicting state, one redemption fails

**Trade-off:** Double-spend prevention requires **online validation** (unlike on-chain Bitcoin which is offline-verifiable). This is the cost of privacy and scalability.

## Part 6: The Blind Signature Math

This section walks through the complete Chaumian blind signature protocol step-by-step.

### Setup

- **Mint:** Generates private key `k` (scalar), computes public key `K = k*G` (elliptic curve point)
- **User:** Wants a signature on value `x` that the mint never sees

### The Protocol

#### Step 1: User Creates a Secret

```
User generates: x ← {0, 1}^256 (random 256-bit secret)
Compute: Y = hash_to_curve(x)  (map secret to elliptic curve point)
```

**Why?** `Y` is the commitment on which the mint will sign. The user keeps `x` secret.

#### Step 2: User Blinds the Commitment

```
User generates: r ← {0, 1}^256 (random blinding factor)
Compute: B' = Y + r*G  (add randomness to Y)
Send to Mint: B' (blinded commitment)
```

**Why?** The blinding factor `r*G` randomizes the commitment. The mint cannot compute `Y` from `B'` without knowing `r`.

#### Step 3: Mint Signs the Blinded Commitment

```
Mint receives: B'
Compute: C' = k * B'  (scalar multiplication with private key)
Send to User: C'
```

**Note:** The mint signs blindly—it has no idea what it's actually signing.

#### Step 4: User Unblinds the Signature

```
User receives: C'
Compute: C = C' - r*K  (subtract the blinding factor's effect)
Result: C = k*Y  (valid signature on the user's secret Y)
```

**Verification:**
```
C' - r*K
= k*B' - r*K
= k*(Y + r*G) - r*(k*G)
= k*Y + k*r*G - r*k*G
= k*Y  ✓
```

#### Step 5: Redemption (What the Mint Sees)

```
User later sends: (x, C)  or  (Y, C)
Mint verifies: k*Y == C  (using public key K = k*G)
Mint marks (Y, C) as spent
```

**The Magic:** The mint performed step 3 on `B'`, but verifies step 5 on `Y`. 

- `B' = Y + r*G` (from blinding)
- `C' = k*B'` (what mint signed)
- `C = C' - r*K = k*Y` (what user unblinds)

The blinding factor `r` ensures `B'` is statistically independent of `Y`, so:
- Mint cannot link `B'` (from minting) to `Y` (from redemption)
- **Perfect unlinkability** ✓

### Complete Example (Pseudocode)

```python
# Toy example with simple elliptic curve (not cryptographically sound)
import hashlib
import secrets

# Elliptic curve: secp256k1 (used in Cashu)
# G = generator point, n = order

def hash_to_curve(data):
    """Hash to a curve point (simplified)"""
    h = hashlib.sha256(data).digest()
    return deserialize_point(h)

# === SETUP ===
mint_privkey = 0x0123456789...  # k
mint_pubkey = multiply(mint_privkey, G)  # K = k*G

# === MINTING ===
# User side
user_secret = secrets.token_bytes(32)  # x
Y = hash_to_curve(user_secret)
r = secrets.randbelow(n)
B_blind = point_add(Y, multiply(r, G))  # B' = Y + r*G

# Send B_blind to mint
# Mint side
C_blind = multiply(mint_privkey, B_blind)  # C' = k*B'

# Send C_blind back to user
# User side
K = mint_pubkey
C = point_subtract(C_blind, multiply(r, K))  # C = C' - r*K

# === REDEMPTION ===
# User sends: (user_secret, C)
# Mint computes Y from user_secret:
Y_check = hash_to_curve(user_secret)
# Verify signature:
assert multiply(mint_privkey, Y_check) == C
# Mark as spent: spent_tokens.add((user_secret, C))
```

### Why Blind Signatures Matter for Bitcoin Privacy

1. **Horizontal privacy:** Receiver cannot prove to sender that sender paid them (mint is intermediary)
2. **Forward privacy:** Even if mint is compromised, old transactions cannot be linked
3. **Scalability:** Tokens are off-chain; no blockchain space needed
4. **Fungibility:** All tokens of same amount are indistinguishable

## Discussion Questions

### Trust & Assumptions

1. **Trust Model:**
   - Bitcoin (on-chain): No trusted third party needed
   - Lightning: Hop nodes see routing info; payment must be atomic
   - Cashu (single mint): Mint must not steal or rug; must maintain database

2. **What are the minimal trust assumptions of eCash vs on-chain Bitcoin?**
   - eCash: Mint doesn't steal, doesn't correlate users, doesn't censor
   - On-chain: Network doesn't 51% attack, script execution is correct

3. **Single Point of Failure:**
   - If the mint goes offline, can you spend your tokens? (No, without swap)
   - If the mint disappears, is your money gone? (Yes)
   - How is this different from custodial exchanges?

### Fedimint & Federation

4. **How could a Fedimint (federation) reduce the single-mint trust assumption?**
   - Instead of `k`, use threshold scheme: `k = k1 + k2 + k3 + ... + kN`
   - M-of-N guardians must cooperate to sign
   - No single operator can steal or link transactions
   - Reference: [Fedimint whitepaper](https://fedimint.org)

5. **What's the tradeoff of using a federation?**
   - Increased complexity (M-of-N threshold signatures)
   - Latency (more parties = slower coordination)
   - But: Reduced trust in any one operator

### Protocol Design

6. **What happens if the mint goes offline?**
   - Active tokens cannot be spent (no swap available)
   - Tokens are no longer useful until mint comes back
   - Compare to on-chain: Can always broadcast your UTXO
   - Compare to Lightning: Can unilaterally close channels

7. **Could the mint identify you by analyzing token timing or amounts?**
   - Yes, if you always mint unique amounts or at predictable times
   - Mitigation: Mix amounts, wait random intervals, use Fedimint

### Practical Deployment

8. **When should you use eCash vs on-chain vs Lightning?**

| Scenario | Best Choice | Why |
|----------|------------|-----|
| Privacy within network | eCash | Perfect sender privacy |
| Cross-custody payments | On-chain | Trustless settlement |
| Instant payments | Lightning | Fast, scalable |
| Offline payments | On-chain | Only option that works |
| High throughput | eCash | Most efficient |

9. **How does Cashu differ from traditional ecash (Digicash)?**
   - Cashu: Multiple keysets, flexible denomination, Lightning-backed
   - Digicash (1990s): Single operator, issued for fiat
   - Both use Chaumian blind signatures

10. **What's the relationship between Cashu and Fedimint?**
    - Cashu: Single-operator or federated eCash
    - Fedimint: Always federated (threshold signatures)
    - Fedimint adds: eCash for privacy + threshold for decentralization

## Troubleshooting

**Mint won't start:**
```bash
# Check if port 3338 is in use
lsof -i :3338
# Kill existing process if needed
kill -9 <PID>
```

**Lightning backend connection fails:**
- Verify LNbits is running: `curl http://localhost:5000`
- Check MINT_LNBITS_KEY in .env
- Ensure LN node has funds: visit LNbits UI

**Token swap fails:**
- Verify token isn't already spent: `curl http://localhost:3338/v1/checkspendable`
- Check token format is valid JSON
- Ensure amounts match (no partial redeems without splitting)

**Blind signature verification fails:**
- Verify you used correct keyset ID
- Check that curve operations are consistent (all secp256k1)
- Ensure C is a valid curve point

## Next Steps

1. **Explore Cashu ecosystem:**
   - [Minibits wallet](https://minibits.cash)
   - [ENuts wallet](https://enuts.cash)
   - [Cashu.me](https://cashu.me)

2. **Study advanced topics:**
   - Chaumian CoinJoin (mixing eCash across users)
   - Threshold cryptography (Fedimint)
   - Privacy-preserving issuance protocols

3. **Run your own mint:**
   - Deploy Nutshell on testnet/signet
   - Integrate with your Lightning node
   - Build a web interface for token management

4. **Read more:**
   - [Cashu NUT specs](https://github.com/cashubtc/nuts)
   - [David Chaum's blind signatures (1983)](https://www.chaum.com/publications/)
   - [Fedimint documentation](https://docs.fedimint.org)

