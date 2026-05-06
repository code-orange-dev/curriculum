# Bitcoin Privacy Developer Track: Phase 2 - Silent Payments (Sessions 5-8)

## Overview

Phase 2 dives deep into **BIP352 Silent Payments**, the next-generation Bitcoin privacy solution. Unlike traditional static payment addresses (which create a privacy leak when reused), Silent Payments allow a sender to generate a unique on-chain output for every payment to the same static address—without on-chain interaction, without per-payment address derivation, and without revealing to observers that multiple payments went to the same recipient. By the end of Phase 2, you'll implement a complete Silent Payments sender, understand scanning and light client architecture, and contribute to production Bitcoin privacy infrastructure.

**Time Commitment:** 4 weeks, 10-12 hours per session  
**Target Audience:** Developers with Phase 1 foundation; crypto/cryptography knowledge helpful  
**Prerequisites:** Complete Phase 1 or equivalent knowledge of chain analysis, UTXO management, transaction structure  
**Outcome:** Functional Silent Payments implementation, production-ready contributions to Bitcoin Core and wallets

---

## Session 5: How Silent Payments Work

### Real-World Scenario

**The Donation Address That Wasn't**  
A Bitcoin educator and podcast host publishes a single static Bitcoin address in her podcast bio and social media: `sp1qqgste6gj5mxqt24dxy2r2rkv7pa3qy9f2mqkp89q0wvxc2yujsydvu7jmj` (Silent Payments address). Her listeners donate regularly. A chain analyst looks at the address and sees... nothing. No historical transactions. No UTXOs. Why? Every donation created a **unique, unrelated on-chain output**. The analyst cannot determine:
- How many donors she has
- The total amount received
- Which transactions belong to her
- Whether donors are recurring or one-time

Meanwhile, the host holds a single private key that can find and spend all incoming Silent Payments without revealing her identity to anyone—not even the donors who funded her. This is Silent Payments: the first practical on-chain privacy solution that solves the "static address reuse" problem without requiring interaction per payment.

### Learning Objectives

By the end of Session 5, you will:
- Understand the fundamental problem Silent Payments solves (address reuse privacy leak)
- Grasp the cryptographic primitives: Elliptic Curve Diffie-Hellman, hash-based derivation, tweaking
- Understand the sender-side protocol: how to derive a unique output for every SP address
- Understand the receiver-side protocol: how to scan and claim Silent Payments
- Recognize real-world use cases where Silent Payments are the optimal solution
- Know the status of Silent Payments implementation across wallets and Bitcoin Core

### Privacy Tools You'll Use

- **BIP352 Specification** (https://github.com/bitcoin/bips/blob/master/bip-0352.md)
- **Cake Wallet** — First production Silent Payments wallet (already shipping SP support)
- **Bitcoin Core PR #28122** — In-progress Silent Payments implementation
- **Sparrow Wallet** — Upcoming Silent Payments support (planned)
- **Kyoto / Floresta** — Light client scanning infrastructure for SP
- **rust-silentpayments** — Reference implementation (github.com/cygnet3/rust-silentpayments)

### Hands-On Exercise: "Follow the Silent Payment"

**Part 1: Understand the Math (Conceptually)**

**Step 1:** Read BIP352 Section 2 (Protocol Description):  
https://github.com/bitcoin/bips/blob/master/bip-0352.md#protocol

You don't need to memorize the math yet, but understand these concepts:
- **Sender side:** "For each payment to SP address, derive a unique output address"
- **Receiver side:** "Use your private key to scan the blockchain and find all outputs intended for you"
- **Key concept:** ECDH (Elliptic Curve Diffie-Hellman) lets the sender create outputs only the receiver can spend

**Step 2:** Compare to traditional Bitcoin:
- **Traditional:** Alice publishes address `1Alice...`. Bob sends to it. Carol sends to it. Chain analyst: "Alice received 2 payments."
- **Silent Payments:** Alice publishes SP address `sp1qqAlice...`. Bob sends to it → output is `4f3a...` (unique). Carol sends to it → output is `7e2b...` (unique). Chain analyst: "I see two unrelated payments; I don't know they're both for Alice."

**Step 3:** Document in your own words:
- Why is address reuse a privacy problem?
- How do Silent Payments prevent address reuse?
- What's the trade-off? (Scanning requires checking every transaction; light clients need special infrastructure)

**Part 2: Interact with a Real Silent Payments Wallet**

**Step 4:** Install **Cake Wallet** (free, open-source):
- iOS: App Store or https://cakewallet.com/
- Android: Play Store or https://cakewallet.com/
- Desktop (beta): https://github.com/cake-tech/cake_wallet

**Step 5:** Create a new Bitcoin wallet in Cake Wallet:
- Go to Settings → Add Wallet → Bitcoin
- Choose "Bitcoin" as the coin
- Create new wallet
- Go to Receive
- You'll see TWO address types:
  - Regular address (starts with `1`, `3`, or `bc1`)
  - **Silent Payments address** (starts with `sp1`)

**Step 6:** Export and document your Silent Payments address:
```
Your SP Address: sp1qq______________________
Receiver key (from wallet): _______________
```

**Step 7:** Use https://oxt.me or mempool.space to search for your SP address:
- Result: Address not found (because SP addresses have no on-chain history until you receive a payment)
- This is normal and expected
- Create a comparison: traditional addresses show transaction history immediately; SP addresses show nothing

**Step 8:** If you have testnet Bitcoin:
- Send a small amount to your Cake Wallet SP address using a testnet sender (or another wallet that supports SP testnet)
- Watch Cake Wallet scan and detect the payment
- Document: How long did scanning take? Did the payment appear in "Pending"?
- Once confirmed, sweep the payment back to verify you can spend Silent Payments

**Part 3: Understand the Scanning Problem**

**Step 9:** Read about Silent Payments scanning:  
https://github.com/bitcoin/bips/blob/master/bip-0352.md#scanning

Key question: How does a receiver know which transactions are theirs?
- Answer: They scan every transaction, test if it contains an output for them
- Problem: Scanning thousands of transactions is slow on mobile
- Solution: Light clients like Kyoto use filters to skip irrelevant transactions

**Step 10:** Document the scanning trade-off:
```
SCANNING TRADE-OFF:

Privacy benefit:
- Static address never appears on-chain
- No address clustering possible
- No way to determine how many payments received

Privacy/performance trade-off:
- Receiver must scan ALL transactions (or use filtered light client)
- Wallet sees every transaction in Bitcoin (though doesn't download full data)
- More CPU usage than traditional wallets

Mitigation strategies:
- Use Cake Wallet's built-in SP support (handles scanning for you)
- Use light client with server-based filtering (Kyoto, Floresta)
- Use full node with bitcoin-cli (maximum privacy, maximum resource usage)
```

**Step 11:** Compare scanning approaches:

| Approach | Privacy | Performance | Practicality |
|---|---|---|---|
| Full node scanning | Perfect | Slow | High setup, runs locally |
| Light client (server filter) | Very good | Fast | Relies on server not tracking you |
| Cake Wallet (built-in) | Excellent | Medium | Ready to use, tested |
| Mobile (future) | ? | TBD | Still experimental |

### Open a PR This Week

**Contribute to Silent Payments Documentation or Wallets**

1. Visit https://github.com/bitcoin/bitcoin/pulls (search "Silent Payments" or "BIP352")
   OR https://github.com/cake-tech/cake_wallet
2. Choose one of:
   - Add documentation to Bitcoin Core PR #28122 explaining the sender/receiver protocol
   - Write a user guide for Cake Wallet's Silent Payments feature
   - Create test vectors or test cases for BIP352 compliance
   - Document the scanning optimization techniques in a GitHub wiki
3. Submit as a PR with clear explanation
4. Link in your Phase 2 submission

**Alternative:** Contribute to Educational Content
1. Go to https://github.com/bitcoinops/bitcoinops.github.io
2. Add a new Mastery Page or FAQ entry explaining:
   - "Why Silent Payments?"
   - "How to generate a Silent Payments address"
   - "Why scanning matters"
3. Submit PR with at least 500 words

### Daily Life Privacy Tip

**Generate your first Silent Payments address today.**

If you use Cake Wallet, you already have a Silent Payments address. If not:

1. Download Cake Wallet (testnet or mainnet)
2. Create a Bitcoin wallet
3. Go to Receive and copy your SP address (starts with `sp1`)
4. Share this address publicly (social media, website, podcast)
5. It will never appear on a blockchain explorer
6. You can receive unlimited payments to one static address
7. No one can see your total balance or payment count

This single address replaces the need to generate new addresses for every donation, invoice, or payment—one of the most impactful privacy improvements in Bitcoin since SegWit.

### Reading List with Links

1. **BIP352: Silent Payments**  
   https://github.com/bitcoin/bips/blob/master/bip-0352.md
   - Complete specification (Sections 1-3 are essential)

2. **"Silent Payments Explained" — Bitcoin Optech**  
   https://bitcoinops.org/en/newsletters/2022/08/03/#overview-of-the-bip352-silent-payments-proposal
   - Non-technical overview of the proposal

3. **"How Silent Payments Will Change Bitcoin Privacy" — Bitcoin Magazine**  
   https://bitcoinmagazine.com/articles/silent-payments
   - Real-world use case analysis

4. **Cake Wallet Silent Payments Guide**  
   https://cakewallet.com/articles/what-are-silent-payments
   - User-friendly walkthrough

5. **Bitcoin Core PR #28122 Discussion**  
   https://github.com/bitcoin/bitcoin/pull/28122
   - Implementation progress and technical discussion

6. **Kyoto: Light Client for Silent Payments**  
   https://github.com/rustaceanrob/kyoto
   - Scanning optimization for mobile wallets

7. **"The Privacy Case for Silent Payments" — Bitcoin Privacy Institute**  
   https://bitcoinprivacyinstitute.org/silent-payments/
   - Comparison to other privacy solutions (CoinJoin, L2 solutions)

---

## Session 6: Implement SP Sender in Python

### Real-World Scenario

**The Invoice Dilemma**  
You're building a freelancing platform where clients need to pay creators with Bitcoin. Traditionally, you'd generate a new address for each invoice—but now your creator has hundreds of invoices scattered across the blockchain. Or they could publish one address... but then anyone can see their total income. Silent Payments solves this: the creator publishes one SP address. Each client's payment creates a unique output. The creator receives all payments with a single private key. You, as the platform builder, implement this by writing a **Silent Payments sender**: code that takes a creator's SP address and produces a unique output for that creator's payment.

### Learning Objectives

By the end of Session 6, you will:
- Understand the BIP352 sender algorithm in detail
- Implement a complete SP sender in Python (or your preferred language)
- Know how to validate a Silent Payments address
- Know how to use shared secrets and tweaking in practice
- Write test cases against BIP352 test vectors
- Understand the difference between testnet and mainnet SP addresses

### Privacy Tools You'll Use

- **Python 3.8+** with `hashlib`, `ecdsa`
- **BIP352 Test Vectors** (github.com/bitcoin/bips/blob/master/bip-0352/vectors.json)
- **bitcoinlib-js** or **libsecp256k1** (for ECDH operations)
- **Sparrow Wallet** or **Bitcoin Core** (to inspect generated transactions)
- **rust-silentpayments** (reference implementation to compare)

### Hands-On Exercise: "Build a Silent Payments Sender"

**Step 1:** Set up your Python environment:
```bash
python3 -m venv sp-env
source sp-env/bin/activate
pip install hashlib ecdsa requests
```

**Step 2:** Download BIP352 test vectors:
```bash
curl https://raw.githubusercontent.com/bitcoin/bips/master/bip-0352/vectors.json > vectors.json
```

**Step 3:** Create a file `sp_sender.py` and start with the address validation:
```python
import hashlib
import json
from typing import Tuple

class SilentPaymentsSender:
    """
    BIP352 Silent Payments Sender Implementation
    
    This implementation derives unique output addresses for a given
    Silent Payments address.
    """
    
    def __init__(self):
        # You'll add ECDH and hashing functions here
        pass
    
    def validate_sp_address(self, sp_address: str) -> bool:
        """
        Validate that a string is a valid Silent Payments address.
        
        SP addresses:
        - Start with 'sp1' (mainnet) or 'sp1' (testnet, same prefix)
        - Are base32 encoded
        - Have a specific format and checksum
        """
        # Implement Bech32m decoding and checksum validation
        # Reference: BIP350 (Bech32m encoding)
        pass
    
    def decode_sp_address(self, sp_address: str) -> Tuple[bytes, bytes]:
        """
        Decode a Silent Payments address into its components.
        
        Returns:
        - (scan_key: bytes, spend_key: bytes)
        
        These are the public keys that allow deriving unique outputs.
        """
        pass
    
    def derive_output_public_key(
        self, 
        sp_address: str, 
        sender_private_key: bytes,
        m: int  # Index (first, second, third payment, etc.)
    ) -> bytes:
        """
        Derive a unique output public key for a payment.
        
        Algorithm (BIP352 Section 2):
        1. Compute shared secret using ECDH with sender's private key
           and the receiver's scan public key
        2. Hash the shared secret with transaction inputs and output index
        3. Tweak the receiver's spend public key with the hash
        4. Result: unique public key for this payment
        
        This is the "Q" value in BIP352 terminology.
        """
        pass
```

**Step 4:** Implement ECDH (Elliptic Curve Diffie-Hellman):
```python
def ecdh(private_key: bytes, public_key: bytes) -> bytes:
    """
    Compute ECDH shared secret.
    
    This uses libsecp256k1 or ecdsa library.
    Returns: 32-byte shared secret
    """
    # Use ecdsa library or libsecp256k1
    # shared_secret = private_key * public_key (elliptic curve multiplication)
    pass
```

**Step 5:** Implement hash-based tweaking:
```python
def hash_tweak_add(data: bytes, point: bytes) -> bytes:
    """
    Hash data and add the result to a point (Taproot-style tweaking).
    
    Algorithm:
    1. h = SHA256(data)
    2. Q = point + h*G (elliptic curve point addition)
    
    Where:
    - h is interpreted as a scalar (256-bit number)
    - G is the elliptic curve generator point
    - Q is the new tweaked point
    """
    pass
```

**Step 6:** Load BIP352 test vectors:
```python
with open('vectors.json') as f:
    test_vectors = json.load(f)

# Test vectors contain:
# - Sender private keys
# - Silent Payments addresses
# - Expected outputs
# Use these to validate your implementation
```

**Step 7:** Test your implementation against test vectors:
```python
def test_sp_sender():
    sender = SilentPaymentsSender()
    
    for vector in test_vectors['vectors']:
        sp_address = vector['address']
        sender_privkey = bytes.fromhex(vector['privkey'])
        
        for output_idx, expected_output in enumerate(vector['outputs']):
            derived_key = sender.derive_output_public_key(
                sp_address, 
                sender_privkey, 
                output_idx
            )
            
            assert derived_key.hex() == expected_output, \
                f"Output {output_idx} mismatch"
    
    print("All test vectors passed!")
```

**Step 8:** Create a complete example transaction:
```python
def create_sp_payment(sp_address: str, amount_sat: int, 
                     sender_private_key: bytes) -> dict:
    """
    Create a complete Silent Payments payment.
    
    Returns:
    {
        'address': sp_address,
        'output_public_key': derived_public_key,
        'amount_sat': amount_sat,
        'output_script': p2tr_script_pubkey  # P2TR script
    }
    """
    output_key = derive_output_public_key(sp_address, sender_private_key, 0)
    
    # Convert to Taproot (P2TR) script format
    script = create_p2tr_script(output_key)
    
    return {
        'address': sp_address,
        'output_key': output_key.hex(),
        'amount_sat': amount_sat,
        'script': script.hex()
    }
```

**Step 9:** Document your implementation:
```
IMPLEMENTATION SUMMARY:

Silent Payments Sender Requirements:
- Input: SP address, sender private key
- Output: Unique public key for each payment
- Privacy guarantee: Each output is unique and cannot be linked

Cryptographic operations used:
1. ECDH (Elliptic Curve Diffie-Hellman)
2. SHA256 hashing
3. Elliptic curve point addition (Taproot-style tweaking)

Validation:
- Test vectors: PASS
- Mainnet addresses: Ready
- Testnet addresses: Ready
```

### Open a PR This Week

**Contribute to Silent Payments Implementation**

1. Visit https://github.com/cygnet3/rust-silentpayments (Rust reference)
   OR https://github.com/bitcoin/bitcoin/pull/28122 (Bitcoin Core)
2. Pick one of:
   - Add Python test cases to rust-silentpayments (if they have test suite)
   - Create comprehensive documentation for sender algorithm
   - Implement sender in a new language (Go, Rust, JavaScript)
   - Add test vector validation to an existing implementation
3. Submit PR with:
   - Complete sender implementation
   - Test cases (at least 10 test vectors)
   - Documentation of algorithm
4. Link in Phase 2 submission

**Alternative:** Create Educational Implementation
1. Create a `python-silentpayments` library on GitHub
2. Implement sender (and bonus: receiver protocol)
3. Include comprehensive documentation
4. Submit as a new repo (mention in your Phase 2 submission)

### Daily Life Privacy Tip

**Test your Silent Payments sender on Bitcoin testnet.**

Before deploying production code:

1. Generate a testnet SP address in Cake Wallet
2. Use your sender code to create a payment to that address
3. Broadcast on testnet
4. Watch Cake Wallet detect and confirm the payment
5. Verify you can spend the output

This validates your implementation against real Bitcoin before going mainnet.

### Reading List with Links

1. **BIP352 Sender Algorithm (Section 2)**  
   https://github.com/bitcoin/bips/blob/master/bip-0352.md#sending
   - Complete sender protocol specification

2. **BIP352 Test Vectors**  
   https://github.com/bitcoin/bips/blob/master/bip-0352/vectors.json
   - Reference test cases for validation

3. **rust-silentpayments Reference Implementation**  
   https://github.com/cygnet3/rust-silentpayments
   - Production-ready Rust implementation to compare

4. **Elliptic Curve Cryptography Primer**  
   https://www.youtube.com/watch?v=F3zzNa42-tQ
   - Visual explanation of ECDH (YouTube, 10 min)

5. **BIP350: Bech32m Checksum Format**  
   https://github.com/bitcoin/bips/blob/master/bip-0350.md
   - Address encoding/decoding specification

6. **Taproot Key Aggregation and Tweaking**  
   https://github.com/bitcoin/bips/blob/master/bip-0340.md#public-key-tweaking
   - Understanding point tweaking (used in SP)

7. **Bitcoin Core Silent Payments PR Comments**  
   https://github.com/bitcoin/bitcoin/pull/28122
   - Implementer discussion and design decisions

---

## Session 7: SP Scanning & Light Clients

### Real-World Scenario

**The Scanning Nightmare**  
You build a Bitcoin mobile wallet with Silent Payments support. Your users publish SP addresses and receive payments. But when they open the app, they expect their balance to update immediately—not after scanning 800,000 transactions. A traditional wallet downloads headers and filters transactions. A Silent Payments wallet must test every transaction to see if it contains a payment for the user. On 4G, this takes minutes. Your app crashes. Users complain. The solution: **light clients with server-assisted filtering**. The server scans transactions and creates filters that tell the client "these blocks might contain your payment." The client downloads only the relevant blocks. Privacy is nearly perfect (the server doesn't learn which outputs belong to you), and the app is fast.

### Learning Objectives

By the end of Session 7, you will:
- Understand why Silent Payments receivers need to scan (unlike traditional addresses)
- Know how light clients optimize scanning using block filters or other techniques
- Understand the privacy/performance/complexity trade-offs
- Evaluate different light client architectures (server-side filtering, client-side filtering, full node)
- Know which tools exist today (Cake Wallet, Kyoto, Floresta) and their approaches
- Implement or contribute to a light client scanning infrastructure

### Privacy Tools You'll Use

- **Cake Wallet** — Production SP scanning (built-in)
- **Kyoto** (https://github.com/rustaceanrob/kyoto) — Rust light client with SP support
- **Floresta** (https://github.com/commerceblock/floresta) — Utreexo-based light client
- **Bitcoin Core with pruning** — Full node SP scanning (reference)
- **BDK (Bitcoin Dev Kit)** — Wallet framework with SP support (planned)
- **electrs** — Electrum server (for understanding server-side filtering)

### Hands-On Exercise: "Build a Light Client Scanner"

**Part 1: Understand the Scanning Problem**

**Step 1:** Estimate the computational cost:
```
Bitcoin blocks per day: ~144
Transactions per block: ~2500 (average)
Daily transactions: ~360,000

For a Silent Payments receiver:
- Must test each transaction's outputs
- ECDH + hash per output: ~1ms CPU
- 360,000 tx * 1ms = 6 minutes per day
- Mobile device: 3-4x slower = 18-24 minutes

Solution: Filter to relevant transactions first
```

**Step 2:** Understand filter-based scanning:
```
Traditional: Test all transactions
Filter-based: Only test transactions that match filter

Filters used:
1. Output script pattern (P2TR outputs, which SP uses)
2. Sender-provided filter (server tells client which blocks to check)
3. BIP157 Compact Block Filters (standardized filters)

Trade-off: Server learns which blocks you're interested in
          (but not which outputs you own, if implemented carefully)
```

**Step 3:** Read Cake Wallet's approach:
- Visit https://github.com/cake-tech/cake_wallet/tree/master/lib/bitcoin
- Look for Silent Payments scanning code
- Document: Does it scan locally? Use a server? Both?

**Step 4:** Read Kyoto's approach:
- Visit https://github.com/rustaceanrob/kyoto
- Read README and architecture docs
- Kyoto uses BIP157 filters for optimization
- Document: How does Kyoto balance privacy and performance?

**Part 2: Implement a Naive Scanner (Educational)**

**Step 5:** Create a basic scanning client in Python:

```python
import requests
import json
from typing import List

class SilentPaymentsScanner:
    """
    Educational SP Scanner
    
    WARNING: This is naive and slow. Real implementations like Kyoto
    are much more sophisticated. This is to understand the concept.
    """
    
    def __init__(self, sp_private_key: bytes):
        self.sp_private_key = sp_private_key
        self.sp_outputs_found = []
    
    def scan_block(self, block_data: dict) -> List[dict]:
        """
        Scan a single block for SP outputs.
        
        For each transaction in the block:
        - Extract outputs
        - Test if output is intended for this SP receiver
        
        Returns list of found outputs
        """
        found = []
        
        for tx in block_data['tx']:
            for vout_idx, output in enumerate(tx['vout']):
                if self.is_sp_output_for_me(output):
                    found.append({
                        'txid': tx['txid'],
                        'vout': vout_idx,
                        'amount': output['value'],
                        'scriptPubKey': output['scriptPubKey']['hex']
                    })
        
        return found
    
    def is_sp_output_for_me(self, output: dict) -> bool:
        """
        Test if an output is a Silent Payment for this receiver.
        
        Algorithm:
        1. Extract the output's public key
        2. Try to decrypt/verify it matches our key
        3. Return True if it does
        
        (This is simplified; real implementation is more complex)
        """
        # Extract public key from output script
        script = output['scriptPubKey']['hex']
        
        # Check if it's P2TR (Taproot)
        if not script.startswith('5120'):
            return False
        
        pubkey = bytes.fromhex(script[4:])  # Skip OP_1 + length
        
        # Test if pubkey matches one of our SP outputs
        # (Real implementation uses ECDH to derive expected keys)
        return self.test_pubkey(pubkey)
    
    def test_pubkey(self, pubkey: bytes) -> bool:
        """
        Test if a public key was derived for this SP address.
        
        Requires:
        - Our scanning private key
        - The sender's inputs (for shared secret)
        - ECDH computation
        """
        # Implementation would use ECDH here
        pass
    
    def scan_blockchain(self, height_start: int, height_end: int):
        """
        Scan a range of blocks for SP outputs.
        
        Real implementation would:
        - Use BIP157 filters to skip irrelevant blocks
        - Parallelize ECDH computation
        - Cache results
        """
        for block_height in range(height_start, height_end + 1):
            block_data = self.fetch_block(block_height)
            outputs = self.scan_block(block_data)
            self.sp_outputs_found.extend(outputs)
    
    def fetch_block(self, height: int) -> dict:
        """
        Fetch block data from a block explorer or node.
        """
        # Use mempool.space API or bitcoin-cli
        url = f"https://mempool.space/api/block/{height}"
        response = requests.get(url)
        return response.json()
```

**Step 6:** Understand filter optimization:

```python
class FilterOptimizedScanner(SilentPaymentsScanner):
    """
    Optimized scanner using BIP157 compact block filters.
    
    Instead of scanning all transactions, use pre-computed filters
    to skip irrelevant blocks.
    """
    
    def get_filter_for_block(self, block_hash: str) -> bytes:
        """
        Get BIP157 compact block filter for a block.
        
        BIP157 filters are ~20KB per block and can be downloaded quickly.
        They tell us: "This block might contain outputs to P2TR addresses"
        """
        # Fetch from filter server
        url = f"https://filter.server/cfilter/{block_hash}"
        return requests.get(url).content
    
    def test_filter(self, cfilter: bytes, pubkey: bytes) -> bool:
        """
        Test if a pubkey might be in a block's filter.
        
        Returns False = definitely not in block
        Returns True = maybe in block (need to download)
        """
        # BIP157 Golomb-Rice coded set test
        # Check if pubkey hash is in the filter
        pass
    
    def scan_blockchain_with_filters(self, height_start: int, 
                                     height_end: int):
        """
        Optimized scan: only download and test blocks that
        might contain our outputs.
        """
        for height in range(height_start, height_end + 1):
            block_hash = self.get_block_hash(height)
            cfilter = self.get_filter_for_block(block_hash)
            
            # If filter matches, we need to fetch full block data
            if self.test_filter(cfilter, self.get_search_key()):
                block_data = self.fetch_block(height)
                self.scan_block(block_data)
```

**Step 7:** Compare scanning approaches:

| Approach | Privacy | Speed | Complexity | Tools |
|---|---|---|---|---|
| **Full node scanning** | Perfect | Slow | High | Bitcoin Core + SP patch |
| **BIP157 filters** | Very good | Fast | Medium | Kyoto, Electrum (with SP) |
| **Server-assisted** | Good | Very fast | Low | Cake Wallet, Floresta |
| **Wallet API** | Limited | Instant | Very low | Centralized wallet |

**Step 8:** Document your findings:

```
SCANNING APPROACH ANALYSIS:

For my use case (mobile + privacy):
- Best: Kyoto with BIP157 filters
  (Privacy: 9/10, Speed: 8/10, Complexity: 6/10)

Why not full node scanning?
- Mobile doesn't have CPU/storage for full node
- Scanning would take hours

Why not wallet API?
- Server learns exactly which outputs you own
- Privacy: 2/10

Recommendation:
- Use Kyoto or similar for production
- Test full node scanning locally for development
```

### Open a PR This Week

**Contribute to Light Client Scanning**

1. Visit https://github.com/rustaceanrob/kyoto 
   OR https://github.com/commerceblock/floresta
2. Pick one of:
   - Add documentation for SP scanning architecture
   - Implement BIP157 filter testing (if not present)
   - Add test cases for scanning edge cases (no payments, multiple payments per block, etc.)
   - Optimize filter matching for performance
3. Research existing issues tagged "scanning" or "performance"
4. Submit PR with code + documentation

**Alternative:** Contribute to Bitcoin Core
1. Go to https://github.com/bitcoin/bitcoin/pull/28122 (Silent Payments PR)
2. Add documentation or test cases for scanning performance
3. Propose optimizations for light client support
4. Submit PR

### Daily Life Privacy Tip

**Use Cake Wallet to see Silent Payments scanning in action.**

Cake Wallet handles all scanning internally:

1. Open Cake Wallet
2. Create a Bitcoin wallet
3. Go to Receive and copy your SP address
4. Send a small amount of Bitcoin to it (on testnet)
5. Watch the wallet's status as it scans
6. Your payment will appear once scan is complete

This shows you: Silent Payments are practical today, and scanning is handled transparently. Cake Wallet's app doesn't slow down, even with SP enabled.

### Reading List with Links

1. **BIP352 Scanning (Section 3)**  
   https://github.com/bitcoin/bips/blob/master/bip-0352.md#scanning
   - Receiver scanning algorithm specification

2. **BIP157: Compact Block Filters**  
   https://github.com/bitcoin/bips/blob/master/bip-0157.md
   - Filter-based block scanning optimization

3. **Kyoto Light Client**  
   https://github.com/rustaceanrob/kyoto
   - Production-ready Rust implementation with SP support

4. **Floresta: Utreexo-Based Light Client**  
   https://github.com/commerceblock/floresta
   - Alternative approach to efficient scanning

5. **"Silent Payments Scanning Optimization" — Bitcoin Optech**  
   https://bitcoinops.org/en/newsletters/2024/01/10/#silent-payments-scanning-optimization
   - Latest research on efficient scanning

6. **Cake Wallet Architecture**  
   https://cakewallet.com/articles/technical-details
   - How production wallet implements SP scanning

7. **BDK (Bitcoin Dev Kit) — Wallet Framework**  
   https://github.com/bitcoindevkit/bdk
   - Wallet library with SP support (in development)

---

## Session 8: Contributing to Silent Payments

### Real-World Scenario

**The Production Moment**  
Your Silent Payments implementation is tested. You've submitted PRs. Now comes the hard part: getting your code merged into production. Bitcoin Core PR #28122 has 50+ comments. You need to address reviewer feedback on cryptographic correctness, test coverage, and performance. A wallet developer is waiting for your light client optimization to improve their app's speed. A freelancer's platform is ready to deploy Silent Payments but needs wallet integration. This session is about professional-grade contribution: understanding the Bitcoin development process, responding to code reviews, ensuring production readiness, and getting your privacy infrastructure into the hands of users.

### Learning Objectives

By the end of Session 8, you will:
- Understand the Bitcoin Core development and review process
- Know which Silent Payments repositories are most impactful
- Write production-ready code with comprehensive tests
- Respond professionally to code review feedback
- Know the path to getting features merged and deployed
- Build a portfolio of Privacy infrastructure contributions

### Privacy Tools You'll Use

- **Bitcoin Core** (https://github.com/bitcoin/bitcoin)
  - PR #28122: Silent Payments (in active review)
  - PR #30152: BIP352 integration (planned/in progress)
- **rust-silentpayments** (https://github.com/cygnet3/rust-silentpayments)
  - Reference implementation, good for tests and examples
- **Sparrow Wallet** (https://github.com/sparrowwallet/sparrow)
  - Upcoming Silent Payments support
- **Cake Wallet** (https://github.com/cake-tech/cake_wallet)
  - Production Silent Payments wallet
- **Bitcoin Optech** (https://bitcoinops.org/)
  - Tracking implementation status and PRs

### Hands-On Exercise: "Professional Contribution Workflow"

**Part 1: Understand the Contribution Landscape**

**Step 1:** Map existing Silent Payments PRs:
```
SILENT PAYMENTS CONTRIBUTION MAP:

Bitcoin Core:
  - PR #28122: Full BIP352 implementation (in review since 2023)
    Status: Core implementation, active review
    Needs: Testing, documentation, optimization
    Impact: HIGHEST (enables all other implementations)
  
  - PR #30152: Additional improvements (TBD)
    Status: Planned
    Needs: TBD

Rust Reference:
  - rust-silentpayments (https://github.com/cygnet3/rust-silentpayments)
    Status: Production ready
    Needs: Wallet integration, testing

Wallets:
  - Cake Wallet: Already ships SP (complete)
  - Sparrow Wallet: SP planned (https://github.com/sparrowwallet/sparrow)
    Needs: Integration, testing
  - Bitcoin Core: Integrated in PR #28122

Light Clients:
  - Kyoto: SP support ready
    Needs: Documentation, optimization
  - Floresta: SP planned
    Needs: Implementation, testing
```

**Step 2:** Read Bitcoin Core PR #28122:
- Go to https://github.com/bitcoin/bitcoin/pull/28122
- Read the initial description
- Scroll through comments (50+)
- Note: What are reviewers asking for?
  - Test coverage
  - Documentation
  - Performance
  - Cryptographic correctness

**Step 3:** Evaluate the top 3 contribution opportunities:
```
OPPORTUNITY 1: Bitcoin Core Test Coverage
Impact: HIGH (PR #28122 is blocked on test completeness)
Difficulty: MEDIUM
Path: Write comprehensive test cases for sender/receiver protocol
Time: 20-40 hours
Expected result: PR merged, feature in Bitcoin Core

OPPORTUNITY 2: Sparrow Wallet Integration
Impact: MEDIUM (wallet used by 50k+ users)
Difficulty: MEDIUM
Path: Implement SP receiver in Sparrow, test with rust-silentpayments
Time: 30-50 hours
Expected result: SP support in next Sparrow release

OPPORTUNITY 3: Light Client Optimization
Impact: MEDIUM (Kyoto + Floresta need performance work)
Difficulty: HARD
Path: Optimize filter matching, parallelize ECDH
Time: 40-60 hours
Expected result: Mobile SP wallets that scan in <1 minute

OPPORTUNITY 4: Documentation
Impact: MEDIUM (SP is hard to understand; docs help adoption)
Difficulty: LOW
Path: Write guides, test vectors, protocol explainers
Time: 10-20 hours
Expected result: Bitcoin Optech article, Sparrow docs, community appreciation
```

**Part 2: Detailed Walkthrough - Bitcoin Core Test Contribution**

**Step 4:** Clone Bitcoin Core and examine test structure:
```bash
git clone https://github.com/bitcoin/bitcoin.git
cd bitcoin
git checkout origin/PR-28122  # or latest commit from PR

# Find Silent Payments test files
find . -name "*silent*" -o -name "*sp*"

# Likely files:
# src/test/silentpayments_tests.cpp
# src/wallet/test/sp_wallet_tests.cpp
```

**Step 5:** Understand the test structure:
```cpp
// Example Bitcoin Core test structure:

#include <boost/test/unit_test.hpp>
#include <silentpayments.h>

BOOST_FIXTURE_TEST_SUITE(silentpayments_tests, BasicTestingSetup)

BOOST_AUTO_TEST_CASE(sp_address_encoding)
{
    // Test valid SP address encoding/decoding
    std::string sp_addr = "sp1qq...";
    auto [scan_key, spend_key] = DecodeSilentPaymentsAddress(sp_addr);
    
    // Verify round-trip encoding
    auto reencoded = EncodeSilentPaymentsAddress(scan_key, spend_key);
    BOOST_CHECK_EQUAL(sp_addr, reencoded);
}

BOOST_AUTO_TEST_CASE(sp_sender_protocol)
{
    // Test sender deriving output
    // ...
}

BOOST_AUTO_TEST_CASE(sp_receiver_scanning)
{
    // Test receiver finding payments
    // ...
}

BOOST_AUTO_TEST_SUITE_END()
```

**Step 6:** Write a new test case for edge cases:
```cpp
BOOST_AUTO_TEST_CASE(sp_multiple_payments_same_block)
{
    // Test: Receiver gets 3 payments in same block
    // All should be correctly identified and spendable
    
    std::string sp_address = "sp1qq...";
    
    // Create 3 transactions to same SP address
    CMutableTransaction tx1, tx2, tx3;
    // ... populate tx1, tx2, tx3 ...
    
    // Create block containing all 3
    CBlock block;
    block.vtx.push_back(MakeTransactionRef(tx1));
    block.vtx.push_back(MakeTransactionRef(tx2));
    block.vtx.push_back(MakeTransactionRef(tx3));
    
    // Scan block
    auto outputs = ScanBlockForSilentPayments(block, sp_address);
    
    // Verify
    BOOST_CHECK_EQUAL(outputs.size(), 3);
    
    // Verify all outputs are different
    std::set<CPubKey> output_keys;
    for (auto& output : outputs) {
        output_keys.insert(output.pubkey);
    }
    BOOST_CHECK_EQUAL(output_keys.size(), 3);  // All unique
}
```

**Step 7:** Run the test suite:
```bash
cd bitcoin
./configure
make
make test TESTS_WANTJOUR=silentpayments_tests

# Should show:
# PASS: silentpayments_tests
# Ran 47 test cases
```

**Step 8:** Create a GitHub issue for test coverage gaps:
1. Go to https://github.com/bitcoin/bitcoin/issues
2. Search for existing issues about SP testing
3. If not found, create one:
```
Title: "Silent Payments: Test coverage for [specific scenario]"

Body:
BIP352 requires testing for:
- [ ] Multiple payments in single block (done in Session 8)
- [ ] Multiple payments in multiple blocks
- [ ] Maximum output count (999)
- [ ] Address encoding/decoding round-trip
- [ ] Fee calculation with SP outputs
- [ ] Integration with coin selection

Currently missing: [List what you'll add]
```

**Part 3: Code Review Response Workflow**

**Step 9:** Get feedback on your PR:
When you submit a PR to Bitcoin Core or a wallet, reviewers will comment. Example:

```
Reviewer comment:
"Have you tested this against all BIP352 test vectors?
I don't see test cases for failure scenarios."
```

**Step 10:** Respond professionally:
```
Response:
"Good point. I've added the following:

1. Test cases for all vectors in bip-0352/vectors.json
2. Failure scenarios:
   - Invalid SP address format → correct error message
   - Mismatched sender/receiver keys → output not found
   - Corrupted block data → graceful handling

See commits [xxx], [yyy], [zzz] for changes."
```

**Step 11:** Update your PR with improvements:
```bash
git checkout your-feature-branch
# Make improvements based on feedback
git add src/test/silentpayments_tests.cpp
git commit -m "test: Add failure scenario tests for Silent Payments"
git push origin your-feature-branch
# GitHub automatically updates PR
```

### Open a PR This Week

**Make Your Final Contribution**

Choose ONE of these production-grade contributions:

**Option A: Bitcoin Core PR #28122 Enhancement**
1. Read the PR and comments carefully
2. Identify a specific gap (test coverage, documentation, optimization)
3. Create a focused PR that addresses that gap
4. Example: "test: Add test cases for [specific scenario]"
5. Submit to bitcoin/bitcoin

**Option B: Sparrow Wallet Integration**
1. Fork https://github.com/sparrowwallet/sparrow
2. Add Silent Payments receiver support
3. Integrate with rust-silentpayments library
4. Test against Cake Wallet SP address
5. Submit PR with comprehensive tests

**Option C: Light Client Optimization**
1. Fork https://github.com/rustaceanrob/kyoto
2. Optimize scanning (parallelize ECDH, improve filters)
3. Benchmark before/after
4. Document improvements
5. Submit PR

**Option D: Documentation/Educational**
1. Create a comprehensive SP guide
2. Real-world examples (podcast donations, freelancer invoicing, merchant payments)
3. Compare to other privacy solutions
4. Submit as Bitcoin Optech article, Sparrow docs, or GitHub wiki
5. Quality bar: 3000+ words, multiple code examples

All options should:
- Have comprehensive tests
- Include documentation
- Be production-ready
- Be reviewed by community before merging

### Daily Life Privacy Tip

**Follow Bitcoin Core development and Silent Payments progress.**

Subscribe to:
1. Bitcoin Optech Newsletter (weekly): https://bitcoinops.org/en/newsletters/
2. Bitcoin Core PR #28122: https://github.com/bitcoin/bitcoin/pull/28122 (watch for updates)
3. Sparrow Wallet releases: https://www.sparrowwallet.com/
4. Cake Wallet releases: https://cakewallet.com/

When a feature is released:
- Test it immediately
- Report bugs
- Give feedback
- Help improve the implementation

Silent Payments deployment is happening NOW. Your involvement speeds up the process.

### Reading List with Links

1. **Bitcoin Core PR #28122: Silent Payments**  
   https://github.com/bitcoin/bitcoin/pull/28122
   - The main Silent Payments implementation effort

2. **Bitcoin Core Contribution Guide**  
   https://github.com/bitcoin/bitcoin/blob/master/CONTRIBUTING.md
   - How to submit PRs to Bitcoin Core

3. **Effective Bitcoin Core PR Review**  
   https://bitcoinops.org/en/newsletters/2022/01/05/#effective-bitcoin-core-pr-review
   - Understanding the review process

4. **rust-silentpayments Examples**  
   https://github.com/cygnet3/rust-silentpayments/tree/master/examples
   - Real-world usage examples

5. **Sparrow Wallet Contribution Guide**  
   https://github.com/sparrowwallet/sparrow/blob/master/CONTRIBUTING.md
   - How to contribute to Sparrow

6. **Bitcoin Optech Silent Payments Status**  
   https://bitcoinops.org/en/topics/silent-payments/
   - Current implementation status across projects

7. **Code Review Best Practices**  
   https://google.github.io/eng-practices/review/reviewer/
   - How to respond to and incorporate feedback

---

## Phase 2 Capstone Project

### Your Mission

Submit a **production-grade Silent Payments contribution** that ships in a real Bitcoin wallet or tool:

**Required:**
1. **Implement** sender, receiver, or light client component
2. **Test** with comprehensive test cases (minimum 50+ tests)
3. **Document** algorithm and usage clearly
4. **Submit as PR** to Bitcoin Core, Sparrow, Kyoto, or equivalent
5. **Engage professionally** with code reviewers
6. **Achieve merge** or get clear feedback path to merge

**Deliverables:**
- [ ] Complete, tested implementation
- [ ] Pull request to production repository
- [ ] Code review engagement (respond to 5+ comments)
- [ ] Comprehensive test suite
- [ ] Documentation (algorithm, usage, examples)
- [ ] Evidence of merge or clear merge path

### Success Metrics

- Code follows Bitcoin Core/wallet coding standards
- All tests pass
- Implements BIP352 correctly (against test vectors)
- Documentation is clear to external developers
- Community engagement shows maturity

---

## Getting Help

- **Bitcoin Optech**: https://bitcoinops.org/
- **Bitcoin Core PR #28122**: https://github.com/bitcoin/bitcoin/pull/28122
- **Cake Wallet**: https://github.com/cake-tech/cake_wallet
- **Sparrow Wallet**: https://github.com/sparrowwallet/sparrow
- **Kyoto**: https://github.com/rustaceanrob/kyoto
- **Bitcoin Core Slack**: https://bitcoincoredev.slack.com/ (ask to join)

---

## Beyond Phase 2

After completing Phase 2, you're ready for advanced privacy infrastructure:
- Layer 2 privacy (Lightning Network on private channels)
- Mixing protocols (CoinJoin variants)
- Cross-chain atomic swaps with privacy
- ZK-proof-based systems (future Bitcoin research)

The knowledge you've built—chain analysis, transaction structure, UTXO management, cryptography, and production development—applies to all of these.

You're now a **Bitcoin Privacy Infrastructure Developer**. Use this power responsibly.
