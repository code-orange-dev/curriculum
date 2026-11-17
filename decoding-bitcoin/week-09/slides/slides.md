---
marp: true
theme: default
paginate: true
title: "Decoding Bitcoin, Week 9: Taproot: keys and Schnorr"
---

# Decoding Bitcoin
## Week 9: Taproot: keys and Schnorr

Code Orange Dev School · Monday seminar

<!--
Welcome. Tonight we start Taproot: why it exists, how a P2TR output is built, Schnorr signatures, and the key-path spend.
Next week covers script paths, so if someone asks about control blocks, park it for week 10.
-->

---

# Tonight (90 minutes)

| Time | Block |
|---|---|
| 0:00 | Welcome and roles (5) |
| 0:05 | Opening question (10) |
| 0:15 | Concept recap (15) |
| 0:30 | Question round (30) |
| 1:00 | Exercise walkthrough: key-path spend (20) |
| 1:20 | Wrap-up and next week (10) |

<!--
Keep the concept recap short: people read the lessons. Use it to fix shared vocabulary: internal key, output key, tweak, x-only.
-->

---

# Roles tonight

- **Facilitator:** time, opening question, quiet voices
- **Summariser:** takeaways on Discord within a day
- **Devil's advocate:** "is Taproot really more private?"
- **Exercise driver:** shares screen for regtest lab
- Everyone: owns one discussion question

<!--
Rotate roles from last week. The Exercise driver should have a regtest node with -txindex ready before the session.
-->

---

# Opening question

> Taproot makes many different spending setups look the same on-chain. Why is that good for everyone?

<!--
Push for the "crowd" argument: privacy improves for everyone when more people look the same, not only for the complex users.
Devil's advocate: does it hurt anyone? (Chain analysis firms, maybe some auditing use cases.)
-->

---

# Why Taproot (2021)

| Goal | How |
|---|---|
| Privacy | every output is one 32-byte key |
| Efficiency | 64-byte Schnorr sigs, key aggregation |
| Flexibility | script tree, leaf versions, `OP_SUCCESSx` |

- BIP340 + BIP341 + BIP342
- Activated at block 709,632

<!--
Three BIPs: 340 is Schnorr, 341 is Taproot outputs and spending rules, 342 is tapscript (week 10).
Ask: which goal matters most to you as a developer?
-->

---

# Building a P2TR output

```
internal key P  (+ optional script tree root)
        |
   t = H_TapTweak(P || root)
        |
   Q = P + t*G          output key
        |
scriptPubKey = OP_1 <32-byte Q>    -> bc1p...
```

- No scripts: tweak with H(P) only (BIP86)

<!--
Stress: the key in the wallet descriptor is P, the key in the output is Q. Lab 1 shows they are different.
The tweak commits to the script tree: you cannot change the scripts later without changing Q.
-->

---

# x-only keys

- BIP340 keys are 32 bytes: x coordinate only
- y is assumed even, no `02`/`03` prefix
- Saves 1 byte per output and signature
- Odd y? Signer negates their key
- Script path keeps the parity bit

<!--
This is a common source of confusion. Ask: if we drop the prefix, how does the verifier know which point? Answer: always the even-y one.
The parity bit appears in the control block (week 10).
-->

---

# Schnorr versus ECDSA

| | Schnorr (BIP340) | ECDSA |
|---|---|---|
| Signature | s = k + e·x | s = k⁻¹(z + r·x) |
| Size | 64 bytes, fixed | ~71-72 bytes DER |
| Linear? | yes | no |
| Aggregation | MuSig2, FROST | hard |

<!--
Linearity is the key word. Keys add, signatures add.
Batch verification is another benefit: verify many signatures faster than one by one.
-->

---

# Key-path spend

```
witness: [ 64-byte Schnorr signature ]
```

1. scriptPubKey is `OP_1 <Q>`: segwit v1
2. One witness item: key path
3. Build BIP341 sighash (all amounts, all scriptPubKeys)
4. Verify signature against Q

<!--
No script runs and no key is revealed: Q is already in the output.
65 bytes if a sighash byte is added; Bitcoin Core uses SIGHASH_DEFAULT, so 64.
-->

---

# Why bech32m?

- Bech32 bug: before a final `p`, add or drop `q`s
- v0 safe: program must be 20 or 32 bytes
- v1+ allows 2 to 40 bytes: typos could pass
- Bech32m (BIP350): new checksum constant
- `q` = version 0, `p` = version 1

<!--
Fun fact: this is why taproot addresses start with bc1p. The p is the witness version 1 in the bech32 character set.
-->

---

# Question round

1. What did Taproot solve: privacy, efficiency, flexibility?
2. What is a tweaked key? Why x-only keys?
3. Schnorr versus ECDSA: what does linearity allow?
4. What is MuSig, and why does it look single-sig?
5. Walk through a key-path spend.
6. Why bech32m instead of bech32?

<!--
Each owner explains for 3 to 4 minutes. Others add.
Devil's advocate: challenge Q1 and Q4. Is the privacy gain real if most people still use single-sig?
-->

---

# Exercise walkthrough: regtest key path

```
getnewaddress "" bech32m      -> bcrt1p...
getaddressinfo                -> desc key P != program Q
sendtoaddress, -generate 1
sendtoaddress (from taproot wallet)
getrawtransaction -> 1 witness item, 64 bytes
```

- Check vsize by hand: 154 vB (1 in, 2 P2TR out)

<!--
Exercise driver runs Labs 1 and 2 from exercises/README.md.
Ask the group to compute weight: 137 non-witness bytes x 3 + 205 total = 616, vsize 154.
If time allows, run Lab 4 (tweak.py) to show P becomes Q.
-->

---

# Before next Monday: Taproot scripts

- [Script-path Taproot](https://bitcoindevs.xyz/decoding/script-path-taproot)
- [Taproot Signatures](https://bitcoindevs.xyz/decoding/taproot-signatures)
- [Capstone: Build & Spend a P2TR](https://bitcoindevs.xyz/decoding/build-spend-p2tr)
- Prepare a 3-minute capstone demo

<!--
Next week is the last session. Everyone presents for 3 minutes: the capstone or an exercise they are proud of.
Assign roles and question owners now.
-->

---

# Thank you

- Summariser: post takeaways within a day
- Post your tweak explanation on Discord
- Start the capstone early

<!--
Remind people that the capstone takes longer than they think. Encourage pairing.
-->
