# Decoding Bitcoin - Week 1 Exercises: Bitcoin Core CLI

> Code Orange Dev School | [codeorange.dev](https://codeorange.dev)

This lab gets a private Bitcoin network (regtest) running on your machine and walks you through your first `bitcoin-cli` commands. Week 1 has no homework, so treat this as setup for week 2. Model answers are in [`../solutions/README.md`](../solutions/README.md).

## Prerequisites

- Bitcoin Core v29 or newer (`bitcoind` and `bitcoin-cli`)
- A terminal on Linux, macOS or Windows (WSL2 works well on Windows)
- About 1 GB of free disk space (regtest data is tiny; building from source needs more)

You have two ways to get Bitcoin Core. Pick one.

### Option A (easy): install a release binary

1. Go to [bitcoincore.org/en/download](https://bitcoincore.org/en/download/) and download the latest release for your system (for Linux on a normal PC: `bitcoin-<version>-x86_64-linux-gnu.tar.gz`).
2. Download `SHA256SUMS` and `SHA256SUMS.asc` from the same page and check the file. The download page explains how to verify the signatures too. Do it: "don't trust, verify" starts here.

```bash
# In the folder where you downloaded the files
sha256sum --ignore-missing --check SHA256SUMS

# Unpack and install (replace <version> with the version you downloaded)
tar -xzf bitcoin-<version>-x86_64-linux-gnu.tar.gz
sudo install -m 0755 -o root -g root -t /usr/local/bin bitcoin-<version>/bin/*

# Check it works
bitcoind -version
bitcoin-cli -version
```

On macOS, download the `.tar.gz` for your chip (Apple silicon is `arm64-apple-darwin`) and copy the files from `bin/` into a folder on your `PATH`.

### Option B: build from source (CMake)

Since v29, Bitcoin Core builds with CMake. The old `./autogen.sh`, `./configure` and `make` steps no longer work. These steps are for Ubuntu/Debian; for other systems see [`doc/build-unix.md`](https://github.com/bitcoin/bitcoin/blob/master/doc/build-unix.md) and the other `doc/build-*.md` files in the Bitcoin Core repository.

```bash
# Install build dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install build-essential cmake pkgconf python3 \
  libevent-dev libboost-dev libsqlite3-dev libcapnp-dev capnproto

# Get the source and check out the newest release tag
git clone https://github.com/bitcoin/bitcoin.git
cd bitcoin
git tag -l 'v*' --sort=-v:refname | grep -v rc | head -5   # newest releases first
git checkout v32.1        # replace with the newest tag in the list

# Configure and build (this takes a while the first time)
cmake -B build
cmake --build build -j"$(nproc)"

# The binaries are in build/bin/
ls build/bin/
./build/bin/bitcoind -version
```

Notes:

- `libsqlite3-dev` is needed for the wallet. Without it CMake builds Bitcoin Core with no wallet, and this lab needs one.
- The GUI (`bitcoin-qt`) is not built by default. You don't need it for this cohort.
- `libcapnp-dev` and `capnproto` (Cap'n Proto) are needed from v30 on, where the multiprocess/IPC build is on by default. Without them `cmake -B build` stops with an error saying Cap'n Proto was not found. If you can't install them, configure with `cmake -B build -DENABLE_IPC=OFF` instead.
- `libevent-dev` is needed up to v31. From v32 on you can leave it out.
- To use the commands below without typing the full path, add the folder to your `PATH`: `export PATH="$PWD/build/bin:$PATH"` (run it from the `bitcoin` folder, or put the full path in your `~/.bashrc`).
- Optional: run the unit tests with `ctest --test-dir build -j"$(nproc)"`.

### Start your regtest node

```bash
bitcoind -regtest -daemon -txindex=1 -fallbackfee=0.0001
```

- `-regtest` runs a private test chain. You make the blocks, and the coins are worthless.
- `-txindex=1` lets `getrawtransaction` find any transaction, not only ones in the mempool.
- `-fallbackfee=0.0001` gives the wallet a fee rate to use (0.0001 BTC/kvB = 10 sat/vB). A fresh regtest chain has no fee history, so without this, `sendtoaddress` fails with "Fee estimation failed".

To stop the node later: `bitcoin-cli -regtest stop`. To start again from an empty chain, stop the node and delete the regtest folder (`~/.bitcoin/regtest` on Linux, `~/Library/Application Support/Bitcoin/regtest` on macOS).

---

## Exercise 1: Start a Regtest Network and Mine Blocks

Regtest (regression test) is a private blockchain that runs on your machine. You control everything, and there is no need to sync with the real network.

### Tasks

**1.1** Start bitcoind in regtest mode (skip this if it is already running):
```bash
bitcoind -regtest -daemon -txindex=1 -fallbackfee=0.0001
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

This creates a descriptor wallet (the default). If you restart the node later, load it again with `bitcoin-cli -regtest loadwallet "mywallet"`.

**1.4** Mine 101 blocks (you need 100 blocks of maturity before coinbase rewards are spendable):
```bash
bitcoin-cli -regtest -generate 101
```

**Question**: Why 101 and not just 1? What is the coinbase maturity rule and why does it exist?

**1.5** Check your balance:
```bash
bitcoin-cli -regtest getbalance
```

**Question**: How many BTC do you have? Each early regtest block reward is 50 BTC. Why is your balance 50 and not 5050?

---

## Exercise 2: Create and Inspect Transactions

**2.1** Generate two addresses:
```bash
bitcoin-cli -regtest getnewaddress "alice"
bitcoin-cli -regtest getnewaddress "bob"
```

"alice" and "bob" are just labels. Both addresses belong to the same wallet.

**Question**: What type of addresses are these? (Hint: look at the prefix: `bcrt1q` = P2WPKH, `bcrt1p` = P2TR)

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
- `txid`:
- `version`:
- `vin` (inputs):
- `vout` (outputs):
- `locktime`:

**Question**: How many outputs does the transaction have? Why are there more than 1? (Hint: change output)

**2.4** Mine a block to confirm the transaction:
```bash
bitcoin-cli -regtest -generate 1
```

**2.5** Check that the transaction is now confirmed:
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

Take the raw hex and try to find the following fields by hand. Use this reference:

| Field | Size | Description |
|-------|------|-------------|
| Version | 4 bytes (little-endian) | Transaction version (usually 01000000 or 02000000) |
| Marker | 1 byte | SegWit marker: 00 |
| Flag | 1 byte | SegWit flag: 01 |
| Input count | compact size | Number of inputs |
| Inputs | variable | Previous txid (32 bytes, reversed) + vout index (4 bytes) + scriptSig length + scriptSig + sequence (4 bytes) |
| Output count | compact size | Number of outputs |
| Outputs | variable | Value (8 bytes, little-endian, in satoshis) + scriptPubKey length + scriptPubKey |
| Witness | variable | Witness data for each input |
| Locktime | 4 bytes | Transaction locktime |

**YOUR TASK**: Label at least the first 20 bytes of your raw transaction hex. Write out what each byte means. (Week 3 goes through every field in detail.)

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

(The `2` gives full transaction details.)

**4.3** Answer these questions about the block:
- How many transactions are in the block?
- What is the coinbase transaction? How is it different from a regular transaction?
- What is the `previousblockhash`? What would it be for block 0 (the genesis block)?
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
# Send an amount larger than any single UTXO, to your "alice" address from 2.1
bitcoin-cli -regtest sendtoaddress <alice_address> 75
```

Then look at the inputs with `bitcoin-cli -regtest getrawtransaction <txid> true` (or `gettransaction <txid>`, which also shows the fee).

**Question**: How many inputs does this transaction have? Why?

**5.4** After mining, check listunspent again:
```bash
bitcoin-cli -regtest -generate 1
bitcoin-cli -regtest listunspent
```

**Question**: How did the UTXO set change? Which UTXOs were consumed? Which new ones were created?

---

## Discussion Questions

Write short, clear answers (a few paragraphs each) and bring them to the Monday session. Model answers are under "Bonus questions" in [`../solutions/README.md`](../solutions/README.md).

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

## Sharing your work

Post questions, errors and screenshots in the cohort Discord channel. If your setup fails, post the exact error message: someone has probably seen it before. Make sure your node works before the week 2 session, because week 2's lab builds on it.

---

*Code Orange Dev School | [codeorange.dev](https://codeorange.dev) | CC0 1.0 Universal*
