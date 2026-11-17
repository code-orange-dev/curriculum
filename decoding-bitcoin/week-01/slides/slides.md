---
marp: true
theme: default
paginate: true
title: "Decoding Bitcoin, Week 1: Orientation and foundations"
---

# Decoding Bitcoin

## Week 1: Orientation and foundations

Code Orange Dev School · 10-week study cohort

<!--
Welcome everyone as they join. Start on time, even if people are still arriving.
Ask people to rename themselves on Discord to the name they want to be called.
-->

---

# Tonight (90 min)

| Time | Block |
|---|---|
| 0:00 | Welcome and how the cohort works (10) |
| 0:10 | Round of introductions (15) |
| 0:25 | Tour: dashboard and Decoding Bitcoin (10) |
| 0:35 | Opening question (10) |
| 0:45 | Concepts: digital cash, hashes, UTXOs (10) |
| 0:55 | Question round (20) |
| 1:15 | Live exercise: hash tool and a real transaction (10) |
| 1:25 | Roles for week 2 and next steps (5) |

<!--
Timings add up to 90 minutes. The facilitator keeps time.
This week is lighter: nobody had homework, so the question round is an open discussion.
-->

---

# How the cohort works

- 10 weeks, one 90-minute session every Monday
- Lessons on Decoding Bitcoin, read before Monday
- Each person owns one discussion question
- Socratic seminar: we ask, explain, challenge
- Homework starts in week 2

<!--
Explain the weekly rhythm: lessons during the week, own one question, come ready to explain it.
Stress that it is fine to be wrong. Explaining out loud is how we learn.
Model answers are in solutions/, but try first.
-->

---

# Rotating roles

- **Facilitator:** keeps time, asks the opening question
- **Summariser:** posts takeaways on Discord within a day
- **Devil's advocate:** pushes back, asks "are you sure?"
- **Exercise driver:** shares screen for one exercise
- Roles change every week

<!--
This week the organisers fill the roles. At the end we ask for volunteers for week 2.
The facilitator also brings in quiet voices: ask people by name, kindly.
-->

---

# Introductions (2 min each)

- Your name and where you are
- What you code in, what you work on
- Why you joined
- One thing you'd like to build

<!--
Keep each intro to about 2 minutes. With a large group, split into breakout rooms of 4-5.
Facilitator goes first to show the length and tone.
-->

---

# Opening question

> If you had to explain Bitcoin to a friend in two sentences, what would you say, and what would you leave out?

<!--
Give 1 minute of silent thinking, then ask 3-4 people.
Follow up: what did you leave out? Why? Mining? Keys? Price?
Write the most common words on a shared note. We come back to them in week 10.
-->

---

# The double-spend problem

- Digital data can be copied
- So what stops spending one coin twice?
- DigiCash: a central company checks every payment
- b-money, Bit Gold: ideas, no complete system
- Bitcoin: proof of work + most-work chain

<!--
The key point: before Bitcoin, preventing double spends needed a trusted party.
Bitcoin gives everyone the same order of transactions with no central server.
Don't go deep into mining here. It comes later.
-->

---

# Hash functions

```
SHA-256("satoshi") -> 32 bytes, looks random
SHA-256("satoshj") -> 32 bytes, totally different
```

- Any input, fixed-size output
- One-way: can't go back
- No two inputs with the same hash (in practice)
- Small change, about half the bits flip

<!--
Ask: where does Bitcoin use hashes? Expected: txids, block hashes, mining, addresses, Merkle trees.
Bitcoin often hashes twice: SHA-256 of SHA-256, called hash256.
-->

---

# Coins, not accounts (UTXOs)

```
tx A: 50 BTC coin  -->  [ 10 to Bob | 39.9999 change ]
tx B: spends Bob's 10 BTC coin --> new coins
```

- Transactions destroy coins and create new ones
- Unspent outputs = UTXOs
- Nodes keep the UTXO set
- "Balance" = your wallet adds up your UTXOs

<!--
Banknote analogy: you can't tear a note in half, you pay and get change.
Ask: where is the fee in this picture? (Inputs minus outputs: 0.0001 BTC here.)
-->

---

# Don't trust, verify

- A full node checks every rule itself
- Signatures, no double spends, 21M limit
- Verify the software you download too
- Some trust remains: crypto, hardware, code

<!--
Link to the bitcoin_core_cli.md lab: verifying release signatures is the first "verify" step.
Ask: what do you trust today when you check your bank balance?
-->

---

# Question round

1. What did Bitcoin solve that DigiCash, b-money, Bit Gold could not?
2. One moment from Bitcoin history: why did it matter?
3. What is a hash function? Three properties Bitcoin uses?
4. The UTXO model in your words. Why no stored balance?
5. One advantage, one disadvantage of UTXOs vs accounts
6. "Don't trust, verify": what can you verify yourself?

<!--
About 3 minutes per question. This week, ask for volunteers or go round the room.
From week 2, each question has an owner who explains it first, then others add or challenge.
Devil's advocate: push on question 5 and 6.
-->

---

# Live exercise

1. Open the Hash Functions tool
2. Hash your name, change one letter, hash again
3. Open a recent block on mempool.space
4. Pick a transaction: inputs, outputs, fee
5. Which output is the change? Why?

<!--
Exercise driver (an organiser this week) shares screen.
Point out: inputs minus outputs = fee. Ask the group to vote on the change output and give reasons.
Exercises are in exercises/README.md.
-->

---

# Before next Monday

Week 2: How a transaction lives

- [Transactions roadmap](https://bitcoindevs.xyz/decoding/roadmap)
- [Transaction Lifecycle](https://bitcoindevs.xyz/decoding/transaction-lifecycle)
- [Transaction Structure](https://bitcoindevs.xyz/decoding/transaction-structure) (first read)
- Pick your question, set up regtest (`bitcoin_core_cli.md`)

<!--
Assign question owners for week 2 now, or ask people to claim one on Discord.
Ask for volunteers: facilitator, summariser, devil's advocate, exercise driver.
Remind people to get Bitcoin Core v29+ running before week 2. The lab builds on it.
-->

---

# Thank you

- Summariser: takeaways on Discord tomorrow
- Questions any time on Discord
- See you next Monday

<!--
End on time. Thank everyone. Stay 5 minutes after for anyone with setup problems.
-->
