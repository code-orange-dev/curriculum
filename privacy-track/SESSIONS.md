# The Privacy Sessions: Season One

**90 min. Every 2 weeks. Hands-on, discussion-driven, review-first.**

- A hangout for privacy-minded, cypherpunk Bitcoiners, not a lecture series
- Every session: use or build a real privacy tool, then study a real open PR together
- Drop in any session. Each one re-teaches what it needs. Signet, testnet or regtest only, cameras optional

We open with Silent Payments because it's happening now. Bitcoin Core merged the BIP352 core logic in September 2026 ([#35301](https://github.com/bitcoin/bitcoin/pull/35301)), libsecp256k1 shipped a `silentpayments` module in v0.8.0, and sending ([#35302](https://github.com/bitcoin/bitcoin/pull/35302)) and receiving ([#32966](https://github.com/bitcoin/bitcoin/pull/32966)) are in review. Participants can learn the protocol, build it, and review it while the work is still going on.

## Season One Schedule

| Month | Session | Topic | Lab / tool |
|---|---|---|---|
| 1 | S1 | Silent Payments I: One Address, No Trail | [SP lab](./labs/silent-payments/): build a sender |
| 1 | S2 | Silent Payments II: Finding Your Money | [SP lab](./labs/silent-payments/): build a scanner, indexers |
| 2 | S3 | Silent Payments III: Review Club | Bitcoin Core / libsecp256k1 SP PRs |
| 2 | S4 | Think Like the Adversary: Chain Analysis & Fingerprinting | [chain-analysis lab](./labs/chain-analysis/), real wallets |
| 3 | S5 | Coin Selection & Change | [coin-selection lab](./labs/coin-selection/), Sparrow, BDK |
| 3 | S6 | Payjoin | payjoin-cli on signet, rust-payjoin |
| 4 | S7 | Light Clients & Your Own Node | [filters lab](./labs/compact-block-filters/), Kyoto, Floresta |
| 4 | S8 | The Network Sees You: Tor, BIP324, Private Broadcast, ASmap | Bitcoin Core 31 |
| 5 | S9 | Breaking the Trail: CoinJoin & OpenSwap | JoinMarket, openswap regtest |
| 5 | S10 | Lightning Privacy | BOLT11 vs BOLT12 on regtest |
| 6 | S11 | Ecash: Cashu & Fedimint | a signet mint |
| 6 | S12 | Contribution Sprint | the season's issue board |

---

## The Format: the same 6 beats every session

| Beat | Min | What happens |
|---|---|---|
| 🩸 Cold Open | 10 | A true surveillance story. Sets the stakes and starts the argument |
| 🕳 Rabbit Hole | 15 | The concept in plain language, with one analogy |
| 🛠 Hands-On | 30 | Everyone does it live on their own machine |
| 🔍 Review Circle | 20 | Read a live PR together: what does it change, how would we test it, what would we ask? |
| 📜 Cypherpunk Corner | 10 | Read a short primary text aloud, then argue about it |
| 🎯 Proof-of-Work Board | 5 | Claim one concrete follow-up: a lab finished, a PR tested, an issue reproduced, a doc fixed |

**Facilitator basics (every session):**
- You're a host, not a professor. If you don't know something, say so and read the code together
- Prep takes ~30-60 min: do the hands-on yourself, pick 1-2 live PRs for the Review Circle, and check that the issues on the board are still open *that morning*
- **The Review Circle does not post upstream on a timer.** Comments go upstream only when they're genuinely useful, e.g. a test report with steps, a reproduced bug, or a question the thread hasn't answered. A clean "built and tested on macOS, here's what I ran" is valuable. Filler ("nice work!", "concept ACK" without reasoning) costs maintainers time and costs us trust. See [PR_CHECKLIST.md](./PR_CHECKLIST.md)
- Sats reward completed proof of work (a finished lab, a test report, a merged doc fix), never comment counts
- Record evidence per the [contributor program](https://github.com/code-orange-dev/code-orange-dev/tree/main/privacy-contributor-program): what was reviewed/built/tested, and links. Merged PRs go on the [PR dashboard](https://github.com/code-orange-dev/PR-tracking-dashboard)
- Test networks only. No real balances on screen. Pseudonyms welcome

---

## S1 · Silent Payments I: "One Address, No Trail"

**You leave with:** your own BIP352 sender passing the official test vectors, and a failed attempt to surveil an SP address.
**Prep:** run `python3 run_vectors.py send --solution` in [labs/silent-payments](./labs/silent-payments/) · pick a public static donation address (a podcaster or open-source project) and pre-load its history on mempool.space · have Dana wallet (signet) or another SP wallet ready to show a real `tsp1...` address · skim [BIP352](https://github.com/bitcoin/bips/blob/master/bip-0352.mediawiki) "Overview" and "Creating outputs"

- 🩸 Scrape the static donation address live: every donation, every amount, when they cash out. That's what reusing an address does. Then show an SP address that has received many payments: on-chain there's nothing to link
- 🕳 The problem SP solves: you want to publish one address, but addresses shouldn't be reused. BIP47 needed a notification transaction, and xpub-sharing needed a server. SP needs neither.
  - **Analogy (paint mixing):** the sender mixes their secret color (input keys) with your public color (scan key). Only you can remake that mix from your side, so only you recognize the result
  - Walk through: `B_scan` / `B_spend`, sum of input keys, input hash (why paying the same person twice gives two different addresses), `t_k`, the x-only taproot output
  - The catch, which is S2's topic: the receiver has to *scan*
- 🛠 **BUILD THE SENDER** ([send.py](./labs/silent-payments/send.py)): 5 small functions, graded against the 28 official vectors. Pair people up, and let the room race to 28/28. Anyone who finishes early reads `txin.py` and explains to the room why P2WSH multisig inputs don't count
- 🔍 [bitcoin/bitcoin#36338](https://github.com/bitcoin/bitcoin/pull/36338) *BIP-352: fix P2PKH pubkey extraction from malleated scriptSig*. It's small, it's live, and it maps directly onto lab vector 21. Questions for the room: what did the old code do, and what would happen to a payment if sender and receiver disagreed here?
- 📜 BIP352 "Motivation". Read it like scripture, argue about it like heretics: does SP make the reuse problem go away, or just move it somewhere else?
- 🎯 Finish the lab to 28/28 · or test Dana/Shroud on signet and file one well-documented bug or UX issue · or read [bdk-sp#55](https://github.com/bitcoindevkit/bdk-sp/issues/55) and check whether vector 27 covers it

## S2 · Silent Payments II: "Finding Your Money"

**You leave with:** a working scanner, a number for "how long to scan a day of mainnet", and an opinion on who should do that work.
**Prep:** `python3 run_vectors.py receive --solution` and `python3 scan_benchmark.py` · read the [BIP352 index server spec](https://github.com/silent-payments/BIP0352-index-server-specification) · know the three scanning models below well enough to draw them · optional: a signet BlindBit Oracle or Frigate instance to demo

- 🩸 "Your phone has to do *what*?" Receiving SP means checking every eligible transaction on the chain. Run the benchmark live, then scale it: a year offline equals X hours of catch-up
- 🕳 Three ways to scan, each with its own privacy trade-off:
  1. **Your own full node** (Bitcoin Core receiving PR, kernel-node): private, but heavy
  2. **Download tweaks** from an indexer (BlindBit Oracle, Shroud's indexer, Dana): the server only learns that you're an SP user, and you do the ECDH yourself. Pair this with BIP158 filters so you don't reveal which outputs matched (bridge to S7)
  3. **Hand your scan key to a server** (Frigate, with ephemeral keys held in RAM): fast and GPU-accelerated, but the server can see your incoming payments
  - **Analogy:** (1) you sort all the mail at the post office yourself; (2) the post office gives you a stamp for each letter and you test them at home; (3) you give the postman a key that opens only your letters, which saves time, and he can read them
  - Labels: one wallet, many distinguishable addresses, still one scan
- 🛠 **BUILD THE SCANNER** ([receive.py](./labs/silent-payments/receive.py)): tweak, scan loop, then labels and spend keys as stretch goals. The grader catches the two classic bugs (checking outputs by position, stopping after the first match). Finish with `scan_benchmark.py` and compare laptops
- 🔍 [bitcoin-core/secp256k1#1912](https://github.com/bitcoin-core/secp256k1/pull/1912) *silentpayments: add light client API*. Which of our three models is this API for? Or, from our own community: [Shroud](https://github.com/CypherCommons/shroud) (Chaitika's wallet) and [kernel-node#50](https://github.com/kernel-node/kernel-node/pull/50) (Peter's SP scanning, merged)
- 📜 Satoshi, whitepaper §10 "Privacy": "keeping public keys anonymous." How far did we drift, and does SP bring us back?
- 🎯 [shroud#132](https://github.com/CypherCommons/shroud/issues/132): unit tests for its Rust BIP-352 scanner (you just learned what to test) · or run BlindBit Oracle on signet and write up the setup · or take on [danawallet#466](https://github.com/cygnet3/danawallet/issues/466) (the output-ambiguity research issue) if you finished the labels stretch

## S3 · Silent Payments III: Review Club, "Silent Payments Land in Core"

**You leave with:** a Bitcoin Core branch built, the BIP352 unit tests run, and a written review of real SP code.
**Prep:** this is a [Review Club](https://github.com/code-orange-dev/code-orange-dev/blob/main/privacy-contributor-program/REVIEW_CLUB.md) session, so announce the PR **one week ahead** and ask people to build it beforehand. Candidates, in order of approachability: [#35301](https://github.com/bitcoin/bitcoin/pull/35301) (merged BIP352 core logic, good for learning the layout), [#35302](https://github.com/bitcoin/bitcoin/pull/35302) (sending, open), [#32966](https://github.com/bitcoin/bitcoin/pull/32966) (receiving, open). Read the [tracking issue #28536](https://github.com/bitcoin/bitcoin/issues/28536). Have a pre-built node ready for people whose builds failed

This session replaces the usual beats with the Review Club format:
- **Context (10):** why SP in Core took three years, and the "take 2" story: first-generation PRs were rebuilt on the libsecp256k1 module ([#1765](https://github.com/bitcoin-core/secp256k1/pull/1765)). What does that ordering tell you about how Core de-risks cryptography?
- **Participants explain (15):** someone who did S1 maps `send.py` to `src/common/bip352.cpp`. Where do `a_sum`, `input_hash` and `t_k` live? Spot the same test-vector file the lab uses in `src/test/data/`
- **Test evidence (15):** compare build/test results across machines. Did everyone's `test_bitcoin --run_test=bip352_tests` pass? On the open PRs, which tests did they add?
- **Conceptual review (25):** what's in scope and what's deferred (labels, wallet integration)? What would you want tested before this reaches users? Where could sender and receiver disagree?
- **Code/test review (15):** pick one function per pair and read it line by line
- **Upstream action (10):** decide together whether anything is worth posting. A tested-on-platform report with exact steps usually is. If nothing is, that's fine. Record the evidence either way
- 🎯 Keep a running review on the open SP PR through the season; carry your notes to S12

## S4 · Think Like the Adversary: "You Are Being Watched"

**You leave with:** the 5 chain-analysis heuristics, a threat model you can reuse, and the ability to name a wallet from raw hex.
**Prep:** make 3 signet transactions from different wallets beforehand (Sparrow, Electrum, Bitcoin Core, bdk-cli) · pick a real deanonymization case on mempool.space · start the shared fingerprint-table doc · 1-2 [BDK](https://github.com/bitcoindevkit/bdk_wallet) or [rust-bitcoin](https://github.com/rust-bitcoin/rust-bitcoin) tx-construction PRs

- 🩸 Walk through a real deanonymization live: one address reuse exposes a whole life. Then put two near-identical transactions on screen. By the end of the night the room can tell them apart, and so can Chainalysis
- 🕳 The reusable framework: **Adversary → Observations → Heuristics → Leakage → Mitigation → Trade-offs**. Heuristics: common-input-ownership, address reuse, round amounts, change detection, wallet fingerprints (nLockTime/anti-fee-sniping, nSequence/RBF, input/output ordering, version, script types). **Analogy:** handwriting analysis on envelopes
- 🛠 **HUNT EACH OTHER:** the room plays analyst on your 3 planted txs: find the change, guess the wallet, trace the money. Then everyone dumps their own wallet's tx hex into the shared fingerprint table. The table grows every season. Solo warm-up: [chain-analysis lab](./labs/chain-analysis/)
- 🔍 A tx-construction PR: "does this change what a transaction looks like on-chain?"
- 📜 Hughes, *A Cypherpunk's Manifesto* (1993): "Privacy is the power to selectively reveal oneself to the world"
- 🎯 Add a wallet row to the fingerprint table with evidence · or run the heuristics on one of your own old txs and write up what leaked (only if you want to share)

## S5 · Coin Selection & Change: "Coins Have Memories"

**You leave with:** labeled UTXOs and a healthy fear of careless merging.
**Prep:** Sparrow on signet with a funded wallet · the frozen-funds story · 2 [BDK](https://github.com/bitcoindevkit/bdk_wallet) coin-selection PRs · one merged Code Orange BDK PR to show

- 🩸 An exchange freezes a user because of where their coins were 3 hops ago
- 🕳 UTXOs are coins with memories, and coin selection chooses which past life to reveal. Algorithms (largest-first, BnB, random) trade fees against privacy. Changeless transactions, labels as self-defense, BIP329 label export
- 🛠 **BREAK IT ON PURPOSE:** label every UTXO, freeze one, force selections. Then merge two labeled identities and watch the damage. Then run the [coin-selection lab](./labs/coin-selection/) and try to beat BnB on privacy without losing on fees
- 🔍 BDK coin-selection PRs. Show [Muhammad's merged audit fixes](https://github.com/bitcoindevkit/bdk_wallet/pull/471): normal people do this
- 📜 Hal Finney on privacy expectations
- 🎯 A BDK beginner issue from the [pool](./ISSUE_POOL.md) · or a test report on an open coin-selection PR

## S6 · Payjoin: "Paying Together"

**You leave with:** a payjoin done in pairs and a broken heuristic.
**Prep:** `payjoin-cli` working on signet (test it yourself first!) · 1 pre-picked [rust-payjoin](https://github.com/payjoin/rust-payjoin) PR for swarm review · beginner-issue list open

- 🩸 The analyst's crown jewel (all inputs belong to one owner) and the transaction type that poisons it for everyone, including people who never use it
- 🕳 BIP78 (sync, the receiver runs a server) vs BIP77 (async, via an untrusted directory with OHTTP). **Analogy:** both people put cash on the restaurant table. Where it ships today: [payjoin.org](https://payjoin.org) lists wallets
- 🛠 **PAYJOIN IN PAIRS:** one person sends, one receives, then swap roles. Inspect the tx and point at the lie it tells
- 🔍 The friendliest repo we know: 4 Code Orange contributors have merged here (Arowolo, Vaan, Mwihoti). Swarm-review one PR
- 📜 Adam Back: privacy has to be default and boring to win
- 🎯 A rust-payjoin beginner issue from the [pool](./ISSUE_POOL.md). Docs count ([#865 `cargo doc` improvements](https://github.com/payjoin/rust-payjoin/issues/865))

## S7 · Light Clients & Your Own Node: "Don't Trust, Verify, Privately"

**You leave with:** your own node syncing, and your wallet pointed at it.
**Prep:** build [Floresta](https://github.com/getfloresta/Floresta) yourself first and note the gotchas · run the [filters lab](./labs/compact-block-filters/) · sats for the race · 2 Floresta/[Kyoto](https://github.com/2140-dev/kyoto) PRs

- 🩸 What your light wallet tells the server: every address, your IP, your balance, your timing
- 🕳 Using someone else's node means a stranger knows your net worth. BIP37 bloom filters leaked; BIP157/158 compact filters flip the model; Utreexo makes a full node light. **Analogy:** telling the librarian every book you want vs taking the catalog home. Tie-in to S2: filters are how an SP light client fetches only the blocks it needs without saying which
- 🛠 **NODE RACE:** build and run Floresta live, and the first to sync wins sats. Connect a wallet to YOUR node. Faster finishers: the filters lab
- 🔍 Floresta: welcoming maintainers and a real good-first-issue culture
- 📜 "Don't trust, verify": what it actually asks of us
- 🎯 A Floresta beginner issue ([#799 RPC docs](https://github.com/getfloresta/Floresta/issues/799) is ideal after tonight) · or turn tonight's setup pain into a docs PR

## S8 · The Network Sees You: "Tor, BIP324, Private Broadcast, ASmap"

**You leave with:** your node's traffic inspected, your broadcasts made private, and a map of your network exposure.
**Prep:** Bitcoin Core **31.x** with Tor configured · Wireshark · an AS-lookup tool · read the 31.0 release notes on `-privatebroadcast` and embedded asmap · 2 [peer-observer](https://github.com/peer-observer/peer-observer) PRs · the May quote

- 🩸 Research tracing transactions to originating IPs through listener networks: your ISP identity glued to your coins. Then the eclipse attack as a heist: replace everyone a node talks to and show it a fake world
- 🕳 How transactions propagate, who's listening, and the three layers of defense that shipped:
  - **BIP324** encrypted transport (hides content from your ISP, not from peers)
  - **`-privatebroadcast`** (Core 31): your own transactions go out only via short-lived Tor/I2P connections, one tx per connection
  - **`-asmap=1`** (Core 31, embedded map, off by default): spread your peers across networks so no single operator surrounds you. **Analogy:** never send all your messengers out the same gate
- 🛠 **WIRETAP YOURSELF:** Wireshark plaintext v1 vs BIP324. Enable `-privatebroadcast`, send a signet tx, inspect `getprivatebroadcastinfo`. Pull `getpeerinfo`, count peers sharing one AS, enable `-asmap=1`, compare diversity
- 🔍 peer-observer: our own Razor has 4 merged PRs here, so review with "what does this detect?" glasses. Or an open private-broadcast follow-up in Core (e.g. [#34322](https://github.com/bitcoin/bitcoin/pull/34322), [#34533](https://github.com/bitcoin/bitcoin/pull/34533))
- 📜 May, *The Crypto Anarchist Manifesto* (1988). Debate: "the network layer is Bitcoin's soft underbelly." Overblown or underrated?
- 🎯 A peer-observer beginner issue · or publish your AS-diversity check as a guide · or a tested-on-platform report on a private-broadcast PR

## S9 · Breaking the Trail: "CoinJoin & OpenSwap"

**You leave with:** a dissected real CoinJoin, a post-mix hygiene checklist, and an atomic swap on regtest.
**Prep:** pick a historical CoinJoin tx to autopsy · Samourai case summary · run the [openswap](https://github.com/citadel-foss/openswap) regtest framework yourself (makerd + taker) · Belcher's CoinSwap design post

- 🩸 The Samourai prosecution: what exactly is being fought over? Then: following the money works because money has one trail. Tonight we look at two ways to cut it
- 🕳 **CoinJoin:** identical envelopes in a box. Equal outputs, anonymity sets, coordinator risk, JoinMarket's maker/taker market as the trustless answer. **Swaps:** trade coin histories with a stranger, like swapping gift cards. On-chain it looks like two boring unrelated payments, and it doesn't look like mixing at all. Fidelity bonds stop Sybils (both JoinMarket and OpenSwap use them)
- 🛠 **AUTOPSY + SWAP:** (15 min) count a real CoinJoin's anonymity set, then find the post-mix mistakes that un-mixed people's coins. (15 min) pairs run makerd + taker on regtest and complete a swap. Challenge: prove a swap happened at all
- 🔍 [JoinMarket](https://github.com/JoinMarket-Org/joinmarket-clientserver) (a deep good-first-issue list) or openswap (a young repo where reviews genuinely matter)
- 📜 Debate: "Using a mixer: moral act, neutral act, or red flag?" Steelman all three
- 🎯 A JoinMarket beginner issue · or write tonight's openswap walkthrough as docs · or the post-mix hygiene checklist

## S10 · Lightning Privacy: "Lightning Doesn't Fix This"

**You leave with:** a probed channel, a traced hop, and a blinded path that beat both.
**Prep:** regtest LN setup with 3+ nodes (Polar is fastest) · a BOLT11 invoice and a BOLT12 offer ready · [LDK](https://github.com/lightningdevkit/rust-lightning)/[ldk-node](https://github.com/lightningdevkit/ldk-node)/Core Lightning offers PRs

- 🩸 "Just use Lightning for privacy." Then show balance probing and a traced payment
- 🕳 What it hides: amounts from the chain. What it leaks: channels are public UTXOs, balances can be probed, invoices link identities, and your node pubkey is a fingerprint. Fixes in progress: BOLT12 offers, blinded paths, unannounced channels, splicing
- 🛠 **LEAK COMPARISON:** pay a BOLT11 invoice and list what each hop learned. Then pay a BOLT12 offer with a blinded path and compare line by line
- 🔍 ldk-node BOLT12 interop tests or Core Lightning offers (Gradale's territory)
- 📜 Debate: "Layer 2 inherits layer 1's sins"
- 🎯 An LDK/CLN docs or test issue on offers/blinded paths

## S11 · Ecash: "Blind Signatures, Community Custody"

**You leave with:** ecash minted, sent and redeemed on a test mint, plus a clear picture of what you traded away for that privacy.
**Prep:** a signet/testnut Cashu mint (or a local `cdk-mintd`) and a Fedimint test federation (Code Orange's Bali federation experience helps here) · wallets installed · 1-2 [cdk](https://github.com/cashubtc/cdk) or [Fedimint](https://github.com/fedimint/fedimint) PRs

- 🩸 The mint knows it issued 1,000 sats and later redeemed 1,000 sats. It can't tell they were the same person, and that's the whole trick
- 🕳 Chaumian blind signatures in 5 minutes. **Analogy:** signing a sealed envelope through carbon paper. Cashu (single mint) vs Fedimint (federated guardians). The trade: you get excellent privacy from the mint, and you give up self-custody. Who is this for? Remittances, community savings, onboarding
- 🛠 **MINT, SEND, REDEEM:** mint tokens, send them over a chat message, redeem them. Then play the mint operator: what do your logs actually show?
- 🔍 A cdk or Fedimint PR touching privacy or the wallet
- 📜 Chaum, *Security without Identification* (1985), the paper that started it
- 🎯 A cdk/Fedimint docs or test issue · or a local-language guide to ecash for your community

## S12 · Contribution Sprint: "Ship It"

**You leave with:** something real submitted upstream tonight, whether that's code, a test report or a review that passed the checklist.
**Prep:** the season scoreboard (reviews, test reports, issues and PRs, with names on screen if people opted in) · a curated board of verified-open issues from the [pool](./ISSUE_POOL.md) · sats budget · the Hughes closing quote

- 🩸 The scoreboard: everything the room shipped this season, including the reviews and test reports, not just PRs
- 🛠 **THE SPRINT (60 min):** pick from the board (SP scanner tests for Shroud, rust-payjoin, Floresta, Kyoto, BDK, peer-observer, JoinMarket, openswap, cdk), pair up, and ship it live. Facilitators float and sats flow
- 🔍 Everyone reviews someone else's draft against the [PR checklist](./PR_CHECKLIST.md) before it goes upstream
- 📜 Hughes' closing lines, read AFTER the sprint: "Cypherpunks write code"
- 🎯 Vote on Season Two topics. Strong contributors: talk to us about the [Review Club and fellowship](https://github.com/code-orange-dev/fellowships)

---

## Season Two candidates (the room votes at S12)

- BIP324 deep-dive: build a v2 transport handshake (Razor's [bip324-mitm](https://github.com/RazorBest/bip324-mitm) as a reference)
- BIP375/BIP374: Silent Payments with PSBTs and hardware wallets (DLEQ proofs)
- Stratum V2 and miner privacy
- Mempool privacy, RBF and fee fingerprinting
- Nostr key hygiene for Bitcoiners
- Taproot, MuSig2 and FROST: multisig that looks like singlesig
- Build our own privacy-scoring tool (original code!)
- The Exit: BTCPay Server and merchant privacy

---

## Why these repos

Newcomers see our own people's merged code in almost every repo. rust-payjoin (4 CO contributors merged) · Shroud (Chaitika) · kernel-node and Bitcoin Core SP (Peter) · peer-observer (Razor, 4 merged) · BDK (Vaan, Muhammad) · LDK and Core Lightning (Gradale, Psychemist) · Floresta · Kyoto · openswap · JoinMarket · cdk. Anything that goes upstream passes the [PR checklist](./PR_CHECKLIST.md). Live targets are in the [issue pool](./ISSUE_POOL.md).

*Privacy isn't something you wait for. It's something you ship.* 🟠
