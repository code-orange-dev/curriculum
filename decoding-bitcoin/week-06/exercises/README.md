# Week 6 exercises

Week 6 is about Bitcoin Script and the stack: how a locking script (scriptPubKey) and an unlocking script (scriptSig) run together, using the two oldest output types, P2PK and P2PKH. Read the lessons listed in the [week README](../README.md) first. Model answers are in [`solutions/`](../solutions/README.md).

You will need pen and paper (or a text file) for the stack traces. Draw the stack as a column, with the top at the top.

## Core exercises

### 1. Decode a P2PK output from an early block

In 2009, coinbase rewards were paid straight to a public key (P2PK).

Steps:

1. Open block 9 on [mempool.space](https://mempool.space/block/9) (or search for height 9). It has one transaction, the coinbase: `0437cd7f8525ceed2324359c2d0ba26006d92d856a9c20fa0241106ee5a597c9`.
2. Expand the output and show the scriptPubKey in hex and in asm.
3. Now open block 170. Its second transaction, `f4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16`, spends that block 9 coin. It is the first known bitcoin payment from one person to another.
4. Look at that transaction's input (the scriptSig) and its two outputs.

Write down:

- The scriptPubKey of block 9's coinbase, split into bytes: the push opcode, the public key, the final opcode. How long is the whole script?
- The first byte of the public key. Is the key compressed or uncompressed?
- What is in the scriptSig of the block 170 input? Why is there no public key in it?
- What type are the two outputs of the block 170 transaction?

### 2. Trace a P2PKH spend on paper

Pick any real P2PKH spend. Any input on mempool.space whose previous output is P2PKH (address starting with `1`) works. Or use your own from the lab below (step 4).

Steps:

1. Copy the scriptSig: `<signature> <public key>`.
2. Copy the scriptPubKey of the coin being spent: `OP_DUP OP_HASH160 <20-byte hash> OP_EQUALVERIFY OP_CHECKSIG`.
3. Run them in order. After each item, draw the full stack.
4. Post a photo or a text version on [Discord](https://discord.gg/xd6dmPF9bA).

Write down:

- The stack after each of the 7 steps (2 pushes from the scriptSig, 5 items in the scriptPubKey).
- Which step would fail if someone used the wrong public key? Which step would fail if they used the right key but a bad signature?
- What is left on the stack at the end, and why does that mean "valid"?

### 3. Identify every output type in a recent transaction

Steps:

1. Open a recent block on mempool.space and pick a transaction with at least 3 outputs. Try to find one with mixed address types.
2. For each output, copy the scriptPubKey hex.
3. Match it against the patterns below.

| Pattern (hex) | Type | Address prefix (mainnet) |
|---|---|---|
| `41 <65 bytes> ac` or `21 <33 bytes> ac` | P2PK | none |
| `76 a9 14 <20 bytes> 88 ac` | P2PKH | `1` |
| `a9 14 <20 bytes> 87` | P2SH | `3` |
| `00 14 <20 bytes>` | P2WPKH | `bc1q` |
| `00 20 <32 bytes>` | P2WSH | `bc1q` (longer) |
| `51 20 <32 bytes>` | P2TR | `bc1p` |
| `6a ...` | OP_RETURN (data) | none |

Write down:

- The txid, and for each output: the type, the size of the scriptPubKey in bytes, and the asm.
- Which output type has the shortest scriptPubKey? Which is longest?

## Hands-on lab (bitcoin-cli, regtest)

Works on Bitcoin Core 28 and 29 or newer, with descriptor wallets (the default). You also need `jq`. Setup help is in the [week 1 guide](../../week-01/exercises/bitcoin_core_cli.md). Since v29, Bitcoin Core builds with CMake (`cmake -B build && cmake --build build -j$(nproc)`, binaries in `build/bin/`).

### Step 0: Start a node

```bash
bitcoind -regtest -daemon -txindex=1 -fallbackfee=0.0001
bitcoin-cli -regtest createwallet miner      # or: loadwallet miner
bitcoin-cli -regtest -rpcwallet=miner -generate 101
```

### Step 1: Decode a tiny script

The script `OP_2 OP_3 OP_ADD OP_5 OP_EQUAL` is `52 53 93 55 87` in hex.

```bash
bitcoin-cli -regtest decodescript 5253935587
```

**Question:** What does the `asm` field show? What `type` does Core give this script?

Now change the last number to 6 (`OP_6` is `0x56`):

```bash
bitcoin-cli -regtest decodescript 5253935687
```

**Question:** Does `decodescript` tell you that this script would fail? What does `decodescript` do, and what does it not do?

### Step 2: Look inside a P2PKH address

```bash
P2PKH=$(bitcoin-cli -regtest -rpcwallet=miner getnewaddress "" legacy)
bitcoin-cli -regtest -rpcwallet=miner getaddressinfo $P2PKH | jq '{address, scriptPubKey, pubkey}'
SPK=$(bitcoin-cli -regtest -rpcwallet=miner getaddressinfo $P2PKH | jq -r .scriptPubKey)
bitcoin-cli -regtest decodescript $SPK | jq '{asm, type}'
```

**Question:** Split the scriptPubKey hex into its parts and name each opcode. How many bytes is it?

### Step 3: Check the public key hash yourself

The 20 bytes in the scriptPubKey are `RIPEMD160(SHA256(pubkey))`, called HASH160.

```bash
PUB=$(bitcoin-cli -regtest -rpcwallet=miner getaddressinfo $P2PKH | jq -r .pubkey)
python3 -c "
import hashlib, sys
pub = bytes.fromhex(sys.argv[1])
sha = hashlib.sha256(pub).digest()
print(hashlib.new('ripemd160', sha).hexdigest())
" $PUB
```

If Python says `unsupported hash type ripemd160` (some OpenSSL 3 systems), use `openssl` with the legacy provider instead:

```bash
echo -n $PUB | xxd -r -p | openssl dgst -sha256 -binary \
  | openssl dgst -provider legacy -provider default -ripemd160
```

**Question:** Does your hash match the 20 bytes in the scriptPubKey? Why does a P2PKH output store a hash and not the public key?

### Step 4: Spend from P2PKH and read the scriptSig

```bash
bitcoin-cli -regtest -rpcwallet=miner -named sendtoaddress address=$P2PKH amount=1 fee_rate=2
bitcoin-cli -regtest -rpcwallet=miner -generate 1

UTXO=$(bitcoin-cli -regtest -rpcwallet=miner listunspent | jq -c --arg a $P2PKH '[.[] | select(.address==$a)][0] | {txid, vout}')
DEST=$(bitcoin-cli -regtest -rpcwallet=miner getnewaddress)
RAW=$(bitcoin-cli -regtest createrawtransaction "[$UTXO]" "[{\"$DEST\":0.9999}]")
SIGNED=$(bitcoin-cli -regtest -rpcwallet=miner signrawtransactionwithwallet $RAW | jq -r .hex)
bitcoin-cli -regtest decoderawtransaction $SIGNED | jq '.vin[0].scriptSig'
SPEND=$(bitcoin-cli -regtest sendrawtransaction $SIGNED)
bitcoin-cli -regtest -rpcwallet=miner -generate 1
```

**Question:** The scriptSig `asm` has two items. What are they? Is the second one the same as `$PUB`? What does `[ALL]` at the end of the first item mean?

Now use this scriptSig and the scriptPubKey from step 2 for core exercise 2.

### Step 5: Make a P2PK output by mining to it

`generatetodescriptor` mines a block whose coinbase pays to any descriptor. `pk(KEY)` is the descriptor for P2PK.

```bash
DESC=$(bitcoin-cli -regtest getdescriptorinfo "pk($PUB)" | jq -r .descriptor)
bitcoin-cli -regtest generatetodescriptor 1 "$DESC"
bitcoin-cli -regtest getblock $(bitcoin-cli -regtest getbestblockhash) 2 | jq '.tx[0].vout[0].scriptPubKey'
```

**Question:** What `type` does Core show? Is there an `address` field? How many bytes is this scriptPubKey, and how does that compare with the 67-byte P2PK scripts in block 9?

**Question:** To spend this output, what would the scriptSig contain? Why is it shorter than a P2PKH scriptSig?

### Step 6: One transaction, many output types

```bash
A_LEG=$(bitcoin-cli -regtest -rpcwallet=miner getnewaddress "" legacy)
A_NEST=$(bitcoin-cli -regtest -rpcwallet=miner getnewaddress "" p2sh-segwit)
A_WPKH=$(bitcoin-cli -regtest -rpcwallet=miner getnewaddress "" bech32)
A_TR=$(bitcoin-cli -regtest -rpcwallet=miner getnewaddress "" bech32m)

MIX=$(bitcoin-cli -regtest -rpcwallet=miner -named sendmany \
  amounts="{\"$A_LEG\":0.1,\"$A_NEST\":0.1,\"$A_WPKH\":0.1,\"$A_TR\":0.1}" fee_rate=2)
bitcoin-cli -regtest getrawtransaction $MIX true \
  | jq '.vout[] | {n, value, type: .scriptPubKey.type, hex: .scriptPubKey.hex, address: .scriptPubKey.address}'
```

**Question:** Match each output to a row in the table in core exercise 3. What are the regtest address prefixes for each type? Which output is the change?

## Stretch tasks

1. **Analyse an unusual mainnet script.** Find a mainnet transaction with an output that is not one of the standard types in the table: for example an `OP_RETURN` output with a text message, or a bare multisig output (`51 ... 53 ae`). Decode the script with `decodescript` and explain what it does and who could spend it.
2. **Run a script by hand that fails.** Write the stack trace for `OP_1 OP_2 OP_ADD OP_4 OP_EQUAL` and for `OP_1 OP_DUP OP_ADD OP_2 OP_EQUALVERIFY`. Which one fails, and at which step? What is left on the stack in each case?
3. **Read the interpreter.** In the Bitcoin Core source, open `src/script/interpreter.cpp` and find `EvalScript`. Find the case for `OP_EQUALVERIFY`. How is it built from `OP_EQUAL`? Find where disabled opcodes like `OP_CAT` are rejected.
4. **Uncompressed vs compressed.** The block 9 key starts with `04`. Your regtest key starts with `02` or `03`. How many bytes does each take, and what extra information does the `02`/`03` byte carry?

When you are done: `bitcoin-cli -regtest stop`.
