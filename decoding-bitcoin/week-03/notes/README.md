# Week 3 notes

[Week 3 overview](../README.md) · [Exercises](../exercises/README.md) · [Solutions](../solutions/README.md) · [Slides](../slides/slides.md)

## Key ideas

- **A transaction is an exact sequence of bytes.** Everyone must hash and sign exactly the same bytes, so there is one precise format. Each field has a fixed size or a length prefix, and fields always come in the same order. If you can label every byte, you understand the format.

- **Numbers are little-endian.** Version, vout, sequence, amounts and locktime are stored smallest byte first. `02000000` is 2, and `80d1f00800000000` is 150,000,000 satoshis (1.5 BTC). Amounts are always whole satoshis in an 8-byte integer, never decimals.

- **Hashes are displayed reversed.** Inside the transaction, a previous txid is stored in the byte order the hash function produced. Bitcoin software shows txids and block hashes reversed. This difference catches everyone at least once.

- **Compact size saves space.** Counts and lengths use 1 byte when the value is below 253, and a prefix (`fd`, `fe`, `ff`) plus 2, 4 or 8 bytes for bigger values. Most transactions only need the 1-byte form.

- **Segwit adds three things to the format.** A marker `00` and flag `01` after the version, and a witness section after the outputs with one witness (a list of items) for each input. Native segwit inputs have an empty scriptSig. A transaction with no segwit inputs uses the old format.

- **Two IDs: txid and wtxid.** The txid is the hash256 of the transaction without marker, flag and witness. The wtxid includes them. Outpoints use the txid, so changing a signature can't change how later transactions refer to this one. Blocks commit to wtxids through the witness commitment in the coinbase.

- **Locktime and sequence work together.** nLockTime sets the earliest block height (below 500,000,000) or time when the transaction can be mined. It only applies if some input has a sequence below `0xffffffff`. Bitcoin Core sets the locktime to the current height (anti fee sniping), and uses sequence `0xfffffffd`, which also signals replaceability.

## Common mix-ups

| Mix-up | Correction |
|---|---|
| The txid inside an input is the same string you search for on an explorer. | It is stored in internal byte order. Reverse it to get the displayed txid. |
| The txid is the hash of the raw hex I got from `getrawtransaction`. | For a segwit transaction, that gives the wtxid. The txid leaves out marker, flag and witness. |
| Amounts are stored as BTC decimals. | Amounts are 8-byte little-endian integers in satoshis. `bitcoin-cli` converts to BTC for display. |
| A compact size is always 1 byte. | Only for values below 253. 253 and above need `fd`, `fe` or `ff` and more bytes. |
| Segwit transactions put the witness at the end. | The witness comes after the outputs but before the 4-byte locktime. |
| Locktime 0 is special and everything else locks. | Any value works as a lock only if one input's sequence is below `0xffffffff`. Values below 500,000,000 are heights, others are timestamps. |

## Session plan

| Time | Block | Who | Notes |
|---|---|---|---|
| 0:00-0:05 | Welcome and roles | Facilitator | Confirm roles and question owners |
| 0:05-0:15 | Opening question | Facilitator | What must the bytes say? What is not in them? |
| 0:15-0:30 | Concepts | Facilitator | Slides 5-10: reading bytes, compact size, layout, segwit detection, txid vs wtxid, malleability |
| 0:30-1:05 | Question round | Question owners, devil's advocate | 6 questions, about 6 minutes each |
| 1:05-1:20 | Exercise walkthrough | Exercise driver | Label a raw transaction live, then hash it (lab steps 2-7) |
| 1:20-1:27 | Takeaways | Summariser | 3 takeaways, open questions |
| 1:27-1:30 | Before next Monday | Facilitator | Week 4 lessons, roles, Python lab reminder |

## Facilitator tips

Before the session:

- Prepare one raw segwit transaction with your labels, in case the exercise driver's node fails.
- Run lab steps 8 and 9 yourself. The "txid doesn't change after signing" demo is the clearest way to explain malleability.
- Check that the Python lab (`python3 week-03/check.py` from `decoding-bitcoin/`) runs on your machine, so you can help people who try it.

Where people get stuck:

- **Counting hex characters instead of bytes.** Two hex characters are one byte. Offsets in bash substrings (`${RAW:14:64}`) are in characters.
- **Reversing a hex string by characters.** `abcd` reversed by bytes is `cdab`, not `dcba`. Use the `reverse` helper.
- **Assuming one input.** If a wallet transaction has 2 inputs, the fixed offsets in lab step 3 point to the wrong place for the second input. Check `vin` first.
- **Signature lengths.** Signatures are 71 or 72 bytes (including the sighash byte), so length bytes are `47` or `48`. People expect a fixed size.
- **Hashing the hex text instead of the bytes.** `sha256sum` on the hex string hashes ASCII characters. Convert from hex to bytes first, as the Python helper does.

## Glossary

- **Hex:** base-16 text form of bytes. 2 characters per byte.
- **Little-endian:** byte order where the least significant byte comes first.
- **Compact size (varint):** a variable-length integer format used for counts and lengths.
- **Outpoint:** a reference to a previous output: 32-byte txid plus 4-byte vout.
- **scriptSig:** unlocking script inside an input. Empty for native segwit inputs.
- **Sequence:** a 4-byte field in each input. Used for replaceability signalling, relative timelocks (BIP68) and enabling nLockTime.
- **Marker and flag:** the bytes `00 01` after the version in a segwit-format transaction.
- **Witness:** the per-input list of items (signatures, public keys, scripts) outside the txid.
- **nLockTime:** the last 4 bytes. Earliest block height or time for inclusion.
- **hash256:** SHA-256 applied twice. Used for txids, wtxids and block hashes.
- **txid:** hash256 of the transaction without witness data, displayed reversed.
- **wtxid:** hash256 of the full transaction including witness data.
- **Malleability:** changing a transaction's bytes (and txid) without making it invalid.
- **Anti fee sniping:** setting the locktime to the current height so the transaction can't be mined in a re-mined older block.

## Further resources

- [BIP 141: Segregated Witness](https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki): defines the witness, wtxid and the witness commitment.
- [BIP 144: Segregated Witness (peer services)](https://github.com/bitcoin/bips/blob/master/bip-0144.mediawiki): defines the marker, flag and serialization.
- [BIP 113: Median time-past as endpoint for lock-time calculations](https://github.com/bitcoin/bips/blob/master/bip-0113.mediawiki).
- [Bitcoin Optech: Segregated witness](https://bitcoinops.org/en/topics/segregated-witness/) and [Fee sniping](https://bitcoinops.org/en/topics/fee-sniping/).
- [learnmeabitcoin: Transaction](https://learnmeabitcoin.com/technical/transaction/): field-by-field diagrams of transaction structure.
- [Programming Bitcoin](https://github.com/jimmysong/programmingbitcoin): the chapter on transactions builds a transaction parser in Python, a good companion to the week 3 Python lab.
- [Mastering Bitcoin](https://github.com/bitcoinbook/bitcoinbook): the chapter on transactions explains serialization and the segwit format.
