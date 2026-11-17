---
marp: true
theme: default
paginate: true
title: "Decoding Bitcoin, Week 3: Inside a transaction, byte by byte"
---

# Decoding Bitcoin

## Week 3: Inside a transaction, byte by byte

Hex, little-endian, compact size, segwit

<!--
Welcome. Tonight is detail-heavy. Encourage people to keep a raw transaction open in a text editor during the session.
-->

---

# Tonight (90 min)

| Time | Block |
|---|---|
| 0:00 | Welcome and roles (5) |
| 0:05 | Opening question (10) |
| 0:15 | Concepts: bytes, endianness, layout, txid (15) |
| 0:30 | Question round: 6 questions (35) |
| 1:05 | Exercise walkthrough: label a transaction (15) |
| 1:20 | Takeaways (7) |
| 1:27 | Before next Monday (3) |

<!--
Same rhythm as last week. Facilitator keeps time.
-->

---

# Roles this week

- **Facilitator:** time, opening question, quiet voices
- **Summariser:** takeaways on Discord within a day
- **Devil's advocate:** "Why not just use JSON?"
- **Exercise driver:** labels a raw transaction live
- Question owners explain first

<!--
Confirm roles and question owners. The exercise driver should have the hex from lab step 2 ready.
-->

---

# Opening question

> A transaction is just bytes. What do those bytes have to say for everyone to agree it's valid?

<!--
Let people list things: which coins, where they go, proof of permission, rules version, when.
Then ask what is NOT there: input amounts, fee, sender. Nodes get those from the UTXO set.
Devil's advocate: why not a human-readable format? (Size, cost, one exact encoding to hash and sign.)
-->

---

# Reading bytes

- 1 byte = 2 hex characters (`ff` = 255)
- Little-endian: smallest byte first
- `02000000` = version 2
- `80d1f00800000000` = 150,000,000 sats
- Displayed txids are byte-reversed

<!--
Have people decode 01000000 and 0100000000000000 out loud.
The txid reversal is the most common trap: show it with lab step 5.
-->

---

# Compact size

| Value | Bytes |
|---|---|
| 0 to 252 | `xx` |
| up to 0xffff | `fd xx xx` |
| up to 0xffffffff | `fe xx xx xx xx` |
| bigger | `ff` + 8 bytes |

- Used for counts and lengths
- 300 = `fd2c01`

<!--
Ask: why not a fixed 4-byte count? Most counts are 1 or 2, so save bytes in every transaction.
Quick quiz: 253? (fdfd00)
-->

---

# Segwit transaction layout

```
02000000         version
00 01            marker, flag
01               input count
  <32> <4>       prev txid, vout
  00             scriptSig length (empty)
  fdffffff       sequence
02               output count
  <8> 16 0014<20>  value, script len, P2WPKH
  <8> 16 0014<20>
02 47<sig> 21<pubkey>   witness for input 0
<4>              locktime
```

<!--
Walk through top to bottom. Point out: no amount in the input, no fee anywhere.
In a legacy transaction, there is no 00 01, and the scriptSig holds the signature.
-->

---

# How a parser spots segwit

- Read 4 bytes of version
- Next byte `00`? That is the marker
- 0 inputs is impossible, so no confusion
- Flag must be `01`
- Witness comes after outputs, before locktime

<!--
Old nodes never see marker, flag or witness: they get the old format.
That is why segwit could be a soft fork.
-->

---

# txid vs wtxid

```
txid  = hash256(version | inputs | outputs | locktime)
wtxid = hash256(everything, incl. marker, flag, witness)
```

- No witness: txid = wtxid
- Outpoints use the txid
- Blocks commit to wtxids in the coinbase

<!--
hash256 = SHA-256 twice. Both are displayed byte-reversed.
Lab step 7: your hash of the raw hex matches "hash" (wtxid), not "txid".
-->

---

# Malleability, fixed

- Old: signature inside scriptSig, inside txid
- Tweak signature encoding: new txid, still valid
- Pre-signed children break
- Segwit: signature in witness, outside txid
- Lab step 9: txid same before and after signing

<!--
Show lab step 9 if time allows: legacy txid changes when signed, segwit txid does not.
Connect to Lightning: refund transactions are signed before funding confirms.
-->

---

# Question round

1. Little-endian, and the txid trap
2. Compact size: what and why?
3. What moves to the witness? Why does that fix malleability?
4. nLockTime: what for? A real use
5. Marker and flag: how does a parser detect segwit?
6. txid vs wtxid: how and why?

<!--
About 6 minutes per question. Owner explains, then the group adds and challenges.
Devil's advocate on 3: "Can't the signer still change the txid?" (Only by changing inputs or outputs, which needs a new signature anyway.)
-->

---

# Exercise walkthrough: label it

```bash
RAW=$(bitcoin-cli -regtest getrawtransaction "$TXID")
echo "$RAW" | fold -w2 | paste -sd' '
echo "${RAW:14:64}"   # prev txid as stored
echo "${RAW: -8}"     # locktime
hash256 "$RAW"        # = wtxid
```

<!--
Exercise driver shares screen with their labelled transaction (core exercise 1, lab steps 2-7).
The group calls out each field in order. Count bytes at the end: must equal size.
Mention the Python lab: python3 week-03/check.py from decoding-bitcoin/.
-->

---

# Takeaways

- Every byte has a field; labels must add up
- Little-endian numbers, reversed txid display
- Compact size keeps counts small
- Witness is outside the txid: no malleability

<!--
Summariser reads back takeaways. Collect open questions for next week.
-->

---

# Before next Monday

Week 4: Building a transaction and paying the fee

- [Creating a Transaction](https://bitcoindevs.xyz/decoding/transaction-creation)
- [Fee Calculation](https://bitcoindevs.xyz/decoding/fee-calculation)
- Claim your question and next week's roles
- Finish the Python parser lab if you can

<!--
Next week we use the byte knowledge to calculate weight and fees by hand.
Assign roles for week 4.
-->

---

# Thank you

- Summariser posts takeaways tomorrow
- Share your labelled hex on Discord
- See you next Monday

<!--
End on time.
-->
