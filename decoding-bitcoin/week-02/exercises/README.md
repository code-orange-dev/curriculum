# Week 2 exercises

[Week 2 overview](../README.md) · [Solutions](../solutions/README.md) · [Syllabus](../../README.md)

Do the three core exercises before Monday. The hands-on lab is where the ideas really stick, so try at least steps 1 to 7. Write your answers down: you will explain them to the group.

## Core exercises

### 1. Watch a transaction confirm on mempool.space

1. Open [mempool.space](https://mempool.space). The blocks on the left of the top bar are "projected" blocks built from the mempool. The ones on the right are mined blocks.
2. Click the first projected block and pick a transaction near the top (a high fee rate, so it should confirm soon). Note the time and copy its txid.
3. Keep the transaction page open. Wait until it shows "Confirmed" with 1 confirmation.
4. Optional: pick a second transaction from the bottom of a projected block further back (low fee rate) and follow it too.

What to write down:

- The txid, the fee rate (sat/vB), the time you first saw it and the time it confirmed.
- How long it took, and how that compares to the average 10 minutes between blocks.
- If you followed a low-fee transaction: did it confirm in the next block? Why not?

### 2. Use the Reorg Calculator

Open the [Reorg Calculator](https://bitcoindevs.xyz/decoding/reorg-calculator).

1. Set the attacker's share of the hashrate to 10%.
2. Read the chance of a successful reversal after 1, 3 and 6 confirmations.
3. Repeat with 30% and with 45%.

What to write down:

- A small table: attacker hashrate (10%, 30%, 45%) against confirmations (1, 3, 6).
- How quickly the risk drops with more confirmations at 10%, and at 45%.
- How many confirmations you would want before handing over a coffee, a laptop and a car. Give a reason for each.

### 3. Read a transaction with the Transaction Decoder

Open the [Transaction Decoder](https://bitcoindevs.xyz/decoding/transaction-decoder).

1. Get a raw transaction. Either use the example in the tool, or on mempool.space open any transaction, and copy its raw hex (on mempool.space, find the hex in the transaction details), or use one from your regtest node (`bitcoin-cli -regtest getrawtransaction <txid>`).
2. Paste it into the decoder.
3. Find the four main parts: version, inputs, outputs, locktime.
4. For each input, find the txid and output index (vout) it points to.
5. Look up one of those previous transactions on mempool.space and find the output that is being spent.

What to write down: the version number, the number of inputs and outputs, the locktime, and for each input "txid:vout" plus the amount of the output it spends.

## Hands-on lab (bitcoin-cli, regtest)

You need Bitcoin Core v29 or newer. If you have not installed it yet, follow [`week-01/exercises/bitcoin_core_cli.md`](../../week-01/exercises/bitcoin_core_cli.md). Some steps use `jq` to pick fields out of JSON. Install it with `sudo apt install jq` (Linux) or `brew install jq` (macOS).

The lab keeps values in shell variables like `$TXID`. If you open a new terminal, set them again.

### Step 1: start a fresh regtest node with two wallets

If you have an old regtest chain, you can start fresh: `bitcoin-cli -regtest stop`, then delete the regtest folder (`~/.bitcoin/regtest` on Linux).

```bash
bitcoind -regtest -daemon -txindex=1 -fallbackfee=0.0001
bitcoin-cli -regtest createwallet alice
bitcoin-cli -regtest createwallet bob
bitcoin-cli -regtest -rpcwallet=alice -generate 101
bitcoin-cli -regtest -rpcwallet=alice getbalance
```

With two wallets loaded, every wallet command needs `-rpcwallet=<name>`.

**Question:** Alice's balance is 50 BTC. Which block's reward is that, and why can't she spend the other 100 rewards yet?

### Step 2: look at the empty mempool

```bash
bitcoin-cli -regtest getmempoolinfo
bitcoin-cli -regtest getrawmempool
```

**Question:** What are `size` and `bytes`? What is `mempoolminfee`, and what does it mean for a transaction that pays less than this?

### Step 3: Alice pays Bob, and we watch the mempool

```bash
BOB_ADDR=$(bitcoin-cli -regtest -rpcwallet=bob getnewaddress)
TXID=$(bitcoin-cli -regtest -rpcwallet=alice sendtoaddress "$BOB_ADDR" 1)
echo "$TXID"

bitcoin-cli -regtest getmempoolinfo
bitcoin-cli -regtest getrawmempool
bitcoin-cli -regtest getmempoolentry "$TXID"
```

Tip: in a second terminal, run `watch -n 1 bitcoin-cli -regtest getmempoolinfo` and keep it open for the rest of the lab.

**Question:** In `getmempoolentry`, what are `vsize`, `weight`, `time`, `height` and `fees.base`? Work out the fee rate in sat/vB from `fees.base` and `vsize`. Is it close to the 10 sat/vB set by `-fallbackfee`?

### Step 4: Bob's view of an unconfirmed payment

```bash
bitcoin-cli -regtest -rpcwallet=bob getbalances
bitcoin-cli -regtest -rpcwallet=bob listunspent 0
```

**Question:** Why does Bob's 1 BTC show as `untrusted_pending` and not `trusted`? Should Bob hand over goods now?

### Step 5: follow the input back

```bash
bitcoin-cli -regtest getrawtransaction "$TXID" true
```

Find `vin[0].txid` and `vin[0].vout` in the output, then look at that previous transaction:

```bash
PREV=$(bitcoin-cli -regtest getrawtransaction "$TXID" true | jq -r '.vin[0].txid')
bitcoin-cli -regtest getrawtransaction "$PREV" true
```

**Question:** What kind of transaction is `$PREV`? Which output of it does Alice's payment spend, and how much was it worth? How many outputs does Alice's payment have, and which one is the change?

### Step 6: mine a block and confirm

```bash
bitcoin-cli -regtest -rpcwallet=alice -generate 1
bitcoin-cli -regtest getmempoolinfo
bitcoin-cli -regtest -rpcwallet=alice gettransaction "$TXID"
bitcoin-cli -regtest -rpcwallet=bob getbalances
```

**Question:** What happened to the mempool? Which fields in `gettransaction` changed? What is Bob's balance now, and in which balance category?

### Step 7: build a transaction by hand

Now do what the wallet did for you, step by step. First pick a coin to spend:

```bash
bitcoin-cli -regtest -rpcwallet=alice listunspent
```

Choose a UTXO with `"amount": 50.00000000` (a matured coinbase reward) and copy its `txid` and `vout`:

```bash
IN_TXID=<paste txid here>
IN_VOUT=<paste vout here>
BOB_ADDR2=$(bitcoin-cli -regtest -rpcwallet=bob getnewaddress)
CHANGE_ADDR=$(bitcoin-cli -regtest -rpcwallet=alice getrawchangeaddress)
```

We pay Bob 2 BTC, pay a fee of 0.0001 BTC, and send the rest back to Alice: 50 - 2 - 0.0001 = 47.9999 BTC.

```bash
INPUTS='[{"txid":"'$IN_TXID'","vout":'$IN_VOUT'}]'
OUTPUTS='{"'$BOB_ADDR2'":2,"'$CHANGE_ADDR'":47.9999}'
RAW=$(bitcoin-cli -regtest createrawtransaction "$INPUTS" "$OUTPUTS")
bitcoin-cli -regtest decoderawtransaction "$RAW"
```

**Question:** The transaction is not signed yet. What is missing in `vin[0]` compared with the transaction from step 5? Where is the fee written?

Now sign it and test it without broadcasting:

```bash
SIGNED=$(bitcoin-cli -regtest -rpcwallet=alice signrawtransactionwithwallet "$RAW" | jq -r '.hex')
bitcoin-cli -regtest testmempoolaccept '["'$SIGNED'"]'
```

**Question:** Is it `allowed`? What `vsize` and `fees` does `testmempoolaccept` report? What fee rate is that in sat/vB?

### Step 8: the classic mistake (don't broadcast this one)

What if you forget the change output?

```bash
BAD_OUTPUTS='{"'$BOB_ADDR2'":2}'
BAD_RAW=$(bitcoin-cli -regtest createrawtransaction "$INPUTS" "$BAD_OUTPUTS")
BAD_SIGNED=$(bitcoin-cli -regtest -rpcwallet=alice signrawtransactionwithwallet "$BAD_RAW" | jq -r '.hex')
bitcoin-cli -regtest testmempoolaccept '["'$BAD_SIGNED'"]'
```

**Question:** Why is it rejected? If a node accepted it, who would get the other 48 BTC? What protects you here, and would it protect you if the mistake were smaller?

### Step 9: broadcast the good transaction

```bash
MANUAL_TXID=$(bitcoin-cli -regtest sendrawtransaction "$SIGNED")
echo "$MANUAL_TXID"
bitcoin-cli -regtest getmempoolentry "$MANUAL_TXID"
```

**Question:** Why can `sendrawtransaction` run without `-rpcwallet`? (Hint: is any secret needed at this point?)

### Step 10: a child that spends an unconfirmed parent

The change output of your manual transaction is output 1 (outputs keep the order you gave them). Spend it before it is confirmed:

```bash
CHILD_INPUTS='[{"txid":"'$MANUAL_TXID'","vout":1}]'
CHILD_OUTPUTS='{"'$BOB_ADDR2'":47.9998}'
CHILD_RAW=$(bitcoin-cli -regtest createrawtransaction "$CHILD_INPUTS" "$CHILD_OUTPUTS")
CHILD_SIGNED=$(bitcoin-cli -regtest -rpcwallet=alice signrawtransactionwithwallet "$CHILD_RAW" | jq -r '.hex')
CHILD_TXID=$(bitcoin-cli -regtest sendrawtransaction "$CHILD_SIGNED")

bitcoin-cli -regtest getrawmempool true
bitcoin-cli -regtest getmempoolentry "$CHILD_TXID"
bitcoin-cli -regtest getmempoolentry "$MANUAL_TXID"
```

**Question:** Look at `depends`, `spentby`, `ancestorcount` and `descendantcount`. How does the mempool know these two transactions are linked? What would happen to the child if the parent were never mined?

### Step 11: confirm both together

```bash
bitcoin-cli -regtest -rpcwallet=alice -generate 1
bitcoin-cli -regtest getblock "$(bitcoin-cli -regtest getbestblockhash)" 1 | jq '.tx'
bitcoin-cli -regtest -rpcwallet=bob getbalances
```

**Question:** How many transactions are in the new block, and in what order? Can a child ever come before its parent in a block?

## Stretch tasks

### A. Simulate a reorg

`invalidateblock` tells your node to treat a block as invalid, which is like a reorg that removes it.

```bash
BEST=$(bitcoin-cli -regtest getbestblockhash)
bitcoin-cli -regtest invalidateblock "$BEST"
bitcoin-cli -regtest getmempoolinfo
bitcoin-cli -regtest -rpcwallet=alice gettransaction "$CHILD_TXID"
bitcoin-cli -regtest reconsiderblock "$BEST"
bitcoin-cli -regtest getblockcount
```

**Question:** Where did the two transactions go when the block was removed? What happened to the coinbase transaction of that block? What does this teach a merchant about 1 confirmation?

### B. Two nodes, two mempools

Start a second regtest node on different ports and connect it to the first:

```bash
mkdir -p "$HOME/regtest-node2"
bitcoind -regtest -daemon -datadir="$HOME/regtest-node2" -bind=127.0.0.1:18555 -rpcport=18554
bitcoin-cli -regtest -datadir="$HOME/regtest-node2" -rpcport=18554 addnode 127.0.0.1:18444 onetry
bitcoin-cli -regtest -datadir="$HOME/regtest-node2" -rpcport=18554 getpeerinfo | jq '.[].addr'
bitcoin-cli -regtest -datadir="$HOME/regtest-node2" -rpcport=18554 getblockcount
```

Send a new payment from Alice on node 1, then compare `getrawmempool` on both nodes after a few seconds. Then disconnect the nodes (`disconnectnode 127.0.0.1:18444` on node 2), send another payment, and compare again.

**Question:** When are the two mempools the same, and when are they different? Why can't there be one global mempool?

### C. Mempool limits

Run `bitcoin-cli -regtest help getmempoolinfo` and read about `maxmempool` and `mempoolminfee`. Read `bitcoind -help | grep -A2 maxmempool`.

**Question:** What does a node do when its mempool is full? How does that change the minimum fee it accepts?
