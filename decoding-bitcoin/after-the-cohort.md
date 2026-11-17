# After the cohort: from learner to contributor

[← Week 10](./week-10/) · [Syllabus](./README.md)

You can now read a transaction byte by byte, explain Script, and build and spend a Taproot output. This guide is the next step: getting to know Bitcoin Core (or another Bitcoin open-source project) and making your first contribution. Work through it alone, with a study buddy, or as a 2-week follow-up to the cohort.

---

## Part 1: Bitcoin Core architecture and development

### Goals

- Navigate the Bitcoin Core codebase
- Build it from source and run the unit and functional tests
- Read and review real pull requests
- Understand how contributions get reviewed and merged

### Readings

- [Bitcoin Core CONTRIBUTING.md](https://github.com/bitcoin/bitcoin/blob/master/CONTRIBUTING.md)
- [Bitcoin Core developer documentation](https://github.com/bitcoin/bitcoin/tree/master/doc), especially `build-unix.md` (or `build-osx.md`) and `developer-notes.md`
- [Functional test framework README](https://github.com/bitcoin/bitcoin/blob/master/test/functional/README.md)
- [Chaincode Labs Bitcoin Curriculum](https://github.com/chaincodelabs/bitcoin-curriculum)
- [Jon Atack: How to review pull requests in Bitcoin Core](https://jonatack.github.io/articles/how-to-review-pull-requests-in-bitcoin-core)
- [Bitcoin Core PR Review Club](https://bitcoincore.reviews/): weekly sessions on one PR, with notes and questions for each

### Exercises

1. **Build from source and run the tests.** Bitcoin Core uses CMake since v29:

   ```bash
   git clone https://github.com/bitcoin/bitcoin.git && cd bitcoin
   cmake -B build
   cmake --build build -j$(nproc)
   ctest --test-dir build -j$(nproc)          # unit tests
   build/test/functional/test_runner.py -j$(nproc)   # functional tests (takes a while)
   ```

2. **Find your way around.** Locate where these live and write one sentence on what each does: transaction validation (`src/validation.cpp`, `src/consensus/`), the script interpreter (`src/script/interpreter.cpp`), the mempool (`src/txmempool.cpp`), P2P networking (`src/net.cpp`, `src/net_processing.cpp`), the wallet (`src/wallet/`) and the RPC layer (`src/rpc/`).
3. **Connect it to the cohort.** Find the code for something you studied: for example `SignatureHash` (the sighash from week 5), `OP_CHECKMULTISIG` and its extra pop (week 7), or the Taproot control block checks (week 10). Read it and explain it to someone.
4. **Run one functional test on its own** (for example `build/test/functional/wallet_basic.py`) and read its source. How does it start nodes, mine blocks and check results?
5. **Review a PR.** Pick a recent PR Review Club session, read the PR and the notes, build the branch, run its tests and write your review comments (you don't have to post them).

### Questions to discuss

1. Describe the Bitcoin Core review process. Why is it considered one of the most careful in open source?
2. What is the functional test suite for? How would you write a test for a new RPC?
3. What is the difference between consensus code and policy code? Why does the difference matter so much for reviewers?

---

## Part 2: Your first open-source contribution

### Goals

- Submit a real pull request (or a written review) to a Bitcoin open-source project
- Use the fork, branch, PR, review, iterate workflow
- Follow a project's contribution guide and coding standards

### Pick a project

Contribution guides for some projects that welcome new contributors:

- [Bitcoin Core](https://github.com/bitcoin/bitcoin/blob/master/CONTRIBUTING.md)
- [rust-bitcoin](https://github.com/rust-bitcoin/rust-bitcoin/blob/master/CONTRIBUTING.md)
- [BDK](https://github.com/bitcoindevkit/bdk/blob/master/CONTRIBUTING.md)
- [LDK](https://github.com/lightningdevkit/rust-lightning/blob/main/CONTRIBUTING.md)
- [The Bitcoin Dev Project](https://bitcoindevs.xyz/): their good first issues list across many projects

Start small and useful. Good first contributions include:

- A documentation fix or clearer explanation
- A new or improved test
- A small bug fix from a "good first issue" label
- A translation
- A careful written review of someone else's PR (in Bitcoin Core, review is the most valued contribution)

### Steps

1. Read the project's CONTRIBUTING file and a few recently merged PRs to see the style.
2. Comment on the issue before you start, so nobody duplicates work.
3. Fork, create a branch, make the change and run the project's tests locally.
4. Write a clear PR description: what, why, and how you tested it.
5. Respond to review politely and quickly. Expect several rounds; that's normal.

### Share it

Present your contribution to the group (5 minutes):

1. What project did you contribute to, and why?
2. What does your PR (or review) do?
3. What did you learn from the review process?
4. What will you work on next?

---

## Keep going

- Aim for one contribution a month, of any size
- Join the [Bitcoin Core PR Review Club](https://bitcoincore.reviews/)
- Continue with the [Privacy Track](../privacy-track/) in this repo
- Apply to fellowships and grant programs (Chaincode Labs, Summer of Bitcoin, Btrust, Vinteum, Brink and others)
- Come back as a facilitator for the next Decoding Bitcoin cohort
