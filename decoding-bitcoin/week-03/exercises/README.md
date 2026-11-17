# Week 3 exercises

[Week 3 overview](../README.md) · [Solutions](../solutions/README.md) · [Syllabus](../../README.md)

This week is all about bytes. Do the three core exercises before Monday, then the regtest lab. Keep a text file open and write the hex and your labels in it: you will share them in the session.

## Core exercises

### 1. Label every field of a raw transaction

1. Get a raw segwit transaction. Use one from your regtest node (lab step 2 below), or on mempool.space pick a transaction whose inputs come from `bc1q...` addresses and copy its raw hex.
2. Paste it into the [Transaction Decoder](https://bitcoindevs.xyz/decoding/transaction-decoder) to see the fields.
3. Now, in your text file, split the hex yourself and write a label next to each piece. Don't skip anything: every byte belongs to some field.

Use this order:

```
version (4) | marker (1) | flag (1) | input count (compact size)
  for each input:  prev txid (32) | vout (4) | scriptSig length | scriptSig | sequence (4)
output count (compact size)
  for each output: value (8) | scriptPubKey length | scriptPubKey
witness: for each input: item count | (item length | item) ...
locktime (4)
```

What to write down:

- Each field's hex and its meaning in plain numbers (for example `02000000` = version 2, `80d1f00800000000` = 150,000,000 sats).
- The total number of bytes you labelled. It should equal the transaction's `size`.

### 2. Reverse a txid

1. In your labelled transaction, take the 32-byte previous txid from the first input exactly as it appears in the hex.
2. Reverse the byte order: take the hex two characters at a time and write the pairs in reverse order (or use the one-liner in lab step 5).
3. Search for the result on [mempool.space](https://mempool.space) (or with `getrawtransaction` on regtest).

What to write down: the txid as it appears in the raw bytes, the reversed version, and whether mempool.space found the transaction with each version. Which output of that transaction is spent?

### 3. Compare a legacy and a segwit transaction

1. On mempool.space, find a transaction whose inputs are all legacy (addresses starting with `1`). Find another whose inputs are native segwit (`bc1q...`). Try to pick two with the same number of inputs and outputs.
2. For each, write down: size (bytes), virtual size (vB) and weight (WU), as shown in the transaction details.
3. Work out weight / size for each.

What to write down: the numbers, and an explanation of why weight is exactly 4 times the size for the legacy transaction but less than 4 times for the segwit one. (Week 4 covers weight in detail. Here, focus on which bytes are in the witness.)

## Hands-on lab (bitcoin-cli, regtest)

This lab builds on the week 2 setup: a regtest node started with `-txindex=1 -fallbackfee=0.0001` and a wallet called `alice` with mature coins. If you are starting fresh:

```bash
bitcoind -regtest -daemon -txindex=1 -fallbackfee=0.0001
bitcoin-cli -regtest createwallet alice
bitcoin-cli -regtest -rpcwallet=alice -generate 101
```

If `alice` exists but is not loaded, run `bitcoin-cli -regtest loadwallet alice`. You need `jq` and `python3`.

### Step 1: a helper for double SHA-256

Bitcoin hashes transactions with SHA-256 twice (hash256). Save this helper in your shell:

```bash
hash256() { python3 -c "import sys,hashlib; b=bytes.fromhex(sys.argv[1]); print(hashlib.sha256(hashlib.sha256(b).digest()).digest()[::-1].hex())" "$1"; }
reverse() { python3 -c "import sys; print(bytes.fromhex(sys.argv[1])[::-1].hex())" "$1"; }
```

`hash256` prints the hash in reversed byte order, the way Bitcoin displays txids. `reverse` flips the byte order of any hex string.

**Question:** Why does the helper end with `[::-1]`? What would you see without it?

### Step 2: make a segwit transaction and get its bytes

```bash
ADDR=$(bitcoin-cli -regtest -rpcwallet=alice getnewaddress)
TXID=$(bitcoin-cli -regtest -rpcwallet=alice sendtoaddress "$ADDR" 1.5)
bitcoin-cli -regtest getblockcount
RAW=$(bitcoin-cli -regtest getrawtransaction "$TXID")
echo "$RAW"
bitcoin-cli -regtest decoderawtransaction "$RAW"
```

To see the bytes in pairs, run `echo "$RAW" | fold -w2 | paste -sd' '`.

**Question:** Label the first 7 bytes (`02000000 00 01 01`). How do you know from these bytes alone that this is a segwit transaction?

### Step 3: find the input fields

The first input starts right after the input count. In hex characters (2 per byte), the version is characters 0-7, marker and flag 8-11, input count 12-13. So:

```bash
echo "prev txid: ${RAW:14:64}"
echo "vout:      ${RAW:78:8}"
echo "scriptSig length: ${RAW:86:2}"
echo "sequence:  ${RAW:88:8}"
```

This only works if the input count is 1 byte and the scriptSig is empty, which is true for this wallet transaction. Check `vin` in the decoded output to be sure there is only one input.

**Question:** What is the `vout` value as a number? Why is the scriptSig length `00`? What does the sequence `fdffffff` mean?

### Step 4: little-endian amounts

Find the outputs. Each starts with an 8-byte amount in satoshis, little-endian.

```bash
python3 -c "print((150000000).to_bytes(8, 'little').hex())"
echo "$RAW" | grep -o 80d1f00800000000
```

**Question:** Where in the hex is the 1.5 BTC amount? What comes right after it (the length and the scriptPubKey)? What does `0014` at the start of the scriptPubKey mean?

### Step 5: reverse the txid

```bash
PREV_TXID=$(bitcoin-cli -regtest getrawtransaction "$TXID" true | jq -r '.vin[0].txid')
echo "displayed txid:    $PREV_TXID"
echo "reversed:          $(reverse "$PREV_TXID")"
echo "bytes in the hex:  ${RAW:14:64}"
```

**Question:** Which version matches the bytes inside the transaction? Why do people get confused when they search a block explorer with a txid copied from raw bytes?

### Step 6: the locktime

```bash
echo "locktime bytes: ${RAW: -8}"
python3 -c "import sys; print(int.from_bytes(bytes.fromhex(sys.argv[1]), 'little'))" "${RAW: -8}"
```

**Question:** What number is it? Compare it to the block count you printed in step 2. Why does Bitcoin Core put this number here?

### Step 7: compute the wtxid by hand

```bash
hash256 "$RAW"
bitcoin-cli -regtest decoderawtransaction "$RAW" | jq -r '.txid, .hash'
```

**Question:** Your hash matches one of the two. Which one, and why does it not match the other?

### Step 8: a legacy transaction, where txid = hash of all bytes

Make a legacy (P2PKH) coin, then spend it to another legacy address. A transaction with no segwit inputs has no witness, so it has no marker or flag.

```bash
LEG1=$(bitcoin-cli -regtest -rpcwallet=alice getnewaddress "" legacy)
LEG2=$(bitcoin-cli -regtest -rpcwallet=alice getnewaddress "" legacy)
FUND_TXID=$(bitcoin-cli -regtest -rpcwallet=alice sendtoaddress "$LEG1" 1)
bitcoin-cli -regtest -rpcwallet=alice -generate 1
LEG_VOUT=$(bitcoin-cli -regtest -rpcwallet=alice listunspent 1 9999999 '["'$LEG1'"]' | jq '.[0].vout')

LEG_RAW=$(bitcoin-cli -regtest createrawtransaction '[{"txid":"'$FUND_TXID'","vout":'$LEG_VOUT'}]' '{"'$LEG2'":0.9999}')
LEG_SIGNED=$(bitcoin-cli -regtest -rpcwallet=alice signrawtransactionwithwallet "$LEG_RAW" | jq -r '.hex')
echo "$LEG_SIGNED"
hash256 "$LEG_SIGNED"
bitcoin-cli -regtest decoderawtransaction "$LEG_SIGNED" | jq -r '.txid, .hash'
```

**Question:** How do the first bytes differ from the segwit transaction? Does `hash256` match the txid now? Find the scriptSig: how long is it, and what two things are pushed in it?

### Step 9: malleability in one command

The txid of a legacy transaction covers the scriptSig, which contains the signature. The txid of a segwit transaction does not cover the witness. Compare the txid before and after signing:

```bash
# Legacy: compare unsigned and signed
bitcoin-cli -regtest decoderawtransaction "$LEG_RAW" | jq -r .txid
bitcoin-cli -regtest decoderawtransaction "$LEG_SIGNED" | jq -r .txid

# Segwit: build and sign a transaction that spends a P2WPKH coin
SW1=$(bitcoin-cli -regtest -rpcwallet=alice getnewaddress "" bech32)
SW2=$(bitcoin-cli -regtest -rpcwallet=alice getnewaddress "" bech32)
SW_FUND=$(bitcoin-cli -regtest -rpcwallet=alice sendtoaddress "$SW1" 1)
bitcoin-cli -regtest -rpcwallet=alice -generate 1
SW_VOUT=$(bitcoin-cli -regtest -rpcwallet=alice listunspent 1 9999999 '["'$SW1'"]' | jq '.[0].vout')
SW_RAW=$(bitcoin-cli -regtest createrawtransaction '[{"txid":"'$SW_FUND'","vout":'$SW_VOUT'}]' '{"'$SW2'":0.9999}')
SW_SIGNED=$(bitcoin-cli -regtest -rpcwallet=alice signrawtransactionwithwallet "$SW_RAW" | jq -r '.hex')
bitcoin-cli -regtest decoderawtransaction "$SW_RAW" | jq -r .txid
bitcoin-cli -regtest decoderawtransaction "$SW_SIGNED" | jq -r .txid
```

**Question:** For which transaction does the txid change when the signature is added? Why does this matter for a chain of transactions that are signed before the first one is confirmed (for example in the Lightning Network)?

### Step 10: compact size in action

Look at the scriptPubKey length byte before each output script in `$RAW` (`16` = 22 bytes for P2WPKH) and the witness item lengths (`47` or `48` for a signature, `21` for a 33-byte public key).

**Question:** Write the compact size encoding for these numbers: 1, 22, 252, 253, 300, 70000. (Rules: below 253 = 1 byte; up to 0xffff = `fd` + 2 bytes; up to 0xffffffff = `fe` + 4 bytes; above = `ff` + 8 bytes. All little-endian.)

### Lab: parse a real transaction in Python

Lab: parse a real transaction in Python (`python3 week-03/check.py` from decoding-bitcoin/). You fill in a parser in `week-03/exercises/parse_tx.py`, and the checker tests it against real transactions. When it passes, run your parser on `$RAW` from step 2 and compare with `decoderawtransaction`.

## Stretch tasks

### A. Strip the witness and compute the txid of a segwit transaction

Take `$SW_SIGNED` from step 9. Remove the marker and flag (`0001` after the version) and the whole witness section (just before the last 4 bytes of locktime). Hash what is left with `hash256`. It should equal the txid. Tip: for one P2WPKH input the witness is `02`, then a signature with its length byte, then `21` and a 33-byte public key, so 107 or 108 bytes.

**Question:** How many bytes did you remove in total? Check it with the numbers from `decoderawtransaction "$SW_SIGNED"`: the stripped (base) size is (`weight` - `size`) / 3, and you should have removed `size` minus that.

### B. A transaction with more than 252 outputs

```bash
OUTS=$(for i in $(seq 1 253); do printf '"%s":0.001\n' "$(bitcoin-cli -regtest -rpcwallet=alice getnewaddress)"; done | paste -sd, -)
BIG_TXID=$(bitcoin-cli -regtest -rpcwallet=alice sendmany "" "{$OUTS}")
BIG_RAW=$(bitcoin-cli -regtest getrawtransaction "$BIG_TXID")
bitcoin-cli -regtest decoderawtransaction "$BIG_RAW" | jq '.vout | length'
```

**Question:** How many outputs are there (remember change)? Find the output count in the hex. How many bytes does it take, and what are they?

### C. Look at a coinbase transaction

```bash
CB=$(bitcoin-cli -regtest getblock "$(bitcoin-cli -regtest getbestblockhash)" | jq -r '.tx[0]')
bitcoin-cli -regtest getrawtransaction "$CB" true
```

**Question:** What is the previous txid and vout of a coinbase input? What is in its scriptSig (hint: BIP34 requires one thing at the start)? Does it have a witness?
