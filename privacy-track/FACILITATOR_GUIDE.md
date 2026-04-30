# Facilitator Guide — Bitcoin Privacy Developer Track

> Everything you need to run this track at your own Bitcoin dev school, hackerspace, or study group.

---

## Before You Start

### Who This Track Is For

Participants should already understand how Bitcoin transactions work at the technical level. Specifically, they should be able to explain what a UTXO is, read a simple Bitcoin Script, and understand how digital signatures authorize spending. If your participants haven't completed a foundational Bitcoin development course (like Bitcoin Dojo, Decoding Bitcoin, or Chaincode seminars), they will struggle with the material starting in Module 2.

The track is designed for groups of 5-15 participants. Smaller groups work better for the hands-on sessions; larger groups work fine for the lecture-style sessions if you break into smaller teams for exercises.

### What You Need

**Technical requirements:**
- Each participant needs a laptop with Python 3.8+ and a text editor
- Bitcoin Core installed (for regtest exercises in Modules 3-4)
- Rust toolchain installed (for Module 3 Payjoin Dev Kit and Module 4 contributions)
- Internet access for reading BIPs and browsing repos during sessions

**Environment setup (do this BEFORE the first session):**

```bash
# Create a shared regtest environment
bitcoind -regtest -daemon
bitcoin-cli -regtest createwallet "facilitator"
ADDR=$(bitcoin-cli -regtest -rpcwallet=facilitator getnewaddress)
bitcoin-cli -regtest generatetoaddress 200 $ADDR

# Verify Python exercises run
cd module-02-silent-payments/exercises/
python3 -c "from silent_payments_sender import *; print('Setup OK')"

# Verify Rust toolchain
rustc --version  # Should be 1.70+
cargo --version
```

**Room setup:**
- Projector or large screen for live coding
- Whiteboard for diagrams (elliptic curves, transaction flows, ECDH)
- Printed copies of the BIP352 and BIP77 specifications (optional but useful)

### Pacing

The track is designed for two pacing options:

| Pace | Duration | Sessions/week | Best for |
|------|----------|---------------|----------|
| Intensive | 6 weeks | 2x per week, 2-3 hours each | Full-time cohorts, bootcamps |
| Standard | 12 weeks | 1x per week, 2-3 hours each | Working developers, study groups |

Each session has more material than can be covered in one sitting. This is intentional — it's better to have too much than too little. Prioritize the exercises over the lecture content. Participants learn more by doing than by listening.

---

## Session-by-Session Plan

### Module 1: Chain Analysis & Why Privacy Matters

#### Session 1: How Bitcoin Surveillance Works (2.5 hours)

| Time | Activity | Notes |
|------|----------|-------|
| 0:00-0:20 | **Intro and context** | Why this track exists. Show the OpenSats blog post on privacy. Ask: "How many of you have reused a Bitcoin address?" |
| 0:20-0:50 | **Lecture: The four heuristics** | CIOH, change detection, address reuse clustering, timing analysis. Use whiteboard to draw example transactions. |
| 0:50-1:00 | **Break** | |
| 1:00-1:45 | **Hands-on: Chain Analysis Lab** | `exercises/chain_analysis_lab.py` — Participants work through Exercises 1-4. Walk around and help. |
| 1:45-2:15 | **Live demo: OXT.me** | Pick a real mainnet transaction and trace it live. Show how CIOH + change detection reveals the entity. |
| 2:15-2:30 | **Discussion** | Use the discussion questions from the README. Key insight: these heuristics are assumptions, not facts. Payjoin and CoinJoin exploit this. |

**Facilitator tips:**
- The chain analysis lab has 8 sample transactions designed to illustrate different patterns. TX 3 is a Payjoin (CIOH is wrong). TX 6 is a CoinJoin. Make sure participants discover this.
- If participants finish early, have them attempt Exercise 6 (entity tracing across multiple transactions).
- The reflection questions at the end are important — assign them as homework if you run out of time.

#### Session 2: Privacy as a Protocol Property (2 hours)

| Time | Activity | Notes |
|------|----------|-------|
| 0:00-0:15 | **Review homework** | Ask 2-3 participants to share their chain analysis lab results. What surprised them? |
| 0:15-0:45 | **Lecture: Greg Maxwell's 2013 post** | Read key excerpts aloud. The "birth control" example. Why privacy matters for fungibility. |
| 0:45-1:15 | **Group exercise: Privacy spectrum** | Draw a spectrum on the whiteboard: Transparent → Pseudonymous → Private → Anonymous. Have groups place different Bitcoin usage patterns on the spectrum. |
| 1:15-1:30 | **Break** | |
| 1:30-1:50 | **Lecture: Privacy improvements that help everyone** | Silent Payments, Payjoin, Taproot. The anonymity set concept. |
| 1:50-2:00 | **Assign essay** | 500-word essay: "What is the most impactful privacy improvement that could be made to Bitcoin today, and why?" Due before Session 3. |

**Facilitator tips:**
- This session is more discussion-heavy than technical. That's intentional — participants need to internalize WHY privacy matters before diving into HOW.
- If the group is technical and engaged, introduce the concept of "privacy by default vs privacy by choice" and ask them to debate which is better.
- The essay is a good filter: participants who write thoughtful essays will get the most out of the technical sessions.

---

### Module 2: Silent Payments — BIP352

#### Session 3: How Silent Payments Work (2.5 hours)

| Time | Activity | Notes |
|------|----------|-------|
| 0:00-0:15 | **Essay discussion** | Ask 2-3 volunteers to summarize their essays. Note common themes. |
| 0:15-0:30 | **Lecture: The address reuse problem** | Show a real donation address (e.g., a public Bitcoin charity). Show all incoming payments on mempool.space. "This is why we need Silent Payments." |
| 0:30-1:00 | **Lecture: ECDH and key derivation** | Use the whiteboard to draw the ECDH key exchange. Emphasize: both parties derive the same shared secret without communicating. This is the magic. |
| 1:00-1:10 | **Break** | |
| 1:10-1:30 | **Lecture: BIP352 walkthrough** | Walk through the specification step by step. Have participants follow along with the PDF/web page open. |
| 1:30-2:10 | **Whiteboard exercise: manual Silent Payment** | Work through a complete Silent Payment by hand on the whiteboard. Pick simple numbers. Compute the shared secret, the tweak, and the output key. |
| 2:10-2:30 | **Preview next session** | Show the `silent_payments_sender.py` exercise. Explain what they'll implement. Assign: read BIP352 Sections 1-3 before the next session. |

**Facilitator tips:**
- The ECDH explanation is the hardest part. Use small numbers first (e.g., G=5, private key=3, public key=15). Then relate to secp256k1.
- If the group has already done the Bitcoin Dojo ECC exercises, reference those directly.
- The whiteboard exercise is critical. Don't skip it. If participants can compute a Silent Payment by hand, the code will make sense.

#### Session 4: Implement a Minimal SP Sender (3 hours)

| Time | Activity | Notes |
|------|----------|-------|
| 0:00-0:15 | **Review: BIP352 key concepts** | Quick whiteboard recap of ECDH, scan/spend keys, shared secret derivation |
| 0:15-1:15 | **Coding: Exercises 1-3** | `silent_payments_sender.py` — Generate keypair, derive shared secret, compute output key. Walk around and help. |
| 1:15-1:25 | **Break** | |
| 1:25-2:15 | **Coding: Exercise 4** | Full Silent Payment simulation. Run tests. Debug together. |
| 2:15-2:45 | **Code review** | Have 1-2 participants share their screen and walk through their implementation. Discuss edge cases. |
| 2:45-3:00 | **Discussion** | Why sum all input keys? What about Taproot inputs? What happens with incorrect parity? |

**Facilitator tips:**
- The pure-Python ECC operations are slow. That's fine — it's for learning, not production.
- Common errors: forgetting `% N` for modular arithmetic, incorrect byte ordering for tagged hashes, confusing x-coordinate-only vs full point serialization.
- If participants finish early, challenge them to implement label support (BIP352 Section 5).

#### Session 5: Scanning and Receiving (3 hours)

| Time | Activity | Notes |
|------|----------|-------|
| 0:00-0:20 | **Lecture: The scanning problem** | "You've built the sender. Now the hard part: how does the receiver find payments?" Calculate mainnet numbers: 300K tx/day × 1 ECDH each. |
| 0:20-1:00 | **Coding: scanner exercises** | `silent_payments_scanner.py` — scan_transaction(), scan_block() |
| 1:00-1:10 | **Break** | |
| 1:10-1:50 | **Coding: benchmark** | Exercise 3 — benchmark scanning performance. Measure tx/s and extrapolate to mainnet. |
| 1:50-2:30 | **Lecture + Discussion: Making it practical** | Compact block filters (preview Module 4), light client trade-offs, Kyoto project |
| 2:30-3:00 | **Planning next session** | "Next session: you'll contribute to a real Silent Payments implementation." Browse open issues together. Each participant picks a target repo. |

**Facilitator tips:**
- The benchmark exercise is eye-opening. Participants will see that scanning mainnet takes minutes (not seconds) on a laptop, and much longer on a phone.
- This naturally motivates Module 4 (compact block filters) — plant that seed now.
- Spend the last 30 minutes browsing GitHub issues together. This makes Session 6 much more productive.

#### Session 6: Contributing to Silent Payments (2.5 hours)

| Time | Activity | Notes |
|------|----------|-------|
| 0:00-0:30 | **Code walkthrough: Bitcoin Core #28122** | Screen-share the PR. Walk through the key files. Show the test vectors. |
| 0:30-1:00 | **Code walkthrough: rust-silentpayments** | API tour, example usage, open issues |
| 1:00-1:10 | **Break** | |
| 1:10-2:00 | **Work time** | Participants fork their chosen repo, set up the dev environment, start working on their chosen issue. Help individuals. |
| 2:00-2:30 | **Check-in and next steps** | Each participant shares what they're working on and any blockers. Set a deadline for the PR (typically 1-2 weeks). |

**Facilitator tips:**
- Not everyone will submit a PR during the session. That's fine. The goal is to get them past the "I don't know where to start" barrier.
- Good first contributions: documentation improvements, test coverage, fixing typos in specifications, adding examples.
- If Bitcoin Core feels too intimidating, steer participants toward rust-silentpayments or wallet integrations.

---

### Module 3: Payjoin — BIP77/78

#### Session 7: How Payjoin Breaks Chain Analysis (2.5 hours)

| Time | Activity | Notes |
|------|----------|-------|
| 0:00-0:20 | **Lecture: CIOH is the backbone of surveillance** | Recap from Module 1. "We're going to break it." |
| 0:20-0:50 | **Lecture: Payjoin V1 → V2** | The liveness problem. How V2 solves it with directories. |
| 0:50-1:00 | **Break** | |
| 1:00-1:30 | **Whiteboard exercise: Payjoin step by step** | Walk through the 9-step Payjoin flow on the whiteboard. Both participants play sender and receiver. |
| 1:30-2:00 | **Exercise: Ambiguity analysis** | Use the exercises from the README. Given a transaction, how many interpretations exist? |
| 2:00-2:30 | **Discussion** | "If every merchant used Payjoin, what would happen to chain analysis as an industry?" |

#### Session 8: Building with Payjoin Dev Kit (3 hours)

| Time | Activity | Notes |
|------|----------|-------|
| 0:00-0:20 | **PDK API overview** | Screen-share the rust-payjoin docs |
| 0:20-1:30 | **Hands-on: regtest Payjoin** | `exercises/payjoin_testnet.md` — Exercises 1-2 |
| 1:30-1:40 | **Break** | |
| 1:40-2:30 | **Hands-on: compare normal vs Payjoin** | Exercise 2 — side-by-side comparison |
| 2:30-3:00 | **Discussion questions** | Coin selection for receivers, sender verification checks, mobile UX |

#### Session 9: Contributing to Payjoin (2.5 hours)

Same structure as Session 6. Code walkthrough of payjoin-rust and BTCPay Server, then guided contribution time.

---

### Module 4: Privacy-Preserving Wallet Development

#### Session 10: Transaction Construction for Privacy (3 hours)

| Time | Activity | Notes |
|------|----------|-------|
| 0:00-0:30 | **Lecture: The invisible fingerprints** | nLockTime, nSequence, version, fee estimation, output ordering |
| 0:30-1:30 | **Coding: Coin Selection Simulator** | `exercises/coin_selection_simulator.py` — Implement 4 algorithms |
| 1:30-1:40 | **Break** | |
| 1:40-2:30 | **Coding: Comparison analysis** | Run all algorithms against different UTXO sets, analyze privacy scores |
| 2:30-3:00 | **Discussion** | "If you were building a wallet from scratch for maximum privacy, what defaults would you choose?" |

#### Session 11: Compact Block Filters (3 hours)

| Time | Activity | Notes |
|------|----------|-------|
| 0:00-0:20 | **Lecture: Why SPV is broken for privacy** | BIP37 Bloom filters leak your addresses to the server |
| 0:20-0:40 | **Lecture: Golomb-Rice coding** | Use whiteboard to work through encoding by hand |
| 0:40-1:30 | **Coding: Build a filter** | `exercises/compact_block_filters.py` — Exercises 1-3 |
| 1:30-1:40 | **Break** | |
| 1:40-2:20 | **Coding: Filter analysis** | Exercise 4 — measure size, FP rate, query time |
| 2:20-2:50 | **Coding: SP + CBF simulation** | Exercise 5 — how filters make Silent Payments viable on mobile |
| 2:50-3:00 | **Preview capstone** | Introduce the capstone project (Module 4 Session 3) |

#### Session 12: CoinJoin, CoinSwap, and the Future (2.5 hours)

| Time | Activity | Notes |
|------|----------|-------|
| 0:00-0:30 | **Lecture: CoinJoin and WabiSabi** | Equal-output mixing, anonymity sets, coordinator trust |
| 0:30-0:50 | **Lecture: CoinSwap and Teleport** | Atomic swaps for privacy, multi-hop routing |
| 0:50-1:00 | **Break** | |
| 1:00-1:20 | **Lecture: The future** | CISA, Ark, Taproot-enabled privacy |
| 1:20-2:00 | **Capstone project introduction** | Explain requirements, review rubric, help participants choose topics |
| 2:00-2:30 | **Final discussion** | "What privacy improvement would you work on if you had a year of funding?" Reflect on the track as a whole. |

---

## Assessment Framework

### Grading Philosophy

This track produces Bitcoin open-source contributors, not exam-takers. Assessment is based on demonstrated ability to understand, implement, and contribute.

### Components

| Component | Weight | Description |
|-----------|--------|-------------|
| Exercises | 30% | Completion of all Python/Rust exercises across modules |
| Session 2 Essay | 10% | 500-word essay on privacy improvements |
| PR Submissions | 30% | At least 1 PR to a Silent Payments or Payjoin repo |
| Capstone Project | 30% | Final report + implementation (see capstone/README.md) |

### Exercise Rubric

| Score | Criteria |
|-------|----------|
| Complete (100%) | All functions implemented, tests pass, reflection questions answered thoughtfully |
| Partial (70%) | Core functions implemented, some tests pass, reflection questions attempted |
| Started (40%) | Some functions implemented, demonstrates understanding of the concepts |
| Not submitted (0%) | No submission |

### PR Rubric

| Score | Criteria |
|-------|----------|
| Merged (100%) | PR accepted and merged by maintainers |
| Under review (80%) | PR submitted, tests pass, responding to review comments |
| Submitted (60%) | PR submitted with clear description |
| Draft (40%) | Draft PR or work-in-progress with progress toward completion |
| Not submitted (0%) | No PR attempted |

---

## Guest Speaker Suggestions

These developers are actively working on the privacy projects covered in this track. Inviting one or two as guest speakers adds enormous credibility and motivation.

| Name | Project | Topic |
|------|---------|-------|
| Josie Baker | Bitcoin Core Silent Payments | BIP352 design decisions, scanning optimization |
| Dan Gould | Payjoin Dev Kit | PDK architecture, BIP77 implementation |
| Ruben Somsen | BIP352 co-author | Silent Payments theory, future improvements |
| Murch | Bitcoin Core coin selection | Branch-and-bound, waste metric, privacy trade-offs |
| Chris Belcher | CoinSwap/Teleport | CoinSwap design, JoinMarket NG |
| Rob (rustaceanrob) | Kyoto light client | BIP157/158 implementation, BDK integration |

**How to invite:**
- Reach out via GitHub, Twitter/X, or Nostr
- Offer a 30-45 minute slot (video call is fine)
- Share the curriculum in advance so they know the audience level
- Ask them to focus on "what needs to be built" — your participants are looking for contribution opportunities

---

## Common Problems and Solutions

**"The ECC math is too hard"**
- Point them back to the Bitcoin Dojo Week 1-2 exercises (FieldElement, Point, etc.)
- Use small numbers on the whiteboard before jumping to secp256k1
- Pair struggling participants with stronger ones

**"I can't find an issue to work on"**
- Documentation improvements always exist
- Test coverage gaps are easy to identify with `cargo tidy` or `gcov`
- Translating error messages is valuable and approachable
- Reviewing other people's PRs counts as contribution

**"Bitcoin Core is too intimidating"**
- Start with rust-silentpayments (smaller codebase, friendlier maintainers)
- BDK and Kyoto are also good entry points
- BTCPay Server's Payjoin code is in C# and well-documented

**"I don't have a full node"**
- All exercises work on regtest (no download required)
- Signet is lightweight enough for laptop use
- For the chain analysis lab, mempool.space provides the data

**"We only have 1 hour per session"**
- Cut the lecture portions to 10-15 minutes
- Assign reading as pre-work
- Focus on one exercise per session instead of the full set
- Extend the track to 18-24 weeks

---

## After the Track

### Contribution Sprint

The track naturally leads into a contribution sprint. Participants should:

1. Continue working on their PRs from Sessions 6 and 9
2. Pick a new issue from the target repos and start a second PR
3. Review each other's PRs (cross-review builds community)
4. Present their capstone projects to the group

### Staying Connected

- Add graduates to a dedicated Discord/Telegram channel for ongoing support
- Share relevant Bitcoin Optech newsletters and PR updates
- Organize monthly "privacy office hours" where graduates can get help with contributions
- Track merged PRs — this is the metric that matters for grant renewals

### Measuring Success

Track these metrics for grant reporting:

| Metric | Target | How to measure |
|--------|--------|----------------|
| Track completions | 80%+ of enrolled | Exercise submissions + capstone |
| PRs submitted | 1+ per participant | GitHub links |
| PRs merged | 30%+ of submitted | GitHub links |
| Ongoing contributors | 50%+ at 3 months | GitHub activity |
| Repeat cohorts | 2+ per year | Enrollment records |

---

*Code Orange Dev School | [codeorange.dev](https://codeorange.dev) | CC0 1.0 Universal*
