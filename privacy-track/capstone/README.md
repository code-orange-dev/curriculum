# Capstone Project — Bitcoin Privacy Developer Track

> Design, implement, and document a meaningful contribution to Bitcoin's privacy infrastructure.

---

## Overview

The capstone is the culmination of the privacy track. You will choose a project that combines what you've learned across all four modules and produce something that matters — code that gets merged, analysis that informs development, or a tool that helps other developers.

This is not a homework assignment. It's a portfolio piece that demonstrates you can contribute to Bitcoin's privacy infrastructure at a professional level.

---

## Timeline

| Week | Milestone |
|------|-----------|
| Week 1 | Submit proposal (1 page) for facilitator approval |
| Week 2-3 | Implementation and iteration |
| Week 4 | Submit deliverables + present to cohort |

---

## Project Options

Choose ONE of the following tracks, or propose your own (must be approved by facilitator).

### Track A: Code Contribution

**Goal:** Ship a meaningful PR to a privacy-related Bitcoin project.

**Requirements:**
- Submit a PR to one of the target repos (Bitcoin Core, rust-silentpayments, payjoin-rust, BDK, Kyoto, BTCPay Server)
- The PR must be non-trivial: a bug fix, feature implementation, test improvement, or significant documentation addition
- Write a 1,000-word technical report explaining: what you changed, why it matters, what you learned from the review process
- Present your PR and the review process to the cohort

**Rubric:**

| Criteria | Points |
|----------|--------|
| PR is well-scoped and clearly described | 20 |
| Code quality: tests, documentation, style compliance | 25 |
| Technical report depth and clarity | 20 |
| Response to reviewer feedback | 15 |
| Presentation quality | 10 |
| PR merged (bonus) | 10 |
| **Total** | **100** |

**Example projects:**
- Add label support to a Silent Payments wallet implementation
- Improve scanning performance in rust-silentpayments with batch ECDH
- Add BIP77 (Payjoin V2) support to an existing wallet
- Implement coin selection privacy scoring in BDK
- Add compact block filter support to a light client library
- Write integration tests for edge cases in payjoin-rust

---

### Track B: Privacy Analysis Tool

**Goal:** Build a tool that helps developers or users understand Bitcoin privacy.

**Requirements:**
- Build a functional tool (CLI, web app, or library)
- The tool must analyze or improve some aspect of Bitcoin privacy
- Write a 1,500-word report documenting: the problem it solves, how it works, privacy model and limitations
- Open-source the code under CC0 or MIT license
- Present a live demo to the cohort

**Rubric:**

| Criteria | Points |
|----------|--------|
| Tool solves a real privacy problem | 25 |
| Implementation quality and completeness | 25 |
| Technical report depth | 20 |
| Privacy model analysis (what it protects against, what it doesn't) | 15 |
| Presentation and demo | 15 |
| **Total** | **100** |

**Example projects:**
- A wallet fingerprint detector: input a raw transaction, output which wallet likely created it and what privacy leaks exist
- A UTXO privacy scorer: given a wallet's UTXO set, score how "private" each UTXO is and recommend actions
- A Payjoin simulator: visual tool showing how Payjoin breaks CIOH with configurable parameters
- A Silent Payment address generator/validator with full BIP352 compliance testing
- A compact block filter explorer: visualize filter contents, false positive rates, compression ratios
- A transaction graph analyzer: given a set of transactions, build and visualize the entity graph using heuristics

---

### Track C: Research and Documentation

**Goal:** Produce a comprehensive technical document that advances understanding of a Bitcoin privacy topic.

**Requirements:**
- Write a 3,000-5,000-word technical document
- Must include original analysis (not just summarizing existing material)
- Must reference at least 5 primary sources (BIPs, academic papers, implementation code)
- Publish under CC0 license
- Present findings to the cohort

**Rubric:**

| Criteria | Points |
|----------|--------|
| Originality of analysis | 25 |
| Technical depth and accuracy | 25 |
| Quality of writing and structure | 20 |
| Practical recommendations for developers | 15 |
| Presentation quality | 15 |
| **Total** | **100** |

**Example projects:**
- "Silent Payments Scanning Optimization: A Comparison of Approaches" — benchmark different scanning strategies, analyze trade-offs for mobile vs desktop
- "Payjoin Adoption Analysis: What Needs to Happen for Critical Mass" — study current adoption, identify barriers, propose solutions
- "Wallet Privacy Audit: Comparing Fingerprints Across the Top 10 Bitcoin Wallets" — test real wallets and document their privacy properties
- "The Economics of CoinJoin: How CISA Would Change the Privacy Landscape" — model fee savings and adoption incentives
- "Compact Block Filters for Silent Payments: Architecture Proposals for Mobile Wallets" — design a practical architecture combining CBF + SP
- "Bitcoin Privacy in Southeast Asia: Regulatory Landscape and Developer Opportunities" — map the regulatory environment and identify where privacy tools are most needed

---

### Track D: Education and Curriculum

**Goal:** Create educational material that extends this curriculum or makes it accessible to a new audience.

**Requirements:**
- Create a complete lesson, exercise set, or tutorial
- Must be technically accurate and tested
- Must fill a gap in the existing curriculum
- CC0 licensed
- Present and teach a sample lesson to the cohort

**Rubric:**

| Criteria | Points |
|----------|--------|
| Educational value and clarity | 25 |
| Technical accuracy | 25 |
| Completeness (ready to use by another facilitator) | 20 |
| Quality of exercises and assessments | 15 |
| Teaching demonstration | 15 |
| **Total** | **100** |

**Example projects:**
- A visual/interactive tutorial explaining Silent Payments using animations
- An exercise set teaching Payjoin integration in a specific programming language (Go, TypeScript, etc.)
- A "Bitcoin Privacy for Non-Developers" workshop module for activists, journalists, and NGO workers
- A Rust-language version of the Silent Payments sender/scanner exercises
- An advanced module on Taproot privacy properties (MuSig2, threshold signatures, scriptless scripts)
- A module on Lightning Network privacy (channel graph analysis, probing attacks, PTLCs)

---

## Proposal Template

Submit this before starting work (1 page max):

```
# Capstone Proposal

**Name:**
**Track:** A / B / C / D
**Title:**

## Problem
What specific problem does this project address? (2-3 sentences)

## Approach
How will you solve it? What technologies/tools will you use? (3-5 sentences)

## Deliverables
What exactly will you produce? Be specific. (Bullet list)

## Timeline
Week 1: ___
Week 2: ___
Week 3: ___
Week 4: ___

## Why It Matters
Who benefits from this work? How does it advance Bitcoin privacy? (2-3 sentences)
```

---

## Presentation Guidelines

Each capstone presentation should be 10-15 minutes:

- 2 minutes: problem statement and motivation
- 5-8 minutes: what you built/wrote and how it works (live demo for Tracks A/B)
- 3-5 minutes: what you learned, what was hard, what you'd do differently

The audience should ask questions. This is a peer review, not a lecture.

---

## Past Capstone Examples

*(This section will be populated as cohorts complete the track. First cohort graduates become examples for the next.)*

---

*Code Orange Dev School | [codeorange.dev](https://codeorange.dev) | CC0 1.0 Universal*
