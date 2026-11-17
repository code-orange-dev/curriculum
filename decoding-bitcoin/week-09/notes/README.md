# Week 9 notes

[Week 9 overview](../README.md) · [Exercises](../exercises/README.md) · [Solutions](../solutions/README.md) · [Slides](../slides/slides.md)

Taproot, part 1: why it exists, how a P2TR output is built, Schnorr signatures, and the key-path spend.

## Key ideas

- **One output type for everything.** A P2TR output is `OP_1 <32-byte key>`. A single user, a group of signers and a complex contract all produce outputs that look the same.
- **Internal key and output key.** The wallet holds an internal key P. The output contains a different key, Q = P + t·G, where t is a tagged hash of P and (optionally) the root of a script tree. The owner can still sign for Q because they know t.
- **The tweak is a commitment.** Changing the scripts would change Q, so the script tree is fixed when the output is created, but it stays hidden until (and unless) it is used. With no scripts, BIP86 tweaks with the hash of P alone, which proves there is no hidden script.
- **x-only keys.** BIP340 uses only the 32-byte x coordinate of keys and nonces, and assumes the y coordinate is even. This saves a byte without hurting security.
- **Schnorr is linear.** A BIP340 signature is (R, s) with s = k + e·x. Keys and signatures can be added, which enables MuSig2 key aggregation (BIP327), threshold signatures and batch verification. ECDSA's inverse step blocks this.
- **The key-path spend is tiny.** The witness is a single 64-byte signature (65 with a sighash byte). No public key is revealed, because Q is already in the output. The node checks the signature against Q using the BIP341 sighash.
- **The new sighash commits to more.** BIP341's signature message commits to the amounts and scriptPubKeys of all inputs, which helps hardware wallets and offline signers check fees safely.
- **Bech32m for v1+.** Bech32 has a typo weakness that matters when program lengths can vary. BIP350's bech32m fixes it. The `p` in `bc1p` is the witness version 1.

## Common mix-ups

| Mix-up | Correction |
|---|---|
| "The key in my wallet descriptor is the key on-chain." | The descriptor shows the internal key P. The output holds the tweaked key Q. They are different (see Lab 1.3). |
| "Taproot makes every transaction smaller." | Inputs are smaller, but a P2TR output is 12 bytes bigger than a P2WPKH output. A simple 1-in-2-out payment is slightly bigger. The big wins are multisig and complex scripts. |
| "MuSig gives you k-of-n multisig." | MuSig2 is n-of-n. For k-of-n, use FROST or a script tree with one leaf per key combination. |
| "x-only keys are less secure because half the key is missing." | The y coordinate is fixed by a rule (even y), so no information the verifier needs is lost. Security is essentially the same. |
| "Bech32m is a new address format." | It is the same bech32 format with a different checksum constant. Version 0 uses bech32; version 1 and above use bech32m. |
| "A Taproot address always means a script exists." | Not necessarily. Most wallets today use BIP86 key-only outputs. From outside, you cannot tell. |

## Session plan

| Time | Block | Who | Notes |
|---|---|---|---|
| 0:00 to 0:05 | Welcome and roles | Facilitator | Confirm roles and question owners. |
| 0:05 to 0:15 | Opening question | Facilitator, everyone | "Why is it good for everyone that setups look the same?" Look for the crowd argument. |
| 0:15 to 0:30 | Concept recap | Facilitator | Slides: why Taproot, building a P2TR output, x-only keys, Schnorr, key path, bech32m. |
| 0:30 to 1:00 | Question round | Question owners, Devil's advocate | 6 questions, about 5 minutes each. |
| 1:00 to 1:20 | Exercise walkthrough | Exercise driver | Labs 1 and 2 on regtest: P versus Q, then a key-path spend. Compute vsize together. |
| 1:20 to 1:30 | Wrap-up and next week | Facilitator, Summariser | Week 10 lessons, capstone demo slots, roles for the final session. |

## Facilitator tips

**Before the session**

- Run Labs 1 and 2 yourself on Bitcoin Core 28 or newer. Check that `getnewaddress "" bech32m` works (it does in any descriptor wallet).
- Make sure the Exercise driver has started `bitcoind` with `-txindex=1`, otherwise `getrawtransaction` fails for confirmed transactions.
- Find one real P2TR key-path spend and one P2WPKH spend on mempool.space ahead of time, in case the group's examples are confusing.
- Read the tweak explanations posted on Discord and pick one or two good ones to praise.

**Where people get stuck**

- **P versus Q.** This is the biggest source of confusion. Draw the arrow from P to Q on the slide, then show Lab 1.3.
- **Elliptic curve maths.** Some participants will want the full maths, others will be lost. Keep the session at the level of "keys can be added", and point maths fans to BIP340.
- **MuSig2 rounds.** People ask why two rounds are needed. Short answer: nonces must be exchanged before signing to stay safe. Park the details.
- **Sighash byte.** People expect 65 bytes. Explain `SIGHASH_DEFAULT`.
- **Script path questions.** Park them for week 10.

## Glossary

| Term | Meaning |
|---|---|
| Taproot | The 2021 soft fork (BIP340, 341, 342) that added segwit v1 outputs. |
| P2TR | Pay to Taproot: the output `OP_1 <32-byte key>`, address `bc1p...` (`bcrt1p...` on regtest). |
| Internal key | The untweaked key P the owner starts with. |
| Output key | The tweaked key Q = P + t·G that appears in the output. |
| Tweak | The value t = tagged_hash("TapTweak", P or P plus Merkle root). |
| Tagged hash | SHA256(SHA256(tag) ‖ SHA256(tag) ‖ data). It keeps hashes for different purposes separate. |
| x-only key | A 32-byte public key: just the x coordinate, with even y assumed. |
| Schnorr signature | A BIP340 signature (R, s), 64 bytes. |
| Key path | Spending a P2TR output with one signature for the output key. |
| Script path | Spending a P2TR output by revealing one script from the tree (week 10). |
| MuSig2 | A two-round protocol (BIP327) for n-of-n key and signature aggregation. |
| SIGHASH_DEFAULT | Taproot-only sighash type 0x00. Signs like ALL but needs no extra byte. |
| Bech32m | The BIP350 checksum variant used for witness version 1 and above. |

## Further resources

- [BIP340: Schnorr signatures](https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki) and its [reference code](https://github.com/bitcoin/bips/blob/master/bip-0340/reference.py).
- [BIP341: Taproot](https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki).
- [BIP86: key derivation for single-key P2TR outputs](https://github.com/bitcoin/bips/blob/master/bip-0086.mediawiki).
- [BIP327: MuSig2](https://github.com/bitcoin/bips/blob/master/bip-0327.mediawiki).
- [BIP350: Bech32m](https://github.com/bitcoin/bips/blob/master/bip-0350.mediawiki).
- [Bitcoin Optech: Taproot](https://bitcoinops.org/en/topics/taproot/), [Schnorr signatures](https://bitcoinops.org/en/topics/schnorr-signatures/), [MuSig](https://bitcoinops.org/en/topics/musig/).
- [Mastering Bitcoin](https://github.com/bitcoinbook/bitcoinbook): the third edition covers Schnorr signatures and Taproot.
- [mempool.space](https://mempool.space): look at real P2TR spends.
- [Bitcoin Core RPC reference](https://developer.bitcoin.org/reference/rpc/): `getaddressinfo`, `decodescript`, `getrawtransaction`.
