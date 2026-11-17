---
marp: true
theme: default
paginate: true
title: "Decoding Bitcoin, Week 7: P2SH and multisig"
---

# Decoding Bitcoin

## Week 7: P2SH and multisig

Code Orange Dev School

<!--
Welcome. Tonight: why more than one key, bare multisig, and how P2SH hides any script behind a hash.
The lab builds a real 2-of-3 on regtest with PSBTs.
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
| 1:20 | Wrap-up and project kickoff (7) |
| 1:27 | Buffer and close (3) |

<!--
Wrap-up is a bit special this week: next week is the project week, so groups should form tonight.
-->

---

# Roles tonight

- **Facilitator:** time, opening question, quiet voices
- **Summariser:** takeaways on Discord within a day
- **Devil's advocate:** pushes back on easy answers
- **Exercise driver:** shares screen for the lab
- **Everyone:** explains their own question

<!--
The Exercise driver should have run the whole lab once before the session. It uses many shell variables.
-->

---

# Opening question

> Why might you want more than one key to move your bitcoin,
> and what new risks does that bring?

<!--
Silent minute, then go round.
Look for: protection against theft of one key and loss of one key, shared control in a company. New risks: complexity, lost descriptor, coordination, bigger fees.
Devil's advocate: "Isn't one key with a good backup enough?"
-->

---

# Bare multisig (P2MS)

```
scriptPubKey: OP_2 <pk1> <pk2> <pk3> OP_3 OP_CHECKMULTISIG
scriptSig:    OP_0 <sig1> <sig2>

2-of-3, compressed keys: 105-byte output
```

- Sender pays for all the keys
- No address format
- Keys public from day one

<!--
Ask: why OP_0 at the start? Save the full answer for question 2.
-->

---

# The off-by-one bug

```
OP_CHECKMULTISIG pops:
  N, N pubkeys, M, M sigs  ... and one extra
```

- Extra item must exist, so push `OP_0`
- Fix would be a hard fork
- BIP147 NULLDUMMY: dummy must be empty
- Tapscript uses `OP_CHECKSIGADD` instead

<!--
Key message: a one-byte cost forever is cheaper than a hard fork.
NULLDUMMY was about malleability.
-->

---

# P2SH: pay to a script hash

```
Output:  OP_HASH160 <20-byte hash> OP_EQUAL   (23 bytes)
Spend:   OP_0 <sig1> <sig2> <redeemScript>

Node: HASH160(redeemScript) == hash?
      then run redeemScript with the sigs
```

- Address starts with `3` (regtest: `2`)
- Receiver pays for the script when spending

<!--
The redeem script is the last push. It appears on chain only when the coin is spent.
Limit: 520 bytes per push, so at most 15 compressed keys.
-->

---

# Why old nodes accepted it

| Node | Checks |
|---|---|
| Old (pre-BIP16) | hash of top item matches |
| New | that, plus run the redeem script |

- Stricter rules only = soft fork
- Activated April 2012

<!--
Question 6 owner will explain this. To an old node, P2SH looks like "anyone who knows the preimage can spend".
-->

---

# Same script, three wrappers

| Wrapper | Output size | Script lives in | 2-of-3 spend |
|---|---|---|---|
| Bare | 105 B | output | about 227 vB |
| P2SH | 23 B | scriptSig | about 334 vB |
| P2WSH | 34 B | witness | about 146 vB |

<!--
Sizes for one input, one P2WPKH output. Bare multisig spend is small but the sender paid 105 bytes earlier.
Lab steps 5 and 6 let people measure P2SH vs P2WSH themselves.
-->

---

# Multisig with PSBTs

```
Coordinator (watch-only):  create + update
Signer 1 ----\
              combine -> finalize -> extract -> broadcast
Signer 3 ----/
```

- Signers never talk to each other
- Back up the descriptor, not only seeds

<!--
Same roles as week 5, now with real co-signers.
Without the descriptor (all public keys and the policy), two seeds alone cannot rebuild the wallet.
-->

---

# Question round

1. How does P2SH move cost to the receiver?
2. The OP_CHECKMULTISIG bug: why not fixed?
3. Why is bare multisig rare today?
4. Redeem script: what, and when on chain?
5. 2-of-3 vs single key plus backup?
6. BIP16 soft fork: why old nodes agree?

<!--
About 6 minutes each. For question 5, ask the group to vote first, then the owner explains.
-->

---

# Exercise walkthrough: 2-of-3 on regtest

```bash
DESC_SH=$(bitcoin-cli -regtest getdescriptorinfo \
  "sh(multi(2,$K1,$K2,$K3))" | jq -r .descriptor)
# ... watch-only wallet, fund, then:
S1=$(... -rpcwallet=signer1 walletprocesspsbt $PSBT ...)
S3=$(... -rpcwallet=signer3 walletprocesspsbt $PSBT ...)
bitcoin-cli -regtest combinepsbt "[\"$S1\",\"$S3\"]"
```

- Read the final scriptSig together

<!--
Exercise driver: lab steps 3 to 5. Run analyzepsbt after each signer so the group sees "next" change.
Finish by decoding the spend: 0, sig, sig, redeemScript.
-->

---

# Before next Monday

Week 8: Project week

- [Project: Build your own bitcoin Stack](https://bitcoindevs.xyz/decoding/project)
- Form pairs or small groups tonight
- Demo on Monday
- Pick your discussion question

<!--
Groups of 2 or 3. Each group shares a repository link on Discord by midweek.
The week 8 folder has a milestone plan and test cases.
-->

---

# Thank you

- Summariser: post takeaways within a day
- Share your 2-of-3 business design on Discord
- See you next Monday

<!--
End on time.
-->
