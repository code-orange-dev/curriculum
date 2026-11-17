# Week 2 solutions

[Week 2 overview](../README.md) · [Exercises](../exercises/README.md) · [Syllabus](../../README.md)

Try the questions yourself before reading these. They are model answers, not the only correct answers.

## Discussion questions

### 1. Walk through the lifecycle of a payment.

1. **Build.** The sender's wallet picks UTXOs it controls that cover the amount plus a fee (coin selection), adds the receiver's output and usually a change output, and sets version, sequence and locktime.
2. **Sign.** The wallet signs each input with the right private key and puts the signature in the scriptSig or the witness.
3. **Relay.** The wallet hands the transaction to a node. The node announces it to its peers, who request it, check it and announce it to their peers. In a few seconds most of the network has it.
4. **Check.** Every node checks it on its own before keeping it in its mempool: the inputs exist and are unspent, the scripts and signatures are valid, outputs are not worth more than inputs, and the node's policy rules (fee rate, standard scripts, size) are met.
5. **Mine.** Miners pick transactions for their block template, usually by fee rate. When a miner finds a valid proof of work, the block spreads and every node checks the whole block again.
6. **Confirm.** Being in a block gives 1 confirmation. Each block on top adds one more. The payment is never 100% final, but each confirmation makes reversing it much more expensive.

### 2. What is the mempool? Why is there no single shared mempool?

The mempool ("memory pool") is the set of valid, unconfirmed transactions that one node keeps in memory. The node uses it to relay transactions, to check new blocks faster (signatures are already checked), to estimate fees and, if it mines, to build block templates.

There is no single mempool because there is no central server. Each node has its own:

- **Propagation takes time.** Transactions reach nodes in different orders and at different times. Some nodes never hear of some transactions.
- **Policies differ.** Nodes can set different limits (`maxmempool`, minimum fee rate, which scripts they relay, replacement rules). A low-fee transaction may be in one mempool and not in another.
- **Conflicts.** If two transactions spend the same coin, a node normally keeps the one it saw first, unless the second is a valid replacement (RBF). Different nodes may see different ones first.
- **Restarts and evictions.** A node that restarts or whose mempool is full drops transactions.

Only the blockchain is shared and agreed on. The mempool is each node's local view of what might come next.

### 3. What is a chain reorganisation, and why wait for more than one confirmation?

A reorganisation (reorg) happens when a node switches from the chain it was following to a different valid chain with more accumulated work. Blocks at the tip of the old chain are disconnected and their transactions go back to the mempool. Those that conflict with the new chain are dropped.

Small reorgs happen naturally when two miners find a block at almost the same time: for a moment the network is split, and the next block decides which side wins. A reorg can also be caused on purpose by an attacker with a lot of hashrate who mines a secret chain where the payment to the merchant is replaced by a payment back to themself (a double spend).

A transaction with 1 confirmation can disappear in a reorg of 1 block. Each extra block makes a successful reorg much less likely, because the attacker must catch up from further behind. The risk falls roughly exponentially with each confirmation when the attacker has less than half the hashrate. So merchants choose confirmations based on the amount: zero or one for a coffee, often six for large amounts.

### 4. Why does change go back as a new output?

A UTXO can only be spent completely, in one go. A transaction input says "I spend output N of transaction X", and after that the output is gone from the UTXO set. There is no rule that lets you spend part of an output and leave the rest behind.

So if you have a 0.5 BTC coin and want to pay 0.2 BTC, your transaction spends the whole 0.5 BTC coin and creates two new outputs: 0.2 BTC to the receiver and about 0.3 BTC (minus the fee) to an address of your own. That second output is the change.

This keeps validation simple: each output is either unspent or spent, nothing in between, and nodes never have to track partial balances. Wallets usually send change to a fresh address so that observers have a harder time telling which output is the payment. If you forget the change output, the leftover becomes part of the fee and goes to the miner.

### 5. Name the main parts of a transaction in order.

1. **Version** (4 bytes): which rules the transaction follows. Version 2 allows relative timelocks (BIP68).
2. **Marker and flag** (2 bytes, segwit only): `00 01`, show that witness data is included.
3. **Input count:** how many inputs follow.
4. **Inputs:** each points to a previous output (txid and vout), has a scriptSig (unlocking data, empty for native segwit) and a sequence number.
5. **Output count:** how many outputs follow.
6. **Outputs:** each has an amount in satoshis and a scriptPubKey (the locking script that says who can spend it).
7. **Witness** (segwit only): signatures and public keys for each input.
8. **Locktime** (4 bytes): earliest block height or time at which the transaction may be mined.

There is no "from" field, no fee field and no sender address. Week 3 goes through each of these down to the bytes.

### 6. What does an input point to, and why is that enough?

An input points to an **outpoint**: the txid of an earlier transaction plus the index (`vout`) of one output in it. Nothing else about the old coin, not even its amount, is copied into the input.

That is enough because every node already has the full UTXO set. When it sees the input, it looks up the outpoint and finds the amount and the locking script (scriptPubKey). Then it runs the unlocking data from the input (scriptSig and/or witness) against that locking script. If the script succeeds, for example because the signature matches the public key whose hash is in the locking script, the spender has proven they are allowed to spend it.

The history of the money is proven by the chain of outpoints: each coin was created by an earlier valid transaction, back to a coinbase that created new coins. Nodes checked each step when it happened, so they only need the current UTXO set, not the whole history.

## Core exercises

### 1. Watching a transaction confirm

A transaction with a high fee rate usually confirms in the next block, so the wait is the time until the next block is found. That time is random: blocks come on average every 10 minutes, but a gap of 1 minute or 30 minutes is normal. If you started watching just after a block, you may wait longer than someone who started 9 minutes in. A low-fee transaction may wait several blocks or hours, because miners fill blocks with higher-paying transactions first.

### 2. Reorg Calculator

The whitepaper (section 11) gives the chance that an attacker with share q of the hashrate ever catches up from z blocks behind. With its formula:

| Attacker hashrate | 1 confirmation | 3 confirmations | 6 confirmations |
|---|---|---|---|
| 10% | 20.5% | 1.3% | 0.024% |
| 30% | 62.8% | 32.5% | 13.2% |
| 45% | 92.0% | 84.4% | 76.6% |

Some calculators use a simpler formula, (q/p)^z where p = 1 - q, which gives lower numbers (for 10%: 11.1%, 0.14% and 0.0002%). Both show the same pattern. With a small attacker, risk drops very fast with each block. With an attacker close to 50%, extra confirmations help only a little, and at 50% or more the attacker eventually wins whatever you do.

A reasonable answer for confirmations: coffee, 0 (the risk and the amount are both small), laptop, 1 to 3, car, 6 or more. What matters is that the cost of attacking must be much higher than what the attacker could steal.

### 3. Transaction Decoder

Answers depend on the transaction you chose. A correct answer lists:

- version (1 or 2 for almost all transactions),
- input count and, for each input, the outpoint `txid:vout`,
- output count and each amount,
- the locktime (0 or a block height; Bitcoin Core wallets usually set it to the current height).

When you look up the previous transaction, output number `vout` (counting from 0) is the coin being spent. Its amount is not in the spending transaction at all. That is why the fee can only be found by looking up the inputs.

## Hands-on lab answers

Your txids, addresses and exact amounts will be different. Here is what a correct result looks like.

**Step 1.** It is block 1's reward. Coinbase outputs need 100 blocks before they can be spent (and the wallet counts them as spendable at 101 confirmations). Blocks 2 to 101 are not old enough yet.

**Step 2.** `size` is the number of transactions (0) and `bytes` is the total virtual size of them (0). `mempoolminfee` is the lowest fee rate, in BTC/kvB, that this node accepts into its mempool right now. It starts at the `minrelaytxfee` setting (1 sat/vB in v29, lowered to 0.1 sat/vB in v30) and goes up if the mempool is full. A transaction paying less is rejected by this node and not relayed.

**Step 3.** `size` becomes 1. `vsize` is about 141 vbytes (1 P2WPKH input, 2 P2WPKH outputs) and `weight` about 561. `time` is when the node first saw it, `height` is the block height at that time, and `fees.base` is the fee in BTC, about 0.0000141. The fee rate is 1410 sat / 141 vB = 10 sat/vB, which is exactly the fallback fee of 0.0001 BTC/kvB.

**Step 4.** The payment is unconfirmed and came from someone else, so Bob's wallet calls it untrusted: Alice could still double-spend it, for example by replacing it with RBF. Bob's wallet won't even spend it yet. For anything valuable, Bob should wait for confirmations.

**Step 5.** `$PREV` is the coinbase transaction of block 1. Its first input has a `coinbase` field and no real txid. Alice's payment spends output 0 of it, worth 50 BTC. The payment has 2 outputs: 1 BTC to Bob and about 48.99998590 BTC change back to Alice. The order of the two outputs is random (Bitcoin Core randomises the change position), so check the amounts.

**Step 6.** The mempool is empty again because the transaction was included in the block. `gettransaction` now shows `confirmations: 1` and new fields `blockhash`, `blockheight`, `blockindex` and `blocktime`. Bob's balance is 1 BTC under `trusted`.

**Step 7.** The unsigned transaction has an empty `scriptSig` and no `txinwitness`. The fee is not written anywhere: it is 50 - (2 + 47.9999) = 0.0001 BTC, the difference between inputs and outputs. `testmempoolaccept` gives `"allowed": true`, `vsize` 141 and `fees.base` 0.0001. The fee rate is 10,000 sat / 141 vB, about 70.9 sat/vB.

**Step 8.** It is rejected with `max-fee-exceeded`. The fee would be 48 BTC (50 in, 2 out), and with no change every satoshi not assigned to an output goes to the miner who mines the block. The protection is a safety check in your own node's RPC: `testmempoolaccept` and `sendrawtransaction` refuse fee rates above `maxfeerate`, which defaults to 0.10 BTC/kvB (10,000 sat/vB). It is not a consensus rule. Another node or a miner would accept the transaction happily. A smaller mistake is not caught: for this 141 vB transaction, any fee below about 0.0141 BTC passes the check.

**Step 9.** `sendrawtransaction` is a node command, not a wallet command. The transaction is already signed, so no private key is needed. The node only checks it and relays it. Anyone can broadcast a signed transaction.

**Step 10.** The child's `depends` contains the parent's txid, and the parent's `spentby` contains the child's txid. The child has `ancestorcount: 2` and the parent has `descendantcount: 2` (each count includes the transaction itself). The node links them because the child's input points to `$MANUAL_TXID:1`, which is not in the UTXO set yet but is an output of a transaction in the mempool. If the parent is never mined (for example it is replaced or evicted), the child's input points to nothing, so the child becomes invalid and is removed too.

**Step 11.** The block has 3 transactions: the coinbase first, then the parent, then the child. Consensus requires that a transaction only spends outputs that already exist, either in earlier blocks or earlier in the same block. So a child can never come before its parent. Bob's balance is now 1 + 2 + 47.9998 = 50.9998 BTC, all trusted.

### Stretch answers

**A.** After `invalidateblock`, the parent and child go back to the mempool (`size` is 2) and `gettransaction` shows `confirmations: 0`. The coinbase transaction of that block is gone: a coinbase can only exist inside its block, so it cannot go back to the mempool. After `reconsiderblock` the block becomes active again and the mempool is empty. Lesson for merchants: a transaction with 1 confirmation can be pushed out of the chain. If the sender also broadcast a conflicting transaction, the payment might never come back.

**B.** When the nodes are connected, a new transaction shows up in both mempools within a few seconds (nodes wait a short random time before announcing transactions, for privacy). When they are disconnected, the new transaction exists only on node 1. They also differ if they have different policies or limits. There is no global mempool because each node only knows what its peers told it, and nothing forces them to agree until a block is mined.

**C.** The default `maxmempool` is 300 MB. When the mempool is full, the node evicts the transactions (with their descendants) that pay the lowest fee rate. It then raises its `mempoolminfee` above the fee rate of what it evicted, so it stops accepting cheaper transactions. This minimum slowly decays back down when the mempool has space again.
