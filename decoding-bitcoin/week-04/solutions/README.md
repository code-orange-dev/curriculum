# Week 4 solutions

[Week 4 overview](../README.md) · [Exercises](../exercises/README.md) · [Syllabus](../../README.md)

Try the questions yourself before reading these. They are model answers, not the only correct answers.

## Discussion questions

### 1. Where is the fee written in a transaction?

Nowhere. There is no fee field. The fee is implicit: it is the sum of the input amounts minus the sum of the output amounts. Whatever value the outputs don't claim goes to the miner.

The input amounts aren't in the transaction either. Each input only names an outpoint (`txid:vout`). To find the fee, a node looks up every outpoint in its UTXO set to get the amounts, adds them, and subtracts the outputs. If the result is negative, the transaction is invalid.

The miner collects the fees through the coinbase transaction: its outputs may claim at most the block subsidy plus the total fees of all transactions in the block. This is also why a wallet must know the amounts of the coins it spends, and why hardware wallets need the previous transactions (or, for segwit, the amount committed in the signature) to show you the real fee. Block explorers can show a fee only because they have looked up the inputs.

### 2. What are weight units and virtual bytes? Why does a witness byte count less?

Segwit (BIP141) replaced the 1,000,000-byte block size limit with a limit of 4,000,000 weight units (WU). Each byte of base (non-witness) data counts 4 WU, and each byte of witness data counts 1 WU:

```
weight = base_size × 4 + witness_size
       = base_size × 3 + total_size
vsize  = weight / 4, rounded up   (virtual bytes, vB)
```

Fee rates are quoted in sat/vB, so a legacy transaction's vsize equals its size, and a segwit transaction's vsize is smaller than its size.

Why the discount: base data (especially outputs) lives in the UTXO set, which every node must keep, possibly forever. Witness data is only needed to check a transaction once and is never needed to calculate the UTXO set afterwards. Before segwit, spending inputs (signature-heavy) was expensive compared with creating outputs, which encouraged people to create many outputs and not consolidate them. The discount makes spending cheaper, which helps keep the UTXO set small. It also allowed a soft fork: old nodes see blocks of at most 1 MB of base data, as before.

### 3. How does a wallet choose which UTXOs to spend? What can go wrong?

This is coin selection. The wallet must find a set of UTXOs that covers the payment plus the fee, where the fee itself grows with every input it adds. Bitcoin Core runs several algorithms and keeps the result with the lowest "waste" score:

- **Branch and Bound:** looks for a set that matches the target closely enough that no change output is needed. No change saves fees and helps privacy.
- **CoinGrinder:** at high fee rates, looks for the lightest set of inputs (lowest weight).
- **Knapsack** and **Single Random Draw:** fallbacks that create change.

What can go wrong:

- **Too many small inputs** at a high fee rate: you pay a lot in fees. Small coins may even cost more to spend than they are worth.
- **Privacy leaks:** spending coins from different sources in one transaction tells observers they belong to the same owner.
- **Tiny change outputs** that are uneconomical (or dust) and stay stuck in the wallet.
- **Spending unconfirmed coins** from others, which can disappear or make your transaction depend on someone else's.
- **Consolidating at the wrong time:** combining many coins is cheap when fees are low and very expensive when they are high.

### 4. What is dust, and why do nodes refuse to relay dust outputs?

Dust is an output whose value is less than the cost of spending it. Bitcoin Core calculates this with the `-dustrelayfee` rate (3 sat/vB by default): the size of the output plus the size of a typical input that spends it, times 3 sat/vB. This gives the well-known limits:

| Output type | Dust limit |
|---|---|
| P2PKH (legacy) | 546 sats |
| P2WPKH | 294 sats |
| P2WSH, P2TR | 330 sats |

Nodes won't relay or mine (by default) a transaction that creates a dust output. This is a policy rule, not a consensus rule: a miner can still put dust in a block. The reason is the UTXO set. Every output must be stored by every full node until it is spent, and a rational owner will never spend an output that costs more to spend than it is worth. Dust outputs would sit in everyone's UTXO set forever, so the network refuses to help create them. Dust is also used to spam the chain or to track people ("dusting attacks"). (Recent versions allow one special case, "ephemeral dust", where the dust output must be spent in the same package.)

### 5. Explain RBF and CPFP.

Both help a stuck, low-fee transaction confirm.

**RBF (replace-by-fee, BIP125):** the sender makes a new version of the transaction that spends at least one of the same inputs and pays a higher fee, usually by lowering the change output. Nodes replace the old version in their mempools if the new one pays more in total fees, plus enough extra to pay for its own relay (the incremental relay fee times its size), and a higher fee rate. Since Bitcoin Core v28 nodes accept replacements by default even if the original did not signal BIP125 ("full RBF"). Use RBF when you are the sender and still control the inputs. It is cheaper than CPFP because only one transaction is mined.

**CPFP (child pays for parent):** someone who can spend an output of the stuck transaction (the receiver, or the sender through the change) creates a child transaction with a high fee. A child can only be mined with or after its parent, so miners look at the combined fee rate of the package (total fees / total vsize) and include both. Use CPFP when you are the receiver, or when the original can't be replaced. Because the parent may be below some nodes' minimum fee, package relay (for example one-parent-one-child packages, available since v28) helps CPFP reach miners.

### 6. What drives the fee market?

Block space is limited: about 4,000,000 WU every 10 minutes on average. Fees are set by an auction. Miners fill blocks with the transactions that pay the highest fee rate, and users bid against each other for the next blocks.

- **Demand changes:** busy periods in markets (big price moves make people move coins to and from exchanges), the time of day and day of week in big economies, exchange batching and consolidation, and new uses of block space. For example, inscriptions in 2023 and the launch of Runes at the April 2024 halving pushed fees very high for a while.
- **Supply is fixed but lumpy:** blocks arrive randomly. A long gap between blocks lets the mempool build up and fees rise, and then a few quick blocks clear it.
- **Patience matters:** people who can wait set low fees and get in when the mempool empties. Fee estimators watch how fast transactions at each fee rate confirm.
- **Floors:** when demand is low, fees fall to the minimum relay fee that nodes accept (1 sat/vB for many years, and lower in newer Bitcoin Core versions).

In the long run, the block subsidy keeps halving, so fees must become a bigger part of what pays miners to secure the chain.

## Core exercises

### 1. Fee of a real transaction

Your numbers depend on the transaction. A correct answer shows: fee = inputs - outputs (in sats), fee rate = fee / vsize, and a result equal to what mempool.space shows (it may round to one decimal place). A common mistake is dividing by the size in bytes instead of the vsize, which gives a lower fee rate for segwit transactions.

### 2. vsize of a 1-input, 2-output P2WPKH transaction

```
base    = 4 + 1 + 41 + 1 + 31 + 31 + 4 = 113 bytes
witness = 2 + 107 = 109 bytes
total   = 222 bytes
weight  = 113 × 4 + 109 = 561 WU
vsize   = 561 / 4 = 140.25, rounded up = 141 vB
```

A real transaction of this shape shows 141 vB (sometimes 140.5 or 141 if the signature is 72 bytes: total 223, weight 562). A handy rule for P2WPKH: about 10.5 vB of overhead, about 68 vB per input and 31 vB per output.

### 3. Fee market at different times

There is no fixed answer. A good answer compares the numbers and links the change to the size of the mempool (more waiting transactions means higher fees for the next block), the time since the last block, and the time of day or week. If both readings were similar, say so and explain why that can happen (low demand, so fees sit near the minimum).

## Hands-on lab answers

Your exact numbers may differ by a byte or two because signatures are sometimes 72 bytes instead of 71.

**Step 1.** For a 1-input, 2-output P2WPKH payment, `vsize` is 141, and the fee is 141 × 5 = 705 sats (0.00000705 BTC). 705 / 141 = 5 sat/vB. The fee depends on the size, and the size depends on which inputs are chosen and how big the signatures will be. So the wallet estimates the size of the signed transaction (using dummy signatures) before it signs, and sets the fee from that.

**Step 2.**

| | size | vsize | weight | fee rate (10,000 sats) |
|---|---|---|---|---|
| Legacy P2PKH | 225 | 225 | 900 | 44.4 sat/vB |
| Segwit P2WPKH | 222 | 141 | 561 | 70.9 sat/vB |

The sizes in bytes are almost the same, but the segwit transaction uses 38% less weight. A miner prefers the segwit transaction: it pays more per unit of block space, and block space (weight) is what the miner is selling. Put the other way round: to reach the same fee rate, the segwit transaction needs a much smaller fee.

**Step 3.** The witness has 2 items: a 71-byte signature and a 33-byte public key. Witness bytes = 2 (marker and flag) + 1 (item count) + 1 + 71 + 1 + 33 = 109. Base size = 222 - 109 = 113. Weight = 113 × 3 + 222 = 561, vsize = ceil(561 / 4) = 141. These match `decoderawtransaction`. The legacy transaction has no witness, so its base size is its whole size: weight = 225 × 3 + 225 = 900 = 4 × 225, vsize = 225.

**Step 4.** For 2 P2WPKH inputs and 3 P2WPKH outputs:

```
base    = 4 + 1 + 2×41 + 1 + 3×31 + 4 = 185
witness = 2 + 2×107 = 216
total   = 401, weight = 185×3 + 401 = 956, vsize = 239
```

Estimate with the rule of thumb: 10.5 + 2 × 68 + 3 × 31 = 239.5, so about 240 vB, and a fee of about 4,800 sats (0.000048 BTC) at 20 sat/vB. `testmempoolaccept` should report a `vsize` of 239 (or 240 if a signature is 72 bytes) and `fees.base` equal to the fee you chose. The real rate is your fee / vsize, for example 4800 / 239 = 20.1 sat/vB. It is not exactly 20 because you estimated the size before signing (signature sizes vary), and vsize is rounded up to whole vbytes.

**Step 5.** The wallet usually picks 1 input (any coin bigger than 3 BTC plus fee) and adds a change output at a random position (`changepos` 0 or 1; -1 means no change was needed). The fee divided by the vsize of the signed transaction is 20 sat/vB or a tiny bit more, because the wallet rounds the fee up.

**Step 6.** `bumpfee` creates a replacement that spends the same input with a higher fee, and returns the new `txid`, `origfee` and `fee`. The old transaction is removed from the mempool (the wallet marks it as replaced) and only the new txid is in `getrawmempool`. The payment to Bob is unchanged and the change output is smaller by the extra fee. The change is the sender's own money, so taking the fee from it keeps the payment the same. If there were no change, the wallet would need to add another input.

### Python lab

A reference solution is in [`fees.py`](fees.py) in this folder (grade it with `python3 week-04/check.py --solution`). When `python3 week-04/check.py` passes, your functions should give the same weight and vsize as `decoderawtransaction` for `$SW_SIGNED` (561 and 141) and `$MULTI_SIGNED` (about 956 and 239).

### Stretch answers

**A.** The child (1 input, 1 output, about 110 vB) pays 1 - 0.9995 = 0.0005 BTC = 50,000 sats, about 455 sat/vB on its own. The parent paid about 141 sats for 141 vB. Together: 50,141 sats / about 251 vB = about 200 sat/vB. A miner can only take the child's fee if the parent is in the same block or an earlier one, so it looks at the combined (ancestor) fee rate. In `getmempoolentry`, `fees.ancestor` divided by `ancestorsize` gives this rate. Bob can't use RBF because he can't sign Alice's inputs: only the sender can replace the parent.

**B.** The wallet refuses with "Transaction amount too small". 200 sats is below the P2WPKH dust limit of 294 sats: (31-byte output + 67 vB to spend it) × 3 sat/vB = 294. A legacy P2PKH output has a higher limit, 546 sats: (34 + 148) × 3, because its output and its input are bigger.

**C.** On a fresh regtest chain, `estimatesmartfee` returns an error such as "Insufficient data or no feerate found". Bitcoin Core estimates fees by watching transactions enter its mempool and then counting how many blocks they took to confirm, at each fee rate. A new regtest node has seen no such history. That's why we set `-fallbackfee`: the wallet uses it when there is no estimate.

## Bonus questions

From the earlier version of this course.

### Explain the witness discount. Why does witness data get a 75% discount, and what behaviour does this encourage?

Under BIP141, base bytes count 4 weight units and witness bytes count 1, so a witness byte costs a quarter as much block space: a 75% discount. Fees are paid per vbyte (weight / 4), so witness data is 4 times cheaper per byte.

The reasons:

- **Different costs for nodes.** Outputs end up in the UTXO set, which every node keeps in fast storage until they are spent. Witness data is checked once and then is only needed for history. It is never needed to know the current state, and pruned nodes delete it with old blocks.
- **Fixing an incentive.** Before segwit, creating outputs was cheap and spending them (big scriptSigs with signatures) was expensive. That pushed users to create UTXOs and not consolidate them, growing the UTXO set. The discount makes inputs cheaper relative to outputs.
- **Soft fork compatibility.** Old nodes don't see the witness. Counting base bytes at 4 WU within a 4,000,000 WU limit means base data can never exceed the old 1 MB limit, so old nodes still accept the blocks.

Behaviour it encourages: using segwit (and later taproot) outputs, consolidating many small UTXOs into fewer ones, and keeping data that doesn't need to be in the UTXO set out of outputs. It also made more complex scripts (multisig via P2WSH) cheaper, because the script lives in the witness. A side effect is that the theoretical maximum block size grew to almost 4 MB if blocks are full of witness data, which some people later used for inscriptions.
