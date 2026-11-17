---
marp: true
theme: default
paginate: true
title: "Decoding Bitcoin, Week 8: Project: build your own Bitcoin stack"
---

# Decoding Bitcoin
## Week 8: Project: build your own Bitcoin stack

Code Orange Dev School · Monday seminar

<!--
Welcome everyone. This is project week: tonight is mostly demos and discussion of what people built.
Check that each group has posted their repository link on Discord before you start.
-->

---

# Tonight (90 minutes)

| Time | Block |
|---|---|
| 0:00 | Welcome and roles (5) |
| 0:05 | Opening question (10) |
| 0:15 | Group demos (30) |
| 0:45 | Question round (25) |
| 1:10 | Exercise walkthrough: P2PKH trace (10) |
| 1:20 | Wrap-up and next week (10) |

<!--
Demos are the core of tonight. Keep each to about 5 minutes. If there are more than 6 groups, cut demos to 4 minutes each.
The Facilitator keeps time and gives a 1-minute warning.
-->

---

# Roles tonight

- **Facilitator:** time, opening question, quiet voices
- **Summariser:** takeaways on Discord within a day
- **Devil's advocate:** pokes holes in each demo
- **Exercise driver:** shares screen for the P2PKH trace
- Everyone: owns one discussion question

<!--
Confirm roles now. The Devil's advocate has a fun job tonight: ask each group "what input breaks your code?"
Rotate roles from last week.
-->

---

# Opening question

> What did you only really understand once you had to build it yourself?

<!--
Give everyone 1 minute to think, then go round quickly. One sentence each.
Typical answers: true/false rules, number encoding, OP_IF, why scripts have limits.
Write the answers in the chat; the Summariser can reuse them.
-->

---

# The machine in one loop

```
for each opcode in script:
    if inside a skipped IF branch: skip
    else: run opcode on the stack
    if a rule breaks: FAIL now
end: PASS if stack not empty and top is true
```

- No loops, no jumps back
- Every item is a byte array

<!--
This is the whole model. Everything else is opcode details.
Stress: no loops means running time is bounded by script length.
Bytes, not integers: numbers are a view of bytes.
-->

---

# True, false and numbers

| Bytes | Meaning | Truth |
|---|---|---|
| (empty) | 0, pushed by `OP_0` | false |
| `00`, `0000` | zero | false |
| `80` | negative zero | false |
| `01` / `81` | 1 / -1 | true |
| `8000` | 128 | true |

- Little-endian, sign bit in last byte

<!--
Ask: why is 128 two bytes? Because 0x80 alone would set the sign bit, so you need an extra 0x00 byte.
Ask: who had a bug with negative zero or OP_0?
-->

---

# Conditionals: an execution stack

```
OP_0 OP_IF  OP_2  OP_ELSE  OP_3  OP_ENDIF
     [F]    skip  [T]      run   []
```

- One true/false entry per open `OP_IF`
- Run an opcode only if all entries are true
- Unbalanced `OP_IF` = FAIL

<!--
The execution stack is separate from the data stack.
IF, ELSE and ENDIF must be handled even inside a skipped branch, otherwise nesting breaks.
-->

---

# Failure and limits

- First failure ends the script: no partial success
- `VERIFY` false, `OP_RETURN`, underflow: all FAIL
- 520-byte push, 1,000 stack items
- 201 opcodes, 10,000-byte script (legacy, v0)
- Why: every node runs every script

<!--
Limits protect nodes from denial of service.
Tapscript (week 10) removes the 201-opcode and 10,000-byte limits but keeps 520 and 1,000, and adds a signature budget.
-->

---

# How do you know it is correct?

- Test the subtle failures, not only happy paths
- `OP_1 OP_VERIFY` fails: empty stack at end
- `OP_5 OP_3 OP_SUB OP_2 OP_EQUAL`: operand order
- Compare with `decodescript` and `script_tests.json`

<!--
Ask groups which test caught their worst bug.
Bitcoin Core's script_tests.json is a great source of real test vectors.
-->

---

# Question round

1. How did you represent the stack and opcodes?
2. How does your stack treat true and false?
3. Which opcode was hardest, and why?
4. How do you handle a script that fails halfway?
5. Which limits did you add, and why do they exist?
6. Which tests best convinced you it is correct?

<!--
Each question owner explains for 2 to 3 minutes, then others add.
Devil's advocate: challenge at least two answers.
Model answers are in solutions/README.md, but let the group get there first.
-->

---

# Exercise walkthrough: P2PKH trace

| Step | Op | Stack (top right) |
|---|---|---|
| 1-2 | push sig, pubkey | `sig pub` |
| 3 | `OP_DUP` | `sig pub pub` |
| 4 | `OP_HASH160` | `sig pub pkh` |
| 5 | push hash | `sig pub pkh pkh` |
| 6 | `OP_EQUALVERIFY` | `sig pub` |
| 7 | `OP_CHECKSIG` | `01` |

<!--
Exercise driver runs their interpreter in trace mode on test case 20.
Ask: where does it fail with the wrong key? (step 6). With the wrong signature? (step 7, then final check).
-->

---

# Before next Monday: Taproot keys

- [Introduction to Taproot](https://bitcoindevs.xyz/decoding/introduction-taproot)
- [Pay to Taproot](https://bitcoindevs.xyz/decoding/p2tr)
- [Schnorr & BIP340](https://bitcoindevs.xyz/decoding/schnorr-bip340)
- [Key-path Taproot](https://bitcoindevs.xyz/decoding/key-path-taproot)
- Leave one review comment on another group's repo

<!--
Week 9 is the start of Taproot. Four lessons, so start early.
Pick roles and question owners for next week before you close.
-->

---

# Thank you

- Summariser: post takeaways within a day
- Push your final code and tests
- Questions? Ask on Discord

<!--
Thank the groups for their demos. Remind people that the code they wrote is a great portfolio piece.
-->
