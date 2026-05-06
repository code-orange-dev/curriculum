# Phase 4: Network & Protocol Privacy — Sessions 13-16

**Objective:** Master the network and protocol layers of Bitcoin privacy, learning how to hide transaction broadcast origins, discover addresses privately, and use Taproot for script obfuscation.

**Why This Matters:** Payjoin solves "who paid whom" (Phase 3). But attackers still ask: "Who broadcast this transaction?" and "What addresses does this person own?" Phase 4 attacks these questions with Dandelion++, Compact Block Filters, light clients, and Taproot. By the end, you'll understand that true privacy requires layers: transaction privacy, network privacy, and scriptpubkey privacy working together.

---

## Session 13: P2P Network Privacy (Dandelion++, Tor, I2P)

### Real-World Scenario

**The Attack:**
You create a transaction and broadcast it to the Bitcoin network. Your ISP-level adversary listens:
- They capture all traffic from your IP address
- They see a Bitcoin transaction leave your computer to multiple peers
- They match the timing and content
- They now know: "The person at IP 192.168.1.100 created transaction 0xabc123"

Even if they can't link the transaction to your identity initially, they've created a powerful surveillance vector. They can correlate your IP with your behavior on other platforms.

**The Solution:**
You enable Dandelion++ (RFC 6979 for Bitcoin) or route through Tor/I2P:
- Dandelion++ has two phases: "stem" (hops through 3-5 random nodes) and "fluff" (normal broadcast)
- An attacker needs to observe multiple transactions to derive the source
- Tor/I2P hides your IP entirely behind onion routing

Result: Broadcasting a transaction no longer reveals your IP address.

### Learning Objectives

- Understand how network-level surveillance works (IP address correlation)
- Learn Dandelion++ protocol (stem/fluff phases, anonymity analysis)
- Configure Bitcoin Core to broadcast over Tor
- Set up I2P integration with Bitcoin Core
- Measure network privacy properties (latency vs. anonymity tradeoffs)

### Privacy Tools You'll Use

- **Bitcoin Core** — full node with Tor/I2P support
- **Tor** — onion routing network
- **I2P** — decentralized anonymity network
- **Dandelion++** — transaction broadcast privacy (conceptual)
- **bitcoin-cli getpeerinfo** — peer analysis
- **tcpdump** — network traffic inspection

### Detailed Hands-On Exercise

**Part 1: Understand the Attack**

1. **Set up network monitoring:**
   ```bash
   # Start Bitcoin Core on testnet (not production)
   bitcoind -testnet -listen -upnp=0

   # In another terminal, monitor peer connections
   bitcoin-cli -testnet getpeerinfo | jq '.[] | {addr: .addr, inbound: .inbound_onion}'
   ```

2. **Create a transaction and observe broadcast:**
   ```bash
   # Send a test transaction
   bitcoin-cli -testnet sendtoaddress $(bitcoin-cli -testnet getnewaddress) 0.001

   # Verify it propagates to peers
   bitcoin-cli -testnet getrawmempool | jq '.[] | select(. == "YOUR_TXID")'
   ```

3. **Document what an observer sees:**
   - Your IP address connects to Bitcoin peers
   - Transaction broadcast originates from your IP
   - Timing correlates with your transaction creation
   - Conclusion: Your IP likely owns this transaction

**Part 2: Configure Tor in Bitcoin Core**

1. **Install Tor** (macOS/Linux):
   ```bash
   # macOS
   brew install tor

   # Linux (Ubuntu)
   sudo apt-get install tor
   ```

2. **Start Tor:**
   ```bash
   tor  # Run in background
   ```

3. **Configure Bitcoin Core for Tor** (bitcoin.conf):
   ```
   # Use Tor for outgoing connections
   proxy=127.0.0.1:9050

   # Listen as a Tor hidden service
   listen=1
   bind=127.0.0.1
   onlynet=onion

   # Optional: use specific onion address
   externalip=YOUR_ONION_ADDRESS.onion
   ```

4. **Restart Bitcoin Core:**
   ```bash
   bitcoind -testnet -conf=/path/to/bitcoin.conf
   ```

5. **Verify Tor integration:**
   ```bash
   bitcoin-cli -testnet getnetworkinfo | grep onion
   ```

**Part 3: Set Up I2P (Advanced)**

1. **Install I2P:**
   ```bash
   # Download from https://geti2p.net
   # Or: brew install i2p (macOS)
   i2pd  # Run i2p daemon
   ```

2. **Configure Bitcoin for I2P** (bitcoin.conf):
   ```
   i2psam=127.0.0.1:7656
   onlynet=i2p
   ```

3. **Monitor I2P connections:**
   ```bash
   bitcoin-cli -testnet getnetworkinfo | jq '.networks[] | select(.name == "i2p")'
   ```

**Part 4: Understand Dandelion++ (Conceptual)**

While Bitcoin Core doesn't implement Dandelion++ yet, understand the protocol:

1. **Dandelion++ Phases:**
   - Stem phase: transaction hops through 3-5 random nodes before broadcast
   - Fluff phase: normal gossiping to the network
   - Goal: Attacker needs to observe multiple transactions to trace back to source

2. **Create a document explaining:**
   - Why stem phase provides anonymity
   - How an attacker could break Dandelion++ (observe full stem chain)
   - Why combining Dandelion++ + Tor is optimal

3. **Pseudocode for Dandelion++ flow:**
   ```
   When creating a transaction:
   ├─ Choose random peer for stem phase (probability p)
   ├─ If stem: send to peer (don't broadcast yet)
   ├─ If fluff: normal broadcast to all peers
   └─ After stem timeout (60-300s):
      ├─ If you're still in stem: flip coin
      │  ├─ Heads: continue stem to next random peer
      │  └─ Tails: start fluff phase
      └─ If you're not original sender: flip coin
         ├─ Heads: relay to random peer (continue stem)
         └─ Tails: start fluff phase
   ```

**Part 5: Measure Privacy Properties**

1. **Compare broadcast patterns:**
   - Standard Bitcoin Core: Observe latency from node to all peers
   - Tor: Random latency, harder to trace
   - I2P: Even higher variance
   - Dandelion++: Asymmetric—harder to measure

2. **Create a test:**
   - Send 5 transactions without Tor
   - Send 5 transactions with Tor
   - Measure: average peer count, broadcast latency, peer address diversity
   - Document findings

3. **Privacy analysis:**
   ```markdown
   # Network Privacy Test Results

   ## Standard (clearnet)
   - Peers: 10
   - Broadcast latency: 0-50ms (low variance)
   - Conclusion: Easy to fingerprint source IP

   ## Tor
   - Peers: 5 (Tor peers only)
   - Broadcast latency: 500-2000ms (high variance)
   - Conclusion: Source IP hidden, but Tor analysis possible

   ## Best Practice
   - Use Tor + Dandelion++ + varying broadcast timing
   - Don't broadcast multiple transactions from same IP quickly
   - Consider batching transactions over time
   ```

### Open a PR This Week

**Target: bitcoin/bitcoin**

1. **Navigate to:**
   - https://github.com/bitcoin/bitcoin/issues
   - Filter by label: "P2P" or "privacy"

2. **Common contributions:**
   - Improve Tor/I2P documentation in bitcoin.conf comments
   - Add test cases for Tor peer connection
   - Document Dandelion++ research in comments

3. **Example PR:**
   - Improve `bitcoin.conf.example` with detailed Tor/I2P section
   - Include examples of `proxy=`, `listen=`, `onlynet=` configuration
   - Add privacy implications for each setting

**OR Target: bitcoin-core/secp256k1 or protocol research**

- Write research doc on Dandelion++ anonymity analysis
- Create implementation proposal for Dandelion++ in Bitcoin Core

### Daily Life Privacy Tip

**Run Bitcoin Core Over Tor Today**

If you run a node:

1. **Install Tor:**
   ```bash
   brew install tor  # macOS
   sudo apt-get install tor  # Ubuntu
   ```

2. **Edit bitcoin.conf:**
   ```
   proxy=127.0.0.1:9050
   listen=1
   onlynet=onion
   ```

3. **Restart Bitcoin Core**

4. **Verify:**
   ```bash
   bitcoin-cli getnetworkinfo | grep "onion\|ipv4"
   ```

Result: Your transactions are broadcast through Tor. An ISP-level observer can no longer correlate your IP with your transactions.

### Reading List

- **Dandelion++ Paper:** https://arxiv.org/abs/1805.11060
- **Bitcoin Wiki - Tor:** https://en.bitcoin.it/wiki/Tor
- **Bitcoin Core I2P Support:** https://github.com/bitcoin/bitcoin/pull/20685
- **Tor Project:** https://www.torproject.org
- **I2P Project:** https://geti2p.net
- **Bitcoin Core bitcoin.conf Guide:** https://github.com/bitcoin/bitcoin/blob/master/share/examples/bitcoin.conf
- **Network Surveillance Risks:** https://en.bitcoin.it/wiki/Privacy

---

## Session 14: Compact Block Filters (BIP157/158)

### Real-World Scenario

**The Problem:**
You want to use a mobile Bitcoin wallet without running a full node. Traditional SPV (Simple Payment Verification) wallets:
- Connect to a server
- Send all their addresses to the server
- The server responds with relevant transactions
- Result: "The server now knows all of my addresses"

This is worse than Payjoin or Tor can fix. Your address privacy is compromised at the source.

**The Solution:**
Compact Block Filters (BIP157/158) let you discover which transactions are yours without revealing which addresses you own:

1. Full nodes create filter sets for each block (Golomb-Rice coded)
2. Light clients download filters, not addresses
3. Light clients scan filters locally: "Is transaction X relevant to me?"
4. Result: "I see which transactions might be mine, without the server knowing which addresses I own"

Privacy moves from "trust the server" to "trust the math."

### Learning Objectives

- Understand why SPV wallets leak address privacy
- Learn the Golomb-Rice coding scheme for filters
- Understand BIP157 (filter creation) and BIP158 (filter format)
- Build a Golomb-Rice encoder/decoder from scratch
- Implement filter scanning in a light client

### Privacy Tools You'll Use

- **Compact Block Filters (BIP157/158)** — filter specification
- **Kyoto** — Rust light client with CBF support
- **Floresta** — Utreexo-based light client
- **Neutrino** (LND) — Lightning client with CBF support
- **Python/Rust** — filter implementation

### Detailed Hands-On Exercise

**Part 1: Understand the Privacy Problem**

1. **Traditional SPV (Breaks Privacy):**
   ```
   Light Client                    Server
   ├─ "Do you have txs for:"      →
   ├─ " - addr1"
   ├─ " - addr2"
   ├─ " - addr3"
   └─ " - addr4"
   
   Server sees all 4 addresses.
   Server now knows: "This person owns these addresses"
   ```

2. **Compact Block Filters (Preserves Privacy):**
   ```
   Full Node            Light Client
   ├─ Filter(block 1)   →
   ├─ Filter(block 2)   →
   ├─ Filter(block 3)   →
   └─ Filter(block N)   →
   
   Light Client filters locally:
   ├─ Check: "Do I have addr1?"
   ├─ Check: "Do I have addr2?"
   ├─ If "yes", download full block
   
   Server never learns which addresses you own.
   ```

3. **Document the trade-off:**
   - SPV: Server knows addresses, but small bandwidth
   - CBF: Server doesn't know addresses, slightly larger bandwidth (filters)
   - Result: Worth the bandwidth increase

**Part 2: Build a Golomb-Rice Encoder**

1. **Understand Golomb-Rice coding:**
   - Golomb-Rice code is a compression scheme for integers
   - Parameter M (2^M determines compression ratio)
   - Useful for encoding sparse sets like Bitcoin addresses

2. **Implement in Python (simple version):**
   ```python
   def golomb_rice_encode(value, m):
       """Encode a single value using Golomb-Rice code"""
       q, r = divmod(value, 1 << m)  # value // 2^m, value % 2^m
       
       # Unary code: q ones followed by a zero
       unary = '1' * q + '0'
       
       # Binary code: r in m bits
       binary = bin(r)[2:].zfill(m)
       
       return unary + binary

   def golomb_rice_decode(bitstring, m):
       """Decode Golomb-Rice encoded bitstring"""
       idx = 0
       
       # Count ones (unary part)
       q = 0
       while idx < len(bitstring) and bitstring[idx] == '1':
           q += 1
           idx += 1
       
       # Skip zero separator
       idx += 1
       
       # Read m bits (binary part)
       r = int(bitstring[idx:idx+m], 2)
       
       return (q << m) + r

   # Test
   encoded = golomb_rice_encode(5, 2)  # Encode 5 with m=2
   decoded = golomb_rice_decode(encoded, 2)
   print(f"Encoded 5: {encoded}")
   print(f"Decoded: {decoded}")
   assert decoded == 5
   ```

3. **Build a set encoder:**
   ```python
   def encode_set_as_filter(addresses, m=19):
       """
       Encode a set of addresses as a Golomb-Rice filter
       addresses: list of 32-bit values (hash of addresses)
       m: Golomb-Rice parameter (19 is standard for Bitcoin)
       """
       # Sort addresses
       sorted_addrs = sorted(addresses)
       
       # Encode differences (more compressible than absolute values)
       bitstring = ""
       prev = 0
       for addr in sorted_addrs:
           diff = addr - prev
           bitstring += golomb_rice_encode(diff, m)
           prev = addr
       
       # Convert bitstring to bytes
       # Pad to byte boundary
       bitstring = bitstring.ljust(((len(bitstring) + 7) // 8) * 8, '0')
       
       return bytes(int(bitstring[i:i+8], 2) for i in range(0, len(bitstring), 8))

   # Test
   addresses = [100, 200, 300, 1000, 2000]
   filter_bytes = encode_set_as_filter(addresses, m=4)
   print(f"Filter size: {len(filter_bytes)} bytes for {len(addresses)} addresses")
   ```

**Part 3: Build a Light Client Filter Scanner**

1. **Create a simple filter scanner:**
   ```python
   import hashlib

   def hash_address(address_bytes):
       """Hash an address for filter matching"""
       return int.from_bytes(hashlib.sha256(address_bytes).digest()[:4], 'big')

   def address_in_filter(address_bytes, filter_bytes, m=19):
       """Check if address might be in filter"""
       # Hash the address
       hashed = hash_address(address_bytes)
       
       # Decode filter and check
       # (This is simplified—real implementation more complex)
       filter_values = decode_filter_from_bytes(filter_bytes, m)
       
       # Check for false positives (expected)
       return hashed in filter_values

   # Light client usage:
   my_addresses = [b"addr1", b"addr2", b"addr3"]
   block_filter = receive_filter_from_node()  # Get filter for latest block

   relevant_txns = []
   for address in my_addresses:
       if address_in_filter(address, block_filter):
           # Download full block to verify (false positive check)
           full_block = download_full_block()
           for txn in full_block.txns:
               if contains_address(txn, address):
                   relevant_txns.append(txn)
   ```

**Part 4: Deploy Kyoto or Floresta**

1. **Try Kyoto (Rust light client):**
   ```bash
   git clone https://github.com/rustacean-labs/kyoto.git
   cd kyoto
   cargo build --release

   # Run light client with CBF
   ./target/release/kyoto --network testnet --filters
   ```

2. **Or Floresta (Utreexo-based):**
   ```bash
   git clone https://github.com/mit-dci/floresta.git
   cd floresta
   cargo build --release

   ./target/release/floresta-cli
   ```

3. **Monitor privacy:**
   - What data does the server see? (Check network logs)
   - What's the bandwidth overhead?
   - How long to sync?

**Part 5: Measure Privacy Properties**

1. **Create a test comparing:**
   - Full node (knows everything, largest bandwidth)
   - SPV wallet (leaks addresses, smallest bandwidth)
   - CBF light client (hides addresses, medium bandwidth)

2. **Document:**
   ```markdown
   # Light Client Privacy Comparison

   | Method | Addresses Leaked | Bandwidth | Sync Time |
   |--------|------------------|-----------|-----------|
   | Full Node | No | ~3.5 GB | 1-2 days |
   | SPV | All | ~50 MB | 1 minute |
   | CBF (Kyoto) | No | ~200 MB | 30 minutes |
   | Floresta | No | ~100 MB | 20 minutes |

   ## Recommendation
   For mobile wallets, CBF (Kyoto/Floresta) is the clear win:
   - Full address privacy (like full node)
   - Reasonable bandwidth (like SPV)
   - Reasonable sync time (between SPV and full node)
   ```

### Open a PR This Week

**Target: bitcoindevkit/bdk or lightningdevkit/ldk**

1. **Navigate to:**
   - https://github.com/bitcoindevkit/bdk/issues (filter "privacy")
   - https://github.com/lightningdevkit/ldk/issues

2. **Common contributions:**
   - Improve CBF documentation
   - Add examples showing privacy properties
   - Write tests for filter correctness
   - Implement missing filter validation

3. **Example PR:**
   - Add comprehensive example: "Using BDK with Compact Block Filters for Privacy"
   - Include code showing filter-based address scanning
   - Compare to SPV privacy implications

### Daily Life Privacy Tip

**Use a CBF-Based Light Client**

If you use mobile Bitcoin:

1. **Install Kyoto** (if available on your platform):
   ```bash
   # iOS/Android via companion app
   # Scans blocks using BIP157/158
   ```

2. **Or use Sparrow Wallet** with Private Electrum server

3. **Why:**
   - Your addresses stay private
   - Server can't track which coins you own
   - Full validation (not "trust the server")

### Reading List

- **BIP157 (Client-Side Block Filtering):** https://github.com/bitcoin/bips/blob/master/bip-0157.mediawiki
- **BIP158 (Compact Block Filters):** https://github.com/bitcoin/bips/blob/master/bip-0158.mediawiki
- **Golomb-Rice Coding:** https://en.wikipedia.org/wiki/Golomb_coding
- **Kyoto:** https://github.com/rustacean-labs/kyoto
- **Floresta:** https://github.com/mit-dci/floresta
- **BDK Documentation:** https://bitcoindevkit.org
- **SPV Privacy Analysis:** https://en.bitcoin.it/wiki/Payment_Verification

---

## Session 15: Light Client Privacy — Floresta & Kyoto

### Real-World Scenario

**Your Constraint:**
You can't run a full node on your phone—it requires ~500GB storage and ~10Mbps constant bandwidth.

**Your Goal:**
You want full validation (don't trust servers) AND address privacy (don't leak which addresses you own).

**Floresta's Solution:**
Floresta uses Utreexo accumulators to compress the UTXO set from ~10GB to ~600MB. Combined with CBF (from Session 14), it becomes a practical light client:
- Download headers only (~5MB)
- Download filters (~200MB)
- Download relevant blocks
- Use Utreexo proofs to verify UTXO validity without full node state
- Result: "Mobile validation with full privacy"

### Learning Objectives

- Understand Utreexo accumulators (tree-based UTXO proofs)
- Deploy Floresta or Kyoto locally
- Query light client for transaction history
- Measure privacy properties vs. SPV
- Contribute to light client ecosystem

### Privacy Tools You'll Use

- **Floresta** — Utreexo-based light client (Rust)
- **Kyoto** — Header-based light client with CBF (Rust)
- **Bitcoin Core** — full node for Utreexo bridge
- **bitcoin-cli** — validation

### Detailed Hands-On Exercise

**Part 1: Understand Utreexo**

1. **The Problem Utreexo Solves:**
   - Full nodes maintain UTXO set (~10GB, grows over time)
   - Light clients need to verify "Is this UTXO valid?" without storing entire set
   - Traditional: Download full UTXO set (impractical)

2. **The Utreexo Solution:**
   - Accumulator: Hash-based proof that UTXO exists without storing all UTXOs
   - Proof size: ~600 bytes per UTXO
   - Verification: Fast (O(log N) operations)

3. **Create a diagram:**
   ```
   Full Node UTXO Set (10GB):
   {UTXO1, UTXO2, UTXO3, ..., UTXO1000000}

   Utreexo Accumulator:
   └─ Root Hash (32 bytes)
      └─ Proof for UTXO42 (600 bytes)
      └─ Proof for UTXO999 (600 bytes)
      └─ Proof for UTXO5000 (600 bytes)

   Light client can verify: "UTXO42 is valid"
   Without storing the full 10GB
   ```

**Part 2: Deploy Floresta**

1. **Clone and build:**
   ```bash
   git clone https://github.com/mit-dci/floresta.git
   cd floresta
   cargo build --release --bin floresta-cli
   ```

2. **Configure Floresta:**
   Create `floresta.toml`:
   ```toml
   [network]
   network = "testnet"  # Use testnet first

   [filters]
   use_compact_filters = true
   filter_cache_dir = "./filter_cache"

   [storage]
   datadir = "./floresta_data"
   assume_utreexo = false  # Set true if you trust genesis UTXO set
   ```

3. **Start Floresta:**
   ```bash
   ./target/release/floresta-cli
   ```

4. **Query wallet:**
   ```bash
   # In Floresta CLI:
   > sync_status
   > get_balance
   > list_unspent
   ```

**Part 3: Test Light Client Privacy**

1. **Create test addresses:**
   ```bash
   # In Floresta
   > getnewaddress
   > getnewaddress
   > getnewaddress
   ```

2. **Have testnet coins sent to your addresses** (use faucet)

3. **Monitor network traffic:**
   ```bash
   # Terminal 1: Floresta
   ./target/release/floresta-cli

   # Terminal 2: Monitor DNS/network
   # macOS
   nettop -p floresta-cli

   # Linux
   tcpdump -i any -n 'tcp port 8333 or 8334'
   ```

4. **Observe:**
   - What data leaves your device?
   - Does the server learn your addresses?
   - What blocks are downloaded?

5. **Document findings:**
   ```markdown
   # Floresta Privacy Test

   Test Environment: Testnet, 1 hour usage

   ## What Server Sees
   - Block headers: Yes (unavoidable)
   - Filter requests: Yes (normal)
   - Address list: NO (Floresta hides)
   - Transaction timing: Partially (you request blocks)

   ## What Server Doesn't See
   - Which specific addresses you own
   - Full transaction history (only relevant blocks)
   - Balance totals
   - Spending patterns

   ## Conclusion
   Floresta provides address privacy superior to SPV,
   comparable to full node, with mobile-friendly bandwidth.
   ```

**Part 4: Compare Implementations**

Create a comparison table:

| Property | Full Node | SPV | Kyoto (CBF) | Floresta (Utreexo) |
|----------|-----------|-----|-------------|-------------------|
| Bandwidth (monthly) | 5 GB | 50 MB | 200 MB | 100 MB |
| Storage | 500 GB+ | 100 MB | 2 GB | 1 GB |
| Validation | Full | Weak | Full (headers) | Full (UTXO proofs) |
| Address Privacy | Yes | No | Yes | Yes |
| Sync Time | 1-2 days | 5 minutes | 2 hours | 1 hour |
| Mobile-Friendly | No | Yes | Partial | Yes |

### Open a PR This Week

**Target: mit-dci/floresta or rustacean-labs/kyoto**

1. **Navigate to:**
   - https://github.com/mit-dci/floresta/issues
   - https://github.com/rustacean-labs/kyoto/issues

2. **Common contributions:**
   - Improve documentation (setup guide, troubleshooting)
   - Write tests for Utreexo proof validation
   - Add examples showing privacy properties
   - Improve error messages

3. **Example PR:**
   - Write "Floresta Mobile Setup Guide" with screenshots
   - Include privacy properties explanation
   - Add troubleshooting section

### Daily Life Privacy Tip

**Deploy Floresta on a Home Server**

If you have a Raspberry Pi or old laptop:

1. **Build Floresta:**
   ```bash
   git clone https://github.com/mit-dci/floresta.git
   cd floresta
   cargo build --release
   ```

2. **Run as daemon:**
   ```bash
   ./target/release/floresta-cli > floresta.log 2>&1 &
   ```

3. **Connect mobile wallet:**
   - Point wallet to your home server
   - Syncs with full privacy
   - You own the infrastructure

### Reading List

- **Floresta GitHub:** https://github.com/mit-dci/floresta
- **Kyoto GitHub:** https://github.com/rustacean-labs/kyoto
- **Utreexo Paper:** https://eprint.iacr.org/2019/611.pdf
- **Compact Block Filters (BIP157/158):** https://github.com/bitcoin/bips/blob/master/bip-0157.mediawiki
- **Bitcoin Core Utreexo Integration:** https://github.com/bitcoin/bitcoin/pull/27050
- **Light Client Privacy Primer:** https://en.bitcoin.it/wiki/Lightweight_client

---

## Session 16: Taproot Privacy — Schnorr, MAST, MuSig2

### Real-World Scenario

**The Visual Problem:**
Alice, Bob, and Carol are business partners sharing a 3-of-3 multisig. On-chain, it looks obviously like a multisig:
```
Script: OP_3 <pubkey1> <pubkey2> <pubkey3> OP_3 OP_CHECKMULTISIG
Size: ~100 bytes (bloated)
Hashing: Recursive (expensive)
```

A chain analyst sees this and immediately knows: "Three people control this address" or "This is a smart contract."

**Taproot's Solution:**
With Taproot, the same 3-of-3 multisig:
1. Uses a "key spend" path (MuSig2): All 3 parties cooperatively spend using a single Schnorr signature
2. The scriptpubkey is just a Schnorr key (32 bytes, identical to single-sig)
3. On-chain: Indistinguishable from a single-signature payment
4. Result: "The 3-of-3 multisig looks identical to a plain payment. It's in the largest anonymity set on Bitcoin."

### Learning Objectives

- Understand Schnorr signatures (BIP340) and why they're better than ECDSA
- Learn Taproot (BIP341) and its privacy implications
- Understand MuSig2 (BIP327) for aggregated signatures
- Build Taproot addresses from scratch
- Use P2TR addresses for maximum privacy

### Privacy Tools You'll Use

- **bitcoin-cli** — create Taproot addresses and transactions
- **Sparrow Wallet** — full Taproot support
- **bitcoinjs-lib** (JavaScript) — Taproot construction
- **rust-bitcoin** — Taproot primitives
- **libsecp256k1-zkp** — Schnorr signatures

### Detailed Hands-On Exercise

**Part 1: Understand Schnorr Signatures**

1. **Why Schnorr > ECDSA for Privacy:**

   **ECDSA (Bitcoin legacy):**
   - Signature: (r, s) — two 32-byte values
   - Different signatures for same key/message (randomness in signing)
   - Non-linear signature equation (harder to aggregate)

   **Schnorr (Taproot):**
   - Signature: (R, s) — one 32-byte point + one 32-byte scalar
   - Deterministic signatures (same input → same signature)
   - Linear equation (easy to aggregate multiple signatures)

2. **Create a comparison table:**
   ```
   | Property | ECDSA | Schnorr |
   |----------|-------|---------|
   | Signature size | 72 bytes | 64 bytes |
   | Aggregation | Impossible | BIP327 (MuSig2) |
   | Hashing | Legacy (SigHash) | Modern (BIP341) |
   | Privacy | Reveals key type | Hidden script |
   | Adoption | Legacy | Taproot |
   ```

3. **Understand the math** (simplified):
   ```
   ECDSA signature: (r, s)
   where s = k^-1 (h + r*x) mod n
   (k is random, so different s each time)

   Schnorr signature: (R, s)
   where s = k + h*x mod n
   where R is the public point k*G
   (k is random, but signature is deterministic in x)

   Key insight: With Schnorr, you can aggregate:
   sig1 = k1 + h*x1
   sig2 = k2 + h*x2
   combined_sig = (k1+k2) + h*(x1+x2) = k_combined + h*x_combined
   (This is impossible with ECDSA)
   ```

**Part 2: Build Taproot Addresses**

1. **Using bitcoin-cli (testnet):**
   ```bash
   # Start Bitcoin Core on testnet
   bitcoind -testnet -server

   # Create a new Taproot address
   bitcoin-cli -testnet createwallet test_taproot
   bitcoin-cli -testnet -rpcwallet=test_taproot getnewaddress "" bech32m

   # Verify it's P2TR (starts with 'tb1p' on testnet)
   # Example: tb1pzzr4m4gts9d3j5qvpwd6qw8mvqxlgx7mlhpfchqwyz8p4wc65lgsx3lnsm
   ```

2. **Using Sparrow Wallet (GUI):**
   - Open Sparrow
   - Create new wallet
   - Settings → Script type → P2TR (Pay to Taproot)
   - Generate address
   - All addresses are now Taproot

3. **Using rust-bitcoin (programmatic):**
   ```rust
   use bitcoin::PublicKey;
   use bitcoin::taproot::TaprootBuilder;
   use bitcoin::key::Secp256k1;

   let secp = Secp256k1::new();
   let (secret_key, public_key) = secp.generate_keypair(&mut rand::thread_rng());

   // Create a simple Taproot key-only address
   let builder = TaprootBuilder::new().finalize(&secp, public_key).unwrap();
   let taproot_address = bitcoin::Address::p2tr(&secp, public_key, None, bitcoin::Network::Testnet);

   println!("Taproot address: {}", taproot_address);
   ```

**Part 3: Understand Taproot Privacy**

1. **Script Types on Bitcoin:**

   **Pre-Taproot:**
   ```
   P2PKH: OP_DUP OP_HASH160 <pubkeyhash> OP_EQUALVERIFY OP_CHECKSIG
   P2SH: OP_HASH160 <scripthash> OP_EQUAL
   P2WPKH: <pubkeyhash> (witness)
   P2WSH: <scripthash> (witness)
   ```
   - All different sizes/formats
   - Analyst can see: "This is multisig" vs "This is single-sig" vs "This is contract"

   **Taproot (P2TR):**
   ```
   OP_1 <32-byte-taproot-key>
   ```
   - Everything looks identical
   - Single-sig payment? Could be
   - Multisig? Could be
   - Smart contract? Could be
   - Analyst can't tell

2. **Anonymity Set:**
   - Pre-Taproot: Anonymity set = same script type
   - Taproot: Anonymity set = ALL Taproot transactions (and growing)
   - Benefit: Massive privacy improvement

3. **Create a visualization:**
   ```
   On-chain (2024):
   ├─ P2PKH: 25% (old, declining)
   ├─ P2SH: 20% (old, declining)
   ├─ P2WPKH: 40% (SegWit, standard)
   ├─ P2WSH: 5% (SegWit, multisig)
   ├─ P2TR: 10% (Taproot, growing)
   └─ Other: <1%

   Taproot privacy benefit:
   - Old P2PKH multisig: Anonymity set = P2SH (20% of transactions)
   - New P2TR multisig: Anonymity set = P2TR (10% now, >50% future)
   - By 2026, P2TR will be >50% of transactions
   - All P2TR transactions will look identical on-chain
   ```

**Part 4: Create Taproot Multisig (MuSig2)**

1. **Conceptual: How MuSig2 Works**
   ```
   Alice, Bob, Carol want to create 3-of-3 multisig

   Old way (P2WSH):
   - Alice creates pubkey_alice
   - Bob creates pubkey_bob
   - Carol creates pubkey_carol
   - Script: OP_3 pubkey_alice pubkey_bob pubkey_carol OP_3 OP_CHECKMULTISIG
   - On-chain: ~100 bytes, obviously multisig

   New way (Taproot + MuSig2):
   - Alice, Bob, Carol exchange pubkeys
   - Collaborate to compute aggregate_pubkey = MuSig2(pubkey_alice, pubkey_bob, pubkey_carol)
   - Taproot address: P2TR(aggregate_pubkey)
   - On-chain: 34 bytes, indistinguishable from single-sig
   - To spend: All 3 collaborate to create 1 Schnorr signature
   - Result: Looks like a normal payment on-chain
   ```

2. **Using Sparrow (practical):**
   - Sparrow doesn't yet have full MuSig2 UI, but work is underway
   - For now: Use single-sig P2TR addresses (same privacy benefit)

3. **Using rust-bitcoin (advanced):**
   ```rust
   // MuSig2 requires secp256k1-zkp (not yet in rust-bitcoin)
   // Check: https://github.com/blockstream/secp256k1-zkp
   // For now, prefer single-sig P2TR
   ```

**Part 5: Measure Taproot Impact**

1. **Analyze blockchain:**
   ```bash
   # Count Taproot transactions in recent blocks
   bitcoin-cli -testnet getblockcount
   for i in {0..100}; do
       block=$(bitcoin-cli -testnet getblockhash $(bitcoin-cli -testnet getblockcount | jq '. - 100 + '$i))
       bitcoin-cli -testnet getblock $block | grep -c '"version": 1'  # P2TR outputs
   done
   ```

2. **Create a document:**
   ```markdown
   # Taproot Privacy Analysis

   ## Current State (2026)
   - P2TR adoption: ~25% of UTXOs
   - Anonymity set: All P2TR looks identical

   ## Single-Sig P2TR
   - Address: P2TR(single_pubkey)
   - Cost: 34 bytes (smaller than P2WPKH!)
   - Privacy: In anonymity set with all other P2TR

   ## Multisig P2TR (MuSig2)
   - Address: P2TR(aggregate_pubkey)
   - Cost: 34 bytes (vs 100+ for P2WSH)
   - Privacy: Identical to single-sig on-chain
   - Assumption: User who controls multisig is unknown

   ## Recommendation
   All new addresses should use P2TR for:
   - Maximum privacy
   - Smaller on-chain footprint
   - Better signature aggregation (future)
   ```

### Open a PR This Week

**Target: sparrowwallet/sparrow or bitcoin-core/secp256k1**

1. **For Sparrow:**
   - Improve Taproot address display
   - Add documentation: "Why use P2TR?"
   - Create migration guide from P2WPKH → P2TR

2. **For secp256k1:**
   - Improve Schnorr signature documentation
   - Add examples of signature aggregation concepts

3. **Example PR:**
   - Write comprehensive Taproot guide for Sparrow documentation
   - Include privacy implications
   - Show address creation steps
   - Compare script types visually

### Daily Life Privacy Tip

**Use P2TR Addresses Exclusively**

Effective immediately:

1. **Generate only P2TR addresses:**
   - Sparrow: Settings → Script type → P2TR
   - Bitcoin Core: `getnewaddress "" bech32m`
   - Bull Bitcoin: Automatically P2TR

2. **Why:**
   - Smallest anonymity set (and growing)
   - Smallest on-chain footprint
   - Best future-proofing (MuSig2 support coming)

3. **Migration:**
   - Keep old addresses for receiving
   - Consolidate to P2TR in future Coinjoin

### Reading List

- **BIP340 (Schnorr Signatures):** https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki
- **BIP341 (Taproot):** https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki
- **BIP327 (MuSig2):** https://github.com/bitcoin/bips/blob/master/bip-0327.mediawiki
- **Taproot Privacy Analysis:** https://arxiv.org/pdf/2201.07569.pdf
- **Sparrow Wallet Taproot Support:** https://sparrowwallet.com
- **rust-bitcoin Taproot:** https://docs.rs/bitcoin/latest/bitcoin/taproot/
- **Bitcoin Script Improvements:** https://bitcoin-dev.wiki/w/index.php/Taproot

---

## Phase 4 Summary & Next Steps

**What You've Achieved:**
1. Secured transaction broadcast (Tor, I2P, Dandelion++ concepts)
2. Built address discovery privacy (Compact Block Filters)
3. Deployed light clients (Floresta, Kyoto)
4. Maximized script privacy (Taproot, MuSig2)

**Privacy Layers (Integrated):**
- Transaction: Payjoin (Phase 3) + Taproot (Phase 4) = indistinguishable outputs
- Network: Tor/I2P + Dandelion++ = hidden broadcast origin
- Address: CBF filters + Light clients = no server knows your addresses
- Script: P2TR + MuSig2 = identical to single-sig on-chain

**You've Now Learned:**
- Phase 1: UTXO Management (coin selection, consolidation)
- Phase 2: CoinJoin (mixing, Wasabi, coordination)
- Phase 3: Payjoin (sender/receiver cooperation)
- Phase 4: Network & Protocol Privacy (broadcast, addresses, scripts)

**The Real-World Impact:**
A Bitcoiner who implements all four phases becomes:
- Immune to CIOH analysis (Payjoin)
- Invisible to network surveillance (Tor)
- Hidden from address discovery (CBF)
- Indistinguishable in the largest anonymity set (Taproot)

**Your Next Challenge:**
The best privacy tool is adoption. Your mission now: Build, deploy, and teach others the tools you've learned. Privacy is not a feature—it's a human right.
