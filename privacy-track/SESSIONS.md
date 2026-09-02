# The Privacy Sessions - Biweekly Cypherpunk Hangouts

**90 min. Every 2 weeks. Hands-on, discussion-driven, contribution-first.**

- A hangout for privacy-minded, cypherpunk Bitcoiners, not a lecture series
- Every session: use a real privacy tool, then review a real open PR together, live
- Drop in any session. No prerequisites, no sequence. Testnet always, cameras optional

## Season One Schedule

**Month 1**
- Session 1: Chain Analysis
- Session 2: Wallet Fingerprinting

**Month 2**
- Session 3: Coin Selection & UTXO Management
- Session 4: Silent Payments

**Month 3**
- Session 5: Payjoin
- Session 6: Light Clients (Floresta & Kyoto)

**Month 4**
- Session 7: P2P Privacy & Node Fingerprinting
- Session 8: ASmap & Network Attacks

**Month 5**
- Session 9: CoinJoin (JoinMarket)
- Session 10: OpenSwap (formerly CoinSwap)

**Month 6**
- Session 11: Lightning Privacy
- Session 12: Contribution Sprint

---

## The Format - same 6 beats, every session

| Beat | Time | What happens |
|---|---|---|
| 🩸 Cold Open | 10 | True surveillance story. Sets stakes, starts the argument |
| 🕳 Rabbit Hole | 15 | The concept, plain language, one analogy |
| 🛠 Hands-On | 30 | Everyone does it live on their own machine |
| 🔍 Review Circle | 20 | Read a live PR together. Someone posts a real review comment before it ends |
| 📜 Cypherpunk Corner | 10 | Read a short primary text aloud. Argue |
| 🎯 Bounty Board | 5 | Claim homework. Sats for completions |

**Facilitator basics (every session):**
- You're a host, not a professor. Don't know? Say so, read the code together
- Prep takes ~30 min: pick 2-3 small live PRs for the Review Circle + 3-5 bounty items, verify open that morning
- Track one metric: reviews + PRs posted by the room. Post to the [PR dashboard](https://github.com/code-orange-dev/PR-tracking-dashboard)
- Testnet/signet only. No real balances on screen. Pseudonyms welcome

---

## S1 · Chain Analysis - "You Are Being Watched"

**You leave with:** the 5 surveillance heuristics + your first diff read.
**Prep:** make 3 testnet txs beforehand (for the game) · pick a real deanonymization case on mempool.space · pick 2 PRs ([mempool](https://github.com/mempool/mempool) or [BDK](https://github.com/bitcoindevkit/bdk_wallet)) · print Hughes quote

- 🩸 Walk a real deanonymization live: one address reuse, whole life exposed
- 🕳 The 5 heuristics: common-input-ownership, address reuse, round amounts, change detection, wallet fingerprinting. Analogy: binoculars at a market
- 🛠 **HUNT EACH OTHER:** room plays analyst on your 3 planted txs. Find change, guess wallet, trace money. Sats for first correct trace
- 🔍 Learn to read a diff. One brave soul comments
- 📜 Hughes, *A Cypherpunk's Manifesto* (1993): "Privacy is the power to selectively reveal oneself"
- 🎯 Run the 5 heuristics on your own old tx. Share what you leaked (voluntarily)

## S2 · Wallet Fingerprinting - "Your Wallet Has Handwriting"

**You leave with:** ability to identify a wallet from raw hex.
**Prep:** install 3-4 wallets (Sparrow, Electrum, Cake, bdk-cli) · start a shared fingerprint-table doc · pick 2 [rust-bitcoin](https://github.com/rust-bitcoin/rust-bitcoin) tx-construction PRs

- 🩸 Two identical-looking txs on screen. By night's end the room tells them apart. So does Chainalysis
- 🕳 The tells: nLockTime, RBF flags, input ordering (BIP69 or not), version bytes
- 🛠 **BUILD THE FINGERPRINT TABLE:** everyone makes a testnet tx with a different wallet, dump hex, compare, fill the table. It grows every season
- 🔍 rust-bitcoin PR: "does this change what a tx looks like on-chain?"
- 📜 Whitepaper section 10: the original privacy model and where it broke
- 🎯 Add a wallet row to the table, or file a fingerprint docs issue upstream

## S3 · Coin Selection & UTXO Management - "Coins Have Memories"

**You leave with:** labeled UTXOs + fear of careless merging.
**Prep:** Sparrow on testnet with a funded wallet · the frozen-funds story · 2 [BDK](https://github.com/bitcoindevkit/bdk_wallet) coin-selection PRs · one merged Code Orange BDK PR to show

- 🩸 Exchange freezes a user for where coins were 3 hops ago
- 🕳 UTXOs = coins with memories. Coin selection = choosing which past life to reveal. Labels are self-defense
- 🛠 **BREAK IT ON PURPOSE:** label every UTXO, freeze one, force selections. Then merge two labeled identities and watch the damage
- 🔍 BDK PRs. Show Muhammad's merged audit fixes: normal people do this
- 📜 Hal Finney on privacy expectations
- 🎯 BDK docs/test issue, or async review of one open PR

## S4 · Silent Payments - "One Address to Rule Them All"

**You leave with:** an SP payment sent + a failed trace.
**Prep:** SP-capable wallet ready (Cake or tooling) · a public donation address to scrape live · 2 PRs from [shroud](https://github.com/CypherCommons/shroud) or [rust-silentpayments](https://github.com/cygnet3/rust-silentpayments)

- 🩸 Scrape a podcaster's static donation address: whole financial history. Then an SP address: nothing
- 🕳 BIP352, paint-mixing analogy: sender's secret color + your public color = address only you detect. Catch: receiver must scan
- 🛠 **FAIL TO SURVEIL:** pay each other via SP on testnet, then try to link payments on-chain. The failure is the demo
- 🔍 shroud is our own community's wallet (Chaitika). Author may be in the call
- 📜 BIP352 motivation section. Read like scripture, argue like heretics
- 🎯 Test shroud and file a bug/UX issue, or review an SP PR

## S5 · Payjoin - "Paying Together"

**You leave with:** a payjoin done in pairs + a poisoned heuristic.
**Prep:** payjoin-cli working on signet (test it yourself first!) · 1 pre-picked [rust-payjoin](https://github.com/payjoin/rust-payjoin) PR for swarm review · good-first-issue list open

- 🩸 The analyst's crown jewel (all inputs = one owner) and the tx type that poisons it for everyone
- 🕳 BIP78 sync, BIP77 async. Analogy: both people put cash on the restaurant table
- 🛠 **PAYJOIN IN PAIRS:** one sends, one receives, swap roles. Inspect the tx: point at the lie it tells
- 🔍 Friendliest repo we know: 4 Code Orange contributors merged (Arowolo, Vaan, Mwihoti). Swarm-review one PR
- 📜 Adam Back: privacy must be default and boring to win
- 🎯 Everyone claims one rust-payjoin good-first-issue. Docs count

## S6 · Light Clients (Floresta & Kyoto) - "Don't Trust, Verify - Privately"

**You leave with:** your own node syncing, wallet pointed at it.
**Prep:** build [Floresta](https://github.com/vinteumorg/Floresta) yourself first, note the gotchas · sats for the race · 2 Floresta/[Kyoto](https://github.com/rustaceanrob/kyoto) PRs

- 🩸 What your light wallet tells the server: every address, IP, balance, timing
- 🕳 Someone else's node = stranger knows your net worth. Filters (BIP157/158) + Utreexo. Analogy: fetch the catalog vs telling the librarian everything
- 🛠 **NODE RACE:** build and run Floresta live. First sync wins sats. Connect a wallet to YOUR node
- 🔍 Floresta: welcoming maintainers, real good-first-issue culture
- 📜 "Don't trust, verify": what it actually demands of us
- 🎯 Floresta good-first-issue, or turn tonight's setup pain into a docs PR

## S7 · P2P Privacy & Node Fingerprinting - "The Network Sees You"

**You leave with:** your node traffic inspected, then Tor-routed.
**Prep:** Wireshark installed + a node you can capture · Tor configured · 2 [peer-observer](https://github.com/peer-observer/peer-observer) PRs · May manifesto quote

- 🩸 Research tracing txs to originating IPs via listener networks. ISP identity glued to your coins
- 🕳 How txs propagate, who listens, Dandelion++, Tor, BIP324. Broadcast privacy is unsolved
- 🛠 **WIRETAP YOURSELF:** Wireshark your node plaintext vs BIP324. Then route over Tor, compare what an observer sees
- 🔍 peer-observer: our own Razor has 4 merged PRs here. Review with "what does this detect?" glasses
- 📜 May, *Crypto Anarchist Manifesto* (1988)
- 🎯 peer-observer issue, or write up your Tor setup as a guide

## S8 · ASmap & Network Attacks - "Surrounded"

**You leave with:** a map of your node's network exposure + a diversification plan.
**Prep:** a running Bitcoin Core node with peers · AS-lookup tool ready · asmap docs · 1-2 asmap/peer-selection PRs or peer-observer detection work

- 🩸 The eclipse attack as a heist: replace everyone a node talks to, show it a fake world
- 🕳 The internet = autonomous systems. One operator on all your connections can watch or isolate you. ASmap spreads peers across networks. Analogy: never send all messengers out the same gate
- 🛠 **MAP YOUR EXPOSURE:** pull your peer list, look up each AS, count peers sharing one network. Enable asmap, compare diversity before/after
- 🔍 Core asmap/peer-selection PRs, or peer-observer
- 📜 Debate: "the network layer is Bitcoin's soft underbelly." Overblown or underrated?
- 🎯 Publish your AS-diversity check as a guide, or review an asmap PR

## S9 · CoinJoin (JoinMarket) - "Mixing Without Trust"

**You leave with:** a dissected real CoinJoin + a post-mix hygiene checklist.
**Prep:** pick a historical CoinJoin tx to autopsy · Samourai case summary · [JoinMarket](https://github.com/JoinMarket-Org) PRs · debate prompts

- 🩸 The Samourai prosecution: what exactly is being fought over
- 🕳 Identical-envelopes-in-a-box analogy. Equal outputs, coordinator risk, JoinMarket's maker/taker market as the trustless answer
- 🛠 **AUTOPSY A COINJOIN:** count the anonymity set, then find the post-mix mistakes that unmixed people's coins. Privacy is a practice, not a purchase
- 🔍 JoinMarket ecosystem PRs, or coinjoin-detection code. Know thy enemy
- 📜 DEBATE: "Using a mixer: moral act, neutral act, or red flag?" Steelman all three
- 🎯 Write the post-mix hygiene checklist as a repo doc, or review a PR

## S10 · OpenSwap - "The Swap That Leaves No Trace"

**You leave with:** an atomic swap on regtest + a coin whose history isn't yours.
**Prep:** run the [openswap](https://github.com/citadel-foss/openswap) regtest framework yourself first (makerd + taker) · Belcher's CoinSwap design post · good-first-issue list

- 🩸 Following the money works because money has one trail. Tonight we cut it - on-chain it's two boring unrelated payments
- 🕳 OpenSwap (formerly CoinSwap): trustless atomic swaps. Gift-card-swap analogy: trackers now follow a card that was never yours. vs CoinJoin: swaps don't even look like mixing. Makers earn fees, takers pay, fidelity bonds stop Sybils, Tor multi-hop hides the route. Extends Belcher's teleport-transactions, now Taproot+MuSig2
- 🛠 **SWAP WITH A STRANGER:** pairs run makerd + taker on regtest, complete a swap, inspect both tx chains. Challenge: prove a swap happened at all. Struggle
- 🔍 openswap: young repo, active good-first-issue label, reviews genuinely matter
- 📜 Belcher's original CoinSwap post: the vision, then how far the code came
- 🎯 openswap good-first-issue, or write tonight's walkthrough as docs

## S11 · Lightning Privacy - "Lightning Doesn't Fix This"

**You leave with:** a probed channel, a traced hop, a blinded path that beat both.
**Prep:** regtest/signet LN setup with 3+ nodes · BOLT11 invoice + BOLT12 offer ready · [LDK](https://github.com/lightningdevkit/rust-lightning)/CLN offers PRs

- 🩸 "Just use Lightning for privacy." Then show balance probing + a traced payment
- 🕳 Hides: amounts from chain. Leaks: channels are public UTXOs, balances probeable, invoices link identity. Fix in progress: BOLT12 + blinded paths
- 🛠 **LEAK COMPARISON:** pay a BOLT11 invoice, list what each hop learned. Then BOLT12 with blinded path, compare line by line
- 🔍 LDK/ldk-node BOLT12 PRs (Gradale's territory) or Core Lightning offers
- 📜 Debate: "Layer 2 inherits layer 1's sins"
- 🎯 LDK/CLN docs or test issue on offers/blinded paths

## S12 · Contribution Sprint - "Ship It"

**You leave with:** something real submitted upstream, tonight.
**Prep:** the season scoreboard (names + numbers on screen) · curated board of verified-open issues across all repos · sats budget · Hughes closing quote

- 🩸 The scoreboard: every review, issue, PR the room shipped. Names on screen
- 🛠 **THE SPRINT (60 min):** pick from the board (rust-payjoin, shroud, Floresta, Kyoto, BDK, openswap, peer-observer), pair up, ship live. Facilitators float, sats flow
- 🔍 Review each other's drafts before they go upstream. Quality floor in action
- 📜 Hughes' closing lines, read AFTER the sprint: "Cypherpunks write code... we're going to write it"
- 🎯 Vote Season Two topics

---

## Season Two candidates (room votes at S12)

- Ecash: Fedimint and Cashu (blind signatures, our Bali federation)
- The Exit: BTCPay Server and merchant privacy
- BIP324 encrypted transport deep-dive
- Mempool privacy and RBF
- Nostr key hygiene for Bitcoiners
- Build our own privacy-scoring tool (original code!)
- Stratum V2 and miner privacy

---

## Why these repos

rust-payjoin (4 CO contributors merged) · shroud (Chaitika) · peer-observer (Razor, 4 merged) · BDK (Vaan, Muhammad) · Floresta · Kyoto · openswap · LDK (Gradale, Psychemist). Newcomers see our own people's merged code in every repo. Anything upstream passes the [PR checklist](./PR_CHECKLIST.md).

*Privacy isn't something you wait for. It's something you ship.* 🟠
