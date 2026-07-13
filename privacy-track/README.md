# Code Orange - Bitcoin Privacy Track

**A drop-in, drop-out program where every session ends with a real contribution to a Bitcoin privacy project.**

You do not have to attend all of this. There is no "start" and no "finish." Each session stands on its own, teaches one privacy topic completely, and guides you to open a real pull request against a real open-source privacy repository before you leave. Come to one session. Come to ten. Come when a topic interests you, skip when it doesn't. The only thing every session has in common is the goal: **you contribute.**

---

## Why this track exists

Privacy on Bitcoin matters for the same reason it matters anywhere else. Someone accepting bitcoin for their work, running a small shop, donating to a cause, or saving for the future expects the same everyday financial privacy they'd get from a bank - their landlord shouldn't see their balance, their employer shouldn't see their donations, and a stranger shouldn't be able to look up how much they hold and target them for it.

But Bitcoin's base layer is public by default. Every transaction is permanently visible to anyone. Most of the privacy weaknesses people actually hit aren't in the protocol - they're in **wallet behavior** and **how transactions get built**. That's exactly the kind of thing open-source contributors can fix. Reusing an address, picking change badly, leaking which wallet you use through subtle fingerprints, broadcasting in a way that reveals your IP - these are software problems, and software problems get solved by people sending pull requests.

That's what this track is for. Not to talk about privacy - to **ship** privacy.

---

## How this track works

- **Online and global.** Sessions run remotely. Anyone, anywhere, any timezone we can manage. You need a laptop and curiosity.
- **Standalone sessions.** Every session is self-contained. You will never be lost because you "missed last week." Each one re-teaches the small amount of context it needs.
- **Drop in, drop out.** Join any session. Leave any session. Come back next month. No attendance requirement, no sequence to follow, no graduation gate. Your progress is measured in merged PRs, not in seats filled.
- **Every session ends in a contribution.** You don't leave with notes. You leave with a pull request open against a real repository - picked from our curated issue pool (see below), run through a quick quality checklist, and submitted upstream.
- **Low barrier on purpose.** Session one can be your first day writing Rust. We've designed the contribution targets so a curious Bitcoiner can ship something real immediately and grow from there.

---

## A note for tutors

**You do not need to be a deep technical developer to teach this track.** You need to be a curious Bitcoiner who wants to build on Bitcoin. That's it. This track is as much a teaching ground for *you* as for the people in the room - you will learn this material by preparing it and by working through the exercises alongside everyone else.

Here is how to teach it well:

1. **Do the reading and the exercise yourself first.** Every session below has a "Tutor preparation" block with plain-language explanations, an analogy you can use, the questions people will ask, and how long to budget for prep. Work through the build *before* the session. If you can do it, you can teach it.
2. **Teach the WHY, not the HOW.** Your job is not to be the smartest coder in the room. Your job is to explain *why this privacy problem matters* and *where in the code it lives*. The repo's own documentation handles the HOW. Point people at it.
3. **Be honest when you don't know.** "I don't know - let's find out together" is the most powerful thing you can say. It models exactly the behavior a good open-source contributor needs. Look it up live. Read the code together. Ask in the repo's chat.
4. **Learn alongside the room.** You are not above the participants, you are one session ahead of them. That's enough. The best tutors here are people who started as participants.
5. **Protect the relationship with maintainers.** This is the one rule you must not bend. We contribute *from a curated issue pool* and we run *a quality checklist* before anything goes upstream. Read `PR_CHECKLIST.md` and make sure every participant runs it. A program that sends sloppy pull requests gets ignored; a program that sends prepared contributors gets welcomed. You are the guardian of that reputation.

If you can host a call, do the homework one session ahead, and stay curious, you can run this track.

---

## How contributing works - read this before any session

We optimize for **volume of merged pull requests** - lots of real, accepted contributions. But there's a trap: the maintainers of these privacy repos are mostly unpaid and time-starved, and the privacy world is small. If we flood them with random, low-quality PRs, "Code Orange" becomes a name they associate with noise, and doors close. So we keep volume high *and* protect the relationship with three rules:

1. **Pick from the curated pool, never the wild.** All contribution targets come from [`ISSUE_POOL.md`](./ISSUE_POOL.md) - a living list of issues we've verified are still open, genuinely wanted, and beginner-appropriate. Don't go hunting for random issues to "fix."
2. **Run the checklist before you submit.** Every PR passes [`PR_CHECKLIST.md`](./PR_CHECKLIST.md): it builds locally, tests pass, it links the issue, and it follows the repo's own CONTRIBUTING guide. Ten minutes that turns a maybe-PR into a merge.
3. **Submit directly upstream - but prepared.** Once it clears the checklist, you open the PR yourself against the real repo and engage with the maintainer's review like a real contributor. Because you are one.

The result: high throughput, defensible quality, and maintainers who are glad to see us.

---

## The repositories we contribute to

All Rust. All central to base-layer privacy. Ordered roughly easiest-to-enter first.

| Repo | What it is | Why privacy cares | Entry level |
|---|---|---|---|
| **rust-bitcoin** | The foundational Bitcoin library in Rust | Everything else is built on it; tx parsing, addresses, script all live here | 🟢 Easiest - strong good-first-issue culture |
| **Floresta** | A Utreexo-based full node in Rust | Lets people run their own node cheaply = no third party watching their wallet | 🟢 Welcoming, active |
| **BDK (bdk_wallet)** | The Bitcoin Dev Kit wallet library | Coin selection, change handling, descriptors - where wallet privacy is won or lost | 🟡 Moderate |
| **Payjoin Dev Kit (rust-payjoin)** | Library for Payjoin collaborative transactions | Breaks the assumption that all transaction inputs belong to one person | 🟡 Moderate |
| **Silent Payments tooling** | Libraries implementing BIP352 | Lets you receive to a single static address with zero address reuse | 🟡 Moderate / advanced |
| **Kyoto** | A BIP157/158 compact-block-filter light client in Rust | Light clients that don't leak which addresses are yours to a server | 🟡 Moderate / advanced |

---

## The privacy problems we're solving

Every session maps to a concrete, well-known weakness. In plain language:

| The problem | What it means for a normal person | Where we fix it |
|---|---|---|
| **Address reuse** | Reusing an address turns your whole history into one searchable profile | Silent Payments sessions |
| **Common-input-ownership** | Spending two coins together usually proves the same person owns both | Heuristics + collaborative-tx sessions |
| **Change detection** | Analysts can often guess which output is your change, then follow your money | Coin selection sessions (BDK) |
| **Wallet fingerprinting** | The *way* your wallet builds a transaction can reveal which wallet - and sometimes which user | Fingerprinting sessions (rust-bitcoin/BDK) |
| **Light-client leakage** | "Light" wallets often tell a server exactly which addresses are yours | Light-client sessions (Kyoto) |
| **Node/IP exposure** | Broadcasting a transaction can leak the IP it came from | P2P privacy + node sessions (Floresta) |
| **Network-level deanonymization** | An attacker controlling network routes can isolate or watch your node | ASmap + eclipse-attack sessions |
| **Linking on receipt** | One static donation address links every donor and every payment together | Silent Payments sessions |

---

## The sessions

These are **modules, not a sequence.** Pick whatever pulls you in. Each lists who it's for, what you'll learn in plain terms, a full tutor-preparation block, what you'll build, and the contribution you'll make.

A good first session for anyone brand new is **F1**. After that, follow your curiosity.

---

### Foundations

#### F1 · Set up your toolchain and ship your first contribution
**Who it's for:** Total newcomers. Possibly your first day writing Rust.
**What you'll learn (plain):** How to clone a Bitcoin repo, build it, run its tests, and open a pull request. The mechanics of contributing - fork, branch, commit, PR, respond to review.

**Tutor preparation** *(prep: ~90 min the first time, ~20 min after)*
- **The concept in plain words:** Contributing to open source is just five moves: copy the project (fork), make a workspace (branch), change something, save it with a note (commit), and offer it back (pull request). Everything else is detail.
- **Analogy to use:** It's like suggesting an edit to a shared recipe. You photocopy the cookbook (fork), scribble your improvement on your copy (branch + commit), and hand it to the author saying "want this?" (PR). They might say yes, or ask you to change it first.
- **Common questions and answers:**
  - *"Do I need to know Rust?"* - Not today. Today we fix a doc, a comment, or a failing-to-be-clear error message. You'll write Rust in later sessions.
  - *"What if my PR gets rejected?"* - Totally normal and not a failure. Maintainers often ask for changes. That conversation *is* contributing.
  - *"Will I break Bitcoin?"* - No. You're proposing a change to a copy. Nothing you do touches the real network or gets merged without review.
- **How to run it:** Screen-share the whole flow once, slowly, on rust-bitcoin. Then everyone does it on a curated `good-first-issue` (docs/typo/clarity issues are ideal here). Budget half the session for "my build is failing" - that's the real lesson.
- **When you get stuck:** rust-bitcoin's CONTRIBUTING.md and its chat are excellent. Reading them together is part of the teaching.

**Build:** Fork, build, and test rust-bitcoin (or Floresta) locally.
**Contribute:** Pick a `good-first-issue` from the pool (a docs/clarity/test fix) and open your first PR.

---

#### F2 · Read a Bitcoin transaction byte by byte
**Who it's for:** Anyone who wants to actually *see* where privacy leaks happen.
**What you'll learn (plain):** What's inside a transaction - inputs, outputs, amounts, scripts, locktime - and which of those fields quietly leak information.

**Tutor preparation** *(prep: ~60 min)*
- **The concept in plain words:** A transaction is just a list of "coins I'm spending" (inputs) and "where the money goes" (outputs), plus some settings. Every one of those fields is public forever, and several of them accidentally say something about you.
- **Analogy to use:** A transaction is like a cheque you photocopy and pin to a public noticeboard for all time. Most people only think about the amount - but the handwriting, the bank, the way you fill in the date, all reveal things too.
- **Common questions:**
  - *"Why are amounts public?"* - Bitcoin needs everyone to verify no money was invented. Public amounts are the price of not trusting a central bank.
  - *"What's a 'script'?"* - The little rulebook attached to each coin saying how it can be spent. Different wallets write it differently - that's a fingerprint.
- **How to run it:** Decode a real transaction together using rust-bitcoin's parsing. Point at each field and ask "what could someone learn from this?"
- **When you get stuck:** rust-bitcoin's `Transaction` docs label every field.

**Build:** A tiny Rust program using rust-bitcoin that decodes a raw transaction and prints each field.
**Contribute:** Improve the docs or examples for transaction parsing in rust-bitcoin - clarity fixes here are genuinely valued. Pick from the pool.

---

### Transaction privacy & wallet behavior

#### T1 · The five privacy heuristics
**Who it's for:** Anyone. No code required to understand it; light code to contribute.
**What you'll learn (plain):** The five rules of thumb chain-analysis firms use to deanonymize people - and how to recognize each one.

**Tutor preparation** *(prep: ~75 min)*
- **The five heuristics in plain words:**
  1. **Common-input-ownership** - if a transaction spends several coins at once, they're probably all owned by the same person. (Like paying with a fistful of bills from the same pocket.)
  2. **Address reuse** - using one address repeatedly ties all those payments into one identity. (Like using one email address for everything.)
  3. **Round amounts** - a payment of exactly 0.05 BTC is probably the *payment*; the weird leftover is probably your *change*.
  4. **Change detection** - combine the above to guess which output comes back to you, then keep following it.
  5. **Wallet fingerprinting** - the style in which a transaction is built points to a specific wallet.
- **Analogy to use:** Imagine watching people at a market through binoculars. You can't hear them, but you notice who pulls cash from the same wallet, who always uses the same stall, who gets exact change back. You'd learn a lot. That's chain analysis.
- **Common questions:**
  - *"Isn't this just for catching criminals?"* - No. The same techniques let anyone - a stalker, a thief, a nosy employer - profile an ordinary person. Privacy is normal; surveillance is the anomaly.
- **How to run it:** Walk through one real transaction and apply each heuristic out loud as a group. Let people *feel* how easy it is.
- **When you get stuck:** These are conceptual; no deep code needed to teach.

**Build:** Annotate a real transaction identifying which heuristics apply.
**Contribute:** Many privacy libraries have docs explaining these heuristics. Improve or extend that explanatory documentation in BDK or rust-bitcoin - pick from the pool.

---

#### T2 · Coin selection and change - how wallets leak
**Who it's for:** People ready for a bit of wallet logic.
**What you'll learn (plain):** How a wallet decides which coins to spend, and how that choice either protects or exposes you.

**Tutor preparation** *(prep: ~90 min)*
- **The concept in plain words:** When you spend, your wallet picks from the coins you hold (your "UTXOs"). Picking badly - grabbing more coins than needed, or producing tell-tale change - hands analysts a map. Good coin selection is quiet.
- **Analogy to use:** It's like paying with coins from a jar. If you tip the whole jar out every time, everyone sees exactly what you have and how much you got back. A careful person picks just enough.
- **Common questions:**
  - *"Why not always pick one coin?"* - Sometimes you can't; the amounts don't line up. The art is choosing to minimize what you reveal.
  - *"What's a 'change output'?"* - Coins almost never match the price exactly, so the wallet sends the leftover back to you. That leftover is the juiciest thing for an analyst.
- **How to run it:** Read BDK's coin-selection code together. You don't need to understand every line - find *where the decision is made* and discuss what each strategy reveals.
- **When you get stuck:** BDK's docs describe its coin-selection algorithms by name; read them as a group.

**Build:** Run BDK's coin selection on sample wallets and observe the change behavior.
**Contribute:** Tests and documentation around coin selection in BDK. Pick a pool issue.

---

#### T3 · Wallet fingerprinting
**Who it's for:** The curious. Moderate.
**What you'll learn (plain):** The subtle "tells" - input ordering, locktime, version numbers, fee-bumping signals - that reveal which wallet built a transaction.

**Tutor preparation** *(prep: ~90 min)*
- **The concept in plain words:** Two wallets can make a valid transaction in slightly different ways - the order they list things, a setting they flip, a number they pick. None of it affects whether it works, but it acts like handwriting: it identifies the author.
- **Analogy to use:** Two people can write the same sentence, but their handwriting, spacing, and how they cross their sevens give them away. Wallets have handwriting too.
- **Common questions:**
  - *"Why does ordering matter?"* - There's a standard (BIP69) for ordering inputs and outputs neutrally. A wallet that *doesn't* follow it stands out.
  - *"What's nLockTime/RBF?"* - Settings about when/whether a tx can be replaced. The specific values a wallet chooses are a fingerprint.
- **How to run it:** Compare transactions from two wallets side by side. Spot the differences as a group - that *is* fingerprinting.
- **When you get stuck:** rust-bitcoin exposes all these fields; the BIP69 spec is short and readable.

**Build:** A script that flags fingerprintable traits in a set of transactions.
**Contribute:** Documentation or test coverage for transaction-construction fields in rust-bitcoin. Pick from the pool.

---

### Collaborative transactions

#### C1 · Payjoin fundamentals (BIP78 / BIP77)
**Who it's for:** Anyone curious about breaking chain-analysis assumptions.
**What you'll learn (plain):** How Payjoin lets the sender *and* receiver both put inputs into one transaction, quietly destroying the "all inputs are one owner" assumption.

**Tutor preparation** *(prep: ~90 min)*
- **The concept in plain words:** Normally one transaction = one payer's coins. Payjoin has the *receiver* also add a coin of their own. Now the common-input-ownership heuristic is simply wrong - and analysts can't tell a Payjoin apart from a normal payment, so it poisons their assumptions for everyone.
- **Analogy to use:** Imagine splitting a restaurant bill where both people put cash on the table into one pile before paying. An onlooker can no longer assume all the cash came from one wallet.
- **Common questions:**
  - *"Does the receiver pay more?"* - No, the amounts net out; they just contribute an input that comes back to them.
  - *"BIP78 vs BIP77?"* - Two versions of the coordination. BIP77 (async) doesn't require both parties online at once. That's the newer, more practical direction.
- **How to run it:** Read Payjoin Dev Kit's README and trace the sender/receiver roles. Don't aim to implement it live - aim to understand the dance.
- **When you get stuck:** Payjoin Dev Kit's docs and example code are the reference.

**Build:** Run a Payjoin example transaction from the Payjoin Dev Kit examples.
**Contribute:** Docs, examples, or test fixes in rust-payjoin. Pick from the pool.

---

#### C2 · Building with Async Payjoin
**Who it's for:** People who did C1 or already grasp Payjoin.
**What you'll learn (plain):** Why "both parties online at once" is a real-world blocker, and how async Payjoin (BIP77) removes it.

**Tutor preparation** *(prep: ~90 min)*
- **The concept in plain words:** The original Payjoin needs sender and receiver online simultaneously - awkward for a shop or a donation page. Async Payjoin uses a relay so the two sides can coordinate without being online together.
- **Analogy to use:** Instead of needing both people on a live phone call, they leave messages in a shared mailbox and pick them up whenever they're around.
- **Common questions:**
  - *"Is the relay a trusted third party?"* - It coordinates but is designed not to learn or control the funds. Discuss the trust boundaries - this is a great real conversation.
- **How to run it:** Walk the async flow in the Payjoin Dev Kit. Identify each message that crosses the relay.
- **When you get stuck:** The rust-payjoin async examples.

**Build:** Trace an async Payjoin flow end to end using the library's examples.
**Contribute:** Pick an async-Payjoin-related pool issue (often docs/tests/examples).

---

#### C3 · CoinJoin and JoinMarket concepts
**Who it's for:** The conceptually curious. Light contribution.
**What you'll learn (plain):** How many people combining one big transaction breaks the link between who put money in and who took it out.

**Tutor preparation** *(prep: ~75 min)*
- **The concept in plain words:** A CoinJoin is one transaction with many participants, all with equal-sized outputs, so you can't tell whose input maps to whose output. JoinMarket adds a marketplace so makers and takers can find each other.
- **Analogy to use:** Twenty people each drop an identical envelope of cash into a box, shake it, and each takes one identical envelope out. You can't match who put in which to who took which.
- **Common questions:**
  - *"Why equal amounts?"* - Unequal amounts would let you match by size. Equality is what makes the mix work.
- **How to run it:** Conceptual walk-through plus reading project docs. Focus on the *why*.
- **When you get stuck:** Stay at the conceptual level; this session is about understanding, with documentation-level contributions.

**Build:** Diagram a CoinJoin and explain why the linkage breaks.
**Contribute:** Documentation improvements to a relevant collaborative-transaction project. Pick from the pool.

---

#### C4 · CoinSwap concepts
**Who it's for:** Those who enjoyed C3.
**What you'll learn (plain):** How swapping coins with someone else - so the coin you end up with has a totally different history - defeats following the money.

**Tutor preparation** *(prep: ~75 min)*
- **The concept in plain words:** Instead of mixing in one visible transaction, two people swap coins in a way that, on-chain, looks like two ordinary unrelated payments. The history trail is cut.
- **Analogy to use:** You and a stranger discreetly trade identical-value gift cards. Anyone tracking your original card now follows a card that was never yours.
- **Common questions:**
  - *"How is this different from CoinJoin?"* - CoinJoin is one obvious group transaction; CoinSwap aims to look like normal, separate payments. Harder to even detect.
- **How to run it:** Conceptual. Read the CoinSwap design notes together.
- **When you get stuck:** Keep it conceptual; contributions here are docs/tests.

**Build:** Diagram a CoinSwap vs. a CoinJoin and contrast their on-chain footprints.
**Contribute:** Docs/test contribution to a relevant project from the pool.

---

### Receiving privately - Silent Payments

#### S1 · Silent Payments fundamentals (BIP352)
**Who it's for:** Anyone who's ever posted a static donation address.
**What you'll learn (plain):** How you can publish *one* unchanging address and still receive every payment to a *different*, unlinkable on-chain address.

**Tutor preparation** *(prep: ~2 hrs - the math is the meat)*
- **The concept in plain words:** Normally a static address links every payment to it. Silent Payments use a shared-secret trick: the sender combines your public address with their own key to compute a fresh, unique address only you can detect and spend. You publish one thing; the chain shows many unrelated things.
- **Analogy to use (the key one):** Mixing paint. You each have a secret color. When the sender mixes their secret with your public color, they get a specific shade. You can recreate that exact shade because you know your own secret - but no onlooker can, because they're missing one of the colors. Each payment produces a different shade.
- **Common questions:**
  - *"Doesn't the sender need to talk to me?"* - No interaction needed. They derive it from your published address alone. That's the magic.
  - *"What's ECDH?"* - The "shared secret from two key pairs" math behind the paint-mixing. You don't need the equations to teach the idea - use the analogy.
  - *"What's the catch?"* - The receiver has to *scan* the chain to find payments meant for them. That's a real cost, and it's why light-client work (Kyoto) matters here.
- **How to run it:** Teach the paint analogy first, *then* show the BIP352 flow. Don't open with math or you'll lose the room.
- **When you get stuck:** BIP352 is the spec; the Rust Silent Payments crates have readable examples.

**Build:** Use a Silent Payments library to derive a payment address from a static one.
**Contribute:** Docs, examples, or tests in a Silent Payments crate. Pick from the pool.

---

#### S2 · Scanning and the light-client connection
**Who it's for:** People who did S1.
**What you'll learn (plain):** Why finding your own Silent Payments is hard, and how compact block filters make it possible without a server spying on you.

**Tutor preparation** *(prep: ~90 min)*
- **The concept in plain words:** Because each Silent Payment lands at a fresh address, your wallet must scan blocks to recognize which are yours. Doing that privately (without telling a server your addresses) is where BIP157/158 filters come in - they let you check blocks yourself.
- **Analogy to use:** Instead of asking the post office "any mail for me?" (and revealing your name), you get a tiny summary of every mailbag and check it yourself at home.
- **Common questions:**
  - *"Why not just ask a server?"* - Because then the server knows every address you own. The whole point is to not leak that.
- **How to run it:** Connect the dots between S1's scanning cost and the light-client sessions (N1). This is the bridge session.
- **When you get stuck:** BIP158 spec + Kyoto docs.

**Build:** Demonstrate filtering a block for relevant outputs.
**Contribute:** A pool issue tying Silent Payments and filters together (often in Kyoto or a SP crate).

---

### Network and node privacy

#### N1 · Light clients and compact block filters (BIP157/158)
**Who it's for:** Anyone who uses a phone wallet. Moderate.
**What you'll learn (plain):** Why most "light" wallets leak your addresses to a server, and how compact block filters fix it.

**Tutor preparation** *(prep: ~90 min)*
- **The concept in plain words:** Old light wallets (BIP37) basically told a server which addresses to watch - handing over your identity. BIP157/158 flips it: the server sends tiny *summaries* of each block, and your wallet checks them privately at home.
- **Analogy to use:** BIP37 is telling the librarian exactly which books you want so they fetch them (now they know your interests). BIP158 is getting the catalog and finding your books yourself.
- **Common questions:**
  - *"Is this slower?"* - There's more data to download, but you stop leaking your addresses. Privacy has a cost; this one's worth it.
- **How to run it:** Read Kyoto's README and find where filters are checked. Trace one block's path.
- **When you get stuck:** Kyoto docs + BIP158.

**Build:** Run Kyoto against the network and watch it sync via filters.
**Contribute:** Docs/tests/examples in Kyoto. Pick from the pool.

---

#### N2 · Run your own node privately (Floresta and Utreexo)
**Who it's for:** Anyone who wants to stop trusting someone else's node. 🟢 Welcoming.
**What you'll learn (plain):** Why running your own node is the single biggest privacy upgrade, and how Utreexo makes it light enough to be realistic.

**Tutor preparation** *(prep: ~90 min)*
- **The concept in plain words:** If you use someone else's node, they can see which addresses are yours and which transactions you broadcast. Your own node fixes that - but a normal full node is heavy. Utreexo shrinks the data you must store using a clever cryptographic accumulator, so a node can run on modest hardware.
- **Analogy to use:** Instead of keeping every receipt you've ever had (full node), you keep one cryptographic "fingerprint" that can still prove any receipt is real (Utreexo).
- **Common questions:**
  - *"Do I lose security?"* - You still verify everything yourself; you just store a compressed proof structure instead of the whole set.
- **How to run it:** Build and run Floresta together. It's an active, friendly Rust project - great for first real contributions.
- **When you get stuck:** Floresta's docs and issue tracker are beginner-friendly.

**Build:** Build and run a Floresta node.
**Contribute:** Floresta has a healthy good-first-issue flow - pick one from the pool (docs, tests, small fixes).

---

#### N3 · P2P privacy, eclipse attacks, and node fingerprinting
**Who it's for:** The networking-curious. Moderate.
**What you'll learn (plain):** How merely *connecting* to the Bitcoin network can leak your IP or let an attacker surround your node.

**Tutor preparation** *(prep: ~90 min)*
- **The concept in plain words:** When your node broadcasts a transaction, the way it spreads can hint at which IP it started from. And if an attacker controls all the peers you connect to (an "eclipse"), they can feed you a fake view of the network or watch everything you do.
- **Analogy to use:** An eclipse attack is like someone quietly replacing everyone you talk to with their own actors - you think you're seeing the world, but you're only seeing what they show you.
- **Common questions:**
  - *"How do I broadcast without leaking my IP?"* - Techniques like routing over Tor and careful peer selection. This session explains the threat; defenses are ongoing work.
- **How to run it:** Conceptual plus reading P2P/networking docs in Floresta or rust-bitcoin's networking pieces.
- **When you get stuck:** Stay conceptual; contributions are docs/tests.

**Build:** Map your node's peer connections and discuss exposure.
**Contribute:** Documentation/test contribution on P2P behavior from the pool.

---

#### N4 · ASmap - defending against network-level deanonymization
**Who it's for:** Those who did N3. Moderate.
**What you'll learn (plain):** How an attacker who controls chunks of internet infrastructure could deanonymize nodes, and how ASmap spreads your connections across independent networks to stop it.

**Tutor preparation** *(prep: ~90 min)*
- **The concept in plain words:** The internet is divided into big networks ("autonomous systems"). If all your node's connections happen to run through one network an attacker controls, they can watch or isolate you. ASmap makes your node deliberately spread its connections across *different* networks so no single operator sees them all.
- **Analogy to use:** Don't send every messenger out the same gate - if one guard is bribed, they see everything. Send them through different gates.
- **Common questions:**
  - *"Is this a real threat for normal users?"* - It's more relevant to dedicated attackers, but it raises everyone's baseline. Worth understanding.
- **How to run it:** Read how ASmap data is used in node connection logic. Conceptual + code-reading.
- **When you get stuck:** ASmap documentation and the relevant networking code.

**Build:** Explain how ASmap would change your node's peer selection.
**Contribute:** Docs/test contribution related to ASmap or peer selection from the pool.

---

## The contribution ladder

You're never stuck at one level, and you can enter at any rung:

1. **Engage** - build a repo, read its code, join its chat, understand an issue.
2. **Fix** - docs, comments, error messages, small clarity improvements. (Most first PRs.)
3. **Test** - add or improve test coverage. Maintainers love this and it teaches you the code.
4. **Build** - implement a small feature or fix a real bug from the pool.
5. **Ship** - take on a substantial issue and see it through review to merge.
6. **Lead** - curate issues for others, mentor newcomers, or become a regular contributor to a repo. (Several tutors started here.)

There's no pressure to climb. A program full of solid rung-2 and rung-3 contributions is a successful program.

---

## What success looks like

We measure four things, in order of importance:

1. **Merged PRs** - the headline. Target: 50–100 merged per year across an active group of 10–20 contributors.
2. **Merge rate** - our quality proxy. If the share of PRs that get merged drops, our quality floor is too low and we tighten the checklist. A healthy merge rate is the real sign we're respecting maintainers.
3. **Repeat contributors** - are people coming back? Drop-in is the model, but people returning is the signal that it works.
4. **Maintainer sentiment** - the leading indicator almost nobody tracks. Are maintainers glad to see Code Orange contributors? This is the asset that compounds. Guard it.

---

## In short

Show up to any session. Learn one privacy topic properly. Pick a vetted issue, run the checklist, open a real pull request. Leave having made Bitcoin a little more private for everyone - whether it's your first PR or your fiftieth.

Privacy isn't something you wait for. It's something you ship.
