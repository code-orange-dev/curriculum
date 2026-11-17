# Week 4 exercises

[Week 4 overview](../README.md) · [Solutions](../solutions/README.md) · [Syllabus](../../README.md)

This week you calculate fees and sizes yourself instead of trusting the wallet. Do the three core exercises before Monday, then the regtest lab. Keep your numbers: the session compares everyone's results.

## Core exercises

### 1. Fee and fee rate of a real transaction

1. On [mempool.space](https://mempool.space), open any confirmed transaction with 2 or more inputs.
2. Write down every input amount and every output amount, in satoshis.
3. Write down the virtual size (vB) shown in the details.
4. Calculate: fee = sum of inputs - sum of outputs. Then fee rate = fee / vsize.
5. Compare with the fee and fee rate mempool.space shows.

What to write down: the txid, your sums, your fee, your fee rate in sat/vB, and whether it matches. If it doesn't match exactly, explain why (rounding, or you used size instead of vsize?).

### 2. Estimate the vsize of a 1-input, 2-output P2WPKH transaction

Work it out on paper before looking anything up. Use these sizes:

| Part | Bytes | Counts as |
|---|---|---|
| version | 4 | base |
| marker + flag | 2 | witness |
| input count, output count | 1 each | base |
| one input: txid 32 + vout 4 + scriptSig length 1 + sequence 4 | 41 | base |
| one P2WPKH output: value 8 + script length 1 + script 22 | 31 | base |
| one P2WPKH witness: item count 1 + sig length 1 + sig 71 + key length 1 + key 33 | 107 | witness |
| locktime | 4 | base |

Steps:

1. Add up the base bytes and the witness bytes.
2. weight = base × 4 + witness × 1 (the same as base × 3 + total size).
3. vsize = weight / 4, rounded up.
4. Find a real 1-input, 2-output transaction with `bc1q` inputs and outputs on mempool.space and compare.

What to write down: base size, witness size, total size, weight, vsize, and the vsize of the real transaction you found.

### 3. Watch the fee market

1. Open [mempool.space](https://mempool.space) and write down the fee estimates (the "Transaction Fees" box: low, medium, high priority) and the number of unconfirmed transactions.
2. Do it again at least 8 hours later (for example morning and night), or on a weekday and on a weekend.
3. Look at the mempool graph for the last week.

What to write down: both sets of numbers and the time, and your explanation of what changed. Think about: how many transactions were waiting, how long since the last block, the time of day in big markets, and any events (price moves, popular token mints, exchange consolidations).

## Hands-on lab (bitcoin-cli, regtest)

> Tested on Bitcoin Core 29.0 (regtest), November 2026.

This lab uses the setup from weeks 2 and 3: a node started with `-txindex=1 -fallbackfee=0.0001`, and wallets `alice` and `bob`. If you are starting fresh:

```bash
bitcoind -regtest -daemon -txindex=1 -fallbackfee=0.0001
bitcoin-cli -regtest createwallet alice
bitcoin-cli -regtest createwallet bob
bitcoin-cli -regtest -rpcwallet=alice -generate 110
```

You need `jq` and `python3`. Set Bob's address once:

```bash
BOB=$(bitcoin-cli -regtest -rpcwallet=bob getnewaddress)
```

### Step 1: choose your own fee rate

```bash
TXID=$(bitcoin-cli -regtest -rpcwallet=alice -named sendtoaddress address="$BOB" amount=0.5 fee_rate=5)
bitcoin-cli -regtest getmempoolentry "$TXID" | jq '{vsize, weight, fee: .fees.base}'
```

`fee_rate` is in sat/vB.

**Question:** Convert the fee to satoshis and divide by `vsize`. Do you get 5? Why must the wallet know the vsize before it can set the fee?

### Step 2: the same payment, legacy versus segwit

Make one legacy coin and one native segwit coin of 1 BTC each:

```bash
LEG_IN=$(bitcoin-cli -regtest -rpcwallet=alice getnewaddress "" legacy)
SW_IN=$(bitcoin-cli -regtest -rpcwallet=alice getnewaddress "" bech32)
LEG_FUND=$(bitcoin-cli -regtest -rpcwallet=alice sendtoaddress "$LEG_IN" 1)
SW_FUND=$(bitcoin-cli -regtest -rpcwallet=alice sendtoaddress "$SW_IN" 1)
bitcoin-cli -regtest -rpcwallet=alice -generate 1
LEG_VOUT=$(bitcoin-cli -regtest -rpcwallet=alice listunspent 1 9999999 '["'$LEG_IN'"]' | jq '.[0].vout')
SW_VOUT=$(bitcoin-cli -regtest -rpcwallet=alice listunspent 1 9999999 '["'$SW_IN'"]' | jq '.[0].vout')
```

Now spend each coin to two outputs of the same type (0.5 and 0.4999 BTC, so the fee is 0.0001 BTC = 10,000 sats):

```bash
L1=$(bitcoin-cli -regtest -rpcwallet=alice getnewaddress "" legacy)
L2=$(bitcoin-cli -regtest -rpcwallet=alice getnewaddress "" legacy)
S1=$(bitcoin-cli -regtest -rpcwallet=alice getnewaddress "" bech32)
S2=$(bitcoin-cli -regtest -rpcwallet=alice getnewaddress "" bech32)

LEG_RAW=$(bitcoin-cli -regtest createrawtransaction '[{"txid":"'$LEG_FUND'","vout":'$LEG_VOUT'}]' '{"'$L1'":0.5,"'$L2'":0.4999}')
SW_RAW=$(bitcoin-cli -regtest createrawtransaction '[{"txid":"'$SW_FUND'","vout":'$SW_VOUT'}]' '{"'$S1'":0.5,"'$S2'":0.4999}')

LEG_SIGNED=$(bitcoin-cli -regtest -rpcwallet=alice signrawtransactionwithwallet "$LEG_RAW" | jq -r '.hex')
SW_SIGNED=$(bitcoin-cli -regtest -rpcwallet=alice signrawtransactionwithwallet "$SW_RAW" | jq -r '.hex')

bitcoin-cli -regtest decoderawtransaction "$LEG_SIGNED" | jq '{size, vsize, weight}'
bitcoin-cli -regtest decoderawtransaction "$SW_SIGNED" | jq '{size, vsize, weight}'
```

**Question:** Fill in a table with size, vsize and weight for both. Both pay 10,000 sats. What is the fee rate (sat/vB) of each? Which one would a miner prefer, and why?

### Step 3: weight and vsize by hand

Take the segwit transaction. Split its size into base bytes and witness bytes:

```bash
bitcoin-cli -regtest decoderawtransaction "$SW_SIGNED" | jq '.vin[0].txinwitness'
```

The witness bytes are: marker + flag (2) + item count (1) + for each item its length byte plus its bytes.

**Question:** How many witness bytes are there? What is the base size (size minus witness bytes)? Calculate weight = base × 3 + size and vsize = weight / 4 rounded up. Do you match `decoderawtransaction`? Do the same for the legacy transaction: what is its witness size?

Check yourself with Python:

```bash
python3 -c "import math; base=113; total=222; w=base*3+total; print('weight', w, 'vsize', math.ceil(w/4))"
```

(Replace 113 and 222 with your own numbers.)

### Step 4: multiple inputs and outputs, fee by hand

Build a transaction with 2 inputs and 3 outputs, aiming for a fee rate of 20 sat/vB.

```bash
bitcoin-cli -regtest -rpcwallet=alice listunspent | jq '.[] | {txid, vout, address, amount}'
```

Pick two UTXOs whose address starts with `bcrt1q` and write down their amounts:

```bash
IN1_TXID=<txid 1>; IN1_VOUT=<vout 1>   # amount A1
IN2_TXID=<txid 2>; IN2_VOUT=<vout 2>   # amount A2
BOB2=$(bitcoin-cli -regtest -rpcwallet=bob getnewaddress)
CHANGE=$(bitcoin-cli -regtest -rpcwallet=alice getrawchangeaddress)
```

Estimate the vsize first (use your numbers from core exercise 2: about 10.5 vB overhead, about 68 vB per P2WPKH input, 31 vB per P2WPKH output). Then the fee is vsize × 20 sats. The change is A1 + A2 - 1 - 0.5 - fee.

```bash
INPUTS='[{"txid":"'$IN1_TXID'","vout":'$IN1_VOUT'},{"txid":"'$IN2_TXID'","vout":'$IN2_VOUT'}]'
OUTPUTS='{"'$BOB'":1,"'$BOB2'":0.5,"'$CHANGE'":<your change amount>}'
MULTI_RAW=$(bitcoin-cli -regtest createrawtransaction "$INPUTS" "$OUTPUTS")
MULTI_SIGNED=$(bitcoin-cli -regtest -rpcwallet=alice signrawtransactionwithwallet "$MULTI_RAW" | jq -r '.hex')
bitcoin-cli -regtest testmempoolaccept '["'$MULTI_SIGNED'"]'
```

**Question:** What vsize did you estimate, and what does `testmempoolaccept` report? What is the real fee rate (fee in sats / vsize)? If it is not exactly 20, why not? Broadcast it with `sendrawtransaction` when you are happy.

### Step 5: let the wallet do it

```bash
EMPTY=$(bitcoin-cli -regtest createrawtransaction '[]' '{"'$BOB'":3}')
bitcoin-cli -regtest -rpcwallet=alice fundrawtransaction "$EMPTY" '{"fee_rate":20}'
```

The returned `hex` is not signed yet, so it has no witness and its vsize is too small. Sign it before you measure:

```bash
FUNDED=$(bitcoin-cli -regtest -rpcwallet=alice fundrawtransaction "$EMPTY" '{"fee_rate":20}' | jq -r '.hex')
FUNDED_SIGNED=$(bitcoin-cli -regtest -rpcwallet=alice signrawtransactionwithwallet "$FUNDED" | jq -r '.hex')
bitcoin-cli -regtest decoderawtransaction "$FUNDED_SIGNED" | jq '{vsize, inputs: (.vin | length)}'
```

**Question:** How many inputs did the wallet choose, and where did it put the change (`changepos`)? Divide the `fee` from `fundrawtransaction` by the vsize of the signed transaction: is it 20 sat/vB (or just above)? What do you get if you use the vsize of the unsigned hex instead?

### Step 6: speed up with RBF

```bash
LOW=$(bitcoin-cli -regtest -rpcwallet=alice -named sendtoaddress address="$BOB" amount=0.1 fee_rate=1)
bitcoin-cli -regtest getmempoolentry "$LOW" | jq '{vsize, fee: .fees.base}'
bitcoin-cli -regtest -rpcwallet=alice bumpfee "$LOW" '{"fee_rate":10}'
bitcoin-cli -regtest getrawmempool
```

**Question:** What happened to the first transaction? Which txid is in the mempool now? What changed in the new transaction: the payment, the change, or both? Why is the change output the natural place to take the extra fee from?

### Lab: fees in Python

Lab: calculate weight, vsize and fees in Python (`python3 week-04/check.py` from decoding-bitcoin/). You fill in the functions in `week-04/exercises/fees.py`, and the checker tests them. Then use your functions on `$SW_SIGNED` and `$MULTI_SIGNED` and compare with `decoderawtransaction`.

## Stretch tasks

### A. CPFP: the receiver pays

Alice sends Bob a payment with a very low fee. Bob spends his unconfirmed output with a high fee so that miners want both:

```bash
BOB3=$(bitcoin-cli -regtest -rpcwallet=bob getnewaddress)
PARENT=$(bitcoin-cli -regtest -rpcwallet=alice -named sendtoaddress address="$BOB3" amount=1 fee_rate=1)
P_VOUT=$(bitcoin-cli -regtest -rpcwallet=bob listunspent 0 0 '["'$BOB3'"]' | jq '.[0].vout')
BOB4=$(bitcoin-cli -regtest -rpcwallet=bob getnewaddress)
CHILD_RAW=$(bitcoin-cli -regtest createrawtransaction '[{"txid":"'$PARENT'","vout":'$P_VOUT'}]' '{"'$BOB4'":0.9995}')
CHILD_SIGNED=$(bitcoin-cli -regtest -rpcwallet=bob signrawtransactionwithwallet "$CHILD_RAW" | jq -r '.hex')
CHILD=$(bitcoin-cli -regtest sendrawtransaction "$CHILD_SIGNED")
bitcoin-cli -regtest getmempoolentry "$CHILD" | jq '{vsize, fees, ancestorcount, ancestorsize}'
```

**Question:** What is the child's own fee rate, and what is the combined fee rate of parent plus child (total fees / total vsize)? Why does a miner look at the combined rate? Why couldn't Bob use RBF here?

### B. Dust

Try to send a tiny amount:

```bash
bitcoin-cli -regtest -rpcwallet=alice sendtoaddress "$BOB" 0.00000200
```

**Question:** What error do you get? Find the dust limit for a P2WPKH output (Bitcoin Core treats an output as dust if spending it would cost more than it is worth at 3 sat/vB). Is the limit the same for a legacy P2PKH output?

### C. Fee estimation on regtest

```bash
bitcoin-cli -regtest estimatesmartfee 6
```

**Question:** Why does this fail or return an error on a fresh regtest chain? What data does Bitcoin Core need to estimate fees, and why did we need `-fallbackfee`?
