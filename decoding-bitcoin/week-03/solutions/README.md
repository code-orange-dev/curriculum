# Week 3 solutions

[Week 3 overview](../README.md) · [Exercises](../exercises/README.md) · [Syllabus](../../README.md)

Try the questions yourself before reading these. They are model answers, not the only correct answers.

## Discussion questions

### 1. What is little-endian, and where does it trip people up when reading a txid?

Little-endian means a multi-byte number is stored with its least significant byte first. The number 1 as a 4-byte little-endian integer is `01 00 00 00`, and 150,000,000 (0x08F0D180) as 8 bytes is `80 d1 f0 08 00 00 00 00`. Bitcoin uses little-endian for version, vout index, sequence, amounts and locktime.

The txid is the classic trap. A txid is a 32-byte hash. Inside transactions and blocks, the hash bytes are stored in the order the hash function produced them. But when people display a txid (in Bitcoin Core, block explorers and wallets), the bytes are shown reversed, as if the hash were one big little-endian number. So the previous txid inside an input looks like the reverse of the txid you would search for. If you copy it straight from the raw hex into mempool.space, you find nothing. Block hashes have the same issue, which is also why displayed block hashes start with zeros.

### 2. What is a compact size (varint), and why does Bitcoin use one?

A compact size is a variable-length way to write an unsigned integer:

| Value | Encoding |
|---|---|
| 0 to 252 | 1 byte: the value itself |
| 253 to 0xffff | `fd` + 2 bytes little-endian |
| 0x10000 to 0xffffffff | `fe` + 4 bytes little-endian |
| larger | `ff` + 8 bytes little-endian |

It is used for counts and lengths: input count, output count, script lengths, witness item counts and item lengths, and the number of transactions in a block.

Almost all these numbers are small. Most transactions have 1 or 2 inputs, and most scripts are under 100 bytes. A fixed 4-byte or 8-byte field would waste 3 to 7 bytes every time, in every transaction, stored forever by every node and paid for in fees. With compact size, the common case costs 1 byte, but large values are still possible. Note: Bitcoin Core's source code also has a different "VarInt" format (used in its database), so "compact size" is the clearer name.

### 3. What does segwit move into the witness, and why does that fix malleability?

Segwit moves the unlocking data of segwit inputs (signatures, public keys, and for script spends the script and its arguments) out of the scriptSig and into a separate witness section. For a native segwit input, the scriptSig is empty.

The txid is calculated from the transaction without the witness. Before segwit, the signature was inside the scriptSig, so it was part of the data hashed for the txid. Signatures could be changed in small ways without making them invalid, for example by flipping the ECDSA S value to N - S, or by changing how the data is pushed. Anyone who relayed the transaction could do this, which gave the same payment a different txid. Any later transaction that spent its outputs by the old txid became invalid.

With segwit, those changes only affect the witness, which the txid does not cover. The txid only changes if the inputs, outputs, version or locktime change, and the signature commits to all of those. So a third party can no longer change the txid. Legacy inputs are still malleable, even inside a segwit transaction.

### 4. What is nLockTime for? Give a real situation.

nLockTime is the last 4 bytes of a transaction. It says the earliest point at which the transaction can be included in a block. If the value is below 500,000,000, it is a block height. Otherwise it is a Unix timestamp (compared with the median time of the last 11 blocks, BIP113). A value of 0 means no restriction. The lock only applies if at least one input has a sequence number below `0xffffffff`.

Real situations:

- **Anti fee sniping.** Bitcoin Core sets the locktime to the current block height. Then the transaction can't be put in a block that replaces the current tip, which removes a small incentive for miners to reorg the chain to steal fees.
- **Pre-signed backups and inheritance.** You sign a transaction that sends coins to your heir with a locktime one year ahead. They can't broadcast it before then, and you can cancel it at any time by spending the coins first.
- **Refunds in contracts.** Early payment channels used a pre-signed refund transaction locked until a future time, so a party could get their money back if the other disappeared.

### 5. What are the marker and flag bytes, and how does a parser know a transaction is segwit?

In the segwit serialization (BIP144), two bytes come right after the 4-byte version: the marker `00` and the flag `01`. They tell the parser that witness data follows the outputs.

A parser reads the version, then looks at the next byte. In the old format, that byte is the input count. An input count of 0 is never valid for a real transaction, so a `00` there can safely mean "this is the extended format". The parser then checks the flag (`01`; other values are reserved for future use), reads inputs and outputs as normal, then reads one witness for each input, and finally the locktime.

If the byte after the version is not `00`, it is the input count of a legacy-format transaction with no witness. A transaction with no segwit inputs is always sent in the old format, without marker and flag. Old nodes that don't understand segwit receive transactions without the witness, which still look valid to them.

### 6. How is a txid calculated, and why is a wtxid different?

The txid is the double SHA-256 (hash256) of the transaction serialized in the old format: version, inputs, outputs and locktime, without the marker, flag and witness. It is displayed with the bytes reversed.

The wtxid is the hash256 of the full serialization, including marker, flag and witness. For a transaction with no witness the two are identical, because the serializations are the same.

They differ because they have different jobs. The txid is how outputs are referenced (outpoints use it), so it must not depend on the witness, otherwise malleability returns. But nodes also need to commit to the witness data, so that a block can't have its witnesses swapped. So blocks contain a second Merkle tree built from wtxids, and its root is committed in an output of the coinbase transaction (the witness commitment). The coinbase's own wtxid is taken as all zeros in that tree. Nodes also use wtxids to announce and request transactions on the P2P network (BIP339).

## Core exercises

### 1. Label every field

For a typical Bitcoin Core wallet transaction (1 P2WPKH input, 2 P2WPKH outputs), the hex splits like this:

```
02000000                              version 2
00                                    marker
01                                    flag
01                                    input count: 1
<64 hex chars>                        prev txid (internal byte order)
<8 hex chars, e.g. 00000000>          vout, little-endian (here 0)
00                                    scriptSig length: 0 (native segwit)
fdffffff                              sequence 0xfffffffd (signals RBF)
02                                    output count: 2
<16 hex chars>                        value in sats, little-endian
16                                    scriptPubKey length: 22
0014<40 hex chars>                    OP_0 + push 20 bytes (P2WPKH)
<16 hex chars> 16 0014<40 hex chars>  second output, same shape
02                                    witness for input 0: 2 items
47 <142 hex chars>                    signature (71 bytes, ends in 01 = SIGHASH_ALL)
21 <66 hex chars>                     compressed public key (33 bytes, starts 02 or 03)
<8 hex chars>                         locktime, little-endian
```

That is 4 + 1 + 1 + 1 + 41 + 1 + 31 + 31 + 1 + 72 + 34 + 4 = 222 bytes. If the signature is 72 bytes (length byte `48`), it is 223. Your total should match `size` from `decoderawtransaction`. A mainnet transaction with different input types will look different, but every byte must belong to a field.

### 2. Reverse a txid

The 32 bytes in the input, reversed, give the txid that mempool.space shows. Searching with the unreversed bytes finds nothing (or, in theory, a different transaction). The `vout` field tells you which output of that transaction is being spent, counting from 0.

### 3. Legacy versus segwit

For the legacy transaction, weight = 4 × size exactly, and vsize = size. All its bytes, including the signatures in the scriptSig, are non-witness data, and non-witness bytes count 4 weight units each.

For the segwit transaction, weight is less than 4 × size. The marker, flag and witness (signatures and public keys) count only 1 weight unit per byte. Example with 1 input and 2 outputs: a P2PKH transaction is about 225 bytes, weight 900, 225 vB. A P2WPKH transaction is about 222 bytes, weight about 561, 141 vB. The sizes in bytes are almost the same, but the segwit one costs about 37% less in fees at the same fee rate.

## Hands-on lab answers

**Step 1.** SHA-256 produces bytes in a certain order, but Bitcoin displays txids and block hashes reversed. `[::-1]` reverses them so the output matches what `bitcoin-cli` shows. Without it, you get the internal byte order, the one that appears inside raw transactions and blocks.

**Step 2.** `02000000` = version 2, `00` = marker, `01` = flag, `01` = one input. You know it is segwit because the byte after the version is `00` followed by `01`. In the legacy format this byte would be the input count, and 0 inputs is impossible.

**Step 3.** `vout` is a 4-byte little-endian number, often `00000000` (0) or `01000000` (1), depending on which output of the previous transaction was the coin. The scriptSig is empty (`00`) because a native segwit input puts its signature and public key in the witness. `fdffffff` is sequence 0xfffffffd: below 0xfffffffe, so it signals replaceability (BIP125) and lets the locktime apply. Its top bit is set, so it does not create a relative timelock.

**Step 4.** `80d1f00800000000` appears once, at the start of the 1.5 BTC output. After it comes `16` (22, the script length) and the 22-byte scriptPubKey `0014` + 20 bytes. `00` is OP_0 (witness version 0) and `14` means "push the next 20 bytes", which is the HASH160 of the public key. So this is a P2WPKH output.

**Step 5.** The reversed txid matches `${RAW:14:64}`. Explorers expect the displayed (reversed) form, so a txid copied from raw bytes looks valid but finds nothing.

**Step 6.** The locktime is usually equal to the block count you printed in step 2 (for example `66000000` = 102). Bitcoin Core sets it to the current height so the transaction can only go in the next block or later. This is anti fee sniping: it makes it a bit less attractive for a miner to re-mine the current tip to take its fees. Sometimes (about 1 time in 10) Core picks a slightly lower height, so that transactions which were delayed don't stand out.

**Step 7.** Your hash matches `hash` (the wtxid), not `txid`. You hashed the full serialization including marker, flag and witness. The txid is the hash of the transaction without those parts.

**Step 8.** The legacy transaction starts `02000000 01`: no marker and flag, and the input count comes straight after the version. `hash256` now matches the txid, and `txid` and `hash` are equal, because there is no witness to leave out. The scriptSig is usually `6a` (106 bytes) long and contains two pushes: `47` + a 71-byte signature (DER signature plus the sighash byte `01`), and `21` + a 33-byte compressed public key. (`6b` and `48` if the signature is 72 bytes.)

**Step 9.** The legacy transaction's txid changes when it is signed, because the signature goes into the scriptSig, which is part of the txid. The segwit transaction's txid is the same before and after signing, because the signature goes into the witness. This matters for chains of pre-signed transactions. In Lightning, the two parties sign a refund (commitment) transaction that spends the funding transaction before the funding transaction is broadcast. That only works if the funding txid can't change. With malleable txids, the refund could become invalid and the funds could be stuck.

**Step 10.**

| Value | Compact size |
|---|---|
| 1 | `01` |
| 22 | `16` |
| 252 | `fc` |
| 253 | `fdfd00` |
| 300 | `fd2c01` |
| 70000 | `fe70110100` |

### Python lab

A reference solution is in [`parse_tx.py`](parse_tx.py) in this folder (grade it with `python3 week-03/check.py --solution`). When `python3 week-03/check.py` passes, your parser should give the same version, inputs, outputs, witness items, locktime, txid and wtxid as `decoderawtransaction` for `$RAW`.

### Stretch answers

**A.** You remove 2 bytes (marker and flag) plus the witness: 1 byte item count, 1 + 71 (or 72) bytes of signature, 1 + 33 bytes of public key = 107 or 108 bytes. So 109 or 110 bytes in total. The hash256 of what is left equals the txid. The check works: for 222 bytes and weight 561, the base size is (561 - 222) / 3 = 113, and 222 - 113 = 109.

**B.** 253 payments plus 1 change output = 254 outputs. The output count is `fdfe00`: 3 bytes (`fd` then 254 = 0x00fe little-endian). If the wallet made no change, it would be 253 = `fdfd00`.

**C.** A coinbase input has a previous txid of all zeros and vout `ffffffff`. Its scriptSig starts with the block height (required by BIP34), followed by any extra data the miner wants. Coinbase transactions in blocks made by Bitcoin Core on regtest usually also have a witness: one 32-byte item of zeros (the witness reserved value), which goes with the witness commitment in an `OP_RETURN` output.

## Bonus questions

From the earlier version of this course.

### What is transaction malleability? Why was it a problem, and how did SegWit fix it?

Transaction malleability means that someone can change a transaction's bytes, and so its txid, without making it invalid and without changing what it does: the same inputs are spent and the same outputs are paid. Before segwit, a third party could do this by changing signature encoding details, for example replacing S with N - S in an ECDSA signature or adding extra pushes in the scriptSig, because the signature can't sign itself.

Problems it caused:

- **Wallets and exchanges that tracked payments by txid** got confused. When a malleated version confirmed, the original txid never appeared, and a careless system might think the payment failed and pay again. In 2014, Mt. Gox blamed malleability for withdrawal problems.
- **Chains of unconfirmed or pre-signed transactions broke.** A child transaction names its parent by txid. If the parent confirms with a different txid, the child is invalid. This made payment channels like Lightning unsafe, because their refund transactions are signed before the funding transaction confirms.

Several soft forks and policies reduced the ways to malleate (BIP66 strict DER encoding, low-S as a relay policy, BIP147 NULLDUMMY). SegWit fixed it fully for segwit inputs: signatures and other unlocking data move to the witness, and the txid is calculated without the witness. A third party can't change anything that the txid covers without breaking the signature. The witness is still committed in blocks through the wtxid Merkle tree, so it can't be swapped inside a block either.
