---
marp: true
theme: default
paginate: true
title: "Decoding Bitcoin, Week 10: Taproot scripts and graduation"
---

# Decoding Bitcoin
## Week 10: Taproot scripts and graduation

Code Orange Dev School · Final Monday seminar

<!--
Welcome to the last session. Tonight: script trees, control blocks, the Taproot sighash, then capstone presentations and graduation.
Have the presentation order posted on Discord before you start.
-->

---

# Tonight (90 minutes)

| Time | Block |
|---|---|
| 0:00 | Welcome and roles (5) |
| 0:05 | Opening question (5) |
| 0:10 | Concept recap (15) |
| 0:25 | Question round (20) |
| 0:45 | Capstone presentations (30) |
| 1:15 | Next steps, feedback, graduation (15) |

<!--
Presentations are 3 minutes each. With 10 people that is 30 minutes. If the group is bigger, shorten the concept recap.
The Facilitator is strict on time tonight so everyone gets a turn.
-->

---

# Roles tonight

- **Facilitator:** time, strict 3-minute slots
- **Summariser:** takeaways and graduate list on Discord
- **Devil's advocate:** one kind question per demo
- **Exercise driver:** shares screen for script-path lab
- Everyone: owns one question and presents

<!--
Last rotation. Thank people who took roles throughout the cohort.
-->

---

# Opening question

> Now that you can build and spend a Taproot output, what would you like to build next?

<!--
Keep it to 5 minutes: one sentence each. These answers lead into question 6 and the next-steps block.
The Summariser should note them; they are great for the cohort recap post.
-->

---

# The script tree

```
              root = TapBranch(sorted)
             /                 \
     TapLeaf(A)              TapBranch
                            /         \
                     TapLeaf(B)    TapLeaf(C)

TapLeaf   = H_TapLeaf(0xc0 || len || script)
TapBranch = H_TapBranch(min || max)
Q = P + H_TapTweak(P || root) * G
```

<!--
Sorting the children means proofs do not need left/right flags.
Unbalanced trees are fine: likely scripts go near the root for shorter proofs.
-->

---

# Script-path witness

```
[ script inputs... ]  [ leaf script ]  [ control block ]
```

| Control block part | Size |
|---|---|
| leaf version + parity of Q | 1 byte |
| internal key P | 32 bytes |
| Merkle path | 32 x depth |

<!--
The verifier rebuilds the root from the leaf and path, tweaks P, and checks it equals Q with the right parity.
Only the used leaf is revealed. Others appear only as hashes.
-->

---

# Tapscript in brief (BIP342)

- Schnorr signatures, 32-byte x-only keys
- `OP_CHECKSIGADD` replaces `OP_CHECKMULTISIG`
- No 10,000-byte or 201-opcode limits
- Signature budget per input instead
- `OP_SUCCESSx` for future soft forks

<!--
Connect back to week 7 (CHECKMULTISIG off-by-one) and week 8 (limits).
multi_a in descriptors compiles to CHECKSIG / CHECKSIGADD / NUMEQUAL.
-->

---

# Taproot sighash (BIP341)

| Commits to | Segwit v0 | Taproot |
|---|---|---|
| Own input amount | yes | yes |
| All input amounts | no | yes |
| All input scriptPubKeys | no | yes |
| Leaf being run | no | yes (script path) |
| No-byte default type | no | `SIGHASH_DEFAULT` |

<!--
Ask: why does committing to all amounts help a hardware wallet? It can trust the total input value and so the fee.
-->

---

# Footprint: 2-of-3 multisig input

| Spend | vbytes |
|---|---|
| P2WSH `OP_CHECKMULTISIG` | ~104.5 |
| P2TR script path, `multi_a` leaf | ~108.75 |
| P2TR key path (MuSig2) | 57.5 |

- Taproot wins through the key path

<!--
From Lab 2. Surprise for many: a single multi_a leaf is a bit bigger than P2WSH.
The lesson: design so the common case uses the key path.
-->

---

# Question round

1. What are a tapleaf and a tapbranch?
2. What is in a control block, and what does it prove?
3. Why is only the used script revealed?
4. What changed in the Taproot sighash?
5. Design an inheritance wallet script tree.
6. What's your next step after this cohort?

<!--
About 3 minutes per question. Q5 works well on a shared whiteboard: key path, leaf 1, leaf 2.
Save Q6 for last and let several people answer.
-->

---

# Exercise walkthrough: heir spends leaf B

```
tr(H, { pk(OWNER), and_v(v:pk(HEIR), older(5)) })

sequence=5, broadcast now   -> non-BIP68-final
-generate 5, broadcast      -> accepted
witness: [ sig 64 | script 36 | control block 65 ]
```

- Control block = `c0`/`c1` + H + hash(leaf A)

<!--
Exercise driver shows Lab 1 from exercises/README.md, or the recorded output if time is short.
Point out: the owner's key never appears, only leaf A's hash.
Then move straight to capstone presentations.
-->

---

# Capstone presentations

- 3 minutes each, strict
- What you built, show it, one lesson, what's next
- One kind question from the Devil's advocate
- Applause after every demo

<!--
Read out the order. Give a 30-second warning. If someone cannot present, invite them to post a short video on Discord.
-->

---

# After the cohort

- Read [After the cohort](../../after-the-cohort.md)
- Bitcoin Core: build, run tests, review a PR
- Join a PR review club
- First contribution: docs, tests, small fixes
- Come back as a mentor for the next cohort

<!--
The after-the-cohort guide (decoding-bitcoin/after-the-cohort.md) covers Bitcoin Core architecture and a first open-source contribution path.
Ask each person to name one concrete action for the next 2 weeks.
-->

---

# Feedback and graduation

- Fill in the feedback form today
- Summariser posts the cohort recap
- Congratulations, graduates!

<!--
Post the feedback form link in the chat. Thank everyone, especially those who took roles.
Celebrate: this was 10 weeks of real work.
-->
