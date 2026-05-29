# Bitcoin Privacy Developer Track

**24 bi-weekly sessions. 12 months. Every session produces a contribution to Bitcoin base-layer privacy.**

---

## Why This Track Exists

> *"There are real privacy gaps on-chain today. Much of that sits in wallet behavior and transaction construction, which makes it a great area for open-source development."* — [OpenSats, Spring 2026 Call for Applications](https://opensats.org/blog/call-for-applications-spring-2026)

People accepting bitcoin for their work, running a small business, donating to causes, or saving for the future reasonably expect the same kind of day-to-day financial privacy they would get from traditional banking tools. But Bitcoin's base layer has serious privacy problems: address reuse exposes payment history, the common-input-ownership heuristic lets chain analysis firms cluster wallets, wallet software creates identifiable fingerprints in every transaction, and light clients leak user addresses to third parties.

The solutions exist — [Silent Payments](https://opensats.org/topics/silent-payments), [Payjoin](https://opensats.org/topics/payjoin), [Coinswap](https://opensats.org/blog/developing-advancements-in-onchain-privacy#coinswap), compact block filters ([BIP157](https://opensats.org/topics/bip-157)/[BIP158](https://opensats.org/topics/bip-158)), [ASmap](https://opensats.org/blog/bitcoin-grants-september-2024-7th-wave#asmap), and privacy-aware transaction construction — but they need developers to build, integrate, and maintain them. The biggest bottleneck in Bitcoin privacy is not research. It is a shortage of developers who understand the problems deeply enough to write the code.

**This curriculum produces those developers.**

From session 1, participants read real Bitcoin source code and engage with real repos. By session 8, they've submitted their first PR. By session 24, they have 5-8 PRs across 3+ repos — to the same projects that [OpenSats](https://opensats.org/), [HRF](https://hrf.org/), and [Brink](https://brink.dev/) fund.

---

## Format

| | |
|---|---|
| **Structure** | 24 bi-weekly sessions (every 2 weeks), 2-2.5 hours each |
| **Duration** | 12 months |
| **Participation** | **Open and flexible.** Participants can join at any session, attend the ones relevant to them, and come and go as they wish. Each session is designed to be self-contained — you don't need to have attended previous sessions to get value. Some developers will do all 24; others will drop in for the Payjoin block or the P2P privacy sessions and skip the rest. All are welcome. |
| **Prerequisites** | Basic Bitcoin knowledge (completed Bitcoin Dojo or equivalent). Comfortable reading code. Python or Rust experience helpful. |
| **Outcome** | Every graduate has multiple merged PRs across Bitcoin privacy projects. Every graduate can articulate what base-layer privacy problems remain unsolved and how to fix them. |
| **License** | CC0 1.0 Universal (public domain) |

---

## A Note for Tutors

**You don't need to be a deep technical expert to teach this track.** This curriculum is designed so that the tutor learns alongside the participants. Every session includes a "Tutor Preparation" section that explains the concepts in plain language, tells you exactly what to study before the session, gives you the key points to convey, warns you about common questions participants will ask, and tells you how to handle things you don't know.

The secret to teaching this well:

1. **Do the reading.** Each session lists 2-3 resources. Read them the week before. You don't need to understand every line of code — you need to understand the *concept* well enough to explain *why it matters for privacy*.
2. **Do the exercises yourself first.** Run through the Build section before the session. You'll hit the same errors participants will hit. That's gold — you'll know how to help them.
3. **Be honest about what you don't know.** "I don't know, let's figure it out together" is a perfectly valid answer. The participants are developers — they respect honesty over faking expertise. Often someone in the room will know the answer.
4. **Focus on the WHY, not just the HOW.** You can always look up how ECDH works. What matters is *why* Silent Payments need ECDH, and what happens to user privacy without it.
5. **Use the analogies.** Each Tutor Preparation section includes plain-language analogies. Use them. They work.

---

## What This Track Directly Addresses

OpenSats' [Spring 2026 Call for Applications](https://opensats.org/blog/call-for-applications-spring-2026) specifically highlights that base-layer privacy work is where improvements carry the furthest. They call out that "much of [the privacy gap] sits in wallet behavior and transaction construction" and want to see "deeper integration of existing techniques into widely used wallets, research and tooling that strengthen the surrounding ecosystem."

This curriculum is built around those specific priorities:

| Privacy Gap | Plain-Language Explanation | Where We Contribute | Sessions |
|---|---|---|---|
| **Address reuse** | If you use the same Bitcoin address twice, anyone can see all payments you've ever received to it. It's like having one bank account number printed on a billboard. | [Silent Payments (BIP352)](https://github.com/bitcoin/bips/blob/master/bip-0352.mediawiki), [rust-silentpayments](https://github.com/cygnet3/rust-silentpayments), wallet integrations | 5-8 |
| **Common-input-ownership heuristic (CIOH)** | When you spend from multiple addresses in one transaction, chain analysts assume all those addresses belong to you — and they're usually right. This one assumption lets them cluster your entire wallet. | [Payjoin Dev Kit (BIP77/78)](https://github.com/payjoin/rust-payjoin), wallet integrations, [BTCPay Server](https://github.com/btcpayserver/btcpayserver) | 9-12 |
| **Wallet fingerprinting** | Every wallet builds transactions slightly differently — different version numbers, fee rates, output ordering. These tiny differences let analysts identify which wallet you use, even without knowing your address. | [Bitcoin Core](https://github.com/bitcoin/bitcoin) wallet, [BDK](https://github.com/bitcoindevkit/bdk), any wallet that constructs transactions | 2-4, 22 |
| **Light client privacy** | Most people don't run full nodes. Light wallets ask a server "do you have transactions for my address?" — which tells the server exactly which addresses are yours. | [Kyoto (BIP157/158)](https://github.com/rustaceanrob/kyoto), [Floresta](https://github.com/vinteumorg/Floresta) | 7, 14-15 |
| **P2P network surveillance** | When your node broadcasts a transaction, the first node that sees it can link your IP address to that transaction. Your ISP or a state-level adversary can monitor this. | [Bitcoin Core P2P](https://github.com/bitcoin/bitcoin), Dandelion++, [ASmap](https://github.com/sipa/asmap), Tor/I2P integration | 13-14 |
| **Transaction graph analysis** | Even if you mix your coins, analysts can follow the trail of transactions. Your coins leave a chain of breadcrumbs on the blockchain. | [Coinswap/Teleport](https://github.com/nickhntv/teleport-transactions), [JoinMarket NG](https://github.com/nickhntv/joinmarket-ng), CoinJoin tooling | 17-18 |
| **Coin selection privacy leaks** | How your wallet chooses which coins to spend reveals information. If it always picks the biggest coin, analysts can predict your balance. If it creates change, they can tell which output is payment and which is change. | [Bitcoin Core coin selection](https://github.com/bitcoin/bitcoin/blob/master/src/wallet/coinselection.cpp), [BDK](https://github.com/bitcoindevkit/bdk) | 3, 21 |
| **Taproot adoption gap** | Taproot makes complex transactions (multisig, timelocks) look identical to simple ones. But if only 5% of transactions use Taproot, those users stand out. Privacy needs a crowd. | Wallet integrations, [rust-bitcoin](https://github.com/rust-bitcoin/rust-bitcoin), BDK defaults | 16 |

---

## The Contribution Ladder

Contributions scale with knowledge. Nobody gets thrown into the deep end.

| Sessions | Contribution Level | Examples |
|---|---|---|
| 1-4 | **Engage** | Star repos, read source code, file issues, improve docs |
| 5-8 | **Submit** | Review PRs, add test cases, submit first PR |
| 9-12 | **Build** | Fix bugs, add features, submit PRs to multiple repos |
| 13-16 | **Lead** | Tackle harder issues, review others' PRs, mentor newcomers |
| 17-20 | **Research** | Identify gaps, propose improvements, build new tooling |
| 21-24 | **Ship** | Substantial contributions, present to community, join fellowship |

---

## Curriculum

### Phase 1: Foundations — How Privacy Breaks on Bitcoin's Base Layer
*Months 1-2 · Sessions 1-4*

Before building privacy solutions, developers must understand exactly how privacy fails today. This phase teaches the 5 primary chain analysis heuristics, how wallet software creates identifiable fingerprints, and why privacy must be solved at the protocol and wallet level — not bolted on as an afterthought.

---

#### Session 01: Chain Analysis & Surveillance — How Privacy Fails Today

##### Tutor Preparation

**Study time needed:** 2-3 hours the week before.

**What this session is about in plain language:** Chain analysis companies (Chainalysis, Elliptic) use a handful of simple tricks to figure out who owns which Bitcoin addresses. These tricks are called "heuristics" — rules of thumb that work most of the time. The most important one is: if two addresses appear as inputs in the same transaction, they probably belong to the same person. That single assumption lets them cluster hundreds of addresses into one identity. This session teaches participants what those tricks are, so they can later build tools that break them.

**The 5 heuristics you need to understand (and explain):**

1. **Common-input-ownership (CIOH):** "If Alice uses two different addresses as inputs in one transaction, both addresses are probably Alice's." *Analogy: if you pay for dinner using money from two different pockets, a watcher concludes both pockets are yours.*

2. **Change detection:** "In a 2-output transaction, one output is the payment and one is change sent back to the sender. Analysts try to figure out which is which." *Analogy: you hand a shopkeeper a $50 bill for a $30 item — they give you $20 back. An observer who sees both the $30 and $20 outputs can figure out which one is change if the wallet does something predictable (like always putting change second, or using a different address type for change).*

3. **Address reuse:** "If an address appears in multiple transactions, all those transactions are linked." *Analogy: using the same email address for everything — your Amazon purchases, your political donations, your medical bills — lets anyone who knows one of those accounts see all the others.*

4. **Timing analysis:** "When a transaction appears on the network correlates with time zones, working hours, and personal patterns." *Analogy: if someone always sends Bitcoin at 9am Bangkok time, they probably live in Southeast Asia.*

5. **Amount correlation:** "Round payment amounts (0.1 BTC, 0.01 BTC) stand out. Unusual amounts can be matched across transactions." *Analogy: if Alice sends exactly 0.31337 BTC and Bob receives 0.31337 BTC a few blocks later, they're probably connected even through a mixing step.*

**Key point to drive home:** These heuristics are not theoretical. Chainalysis uses them every day to trace millions of dollars. Governments buy this data. People have gone to prison based on chain analysis. This is why privacy tools matter — they're not for criminals, they're for everyone who wants basic financial privacy.

**Common questions participants will ask:**
- *"Isn't this just for criminals?"* → No. Greg Maxwell's 2013 quote is your answer: your in-laws seeing your birth control purchases, your employer seeing your donations, thieves seeing your wealth. Privacy is normal.
- *"Can't you just use a VPN/Tor?"* → That helps with IP privacy but doesn't help with on-chain analysis at all. The blockchain is permanent and public.
- *"Is Monero better?"* → Different tradeoffs. This track is about fixing Bitcoin's privacy, not switching chains.

**How to run this session:**
1. Open [mempool.space](https://mempool.space) on the projector. Pick a random recent transaction. Walk through it together: how many inputs? How many outputs? What script types? Can you guess which output is change?
2. Show a real address that's been reused (donation addresses are good examples). Show how you can see every transaction to/from it.
3. Then have participants do the Build exercises themselves.

---

**The problem:** Chain analysis firms like Chainalysis and Elliptic use 5 core heuristics to deanonymize Bitcoin users. Every on-chain transaction reveals information. Understanding what it reveals — and why — is the prerequisite for building solutions.

**Learn:**
- The 5 primary chain analysis heuristics: common-input-ownership (CIOH), change detection, address reuse, timing analysis, amount correlation
- How chain analysis firms cluster addresses into identity groups
- What the UTXO model reveals vs what an account model reveals
- Why privacy is a protocol-level requirement, not a user preference — with real-world examples of harm from poor financial privacy (targeted theft, business intelligence leaks, discrimination)
- The chain analysis arms race: what's detectable today that wasn't 3 years ago

**Build:**
- Trace a 5-hop transaction chain on [mempool.space](https://mempool.space) and [OXT.me](https://oxt.me)
- Apply CIOH to cluster addresses. Identify likely change outputs using 4 different heuristics
- Write a Python script that takes a transaction ID and returns: input count, output count, script types, likely change output, fee rate, and a "privacy score" (0-100)
- Analyze 10 real mainnet transactions and classify each by privacy quality

**Contribute this session:**
- Create a GitHub account if you don't have one
- Star and fork these 7 repos (the projects you'll contribute to over 12 months):
  - [bitcoin/bitcoin](https://github.com/bitcoin/bitcoin) — Bitcoin Core
  - [cygnet3/rust-silentpayments](https://github.com/cygnet3/rust-silentpayments) — Silent Payments library
  - [payjoin/rust-payjoin](https://github.com/payjoin/rust-payjoin) — Payjoin Dev Kit
  - [vinteumorg/Floresta](https://github.com/vinteumorg/Floresta) — Privacy-preserving light client
  - [rustaceanrob/kyoto](https://github.com/rustaceanrob/kyoto) — BIP157/158 compact block filter client
  - [bitcoindevkit/bdk](https://github.com/bitcoindevkit/bdk) — Bitcoin Dev Kit
  - [rust-bitcoin/rust-bitcoin](https://github.com/rust-bitcoin/rust-bitcoin) — Rust Bitcoin library
- Clone `bitcoin/bitcoin` and build it locally. Read `src/wallet/coinselection.cpp` — you won't understand all of it yet, but you start reading real Bitcoin code on day one
- Read the [Bitcoin Wiki Privacy page](https://en.bitcoin.it/wiki/Privacy). Identify one section that's outdated or unclear — you'll file an issue or edit later

**Reading:**
- [Bitcoin Privacy Wiki](https://en.bitcoin.it/wiki/Privacy) (read fully)
- Greg Maxwell's [CoinJoin original post](https://bitcointalk.org/index.php?topic=279249.0) (2013)
- [An Empirical Analysis of Traceability in the Monero Blockchain](https://arxiv.org/abs/1704.04299) — read the methodology, not for Monero but to understand how academic deanonymization research works

---

#### Session 02: Transaction Anatomy for Privacy — What Every Byte Reveals

##### Tutor Preparation

**Study time needed:** 2-3 hours.

**What this session is about in plain language:** A Bitcoin transaction is just a blob of data — a few hundred bytes. But every byte carries information. The version number, the locktime field, the sequence numbers, the order of outputs, the type of script used — all of these are slightly different depending on which wallet software built the transaction. It's like handwriting analysis: even if you write the same words, an expert can tell which pen you used, whether you're left-handed, and approximately where you went to school. That's what wallet fingerprinting is.

**Key concept to explain — "transaction construction":** This is the term OpenSats uses repeatedly. It means: the process by which a wallet builds a raw Bitcoin transaction before broadcasting it. The *choices* the wallet makes during construction — which inputs to use, what order to put outputs in, what fee rate to set, what locktime value to pick — these are the fingerprint. OpenSats specifically says this is "a great area for open-source development to improve the experience for users."

**What you need to understand about transaction fields:**
- **nVersion:** Almost always 1 or 2. Some wallets always use 2, some use 1. This alone is a tell.
- **nLockTime:** Anti-fee-sniping wallets set this to the current block height. Others leave it at 0. If your locktime is 0 and Bitcoin Core's is the block height, analysts know you're not using Bitcoin Core.
- **nSequence:** RBF (replace-by-fee) signaling. Bitcoin Core uses `0xFFFFFFFD` by default. Other wallets use `0xFFFFFFFF`. Another fingerprint.
- **Output ordering:** Some wallets put the payment first, change second. Some do the opposite. Some randomize. BIP69 suggests a deterministic order — but using BIP69 is itself a fingerprint.
- **Script types:** If your inputs are P2WPKH (SegWit) but your change is P2TR (Taproot), that mismatch tells the analyst which output is change.

**Analogy for participants:** Imagine you're sending a letter. The words are what you want to say (the payment). But the envelope, the stamp placement, the handwriting, the ink color, the type of paper — all of that tells the postal service (the analyst) who you are, even if you don't write your return address.

**Common questions:**
- *"Why don't all wallets just agree on one standard?"* → They should! That's partly what this track is about. But coordination is hard, and many wallet developers don't prioritize privacy.
- *"How much does fingerprinting really matter?"* → A lot. If an analyst can narrow you down to "this came from Electrum," they've eliminated 90% of wallets. Combined with other heuristics, it's very powerful.

**How to run this session:**
1. Have participants decode a raw transaction hex manually — field by field. You can use [learnmeabitcoin.com](https://learnmeabitcoin.com/technical/transaction/) as a reference.
2. Show 3-4 transactions side by side. Ask: "which wallet made each one?" Walk through the clues together.
3. Then have them build a transaction that's intentionally fingerprint-clean.

---

**The problem:** Every field in a raw Bitcoin transaction carries information. Version numbers, locktime values, sequence numbers, output ordering, script types, and fee rates create fingerprints that identify which wallet software created the transaction.

**Learn:**
- Raw transaction structure byte-by-byte: nVersion, vin[], vout[], nLockTime
- How nVersion, nLockTime, and nSequence differ across wallet implementations — and why those differences matter
- Script types and their privacy implications: P2PKH, P2SH, P2WPKH, P2WSH, P2TR
- Fee estimation patterns as wallet fingerprints
- Output ordering: BIP69 (deterministic) vs random vs amount-sorted — each is a tell
- How [0xB10C's wallet fingerprinting research](https://b10c.me/observations/03-blocktemplate-coinbase-transactions/) revealed identifiable patterns in production wallets
- Why transaction construction is the Layer 1 privacy problem OpenSats specifically wants solved

**Build:**
- Decode 5 raw testnet transactions manually. For each, extract: version, locktime, sequence values, script types, fee rate, output ordering
- Determine which wallet software likely created each transaction based on fingerprints alone
- Construct a raw transaction that avoids all known wallet fingerprints — use random output ordering, anti-fee-sniping locktime, minimal nSequence signaling, and consistent script types

**Contribute this session:**
- Pick one wallet (Sparrow, BlueWallet, Electrum, Green, Nunchuk). Test its current version against known fingerprint patterns. Document: wallet version, transaction version, locktime behavior, sequence behavior, output ordering, script type defaults, fee estimation pattern
- If the behavior differs from published research, this is an issue worth filing. Draft a GitHub issue (you'll submit it in Session 4 after review)
- Browse the [Bitcoin Optech Topics page](https://bitcoinops.org/en/topics/). Find the "Transaction compatibility" section. Note anything missing or outdated

**Reading:**
- 0xB10C's [wallet fingerprinting observations](https://b10c.me/)
- [Wallet fingerprinting and transaction construction](https://ishaana.com/blog/wallet_fingerprinting/) by Ishaana Misra
- Bitcoin Core source: `src/wallet/spend.cpp` — focus on `CreateTransaction()` and how it sets version, locktime, output ordering

---

#### Session 03: UTXO Management & Coin Selection — The Hidden Privacy Leak

##### Tutor Preparation

**Study time needed:** 2 hours.

**What this session is about in plain language:** When you want to send 0.5 BTC, your wallet has to decide *which* of your coins to use. Maybe you have a 1 BTC coin and three 0.2 BTC coins. The wallet could use the 1 BTC coin (simpler, but creates a 0.5 BTC change output). Or it could use the three 0.2 BTC coins (0.6 BTC total, smaller change). This choice — called "coin selection" — has huge privacy implications. The wrong choice can reveal your total balance, link your addresses together, or make it obvious which output is change.

**The 4 coin selection algorithms (explain these simply):**

1. **Largest-first:** Always pick the biggest coin. Simple, but terrible for privacy — it reveals you have a coin at least that big, and always creates large change.
2. **Branch-and-bound (BnB):** Try to find an exact combination of coins that equals the payment amount. If it works, there's NO change output at all — which is ideal for privacy. This is what Bitcoin Core prefers.
3. **Knapsack:** Randomly tries combinations until it finds one close to the target. Less predictable, moderate privacy.
4. **Random:** Pick coins randomly until you have enough. Unpredictable to analysts, but may use more coins than necessary (linking more addresses together via CIOH).

**Key insight for participants:** The *best* outcome is no change output at all (BnB finds an exact match). The *worst* is when the change output is obviously identifiable (e.g., you pay 1.0 BTC and get back 0.00003241 BTC — that tiny output is obviously change).

**Why this matters for OpenSats:** Both [Bitcoin Core](https://github.com/bitcoin/bitcoin) and [BDK](https://opensats.org/projects/bdk) handle coin selection. Both are funded by OpenSats. Improvements to coin selection in these foundational libraries cascade to every wallet that uses them.

**Common questions:**
- *"Why can't the wallet just always use BnB?"* → BnB only works when there's a combination of coins that exactly matches the target. Often there isn't.
- *"What about dust attacks?"* → Someone sends you tiny amounts (dust) to create trackable UTXOs in your wallet. If your wallet later spends that dust alongside your real coins, the attacker links your addresses.

---

**The problem:** How a wallet chooses which UTXOs to spend reveals enormous amounts of information. This is where [Bitcoin Core](https://github.com/bitcoin/bitcoin/blob/master/src/wallet/coinselection.cpp) and [BDK](https://github.com/bitcoindevkit/bdk) — two of the most important foundational libraries funded by OpenSats — directly affect every user's privacy.

**Learn:**
- 4 coin selection algorithms: largest-first, branch-and-bound (BnB), knapsack, and random
- How each algorithm affects privacy differently — and why BnB is preferred when it finds an exact match (no change output = no change detection heuristic)
- [Murch's coin selection research](https://murch.one/wp-content/uploads/2016/11/erhardt2016coinselection.pdf) and its influence on Bitcoin Core
- Dust attacks: how tiny UTXOs are used as tracking beacons
- Coin control: manual UTXO selection as a privacy tool
- How BDK exposes coin selection to wallet developers — and why privacy-aware defaults matter

**Build:**
- Implement all 4 coin selection algorithms in Python
- Run each against an identical UTXO set for the same payment amount
- Score each for privacy leakage: input count, change amount, whether change is detectable, total fees
- Identify which algorithm produces a changeless transaction (if any) for the given inputs and amount
- Build a "privacy-optimized" selector that prefers: changeless transactions > same-script-type change > minimal input count

**Contribute this session:**
- Read Bitcoin Core's coin selection: `src/wallet/coinselection.cpp` and `src/wallet/spend.cpp`. Find a comment that could be clearer, a variable name that's confusing, or an edge case that isn't tested. Even a 1-line documentation improvement counts
- Browse [BDK issues labeled "coin-selection"](https://github.com/bitcoindevkit/bdk/labels/coin-selection). Read through open issues. If you can reproduce one, comment with your findings
- Look at Murch's research. Are the algorithms described there fully implemented in Bitcoin Core today? If something's missing, that's a potential contribution

**Reading:**
- Murch's [coin selection thesis](https://murch.one/wp-content/uploads/2016/11/erhardt2016coinselection.pdf)
- Bitcoin Core source: `src/wallet/coinselection.cpp` (full file)
- BDK documentation on [coin selection](https://docs.rs/bdk_wallet/latest/bdk_wallet/)

---

#### Session 04: Wallet Fingerprinting & Privacy-Clean Transaction Construction

##### Tutor Preparation

**Study time needed:** 2 hours.

**What this session is about in plain language:** This is the "pull it all together" session for Phase 1. Participants now know the 5 heuristics (Session 1), understand what each byte of a transaction reveals (Session 2), and know how coin selection leaks information (Session 3). Now they put it all into practice: analyze real transactions to identify wallets, and build a transaction that's intentionally designed to leak nothing.

**This is also the first real contribution session.** Participants file their first GitHub issue or documentation PR. This is a big deal — many people are intimidated by contributing to open-source Bitcoin projects. Your job as tutor is to make it feel achievable:
- "You're not rewriting Bitcoin Core. You're filing a well-described issue about a wallet fingerprint you found."
- "Documentation PRs are how every Bitcoin Core contributor started."
- "The maintainers want help. They'll be glad to see your issue."

**How to handle the contribution part:**
1. Have everyone pick Option A, B, C, or D before they start
2. Walk the room and help people draft their issue/PR. Read their text. Suggest improvements.
3. If someone is stuck, pair them with someone more confident
4. The goal: everyone leaves with something submitted or ready to submit

---

**The problem:** If every Bitcoin wallet constructed transactions identically, chain analysis would lose one of its most powerful tools. Fixing this requires work in the foundational libraries ([rust-bitcoin](https://github.com/rust-bitcoin/rust-bitcoin), [BDK](https://github.com/bitcoindevkit/bdk)) and in individual wallets. This is the "deeper integration of existing techniques into widely used wallets" that OpenSats wants to see.

**Learn:**
- Complete catalog of known wallet fingerprints: Bitcoin Core, Electrum, BlueWallet, Wasabi, Sparrow, Green, Nunchuk, Samourai (legacy)
- How to construct a "fingerprint-clean" transaction: randomized output ordering, anti-fee-sniping locktime, consistent script types, standard fee rates
- Transaction batching and its privacy implications — when it helps and when it hurts
- How rust-bitcoin's transaction builder API affects downstream wallet privacy
- The concept of "privacy by default" in wallet design — users shouldn't need to think about fingerprinting

**Build:**
- Given 10 raw transactions, identify which wallet created each by analyzing every available signal
- Construct a raw transaction that avoids all known fingerprints. Have another participant try to identify the wallet — if they can't, you succeeded
- Write a "transaction construction privacy checklist" that wallet developers can use as a reference

**Contribute this session — your first real contribution:**
- **Option A:** File an issue on a Bitcoin wallet repo documenting a privacy fingerprint you discovered. Include: wallet version, the specific fingerprint, and why it matters for privacy
- **Option B:** Submit a documentation PR to the [Bitcoin Wiki Privacy page](https://en.bitcoin.it/wiki/Privacy) adding your fingerprint data
- **Option C:** Submit a PR to [rust-bitcoin](https://github.com/rust-bitcoin/rust-bitcoin) or [BDK](https://github.com/bitcoindevkit/bdk) improving transaction construction documentation or adding a privacy-related test case
- **Option D:** Write up your wallet fingerprinting analysis as a structured report and publish it as a GitHub gist — share in Code Orange Discord for community review

> **Phase 1 checkpoint:** Every participant has starred 7 repos, read real Bitcoin Core source code, analyzed real transactions, and filed at least 1 issue or documentation PR. They understand the 5 chain analysis heuristics and how wallet behavior creates privacy leaks.

---

### Phase 2: Silent Payments (BIP352) — Solving Address Reuse at the Protocol Level
*Months 3-4 · Sessions 5-8*

> Every on-chain transaction that uses Silent Payments instead of reusing addresses raises the baseline privacy of everyday users with minimal change, if any, to how they already transact. — [OpenSats](https://opensats.org/blog/call-for-applications-spring-2026)

Address reuse is the most common on-chain privacy failure. [BIP352 Silent Payments](https://github.com/bitcoin/bips/blob/master/bip-0352.mediawiki) solves this by deriving unique addresses from a single public identifier using ECDH, without requiring any interaction between sender and receiver.

---

#### Session 05: BIP352 Deep Dive — How Silent Payments Work

##### Tutor Preparation

**Study time needed:** 3 hours. This is the most cryptography-heavy session. Don't panic.

**What this session is about in plain language:** The problem: if you put a Bitcoin address on your website for donations, everyone who donates to that address can see every other donation. They can see your total balance. They can see when you spend. Your donation page is a privacy disaster.

Silent Payments fix this. You publish ONE static identifier (not a regular Bitcoin address — a *Silent Payment address*). When someone sends you bitcoin, their wallet uses math (ECDH — more on this below) to derive a *unique, one-time address* that only you can spend from. No two senders ever use the same address. And the sender and receiver never need to communicate — the math works purely from public keys.

**ECDH explained simply (you MUST understand this to teach it):**

ECDH stands for Elliptic Curve Diffie-Hellman. Here's the core idea:
- Alice has a private key `a` and a public key `A = a*G` (where G is a known point on the curve)
- Bob has a private key `b` and a public key `B = b*G`
- Alice can compute `a*B = a*b*G`
- Bob can compute `b*A = b*a*G`
- These are the same point! `a*b*G = b*a*G`
- So they've created a shared secret without ever communicating their private keys

*Analogy: Alice and Bob each have a secret color. They publicly share yellow paint. Alice mixes her secret color with yellow, Bob mixes his with yellow, and they exchange results. Now each can mix in their own secret to arrive at the same final color — but nobody watching can figure out what it is.*

For Silent Payments, the sender uses their private key and the receiver's public scan key to derive a shared secret. That shared secret tweaks the receiver's spend key to produce a unique output. Only the receiver (who has the scan private key) can detect and spend the output.

**The scanning problem (important to explain):**
The receiver doesn't know when someone has sent them a Silent Payment. They have to check EVERY transaction in EVERY block — "does this transaction contain an output for me?" This is computationally expensive. For a full node it's feasible. For a phone wallet, it's a real challenge. This is why compact block filters (BIP157/158) and projects like [Kyoto](https://github.com/rustaceanrob/kyoto) matter — they reduce the scanning burden.

**Common questions:**
- *"Why not just use HD wallets?"* → HD wallets generate fresh addresses, but you need to give each sender a different address. That requires interaction (the receiver must be online or pre-generate addresses). Silent Payments work with a single static identifier — no interaction needed.
- *"How is this different from Monero stealth addresses?"* → Similar concept, but BIP352 is designed specifically for Bitcoin's UTXO model and uses input keys for the ECDH, which is a novel approach.

---

**The problem:** Existing solutions to address reuse (HD wallets, BIP47 payment codes) require interaction — the receiver must give the sender a fresh address. Silent Payments solve this using ECDH to derive unique outputs from a single static identifier.

**Learn:**
- The address reuse problem in depth: what exactly is revealed and to whom
- ECDH (Elliptic Curve Diffie-Hellman) shared secret derivation on secp256k1
- BIP352 specification walkthrough: scan keys vs spend keys, how the shared secret produces a unique output address, labeling for payment identification
- Why scanning is computationally expensive — the sender's public keys must be extracted from every transaction input, and ECDH computed for each
- How Silent Payments compare to BIP47 (payment codes) and stealth addresses
- Current implementation status: Bitcoin Core PR [#28122](https://github.com/bitcoin/bitcoin/pull/28122), [rust-silentpayments](https://github.com/cygnet3/rust-silentpayments), wallet integrations in progress

**Build:**
- Derive Silent Payment shared secrets by hand using pure Python secp256k1 math
- Given a sender's private key and an SP address, compute the output key step by step: extract scan key, compute ECDH shared secret, derive tweak, add to spend key
- Verify your result against the official [BIP352 test vectors](https://github.com/bitcoin/bips/tree/master/bip-0352)

**Contribute this session:**
- Read the [BIP352 specification](https://github.com/bitcoin/bips/blob/master/bip-0352.mediawiki) end to end. If anything is ambiguous or could be explained better, file an issue on [bitcoin/bips](https://github.com/bitcoin/bips) with a specific suggestion
- Clone [cygnet3/rust-silentpayments](https://github.com/cygnet3/rust-silentpayments). Build it. Run the test suite. Read `sending.rs` — you just implemented this math by hand
- Browse [rust-silentpayments open issues](https://github.com/cygnet3/rust-silentpayments/issues). Comment on one with your understanding of the problem

---

#### Session 06: Implement a Silent Payments Sender

##### Tutor Preparation

**Study time needed:** 2 hours. Do the Build exercise yourself before class.

**What this session is about:** Participants implement the full Silent Payments sending pipeline. They did the math by hand in Session 5; now they build the complete flow in code: take an SP address, select inputs, compute the shared secret for each recipient, derive the unique output keys, and construct the transaction. Then they validate against the official test vectors.

**Your role this session:** This is mostly hands-on coding. Walk the room. Help people debug. The most common issues will be:
- Byte ordering mistakes (Bitcoin uses little-endian in many places)
- Key serialization errors (compressed vs uncompressed public keys)
- Getting the ECDH input wrong (it's the sum of all input public keys, not just one)

**If someone is stuck:** Have them pair up with someone who got further. Pair programming is how real open-source development works.

---

**Learn:**
- Complete SP send flow: input selection, key aggregation for multiple inputs, shared secret computation, output key derivation, transaction construction
- Handling edge cases: single vs multiple inputs, Taproot vs SegWit inputs, multiple SP recipients in one transaction
- Testing against the full BIP352 test vector suite

**Build:**
- Implement the full SP sending pipeline in Python: parse SP address → aggregate sender input keys → compute ECDH shared secret → derive output key → construct transaction
- Handle all edge cases: single Taproot input, mixed input types (P2WPKH + P2TR), multiple SP recipients
- Run your implementation against every test vector in [BIP352's test suite](https://github.com/bitcoin/bips/tree/master/bip-0352). All must pass

**Contribute this session:**
- Check the BIP352 test vectors. Are any edge cases missing? If you find a gap, file an issue on [bitcoin/bips](https://github.com/bitcoin/bips) proposing the additional test vector
- Add a test case to [rust-silentpayments](https://github.com/cygnet3/rust-silentpayments) exercising an edge case you identified
- If you're more comfortable in Python: clean up your sender implementation, add docstrings, and publish it as a reference tool on GitHub

---

#### Session 07: Scanning, Receiving & Compact Block Filters (BIP157/158)

##### Tutor Preparation

**Study time needed:** 2-3 hours.

**What this session is about in plain language:** Session 5-6 was about *sending* Silent Payments. This session is about *receiving* them — and that's where the hard problem is.

When someone sends you a Silent Payment, the transaction doesn't contain your address anywhere. The only way to know it's yours is to take every transaction in every block, extract the sender's public keys, run the ECDH math, and check if any output matches. For a full node processing every block, this is slow but possible. For a phone wallet? Way too heavy.

**The solution is compact block filters (BIP157/158).** Instead of downloading every block and checking every transaction, the light client downloads a small "filter" for each block (a few kilobytes). The filter lets the client check: "does this block *possibly* contain a transaction relevant to me?" If the answer is no, skip the block. If yes, download the full block and check properly. This dramatically reduces bandwidth and computation.

**Analogy:** You're looking for a specific book in a library. Instead of reading every book, you check the catalog (the filter). The catalog might say "this shelf possibly has your book" (a match, which could be a false positive) or "definitely not on this shelf" (a definite negative). You only read books from shelves the catalog flags.

**Why Kyoto and Floresta matter:** [Kyoto](https://github.com/rustaceanrob/kyoto) implements BIP157/158 in Rust — it's the light client that Silent Payments rely on for mobile wallets. [Floresta](https://github.com/vinteumorg/Floresta) takes a different approach using "utreexo" to validate transactions with very little storage. Both are funded by OpenSats. Both need contributors.

---

**The problem:** Receiving Silent Payments requires scanning every transaction in every block. Compact block filters let light clients check whether a block might contain relevant transactions without downloading the full block or revealing their addresses to a server.

**Learn:**
- The SP scanning algorithm: for each transaction, extract input public keys → compute ECDH → check if any output matches
- Compact block filters: Golomb-Rice Coded Sets (GCS), false positive rates, how BIP157 client-server protocol works
- How CBFs optimize SP scanning: download filter → check if block might have SP outputs → download full block only if filter matches
- Bandwidth vs privacy tradeoffs: full node scanning vs CBF light client vs Electrum-style server query
- [Kyoto](https://github.com/rustaceanrob/kyoto) architecture — a BIP157/158 light client that Silent Payments and other privacy tools rely on
- Tweak caching and other scanning optimizations

**Build:**
- Build a minimal SP scanner in Python: given a scan private key, iterate through blocks and find outputs addressed to you
- Implement Golomb-Rice encoding/decoding from scratch
- Build a compact block filter. Query it for a known output. Measure false positive rate
- Combine: use your CBF to skip blocks, then full-scan only matching blocks. Measure the speedup

**Contribute this session:**
- Review an open PR on [bitcoin/bitcoin](https://github.com/bitcoin/bitcoin) related to Silent Payments or compact block filters. Leave a thoughtful review
- Clone [rustaceanrob/kyoto](https://github.com/rustaceanrob/kyoto). Build it. Run it. This is an early-stage project that needs contributors
- If you found performance issues or bugs in your scanner, file them on the relevant repo with reproduction steps

---

#### Session 08: Contributing to Silent Payments — Your First PR

##### Tutor Preparation

**Study time needed:** 1-2 hours prep. This session is mostly facilitation.

**What this session is about:** This is a working session. Everyone submits a PR or a detailed code review. Your job is matchmaking — pairing each participant with an issue that matches their skill level.

**Before the session:**
1. Browse open issues on rust-silentpayments, Kyoto, and bitcoin/bitcoin (SP-related). Make a list of 10-15 approachable issues.
2. Categorize them: docs (easy), test cases (medium), bug fixes (harder), features (hardest).
3. For each participant, think about their skill level from Sessions 5-7. Who's strong in Rust? Who's more comfortable in Python? Who's a good writer (docs)?

**During the session:**
1. Spend the first 15 minutes matching people to issues. Write the assignments on a whiteboard.
2. Then let them work. Walk the room. Help with git, build issues, PR formatting.
3. At the end, have everyone show their PR (even if it's draft). Celebrate every submission.

**The phrase to repeat:** "Your PR doesn't have to be perfect. It has to exist." Maintainers can request changes. An imperfect PR that exists beats a perfect one that doesn't.

---

**Learn:**
- Bitcoin Core SP implementation walkthrough: code paths, test structure, review process
- [rust-silentpayments](https://github.com/cygnet3/rust-silentpayments) architecture deep dive
- Current wallet integration status: which wallets support SP, which are working on it, where the gaps are
- How to write a PR that gets reviewed and merged: commit messages, test coverage, description format

**Build:**
- Clone your target repo. Build locally. Run full test suite. Pick a Good First Issue. Write your fix. Submit your first PR.

**Contribute this session — submit a PR:**
- **Option A (Rust):** Add a test case, fix documentation, or implement a small feature in [rust-silentpayments](https://github.com/cygnet3/rust-silentpayments) or [Kyoto](https://github.com/rustaceanrob/kyoto)
- **Option B (C++):** Review and test a Silent Payments PR on [bitcoin/bitcoin](https://github.com/bitcoin/bitcoin). Leave a detailed review with test results
- **Option C (Any language):** Improve documentation for Silent Payments: BIP352, wallet integration guides, Bitcoin Optech
- **Option D (Ambitious):** Start integrating Silent Payments into a wallet that doesn't have it yet — even a proof-of-concept counts

**Nobody leaves this session without a PR submitted or a substantive review posted.**

> **Phase 2 checkpoint:** Every participant has submitted at least 1 PR or detailed code review to a Silent Payments or compact block filter project. They understand BIP352 cryptography, the scanning problem, and how CBFs enable light client privacy.

---

### Phase 3: Payjoin (BIP77/78) — Breaking the Most Powerful Chain Analysis Heuristic
*Months 5-6 · Sessions 9-12*

> Base-layer work is where privacy improvements carry the furthest. Every on-chain transaction that uses collaborative transaction methods such as Payjoin raises the baseline privacy of everyday users. — [OpenSats](https://opensats.org/blog/call-for-applications-spring-2026)

The common-input-ownership heuristic (CIOH) is the single most powerful tool in chain analysis. [Payjoin](https://opensats.org/topics/payjoin) breaks this assumption by having both sender and receiver contribute inputs — making the on-chain result indistinguishable from a regular payment.

Unlike CoinJoin (which creates distinctive equal-output transactions), Payjoin transactions look like ordinary payments. This means Payjoin improves privacy for *all* Bitcoin users — because analysts can no longer assume CIOH holds for any transaction.

[Payjoin Dev Kit](https://opensats.org/projects/payjoin) and [Async Payjoin (BIP77)](https://opensats.org/projects/payjoin) are actively funded by OpenSats.

---

#### Session 09: BIP77/78 Theory — How Payjoin Defeats Chain Analysis

##### Tutor Preparation

**Study time needed:** 2-3 hours.

**What this session is about in plain language:** Remember CIOH from Session 1? "If two addresses are inputs in the same transaction, they belong to the same person." That assumption is how Chainalysis clusters wallets. Payjoin destroys it.

Here's how: normally, when Alice pays Bob, only Alice puts inputs into the transaction. Bob just receives an output. But in a Payjoin, *both* Alice and Bob put inputs in. The transaction looks like a normal payment on the blockchain — but the CIOH assumption is wrong. The inputs belong to TWO different people.

*Analogy: Imagine you're at a restaurant. Normally, one person puts money on the table (the payer). In a Payjoin, both people put money on the table, and the waiter gives change to both. An observer who sees the money on the table can't tell whose is whose — they might assume it's all from one person, but they'd be wrong.*

**Why this is so powerful:** Every Payjoin transaction makes CIOH unreliable not just for that transaction, but for ALL transactions — because if *some* transactions violate CIOH, analysts can never be sure *any* transaction follows it. This is what OpenSats means by "raises the baseline privacy of everyday users."

**BIP77 vs BIP78 (you need to explain the difference):**
- **BIP78 (Payjoin V1):** The receiver must be online. The sender creates a transaction, sends it to the receiver (over HTTPS), the receiver modifies it, sends it back, and the sender broadcasts. Problem: the receiver needs a web server running.
- **BIP77 (Async Payjoin, V2):** Serverless. Uses a "Payjoin Directory" as a relay. The sender posts an encrypted PSBT to the directory, the receiver picks it up whenever they're online, modifies it, and posts back. Neither party needs to be online at the same time.

**The 5 sender verification checks (important!):**
When the receiver modifies the transaction, the sender must verify it wasn't tampered with. There are 5 checks:
1. No new outputs added (prevents receiver from redirecting funds)
2. Original outputs aren't reduced (prevents receiver from skimming)
3. No inputs removed (prevents receiver from de-funding the transaction)
4. Fee doesn't increase unreasonably (prevents fee manipulation)
5. The transaction is still valid to sign (prevents malformed transactions)

---

**Learn:**
- CIOH in depth: why it's chain analysis's most powerful tool, how many wallets it clusters, and what breaks when it fails
- Payjoin V1 (BIP78): the original interactive protocol — how it works, its limitations
- Payjoin V2 (BIP77, "Async Payjoin"): the serverless, asynchronous protocol using the Payjoin Directory
- The 5 critical sender verification checks that prevent output substitution attacks
- Why Payjoin is more powerful than CoinJoin for systemic privacy
- Current adoption: [BTCPay Server](https://github.com/btcpayserver/btcpayserver), [Bull Bitcoin](https://www.bullbitcoin.com/)

**Build:**
- Analyze 10 testnet transactions — determine which are Payjoins (hint: it should be hard to tell)
- Walk through the full BIP77 async flow: sender creates original PSBT → posts to directory → receiver modifies PSBT → sender validates 5 checks → sender signs and broadcasts
- Implement all 5 sender verification checks in pseudocode

**Contribute this session:**
- Clone [payjoin/rust-payjoin](https://github.com/payjoin/rust-payjoin). Build it. Run the test suite. Read `src/send.rs` and `src/receive.rs`
- Browse [rust-payjoin open issues](https://github.com/payjoin/rust-payjoin/issues). Issues labeled `good first issue` are your targets
- Read the [BIP77 specification](https://github.com/bitcoin/bips/blob/master/bip-0077.mediawiki). If you find inconsistencies, file an issue

---

#### Session 10: Building with Payjoin Dev Kit (Rust)

##### Tutor Preparation

**Study time needed:** 2-3 hours. Build the Rust exercise yourself — you'll need Rust installed and working.

**What this session is about:** Participants implement a complete Payjoin flow using PDK (Payjoin Dev Kit). This is hands-on Rust coding. If you're not deeply comfortable in Rust, that's okay — focus on helping people with the *logic* (which you now understand from Session 9) and let participants who know Rust help each other with syntax.

**Your job this session:** Circulate. Help people understand the *flow* (sender creates PSBT → receiver modifies → sender validates → broadcast). The Rust specifics are secondary — the participants are developers, they can read docs. What they need from you is understanding of *what* the code is doing and *why*.

**If someone can't do Rust:** They can follow along in Python using the pseudocode from Session 9, or pair with a Rust developer.

---

**Learn:**
- [PDK (Payjoin Dev Kit)](https://github.com/payjoin/rust-payjoin) architecture: send module, receive module, PSBT handling, the Payjoin Directory
- PSBT construction and modification: how PDK creates, modifies, and validates PSBTs
- Integrating PDK into a wallet application: the minimum code needed to add Payjoin support
- Testing Payjoin flows on signet

**Build:**
- Complete Payjoin flow in Rust using PDK:
  1. Sender creates original PSBT
  2. Receiver modifies it (adds input, adjusts change)
  3. Sender validates all 5 checks
  4. Sender signs and broadcasts
- Analyze the on-chain result — can you tell it was a Payjoin?

**Contribute this session:**
- Your PDK integration exercise surfaced rough edges. File issues on [rust-payjoin](https://github.com/payjoin/rust-payjoin): unclear documentation, unhelpful error messages, missing examples, API friction
- Even better: fix the documentation yourself. Docs PRs are the fastest path to merged code
- If you wrote a clean integration example, submit it as a PR to the examples/ directory

---

#### Session 11: Payjoin in Production — Adoption Is the Privacy Multiplier

##### Tutor Preparation

**Study time needed:** 2 hours.

**What this session is about:** Payjoin only works at scale if wallets adopt it. This is the "deeper integration" session — the work OpenSats specifically calls for. Participants evaluate real wallets, test existing integrations, and write feasibility assessments for wallets that don't support Payjoin yet.

**Key insight for participants:** One well-researched GitHub issue titled "Payjoin (BIP77) Support — Feasibility Assessment" on a popular wallet's repo can be the seed that leads to adoption. Wallet developers are busy. If someone hands them a clear analysis of what it would take to add Payjoin, they're much more likely to do it.

**How to run this session:**
1. Demo BTCPay Server with Payjoin enabled (set this up before class on signet/testnet)
2. Have participants make Payjoin payments to each other through BTCPay
3. Then have each person pick a wallet that DOESN'T support Payjoin and research what it would take

---

**The problem:** Payjoin only achieves its full privacy benefit with widespread adoption. Every wallet that supports Payjoin makes the CIOH weaker for all users.

**Learn:**
- BTCPay Server's Payjoin implementation — code walkthrough
- UX considerations: how to make Payjoin invisible to users (it should "just work")
- The adoption curve: which wallets support Payjoin today, which are working on it, which should be next
- How to write a convincing "Payjoin support" feature request for a wallet that doesn't have it

**Build:**
- Set up BTCPay Server with Payjoin enabled. Make a Payjoin payment. Trace the code path
- Compare on-chain footprints: Payjoin transaction vs regular payment. Document every observable difference (there should be none)

**Contribute this session:**
- Pick a Bitcoin wallet that doesn't support Payjoin. Write a detailed GitHub issue: "Payjoin (BIP77) Support — Feasibility Assessment" including which library to use (PDK), estimated effort, and the privacy benefit. **This is how adoption starts.**
- Test BTCPay Server's Payjoin with different sender wallets. If something breaks, file a detailed issue
- Review an open Payjoin-related PR on BTCPay Server or rust-payjoin

---

#### Session 12: Contributing to Payjoin — Ship Your Code

##### Tutor Preparation

**Study time needed:** 1 hour prep + curate issues.

**Same format as Session 08.** Working session. Everyone submits a PR. Curate 10-15 approachable issues from rust-payjoin, BTCPay Server, and wallet repos beforehand. Match participants to issues. Walk the room. Celebrate submissions.

---

**Learn:**
- [rust-payjoin](https://github.com/payjoin/rust-payjoin) codebase deep dive: module architecture, testing strategy, CI pipeline
- How to get PRs merged: writing good commit messages, responding to review feedback, keeping PRs small

**Build & Contribute — submit a PR:**
- Target repos: [payjoin/rust-payjoin](https://github.com/payjoin/rust-payjoin), [btcpayserver/btcpayserver](https://github.com/btcpayserver/btcpayserver), or any wallet
- Bug fix, test case, documentation improvement, or feature — all count
- **Peer review:** every participant reviews at least one other participant's PR before next session

> **Phase 3 checkpoint:** Every participant has PRs in both the Silent Payments and Payjoin ecosystems. They can articulate how CIOH works and how Payjoin defeats it.

---

### Phase 4: Network & Protocol Privacy — Your Node Leaks Too
*Months 7-8 · Sessions 13-16*

Base-layer privacy isn't just about transactions. Your Bitcoin node's network connections, peer selection, transaction relay behavior, and light client queries all leak information.

---

#### Session 13: P2P Network Privacy — Transaction Relay, ASmap & Eclipse Attacks

##### Tutor Preparation

**Study time needed:** 2-3 hours.

**What this session is about in plain language:** Everything so far has been about what's visible ON the blockchain. This session is about what's visible on the NETWORK — the internet connections your Bitcoin node makes.

When your node broadcasts a transaction, the first node that receives it can link your IP address to that transaction. Your ISP can see you're running a Bitcoin node. A sophisticated attacker can fill your node's connections with their own nodes ("eclipse attack"), isolating you from the real network.

**Three key concepts to explain:**

1. **Transaction relay and first-spy attacks:** Your node sends a transaction to its peers. The first peer to receive it knows it probably originated from you. *Analogy: if you whisper a secret to 8 people at the same time, anyone listening knows you're the source because you told them first.* **Dandelion++** fixes this by first sending the transaction along a random single path (the "stem") before broadcasting it widely (the "fluff"). Now the first listener can't be sure where it came from.

2. **Eclipse attacks:** Your node connects to ~8 outbound peers. If an attacker controls all 8, they control what you see — they can hide transactions, feed you a fake chain, or deanonymize you. **Mitigation:** Bitcoin Core uses clever bucketing in its address manager (addrman) and "anchor connections" (peers you always reconnect to).

3. **ASmap (Autonomous System mapping):** An AS is a chunk of the internet controlled by one organization (like an ISP or cloud provider). If all your peers are in the same AS, that organization sees all your traffic. [ASmap](https://github.com/sipa/asmap) maps IP addresses to their AS, so Bitcoin Core can ensure your peers are spread across different network boundaries. **This is specifically funded by OpenSats and actively needs contributors.**

**Common questions:**
- *"Can't I just use Tor?"* → Yes, and Session 13 covers Tor configuration. But Tor has its own tradeoffs: slower connections, potential Sybil attacks on Tor exit nodes, and if you ONLY use Tor, you're dependent on the Tor network.
- *"Does this matter if I'm not broadcasting transactions from my own node?"* → Less critical, but you're still receiving blocks and transactions. An eclipse attack could feed you false information.

---

**The problem:** When your node broadcasts a transaction, the first node that sees it can associate your IP address with the transaction. Eclipse attacks isolate your node. And because nodes don't consider network topology, a single ISP can see a disproportionate share of your traffic.

**Learn:**
- How transaction relay reveals your IP: first-spy attacks, timing analysis, relay topology inference
- Dandelion++ (stem-and-fluff): plausible deniability for transaction origin
- [ASmap](https://github.com/sipa/asmap): mapping IP addresses to autonomous systems for peer diversity — **specifically funded by OpenSats**
- Tor and I2P integration in Bitcoin Core: configuration, tradeoffs, hybrid mode
- Eclipse attack mitigations: anchors, addrman bucketing, peer eviction logic
- [Naiyoma's P2P privacy and node-fingerprinting research](https://opensats.org/blog/five-grants-to-strengthen-bitcoin-development#naiyoma)

**Build:**
- Configure Bitcoin Core in three modes: clearnet-only, Tor-only, and hybrid. Analyze peer connections in each
- Map your node's current peers to autonomous systems. Calculate AS diversity and eclipse attack surface
- Simulate adversary IP linking probability for each configuration

**Contribute this session:**
- Bitcoin Core's Tor and I2P documentation (`doc/tor.md`, `doc/i2p.md`) can always be improved. Submit a PR for anything outdated
- [ASmap](https://github.com/sipa/asmap) needs contributors — better AS data sources, testing improvements, documentation
- Search Bitcoin Core issues for P2P or privacy labels. Comment with test results or analysis

---

#### Session 14: Compact Block Filters (BIP157/158) — Privacy-Preserving Light Clients

##### Tutor Preparation

**Study time needed:** 2 hours.

**What this session is about:** We covered CBFs briefly in Session 7 (for Silent Payments scanning). This session goes deeper: how CBFs work internally, why the old approach (BIP37 Bloom filters) was a privacy disaster, and how Kyoto and Floresta implement light clients that don't leak your addresses.

**BIP37 vs BIP157 (explain the key difference):**
- **BIP37 (the old way):** The client creates a "Bloom filter" — a fuzzy set that says "I'm interested in these things." It sends this to a server. The problem: the server can analyze the filter and figure out which addresses you're interested in. It was supposed to be private, but [researchers showed it leaks almost everything](https://eprint.iacr.org/2014/763.pdf).
- **BIP157 (the new way):** The *server* creates a filter for each block. The client downloads the filter and checks locally. The server never learns what the client is looking for. The client's privacy is preserved by design.

*Analogy: BIP37 is like telling a librarian "I'm looking for books about X, Y, and Z" — they know your interests. BIP157 is like the librarian posting a catalog for each shelf, and you checking the catalog yourself without ever talking to the librarian.*

---

**The problem:** [BIP37 Bloom filters leaked which addresses the client was interested in](https://eprint.iacr.org/2014/763.pdf). BIP157/158 compact block filters fix this by letting the client check locally whether a block might contain relevant transactions.

**Learn:**
- Why BIP37 was broken: false positive rates, filter update attacks, server-side inference
- Golomb-Rice Coded Sets (GCS): the compression scheme behind compact block filters
- BIP157 client-server protocol: how clients request filters, verify them, and decide which blocks to download
- How [Kyoto](https://github.com/rustaceanrob/kyoto) implements BIP157/158 in Rust
- How [Floresta](https://github.com/vinteumorg/Floresta) uses utreexo for a different approach to light client privacy

**Build:**
- Implement Golomb-Rice encoding and decoding from scratch in Python
- Build a GCS filter from a set of scripts. Query it for matches. Calculate the actual false positive rate
- Compare bandwidth: for a wallet with 100 addresses, how many false-positive blocks would BIP157/158 cause the client to download?

**Contribute this session:**
- [Kyoto](https://github.com/rustaceanrob/kyoto) is early-stage and needs contributors. Clone, build, and run it. File well-described bugs
- [Floresta](https://github.com/vinteumorg/Floresta) has issues related to block filter handling. Browse and comment
- Test both on signet. Document setup instructions if they're missing — submit as a docs PR

---

#### Session 15: Light Client Privacy — Floresta, Kyoto & the Privacy Spectrum

##### Tutor Preparation

**Study time needed:** 2 hours.

**What this session is about:** Comparing all the ways a user can interact with the Bitcoin network, from worst privacy (SPV) to best (full node). The key message: there's a *spectrum*, and projects like Kyoto and Floresta are pushing the light client end of the spectrum toward much better privacy.

**The spectrum (draw this on a whiteboard):**
1. **SPV (worst):** Asks peers for transactions matching specific addresses. Everyone knows what you're looking for.
2. **Electrum-style:** Asks a specific server for address history. The server knows everything about you.
3. **BIP157/158 / Kyoto (good):** Downloads block filters, checks locally. Server doesn't know what you're looking for.
4. **Floresta / Utreexo (good, different tradeoffs):** Validates transactions using compact proofs. Very little storage needed.
5. **Full node (best):** Downloads and validates everything. Maximum privacy, maximum resource usage.

**Key question to pose to participants:** "If you're building a mobile wallet, which approach gives the best privacy for the resource constraints of a phone?" This is the design question Kyoto and Floresta are trying to answer.

---

**Learn:**
- The light client privacy spectrum: SPV (worst) → Electrum (bad) → BIP157/158 (good) → full node (best)
- [Floresta](https://github.com/vinteumorg/Floresta): utreexo-based validation, privacy properties
- [Kyoto](https://github.com/rustaceanrob/kyoto): BIP157/158 implementation, architecture
- How Silent Payments scanning works differently in each light client model
- Bandwidth, storage, and privacy comparison across 5 approaches

**Build:**
- Set up Floresta on signet. Connect a wallet. Monitor what information flows between client and network
- Build a structured privacy comparison matrix for all 5 light client approaches

**Contribute this session:**
- [Floresta is actively looking for contributors](https://github.com/vinteumorg/Floresta/issues). Check "good first issue" labels
- Your privacy comparison matrix is publishable content. Submit as a PR to Floresta or Kyoto docs
- Test both against edge cases. File issues with detailed reproduction steps

---

#### Session 16: Taproot Privacy — Making Complex Transactions Invisible

##### Tutor Preparation

**Study time needed:** 2 hours.

**What this session is about in plain language:** Before Taproot, you could tell a lot about a transaction just by looking at its script type. Multisig transactions (multiple people authorizing a spend) looked different from regular transactions. Timelocked transactions (funds that can't move until a certain date) looked different too. This meant complex spending conditions stood out on-chain.

Taproot fixes this. With Taproot, a 2-of-3 multisig can look *identical* to a simple single-signature transaction on the blockchain. The complex script is hidden — only revealed if something goes wrong (like one signer being unavailable). In the happy path, it's indistinguishable.

**But here's the catch:** Taproot only provides privacy if enough people use it. If only 5% of transactions are Taproot, those 5% stand out as "probably doing something complex." Privacy needs a crowd. This is why wallet defaults matter — if wallets default to Taproot addresses, adoption rises, and everyone benefits.

**Key concepts:**
- **Key path spending:** The "happy path" — looks like a regular single-sig transaction. Used when all parties agree.
- **Script path spending:** The "backup path" — reveals which branch of the script was used. Used when the key path can't be used.
- **MuSig2:** A protocol for multiple parties to cooperatively produce a single signature that looks like a regular signature on-chain. 2-of-2 multisig that's invisible.
- **FROST:** Like MuSig2 but for threshold signatures (e.g., 2-of-3). Also looks like single-sig on-chain.

---

**Learn:**
- How Taproot makes multisig indistinguishable from single-sig (key path spending)
- MAST (Merklized Alternative Script Trees): complex spending conditions that only reveal the branch used
- MuSig2 for multi-party Taproot key aggregation
- FROST: threshold signatures that look like single-sig on-chain
- CISA (Cross-Input Signature Aggregation): a future proposal making CoinJoin cheaper
- Why Taproot adoption matters for systemic privacy

**Build:**
- Create three Taproot transactions on signet: single-sig, 2-of-2 MuSig, and script path with 2 branches
- Compare on-chain footprints: the first two should be indistinguishable
- Analyze current Taproot adoption metrics and trends

**Contribute this session:**
- Research which wallets default to Taproot addresses and which don't. File issues on wallets that don't default to P2TR
- Review a Taproot-related PR on Bitcoin Core, rust-bitcoin, or BDK

> **Phase 4 checkpoint:** Participants have contributed to 3-4 different repos. They understand P2P privacy, ASmap, compact block filters, light client tradeoffs, and Taproot's privacy benefits.

---

### Phase 5: Advanced Privacy Techniques — CoinJoin, CoinSwap, eCash & Lightning
*Months 9-10 · Sessions 17-20*

This phase covers advanced privacy techniques that complement base-layer improvements: CoinJoin ([JoinMarket NG](https://opensats.org/blog/seventeenth-wave-of-bitcoin-grants#joinmarket-ng)), [Coinswap](https://opensats.org/blog/developing-advancements-in-onchain-privacy#coinswap), eCash ([Fedimint](https://github.com/fedimint/fedimint), [Cashu](https://github.com/cashubtc/nutshell)), and Lightning privacy (BOLT12). While OpenSats' Spring 2026 focus is Layer 1, these techniques interact with base-layer privacy in critical ways — and several are actively funded.

---

#### Session 17: CoinJoin & JoinMarket NG — Equal-Output Mixing

##### Tutor Preparation

**Study time needed:** 2-3 hours.

**What this session is about in plain language:** CoinJoin is the oldest privacy technique in Bitcoin (Greg Maxwell proposed it in 2013). The idea: multiple users combine their transactions into one big transaction where everyone's outputs are the same amount. If 5 people each put in different amounts and all get out exactly 0.1 BTC, an observer can't tell which input corresponds to which output.

*Analogy: 5 people each put a $100 bill into a hat. The hat shakes. 5 people each take out a $100 bill. An observer knows $500 went in and $500 came out, but they can't tell whose $100 is whose.*

**The problem with CoinJoin:** The change. If Alice puts in 0.15 BTC and takes out 0.1 BTC (the equal output) plus 0.05 BTC (change), that change amount might be unique enough to link back to Alice. This is called "toxic change."

**JoinMarket NG (explain why it matters):**
Traditional CoinJoin services used a central coordinator (like Wasabi Wallet's WabiSabi coordinator or the now-shut-down Samourai Whirlpool). JoinMarket takes a different approach: it's an *orderbook* — "makers" offer liquidity (their coins for mixing) and earn fees, "takers" pay fees to mix their coins. No central coordinator required. [JoinMarket NG](https://opensats.org/blog/seventeenth-wave-of-bitcoin-grants#joinmarket-ng) is the next generation of this system, actively funded by OpenSats.

**CoinJoin vs Payjoin (key distinction for participants):**
- CoinJoin: *visible* on-chain as a mixing transaction (equal outputs are a giveaway), but provides ambiguity within the mix
- Payjoin: *invisible* on-chain (looks like a normal payment), but only involves 2 parties

---

**Learn:**
- CoinJoin mechanics: multiple users combine inputs into a single transaction with equal-value outputs
- Toxic change: why CoinJoin doesn't work if change outputs can be linked back to inputs
- WabiSabi protocol: the credential system used by Wasabi Wallet for flexible CoinJoin
- [JoinMarket NG](https://opensats.org/blog/seventeenth-wave-of-bitcoin-grants#joinmarket-ng): the next generation orderbook-based CoinJoin — **funded by OpenSats**
- CoinJoin weaknesses: Sybil attacks on coordinators, timing analysis, amount analysis
- CISA's potential impact on CoinJoin economics

**Build:**
- Analyze 20 real mainnet transactions. Identify CoinJoins. Calculate anonymity sets, identify toxic change
- Simulate a 5-user CoinJoin construction. Analyze what a chain analyst can determine
- Compare CoinJoin vs Payjoin: privacy properties, on-chain footprint, detectability, cost

**Contribute this session:**
- Publish your CoinJoin analyzer under CC0 as a standalone repo
- Research [Teleport Transactions](https://github.com/nickhntv/teleport-transactions) (next session). Clone, build, file issues
- Write a structured comparison of CoinJoin implementations: JoinMarket NG, Wasabi WabiSabi, legacy Whirlpool

---

#### Session 18: CoinSwap & Teleport — Breaking the Transaction Graph Entirely

##### Tutor Preparation

**Study time needed:** 2 hours.

**What this session is about in plain language:** CoinJoin mixes coins *within* a single transaction — but that transaction is still identifiable on-chain as a CoinJoin. CoinSwap goes further: two users make *separate, normal-looking transactions* that swap their coins. There is NO visible connection between the two transactions.

*Analogy: Alice has a red ball and Bob has a blue ball. In a CoinJoin, they put both balls in a box, shake it, and each take one out — an observer sees the box shaking. In a CoinSwap, Alice hands her red ball to a trusted dropbox, and Bob does the same with his blue ball. Later, Alice picks up the blue ball and Bob picks up the red one. An observer sees two separate, ordinary-looking handoffs.*

The magic is that these swaps are **trustless** — neither party can steal the other's funds, thanks to Hash Time-Locked Contracts (HTLCs). If one party doesn't follow through, the funds are returned automatically.

**[Teleport Transactions](https://github.com/nickhntv/teleport-transactions)** is the active CoinSwap implementation. It's early-stage and specifically mentioned by OpenSats as a project they want to see improved. **This is high-impact contribution territory.**

---

**The problem:** CoinSwap creates two ordinary-looking payments that swap ownership. No on-chain evidence of a swap.

**Learn:**
- How CoinSwap breaks the transaction graph
- Hash time-locked contracts (HTLCs): trustless atomic swaps
- Multi-hop CoinSwap: adding intermediate hops for plausible deniability
- [Teleport Transactions](https://github.com/nickhntv/teleport-transactions) — **OpenSats specifically wants work here**
- CoinSwap vs CoinJoin: privacy comparison

**Build:**
- Walk through a 2-party CoinSwap on paper. Diagram every on-chain transaction. Analyze what an observer sees
- Walk through a 3-hop CoinSwap. How does each hop add deniability?
- Calculate costs: CoinJoin vs CoinSwap — with and without CISA

**Contribute this session:**
- [Teleport Transactions](https://github.com/nickhntv/teleport-transactions) is early-stage and needs contributors. This is **high-impact**
- File issues for bugs, documentation gaps, or UX problems
- Start working on a Teleport issue — even a documentation PR matters

---

#### Session 19: eCash Privacy — Fedimint & Cashu

##### Tutor Preparation

**Study time needed:** 2 hours.

**What this session is about in plain language:** Everything we've covered so far improves privacy on the blockchain itself. eCash takes a completely different approach: move transactions OFF the blockchain into a system where the operator (the "mint") literally cannot see who is transacting.

The magic is **blind signatures**. When you deposit bitcoin into a Cashu mint, the mint gives you digital "tokens" — but the minting process uses a cryptographic trick where the mint signs the tokens *without seeing what they are*. Later, when you redeem a token, the mint can verify it's genuine (its signature is valid) but can't link it to the original deposit. Perfect transaction privacy from the operator.

*Analogy: You put money in an envelope with carbon paper inside. The bank stamps the outside of the envelope (signing it) without opening it. Later, you open the envelope — the stamp has transferred through the carbon paper onto your check inside. The bank recognizes its stamp but never saw the check.*

**Trust tradeoff:** eCash requires trusting the mint not to steal funds or inflate the supply. This is the fundamental tradeoff vs on-chain transactions. Cashu uses single-operator mints; Fedimint uses federated custody (multiple operators, threshold signatures) to reduce trust.

**Why it's in this curriculum:** OpenSats notes that "grantees building Cashu, Nutshell, Minibits, Fedimint, and related projects have turned Chaumian ecash from research into production infrastructure." While the Spring 2026 focus is Layer 1, understanding how eCash complements on-chain privacy is essential.

---

**Learn:**
- Chaumian blind signatures: how the mint signs tokens without knowing which tokens it signed
- [Cashu](https://github.com/cashubtc/nutshell): mint-receive-send-melt lifecycle, proof structure
- [Fedimint](https://github.com/fedimint/fedimint): federated custody, threshold Chaumian minting, Lightning gateway
- How eCash complements on-chain privacy: eCash for small payments, on-chain for settlement
- Trust assumptions: eCash vs on-chain privacy tools

**Build:**
- Set up a Cashu mint on signet. Mint tokens, send them, redeem them. Walk through the blind signature math
- Analyze what the mint learns at each stage: where does privacy hold? Where does it break?

**Contribute this session:**
- [cashubtc/nutshell](https://github.com/cashubtc/nutshell) is Python — accessible to everyone. Browse issues
- [fedimint/fedimint](https://github.com/fedimint/fedimint) has "good first issue" labels. Very welcoming community
- Write a step-by-step setup guide and submit as a PR to the docs

---

#### Session 20: Lightning Privacy — BOLT12, Blinded Paths & Channel Privacy

##### Tutor Preparation

**Study time needed:** 2 hours.

**What this session is about in plain language:** Lightning Network routes payments through multiple nodes using onion routing (each node only sees the previous and next hop, not the full path). This gives good *payment routing* privacy. But Lightning has its own privacy problems: channel balances can be probed, the channel graph is public, and BOLT11 invoices reveal the receiver's node identity.

**BOLT12 (the big improvement):** BOLT12 "offers" are reusable payment requests that DON'T reveal the receiver's node. They use "blinded paths" — the last few hops of the route are encrypted, so the sender doesn't know who they're ultimately paying. This is a huge privacy upgrade for receivers.

**Why it's here:** OpenSats mentions that "grantees have advanced BOLT12 offers and receiver-side privacy for Lightning payments." Understanding Lightning privacy helps participants see the full picture: Layer 1 privacy (this track's focus) interacts with Layer 2 privacy in important ways — e.g., when you open a Lightning channel, that's an on-chain transaction that needs base-layer privacy.

---

**Learn:**
- Lightning's privacy model: onion-routed payments (good), but channel balance probing (bad)
- Blinded paths (BOLT12): receiver privacy through encrypted last-hop routes
- BOLT12 offers: reusable payment requests without node identity exposure
- Private vs public channels: tradeoffs
- Trampoline routing: privacy through delegation

**Build:**
- Set up two LN nodes on signet. Open a channel. Probe your own channel balance
- Compare BOLT11 invoices vs BOLT12 offers: what information does each reveal?
- Design a maximum-privacy Lightning configuration

**Contribute this session:**
- [lightningdevkit/rust-lightning (LDK)](https://github.com/lightningdevkit/rust-lightning) has "good first issue" labels. LDK powers many wallets
- Publish your Lightning privacy analysis
- File privacy issues found during testing

> **Phase 5 checkpoint:** Participants are contributing across 5+ different repos. They understand CoinJoin, CoinSwap, eCash, and Lightning privacy — and how each complements base-layer improvements.

---

### Phase 6: Building & Shipping — Substantial Work That Gets Merged
*Months 11-12 · Sessions 21-24*

Everything learned, applied. Every graduate ships real code.

---

#### Session 21: Privacy-Preserving Wallet Development with BDK

##### Tutor Preparation

**Study time needed:** 2-3 hours.

**What this session is about:** [BDK (Bitcoin Dev Kit)](https://opensats.org/projects/bdk) is the foundation for many Bitcoin wallets. Privacy improvements in BDK cascade to every wallet built on it. This session is about building wallets that are private by default — the user shouldn't have to think about fingerprinting, coin selection, or address reuse.

**This is the "deeper integration" work OpenSats wants.** When participants build a privacy-by-default BDK wallet with Payjoin support and privacy-optimized coin selection, they're demonstrating exactly the kind of integration work the ecosystem needs.

**Your role:** Help participants scaffold the wallet. If you're not a Rust developer, focus on the *design decisions*: "What coin selection strategy should the wallet default to? Why? What should happen when a user tries to reuse an address? Should the wallet warn them or prevent it?"

---

**The problem:** Privacy improvements in BDK cascade to every wallet built on it. This session focuses on building privacy-by-default wallets — the "deeper integration" work OpenSats wants to see.

**Learn:**
- BDK architecture: descriptor wallets, coin selection API, PSBT building, chain data sources
- Privacy-by-default wallet design: what a wallet should do automatically
- Privacy-optimized coin selection in BDK
- How to add Silent Payments or Payjoin support to a BDK wallet

**Build:**
- Scaffold a BDK wallet with: privacy-optimized coin selection, change output safety, address reuse detection, anti-fee-sniping locktime
- Add basic Payjoin send support using PDK
- Run your wallet through a privacy scorer

**Contribute this session:**
- Submit a PR to [bitcoindevkit/bdk](https://github.com/bitcoindevkit/bdk): missing privacy configuration options, documentation improvements, coin selection edge cases
- File issues for privacy-related improvements

---

#### Session 22: Privacy Testing, Scoring & Mempool Analysis

##### Tutor Preparation

**Study time needed:** 2 hours.

**What this session is about:** Participants build a tool that automatically scores any transaction's privacy quality. This is useful for wallet developers (test your wallet's output in CI) and for the community (audit real transactions). It pulls together everything from the entire curriculum.

**This is also great publishable work.** A well-built privacy scoring tool submitted to the Bitcoin Dev Project or published as a standalone repo is a visible, citable contribution.

---

**Learn:**
- Systematic transaction privacy evaluation: what to check and how to score it
- Mempool analysis: how timing, fee rates, and propagation patterns reveal information
- Building automated privacy testing for wallet software

**Build:**
- Build a comprehensive transaction privacy scorer in Python. Check for: address reuse, script type mixing, round amounts, detectable change, fee rate fingerprint, locktime pattern, sequence pattern, consolidation without payment, output ordering predictability
- Score 20 real mainnet transactions. Identify the worst offenders

**Contribute this session:**
- Publish your privacy scoring tool under CC0 as a standalone repo
- Run your scorer against transactions from popular wallets. File issues with your data
- Submit your methodology to [Bitcoin Optech](https://bitcoinops.org/) or the [Bitcoin Wiki](https://en.bitcoin.it/wiki/Privacy)

---

#### Session 23: Contribution Sprint — The Big Push

##### Tutor Preparation

**Before the session:** Prepare a curated list of 15-20 open issues across all target repos. Categorize by difficulty and language. Print it out or put it on a shared doc.

**This is a 3-hour working session. Code ships today.**

| Time | Activity |
|---|---|
| 00:00 - 00:30 | **Issue selection:** each participant picks a target from the curated list |
| 00:30 - 02:00 | **Code:** write your fix, test it, prepare the PR |
| 02:00 - 02:30 | **Peer review:** every participant reviews one other PR |
| 02:30 - 03:00 | **Submit:** push, open the PR, celebrate |

**Curated issue list (updated monthly by facilitator):**

| Repo | Language | What to Look For |
|---|---|---|
| [bitcoin/bitcoin](https://github.com/bitcoin/bitcoin) | C++ | Silent Payments, compact block filters, P2P privacy, ASmap, coin selection |
| [cygnet3/rust-silentpayments](https://github.com/cygnet3/rust-silentpayments) | Rust | Test coverage, edge cases, documentation |
| [payjoin/rust-payjoin](https://github.com/payjoin/rust-payjoin) | Rust | Good first issues, integration examples, docs |
| [vinteumorg/Floresta](https://github.com/vinteumorg/Floresta) | Rust | Good first issues, testing, documentation |
| [rustaceanrob/kyoto](https://github.com/rustaceanrob/kyoto) | Rust | Early-stage — lots of opportunities |
| [nickhntv/teleport-transactions](https://github.com/nickhntv/teleport-transactions) | Rust | CoinSwap implementation, testing, docs |
| [fedimint/fedimint](https://github.com/fedimint/fedimint) | Rust | Good first issues, module development |
| [cashubtc/nutshell](https://github.com/cashubtc/nutshell) | Python | Testing, documentation, mint features |
| [bitcoindevkit/bdk](https://github.com/bitcoindevkit/bdk) | Rust | Coin selection, privacy features |
| [lightningdevkit/rust-lightning](https://github.com/lightningdevkit/rust-lightning) | Rust | Good first issues, privacy features |
| [rust-bitcoin/rust-bitcoin](https://github.com/rust-bitcoin/rust-bitcoin) | Rust | Transaction construction, encoding |
| [sipa/asmap](https://github.com/sipa/asmap) | Python/C++ | AS mapping, peer diversity tooling |

---

#### Session 24: Capstone — Present Your Contributions

##### Tutor Preparation

**Before the session:** Confirm presentations with each participant. Help anyone who needs it to prepare their slides or talking points. Invite the broader Code Orange community.

**How to run presentations:** Keep to time strictly (10 min each). Use a timer visible to the presenter. Celebrate every contribution — a documentation PR is as worthy as a feature PR.

Each participant presents (10 minutes):

1. **What you contributed (4 min)** — Walk through your PRs. Show the code. Link to each one
2. **What impact it has (2 min)** — Who benefits? How does this make Bitcoin more private?
3. **What you learned (2 min)** — What was harder than expected? What changed how you think about privacy?
4. **What's next (2 min)** — If you had 6 more months of funded time, what would you build?

Open to the full Code Orange community — Bitcoin Dojo, rawBit, Decoding Bitcoin cohorts all attend.

**Graduation requirements:**
- Submitted 3+ PRs to Bitcoin privacy projects
- Presented at capstone

Graduates meeting these requirements are eligible for the **Code Orange Developer Fellowship** ($500/month, 6 months) to continue contributing to Bitcoin privacy open-source full-time.

---

## Expected Output

### Per participant (12 months):

| Metric | Target |
|---|---|
| PRs submitted | 5-8 |
| PRs merged | 3-5 |
| Distinct repos contributed to | 3+ |
| Code reviews posted | 10+ |
| Issues filed | 5+ |

### Per cohort (15 participants, 12 months):

| Metric | Target |
|---|---|
| PRs submitted | 75-120 |
| PRs merged | 45-75 |
| New privacy developers produced | 15 |
| Repos contributed to | 12+ |

---

## Session Format

Every session follows the same structure. The last 30 minutes are always about contributing.

| Time | Activity |
|---|---|
| 00:00 - 00:15 | **Review:** Show contributions since last session. What got merged? What feedback? What's blocking? |
| 00:15 - 00:45 | **Concept:** Theory and protocol walkthrough |
| 00:45 - 01:45 | **Build:** Hands-on coding exercise |
| 01:45 - 02:15 | **Contribute:** Open laptops. Find issues. File PRs. Review code. Facilitator matches participants to issues in real time. |
| 02:15 - 02:30 | **Plan:** Assigned reading + specific contribution goal for next 2 weeks |

The "Review" at the start creates accountability. When you know you'll be asked "what did you contribute since last time?" — you contribute.

---

## Contribution Tracker

Every participant maintains a public contribution log. This is what grant reviewers see.

| Session | Minimum Contribution | Target Repos |
|---|---|---|
| 01 | Star 7 repos. Clone bitcoin/bitcoin. Read coinselection.cpp | bitcoin/bitcoin, BDK, rust-silentpayments, rust-payjoin, Floresta, Kyoto, rust-bitcoin |
| 02 | Test a wallet's fingerprint. Draft issue for Session 4 | Any Bitcoin wallet repo, Bitcoin Optech |
| 03 | Comment on a BDK coin selection issue with analysis | bitcoindevkit/bdk, bitcoin/bitcoin |
| 04 | File your first issue or docs PR (wallet fingerprint or wiki) | Any wallet repo, Bitcoin Wiki, rust-bitcoin |
| 05 | Read BIP352. Comment on a rust-silentpayments issue | bitcoin/bips, rust-silentpayments |
| 06 | Add a test case or file issue on SP test vectors | bitcoin/bips, rust-silentpayments |
| 07 | Review a PR on bitcoin/bitcoin or Kyoto (CBF-related) | bitcoin/bitcoin, kyoto |
| 08 | **Submit your first PR** to an SP or CBF project | rust-silentpayments, kyoto, bitcoin/bitcoin |
| 09 | Clone rust-payjoin. Comment on an open issue | payjoin/rust-payjoin |
| 10 | File issues on PDK documentation or API rough edges | payjoin/rust-payjoin |
| 11 | File Payjoin feasibility issue on a wallet that lacks support | Any wallet repo, BTCPay |
| 12 | **Submit a PR** to Payjoin ecosystem | rust-payjoin, BTCPay |
| 13 | Improve Bitcoin Core P2P documentation or test ASmap | bitcoin/bitcoin, sipa/asmap |
| 14 | Test and file issues on Kyoto or Floresta | kyoto, Floresta |
| 15 | **Submit a PR** to Floresta or Kyoto | Floresta, kyoto |
| 16 | File Taproot adoption issues on wallets not defaulting to P2TR | Any wallet repo |
| 17 | Publish CoinJoin analysis tool. Research Teleport issues | teleport-transactions |
| 18 | **Submit a PR** to Teleport Transactions | teleport-transactions |
| 19 | Submit docs or test PR to Cashu or Fedimint | nutshell, fedimint |
| 20 | Submit a PR to LDK (privacy-related) | rust-lightning |
| 21 | **Submit a PR** to BDK (privacy feature or coin selection) | bdk |
| 22 | Publish privacy scoring tool. File issues on wallets tested | Any wallet repo |
| 23 | **Contribution sprint: submit a PR** | Any privacy-related repo |
| 24 | Present all contributions. Apply for fellowship if eligible | — |

---

## Exercises & Code

```
phase-1-foundations/
  session-01/  chain_analysis_lab.py      — Trace transactions, apply heuristics, privacy scoring
  session-02/  tx_anatomy_lab.py          — Decode raw transactions, identify wallet fingerprints
  session-03/  coin_selection_simulator.py — 4 algorithms, privacy scoring, BnB optimization
  session-04/  wallet_fingerprint_lab.py   — Identify wallets from raw transactions

phase-2-silent-payments/
  session-05/  sp_ecdh_derivation.py      — ECDH shared secret math from scratch
  session-06/  silent_payments_sender.py   — Full SP sender with test vector validation
  session-07/  sp_scanner_cbf.py          — SP scanner with compact block filter optimization

phase-3-payjoin/
  session-09/  payjoin_analysis.py        — Identify Payjoins from raw transactions
  session-10/  pdk_integration/           — Rust project using Payjoin Dev Kit
  session-11/  btcpay_payjoin_lab.md      — BTCPay Server Payjoin walkthrough

phase-4-network-privacy/
  session-13/  p2p_privacy_lab.py         — Peer analysis, AS mapping, relay timing
  session-14/  compact_block_filters.py   — Golomb-Rice coding from scratch, GCS construction
  session-16/  taproot_privacy_lab.py     — Key path vs script path analysis, CISA estimation

phase-5-advanced/
  session-17/  coinjoin_analysis.py       — CoinJoin detection, anonymity set calculation
  session-18/  coinswap_walkthrough.md    — CoinSwap flow analysis
  session-19/  cashu_mint_exercise.md     — Set up a Cashu mint on signet

phase-6-contributing/
  session-21/  bdk_privacy_wallet/        — Privacy-by-default BDK wallet scaffold
  session-22/  privacy_scorer.py          — Comprehensive transaction privacy scoring tool
```

---

## Resources

- **[Reading List](reading-list.md)** — 70+ resources organized by phase
- **[Glossary](glossary.md)** — 60+ terms covering all 6 phases
- **[Facilitator Guide](facilitator-guide.md)** — Session-by-session facilitation notes
- **[Capstone Projects](capstone-projects.md)** — 4 project tracks with rubrics
- **[Contributing](CONTRIBUTING.md)** — How to contribute to this curriculum

---

## For Grant Reviewers

**This is not a lecture series. This is a contribution pipeline specifically aligned with the base-layer privacy work that OpenSats, HRF, and Brink fund.**

OpenSats' [Spring 2026 Call for Applications](https://opensats.org/blog/call-for-applications-spring-2026) states: "We would especially welcome proposals that extend and improve Layer 1 work... as well as new projects taking fresh approaches to on-chain privacy. That includes deeper integration of existing techniques into widely used wallets, research and tooling that strengthen the surrounding ecosystem."

This curriculum directly addresses every priority:

| OpenSats Priority | Where We Address It | What Participants Build |
|---|---|---|
| Silent Payments (BIP352) | Phase 2 (Sessions 5-8) | SP sender/scanner from scratch, PRs to rust-silentpayments |
| Payjoin / collaborative transactions | Phase 3 (Sessions 9-12) | Full Payjoin flow with PDK, wallet integration assessments |
| Wallet behavior and transaction construction | Phases 1 + 6 (Sessions 2-4, 21-22) | Wallet fingerprint research, privacy-by-default BDK wallets, privacy scoring tools |
| Compact block filters (BIP157/158) | Sessions 7, 14 | CBF implementation, contributions to Kyoto |
| Floresta & light client privacy | Sessions 14-15 | Testing, issues, PRs to Floresta and Kyoto |
| ASmap & P2P privacy | Session 13 | AS mapping analysis, Bitcoin Core P2P docs, ASmap contributions |
| Coinswap | Session 18 | CoinSwap flow analysis, PRs to Teleport Transactions |
| JoinMarket NG / CoinJoin | Session 17 | CoinJoin analysis tooling, anonymity set calculation |
| rust-bitcoin and BDK (foundational libraries) | Throughout, especially Sessions 3-4, 21 | Coin selection improvements, transaction construction, privacy features |
| Deeper integration into widely used wallets | Sessions 4, 11, 16, 21 | Wallet fingerprint issues, Payjoin feasibility assessments, Taproot adoption issues |

From session 1, participants are reading real Bitcoin source code and engaging with real repos. By session 4, they've filed their first issue. By session 8, they've submitted their first PR. By session 24, they have 5-8 PRs across 3+ repos.

**Expected output for one cohort (15 participants, 12 months): 75-120 PRs submitted to Bitcoin privacy repos, 45-75 merged.**

Our track record proves this works. Code Orange has already produced **45+ merged PRs** across Bitcoin Core, rust-bitcoin, BDK, rust-payjoin, peer-observer, LDK, hex-conservative, kernel-node, and more. Our graduates — [Chaitika](https://github.com/chaitika) (Silent Payments), [Arowolo](https://github.com/Arowolokehinde) (Payjoin), [Peter](https://github.com/pzafonte) (Bitcoin Core), [Razor](https://github.com/RazorBest) (peer-observer), [Vaan](https://github.com/va-an) (BDK/rust-bitcoin) — are already contributing to the exact projects this curriculum targets.

**That's what your grant buys: more developers building the base-layer privacy tools that Bitcoin needs.**

---

*Code Orange Dev School · Bitcoin House Bali, Indonesia · [codeorange.dev](https://codeorange.dev) · CC0 1.0 Universal*
