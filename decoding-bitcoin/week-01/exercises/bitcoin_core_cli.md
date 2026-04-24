# Decoding Bitcoin — Week 1 Exercises: Bitcoin Core CLI

> Code Orange Dev School | [codeorange.dev](https://codeorange.dev)

## Prerequisites

- Bitcoin Core installed and built from source
- A running regtest node

If you haven't set up your environment yet, follow these steps first:

```bash
# Clone Bitcoin Core
git clone https://github.com/bitcoin/bitcoin.git
cd bitcoin

# Install dependencies (Ubuntu/Debian)
sudo apt-get install build-essential libtool autotools-dev automake pkg-config \
  bsdmainutils python3 libevent-dev libboost-dev libsqlite3-dev

# Build
./autogen.sh
./configure --without-gui
make -j$(nproc)

# Start regtest
./src/bitcoind -regtest -daemon
```

---

## Exercise 1: Start a Regtest Network and Mine Blocks

Regtest (regression test) is a private blockchain that runs on your machine. You control everything — no need to sync with the real network.

### Tasks

**1.1** Start bitcoind in regtest mode:
```bash
bitcoind -regtest -daemon
```

**1.2** Check that the node is running:
```bash
bitcoin-cli -regtest getblockchaininfo
```

**Question**: What is the block height? What is the chain name? What is the difficulty?

**1.3** Create a wallet:
```bash
bitcoin-cli -regtest createwallet "mywallet"
```

**1.4** Mine 101 blocks (you need 100 blocks of maturity before coinbase rewards are spendable):
```bash
bitcoin-cli -regtest -generate 101
```

**Question**: Why 101 and not just 1? What is the coinbase maturity rule and why does it exist?

**1.5** Check your balance:
```bash
bitcoin-cli -regtest getbalance
```

**Question**: How many BTC do you have? Each regtest block reward is 50 BTC. Why is your balance 50 and not 5050?

---

## Exercise 2: Create and Inspect Transactions

**2.1** Generate two addresses:
```bash
bitcoin-cli -regtest getnewaddress "alice"
bitcoin-cli -regtest getnewaddress "bob"
```

**Question**: What type of addresses are these? (Hint: look at the prefix — `bcrt1q` = P2WPKH, `bcrt1p` = P2TR)

**2.2** Send 10 BTC to "bob":
```bash
bitcoin-cli -regtest sendtoaddress <bob_address> 10
```

Save the returned txid.

**2.3** Inspect the transaction before mining:
```bash
bitcoin-cli -regtest gettransaction <txid>
bitcoin-cli -regtest getrawtransaction <txid> true
```

**Question**: What are the fields in the decoded transaction? List each one and explain what it does:
- `txid` — 
- `version` — 
- `vin` (inputs) — 
- `vout` (outputs) — 
- `locktime` — 

**Question**: How many outputs does the transaction have? Why are there more than 1? (Hint: change output)

**2.4** Mine a block to confirm the transaction:
```bash
bitcoin-cli -regtest -generate 1
```

**2.5** Verify the transaction is now confirmed:
```bash
bitcoin-cli -regtest gettransaction <txid>
```

**Question**: What changed in the transaction details after mining?

---

## Exercise 3: Decode a Raw Transaction

**3.1** Get the raw hex of your transaction:
```bash
bitcoin-cli -regtest getrawtransaction <txid>
```

**3.2** Decode it:
```bash
bitcoin-cli -regtest decoderawtransaction <raw_hex>
```

**3.3** Manual decoding challenge:

Take the raw hex and try to identify the following fields by hand. Use this reference:

| Field | Size | Description |
|-------|------|-------------|
| Version | 4 bytes (little-endian) | Transaction version (usually 01000000 or 02000000) |
| Marker | 1 byte | SegWit marker: 00 |
| Flag | 1 byte | SegWit flag: 01 |
| Input count | varint | Number of inputs |
| Inputs | variable | Previous txid (32 bytes, reversed) + vout index (4 bytes) + scriptSig + sequence |
| Output count | varint | Number of outputs |
| Outputs | variable | Value (8 bytes, little-endian, in satoshis) + scriptPubKey |
| Witness | variable | Witness data for each input |
| Locktime | 4 bytes | Transaction locktime |

**YOUR TASK**: Label at least the first 20 bytes of your raw transaction hex. Write out what each byte means.

---

## Exercise 4: Explore a Block

**4.1** Get the best (latest) block hash:
```bash
bitcoin-cli -regtest getbestblockhash
```

**4.2** Get the full block data:
```bash
bitcoin-cli -regtest getblock <blockhash> 2
```

(The `2` parameter gives full transaction details)

**4.3** Answer these questions about the block:
- How many transactions are in the block?
- What is the coinbase transaction? How is it different from a regular transaction?
- What is the `previousblockhash`? What would it be for block 0 (genesis block)?
- What is the `merkleroot`? How is it calculated?
- What are the `nonce` and `bits` fields? How do they relate to mining?

**4.4** Get the genesis block (block 0):
```bash
bitcoin-cli -regtest getblockhash 0
bitcoin-cli -regtest getblock <genesis_hash>
```

**Question**: What is special about the genesis block?

---

## Exercise 5: The UTXO Model

**5.1** List your unspent transaction outputs:
```bash
bitcoin-cli -regtest listunspent
```

**5.2** Answer these questions:
- How many UTXOs do you have?
- What is the total value across all UTXOs?
- Why do you have multiple UTXOs instead of one big balance?

**5.3** Send a transaction that combines multiple UTXOs:
```bash
# Send an amount larger than any single UTXO
bitcoin-cli -regtest sendtoaddress <address> 75
```

**Question**: How many inputs does this transaction have? Why?

**5.4** After mining, check listunspent again:
```bash
bitcoin-cli -regtest -generate 1
bitcoin-cli -regtest listunspent
```

**Question**: How did the UTXO set change? Which UTXOs were consumed? Which new ones were created?

---

## Assessment Questions

Write clear, detailed answers (3-5 paragraphs each). Bring these to the Friday TA session.

### Question 1

**Explain the UTXO model. How does it differ from an account-based model (like Ethereum)? What are the trade-offs?**

Consider:
- How does each model track balances?
- What are the privacy implications?
- What are the parallelisation advantages of UTXOs?
- What are the downsides (e.g., UTXO management, dust)?

### Question 2

**Walk through the lifecycle of a Bitcoin transaction from creation to confirmation. What happens at each stage?**

Cover:
1. Transaction creation (selecting UTXOs, constructing inputs/outputs)
2. Transaction signing
3. Broadcasting to the network
4. Mempool validation
5. Mining (inclusion in a block)
6. Confirmation (subsequent blocks)

---

## Submission

Post your answers in the Discord `#week-01` channel before the Friday session. Be prepared to explain your answers to your study group.

---

*Code Orange Dev School | [codeorange.dev](https://codeorange.dev) | CC0 1.0 Universal*
