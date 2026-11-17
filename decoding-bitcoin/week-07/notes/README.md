# Week 7 notes

Notes for [week 7: P2SH and multisig](../README.md). For the full course plan, see the [syllabus](../../README.md).

## Key ideas

- **Multisig spreads control over several keys.** An M-of-N script needs M valid signatures from N listed public keys. 2-of-3 is the most common: one key can be lost and one key can be stolen without losing the coins.
- **Bare multisig puts everything in the output.** `OP_M <keys> OP_N OP_CHECKMULTISIG` is the scriptPubKey. The sender pays for every key, there is no address, and the keys are public from the start. That is why it is rarely used for payments today.
- **OP_CHECKMULTISIG has an off-by-one bug.** It pops one extra stack item, so every spend starts with a dummy `OP_0`. Fixing it would need a hard fork. BIP147 made the dummy rule stricter (it must be empty) to stop malleability.
- **P2SH locks to a hash of the script.** The output is a fixed 23-byte pattern and an address starting with `3`. The receiver reveals the redeem script, and pays for it, only when spending. The redeem script is limited to 520 bytes.
- **P2SH was a soft fork.** Old nodes only check that the revealed script matches the hash. New nodes also run the script. Every block that new nodes accept, old nodes accept too.
- **P2WSH is the segwit version of the same idea.** The output holds a 32-byte SHA256 hash of the witness script, and the script and signatures move to the witness. A 2-of-3 spend costs less than half the vbytes of the P2SH version.
- **Multisig wallets need more than seeds.** To rebuild the wallet you need the descriptor: all public keys (or xpubs) with their paths, M, and the script type. Signers coordinate with PSBTs and never need to share private keys.

## Common mix-ups

| Mix-up | Correction |
|---|---|
| "A `3...` address is a multisig address." | It is a P2SH address. It could hold any script: multisig, a timelock, or nested segwit (P2SH-P2WPKH). You only know when it is spent. |
| "The redeem script is stored in the output." | Only its 20-byte hash is in the output. The script itself appears in the spending input's scriptSig. |
| "The signatures can be in any order." | They must be in the same order as their public keys in the script. `OP_CHECKMULTISIG` walks the key list once. |
| "The `OP_0` at the start is a signature placeholder for the missing key." | It is the dummy item for the off-by-one bug. It is needed even for 1-of-1, and it must be empty. |
| "With two of my three seeds I can always recover." | Only if you also have the third public key (or xpub) and the policy. Back up the descriptor. |
| "Multisig is always better than one key." | It removes the single point of theft, but adds complexity, cost and new ways to fail (lost descriptor, unavailable co-signer). |

## Session plan

| Time | Block | Who | Notes |
|---|---|---|---|
| 0:00 to 0:05 | Welcome and roles | Facilitator | Confirm roles. Remind people next week is the project. |
| 0:05 to 0:15 | Opening question | Facilitator, everyone | "Why more than one key, and what new risks?" Silent minute first. |
| 0:15 to 0:25 | Concept recap | Facilitator | Slides: bare multisig, off-by-one, P2SH, soft fork, three wrappers, PSBT roles. |
| 0:25 to 1:05 | Question round | Question owners | About 6 minutes per question. Vote before question 5. |
| 1:05 to 1:20 | Exercise walkthrough | Exercise driver | Lab steps 3 to 5: watch-only wallet, two signers, combine, decode the scriptSig. |
| 1:20 to 1:27 | Wrap-up and project kickoff | Facilitator, Summariser | 3 takeaways. Form project groups for week 8. Assign roles. |
| 1:27 to 1:30 | Buffer and close | Facilitator | Overrun or open questions. |

## Facilitator tips

Before the session:

- Run the whole lab on a fresh regtest node. It uses many shell variables (`$K1`, `$DESC_SH`, `$PSBT`), so it must run in one terminal. Keep a copy of your terminal history to paste from if the live demo breaks.
- Find one real P2SH multisig spend on mempool.space in advance, in case people could not find one for exercise 2.
- Think about how to split people into project groups of 2 or 3 for week 8, mixing stronger and newer programmers.

Where people get stuck:

- **`addmultisigaddress` or `dumpprivkey` errors.** These only work with legacy wallets, which are no longer the default. Point them to the descriptor-based lab.
- **Signer does not sign.** The keys in the descriptor need their origin (`[fingerprint/path]`), otherwise the PSBT has no `bip32_derivs` and the signer wallet does not recognise its key. Check with `decodepsbt`.
- **"Transaction needs a change address".** The watch-only wallet cannot make change. Spend the whole coin with `subtractFeeFromOutputs` or set `changeAddress`.
- **Missing descriptor checksum.** `importdescriptors` needs the `#checksum`. Always run the descriptor through `getdescriptorinfo` first.
- **Counting hex vs bytes.** `wc -c` on a hex string counts characters. Divide by 2.
- **Question 6 confusion.** People mix up soft and hard forks. Use the table on the slides: a soft fork only adds checks.

## Glossary

- **Multisig (M-of-N):** a spending condition that needs M signatures from N listed public keys.
- **P2MS (bare multisig):** a multisig script used directly as the scriptPubKey.
- **OP_CHECKMULTISIG:** the opcode that checks M signatures against N keys. Pops one extra dummy item.
- **NULLDUMMY (BIP147):** the rule that the dummy item must be an empty byte array.
- **P2SH (BIP16):** Pay to Script Hash. Output: `OP_HASH160 <hash> OP_EQUAL`.
- **Redeem script:** the script whose hash is in a P2SH output. Revealed when spending.
- **Witness script:** the P2WSH equivalent of a redeem script, stored in the witness.
- **P2WSH:** Pay to Witness Script Hash. Output: `OP_0 <32-byte SHA256 hash>`.
- **Soft fork:** a rule change that only makes rules stricter, so old nodes still accept new blocks.
- **Hard fork:** a rule change that makes something valid that was invalid before. Old nodes reject the new blocks.
- **Descriptor:** a string that describes exactly which scripts a wallet uses, such as `wsh(multi(2,...))`.
- **Key origin:** the `[fingerprint/path]` part of a key in a descriptor, showing which master key and path it came from.
- **BIP67:** sorting multisig public keys so everyone builds the same script from the same set of keys.

## Further resources

- [BIP 16: Pay to Script Hash](https://github.com/bitcoin/bips/blob/master/bip-0016.mediawiki)
- [BIP 11: M-of-N standard transactions](https://github.com/bitcoin/bips/blob/master/bip-0011.mediawiki)
- [BIP 147: Dealing with dummy stack element malleability](https://github.com/bitcoin/bips/blob/master/bip-0147.mediawiki)
- [BIP 67: Deterministic P2SH multi-signature addresses](https://github.com/bitcoin/bips/blob/master/bip-0067.mediawiki)
- [BIP 141: Segregated Witness](https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki) (P2WSH)
- [BIP 174: PSBT](https://github.com/bitcoin/bips/blob/master/bip-0174.mediawiki)
- [Bitcoin Optech: PSBTs](https://bitcoinops.org/en/topics/psbt/)
- [Bitcoin Core multisig tutorial](https://github.com/bitcoin/bitcoin/blob/master/doc/multisig-tutorial.md) (descriptor wallets and PSBTs, the same approach as our lab)
- [Mastering Bitcoin](https://github.com/bitcoinbook/bitcoinbook), the chapter on authorization and authentication (multisig and P2SH)
- [Programming Bitcoin](https://github.com/jimmysong/programmingbitcoin), chapter 8 (Pay to Script Hash)
- [Bitcoin Core RPC reference](https://developer.bitcoin.org/reference/rpc/) (`createmultisig`, `importdescriptors`, `walletcreatefundedpsbt`)
