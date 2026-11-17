# Week 1 notes

[Week 1 overview](../README.md) · [Exercises](../exercises/README.md) · [Solutions](../solutions/README.md) · [Slides](../slides/slides.md)

## Key ideas

- **The double-spend problem.** Digital information can be copied for free. Any digital cash system has to stop people spending the same coin twice. Before Bitcoin, the working answer was a trusted company that kept the only ledger. Bitcoin's answer is a shared ledger that anyone can check, where the order of transactions is decided by proof of work.

- **Proof of work gives an order without a boss.** Miners repeatedly hash a block header until the result is below a target. Finding such a hash is expensive, but checking it is cheap. Nodes follow the valid chain with the most accumulated work. To rewrite history, an attacker has to redo that work faster than everyone else.

- **Hash functions are everywhere.** A hash function turns any input into a fixed-size fingerprint. Bitcoin relies on it being one-way, collision resistant, and on small input changes giving unrelated outputs. Hashes name transactions (txid) and blocks, link blocks into a chain, build the Merkle root of a block, and shorten public keys into addresses.

- **Coins, not accounts.** Bitcoin does not store balances. It stores unspent transaction outputs (UTXOs). A transaction spends whole UTXOs as inputs and creates new outputs. Whatever you don't send to the receiver comes back to you as a change output, and what is left over goes to the miner as the fee.

- **Your balance is calculated by your wallet.** The wallet finds the UTXOs that your keys can unlock and adds them up. Nodes don't know or care who owns what. They only check that each spend follows the rules.

- **Don't trust, verify.** A full node checks every block and transaction itself. You can also verify the software you install (release signatures, reproducible builds) and check your own payments. Some trust is still left (in cryptography, hardware, code review), but you choose it.

- **Regtest is your lab.** Regtest is a private chain on your laptop. You can mine blocks instantly and the coins have no value. From week 2 we use it to try every idea with `bitcoin-cli`.

## Common mix-ups

| Mix-up | Correction |
|---|---|
| "My wallet holds my bitcoin." | The coins are UTXOs recorded on the blockchain. Your wallet holds the keys that can spend them. |
| "Bitcoin stores my balance like a bank account." | No balance exists in the protocol. Your wallet adds up the UTXOs your keys control. |
| "Hashing is a kind of encryption." | Encryption can be reversed with a key. A hash cannot be reversed at all. You can only guess inputs and compare. |
| "Spending part of a coin leaves the rest in the old output." | An output is always spent completely. The rest goes to a new change output. |
| "Miners decide the rules." | Every full node checks every block. A miner that breaks the rules makes a block that nodes reject. |
| "Bitcoin was the first digital cash." | DigiCash and others came earlier. Bitcoin was the first to work without a trusted central party. |

## Session plan

| Time | Block | Who | Notes |
|---|---|---|---|
| 0:00-0:10 | Welcome and how the cohort works | Facilitator | Weekly rhythm, question ownership, where materials live, code of conduct |
| 0:10-0:25 | Round of introductions | Everyone | About 2 minutes each. Use breakout rooms of 4-5 if the group is large |
| 0:25-0:35 | Tour: dashboard and Decoding Bitcoin | Facilitator | Show the dashboard, a lesson page, the tools, and this repository's week folders |
| 0:35-0:45 | Opening question | Facilitator | One minute of silent thinking, then 3-4 voices. Note common words |
| 0:45-0:55 | Concepts: double spend, hashes, UTXOs | Facilitator | Slides 7-10. Keep it short. Ask questions, don't lecture |
| 0:55-1:15 | Question round | Everyone, devil's advocate | Open discussion of the 6 questions, about 3 minutes each |
| 1:15-1:25 | Live exercise | Exercise driver | Hash tool, then one transaction on mempool.space. Vote on the change output |
| 1:25-1:30 | Roles for week 2 and next steps | Facilitator | Assign question owners and roles. Remind about regtest setup |

## Facilitator tips

Before the session:

- Check that the Discord voice channel, screen sharing and the dashboard work.
- Have the Hash Functions tool and mempool.space open in browser tabs.
- Prepare the list of the week 2 questions and roles so people can claim them at the end.
- Install Bitcoin Core yourself on a clean machine (or check that [`bitcoin_core_cli.md`](../exercises/bitcoin_core_cli.md) still matches the latest release), so you can help with setup problems.

Where people get stuck:

- **Setup.** Building from source takes time and fails on missing packages. Point most people to the release binary (Option A in the lab). Make sure people use Bitcoin Core v29 or newer, where builds use CMake, not `./configure` and `make`.
- **`sendtoaddress` fails on regtest** with "Fee estimation failed". The node needs `-fallbackfee=0.0001` (or the command needs a `fee_rate`).
- **`getrawtransaction` can't find a confirmed transaction.** Start the node with `-txindex=1`.
- **Balance confusion.** People expect 5050 BTC after mining 101 blocks. This is a great moment to explain coinbase maturity.
- **Quiet participants.** Many people are reading in their second language. Give thinking time before asking, and invite people by name in a friendly way. Allow answers in the text chat too.

## Glossary

- **Double spend:** trying to spend the same coin in two different transactions.
- **Proof of work:** finding a block header hash below a target by trying many nonces. Hard to do, easy to check.
- **Hash function:** a function that maps any input to a fixed-size output that cannot be reversed. Bitcoin mostly uses SHA-256 (and SHA-256 twice, called hash256).
- **Avalanche effect:** a tiny change in the input changes about half of the output bits.
- **UTXO:** unspent transaction output. A coin that can still be spent.
- **UTXO set:** the list of all UTXOs that every full node keeps.
- **Change output:** an output that sends the leftover amount back to the sender.
- **Fee:** sum of inputs minus sum of outputs. It goes to the miner.
- **Coinbase transaction:** the first transaction in each block. It creates new coins (subsidy plus fees) and pays the miner.
- **Coinbase maturity:** coinbase outputs can only be spent 100 blocks later.
- **Full node:** software that downloads and checks every block and transaction against the rules.
- **Regtest:** a private local test chain where you mine blocks instantly.

## Further resources

- [Bitcoin whitepaper](https://bitcoin.org/bitcoin.pdf): short and readable. Sections 1 to 5 match this week.
- [Mastering Bitcoin](https://github.com/bitcoinbook/bitcoinbook): free book. The first chapters cover the overview and how Bitcoin works.
- [learnmeabitcoin.com](https://learnmeabitcoin.com/): clear explanations with diagrams. Its [transaction pages](https://learnmeabitcoin.com/technical/transaction/) are useful from week 2.
- [Programming Bitcoin](https://github.com/jimmysong/programmingbitcoin): a free book that builds Bitcoin's pieces in Python, for those who learn by coding.
- [mempool.space](https://mempool.space): a block explorer to look at real blocks, transactions and fees.
- [Bitcoin Core download page](https://bitcoincore.org/en/download/): release binaries and how to verify them.
- [Bitcoin Core `doc/build-unix.md`](https://github.com/bitcoin/bitcoin/blob/master/doc/build-unix.md): official build instructions.
- [Bitcoin Core RPC reference](https://developer.bitcoin.org/reference/rpc/): descriptions of `bitcoin-cli` commands (written for an older version; `bitcoin-cli help <command>` is always current).
