# Week 10 notes

[Week 10 overview](../README.md) · [Exercises](../exercises/README.md) · [Solutions](../solutions/README.md) · [Slides](../slides/slides.md) · [After the cohort](../../after-the-cohort.md)

Taproot, part 2: script trees, control blocks and the Taproot sighash. Then capstone presentations and graduation.

## Key ideas

- **A Taproot output can hide a tree of scripts.** Each script is a leaf. Leaves are hashed with the "TapLeaf" tag, and pairs of hashes are combined with the "TapBranch" tag (sorted first) up to a single Merkle root. The root goes into the tweak that turns the internal key P into the output key Q.
- **Two ways to spend.** The key path uses one signature for Q. The script path reveals one leaf script, the inputs that satisfy it, and a control block.
- **The control block is a proof.** It holds the leaf version and the parity of Q (1 byte), the internal key (32 bytes), and the Merkle path (32 bytes per level). The verifier rebuilds Q from these and checks it matches the output.
- **Only the used leaf is revealed.** Other leaves appear only as hashes in the Merkle path. Unused conditions stay private, which P2SH and P2WSH could not do.
- **Tapscript (BIP342) updates Script.** Schnorr signatures, x-only keys, `OP_CHECKSIGADD` instead of `OP_CHECKMULTISIG`, no 10,000-byte or 201-opcode limits, a per-input signature budget, and `OP_SUCCESSx` for future upgrades.
- **The Taproot sighash commits to more.** BIP341 signatures commit to all input amounts and scriptPubKeys, the spend type, and (for script paths) the leaf being run. `SIGHASH_DEFAULT` saves a byte.
- **Design for the key path.** A single `multi_a` leaf is about the same size as P2WSH multisig. The big savings, and the best privacy, come when the common case is a key-path spend, for example with MuSig2.
- **Unspendable internal keys.** When every spend must go through a script, use a key with no known private key, such as BIP341's point H, or better H + r·G to hide that fact.

## Common mix-ups

| Mix-up | Correction |
|---|---|
| "The control block contains the whole tree." | It contains only the internal key and the sibling hashes on one path. Other scripts are never revealed. |
| "The first byte of the control block is just the leaf version." | It is the leaf version **plus** the parity bit of Q. For tapscript it is `c0` or `c1`. |
| "Taproot multisig is always smaller than P2WSH." | Only on the key path. A single 2-of-3 `multi_a` leaf is slightly bigger than P2WSH 2-of-3. |
| "`OP_CHECKMULTISIG` works in tapscript." | It is disabled in tapscript. Use `OP_CHECKSIGADD` (`multi_a` in descriptors). |
| "The order of leaves in the descriptor fixes left and right in the proof." | Branch hashes sort their two children, so the proof does not depend on left or right. Depth still matters for proof size. |
| "A relative timelock protects an inheritance forever." | `older()` restarts each time the coin moves. The owner must refresh, and the maximum is 65,535 blocks. For longer delays use `after()`. |

## Session plan

| Time | Block | Who | Notes |
|---|---|---|---|
| 0:00 to 0:05 | Welcome and roles | Facilitator | Post the presentation order. Confirm roles. |
| 0:05 to 0:10 | Opening question | Facilitator, everyone | "What would you like to build next?" One sentence each. |
| 0:10 to 0:25 | Concept recap | Facilitator, Exercise driver | Script tree, control block, tapscript, sighash, footprint. Show Lab 1 output briefly. |
| 0:25 to 0:45 | Question round | Question owners, Devil's advocate | About 3 minutes each. Q5 on a whiteboard. Q6 last. |
| 0:45 to 1:15 | Capstone presentations | Everyone | 3 minutes each, strict. One question per demo. |
| 1:15 to 1:30 | Next steps, feedback, graduation | Facilitator, Summariser | After-the-cohort guide, feedback form, congratulations. |

## Facilitator tips

**Before the session**

- Post the presentation order and the 3-minute rule on Discord two days before.
- Run Lab 1 yourself and save the output, so you can show it even if a live node misbehaves.
- Prepare the feedback form link and post it in the chat during the last block.
- Read [After the cohort](../../after-the-cohort.md) so you can point people to a concrete first step.
- With more than 10 participants, shorten the concept recap or split presentations across a bonus session.

**Where people get stuck**

- **Capstone not finished.** Let them present any exercise they are proud of. Finishing matters less than explaining.
- **Control block bytes.** Walk through Lab 1.5 byte by byte: first byte, H, sibling hash.
- **Timelock errors.** `non-BIP68-final` confuses people. It means "too early", not "invalid".
- **Size surprises.** People expect Taproot multisig to be smaller. Use the Lab 2 table to show why the key path matters.
- **Next steps feel too big.** Help people shrink their goal to one action in the next two weeks.

## Glossary

| Term | Meaning |
|---|---|
| Tapleaf | One script in a Taproot tree, with its leaf version. |
| Tapbranch | A node that combines two child hashes (sorted) with the "TapBranch" tag. |
| Merkle root | The single hash at the top of the script tree, committed in the tweak. |
| Merkle path | The sibling hashes from one leaf up to the root. |
| Control block | The last witness item of a script-path spend: leaf version and parity, internal key, Merkle path. |
| Leaf version | A byte that says how to run the leaf. `0xc0` is tapscript. |
| Tapscript | The Script rules for leaf version `0xc0` (BIP342). |
| `OP_CHECKSIGADD` | Tapscript opcode that checks a signature and adds 1 to a counter if valid. |
| `OP_SUCCESSx` | Reserved tapscript opcodes that make a script succeed, kept for future soft forks. |
| NUMS point | "Nothing up my sleeve": a key with no known private key, such as BIP341's H. |
| `multi_a` | Descriptor for a k-of-n tapscript multisig using `OP_CHECKSIGADD`. |
| Annex | An optional last witness item starting with `0x50`, reserved for future use. |

## Further resources

- [BIP341: Taproot](https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki) and its [wallet test vectors](https://github.com/bitcoin/bips/blob/master/bip-0341/wallet-test-vectors.json).
- [BIP342: Tapscript](https://github.com/bitcoin/bips/blob/master/bip-0342.mediawiki).
- [BIP386: `tr()` output script descriptors](https://github.com/bitcoin/bips/blob/master/bip-0386.mediawiki).
- [Bitcoin Optech: Tapscript](https://bitcoinops.org/en/topics/tapscript/), [Taproot](https://bitcoinops.org/en/topics/taproot/), [Miniscript](https://bitcoinops.org/en/topics/miniscript/), [Output script descriptors](https://bitcoinops.org/en/topics/output-script-descriptors/).
- [Mastering Bitcoin](https://github.com/bitcoinbook/bitcoinbook): the third edition covers Taproot and tapscript.
- [Bitcoin Core CONTRIBUTING.md](https://github.com/bitcoin/bitcoin/blob/master/CONTRIBUTING.md): how contributions to Bitcoin Core work.
- [Bitcoin Core PR Review Club](https://bitcoincore.reviews/): weekly guided reviews of real pull requests.
- [Bitcoin Optech newsletter](https://bitcoinops.org/en/newsletters/): a weekly summary of technical Bitcoin news.
