---
marp: true
theme: default
paginate: true
title: "Decoding Bitcoin, Week 4: Building a transaction and paying the fee"
---

# Decoding Bitcoin

## Week 4: Building a transaction and paying the fee

Coin selection, weight, vbytes, fee markets

<!--
Welcome. Tonight is the most numbers-heavy session so far. Have a calculator or Python ready.
-->

---

# Tonight (90 min)

| Time | Block |
|---|---|
| 0:00 | Welcome and roles (5) |
| 0:05 | Opening question (10) |
| 0:15 | Concepts: fees, weight, coin selection, RBF/CPFP (15) |
| 0:30 | Question round: 6 questions (35) |
| 1:05 | Exercise walkthrough: legacy vs segwit (15) |
| 1:20 | Takeaways (7) |
| 1:27 | Before next Monday (3) |

<!--
Facilitator keeps time.
-->

---

# Roles this week

- **Facilitator:** time, opening question, quiet voices
- **Summariser:** takeaways on Discord within a day
- **Devil's advocate:** "Why not just make blocks bigger?"
- **Exercise driver:** legacy vs segwit, live
- Question owners explain first

<!--
Confirm roles and question owners. The exercise driver should have lab step 2 ready.
-->

---

# Opening question

> Who should pay for block space, and how should they decide how much?

<!--
Possible directions: sender vs receiver, per byte vs per value, auction vs fixed price.
Ask: why does a 1 BTC payment and a 1000 BTC payment pay the same fee if they are the same size?
Devil's advocate: bigger blocks. Bring it back: every node must check and store the data.
-->

---

# The fee is not written down

```
inputs  (looked up in UTXO set):  1.00000000
outputs (in the transaction):    -0.99990000
fee (to the miner):               0.00010000
```

- Nodes look up input amounts by outpoint
- Miner claims fees in the coinbase
- Forgotten change = huge fee

<!--
Ask the owner of question 1 to hold their answer: just tease it here.
Connect to week 2: the max-fee-exceeded error.
-->

---

# Weight and vbytes

```
weight = base × 4 + witness × 1
       = base × 3 + total
vsize  = ceil(weight / 4)
block limit = 4,000,000 WU
```

- Fee rate is quoted in sat/vB
- Legacy: vsize = size
- Segwit: witness bytes are 4× cheaper

<!--
Do one example out loud: base 113, total 222. Weight 561, vsize 141.
-->

---

# Same payment, two formats

| 1 in, 2 out | size | weight | vsize |
|---|---|---|---|
| P2PKH (legacy) | 225 | 900 | 225 |
| P2WPKH (segwit) | 222 | 561 | 141 |

- Same 10,000 sat fee
- 44 sat/vB vs 71 sat/vB
- Rule of thumb: 10.5 + 68/input + 31/output

<!--
These numbers come from lab step 2. Byte sizes are almost equal; weight is very different.
Ask: why is the segwit input "68 vB" when it is 148 bytes in legacy? (Signature and key moved to the discounted witness.)
-->

---

# Coin selection

- Cover amount + fee (fee grows with each input)
- Branch and Bound: exact match, no change
- CoinGrinder: lightest inputs when fees are high
- Watch out: many tiny inputs, privacy leaks
- Dust: costs more to spend than it's worth

<!--
Bitcoin Core runs several algorithms and keeps the lowest "waste".
Dust limits: 546 sats P2PKH, 294 P2WPKH, 330 P2TR (at 3 sat/vB dustrelayfee).
-->

---

# Stuck? RBF or CPFP

```
RBF:   tx (1 sat/vB)  --replaced by-->  tx' (10 sat/vB)
CPFP:  parent (1 sat/vB) <-- child (high fee)
       miner sees package rate = total fee / total vsize
```

- RBF: sender, cheaper, one transaction
- CPFP: receiver can do it too

<!--
Full RBF is default since v28. 1-parent-1-child package relay since v28 helps CPFP.
Lab step 6 shows bumpfee; stretch A shows CPFP.
-->

---

# Question round

1. Where is the fee written? (Trick question)
2. Weight units and vbytes: why is witness cheaper?
3. How does a wallet choose UTXOs? What goes wrong?
4. What is dust? Why refuse to relay it?
5. RBF and CPFP: when to use each?
6. What drives the fee market?

<!--
About 6 minutes per question. Owner explains, then discussion.
Devil's advocate on 2: "Isn't the discount just a subsidy for some users?"
-->

---

# Exercise walkthrough: legacy vs segwit

```bash
bitcoin-cli -regtest decoderawtransaction "$LEG_SIGNED" \
  | jq '{size, vsize, weight}'
bitcoin-cli -regtest decoderawtransaction "$SW_SIGNED" \
  | jq '{size, vsize, weight}'
python3 -c "import math; w=113*3+222; print(w, math.ceil(w/4))"
```

<!--
Exercise driver shares lab steps 2 and 3. Do the weight calculation by hand together.
If time allows, show bumpfee (step 6).
Mention the Python lab: python3 week-04/check.py from decoding-bitcoin/.
-->

---

# Takeaways

- Fee = inputs - outputs; nobody writes it down
- Pay per vbyte, not per bitcoin
- Witness bytes count a quarter
- RBF for senders, CPFP for anyone with an output

<!--
Summariser reads back takeaways. Collect open questions.
-->

---

# Before next Monday

Week 5: Signing and the transaction exercises

- [Signing Transactions](https://bitcoindevs.xyz/decoding/transaction-signing)
- [Exercises (GitHub Classroom)](https://bitcoindevs.xyz/decoding/transaction_exercises)
- Claim your question and next week's roles
- Finish the Python fees lab if you can

<!--
Next week: what exactly a signature commits to. Start the GitHub Classroom exercises early, they take time.
Assign roles for week 5.
-->

---

# Thank you

- Summariser posts takeaways tomorrow
- Post your fee market readings on Discord
- See you next Monday

<!--
End on time.
-->
