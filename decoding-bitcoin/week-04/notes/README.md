# Week 4 notes

[Week 4 overview](../README.md) · [Exercises](../exercises/README.md) · [Solutions](../solutions/README.md) · [Slides](../slides/slides.md)

## Key ideas

- **The fee is what is left over.** A transaction has no fee field. Fee = sum of inputs - sum of outputs. The input amounts come from the UTXO set, not from the transaction. The miner collects all fees in the coinbase.

- **Fees are paid for space, not for value.** Moving 1 BTC or 1000 BTC costs the same if the transactions have the same size. What you buy is a share of the block, measured in weight.

- **Weight and virtual bytes.** Since segwit, blocks are limited to 4,000,000 weight units. Base bytes count 4 WU and witness bytes count 1 WU. vsize = weight / 4, rounded up, and fee rates are quoted in sat/vB. For a legacy transaction, vsize equals size.

- **Why the witness discount.** Outputs go into the UTXO set that every node must keep. Witnesses are checked once and never needed again to know the current state. The discount makes spending (and consolidating) cheaper compared with creating outputs, and it let segwit be a soft fork.

- **Coin selection is a real problem.** The wallet must cover the amount and the fee, but each input it adds increases the fee. Good selection avoids change when possible, keeps fees low at busy times, and avoids linking unrelated coins.

- **Dust is uneconomical.** An output worth less than the cost to spend it may never be spent. Nodes refuse to relay transactions that create dust (546 sats for P2PKH, 294 for P2WPKH, 330 for P2TR by default), to protect the UTXO set.

- **Two ways to unstick a transaction.** RBF: the sender replaces the transaction with one that pays more. CPFP: someone who can spend one of its outputs adds a child with a high fee, and miners take the pair because of the combined fee rate.

- **The fee market is an auction.** Supply is roughly fixed (one block about every 10 minutes) and demand changes all the time. Users who can wait pay less.

## Common mix-ups

| Mix-up | Correction |
|---|---|
| Fee rate = fee / size in bytes. | Fee rate = fee / vsize. For segwit transactions, bytes and vbytes differ a lot. |
| Bigger payments pay higher fees. | Fees depend on size (weight), not on the amount moved. Many inputs cost more than a big amount. |
| Segwit transactions are smaller in bytes. | They are about the same size in bytes. They are smaller in weight and vsize, because witness bytes are discounted. |
| Dust is invalid. | Dust is a relay policy rule. A block containing dust outputs is still valid. |
| Only the sender can speed up a transaction. | The receiver can use CPFP by spending their output with a high fee. Only the sender can use RBF. |
| A replacement only needs a higher fee rate. | It must also pay a higher absolute fee, plus extra for its own relay (the incremental relay fee). |

## Session plan

| Time | Block | Who | Notes |
|---|---|---|---|
| 0:00-0:05 | Welcome and roles | Facilitator | Confirm roles and question owners |
| 0:05-0:15 | Opening question | Facilitator | Who should pay for block space? |
| 0:15-0:30 | Concepts | Facilitator | Slides 5-9: implicit fee, weight, legacy vs segwit table, coin selection, RBF/CPFP |
| 0:30-1:05 | Question round | Question owners, devil's advocate | 6 questions, about 6 minutes each |
| 1:05-1:20 | Exercise walkthrough | Exercise driver | Lab steps 2-3: legacy vs segwit, weight by hand. Step 6 (bumpfee) if time |
| 1:20-1:27 | Takeaways | Summariser | 3 takeaways, open questions |
| 1:27-1:30 | Before next Monday | Facilitator | Week 5 lessons, roles, Python lab reminder |

## Facilitator tips

Before the session:

- Run lab steps 2, 3 and 6 yourself so you can show the numbers if the exercise driver's setup breaks.
- Check the current mempool.space fee estimates just before the session, to compare with what participants recorded.
- Check that `python3 week-04/check.py` (from `decoding-bitcoin/`) runs, so you can help people with the Python lab.

Where people get stuck:

- **Rounding vsize.** vsize is weight / 4 rounded up. 561 WU is 141 vB, not 140.
- **Counting the marker and flag.** They are witness bytes (1 WU each), not base bytes.
- **Weight formula confusion.** `base × 4 + witness` and `base × 3 + total` are the same thing. People mix up "total" and "witness".
- **Change arithmetic in step 4.** Amounts with many decimals are easy to get wrong. Suggest doing it in satoshis with Python, then converting back to BTC.
- **`bumpfee` errors.** If a transaction is already confirmed (someone mined a block), it can't be bumped. Send a new low-fee transaction and bump it before mining.
- **Picking non-segwit inputs in step 4.** Legacy inputs from the week 3 lab change the size estimate. Check that both addresses start with `bcrt1q`.

## Glossary

- **Fee:** sum of inputs minus sum of outputs.
- **Fee rate:** fee divided by vsize, in sat/vB.
- **Weight unit (WU):** the block space unit since segwit. Base bytes count 4, witness bytes count 1.
- **Virtual size (vsize, vB):** weight / 4, rounded up.
- **Base size (stripped size):** the size of the transaction without marker, flag and witness.
- **Witness discount:** witness bytes cost 1/4 of base bytes.
- **Coin selection:** choosing which UTXOs to spend.
- **Change output:** the output that returns leftover value to the sender.
- **Dust:** an output worth less than the cost of spending it at the dust relay fee rate.
- **RBF (replace-by-fee):** replacing an unconfirmed transaction with a conflicting one that pays more.
- **CPFP (child pays for parent):** a child transaction with a high fee that pulls its parent into a block.
- **Package:** a group of related unconfirmed transactions (parent and child) considered together.
- **Mempool minimum fee:** the lowest fee rate a node accepts right now. Rises when the mempool is full.

## Further resources

- [BIP 141: Segregated Witness](https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki): defines weight, the block weight limit and virtual size.
- [BIP 125: Opt-in Full Replace-by-Fee Signaling](https://github.com/bitcoin/bips/blob/master/bip-0125.mediawiki): the original RBF rules.
- [Bitcoin Optech: Replace-by-fee](https://bitcoinops.org/en/topics/replace-by-fee/), [CPFP](https://bitcoinops.org/en/topics/cpfp/), [Coin selection](https://bitcoinops.org/en/topics/coin-selection/) and [Fee estimation](https://bitcoinops.org/en/topics/fee-estimation/).
- [Bitcoin Optech: Segregated witness](https://bitcoinops.org/en/topics/segregated-witness/): history and the witness discount.
- [learnmeabitcoin: Transaction](https://learnmeabitcoin.com/technical/transaction/): includes sizes of each field, useful for estimating vsize.
- [mempool.space](https://mempool.space): live fee estimates and mempool history graphs.
- [Mastering Bitcoin](https://github.com/bitcoinbook/bitcoinbook): the chapter on transaction fees.
