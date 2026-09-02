# The Privacy Sessions - Biweekly Cypherpunk Hangouts

**90 minutes. Every two weeks. Hands-on, discussion-driven, contribution-first.**

- Not a lecture series. A hangout for privacy-minded, cypherpunk Bitcoiners
- Every session: get hands dirty with a real privacy tool, then review a real open PR together, live
- You leave every session having done something that matters on a real repo
- Drop in any session. No prerequisites, no sequence, no registration guilt
- Cameras optional. Curiosity mandatory. Testnet always

---

## The Format - same rhythm every session

| Segment | Time | What happens |
|---|---|---|
| 🩸 The Cold Open | 10 min | True surveillance story. Real people deanonymized, traced, robbed, or arrested via chain analysis. Sets stakes, sparks the first argument |
| 🕳 The Rabbit Hole | 15 min | Tonight's concept in plain language plus one analogy. Whiteboard energy, no slide walls |
| 🛠 Hands-On | 30 min | Everyone does the thing live on their own machine. Facilitator screen-shares, room follows, chaos welcome |
| 🔍 The Review Circle | 20 min | Open a live PR on a privacy repo. Read the diff together. Ask: what changes, what could break, what would I ask the author? At least one person posts a real review comment before the segment ends |
| 📜 Cypherpunk Corner | 10 min | Read a short primary text aloud. Argue about it |
| 🎯 The Bounty Board | 5 min | Claim homework: a curated review, issue, or tiny PR. Sats bounties for completions |

**The one metric:** review comments + PRs posted by the room per session. Goes straight on the [PR dashboard](https://github.com/code-orange-dev/PR-tracking-dashboard).

**Facilitator rule:** you are the host of a hangout, not a professor. Don't know something? Say so and read the code together. That IS the lesson.

---

# SEASON ONE - 12 Sessions (Oct/Nov start, ~6 months)

---

## S1 · "You Are Being Watched" - Chain Analysis Night

**You leave with:** the 5 surveillance heuristics in your bones, and your first diff read.

- 🩸 **Cold Open:** walk a real deanonymization on mempool.space, live. One address reuse, whole life exposed
- 🕳 **Rabbit Hole:** the 5 heuristics analysts use
  - common-input-ownership, address reuse, round amounts, change detection, wallet fingerprinting
  - analogy: watching strangers at a market through binoculars
- 🛠 **Hands-On: HUNT EACH OTHER**
  - facilitator posts 3 testnet transactions made before the session
  - room plays analyst: find the change, guess the wallet, trace the money
  - first correct trace wins sats
- 🔍 **Review Circle:** [mempool](https://github.com/mempool/mempool) or [BDK](https://github.com/bitcoindevkit/bdk_wallet) open PR. Tonight's goal: learn to read a diff, one brave soul posts a comment
- 📜 **Cypherpunk Corner:** Eric Hughes, *A Cypherpunk's Manifesto* (1993). "Privacy is the power to selectively reveal oneself to the world"
- 🎯 **Bounty:** run the 5 heuristics on one of your own old transactions. Report what you leaked (voluntarily!)

---

## S2 · "Your Wallet Has Handwriting" - Fingerprinting Night

**You leave with:** the ability to tell which wallet made a transaction from raw hex.

- 🩸 **Cold Open:** two identical-looking transactions on screen. By night's end the room can tell them apart. So can Chainalysis
- 🕳 **Rabbit Hole:** wallet "handwriting"
  - nLockTime values, RBF signaling, input ordering (BIP69 or not), version bytes
- 🛠 **Hands-On: BUILD THE FINGERPRINT TABLE**
  - everyone makes a testnet tx with a different wallet (Sparrow, Electrum, Cake, bdk-cli)
  - dump raw hex, compare side by side
  - build the room's shared fingerprint table, keep it forever, grow it every season
- 🔍 **Review Circle:** [rust-bitcoin](https://github.com/rust-bitcoin/rust-bitcoin) PR touching tx construction. Ask: does this change what a tx looks like on-chain?
- 📜 **Cypherpunk Corner:** Satoshi's whitepaper, section 10 (Privacy). The original model and exactly where it broke
- 🎯 **Bounty:** add a wallet row to the fingerprint table, or file one fingerprint docs issue upstream

---

## S3 · "Coins Have Memories" - UTXO & Coin Control Night

**You leave with:** labeled UTXOs and a visceral fear of merging them carelessly.

- 🩸 **Cold Open:** the frozen-funds story. Exchange blocks a user because of where their coins were 3 hops ago
- 🕳 **Rabbit Hole:**
  - UTXOs are physical coins with memories
  - coin selection = choosing which of your past lives to reveal
  - labels are self-defense
- 🛠 **Hands-On: BREAK IT ON PURPOSE**
  - Sparrow on testnet: label every UTXO, freeze one, force a specific coin selection
  - then deliberately merge two labeled identities and watch the damage on-chain
- 🔍 **Review Circle:** [BDK](https://github.com/bitcoindevkit/bdk_wallet) coin selection PRs
  - show one merged Code Orange PR here (Muhammad's audit fixes) as proof that normal people do this
- 📜 **Cypherpunk Corner:** Hal Finney's early posts on privacy expectations
- 🎯 **Bounty:** curated BDK docs/test issue, or async review of one open coin-selection PR

---

## S4 · "One Address to Rule Them All" - Silent Payments Night

**You leave with:** a silent payment sent and a failed attempt to trace one.

- 🩸 **Cold Open:** scrape a podcaster's static donation address live, show the room their entire financial history. Then show a silent payments address: nothing
- 🕳 **Rabbit Hole:** BIP352 via the paint-mixing analogy
  - sender's secret color + your public color = an address only you can detect
  - no interaction, no reuse, no trail. Catch: the receiver must scan
- 🛠 **Hands-On: FAIL TO SURVEIL EACH OTHER**
  - generate SP addresses, pay each other on testnet
  - then try to link the payments on-chain. The failure is the demo
- 🔍 **Review Circle:** [shroud](https://github.com/CypherCommons/shroud) (Chaitika's SP wallet, our own community) or [rust-silentpayments](https://github.com/cygnet3/rust-silentpayments)
  - the PR author might literally be in the call
- 📜 **Cypherpunk Corner:** BIP352 motivation section. Read the spec like scripture, argue like heretics
- 🎯 **Bounty:** test shroud, file a real bug or UX issue, or review an open SP PR

---

## S5 · "Paying Together" - Payjoin Night

**You leave with:** a payjoin completed in pairs and a poisoned surveillance heuristic.

- 🩸 **Cold Open:** the analyst's crown-jewel assumption (all inputs = one owner) and the transaction type that quietly poisons it for everyone, even non-users
- 🕳 **Rabbit Hole:** BIP78 sync payjoin, BIP77 async payjoin
  - analogy: both people put cash on the restaurant table before paying
- 🛠 **Hands-On: PAYJOIN IN PAIRS**
  - payjoin-cli on signet, one sends, one receives, swap roles
  - inspect the final tx together: point at the lie it tells analysts
- 🔍 **Review Circle:** [rust-payjoin](https://github.com/payjoin/rust-payjoin)
  - friendliest repo we know: 4 Code Orange contributors already merged (Arowolo, Vaan, Mwihoti)
  - swarm-review tonight's pre-picked open PR
- 📜 **Cypherpunk Corner:** Adam Back on why privacy tech must be default and boring to win
- 🎯 **Bounty:** everyone claims one rust-payjoin good-first-issue. Docs count

---

## S6 · "Don't Trust, Verify - Privately" - Run Your Node Night

**You leave with:** your own node syncing and your wallet pointed at it.

- 🩸 **Cold Open:** what your light wallet tells the server: every address, your IP, your balance, your timing. You are the product
- 🕳 **Rabbit Hole:**
  - someone else's node = a stranger knows your net worth
  - full node vs compact block filters (BIP157/158) vs Utreexo
  - analogy: fetch the catalog and look it up yourself vs telling the librarian everything you read
- 🛠 **Hands-On: NODE RACE**
  - build and run [Floresta](https://github.com/vinteumorg/Floresta) live, light enough for a laptop
  - first synced node wins sats
  - connect a wallet to YOUR node before the segment ends
- 🔍 **Review Circle:** Floresta open PRs (welcoming maintainers, real good-first-issue culture) or [Kyoto](https://github.com/rustaceanrob/kyoto)
- 📜 **Cypherpunk Corner:** "Don't trust, verify." Trace the phrase, then ask what it demands of us in practice
- 🎯 **Bounty:** Floresta good-first-issue, or turn tonight's setup pain into a docs PR

---

## S7 · "The Network Sees You" - P2P Privacy Night

**You leave with:** your node traffic inspected and rerouted over Tor.

- 🩸 **Cold Open:** research tracing transactions to originating IPs via listener nodes. Your ISP identity glued to your coins
- 🕳 **Rabbit Hole:**
  - how transactions propagate and who is listening (companies run listener networks)
  - Dandelion++, Tor, BIP324 encrypted transport, and why broadcast privacy is still unsolved
- 🛠 **Hands-On: WIRETAP YOURSELF**
  - Wireshark your own node's traffic, plaintext vs BIP324 encrypted
  - then route the node over Tor and compare what an observer sees
- 🔍 **Review Circle:** [peer-observer](https://github.com/peer-observer/peer-observer)
  - 0xB10C's monitoring tool where our own Razor has 4 merged PRs
  - review with "what does this let us detect?" glasses
- 📜 **Cypherpunk Corner:** Tim May, *The Crypto Anarchist Manifesto* (1988). "The State will of course try to slow the spread of this technology..."
- 🎯 **Bounty:** peer-observer issue, or document your Tor node setup as a guide

---

## S8 · "Mixing Without Trust" - CoinJoin Night

**You leave with:** a dissected real CoinJoin and a post-mix hygiene checklist.

- 🩸 **Cold Open:** the Samourai prosecution. What exactly is being fought over when mixing meets the state
- 🕳 **Rabbit Hole:**
  - CoinJoin via the identical-envelopes-in-a-box analogy
  - why equal outputs matter, why coordinators are the weak point
  - JoinMarket's maker/taker market as the trustless answer
- 🛠 **Hands-On: AUTOPSY A COINJOIN**
  - dissect a real historical CoinJoin on-chain
  - count the anonymity set, then find the post-mix spending mistakes that unmixed people's coins
  - lesson: privacy is a practice, not a purchase
- 🔍 **Review Circle:** [JoinMarket](https://github.com/JoinMarket-Org) ecosystem PRs, or coinjoin-detection code in analysis tools. Know thy enemy
- 📜 **Cypherpunk Corner:** DEBATE NIGHT. "Using a mixer: moral act, neutral act, or red flag?" Steelman all three
- 🎯 **Bounty:** write the room's post-mix hygiene checklist as a repo doc, or review an open JoinMarket PR

---

## S9 · "Cash, Digitally" - Ecash Night

**You leave with:** tokens minted, sent, melted, and a 1982 paper that predicted it all.

- 🩸 **Cold Open:** our own Bali Fedimint federation. Restaurants, drivers, street vendors. Some of us live on this
- 🕳 **Rabbit Hole:** Chaumian blind signatures
  - analogy: the mint signs through a carbon-paper envelope, validating what it cannot see
  - honest tradeoff stated plainly: custody risk in exchange for perfect payer privacy
- 🛠 **Hands-On: RUN A MINT**
  - spin up a Cashu mint on testnet, everyone mints, sends, melts
  - try to surveil each other's payments and fail
  - compare with an on-chain payment made the same minute
- 🔍 **Review Circle:** [Cashu](https://github.com/cashubtc) (Dayvvo contributed to cashu-ts) or [Fedimint](https://github.com/fedimint/fedimint) open PRs
- 📜 **Cypherpunk Corner:** David Chaum, *Blind Signatures for Untraceable Payments* (1982). This fight is older than most of the room
- 🎯 **Bounty:** Cashu/Fedimint good-first-issue, or file UX feedback from tonight's mint chaos

---

## S10 · "Lightning Doesn't Fix This" - Lightning Privacy Night

**You leave with:** a probed channel, a traced hop, and a blinded path that beat both.

- 🩸 **Cold Open:** "just use Lightning for privacy." Then show a balance-probing attack and a payment traced through a hop
- 🕳 **Rabbit Hole:** what LN hides vs leaks
  - hides: amounts from the chain
  - leaks: channels are public UTXOs, balances are probeable, invoices link identity
  - the fix in progress: BOLT12 offers + blinded paths
- 🛠 **Hands-On: LEAK COMPARISON**
  - on regtest/signet LN: pay a BOLT11 invoice, list what each hop learned
  - then a BOLT12 offer with a blinded path, compare the leak surface line by line
- 🔍 **Review Circle:** [LDK](https://github.com/lightningdevkit/rust-lightning) / ldk-node BOLT12 PRs (Gradale's territory) or Core Lightning offers PRs
- 📜 **Cypherpunk Corner:** "Layer 2 inherits layer 1's sins." Attack or defend
- 🎯 **Bounty:** LDK/CLN docs or test issue around offers and blinded paths

---

## S11 · "The Exit" - Selling & Spending Privately Night

**You leave with:** a BTCPay store running with payjoin enabled, end to end.

- 🩸 **Cold Open:** KYC breach dumps: names, addresses, balances, leaked and sold. The $5-wrench threat model is not hypothetical
- 🕳 **Rabbit Hole:** the full lifecycle, and the rule that privacy fails at the weakest link
  - earn: silent payments
  - hold: your node + coin control
  - spend: payjoin, ecash
  - exit: P2P, merchant self-custody
- 🛠 **Hands-On: OPEN A STORE**
  - deploy BTCPay Server (or use the shared instance), enable payjoin
  - roleplay merchant and customer, complete a private sale
  - bonus: point it at your Floresta node from S6
- 🔍 **Review Circle:** [BTCPay Server](https://github.com/btcpayserver/btcpayserver) privacy/payjoin PRs
- 📜 **Cypherpunk Corner:** the room writes its own manifesto, one sentence per person, live doc, kept forever
- 🎯 **Bounty:** BTCPay docs issue, or bring a friend's privacy setup to roast next session

---

## S12 · "Ship It" - Contribution Sprint Finale

**You leave with:** something real submitted upstream, tonight.

- 🩸 **Cold Open:** the season scoreboard. Every review, issue, and PR the room shipped, names on screen, dashboard live
- 🕳 **Rabbit Hole:** none. Tonight we work
- 🛠 **Hands-On (60 min): THE SPRINT**
  - pick from the curated board: rust-payjoin, shroud, Floresta, BDK, Cashu, peer-observer
  - pair up: draft PRs, post reviews, file issues, live
  - facilitators float, sats flow
- 🔍 **Review Circle:** review each other's draft PRs before they go upstream. The quality floor in action
- 📜 **Cypherpunk Corner:** Hughes' closing lines, read AFTER the sprint, not before: "Cypherpunks write code... we're going to write it." It lands differently once you just did
- 🎯 **Bounty:** vote Season Two topics

---

## Season Two candidates (room votes at S12)

- CoinSwap and Teleport transactions
- ASmap and eclipse attacks
- BIP324 encrypted transport deep-dive
- Mempool privacy and RBF
- Nostr key hygiene for Bitcoiners
- Build our own privacy-scoring tool (original code!)
- Stratum V2 and miner privacy

---

## Operating notes

- **Repos chosen because we already have standing there**
  - rust-payjoin (4 CO contributors merged), shroud (Chaitika), peer-observer (Razor), BDK (Vaan, Muhammad), Floresta, LDK (Gradale, Psychemist)
  - newcomers see our own people's merged code in every repo: the "people like me do this" effect
- **Review > PR for newcomers**
  - a thoughtful review comment takes 20 minutes, needs no Rust, and maintainers are starved for reviewers
  - "I tested this on signet, works, one question about X" is a real contribution
  - PRs follow naturally by S4-S6
- **Curate before every session (30 min, non-negotiable)**
  - 2-3 live open PRs pre-picked for the Review Circle: small diffs, active authors, friendly repos
  - 3-5 bounty items, verified still open that morning
  - perfect Educator Fellow duty
- **Quality floor still applies**
  - anything upstream passes the [PR checklist](./PR_CHECKLIST.md)
  - reviews are kind, specific, honest. We are the program that sends prepared people
- **Opsec is modeled, not preached**
  - testnet/signet always, no real balances on screen, pseudonyms welcome, cameras optional
- **Every session is standalone**
  - open with 60 seconds of framing so a first-timer is never lost
- **Track and celebrate**
  - every review and PR goes on the [PR dashboard](https://github.com/code-orange-dev/PR-tracking-dashboard)
  - public proof of work, the Code Orange way

*Privacy isn't something you wait for. It's something you ship.* 🟠
