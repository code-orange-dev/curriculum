---
marp: true
theme: default
paginate: true
title: "Decoding Bitcoin, Week 5: Signing and the transaction exercises"
---

# Decoding Bitcoin

## Week 5: Signing and the transaction exercises

Code Orange Dev School

<!--
Welcome everyone. Tonight is about signatures: what they commit to, where they live, and how wallets pass unsigned transactions around.
Check that the Summariser and Exercise driver are ready.
-->

---

# Tonight (90 minutes)

| Time | Block |
|---|---|
| 0:00 | Welcome and roles (5) |
| 0:05 | Opening question (10) |
| 0:15 | Concept recap (10) |
| 0:25 | Question round (40) |
| 1:05 | Exercise walkthrough (15) |
| 1:20 | Wrap-up and next week (7) |
| 1:27 | Buffer and close (3) |

<!--
Facilitator keeps time. If the question round runs long, shorten the walkthrough, not the wrap-up.
-->

---

# Roles tonight

- **Facilitator:** time, opening question, quiet voices
- **Summariser:** takeaways on Discord within a day
- **Devil's advocate:** pushes back on easy answers
- **Exercise driver:** shares screen for the lab
- **Everyone:** explains their own question

<!--
Confirm who has each role. Remind people that the devil's advocate is a role, not a personality.
-->

---

# Opening question

> A signature proves something very specific.
> What exactly does it prove, and what doesn't it?

<!--
Give 1 minute of silent thinking, then go round.
Look for: it proves the holder of a key approved a specific message (the sighash). It does not prove identity, ownership in a legal sense, or that the parts left out by the sighash flag are fixed.
Devil's advocate: "So a signature proves I own the coins?"
-->

---

# What gets signed: the sighash

```
spending tx (modified copy)
  + previous scriptPubKey (scriptCode)
  + amount            (segwit v0 and taproot)
  + sighash flag      (4 bytes)
        |
   SHA256(SHA256(...))  -> 32-byte message
        |
   sign with private key
```

- Signature cannot sign itself, so it is left out

<!--
Key point: the signer hashes a modified copy of the transaction. Legacy, BIP143 (segwit v0) and BIP341 (taproot) each build this message differently.
Taproot uses tagged hashes, not double SHA-256, but the idea is the same.
-->

---

# Sighash flags

| Flag | Inputs signed | Outputs signed |
|---|---|---|
| ALL `01` | all | all |
| NONE `02` | all | none |
| SINGLE `03` | all | same index only |
| `+ANYONECANPAY` `80` | this one only | as above |

- Flag is the last byte of the signature

<!--
Ask: which of these would you never use alone? (NONE.)
SINGLE|ANYONECANPAY = 0x83 is used for marketplace offers.
-->

---

# Why segwit signs the amount

- Legacy: amount not in the signed message
- Offline signer had to trust or re-check
- Attacker lies about input value, fee explodes
- BIP143: amount committed, wrong amount fails
- BIP341: commits to all input amounts

<!--
Also mention quadratic hashing: legacy re-hashes the tx for every input. BIP143 caches the shared parts.
The 2020 multi-session attack on segwit v0 is why taproot commits to every input's amount and scriptPubKey.
-->

---

# Where the signature lives

```
Legacy P2PKH input
  txid | vout | scriptSig: <sig> <pubkey> | sequence

Native segwit P2WPKH input
  txid | vout | scriptSig: (empty)        | sequence
  ... after outputs:  witness: [<sig>, <pubkey>]
```

- Witness is not in the txid
- Witness bytes weigh 1, not 4

<!--
Connect to week 3 (malleability) and week 4 (weight).
-->

---

# Nonce reuse leaks the key

- ECDSA: `s = k⁻¹(z + r·d)`
- Same `k` twice means same `r`
- Two equations, two unknowns: solve for `d`
- Real cases: PS3, Android wallets 2013
- Fix: deterministic nonces (RFC 6979)

<!--
Do not go deep into the math. The lesson: the nonce is as secret as the key.
Lab step 2 shows Bitcoin Core produces identical signatures for the same message.
-->

---

# PSBT: signing without the key online

```
Creator -> Updater -> Signer(s) -> Combiner
        -> Finalizer -> Extractor -> broadcast
```

- Computer builds, device signs
- PSBT carries UTXOs and key paths
- Check address and amount on device screen

<!--
This sets up question 6 and the bonus questions. Week 7 uses the same roles for multisig.
-->

---

# Question round

1. What is the sighash? Why not sign the raw tx?
2. ALL vs NONE vs SINGLE. When ANYONECANPAY?
3. Why does segwit sign the amount?
4. What happens on nonce reuse?
5. Where is the signature: legacy vs segwit?
6. How does a hardware wallet keep its key?

<!--
About 6 minutes per question. Owner explains (2-3 min), then one follow-up from the group, then the devil's advocate.
-->

---

# Exercise walkthrough: lab steps 1 to 3

```bash
RAW=$(bitcoin-cli -regtest createrawtransaction ...)
bitcoin-cli -regtest -rpcwallet=alice \
  signrawtransactionwithwallet $RAW
bitcoin-cli -regtest -rpcwallet=alice -named \
  signrawtransactionwithwallet hexstring=$RAW \
  sighashtype=NONE
```

- Did the txid change after signing?
- What is the last signature byte?

<!--
Exercise driver shares screen. Show decoderawtransaction before and after signing. Point at txinwitness[0], last byte 01 vs 02.
Ask the group to predict before each command.
-->

---

# Before next Monday

Week 6: Script basics

- [Scripts overview](https://bitcoindevs.xyz/decoding/overview)
- [P2PK: Pay To Public Key](https://bitcoindevs.xyz/decoding/p2pk)
- [P2PKH: Pay To Public Key Hash](https://bitcoindevs.xyz/decoding/p2pkh)
- Pick your discussion question

<!--
Assign roles for next week now. Remind people to finish the GitHub Classroom exercises and the pair review.
-->

---

# Thank you

- Summariser: post takeaways within a day
- Questions? Ask on Discord
- See you next Monday

<!--
Thank the Exercise driver and the devil's advocate. End on time.
-->
