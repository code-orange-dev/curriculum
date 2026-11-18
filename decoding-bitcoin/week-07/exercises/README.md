# Week 7 exercises

Week 7 is about multisig: bare multisig (P2MS), and how P2SH hides any script, including multisig, behind a 20-byte hash. The lab builds a real 2-of-3 wallet on regtest and spends from it with PSBTs. Read the lessons listed in the [week README](../README.md) first. Model answers are in [`solutions/`](../solutions/README.md).

## Core exercises

### 1. P2MS exercises on Decoding Bitcoin

Do the exercises at the end of the [P2MS lesson](https://bitcoindevs.xyz/decoding/p2ms), including the hard one.

Steps:

1. Before you start, write down the general shape of an M-of-N multisig scriptPubKey and its scriptSig from memory.
2. Work through the exercises. For each one, write the script in asm first, then in hex.
3. For the hard one, write the full stack trace.

Write down:

- The size in bytes of a 2-of-3 bare multisig scriptPubKey with compressed keys.
- Why the scriptSig starts with `OP_0`.
- Anything in the exercises that surprised you.

### 2. Pull the redeem script out of a real P2SH multisig spend

Steps:

1. Find a mainnet transaction that spends a P2SH output (an input whose previous address starts with `3`). Many older exchange and custody wallets used P2SH multisig, so look at transactions from around 2014 to 2018. Search online for "P2SH multisig transaction example" if you need a starting point.
2. On mempool.space, open the input and look at the scriptSig asm.
3. The **last** push is the redeem script. Copy it and decode it, either by hand or with `bitcoin-cli decodescript <hex>` (decoding works on any network, even regtest).

Write down:

- The txid and input index.
- The redeem script in asm.
- M (the first opcode: `OP_2` is `52`, so M = 0x52 − 0x50 = 2) and N (the opcode before `OP_CHECKMULTISIG`, `ae`).
- How many signatures are in the scriptSig, and what is the first item of the scriptSig.
- Check: does HASH160 of the redeem script equal the 20 bytes in the P2SH scriptPubKey?

### 3. Design a 2-of-3 for a small business

A small coffee roastery with two owners wants to hold its savings in bitcoin.

Steps:

1. Decide who holds each of the three keys and what kind of device each one is.
2. Decide where each key and each seed backup is stored.
3. Write the recovery plan for: one owner loses their device, one owner leaves the company, the office burns down, one owner dies.

Write down:

- A small diagram or table: key, holder, device, location, backup location.
- What is needed to spend (which two keys) in normal use.
- What else besides the seeds must be backed up so that the wallet can be recovered. (Hint: what does a signer need to know about the other two keys?)

## Hands-on lab (bitcoin-cli, regtest)

> Tested on Bitcoin Core 29.0 (regtest), November 2026.

Works on Bitcoin Core 28 and 29 or newer. Wallets are descriptor wallets by default. Older guides use `addmultisigaddress` and `dumpprivkey`, which only work with legacy wallets and are gone in new versions. We use descriptors and PSBTs instead, the same way the official [Bitcoin Core multisig tutorial](https://github.com/bitcoin/bitcoin/blob/master/doc/multisig-tutorial.md) does.

You need `jq`. Setup help is in the [week 1 guide](../../week-01/exercises/bitcoin_core_cli.md). Since v29, Bitcoin Core builds with CMake (`cmake -B build && cmake --build build -j$(nproc)`, binaries in `build/bin/`).

Run all commands in **one terminal**, because later steps use shell variables from earlier steps.

### Step 0: One miner and three signers

```bash
bitcoind -regtest -daemon -txindex=1 -fallbackfee=0.0001
for W in miner signer1 signer2 signer3; do
  bitcoin-cli -regtest createwallet $W     # or: loadwallet $W
done
bitcoin-cli -regtest -rpcwallet=miner -generate 101
```

### Step 1: Collect one public key from each signer

Each signer shares a public key **with its key origin** (master key fingerprint and derivation path). The origin lets the signer's wallet recognise its own key later in a PSBT.

```bash
for i in 1 2 3; do
  ADDR=$(bitcoin-cli -regtest -rpcwallet=signer$i getnewaddress "" bech32)
  bitcoin-cli -regtest -rpcwallet=signer$i getaddressinfo $ADDR | jq -r .desc
done
```

Each line looks like `wpkh([d34db33f/84h/1h/0h/0/0]03abc...)#checksum`. Save the part inside `wpkh(...)`:

```bash
key() {
  ADDR=$(bitcoin-cli -regtest -rpcwallet=signer$1 getnewaddress "" bech32)
  bitcoin-cli -regtest -rpcwallet=signer$1 getaddressinfo $ADDR \
    | jq -r .desc | sed -E 's/^wpkh\((.*)\)#.*$/\1/'
}
K1=$(key 1); K2=$(key 2); K3=$(key 3)
echo $K1; echo $K2; echo $K3
```

**Question:** What do the fingerprint and the path in square brackets tell another wallet? Is it safe to share this string?

### Step 2: Look at the scripts with `createmultisig`

`createmultisig` takes plain public keys, so strip the origins first.

```bash
P1=${K1##*]}; P2=${K2##*]}; P3=${K3##*]}
bitcoin-cli -regtest createmultisig 2 "[\"$P1\",\"$P2\",\"$P3\"]" legacy
bitcoin-cli -regtest createmultisig 2 "[\"$P1\",\"$P2\",\"$P3\"]" bech32
REDEEM=$(bitcoin-cli -regtest createmultisig 2 "[\"$P1\",\"$P2\",\"$P3\"]" legacy | jq -r .redeemScript)
bitcoin-cli -regtest decodescript $REDEEM | jq '{asm, type}'
echo -n $REDEEM | wc -c
```

**Question:** What do the address prefixes look like for the legacy (P2SH) and bech32 (P2WSH) versions? The redeem script is the same for both. How many bytes is it? (`wc -c` counts hex characters.) What `type` does Core call it?

**Question:** If this exact script were used as a bare multisig scriptPubKey, how many bytes would the sender's output be? How big is the P2SH scriptPubKey instead?

### Step 3: A watch-only wallet for the P2SH 2-of-3

The coordinator wallet knows all three public keys and no private keys.

```bash
DESC_SH=$(bitcoin-cli -regtest getdescriptorinfo "sh(multi(2,$K1,$K2,$K3))" | jq -r .descriptor)
bitcoin-cli -regtest -named createwallet wallet_name=ms_sh disable_private_keys=true blank=true
bitcoin-cli -regtest -rpcwallet=ms_sh importdescriptors "[{\"desc\":\"$DESC_SH\",\"timestamp\":\"now\"}]"
MS_SH=$(bitcoin-cli -regtest deriveaddresses "$DESC_SH" | jq -r '.[0]')
echo $MS_SH
```

**Question:** Is `$MS_SH` the same as the legacy address from step 2? Why?

Fund it:

```bash
bitcoin-cli -regtest -rpcwallet=miner -named sendtoaddress address=$MS_SH amount=1 fee_rate=2
bitcoin-cli -regtest -rpcwallet=miner -generate 1
bitcoin-cli -regtest -rpcwallet=ms_sh getbalances
```

**Question:** Look at the funding transaction's output with `getrawtransaction <txid> true`. Does the output show any public keys? What does a blockchain observer learn about this coin at this point?

### Step 4: Spend it with PSBT roles

```bash
DEST=$(bitcoin-cli -regtest -rpcwallet=miner getnewaddress)

# Creator + Updater: the watch-only coordinator
PSBT=$(bitcoin-cli -regtest -rpcwallet=ms_sh -named walletcreatefundedpsbt \
  outputs="[{\"$DEST\":1}]" \
  options="{\"subtractFeeFromOutputs\":[0],\"fee_rate\":2,\"changeAddress\":\"$MS_SH\"}" | jq -r .psbt)
bitcoin-cli -regtest decodepsbt $PSBT | jq '.inputs[0] | {redeem_script, bip32_derivs}'
bitcoin-cli -regtest analyzepsbt $PSBT
```

We spend the whole coin and subtract the fee from the output, so there is no change. The watch-only wallet cannot make change addresses of its own, so we also name the multisig address as `changeAddress`, just in case.

**Question:** What does the coordinator put into the PSBT input so that signers can sign? What does `analyzepsbt` say is missing?

```bash
# Signers: each signs the same PSBT on their own machine
S1=$(bitcoin-cli -regtest -rpcwallet=signer1 walletprocesspsbt $PSBT | jq -r .psbt)
S3=$(bitcoin-cli -regtest -rpcwallet=signer3 walletprocesspsbt $PSBT | jq -r .psbt)
bitcoin-cli -regtest analyzepsbt $S1 | jq '.inputs[0]'

# Combiner
COMBINED=$(bitcoin-cli -regtest combinepsbt "[\"$S1\",\"$S3\"]")
bitcoin-cli -regtest analyzepsbt $COMBINED | jq '.inputs[0]'

# Finalizer + Extractor
HEX=$(bitcoin-cli -regtest finalizepsbt $COMBINED | jq -r .hex)
SH_SPEND=$(bitcoin-cli -regtest sendrawtransaction $HEX)
bitcoin-cli -regtest -rpcwallet=miner -generate 1
```

**Question:** After only signer 1 has signed, what does `analyzepsbt` say? Why could signer 1 not finalize alone? Why did we not need signer 2 at all?

### Step 5: Read the P2SH spend

```bash
bitcoin-cli -regtest getrawtransaction $SH_SPEND true | jq '{size, vsize, weight, scriptSig: .vin[0].scriptSig.asm}'
```

**Question:** List the items in the scriptSig in order. What is the first item, and why is it there? Which item is the redeem script? Is this the first time the three public keys appear on the blockchain?

### Step 6: The same 2-of-3 as P2WSH

```bash
DESC_WSH=$(bitcoin-cli -regtest getdescriptorinfo "wsh(multi(2,$K1,$K2,$K3))" | jq -r .descriptor)
bitcoin-cli -regtest -named createwallet wallet_name=ms_wsh disable_private_keys=true blank=true
bitcoin-cli -regtest -rpcwallet=ms_wsh importdescriptors "[{\"desc\":\"$DESC_WSH\",\"timestamp\":\"now\"}]"
MS_WSH=$(bitcoin-cli -regtest deriveaddresses "$DESC_WSH" | jq -r '.[0]')
bitcoin-cli -regtest -rpcwallet=miner -named sendtoaddress address=$MS_WSH amount=1 fee_rate=2
bitcoin-cli -regtest -rpcwallet=miner -generate 1

PSBT=$(bitcoin-cli -regtest -rpcwallet=ms_wsh -named walletcreatefundedpsbt \
  outputs="[{\"$DEST\":1}]" \
  options="{\"subtractFeeFromOutputs\":[0],\"fee_rate\":2,\"changeAddress\":\"$MS_WSH\"}" | jq -r .psbt)
S1=$(bitcoin-cli -regtest -rpcwallet=signer1 walletprocesspsbt $PSBT | jq -r .psbt)
S2=$(bitcoin-cli -regtest -rpcwallet=signer2 walletprocesspsbt $PSBT | jq -r .psbt)
HEX=$(bitcoin-cli -regtest finalizepsbt $(bitcoin-cli -regtest combinepsbt "[\"$S1\",\"$S2\"]") | jq -r .hex)
WSH_SPEND=$(bitcoin-cli -regtest sendrawtransaction $HEX)
bitcoin-cli -regtest -rpcwallet=miner -generate 1

bitcoin-cli -regtest getrawtransaction $WSH_SPEND true \
  | jq '{size, vsize, weight, scriptSig: .vin[0].scriptSig.hex, witness: .vin[0].txinwitness}'
```

**Question:** Where are the signatures and the script now? What is the first witness item? Compare `vsize` with the P2SH spend from step 5. Roughly what percentage of the fee does P2WSH save?

## Stretch tasks

1. **The P2SH size limit.** Make 16 public keys (call `key` in a loop, or reuse keys) and try `createmultisig 2 [16 keys] legacy`. What happens, and why? How many compressed keys fit in a P2SH redeem script?
2. **Bare multisig on regtest.** Mine a block to a bare multisig with `generatetodescriptor 1 "$(bitcoin-cli -regtest getdescriptorinfo "multi(1,$P1,$P2)" | jq -r .descriptor)"` and look at the coinbase output's `scriptPubKey`. What `type` does Core give it? Is there an address?
3. **Sorted keys.** Replace `multi` with `sortedmulti` in the descriptor. Does the address change? Why do many multisig wallets use sorted keys (BIP67)?
4. **Recovery drill.** Unload `ms_sh` (`unloadwallet ms_sh`) and pretend it is lost. Using only `$K1`, `$K2`, `$K3` (or the descriptor string), rebuild the watch-only wallet under a new name (the old wallet folder still exists, so `createwallet ms_sh` fails) and find the coin's history again with `listtransactions "*" 10 0 true`. What would you have needed if you had only the three seeds and not the descriptor?

When you are done: `bitcoin-cli -regtest stop`.
