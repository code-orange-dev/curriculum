# Week 1 solutions

[Week 1 overview](../README.md) · [Exercises](../exercises/README.md) · [Syllabus](../../README.md)

Try the questions yourself before reading these. They are model answers, not the only correct answers. If your answer is different but you can defend it, bring it to the session.

## Discussion questions

### 1. What problem did Bitcoin solve that earlier digital cash attempts could not?

Digital money has one big problem: data can be copied, so you need a way to stop people spending the same coin twice (the double-spend problem). DigiCash (David Chaum, 1990s) solved it with a central company that checked every payment. It had strong privacy through blind signatures, but when the company went bankrupt the system died, and the company could always be shut down or pressured. b-money (Wei Dai) and Bit Gold (Nick Szabo) described decentralised ideas, including proof of work, but they never had a complete, working answer to how strangers agree on one history of payments without a trusted party.

Bitcoin combined proof of work with a simple rule: follow the valid chain with the most accumulated work. Anyone can check the rules, anyone can produce blocks, and changing history costs real energy. This gives a shared order of transactions with no central server, so double spends are prevented without a company in the middle.

### 2. Pick one moment from Bitcoin history and explain why it mattered.

Many answers work. Some good ones:

- **The genesis block (3 January 2009).** Its coinbase contains the headline "The Times 03/Jan/2009 Chancellor on brink of second bailout for banks". It shows the block could not have been made before that date, and it shows the motivation: money that does not depend on bank bailouts.
- **The value overflow bug (August 2010).** Someone created about 184 billion BTC in one transaction because of an integer overflow. It was fixed with a soft fork and a new chain within hours. It shows why Bitcoin Core developers are so careful with consensus code today.
- **The block size wars and SegWit (2015 to 2017).** A long fight over how to scale ended with SegWit activating as a soft fork in August 2017. It showed that users running nodes, not miners or companies alone, decide the rules. SegWit also fixed malleability, which we study in week 3.
- **Taproot (November 2021).** The first big upgrade after SegWit, bringing Schnorr signatures and better privacy for complex spending conditions (weeks 9 and 10).

A strong answer names the moment, says what happened, and links it to something in how Bitcoin works or is developed today.

### 3. What is a hash function? Name three properties Bitcoin relies on.

A hash function takes input of any length and returns a fixed-length output (SHA-256 always gives 32 bytes). The same input always gives the same output, and it is fast to compute. Bitcoin relies on:

- **Preimage resistance (one-way):** given a hash, you cannot find an input that produces it. Addresses use hashes of public keys (HASH160 = RIPEMD-160 of SHA-256), and proof of work depends on not being able to work backwards from a target.
- **Collision resistance:** you cannot find two different inputs with the same hash. Transaction IDs and block hashes are double SHA-256 of the data, so a txid safely names exactly one transaction.
- **Avalanche effect (small change, totally different output):** change one bit and about half the output bits change. In mining, every new nonce gives an unpredictable hash, so the only strategy is to keep trying. It also means any change to a block breaks its hash and the link from the next block.

Also used: Merkle trees (hashes of hashes) commit to all transactions in a block header.

### 4. Explain the UTXO model. Why is there no balance stored anywhere?

Bitcoin tracks coins, not accounts. Each transaction destroys some existing coins (its inputs) and creates new ones (its outputs). An output that has not been spent yet is an unspent transaction output, or UTXO. Each UTXO has an amount and a locking script that says what is needed to spend it, usually a signature from a certain key.

Every full node keeps the set of all UTXOs (the UTXO set). To check a new transaction, a node only needs to confirm that each input points to a UTXO in this set, that the unlocking data satisfies the locking script, and that outputs do not add up to more than inputs.

Nothing in the protocol says "Alice has 3 BTC". Your "balance" is something your wallet calculates: it scans for UTXOs that your keys can spend and adds them up. Coins are like banknotes in a wallet: you know your total by counting the notes.

### 5. One advantage and one disadvantage of UTXOs compared with accounts.

**Advantages (any one is fine):**

- Easy, parallel validation: each input spends one specific coin, which can be spent only once. Nodes can check inputs independently, and there is no global nonce or ordering of account updates to worry about.
- Better privacy if used well: a wallet can use a new address for every payment and for change, so coins are not all linked to one account.
- Simple double-spend rule: two transactions spending the same UTXO conflict, and only one can confirm.
- No replay problem: a transaction names the exact coins it spends, so it cannot be replayed later.

**Disadvantages:**

- Wallets are more complex: they must choose which coins to spend (coin selection) and create change outputs.
- Spending many small UTXOs costs more fees, because each input adds bytes. Very small UTXOs can cost more to spend than they are worth (dust).
- Smart contracts that need shared, changing state are harder to build than with accounts.
- Combining coins in one transaction can reveal that they belong to the same owner.

### 6. Why "don't trust, verify"? What can you verify, and what do you take on trust?

Bitcoin was designed so that nobody has to trust a bank or company to know which payments are valid. If you run a full node, your own computer checks every block and transaction against the rules: signatures, no double spends, the block subsidy and the 21 million limit, proof of work, and so on. You don't have to believe anyone's claim about your balance or about whether a payment confirmed.

Things you can verify yourself: the full chain history and current UTXO set, that your received payments are confirmed, the signatures on the Bitcoin Core release you downloaded, and the source code if you build it.

Things most people still take on trust: that the cryptography (SHA-256, secp256k1) is secure, that the code does what reviewers say (few people read all of it), the hardware and operating system, the wallet software that holds keys, and, with light wallets or block explorers, the server that answers their questions. The goal is to reduce trust and make it a choice, not to remove it completely.

## Core exercises

### 1. Introduce yourself on Discord

There is no single answer. A good introduction says what you work with, why you joined and what you would like to build. Replying to others is the important part: this cohort is a peer-learning group.

### 2. Hash Functions tool

- After changing one letter, the output looks completely different. On average about 15 out of 16 hex characters in the same position change, because each hex character matches by chance only 1 time in 16 (so about 4 of the 64 stay the same by luck).
- The output of SHA-256 is always 32 bytes = 64 hex characters, for the empty input, a short input and a very long input. The SHA-256 of the empty string is `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- There is no way back from the output to the input except guessing inputs and hashing them. This is preimage resistance. Short or common inputs (like a name) can be found by guessing, which is why you should never use a hash of a simple word as a secret.

### 3. A real transaction on mempool.space

Sum of inputs minus sum of outputs equals the fee. mempool.space shows the same number. The fee rate is the fee divided by the virtual size in vbytes (week 4 explains vbytes).

For the change, a reasonable guess uses clues:

- The payment is often a round number (in BTC, sats, or a round amount in local currency at that day's price).
- Change often goes to the same address type as the inputs (for example inputs from `bc1q...`, change to `bc1q...`, payment to `3...`).
- If one output is larger than every input, it cannot be change in a normal wallet, because a wallet would not have needed that input otherwise.

These are guesses (heuristics), not facts. Chain analysis companies use the same clues, which is why privacy-aware wallets try to make change look like a payment.

## Hands-on lab answers

### Short lab in this folder

**Step 1.** `bitcoind -version` prints something like `Bitcoin Core daemon version v29.0` (and `bitcoin-cli -version` prints `Bitcoin Core RPC client version v29.0`). Anything v29 or newer is fine.

**Step 2.** `chain` is `regtest`, `blocks` is `0` on a new node, and `difficulty` is about `4.66e-10`. Regtest has a minimum difficulty that never adjusts, so almost any hash is below the target and a laptop finds a valid block at once.

**Step 3.** Each regtest block pays 50 BTC to the miner (the regtest subsidy halves every 150 blocks, so the first 150 blocks pay 50). A coinbase output can only be spent 100 blocks later (coinbase maturity), and the wallet counts it as spendable at 101 confirmations. After 101 blocks, only the reward from block 1 has matured. `getbalances` shows `trusted: 50` and `immature: 5000` (100 more rewards of 50 BTC).

**Step 4.** The two SHA-256 outputs share no visible pattern: this is the avalanche effect. Without `-n`, `echo` adds a newline character, so you hash `satoshi\n`, which gives a totally different result. Tools that disagree about one invisible byte is a very common bug when people check hashes. For reference: SHA-256 of `satoshi` is `da2876b3eb31edb4436fa4650673fc6f01f90de2f1793c4ec332b2387b09726f`, of `satoshj` is `ee4fd5ccc0696b1816c4d946503989c4b7dd2c6e6cea5ac9dad0486c89f60e46` (not one hex character matches in the same position), and the double SHA-256 of `satoshi` is `d3e291220ccc90141e6ada2fc9740a0a1dcc6aadf1c47c65c9243d49b2d7a326`. The avalanche stretch task prints `134 of 256 bits differ` for these two inputs.

**Step 5.** `previousblockhash` points to the previous block, and `merkleroot` commits to all the transactions in this block. Blocks are linked by the double SHA-256 hash of the 80-byte header: each header contains the hash of the one before it.

### bitcoin_core_cli.md answers

**1.2** Height (`blocks`) is 0 on a fresh chain, `chain` is `regtest`, `difficulty` is `4.656542373906925e-10`.

**1.4** The consensus rule says a coinbase output can only be spent in a block at least 100 blocks after the block that created it. Bitcoin Core's wallet is one block more careful: it shows a coinbase output as spendable once it has 101 confirmations. The rule exists because blocks can be reorganised away. If a block disappears in a reorg, its coinbase reward never existed. Without maturity, coins spent from that reward (and every later payment built on them) would become invalid. 100 blocks makes this practically impossible. Mining 101 blocks makes the reward from block 1 spendable.

**1.5** 50 BTC. You mined 101 rewards of 50 BTC each (5050 BTC), but 100 of them are still immature. Only block 1's reward is spendable.

**2.1** Both start with `bcrt1q`, so they are native SegWit v0 P2WPKH addresses (Bech32). This is the default type in Bitcoin Core. `bcrt` is the regtest prefix (mainnet uses `bc`, testnet and signet use `tb`).

**2.3** Fields:

- `txid`: the transaction's ID, the double SHA-256 of the transaction without witness data, shown in reversed byte order.
- `version`: transaction version, `2` for Bitcoin Core wallet transactions. Version 2 enables relative timelocks (BIP68) in `sequence`.
- `vin`: the inputs. Each one points to an earlier output with `txid` and `vout`, and carries the data that unlocks it (`scriptSig`, empty for SegWit, plus `txinwitness`) and a `sequence` number.
- `vout`: the outputs. Each has a `value` in BTC, an index `n`, and a `scriptPubKey` (the locking script) with the address.
- `locktime`: the earliest block height (or time) when the transaction can be mined. Bitcoin Core usually sets it to the current block height (anti fee sniping).

You will also see `hash` (the wtxid), `size`, `vsize` and `weight`. For this one-input, two-output P2WPKH transaction they are `size` 222, `vsize` 141 and `weight` 561 (the signature can be 1 byte shorter now and then, which changes these by 1). At the default fallback fee of 10 sat/vB the fee is 1,410 sats, so the change output is 39.99998590 BTC. `locktime` is 101, the current height.

Because "bob" is an address in your own wallet, `gettransaction` shows `amount` 0 and lists the 10 BTC twice in `details`, once as `send` and once as `receive`. Only the fee really left the wallet.

There are normally 2 outputs: 10 BTC to bob, and the change back to a new address in your wallet. The input was a 50 BTC coinbase output, and a UTXO must be spent completely, so whatever is not paid out (minus the fee) has to come back as change.

**2.5** `confirmations` changes from 0 to 1, and new fields appear: `blockhash`, `blockheight` (102), `blockindex` (1, because the coinbase is index 0) and `blocktime`. `bip125-replaceable` changes from `yes` to `no`, because a confirmed transaction can no longer be replaced. The transaction has also left the mempool.

**3.3** The first bytes of a typical wallet transaction read:

```
02000000   version 2 (little-endian)
00         segwit marker
01         segwit flag
01         input count: 1
<32 bytes> previous txid, in reversed byte order
<4 bytes>  vout index of the output being spent, little-endian
```

That is 4 + 1 + 1 + 1 + 13 bytes of the txid = 20 bytes. Week 3 continues from here.

**4.3**

- The block from step 2.4 has 2 transactions: the coinbase and your payment. (If you mined other blocks, an empty block has only 1.)
- The coinbase is always the first transaction. It has one input that does not spend a real UTXO (`getblock` shows it as a `coinbase` field instead of a `txid` and `vout`) and creates new coins: the block subsidy plus all fees in the block. In this block its first output is 50.00001410 BTC: 50 BTC subsidy plus the 1,410 sat fee of your payment. It also has a second output of 0 BTC with type `nulldata` (an OP_RETURN): the SegWit witness commitment, which commits to the wtxids of the block.
- `previousblockhash` is the hash of the block before. Block 0 has no previous block, so the field is missing in `getblock` output (inside the header, the 32 bytes are all zeros).
- `merkleroot` is the root of a Merkle tree of all txids in the block: hash pairs of txids with double SHA-256, then hash pairs of those results, until one hash is left. It lets the 80-byte header commit to every transaction.
- `bits` is the compact encoding of the target (`207fffff` on regtest, the easiest allowed). `nonce` is the number miners change to get a header hash below the target. On regtest a very small nonce is usually enough.

**4.4** The genesis block is hardcoded in the software, not mined by your node. It has no previous block, and its coinbase output cannot be spent: it is not in the UTXO set. On regtest its hash is `0f9188f13cb7b2c71f2a335e3a4fc328bf5beb436012afca590b1a11466e2206`, which differs from mainnet because the time, nonce and bits differ. The coinbase transaction is the same as mainnet, with the same "The Times 03/Jan/2009" message, so the merkle root is also the same: `4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b`.

**5.2** The count depends on what you did. If you followed the steps above exactly (102 blocks mined, one payment), you have 3 UTXOs worth 99.99998590 BTC in total: one mature 50 BTC coinbase output (from block 2; block 1's reward was spent in 2.2), the 10 BTC "bob" output and the 39.99998590 BTC change output. Your wallet shows a balance by adding up UTXOs; each payment you received and each change output is a separate coin, so you have several.

**5.3** At least 2 inputs, because no single UTXO is worth 75 BTC or more. The wallet had to combine coins (for example a 50 BTC coinbase output and the change output) to pay 75 BTC plus the fee. Coin selection has some randomness: in our test run the wallet used all 3 UTXOs (vsize 276, fee 2,760 sats at 10 sat/vB), leaving 24.99995830 BTC change.

**5.4** The UTXOs used as inputs are gone from `listunspent`. New ones appeared: the 75 BTC output (if you sent it to one of your own addresses, it is in your wallet), the new change output, and one more mature coinbase output, because mining another block made one more reward reach the 101 confirmations the wallet waits for. In our run there were 3 UTXOs again: the 75 BTC "alice" output, the 24.99995830 BTC change and the newly matured 50 BTC coinbase from block 3.

## Bonus questions

These come from the earlier version of this course and match the Bitcoin Core CLI lab.

### Explain the UTXO model. How does it differ from an account-based model? What are the trade-offs?

In the UTXO model, the state is a set of separate coins. Each coin has a value and a locking script. A transaction spends whole coins and creates new ones. In an account model (Ethereum is the usual example), the state is a table of accounts with balances, and a transaction says "subtract X from account A and add X to account B". Each account has a nonce so that a signed transaction cannot be replayed.

Trade-offs:

- **Validation:** UTXO transactions name the exact coins they spend, so nodes can check inputs independently and in parallel. Account transactions depend on the current balance and nonce, so order matters more.
- **Privacy:** UTXO wallets can use a fresh address for every coin. Accounts encourage reusing one address, which links all activity. UTXOs still leak information when coins are combined as inputs.
- **Simplicity of wallets and contracts:** accounts make balances and shared state (like a token contract) easy. UTXO wallets need coin selection and change, and have to manage many small coins.
- **Costs:** in UTXO systems, each input costs fees, and dust can become uneconomical to spend. Full nodes must also store the UTXO set, and creating many small outputs makes it bigger.

### Walk through the lifecycle of a Bitcoin transaction from creation to confirmation.

1. **Creation:** the wallet picks UTXOs that it can spend and that cover the amount plus the fee (coin selection). It builds outputs: the payment and usually a change output back to itself. It sets version, sequence and locktime.
2. **Signing:** for each input, the wallet makes a signature over a hash of the transaction data (the sighash) with the private key that controls that UTXO, and puts the signature in the scriptSig or witness.
3. **Broadcasting:** the wallet gives the transaction to a node, which announces it to its peers. Peers request it and pass it on, so it spreads across the network in seconds.
4. **Mempool validation:** each node checks it before keeping it: inputs exist and are unspent, scripts and signatures are valid, outputs are not worth more than inputs, and it follows the node's policy rules (minimum fee rate, standard scripts, no dust, size limits). Valid transactions wait in that node's mempool.
5. **Mining:** miners build a block template, usually choosing transactions with the highest fee rate, and search for proof of work. When a miner finds a valid block, it is broadcast and every node checks it again in full.
6. **Confirmation:** once in a block, the transaction has 1 confirmation. Each later block on top adds one more. More confirmations make a reorg that removes the transaction less and less likely, so receivers wait for more of them for larger amounts.
