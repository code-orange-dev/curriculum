---
marp: true
theme: default
paginate: true
title: "Decoding Bitcoin, Week 2: How a transaction lives"
---

# Decoding Bitcoin

## Week 2: How a transaction lives

From wallet, to mempool, to block

<!--
Welcome back. This is the first week with homework, so check who did the lessons and exercises.
Remind people that being unsure is fine: we figure it out together.
-->

---

# Tonight (90 min)

| Time | Block |
|---|---|
| 0:00 | Welcome and roles (5) |
| 0:05 | Opening question (10) |
| 0:15 | Concepts: lifecycle, mempool, reorgs, structure (15) |
| 0:30 | Question round: 6 questions (35) |
| 1:05 | Exercise walkthrough: regtest lab (15) |
| 1:20 | Takeaways (7) |
| 1:27 | Before next Monday (3) |

<!--
Facilitator keeps time. Question round is about 6 minutes per question.
If the question round runs long, shorten the exercise walkthrough, not the takeaways.
-->

---

# Roles this week

- **Facilitator:** time, opening question, quiet voices
- **Summariser:** takeaways on Discord within a day
- **Devil's advocate:** "Is it really final?"
- **Exercise driver:** shares screen for the lab
- Question owners: explain first, then discuss

<!--
Read out who has which role and which question.
If a question owner is missing, ask for a volunteer or take it yourself.
-->

---

# Opening question

> When is a bitcoin payment actually final, and who gets to decide?

<!--
Give a minute to think. Push for specifics: after broadcast? 1 block? 6 blocks? Never fully?
Who decides: the receiver! Each receiver chooses how much risk to accept.
Devil's advocate: "What about a 100-block reorg?"
-->

---

# The life of a payment

```
wallet --build+sign--> node --relay--> peers --> mempools
                                                  |
                        miner picks by fee rate <-+
                                  |
                       block --> every node re-checks
                                  |
                    1 conf, 2 conf, ... 6 conf
```

- Every node checks everything itself

<!--
Walk the diagram left to right. Ask: where does validation happen? (Every node, at relay time and again in the block.)
Point out that the wallet does the creative work, nodes just verify.
-->

---

# The mempool is local

- Valid, unconfirmed transactions in one node's memory
- Every node has its own mempool
- Different arrival order, different policies
- Full mempool: lowest fee rate evicted
- Only the blockchain is shared

<!--
Ask: if you look at mempool.space, whose mempool are you seeing? (Their nodes'.)
Mention maxmempool default 300 MB, and that mempoolminfee rises when full.
-->

---

# Reorgs and confirmations

```
        +-- B3 -- B4          <- loser (B3 txs back to mempool)
B1 -- B2
        +-- B3' -- B4' -- B5' <- more work wins
```

- Nodes follow the valid chain with most work
- 1 confirmation can be undone
- Risk drops fast with each block (if attacker < 50%)

<!--
Natural 1-block reorgs happen when two miners find blocks at once.
Reorg Calculator, 10% attacker: about 20% after 1 conf, 1.3% after 3, 0.02% after 6 (whitepaper formula).
-->

---

# Coins are spent whole

```
input:  50 BTC coin (txid:0)
outputs: 1 BTC     -> Bob
         48.99998590 -> Alice (change)
fee:     50 - 49.99998590 = 0.0000141 BTC
```

- No partial spending of an output
- Forget change? It becomes fee

<!--
These are real numbers from the regtest lab: 141 vB at 10 sat/vB = 1410 sats.
Ask: where is the fee written in the transaction? Nowhere. Next weeks build on this.
-->

---

# Parts of a transaction

| Part | What it is for |
|---|---|
| version | which rules apply |
| inputs | which coins are spent, plus unlocking data |
| outputs | amount + locking script |
| (witness) | signatures for segwit inputs |
| locktime | earliest time it can be mined |

- An input points to `txid:vout` (an outpoint)

<!--
Keep it high level. Byte-level details are next week.
Ask: what is NOT in a transaction? No sender, no fee field, no input amounts.
-->

---

# Question round

1. Lifecycle: who builds, relays, checks, confirms?
2. What is the mempool? Why no single shared one?
3. What is a reorg? Why wait for more confirmations?
4. Why does change go back as a new output?
5. Main parts of a transaction, in order
6. What does an input point to? Why is that enough?

<!--
Each owner explains for about 2-3 minutes, then 3 minutes of discussion.
Devil's advocate: challenge question 2 (isn't mempool.space "the" mempool?) and question 6 (how do you know the old coin is valid?).
-->

---

# Exercise walkthrough: manual transaction

```bash
bitcoin-cli -regtest createrawtransaction "$INPUTS" "$OUTPUTS"
bitcoin-cli -regtest -rpcwallet=alice \
  signrawtransactionwithwallet "$RAW"
bitcoin-cli -regtest testmempoolaccept '["'$SIGNED'"]'
bitcoin-cli -regtest sendrawtransaction "$SIGNED"
bitcoin-cli -regtest getmempoolentry "$TXID"
```

<!--
Exercise driver shares screen and does lab steps 7-10 (exercises/README.md).
Show the forgotten-change mistake with testmempoolaccept: max-fee-exceeded.
Show depends/spentby for the child transaction. If time is short, skip the child.
-->

---

# Takeaways

- Finality is probability, chosen by the receiver
- Each node has its own mempool
- Outputs are spent whole; change is a new output
- Inputs point to outpoints; nodes look them up

<!--
Ask the summariser to read back 3 takeaways from the discussion. Correct anything wrong.
Ask: what is still unclear? Note it for next week.
-->

---

# Before next Monday

Week 3: Inside a transaction, byte by byte

- [Technical Foundation](https://bitcoindevs.xyz/decoding/technical-foundation)
- [Transaction Structure](https://bitcoindevs.xyz/decoding/transaction-structure) (second read: every field)
- Tool: [Transaction Decoder](https://bitcoindevs.xyz/decoding/transaction-decoder)
- Claim your question and next week's roles

<!--
Next week is byte-level. Suggest people keep their regtest node from this week: the week 3 lab uses it.
Assign roles for week 3 before closing.
-->

---

# Thank you

- Summariser posts takeaways tomorrow
- Questions on Discord any time
- See you next Monday

<!--
End on time. Stay a few minutes for anyone stuck on the regtest setup.
-->
