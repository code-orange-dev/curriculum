# Bitcoin Privacy Developer Track

**Learn Bitcoin privacy. Build privacy tools. Contribute to open source. 24 sessions over 12 months.**

---

## Why This Track Exists

People accepting bitcoin for their work, running a small business, donating to causes, or saving for the future reasonably expect the same kind of day-to-day financial privacy they would get from traditional banking tools. As Greg Maxwell put it back in 2013:

> *"Traditional banking provides a fair amount of privacy by default. Your in-laws don't see that you're buying birth control that deprives them of grandchildren, your employer doesn't learn about the non-profits you support with money from your paycheck, and thieves don't see your latest purchases or how wealthy you are to help them target and scam you. Poor privacy in Bitcoin can be a major practical disadvantage for both individuals and businesses."*

Bitcoin's base layer has real privacy gaps. Address reuse exposes payment history. The common-input-ownership heuristic lets chain analysis firms cluster wallets. Wallet software creates identifiable fingerprints in every transaction. Light clients leak user addresses to third parties. Your node's network connections can reveal which transactions are yours.

The solutions exist — Silent Payments, Payjoin, Coinswap, compact block filters, ASmap, privacy-aware transaction construction — but they need developers to build, integrate, and maintain them. The biggest bottleneck isn't research. It's a shortage of developers who understand these problems deeply enough to write the code.

**This curriculum produces those developers.**

Every session teaches a real privacy problem, shows you the code that solves it, and guides you to contribute to the open-source projects building the fix. You don't need to be an expert developer to start. You need to be curious and willing to learn.

---

## How This Track Works

| | |
|---|---|
| **Structure** | 24 bi-weekly sessions (every 2 weeks), 2-2.5 hours each |
| **Duration** | 12 months |
| **Drop in, drop out** | **Every session stands on its own.** Join at any session. Attend the ones that interest you. Skip the ones that don't. Come back whenever you want. Some people will do all 24. Others will show up for the Payjoin sessions, disappear for three months, and come back for the CoinSwap block. All of that is fine. Each session teaches one complete topic and ends with a real contribution to a real Bitcoin project. |
| **Who is this for** | Anyone with basic Bitcoin knowledge who wants to build. Completed Bitcoin Dojo or equivalent. Comfortable reading code. Python or Rust experience helpful but not required. |
| **What you walk away with** | PRs on real Bitcoin privacy projects. A portfolio of open-source contributions. Deep understanding of how Bitcoin privacy works and what's broken. A community of builders who care about the same things you do. |
| **License** | CC0 1.0 Universal (public domain) |

---

## For Tutors — You Don't Need to Be an Expert

**You don't need to be a deep technical developer to run this track.** You need to be a curious Bitcoiner with a desire to build on Bitcoin and a willingness to learn alongside your participants.

Every session includes a **Tutor Preparation** section written in plain language. It tells you:
- What the session is actually about (no jargon)
- How much time to spend studying beforehand (usually 2-3 hours)
- Analogies you can use to explain the concepts
- Common questions participants will ask, and how to answer them
- How to run the session step by step
- What to do when you don't know the answer

**The five rules for teaching this well:**

1. **Do the reading.** Each session lists 2-3 resources. Read them the week before. You don't need to understand every line of code — you need to understand the *concept* well enough to explain *why it matters*.
2. **Do the exercises yourself first.** Run through the Build section before the session. You'll hit the same errors your participants will hit. That's gold — you'll know how to help them.
3. **Be honest about what you don't know.** "I don't know, let's figure it out together" is a perfectly valid answer. Your participants are developers — they respect honesty over faking expertise. Often someone in the room will know.
4. **Focus on the WHY, not just the HOW.** Anyone can look up how ECDH works. What matters is *why* Silent Payments need ECDH, and what happens to real people's privacy without it.
5. **Use the analogies.** Each Tutor Preparation section includes plain-language analogies. They work. Use them.

**You will learn this material deeply by teaching it.** That's not a bug — it's a feature. The best Bitcoin developers started by teaching what they'd just learned. This track is designed so that the tutor grows alongside the participants.

---

## What Bitcoin Privacy Problems We're Solving

Bitcoin has specific, known privacy weaknesses. Each one has projects working on a fix. This track covers all of them:

| Privacy Problem | What's Actually Happening | The Fix | Sessions |
|---|---|---|---|
| **Address reuse** | If you use the same Bitcoin address twice, anyone can see all payments you've ever received to it. Like having your bank account balance on a billboard. | [Silent Payments (BIP352)](https://github.com/bitcoin/bips/blob/master/bip-0352.mediawiki) — derive a unique address for every payment from one static identifier | 5-8 |
| **Common-input-ownership** | When you spend from multiple addresses in one transaction, analysts assume all those addresses belong to you — and cluster your entire wallet. | [Payjoin (BIP77/78)](https://github.com/payjoin/rust-payjoin) — both sender and receiver contribute inputs, breaking the assumption | 9-12 |
| **Wallet fingerprinting** | Every wallet builds transactions slightly differently. Version numbers, fee rates, output ordering — tiny differences that tell analysts which wallet you use. | Better transaction construction in [Bitcoin Core](https://github.com/bitcoin/bitcoin), [BDK](https://github.com/bitcoindevkit/bdk), [rust-bitcoin](https://github.com/rust-bitcoin/rust-bitcoin) | 2-4, 22 |
| **Light client privacy** | Most people don't run full nodes. Light wallets ask servers "do you have transactions for my addresses?" — telling the server exactly which addresses are yours. | [Compact block filters (BIP157/158)](https://github.com/rustaceanrob/kyoto), [Floresta](https://github.com/vinteumorg/Floresta) — check locally, never reveal your addresses | 7, 14-15 |
| **Network surveillance** | When your node broadcasts a transaction, the first node that sees it can link your IP to it. Your ISP sees everything. | Dandelion++, [ASmap](https://github.com/sipa/asmap), Tor/I2P integration | 13-14 |
| **Transaction graph analysis** | Analysts follow the trail of transactions across the blockchain. Your coins leave breadcrumbs. | [Coinswap/Teleport](https://github.com/nickhntv/teleport-transactions), [JoinMarket NG](https://github.com/nickhntv/joinmarket-ng) — break the trail | 17-18 |
| **Coin selection leaks** | How your wallet chooses which coins to spend reveals information — your balance, which output is change, which addresses are linked. | Privacy-aware coin selection in [Bitcoin Core](https://github.com/bitcoin/bitcoin/blob/master/src/wallet/coinselection.cpp) and [BDK](https://github.com/bitcoindevkit/bdk) | 3, 21 |
| **Taproot adoption gap** | Taproot makes complex transactions look identical to simple ones — but only if enough people use it. Privacy needs a crowd. | Wallet integrations, default P2TR in [rust-bitcoin](https://github.com/rust-bitcoin/rust-bitcoin), BDK | 16 |

---

## The Contribution Ladder

You start by reading code. You end by shipping code. Every step counts.

| Sessions | Level | What You're Doing |
|---|---|---|
| 1-4 | **Engage** | Star repos, read source code, file issues, improve documentation |
| 5-8 | **Submit** | Review PRs, add test cases, submit your first pull request |
| 9-12 | **Build** | Fix bugs, add features, submit PRs to multiple projects |
| 13-16 | **Lead** | Tackle harder issues, review others' PRs, help newcomers |
| 17-20 | **Research** | Identify gaps, propose improvements, build new tools |
| 21-24 | **Ship** | Substantial contributions, present your work, join the fellowship |

---

## Curriculum

### Phase 1: Foundations — How Privacy Breaks on Bitcoin's Base Layer
*Sessions 1-4*

Before you can build privacy tools, you need to understand exactly how privacy fails today. These four sessions teach the core chain analysis techniques, how wallet software creates fingerprints, and how coin selection leaks information.

---

#### Session 01: Chain Analysis & Surveillance — How Privacy Fails Today

##### Tutor Preparation

**Study time:** 2-3 hours the week before.

**What this session is about in plain language:** Chain analysis companies use a handful of simple tricks — called heuristics — to figure out who owns which Bitcoin addresses. The most important one: if two addresses appear as inputs in the same transaction, they probably belong to the same person. That single assumption lets them cluster hundreds of addresses into one identity. This session teaches what those tricks are, so participants can later build tools that break them.

**The 5 heuristics you need to understand and explain:**

1. **Common-input-ownership (CIOH):** "If Alice uses two addresses as inputs in one transaction, both are probably Alice's." *Analogy: paying for dinner with money from two different pockets — a watcher concludes both pockets are yours.*

2. **Change detection:** "In a 2-output transaction, one output is the payment and one is change. Analysts figure out which is which." *Analogy: handing a $50 bill for a $30 item. The $20 coming back is obviously change.*

3. **Address reuse:** "If an address appears in multiple transactions, they're all linked." *Analogy: using the same email for Amazon, political donations, and medical bills — anyone who knows one sees all.*

4. **Timing analysis:** "When transactions appear correlates with time zones and personal patterns." *Analogy: always sending Bitcoin at 9am Bangkok time? Probably in Southeast Asia.*

5. **Amount correlation:** "Round amounts and unusual amounts can be matched across transactions." *Analogy: sending exactly 0.31337 BTC, then someone receiving exactly that — probably connected.*

**Key point to drive home:** These aren't theoretical. Chainalysis uses them daily. Governments buy this data. People's financial lives are traced. Privacy tools aren't for criminals — they're for everyone who wants basic financial privacy.

**Common questions and how to handle them:**
- *"Isn't this just for criminals?"* → No. Read the Greg Maxwell quote in the intro. Your employer seeing your donations, thieves seeing your wealth, your family seeing your medical purchases. Privacy is normal.
- *"Can't I just use Tor?"* → Tor helps with IP privacy but doesn't help with on-chain analysis at all. The blockchain is permanent and public.
- *"Why not just use Monero?"* → Different tradeoffs. We're here to fix Bitcoin's privacy, not switch chains.

**How to run this session:**
1. Open [mempool.space](https://mempool.space) on the projector. Pick a random transaction. Walk through it: how many inputs? Outputs? Script types? Which output is probably change?
2. Show a real reused address (donation addresses work). Show the full transaction history visible to anyone.
3. Then let participants do the Build exercises.

---

**The problem:** Chain analysis firms use 5 core heuristics to deanonymize Bitcoin users. Understanding what every transaction reveals is the prerequisite for building solutions.

**Learn:**
- The 5 chain analysis heuristics: common-input-ownership (CIOH), change detection, address reuse, timing analysis, amount correlation
- How chain analysis firms cluster addresses into identity groups
- What the UTXO model reveals vs what an account model reveals
- Why privacy is a protocol-level requirement, not a user preference
- Real-world examples of harm from poor financial privacy

**Build:**
- Trace a 5-hop transaction chain on [mempool.space](https://mempool.space) and [OXT.me](https://oxt.me)
- Apply CIOH to cluster addresses. Identify likely change outputs using 4 different heuristics
- Write a Python script that takes a transaction ID and returns: input count, output count, script types, likely change output, fee rate, and a "privacy score" (0-100)
- Analyze 10 real mainnet transactions and classify each by privacy quality

**Contribute:**
- Create a GitHub account if you don't have one
- Star and fork these repos — the projects you'll contribute to:
  - [bitcoin/bitcoin](https://github.com/bitcoin/bitcoin) — Bitcoin Core
  - [cygnet3/rust-silentpayments](https://github.com/cygnet3/rust-silentpayments) — Silent Payments library
  - [payjoin/rust-payjoin](https://github.com/payjoin/rust-payjoin) — Payjoin Dev Kit
  - [vinteumorg/Floresta](https://github.com/vinteumorg/Floresta) — Privacy-preserving light client
  - [rustaceanrob/kyoto](https://github.com/rustaceanrob/kyoto) — BIP157/158 compact block filter client
  - [bitcoindevkit/bdk](https://github.com/bitcoindevkit/bdk) — Bitcoin Dev Kit
  - [rust-bitcoin/rust-bitcoin](https://github.com/rust-bitcoin/rust-bitcoin) — Rust Bitcoin library
- Clone `bitcoin/bitcoin` and build it locally. Read `src/wallet/coinselection.cpp` — you won't understand all of it yet, but you start reading real Bitcoin code on day one
- Read the [Bitcoin Wiki Privacy page](https://en.bitcoin.it/wiki/Privacy). Find one section that's outdated or unclear — you'll file an issue or edit later

**Reading:**
- [Bitcoin Privacy Wiki](https://en.bitcoin.it/wiki/Privacy) (read fully)
- Greg Maxwell's [CoinJoin original post](https://bitcointalk.org/index.php?topic=279249.0) (2013)

---

#### Session 02: Transaction Anatomy for Privacy — What Every Byte Reveals

##### Tutor Preparation

**Study time:** 2-3 hours.

**What this session is about in plain language:** A Bitcoin transaction is a blob of data — a few hundred bytes. But every byte carries information. The version number, the locktime, the sequence numbers, the order of outputs, the script type — all slightly different depending on which wallet built the transaction. It's like handwriting analysis: even if you write the same words, an expert can tell which pen you used.

**Key concept — "transaction construction":** This is the process by which a wallet builds a raw Bitcoin transaction. The *choices* the wallet makes — which inputs, what order for outputs, what fee rate, what locktime — these ARE the fingerprint. Improving how wallets construct transactions is one of the most important things Bitcoin privacy needs right now.

**Transaction fields explained simply:**
- **nVersion:** Almost always 1 or 2. Some wallets always use 2, some use 1. That alone is a tell.
- **nLockTime:** Some wallets set this to the current block height (anti-fee-sniping). Others leave it at 0. Different wallets, different behavior.
- **nSequence:** RBF signaling. Bitcoin Core uses one value, other wallets use another. Another fingerprint.
- **Output ordering:** Payment first then change? Change first? Random? Each is a pattern.
- **Script types:** If your inputs are SegWit but your change is Taproot, that mismatch reveals which output is change.

*Analogy: sending a letter. The words are the payment. But the envelope, stamp placement, handwriting, ink color, paper type — all tell the analyst who you are, even without a return address.*

**Common questions:**
- *"Why don't all wallets just agree on one standard?"* → They should. That's partly what this track is about. Coordination is hard, and many developers don't prioritize privacy.
- *"How much does this really matter?"* → A lot. Narrow down to "this came from Electrum" and you've eliminated 90% of wallets. Combined with other heuristics, it's very powerful.

**How to run this session:**
1. Decode a raw transaction hex together on the projector — field by field
2. Show 3-4 transactions side by side. Ask: "which wallet made each one?"
3. Then have them build a fingerprint-clean transaction themselves.

---

**The problem:** Every field in a Bitcoin transaction creates fingerprints that identify which wallet software built it. Fixing this is critical for base-layer privacy.

**Learn:**
- Raw transaction structure byte-by-byte: nVersion, vin[], vout[], nLockTime
- How nVersion, nLockTime, and nSequence differ across wallets
- Script types and their privacy implications: P2PKH, P2SH, P2WPKH, P2WSH, P2TR
- Fee estimation patterns as wallet fingerprints
- Output ordering: BIP69 (deterministic) vs random vs amount-sorted
- [0xB10C's wallet fingerprinting research](https://b10c.me/observations/03-blocktemplate-coinbase-transactions/)

**Build:**
- Decode 5 raw testnet transactions manually. Extract: version, locktime, sequence, script types, fee rate, output ordering
- Determine which wallet software likely created each based on fingerprints alone
- Construct a raw transaction that avoids all known fingerprints

**Contribute:**
- Pick one wallet (Sparrow, BlueWallet, Electrum, Green, Nunchuk). Test its current version against known fingerprint patterns. Document everything
- If the behavior differs from published research, draft a GitHub issue (submit in Session 4)
- Browse the [Bitcoin Optech Topics page](https://bitcoinops.org/en/topics/). Note anything missing or outdated

**Reading:**
- 0xB10C's [wallet fingerprinting observations](https://b10c.me/)
- [Wallet fingerprinting and transaction construction](https://ishaana.com/blog/wallet_fingerprinting/) by Ishaana Misra
- Bitcoin Core source: `src/wallet/spend.cpp` — focus on `CreateTransaction()`

---

#### Session 03: UTXO Management & Coin Selection — The Hidden Privacy Leak

##### Tutor Preparation

**Study time:** 2 hours.

**What this session is about in plain language:** When you want to send 0.5 BTC, your wallet has to decide *which* of your coins to use. Maybe you have a 1 BTC coin and three 0.2 BTC coins. Each choice has different privacy consequences. This is called "coin selection" and it's one of the most underappreciated privacy leaks in Bitcoin.

**The 4 algorithms explained simply:**
1. **Largest-first:** Always picks the biggest coin. Simple but terrible — reveals you have a coin at least that big, always creates large change.
2. **Branch-and-bound (BnB):** Tries to find an exact combination that matches the payment. If it works, NO change output — ideal for privacy. Bitcoin Core prefers this.
3. **Knapsack:** Randomly tries combinations until it finds one close enough. Moderate privacy.
4. **Random:** Pick coins randomly until you have enough. Unpredictable but may link more addresses together.

**Key insight:** The best outcome is no change output at all. The worst is when change is obvious (you pay 1.0 BTC and get back 0.00003241 — that tiny output screams "change").

**Why this matters:** Both Bitcoin Core and BDK handle coin selection. Improvements here cascade to every wallet that uses them.

---

**The problem:** How a wallet chooses which UTXOs to spend reveals enormous amounts of information. Coin selection in [Bitcoin Core](https://github.com/bitcoin/bitcoin/blob/master/src/wallet/coinselection.cpp) and [BDK](https://github.com/bitcoindevkit/bdk) directly affects every user's privacy.

**Learn:**
- 4 coin selection algorithms: largest-first, branch-and-bound, knapsack, random
- How each algorithm affects privacy — why BnB is preferred when it finds an exact match
- [Murch's coin selection research](https://murch.one/wp-content/uploads/2016/11/erhardt2016coinselection.pdf) and its influence on Bitcoin Core
- Dust attacks: how tiny UTXOs are tracking beacons
- Coin control: manual UTXO selection as a privacy tool

**Build:**
- Implement all 4 coin selection algorithms in Python
- Run each against identical UTXO sets. Score for privacy: input count, change amount, detectability
- Build a "privacy-optimized" selector that prefers changeless transactions

**Contribute:**
- Read Bitcoin Core's coin selection: `src/wallet/coinselection.cpp` and `src/wallet/spend.cpp`. Find a comment that could be clearer, a confusing variable name, or an untested edge case
- Browse [BDK issues labeled "coin-selection"](https://github.com/bitcoindevkit/bdk/labels/coin-selection). If you can reproduce one, comment with your findings
- Look at Murch's research. Are the algorithms fully implemented in Core today?

**Reading:**
- Murch's [coin selection thesis](https://murch.one/wp-content/uploads/2016/11/erhardt2016coinselection.pdf)
- Bitcoin Core source: `src/wallet/coinselection.cpp`
- BDK documentation on [coin selection](https://docs.rs/bdk_wallet/latest/bdk_wallet/)

---

#### Session 04: Wallet Fingerprinting & Your First Contribution

##### Tutor Preparation

**Study time:** 2 hours.

**What this session is about:** This pulls together everything from Sessions 1-3. Participants analyze real transactions, identify wallets, and build fingerprint-clean transactions. Then they file their first GitHub issue or documentation PR.

**This is the first real contribution session.** Many people are intimidated by contributing to open-source Bitcoin projects. Your job is to make it feel achievable:
- "You're not rewriting Bitcoin Core. You're filing a well-described issue about a fingerprint you found."
- "Documentation PRs are how every Bitcoin Core contributor started."
- "The maintainers want help. They'll be glad to see your issue."

**How to handle contributions:**
1. Have everyone pick Option A, B, C, or D before starting
2. Walk the room. Read their drafts. Suggest improvements.
3. Pair anyone who's stuck with someone more confident
4. Goal: everyone leaves with something submitted or ready to submit

---

**The problem:** If every wallet constructed transactions identically, chain analysis would lose one of its most powerful tools. Fixing this requires work in foundational libraries and in individual wallets.

**Learn:**
- Complete catalog of known wallet fingerprints
- How to construct a "fingerprint-clean" transaction
- Transaction batching: when it helps privacy and when it hurts
- The concept of "privacy by default" — users shouldn't need to think about fingerprinting

**Build:**
- Given 10 raw transactions, identify which wallet created each
- Construct a fingerprint-clean transaction. Have another participant try to identify the wallet — if they can't, you win
- Write a "transaction construction privacy checklist" for wallet developers

**Contribute — your first real contribution:**
- **Option A:** File an issue on a wallet repo documenting a privacy fingerprint you discovered
- **Option B:** Submit a documentation PR to the [Bitcoin Wiki Privacy page](https://en.bitcoin.it/wiki/Privacy)
- **Option C:** Submit a PR to [rust-bitcoin](https://github.com/rust-bitcoin/rust-bitcoin) or [BDK](https://github.com/bitcoindevkit/bdk) improving docs or adding a test case
- **Option D:** Publish your fingerprinting analysis as a GitHub gist and share with the community

> **Phase 1 checkpoint:** You've read real Bitcoin Core source code, analyzed real transactions, and made your first contribution. You understand how chain analysis works and how wallet behavior creates privacy leaks.

---

### Phase 2: Silent Payments (BIP352) — Solving Address Reuse
*Sessions 5-8*

Address reuse is the most common on-chain privacy failure. Static donation addresses, payment pages, and QR codes all reuse addresses — exposing the full payment history of the recipient. [BIP352 Silent Payments](https://github.com/bitcoin/bips/blob/master/bip-0352.mediawiki) solves this by deriving unique addresses from a single public identifier, without the sender and receiver ever needing to interact.

---

#### Session 05: BIP352 Deep Dive — How Silent Payments Work

##### Tutor Preparation

**Study time:** 3 hours. This is the most cryptography-heavy session. Don't panic.

**What this session is about in plain language:** If you put a Bitcoin address on your website for donations, everyone who donates can see every other donation, your total balance, and when you spend. Silent Payments fix this: you publish ONE identifier, and every sender's wallet automatically derives a *unique, one-time address* that only you can spend from. No two senders ever use the same address. No interaction needed.

**ECDH explained simply (you MUST understand this):**

ECDH = Elliptic Curve Diffie-Hellman. The core idea:
- Alice has secret key `a`, public key `A`
- Bob has secret key `b`, public key `B`
- Alice computes `a × B` → gets a point
- Bob computes `b × A` → gets the SAME point
- They've created a shared secret without revealing their private keys

*Analogy: Alice and Bob each have a secret paint color. They publicly share yellow paint. Alice mixes her secret with yellow, Bob mixes his with yellow, they exchange results. Each adds their own secret to arrive at the same final color — but nobody watching can figure it out.*

For Silent Payments: the sender uses their private key and the receiver's public scan key to derive a shared secret. That secret tweaks the receiver's spend key to produce a unique output.

**The scanning problem:** The receiver doesn't know when someone has sent them a Silent Payment. They must check EVERY transaction in EVERY block. For a full node, slow but possible. For a phone wallet, too heavy. This is why compact block filters (BIP157/158) and [Kyoto](https://github.com/rustaceanrob/kyoto) matter — they reduce the scanning burden.

**Common questions:**
- *"Why not just use HD wallets?"* → HD wallets need you to give each sender a different address. That requires interaction. Silent Payments work from one static identifier.
- *"How is this different from Monero stealth addresses?"* → Similar concept, designed specifically for Bitcoin's UTXO model.

---

**The problem:** Address reuse exposes full payment history. Existing solutions (HD wallets, BIP47) require interaction. Silent Payments solve this using ECDH.

**Learn:**
- The address reuse problem in depth
- ECDH shared secret derivation on secp256k1
- BIP352: scan keys vs spend keys, shared secret → unique output address, labeling
- Why scanning is expensive and how compact block filters help
- Current implementation status: Bitcoin Core, [rust-silentpayments](https://github.com/cygnet3/rust-silentpayments)

**Build:**
- Derive Silent Payment shared secrets by hand using pure Python secp256k1 math
- Compute the full flow: SP address → ECDH shared secret → tweak → output key
- Verify against official [BIP352 test vectors](https://github.com/bitcoin/bips/tree/master/bip-0352)

**Contribute:**
- Read [BIP352](https://github.com/bitcoin/bips/blob/master/bip-0352.mediawiki) end to end. File an issue for anything ambiguous
- Clone [rust-silentpayments](https://github.com/cygnet3/rust-silentpayments). Build it. Run the tests. Read `sending.rs`
- Browse [open issues](https://github.com/cygnet3/rust-silentpayments/issues). Comment on one with your understanding

---

#### Session 06: Implement a Silent Payments Sender

##### Tutor Preparation

**Study time:** 2 hours. Do the Build exercise yourself.

**What this session is about:** Participants implement the full sending pipeline in code. They did the math by hand in Session 5; now they build the complete flow. This is mostly hands-on coding. Walk the room, help debug. Common issues: byte ordering, key serialization, getting the ECDH input wrong.

**If someone is stuck:** Pair them up. Pair programming is how real open-source development works.

---

**Learn:**
- Complete SP send flow: input selection, key aggregation, shared secret computation, output key derivation
- Edge cases: single vs multiple inputs, Taproot vs SegWit, multiple recipients
- Full BIP352 test vector validation

**Build:**
- Implement the full SP sending pipeline in Python
- Handle all edge cases: single Taproot input, mixed types, multiple SP recipients
- Pass every [BIP352 test vector](https://github.com/bitcoin/bips/tree/master/bip-0352)

**Contribute:**
- Check the test vectors. Any edge cases missing? File an issue
- Add a test case to [rust-silentpayments](https://github.com/cygnet3/rust-silentpayments)
- Publish your Python implementation as a reference tool on GitHub

---

#### Session 07: Scanning, Receiving & Compact Block Filters (BIP157/158)

##### Tutor Preparation

**Study time:** 2-3 hours.

**What this session is about in plain language:** Sessions 5-6 were about *sending* Silent Payments. This is about *receiving* them — the hard part. The receiver must check every transaction in every block to find payments addressed to them. Compact block filters solve this: download a small filter per block, check locally whether the block *might* contain your transaction. If no, skip it. If yes, download and check.

*Analogy: looking for a book in a library. Instead of reading every book, check the catalog. The catalog says "possibly on this shelf" or "definitely not." Only check shelves the catalog flags.*

**[Kyoto](https://github.com/rustaceanrob/kyoto)** implements this in Rust — critical infrastructure for mobile Silent Payments wallets. **[Floresta](https://github.com/vinteumorg/Floresta)** takes a different approach using utreexo. Both need contributors.

---

**The problem:** Receiving Silent Payments requires scanning every block. Compact block filters let light clients check locally without revealing addresses to servers.

**Learn:**
- SP scanning algorithm: extract input keys → compute ECDH → check outputs
- Compact block filters: Golomb-Rice Coded Sets, false positive rates, BIP157 protocol
- How CBFs optimize SP scanning
- [Kyoto](https://github.com/rustaceanrob/kyoto) and [Floresta](https://github.com/vinteumorg/Floresta) architectures

**Build:**
- Build a minimal SP scanner in Python
- Implement Golomb-Rice encoding/decoding from scratch
- Build a compact block filter. Measure false positive rate
- Combine CBF + scanner. Measure the speedup

**Contribute:**
- Review a PR on [bitcoin/bitcoin](https://github.com/bitcoin/bitcoin) related to Silent Payments or block filters
- Clone [Kyoto](https://github.com/rustaceanrob/kyoto). Build it. Run it. File well-described bugs
- File issues for any performance problems or bugs in your scanner

---

#### Session 08: Contributing to Silent Payments — Your First PR

##### Tutor Preparation

**Study time:** 1-2 hours prep. This session is mostly facilitation.

**Before the session:** Browse open issues on rust-silentpayments, Kyoto, and bitcoin/bitcoin (SP-related). Make a list of 10-15 approachable issues. Categorize by difficulty and language.

**During the session:** Match each participant to an issue based on their skill level. Let them work. Walk the room. Help with git, build issues, PR formatting.

**The phrase to repeat:** "Your PR doesn't have to be perfect. It has to exist."

---

**Build:**
- Clone your target repo. Build locally. Run tests. Pick an issue. Write your fix. Submit your PR.

**Contribute — submit a PR:**
- **Option A (Rust):** Test case, documentation, or feature in [rust-silentpayments](https://github.com/cygnet3/rust-silentpayments) or [Kyoto](https://github.com/rustaceanrob/kyoto)
- **Option B (C++):** Review and test a Silent Payments PR on [bitcoin/bitcoin](https://github.com/bitcoin/bitcoin)
- **Option C (Any language):** Improve documentation for BIP352, wallet integration guides, Bitcoin Optech
- **Option D (Ambitious):** Start integrating Silent Payments into a wallet that doesn't have it

**Nobody leaves without a PR submitted or a substantive review posted.**

> **Phase 2 checkpoint:** You've submitted at least 1 PR or review to a Silent Payments or block filter project. You understand BIP352 cryptography and the scanning problem.

---

### Phase 3: Payjoin (BIP77/78) — Breaking Chain Analysis's Best Weapon
*Sessions 9-12*

The common-input-ownership heuristic is the single most powerful tool in chain analysis. [Payjoin](https://github.com/payjoin/rust-payjoin) breaks it by having both sender and receiver contribute inputs — making the transaction look ordinary but invalidating the assumption that all inputs belong to one person. Unlike CoinJoin, Payjoin transactions are *invisible*. They improve privacy for everyone.

---

#### Session 09: How Payjoin Defeats Chain Analysis

##### Tutor Preparation

**Study time:** 2-3 hours.

**What this session is about in plain language:** Remember CIOH? "If two addresses are inputs in the same transaction, they belong to the same person." Payjoin destroys it. In a normal payment, only the sender puts inputs in. In a Payjoin, BOTH sender and receiver contribute. The transaction looks normal — but the CIOH assumption is wrong.

*Analogy: at a restaurant, one person puts money on the table. In a Payjoin, both put money on the table and both get change. An observer can't tell whose is whose.*

**Why this is so powerful:** Every Payjoin makes CIOH unreliable not just for that transaction, but for ALL transactions. If some violate CIOH, analysts can never be sure any follows it. This raises the baseline privacy of every Bitcoin user.

**BIP77 vs BIP78:**
- BIP78 (V1): Receiver must be online. Sender → receiver → sender → broadcast.
- BIP77 (V2, "Async Payjoin"): Serverless. Uses a relay directory. Neither party needs to be online at the same time.

**The 5 sender checks** (prevents the receiver from stealing):
1. No new outputs added
2. Original outputs not reduced
3. No inputs removed
4. Fees don't spike unreasonably
5. Transaction still valid to sign

---

**Learn:**
- CIOH in depth: why it's chain analysis's best weapon and what breaks when it fails
- Payjoin V1 (BIP78) and V2 (BIP77, Async Payjoin)
- The 5 sender verification checks
- Why Payjoin is more powerful than CoinJoin for systemic privacy
- Current adoption: [BTCPay Server](https://github.com/btcpayserver/btcpayserver), [Bull Bitcoin](https://www.bullbitcoin.com/)

**Build:**
- Analyze 10 testnet transactions — which are Payjoins? (Should be hard to tell)
- Walk through the full BIP77 async flow
- Implement all 5 sender verification checks in pseudocode

**Contribute:**
- Clone [rust-payjoin](https://github.com/payjoin/rust-payjoin). Build it. Run tests. Read `src/send.rs` and `src/receive.rs`
- Browse [open issues](https://github.com/payjoin/rust-payjoin/issues). Target `good first issue` labels
- Read [BIP77](https://github.com/bitcoin/bips/blob/master/bip-0077.mediawiki). File issues for inconsistencies

---

#### Session 10: Building with Payjoin Dev Kit

##### Tutor Preparation

**Study time:** 2-3 hours. Build the Rust exercise yourself.

**Your role:** Circulate. Help people understand the *flow*. The Rust specifics are secondary — participants can read docs. What they need from you is understanding of what the code does and why. If someone can't do Rust, they can follow along in Python or pair up.

---

**Learn:**
- [PDK (Payjoin Dev Kit)](https://github.com/payjoin/rust-payjoin) architecture
- PSBT construction and modification
- Integrating PDK into a wallet application

**Build:**
- Complete Payjoin flow in Rust using PDK
- Analyze the on-chain result — can you tell it was a Payjoin?

**Contribute:**
- File issues on [rust-payjoin](https://github.com/payjoin/rust-payjoin): unclear docs, bad error messages, missing examples
- Fix documentation yourself — docs PRs are the fastest path to merged code
- Submit integration examples to the examples/ directory

---

#### Session 11: Payjoin Adoption — Integration Is Everything

##### Tutor Preparation

**Study time:** 2 hours. Set up BTCPay Server on testnet before class.

**Key insight:** One well-researched GitHub issue titled "Payjoin (BIP77) Support — Feasibility Assessment" on a popular wallet's repo can be the seed that leads to adoption. Wallet developers are busy. Hand them a clear analysis and they're much more likely to act.

---

**Learn:**
- BTCPay Server's Payjoin implementation
- UX: making Payjoin invisible to users
- The adoption curve: which wallets support Payjoin, which should be next

**Build:**
- Set up BTCPay Server with Payjoin. Make payments. Trace the code path
- Compare on-chain: Payjoin vs regular payment (there should be no observable difference)

**Contribute:**
- Pick a wallet that doesn't support Payjoin. Write a feasibility assessment as a GitHub issue
- Test BTCPay Server's Payjoin with different sender wallets. File bugs
- Review open Payjoin PRs

---

#### Session 12: Contributing to Payjoin — Ship Your Code

##### Tutor Preparation

Same format as Session 08. Working session. Curate 10-15 issues. Match participants. Walk the room.

---

**Contribute — submit a PR:**
- Target: [rust-payjoin](https://github.com/payjoin/rust-payjoin), [BTCPay Server](https://github.com/btcpayserver/btcpayserver), or any wallet
- **Peer review:** every participant reviews one other participant's PR

> **Phase 3 checkpoint:** PRs in both Silent Payments and Payjoin ecosystems. You can explain how CIOH works and how Payjoin defeats it.

---

### Phase 4: Network & Protocol Privacy — Your Node Leaks Too
*Sessions 13-16*

Privacy isn't just about transactions on the blockchain. Your node's network connections, peer selection, and light client queries all leak information.

---

#### Session 13: P2P Network Privacy — Transaction Relay, ASmap & Eclipse Attacks

##### Tutor Preparation

**Study time:** 2-3 hours.

**What this session is about:** Everything so far has been about what's visible ON the blockchain. This session is about what's visible on the NETWORK — the internet connections your Bitcoin node makes.

**Three concepts to explain:**

1. **First-spy attacks:** Your node sends a transaction to its peers. The first peer to receive it knows you're probably the source. *Analogy: whispering a secret to 8 people simultaneously — any listener knows you're the source.* **Dandelion++** fixes this by first sending along a random single path (stem) before broadcasting widely (fluff).

2. **Eclipse attacks:** If an attacker controls all your node's connections, they control what you see. **Mitigated by** clever bucketing in Bitcoin Core's address manager and "anchor connections."

3. **ASmap:** An AS (autonomous system) is a chunk of internet controlled by one organization. If all your peers are in the same AS, that org sees all your traffic. [ASmap](https://github.com/sipa/asmap) maps IPs to ASes so Bitcoin Core diversifies peer connections across network boundaries. **Actively needs contributors.**

---

**Learn:**
- Transaction relay and IP linking
- Dandelion++ stem-and-fluff
- [ASmap](https://github.com/sipa/asmap): peer diversity across autonomous systems
- Tor and I2P integration in Bitcoin Core
- Eclipse attack mitigations

**Build:**
- Configure Bitcoin Core: clearnet-only, Tor-only, and hybrid. Compare peer connections
- Map your node's peers to autonomous systems. Calculate eclipse attack surface

**Contribute:**
- Improve Bitcoin Core's `doc/tor.md` or `doc/i2p.md`
- [ASmap](https://github.com/sipa/asmap) needs contributors — better data sources, testing, documentation
- Comment on P2P-related Bitcoin Core issues with test results

---

#### Session 14: Compact Block Filters — Privacy-Preserving Light Clients

##### Tutor Preparation

**Study time:** 2 hours.

**BIP37 vs BIP157 — the key difference:**
- BIP37 (old): Client tells the server what it's looking for. Server learns your addresses. [Privacy disaster.](https://eprint.iacr.org/2014/763.pdf)
- BIP157 (new): Server creates a filter for each block. Client downloads and checks locally. Server never learns what you're looking for.

*Analogy: BIP37 = telling a librarian your interests. BIP157 = the librarian posts a catalog and you check it yourself.*

---

**Learn:**
- Why BIP37 was broken
- Golomb-Rice Coded Sets: the compression behind compact block filters
- BIP157 client-server protocol
- [Kyoto](https://github.com/rustaceanrob/kyoto) and [Floresta](https://github.com/vinteumorg/Floresta) implementations

**Build:**
- Implement Golomb-Rice encoding/decoding from scratch
- Build a GCS filter. Query it. Calculate false positive rate

**Contribute:**
- [Kyoto](https://github.com/rustaceanrob/kyoto): clone, build, run, file bugs
- [Floresta](https://github.com/vinteumorg/Floresta): browse issues, comment with analysis
- Test both on signet. Submit missing setup docs

---

#### Session 15: Light Client Privacy — The Full Spectrum

##### Tutor Preparation

**Study time:** 2 hours.

**Draw this on a whiteboard — the privacy spectrum:**
1. SPV (worst) → 2. Electrum (bad) → 3. BIP157/Kyoto (good) → 4. Floresta/utreexo (good) → 5. Full node (best)

**Key question to pose:** "If you're building a mobile wallet, which approach gives the best privacy for a phone's constraints?"

---

**Learn:**
- The full light client privacy spectrum
- Floresta: utreexo-based validation
- Kyoto: BIP157/158 implementation
- How Silent Payments scanning differs in each model

**Build:**
- Set up Floresta on signet. Monitor information flow
- Build a privacy comparison matrix for all 5 approaches

**Contribute:**
- [Floresta "good first issue"](https://github.com/vinteumorg/Floresta/issues) labels
- Submit your comparison matrix as a docs PR
- File issues with reproduction steps for any bugs

---

#### Session 16: Taproot Privacy — Making Complex Transactions Invisible

##### Tutor Preparation

**Study time:** 2 hours.

**What this session is about:** Before Taproot, multisig looked different from single-sig on-chain. Taproot fixes this — a 2-of-3 multisig can look identical to a regular payment. But Taproot only provides privacy if enough people use it. If only 5% of transactions are Taproot, those users stand out. Privacy needs a crowd.

**Key concepts:** Key path spending (happy path, invisible), script path spending (backup, reveals the script), MuSig2 (multi-party signatures that look like single-sig), FROST (threshold signatures), CISA (future proposal making CoinJoin cheaper).

---

**Learn:**
- Taproot: multisig indistinguishable from single-sig
- MAST: complex conditions, only reveal the branch used
- MuSig2 and FROST
- CISA: making CoinJoin cheaper
- Why Taproot adoption matters

**Build:**
- Create three Taproot transactions on signet: single-sig, 2-of-2 MuSig, script path
- Compare on-chain footprints
- Analyze Taproot adoption metrics

**Contribute:**
- File issues on wallets that don't default to Taproot
- Review Taproot PRs on Bitcoin Core, rust-bitcoin, or BDK

> **Phase 4 checkpoint:** Contributed to 3-4 repos. Understand P2P privacy, ASmap, block filters, light clients, and Taproot.

---

### Phase 5: Advanced Privacy — CoinJoin, CoinSwap, eCash & Lightning
*Sessions 17-20*

Advanced techniques that complement base-layer privacy. CoinJoin, Coinswap, eCash, and Lightning each solve different parts of the privacy puzzle.

---

#### Session 17: CoinJoin & JoinMarket NG — Equal-Output Mixing

##### Tutor Preparation

**Study time:** 2-3 hours.

**CoinJoin explained:** Multiple users combine transactions into one where everyone's outputs are equal amounts. An observer can't tell which input maps to which output.

*Analogy: 5 people put $100 bills into a hat. Hat shakes. 5 people take out $100 bills. Can't tell whose is whose.*

**The problem — toxic change:** If Alice puts in 0.15 BTC, takes out 0.1 (equal output) + 0.05 (change), that change might link back to her.

**JoinMarket NG:** Orderbook-based CoinJoin without a central coordinator. Makers offer liquidity and earn fees. Takers pay to mix. No coordinator needed.

---

**Learn:**
- CoinJoin mechanics and toxic change
- WabiSabi protocol
- [JoinMarket NG](https://github.com/nickhntv/joinmarket-ng)
- CoinJoin weaknesses: Sybil attacks, timing, amount analysis

**Build:**
- Analyze 20 mainnet transactions. Identify CoinJoins. Calculate anonymity sets
- Simulate a 5-user CoinJoin. Analyze what an analyst can determine
- Compare CoinJoin vs Payjoin

**Contribute:**
- Publish your CoinJoin analyzer as a CC0 repo
- Clone [Teleport Transactions](https://github.com/nickhntv/teleport-transactions) (next session). File issues
- Write a comparison of CoinJoin implementations

---

#### Session 18: CoinSwap & Teleport — Breaking the Transaction Graph

##### Tutor Preparation

**Study time:** 2 hours.

**CoinSwap vs CoinJoin:** CoinJoin mixes within one visible transaction. CoinSwap makes two SEPARATE normal-looking transactions that swap coins. No visible connection.

*Analogy: Alice has a red ball, Bob has a blue ball. They use separate dropboxes. Alice picks up the blue ball, Bob picks up the red one. An observer sees two ordinary handoffs.*

Trustless via Hash Time-Locked Contracts. [Teleport Transactions](https://github.com/nickhntv/teleport-transactions) is the active implementation — early-stage and needs contributors badly.

---

**Learn:**
- How CoinSwap breaks the transaction graph
- HTLCs: trustless atomic swaps
- Multi-hop CoinSwap for plausible deniability
- [Teleport Transactions](https://github.com/nickhntv/teleport-transactions)

**Build:**
- Diagram a 2-party and 3-hop CoinSwap. Analyze what observers see
- Calculate costs vs CoinJoin

**Contribute:**
- [Teleport Transactions](https://github.com/nickhntv/teleport-transactions) is early-stage — **high impact** contribution territory
- File issues, improve docs, start on a bug fix

---

#### Session 19: eCash Privacy — Fedimint & Cashu

##### Tutor Preparation

**Study time:** 2 hours.

**What eCash does differently:** Everything else improves privacy on the blockchain. eCash moves transactions off-chain into a system where the operator literally cannot see who's transacting — via blind signatures.

*Analogy: put money in an envelope with carbon paper. The bank stamps the outside without opening it. The stamp transfers through. Bank recognizes its stamp later but never saw what was inside.*

**Trust tradeoff:** You trust the mint not to steal or inflate. Cashu = single operator, Fedimint = federated (multiple operators, threshold signatures).

---

**Learn:**
- Chaumian blind signatures
- [Cashu](https://github.com/cashubtc/nutshell): mint-receive-send-melt lifecycle
- [Fedimint](https://github.com/fedimint/fedimint): federated custody, Lightning gateway
- How eCash complements on-chain privacy

**Build:**
- Set up a Cashu mint on signet. Mint, send, redeem tokens
- Analyze what the mint learns at each stage

**Contribute:**
- [cashubtc/nutshell](https://github.com/cashubtc/nutshell) is Python — accessible to everyone
- [fedimint/fedimint](https://github.com/fedimint/fedimint) has "good first issue" labels
- Write a setup guide and submit as a docs PR

---

#### Session 20: Lightning Privacy — BOLT12 & Blinded Paths

##### Tutor Preparation

**Study time:** 2 hours.

**Lightning's privacy model:** Onion-routed payments (good). But channel balances can be probed, the graph is public, and BOLT11 invoices reveal the receiver's node. BOLT12 offers fix receiver privacy with blinded paths — the last hops are encrypted.

---

**Learn:**
- Lightning privacy: onion routing, balance probing, graph analysis
- BOLT12 blinded paths: receiver privacy
- Private vs public channels
- Trampoline routing

**Build:**
- Set up LN nodes on signet. Probe channel balances
- Compare BOLT11 vs BOLT12: what information is revealed?

**Contribute:**
- [LDK (rust-lightning)](https://github.com/lightningdevkit/rust-lightning) has "good first issue" labels
- Publish your privacy analysis
- File issues for any problems found during testing

> **Phase 5 checkpoint:** Contributing across 5+ repos. Understand CoinJoin, CoinSwap, eCash, and Lightning privacy.

---

### Phase 6: Building & Shipping
*Sessions 21-24*

Everything learned, applied. Ship real code.

---

#### Session 21: Privacy-Preserving Wallet Development with BDK

##### Tutor Preparation

**Study time:** 2-3 hours.

**What this session is about:** [BDK](https://github.com/bitcoindevkit/bdk) is the foundation for many wallets. Privacy improvements here cascade to every wallet built on it. Participants build a wallet that's private by default.

**Your role:** Help with design decisions. "What coin selection strategy should the wallet default to? What happens when a user reuses an address?"

---

**Learn:**
- BDK architecture: descriptor wallets, coin selection, PSBT building
- Privacy-by-default wallet design
- Adding Silent Payments or Payjoin support to a BDK wallet

**Build:**
- Scaffold a BDK wallet: privacy-optimized coin selection, address reuse detection, anti-fee-sniping
- Add Payjoin send support using PDK

**Contribute:**
- Submit a PR to [BDK](https://github.com/bitcoindevkit/bdk): privacy config, docs, coin selection improvements

---

#### Session 22: Privacy Testing & Scoring

##### Tutor Preparation

**Study time:** 2 hours. Great publishable work — a well-built privacy scorer is a visible community contribution.

---

**Learn:**
- Systematic transaction privacy evaluation
- Mempool analysis
- Automated privacy testing for wallet CI

**Build:**
- Build a transaction privacy scorer: address reuse, script mixing, round amounts, change detection, fee fingerprints, locktime patterns, output ordering
- Score 20 mainnet transactions

**Contribute:**
- Publish your scorer as a CC0 repo
- Run it against popular wallets. File issues with data
- Submit methodology to Bitcoin Optech or Bitcoin Wiki

---

#### Session 23: Contribution Sprint — The Big Push

##### Tutor Preparation

Prepare 15-20 curated issues across all target repos. Categorize by difficulty and language.

**3-hour working session. Code ships today.**

| Time | Activity |
|---|---|
| 00:00 - 00:30 | Pick an issue from the curated list |
| 00:30 - 02:00 | Code: write, test, prepare the PR |
| 02:00 - 02:30 | Peer review: each participant reviews one PR |
| 02:30 - 03:00 | Submit and celebrate |

**Target repos:**

| Repo | Language |
|---|---|
| [bitcoin/bitcoin](https://github.com/bitcoin/bitcoin) | C++ |
| [rust-silentpayments](https://github.com/cygnet3/rust-silentpayments) | Rust |
| [rust-payjoin](https://github.com/payjoin/rust-payjoin) | Rust |
| [Floresta](https://github.com/vinteumorg/Floresta) | Rust |
| [Kyoto](https://github.com/rustaceanrob/kyoto) | Rust |
| [Teleport](https://github.com/nickhntv/teleport-transactions) | Rust |
| [Fedimint](https://github.com/fedimint/fedimint) | Rust |
| [Cashu/nutshell](https://github.com/cashubtc/nutshell) | Python |
| [BDK](https://github.com/bitcoindevkit/bdk) | Rust |
| [LDK](https://github.com/lightningdevkit/rust-lightning) | Rust |
| [rust-bitcoin](https://github.com/rust-bitcoin/rust-bitcoin) | Rust |
| [ASmap](https://github.com/sipa/asmap) | Python/C++ |

---

#### Session 24: Capstone — Present Your Contributions

##### Tutor Preparation

Confirm presentations. Help anyone who needs it prepare. Invite the broader community.

Each participant presents (10 minutes):
1. **What you contributed** — Walk through your PRs. Show the code.
2. **What impact it has** — Who benefits? How does this make Bitcoin more private?
3. **What you learned** — What was harder than expected?
4. **What's next** — If you had 6 more months, what would you build?

Open to the full Code Orange community.

**Graduation:** Submitted 3+ PRs to Bitcoin privacy projects and presented at capstone → eligible for the **Code Orange Developer Fellowship** ($500/month, 6 months) to continue contributing full-time.

---

## Expected Output

### Per participant:

| Metric | Target |
|---|---|
| PRs submitted | 5-8 |
| PRs merged | 3-5 |
| Repos contributed to | 3+ |
| Code reviews posted | 10+ |
| Issues filed | 5+ |

### Per cohort (15 participants, 12 months):

| Metric | Target |
|---|---|
| PRs submitted | 75-120 |
| PRs merged | 45-75 |
| New privacy developers | 15 |
| Repos contributed to | 12+ |

---

## Session Format

Every session follows this structure:

| Time | Activity |
|---|---|
| 00:00 - 00:15 | **Review:** What did you contribute since last session? What got merged? What's blocking? |
| 00:15 - 00:45 | **Concept:** Theory and protocol walkthrough |
| 00:45 - 01:45 | **Build:** Hands-on coding |
| 01:45 - 02:15 | **Contribute:** Open laptops. Find issues. File PRs. Review code. |
| 02:15 - 02:30 | **Plan:** Reading + contribution goal for next 2 weeks |

---

## Contribution Tracker

| Session | Contribution | Target Repos |
|---|---|---|
| 01 | Star repos. Clone bitcoin/bitcoin. Read coinselection.cpp | bitcoin/bitcoin, BDK, rust-silentpayments, rust-payjoin, Floresta, Kyoto, rust-bitcoin |
| 02 | Test a wallet's fingerprint. Draft an issue | Any wallet repo |
| 03 | Comment on a BDK coin selection issue | BDK, bitcoin/bitcoin |
| 04 | **File your first issue or docs PR** | Any wallet repo, Bitcoin Wiki, rust-bitcoin |
| 05 | Read BIP352. Comment on a rust-silentpayments issue | bitcoin/bips, rust-silentpayments |
| 06 | Add a test case or file issue on SP test vectors | bitcoin/bips, rust-silentpayments |
| 07 | Review a PR on bitcoin/bitcoin or Kyoto | bitcoin/bitcoin, Kyoto |
| 08 | **Submit your first PR** | rust-silentpayments, Kyoto, bitcoin/bitcoin |
| 09 | Clone rust-payjoin. Comment on an issue | rust-payjoin |
| 10 | File issues on PDK docs or API | rust-payjoin |
| 11 | File Payjoin feasibility issue on a wallet | Any wallet repo, BTCPay |
| 12 | **Submit a PR** to Payjoin ecosystem | rust-payjoin, BTCPay |
| 13 | Improve Bitcoin Core P2P docs or test ASmap | bitcoin/bitcoin, ASmap |
| 14 | Test and file issues on Kyoto or Floresta | Kyoto, Floresta |
| 15 | **Submit a PR** to Floresta or Kyoto | Floresta, Kyoto |
| 16 | File Taproot adoption issues | Any wallet repo |
| 17 | Publish CoinJoin analysis tool | teleport-transactions |
| 18 | **Submit a PR** to Teleport | teleport-transactions |
| 19 | Submit docs or test PR to Cashu or Fedimint | nutshell, fedimint |
| 20 | Submit a PR to LDK | rust-lightning |
| 21 | **Submit a PR** to BDK | BDK |
| 22 | Publish privacy scoring tool | Any wallet repo |
| 23 | **Contribution sprint** | Any privacy repo |
| 24 | Present. Apply for fellowship. | — |

---

## Exercises & Code

```
phase-1-foundations/
  session-01/  chain_analysis_lab.py
  session-02/  tx_anatomy_lab.py
  session-03/  coin_selection_simulator.py
  session-04/  wallet_fingerprint_lab.py

phase-2-silent-payments/
  session-05/  sp_ecdh_derivation.py
  session-06/  silent_payments_sender.py
  session-07/  sp_scanner_cbf.py

phase-3-payjoin/
  session-09/  payjoin_analysis.py
  session-10/  pdk_integration/
  session-11/  btcpay_payjoin_lab.md

phase-4-network-privacy/
  session-13/  p2p_privacy_lab.py
  session-14/  compact_block_filters.py
  session-16/  taproot_privacy_lab.py

phase-5-advanced/
  session-17/  coinjoin_analysis.py
  session-18/  coinswap_walkthrough.md
  session-19/  cashu_mint_exercise.md

phase-6-contributing/
  session-21/  bdk_privacy_wallet/
  session-22/  privacy_scorer.py
```

---

## Resources

- **[Reading List](reading-list.md)** — 70+ resources organized by phase
- **[Glossary](glossary.md)** — 60+ terms
- **[Facilitator Guide](facilitator-guide.md)** — Session-by-session notes
- **[Capstone Projects](capstone-projects.md)** — 4 project tracks with rubrics
- **[Contributing](CONTRIBUTING.md)** — How to contribute to this curriculum

---

## Our Track Record

Code Orange Dev School has already produced **45+ merged PRs** across Bitcoin Core, rust-bitcoin, BDK, rust-payjoin, peer-observer, LDK, hex-conservative, kernel-node, and more. Our graduates — [Chaitika](https://github.com/chaitika) (Silent Payments), [Arowolo](https://github.com/Arowolokehinde) (Payjoin), [Peter](https://github.com/pzafonte) (Bitcoin Core), [Razor](https://github.com/RazorBest) (peer-observer), [Vaan](https://github.com/va-an) (BDK/rust-bitcoin) — are already contributing to the exact projects this curriculum targets.

This works. We've proven it. The Privacy Track takes what we've learned and focuses it on the biggest open problem in Bitcoin: building the privacy tools that every user needs.

---

*Code Orange Dev School · Bitcoin House Bali, Indonesia · [codeorange.dev](https://codeorange.dev) · CC0 1.0 Universal*
