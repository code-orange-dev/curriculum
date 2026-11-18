# Week 5 exercises

Week 5 is about signing: what a signature commits to, where it is stored, and how wallets pass unsigned transactions around (PSBTs). Read the lessons listed in the [week README](../README.md) first. Model answers are in [`solutions/`](../solutions/README.md), so try everything before you look.

## Core exercises

### 1. Decoding Bitcoin transaction exercises

Open the [transaction exercises](https://bitcoindevs.xyz/decoding/transaction_exercises) and accept the GitHub Classroom assignment.

Steps:

1. Clone your assignment repository and read its README before you write any code.
2. Run the tests once before you change anything, so you know what "failing" looks like.
3. Solve one exercise at a time. Commit after each passing test.
4. Push to GitHub so the automatic checks run.

Write down:

- Which exercise took you longest, and why.
- One thing about the transaction format you only understood after the code worked.
- Any test you could not make pass. Bring it to Monday's session.

### 2. Pair review on Discord

Find a partner on [Discord](https://discord.gg/xd6dmPF9bA) and swap links to your exercise repositories.

Steps:

1. Read your partner's code for one exercise you both solved.
2. Check: Is little-endian vs big-endian handled correctly? Are variable-length integers (CompactSize) parsed for all sizes, not only the 1-byte case? Are magic numbers named?
3. Leave at least one comment (a GitHub comment or a Discord message).

Write down:

- One thing your partner did better than you.
- One thing you would do differently in their code, and why.

### 3. Find a non-ALL sighash in the wild

Most signatures use SIGHASH_ALL. Find one that does not.

Steps:

1. Search online for examples of `SIGHASH_SINGLE|ANYONECANPAY`, `SIGHASH_NONE` or `SIGHASH_ALL|ANYONECANPAY` transactions. Ordinals marketplace listings and old crowdfunding experiments are good places to start.
2. Open the transaction on [mempool.space](https://mempool.space) and expand the input details.
3. Look at the **last byte** of the signature (in the witness for segwit inputs, in the scriptSig for legacy inputs). For a taproot input, a 64-byte signature means SIGHASH_DEFAULT and a 65-byte signature carries an explicit sighash byte.

| Last byte | Flag |
|---|---|
| `01` | ALL |
| `02` | NONE |
| `03` | SINGLE |
| `81` | ALL\|ANYONECANPAY |
| `82` | NONE\|ANYONECANPAY |
| `83` | SINGLE\|ANYONECANPAY |

Write down:

- The txid and the input index.
- The flag you found.
- What that flag allowed other people to do with the transaction after it was signed.

## Hands-on lab (bitcoin-cli, regtest)

> Tested on Bitcoin Core 29.0 (regtest), November 2026.

This lab works on Bitcoin Core 28 and 29 or newer. Wallets are descriptor wallets by default. You also need `jq` (`sudo apt install jq` or `brew install jq`).

If you do not have a node yet, follow the [week 1 setup guide](../../week-01/exercises/bitcoin_core_cli.md). Since v29, Bitcoin Core builds with CMake: `cmake -B build && cmake --build build -j$(nproc)`, and the binaries end up in `build/bin/`.

### Step 0: Start a node and fund a miner wallet

Regtest has no fee estimates, so we give the node a fallback fee rate and also pass `fee_rate` (sat/vB) where we can.

```bash
bitcoind -regtest -daemon -txindex=1 -fallbackfee=0.0001
bitcoin-cli -regtest createwallet miner
bitcoin-cli -regtest createwallet alice
bitcoin-cli -regtest createwallet bob
bitcoin-cli -regtest -rpcwallet=miner -generate 101
bitcoin-cli -regtest -rpcwallet=miner getbalance
```

If `createwallet` says the wallet already exists (from an earlier week), use `bitcoin-cli -regtest loadwallet <name>` instead.

**Question:** Why do you need 101 blocks before the miner has a spendable balance?

### Step 1: Sign a raw transaction with `signrawtransactionwithwallet`

Give Alice a coin, then build a transaction that spends it.

```bash
ALICE=$(bitcoin-cli -regtest -rpcwallet=alice getnewaddress)
bitcoin-cli -regtest -rpcwallet=miner -named sendtoaddress address=$ALICE amount=1 fee_rate=2
bitcoin-cli -regtest -rpcwallet=miner -generate 1

UTXO=$(bitcoin-cli -regtest -rpcwallet=alice listunspent | jq '.[0]')
TXID=$(echo "$UTXO" | jq -r .txid)
VOUT=$(echo "$UTXO" | jq -r .vout)
DEST=$(bitcoin-cli -regtest -rpcwallet=miner getnewaddress)

RAW=$(bitcoin-cli -regtest createrawtransaction \
  "[{\"txid\":\"$TXID\",\"vout\":$VOUT}]" "[{\"$DEST\":0.9999}]")
bitcoin-cli -regtest decoderawtransaction $RAW | jq '.vin[0]'
```

**Question:** What is in `scriptSig` and is there a `txinwitness` field before signing?

Now sign it:

```bash
SIGNED=$(bitcoin-cli -regtest -rpcwallet=alice signrawtransactionwithwallet $RAW | jq -r .hex)
bitcoin-cli -regtest decoderawtransaction $SIGNED | jq '.vin[0]'
```

**Question:** How many items are in `txinwitness`? What is each one? What is the last byte of the first item, and what does it mean?

Compare the txid before and after signing:

```bash
bitcoin-cli -regtest decoderawtransaction $RAW    | jq -r '.txid, .hash'
bitcoin-cli -regtest decoderawtransaction $SIGNED | jq -r '.txid, .hash'
```

**Question:** Did the `txid` change when you signed? Did the `hash` (wtxid) change? Why?

Do not broadcast yet. We will reuse `$RAW` in the next steps.

### Step 2: Sign the same transaction twice

```bash
SIGNED2=$(bitcoin-cli -regtest -rpcwallet=alice signrawtransactionwithwallet $RAW | jq -r .hex)
[ "$SIGNED" = "$SIGNED2" ] && echo "identical" || echo "different"
```

**Question:** Are the two signatures identical? An ECDSA signature needs a secret nonce. How can it be the same twice, and why is that safe?

### Step 3: Try other sighash flags

```bash
S_NONE=$(bitcoin-cli -regtest -rpcwallet=alice -named signrawtransactionwithwallet \
  hexstring=$RAW sighashtype=NONE | jq -r .hex)
S_SACP=$(bitcoin-cli -regtest -rpcwallet=alice -named signrawtransactionwithwallet \
  hexstring=$RAW sighashtype="SINGLE|ANYONECANPAY" | jq -r .hex)

for TX in $SIGNED $S_NONE $S_SACP; do
  bitcoin-cli -regtest decoderawtransaction $TX | jq -r '.vin[0].txinwitness[0]' | tail -c 3
done
```

**Question:** What are the last bytes of the three signatures? Why are the signatures themselves completely different, even though the key and the transaction are the same?

**Question:** With the `NONE` signature, what could anyone who sees this transaction change before broadcasting it?

### Step 4: A legacy input for comparison

```bash
LEGACY=$(bitcoin-cli -regtest -rpcwallet=alice getnewaddress "" legacy)
bitcoin-cli -regtest -rpcwallet=miner -named sendtoaddress address=$LEGACY amount=0.5 fee_rate=2
bitcoin-cli -regtest -rpcwallet=miner -generate 1

LUTXO=$(bitcoin-cli -regtest -rpcwallet=alice listunspent | jq --arg a $LEGACY '[.[] | select(.address==$a)][0]')
LTXID=$(echo "$LUTXO" | jq -r .txid)
LVOUT=$(echo "$LUTXO" | jq -r .vout)
LRAW=$(bitcoin-cli -regtest createrawtransaction \
  "[{\"txid\":\"$LTXID\",\"vout\":$LVOUT}]" "[{\"$DEST\":0.4999}]")
LSIGNED=$(bitcoin-cli -regtest -rpcwallet=alice signrawtransactionwithwallet $LRAW | jq -r .hex)

bitcoin-cli -regtest decoderawtransaction $LSIGNED | jq '.vin[0]'
bitcoin-cli -regtest decoderawtransaction $LRAW    | jq -r .txid
bitcoin-cli -regtest decoderawtransaction $LSIGNED | jq -r .txid
```

**Question:** What prefix does a regtest legacy address have? Where is the signature now? Did the txid change after signing this time?

Broadcast both signed transactions (the `ALL` one from step 1 and the legacy one) and mine a block:

```bash
bitcoin-cli -regtest sendrawtransaction $SIGNED
bitcoin-cli -regtest sendrawtransaction $LSIGNED
bitcoin-cli -regtest -rpcwallet=miner -generate 1
```

**Question:** Look up both with `getrawtransaction <txid> true`. Compare `size`, `vsize` and `weight`. Which input is cheaper, and why?

### Step 5: The PSBT workflow in one wallet

A PSBT (BIP174) carries an unsigned transaction plus the data a signer needs.

```bash
bitcoin-cli -regtest -rpcwallet=miner -named sendtoaddress address=$(bitcoin-cli -regtest -rpcwallet=alice getnewaddress) amount=2 fee_rate=2
bitcoin-cli -regtest -rpcwallet=miner -generate 1

PSBT=$(bitcoin-cli -regtest -rpcwallet=alice -named walletcreatefundedpsbt \
  outputs="[{\"$DEST\":0.3}]" options='{"fee_rate":2}' | jq -r .psbt)
bitcoin-cli -regtest decodepsbt $PSBT | jq '{tx: .tx.vin, inputs: .inputs, fee: .fee}'
bitcoin-cli -regtest analyzepsbt $PSBT
```

**Question:** Which fields does the PSBT input carry (look for `witness_utxo` and `bip32_derivs`)? Why does a signer need the UTXO amount? What does `analyzepsbt` say the next role is?

```bash
SIGNED_PSBT=$(bitcoin-cli -regtest -rpcwallet=alice -named walletprocesspsbt psbt=$PSBT finalize=false | jq -r .psbt)
bitcoin-cli -regtest decodepsbt $SIGNED_PSBT | jq '.inputs[0].partial_signatures'
bitcoin-cli -regtest analyzepsbt $SIGNED_PSBT | jq -r .next

HEX=$(bitcoin-cli -regtest finalizepsbt $SIGNED_PSBT | jq -r .hex)
bitcoin-cli -regtest sendrawtransaction $HEX
bitcoin-cli -regtest -rpcwallet=miner -generate 1
```

**Question:** What changed between `partial_signatures` and the final transaction? Which BIP174 roles did `walletprocesspsbt` and `finalizepsbt` play?

### Step 6: Two signers, one transaction (`combinepsbt`)

Alice and Bob each own one input. Neither can sign the other's input, so they sign separately and combine.

```bash
bitcoin-cli -regtest -rpcwallet=miner -named sendtoaddress address=$(bitcoin-cli -regtest -rpcwallet=alice getnewaddress) amount=1 fee_rate=2
bitcoin-cli -regtest -rpcwallet=miner -named sendtoaddress address=$(bitcoin-cli -regtest -rpcwallet=bob getnewaddress) amount=1 fee_rate=2
bitcoin-cli -regtest -rpcwallet=miner -generate 1

A=$(bitcoin-cli -regtest -rpcwallet=alice listunspent | jq -c '[.[] | select(.amount==1)][0] | {txid, vout}')
B=$(bitcoin-cli -regtest -rpcwallet=bob   listunspent | jq -c '[.[] | select(.amount==1)][0] | {txid, vout}')

JOINT=$(bitcoin-cli -regtest createpsbt "[$A,$B]" "[{\"$DEST\":1.9999}]")
PA=$(bitcoin-cli -regtest -rpcwallet=alice walletprocesspsbt $JOINT | jq -r .psbt)
PB=$(bitcoin-cli -regtest -rpcwallet=bob   walletprocesspsbt $JOINT | jq -r .psbt)
bitcoin-cli -regtest analyzepsbt $PA | jq '.inputs[] | {is_final, next}'

COMBINED=$(bitcoin-cli -regtest combinepsbt "[\"$PA\",\"$PB\"]")
bitcoin-cli -regtest analyzepsbt $COMBINED | jq '.inputs[] | {is_final, next}'
HEX=$(bitcoin-cli -regtest finalizepsbt $COMBINED | jq -r .hex)
bitcoin-cli -regtest sendrawtransaction $HEX
```

**Question:** After Alice processes the PSBT, which input is final and which is not? What fee does this transaction pay, in sats? (Hint: inputs minus outputs.)

**Question:** Alice signed with SIGHASH_ALL. Could Bob change the output after Alice signed? Why not?

## Stretch tasks

1. **Prove why NONE is dangerous.** Take `$S_NONE` from step 3 (it spends the same coin as `$SIGNED`, so create a fresh coin and a fresh `RAW` first). Find the destination scriptPubKey with `OLD_SPK=$(bitcoin-cli -regtest -rpcwallet=miner getaddressinfo $DEST | jq -r .scriptPubKey)` (`getaddressinfo` is a wallet command, so it needs `-rpcwallet` when several wallets are loaded). Make a new address in Bob's wallet (the "thief") and get its scriptPubKey `NEW_SPK` the same way. Replace the old scriptPubKey hex with the new one inside the signed hex (both are 22 bytes for P2WPKH). Try the `ALL`-signed transaction first: `NEW=${SIGNED/$OLD_SPK/$NEW_SPK}` and broadcast `$NEW`. Then do the same with `NEW=${S_NONE/$OLD_SPK/$NEW_SPK}`. (Do `ALL` first: once the `NONE` version is in the mempool the coin is spent, and the `ALL` attempt fails for that reason instead.) What happens in each case?
2. **Hardware wallet simulator.** Install [HWI](https://github.com/bitcoin-core/HWI) and a device emulator (the Trezor emulator works well). Run `hwi enumerate`, get an xpub with `hwi -t trezor -d <path> --chain regtest getxpub m/84h/1h/0h`, import it into a watch-only wallet as a `wpkh(...)` descriptor, build a PSBT there, and sign it with `hwi ... signtx <psbt>`. Check flags with `hwi --help`, as they change between versions. What did the emulator show on its screen before signing?
3. **Read the sighash code.** In the Bitcoin Core source, open `src/script/interpreter.cpp` and find `SignatureHash`. Which branch handles segwit v0 (BIP143)? Which values are cached between inputs, and why does that matter for large transactions?

When you are done: `bitcoin-cli -regtest stop`.
