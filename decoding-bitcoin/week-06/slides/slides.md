---
marp: true
theme: default
paginate: true
title: "Decoding Bitcoin, Week 6: Script basics"
---

# Decoding Bitcoin

## Week 6: Script basics

Code Orange Dev School

<!--
Welcome. Tonight we open up Bitcoin Script: the stack, locking and unlocking scripts, and the two oldest output types, P2PK and P2PKH.
Ask people to have pen and paper ready for stack traces.
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
Same shape as every week. Facilitator keeps time.
-->

---

# Roles tonight

- **Facilitator:** time, opening question, quiet voices
- **Summariser:** takeaways on Discord within a day
- **Devil's advocate:** pushes back on easy answers
- **Exercise driver:** shares screen for the lab
- **Everyone:** explains their own question

<!--
Confirm roles. Exercise driver should have a regtest node running already.
-->

---

# Opening question

> Why does Bitcoin use a tiny stack language
> instead of letting people write any program they like?

<!--
One minute of silent thinking, then go round.
Look for: every node runs every script, so cost must be bounded and predictable. Simplicity reduces consensus bugs.
Devil's advocate: "Ethereum lets you write anything. Isn't Bitcoin just behind?"
-->

---

# The stack machine

```
OP_2 OP_3 OP_ADD OP_5 OP_EQUAL

push 2     | 2
push 3     | 2 3
OP_ADD     | 5
push 5     | 5 5
OP_EQUAL   | 1      -> true, valid
```

- Read left to right
- Data pushes, opcodes pop and push

<!--
This is discussion question 1, so keep it light here and let the owner go deeper.
Hex: 52 53 93 55 87. Lab step 1 decodes it.
-->

---

# Lock and key

```
Output (tx A):  scriptPubKey  = the lock
Input  (tx B):  scriptSig     = the key

Run scriptSig  -> leaves a stack
Run scriptPubKey on that stack
Valid if no failure and top is true
```

- Run separately since 2010 (OP_RETURN bug)

<!--
Stress the order. The scriptSig supplies evidence, the scriptPubKey checks it.
Segwit moves the evidence to the witness, but the idea is the same.
-->

---

# P2PK: pay to public key

```
scriptPubKey: <pubkey> OP_CHECKSIG
scriptSig:    <sig>

21 <33-byte key> ac   = 35 bytes
41 <65-byte key> ac   = 67 bytes (2009)
```

- Used in early coinbase outputs
- No address format
- Public key visible from the start

<!--
Block 9 coinbase and block 170 are the classic examples. Exercise 1.
-->

---

# P2PKH: pay to public key hash

```
scriptPubKey: OP_DUP OP_HASH160 <20 bytes>
              OP_EQUALVERIFY OP_CHECKSIG
hex:          76 a9 14 <20 bytes> 88 ac  (25 bytes)
scriptSig:    <sig> <pubkey>
```

- HASH160 = RIPEMD160(SHA256(pubkey))
- Short address with checksum (starts with 1)

<!--
Why replace P2PK? Shorter addresses, smaller outputs, key hidden until spent. That is question 3.
-->

---

# P2PKH stack trace

| Step | Stack (top right) |
|---|---|
| `<sig> <pubkey>` | `sig pubkey` |
| `OP_DUP` | `sig pubkey pubkey` |
| `OP_HASH160` | `sig pubkey h` |
| `<pkh>` | `sig pubkey h pkh` |
| `OP_EQUALVERIFY` | `sig pubkey` |
| `OP_CHECKSIG` | `1` |

<!--
Ask: which step fails with the wrong key? (EQUALVERIFY.) With a bad signature? (CHECKSIG.)
Question 4 owner will walk through it in detail.
-->

---

# Limits and disabled opcodes

- No loops, `OP_IF` only jumps forward
- 10,000-byte script, 201 opcodes
- 520-byte stack items, 1,000 items
- 2010: `OP_CAT`, `OP_MUL` and others disabled
- Disabling = stricter rules = soft fork

<!--
Sets up questions 5 and 6. A script containing a disabled opcode fails even in an unexecuted branch.
-->

---

# Question round

1. Run `OP_2 OP_3 OP_ADD OP_5 OP_EQUAL`
2. scriptPubKey vs scriptSig, and run order?
3. Why did P2PKH replace P2PK?
4. P2PKH spend: stack after each opcode?
5. Why is Script not Turing complete?
6. Why disable opcodes in a live system?

<!--
About 6 minutes each. Ask the owners of questions 1 and 4 to draw the stack in a shared text box or on screen.
-->

---

# Exercise walkthrough: decode and trace

```bash
bitcoin-cli -regtest decodescript 5253935587
bitcoin-cli -regtest -rpcwallet=miner \
  getaddressinfo $P2PKH
bitcoin-cli -regtest decoderawtransaction $SIGNED \
  | jq '.vin[0].scriptSig'
```

- Split the scriptPubKey into bytes
- Trace the real scriptSig on screen

<!--
Exercise driver: lab steps 1, 2 and 4. Then the group traces the real P2PKH spend together, step by step.
If time allows, show step 5 (mining to a pk() descriptor).
-->

---

# Before next Monday

Week 7: P2SH and multisig

- [P2SH: Pay To Script Hash (BIP 16)](https://bitcoindevs.xyz/decoding/p2sh)
- [P2MS: Pay To Multisig](https://bitcoindevs.xyz/decoding/p2ms)
- Pick your discussion question

<!--
Assign roles and questions for week 7. The week 7 lab uses PSBTs again, so point people back to week 5 lab steps 5 and 6.
-->

---

# Thank you

- Summariser: post takeaways within a day
- Post your P2PKH trace on Discord
- See you next Monday

<!--
End on time.
-->
