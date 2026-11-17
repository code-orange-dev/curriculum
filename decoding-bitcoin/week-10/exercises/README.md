# Week 10 exercises

[Week 10 overview](../README.md) · [Solutions](../solutions/README.md) · [Syllabus](../../README.md) · [After the cohort](../../after-the-cohort.md)

The final week. You will finish the capstone, spend a Taproot output through a script path, compare on-chain sizes, and present what you built. Read the three lessons in the [week overview](../README.md) first.

---

## Exercise 1: Complete the capstone

Do the [Capstone: Build & Spend a P2TR](https://bitcoindevs.xyz/decoding/build-spend-p2tr) on Decoding Bitcoin. Run it on regtest or signet. If you get stuck, the regtest lab below walks through the same ideas with Bitcoin Core doing the signing.

**Write down** (in your repository README or a Discord post):

1. Your internal key and how you chose it.
2. Your script tree (if any): each leaf script in `asm`, and the Merkle root.
3. The output key and the `bc1p`/`tb1p`/`bcrt1p` address.
4. The txid that funded the output and the txid that spent it.
5. Which path you used to spend (key path or script path) and what was in the witness.
6. One thing that went wrong and how you fixed it.

---

## Exercise 2: Present in 3 minutes

At the final session everyone presents for 3 minutes: the capstone, or any exercise from the cohort you are proud of (your week 8 stack machine counts).

A simple structure that fits in 3 minutes:

1. **What** you built (30 seconds).
2. **Show** it: one screen, one command, or one transaction (90 seconds).
3. **One thing you learned** that surprised you (30 seconds).
4. **What's next** for you (30 seconds).

Practise once with a timer. Have your screen ready before your turn.

---

## Exercise 3: Share your feedback

Fill in the cohort feedback form the Facilitator posts on Discord. Be specific: which week helped most, which week was confusing, and one thing you would change. Your answers shape the next cohort.

---

## Hands-on lab (bitcoin-cli, regtest)

You need Bitcoin Core 28 or newer and `jq`. Earlier labs explain the setup: see [Week 1: Bitcoin Core CLI](../../week-01/exercises/bitcoin_core_cli.md) for regtest basics and [week 9's lab](../../week-09/exercises/README.md#hands-on-lab-bitcoin-cli-regtest) for key-path spends.

### Setup

```bash
bitcoind -regtest -daemon -txindex=1
bitcoin-cli -regtest -named createwallet wallet_name=lab || bitcoin-cli -regtest loadwallet lab
bitcoin-cli -regtest -rpcwallet=lab -generate 101

# The lab wallet's master private key (regtest only, never do this with real funds)
XPRV=$(bitcoin-cli -regtest -rpcwallet=lab listdescriptors true | jq -r '.descriptors[].desc' | grep -o 'tprv[[:alnum:]]*' | head -1)

# BIP341's "nothing up my sleeve" point: an x-only key with no known private key
H=50929b74c1a04954b78b4b6035e97a5e078a5a0f28ec96d547bfee9ace803ac0
```

### Lab 1: An inheritance output with a script-path spend (old Week 5, exercise 3)

You will build a Taproot output with **no usable key path** and two leaves:

- Leaf A: the owner can spend at any time with their key.
- Leaf B: the heir can spend with their key, but only 5 blocks after the coin confirmed.

Then you will spend it as the heir, through leaf B.

**1.1** Get the owner's key (public only, as an x-only key) and build the descriptor. The heir's key comes from `XPRV`.

```bash
OWNER=$(bitcoin-cli -regtest -rpcwallet=lab getaddressinfo "$(bitcoin-cli -regtest -rpcwallet=lab getnewaddress)" | jq -r .pubkey | cut -c3-)
DESC="tr($H,{pk($OWNER),and_v(v:pk($XPRV/1003/0),older(5))})"
DESC="$DESC#$(bitcoin-cli -regtest getdescriptorinfo "$DESC" | jq -r .checksum)"
ADDR=$(bitcoin-cli -regtest deriveaddresses "$DESC" | jq -r '.[0]')
echo "$ADDR"
```

**Question:** Why does `cut -c3-` turn the owner's public key into an x-only key? Why use `H` as the internal key?

**1.2** Create a blank `heir` wallet that only knows this descriptor, and fund the address:

```bash
bitcoin-cli -regtest -named createwallet wallet_name=heir blank=true
bitcoin-cli -regtest -rpcwallet=heir importdescriptors "[{\"desc\":\"$DESC\",\"timestamp\":\"now\"}]"

TXID=$(bitcoin-cli -regtest -rpcwallet=lab sendtoaddress "$ADDR" 1)
bitcoin-cli -regtest -rpcwallet=lab -generate 1
VOUT=$(bitcoin-cli -regtest getrawtransaction "$TXID" true | jq ".vout[] | select(.scriptPubKey.address==\"$ADDR\") | .n")
bitcoin-cli -regtest -rpcwallet=heir listunspent
```

**1.3** Build the heir's spend with `sequence` 5, sign it, and try to broadcast at once:

```bash
DEST=$(bitcoin-cli -regtest -rpcwallet=lab getnewaddress "" bech32m)
PSBT=$(bitcoin-cli -regtest -named createpsbt \
  inputs="[{\"txid\":\"$TXID\",\"vout\":$VOUT,\"sequence\":5}]" \
  outputs="[{\"$DEST\":0.9999}]")
SIGNED=$(bitcoin-cli -regtest -rpcwallet=heir walletprocesspsbt "$PSBT" | jq -r .psbt)
HEX=$(bitcoin-cli -regtest finalizepsbt "$SIGNED" | jq -r .hex)
bitcoin-cli -regtest sendrawtransaction "$HEX"
```

**Question:** Why is it rejected? What would the owner need to do to stop the heir from ever being able to spend?

**1.4** Mine 5 blocks and broadcast again:

```bash
bitcoin-cli -regtest -rpcwallet=lab -generate 5
SPEND=$(bitcoin-cli -regtest sendrawtransaction "$HEX")
bitcoin-cli -regtest -rpcwallet=lab -generate 1
bitcoin-cli -regtest getrawtransaction "$SPEND" true | jq '{vsize, weight, witness: .vin[0].txinwitness}'
```

**Question:** How many witness items are there? For each one, give its size in bytes and say what it is.

**1.5** Look at the leaf script and the control block:

```bash
LEAF=$(bitcoin-cli -regtest getrawtransaction "$SPEND" true | jq -r '.vin[0].txinwitness[1]')
CB=$(bitcoin-cli -regtest getrawtransaction "$SPEND" true | jq -r '.vin[0].txinwitness[2]')
bitcoin-cli -regtest decodescript "$LEAF" | jq -r .asm
echo "first byte: ${CB:0:2}"
echo "bytes 2-33: ${CB:2:64}"
echo "bytes 34-65: ${CB:66:64}"
```

**Question:** Write the leaf script `asm`. What is the first byte of the control block, and what two things does it encode? What are bytes 2 to 33? What are bytes 34 to 65? Does the owner's key appear anywhere in this transaction?

**1.6** Verify the commitment yourself. This script recomputes the output key from the leaf script and the control block, using only the Python standard library:

```python
# check_control_block.py: verify a Taproot script-path commitment.
# Usage: python3 check_control_block.py <leaf script hex> <control block hex> <witness program hex>
# Learning code only: slow and not safe for real keys.
import hashlib, sys

p = 2**256 - 2**32 - 977
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
     0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)

def add(P, Q):
    if P is None: return Q
    if Q is None: return P
    if P[0] == Q[0] and P[1] != Q[1]: return None
    if P == Q:
        lam = 3 * P[0] * P[0] * pow(2 * P[1], p - 2, p) % p
    else:
        lam = (Q[1] - P[1]) * pow(Q[0] - P[0], p - 2, p) % p
    x = (lam * lam - P[0] - Q[0]) % p
    return (x, (lam * (P[0] - x) - P[1]) % p)

def mul(P, k):
    R = None
    while k:
        if k & 1: R = add(R, P)
        P = add(P, P)
        k >>= 1
    return R

def lift_x(x):
    y = pow((x**3 + 7) % p, (p + 1) // 4, p)
    return (x, y if y % 2 == 0 else p - y)

def tagged_hash(tag, msg):
    t = hashlib.sha256(tag.encode()).digest()
    return hashlib.sha256(t + t + msg).digest()

def compact_size(n):
    return bytes([n]) if n < 0xFD else b"\xfd" + n.to_bytes(2, "little")

script, cb, program = (bytes.fromhex(a) for a in sys.argv[1:4])
leaf_version, parity = cb[0] & 0xFE, cb[0] & 1
internal = cb[1:33]
path = [cb[i:i + 32] for i in range(33, len(cb), 32)]
print("leaf version:", hex(leaf_version), " parity:", parity)
print("internal key:", internal.hex())
print("merkle path: ", len(path), "hash(es)")

k = tagged_hash("TapLeaf", bytes([leaf_version]) + compact_size(len(script)) + script)
print("leaf hash:   ", k.hex())
for sibling in path:
    k = tagged_hash("TapBranch", min(k, sibling) + max(k, sibling))
print("merkle root: ", k.hex())

t = int.from_bytes(tagged_hash("TapTweak", internal + k), "big")
Q = add(lift_x(int.from_bytes(internal, "big")), mul(G, t))
print("computed Q:  ", Q[0].to_bytes(32, "big").hex(), " parity:", Q[1] % 2)
ok = Q[0].to_bytes(32, "big") == program and Q[1] % 2 == parity
print("MATCH: the script is committed in this output" if ok else "NO MATCH")
```

First test it on a BIP341 test vector (a two-leaf tree):

```bash
python3 check_control_block.py \
  20387671353e273264c495656e27e39ba899ea8fee3bb69fb2a680e22093447d48ac \
  c0ee4fe085983462a184015d1f782d6a5f8b9c2b60130aff050ce221ecf3786592f224a923cd0021ab202ab139cc56802ddb92dcfc172b9212261a539df79a112a \
  712447206d7a5238acc7ff53fbe94a3b64539ad291c7cdbc490b7577e4b17df5
```

Then run it on your own spend:

```bash
PROGRAM=$(bitcoin-cli -regtest getrawtransaction "$TXID" true | jq -r ".vout[$VOUT].scriptPubKey.hex" | cut -c5-)
python3 check_control_block.py "$LEAF" "$CB" "$PROGRAM"
```

**Question:** Does it print MATCH? Which three hashes (with which tags) did it compute on the way?

### Lab 2: On-chain footprint, Taproot versus P2WSH multisig (old Week 5, exercise 4)

**2.1 By hand.** Work out the size of one **input** that spends a 2-of-3 multisig in each of these ways. Use 72 bytes for an ECDSA signature with its sighash byte, 64 bytes for a Schnorr signature, and 33-byte (P2WSH) or 32-byte (Taproot) keys. Remember that every input has 41 non-witness bytes (outpoint 36, empty scriptSig length 1, sequence 4).

| Spend type | Witness items | Witness bytes | Input weight | Input vbytes |
|---|---|---|---|---|
| P2WSH `OP_2 <K1> <K2> <K3> OP_3 OP_CHECKMULTISIG` | | | | |
| P2TR script path, one leaf `multi_a(2,K1,K2,K3)` | | | | |
| P2TR key path (MuSig2 aggregate of the signers) | | | | |

Hint: a `multi_a(2,K1,K2,K3)` leaf is `<K1> OP_CHECKSIG <K2> OP_CHECKSIGADD <K3> OP_CHECKSIGADD OP_2 OP_NUMEQUAL`, and it needs one witness item per key (a signature or an empty item).

**2.2 Measure it.** Create both multisig outputs with keys from `XPRV`, then spend each one with `sendall` (one input, one output):

```bash
measure() {
  local desc="$1#$(bitcoin-cli -regtest getdescriptorinfo "$1" | jq -r .checksum)"
  bitcoin-cli -regtest -named createwallet wallet_name="$2" blank=true > /dev/null
  bitcoin-cli -regtest -rpcwallet="$2" importdescriptors "[{\"desc\":\"$desc\",\"timestamp\":\"now\"}]" > /dev/null
  local addr=$(bitcoin-cli -regtest deriveaddresses "$desc" | jq -r '.[0]')
  bitcoin-cli -regtest -rpcwallet=lab sendtoaddress "$addr" 1 > /dev/null
  bitcoin-cli -regtest -rpcwallet=lab -generate 1 > /dev/null
  local dest=$(bitcoin-cli -regtest -rpcwallet=lab getnewaddress "" bech32m)
  local txid=$(bitcoin-cli -regtest -rpcwallet="$2" -named sendall recipients="[\"$dest\"]" fee_rate=2 | jq -r .txid)
  bitcoin-cli -regtest getrawtransaction "$txid" true | jq "{wallet: \"$2\", vsize, weight, witness_items: (.vin[0].txinwitness | length)}"
}

K1="$XPRV/2001/0"; K2="$XPRV/2002/0"; K3="$XPRV/2003/0"
measure "wsh(multi(2,$K1,$K2,$K3))" ms_wsh
measure "tr($H,multi_a(2,$K1,$K2,$K3))" ms_tr
```

**Question:** Which transaction is smaller? Does that match your table? Both transactions have the same non-witness part, so the whole difference is in the witness.

**Question:** If the three signers used MuSig2 and a key-path spend instead, how big would the same transaction be? Why is Bitcoin Core not doing that here?

---

## Stretch tasks

1. **Spend through leaf A.** Make a second descriptor where the wallet holds the owner's private key (use `$XPRV/1004/0` for the owner and a public key for the heir). Spend through leaf A with no timelock. Compare the witness and the control block with Lab 1.
2. **A split multisig tree.** Instead of one `multi_a` leaf, put each 2-of-2 pair in its own leaf: `tr($H,{and_v(v:pk($K1),pk($K2)),{and_v(v:pk($K1),pk($K3)),and_v(v:pk($K2),pk($K3))}})`. Measure it with `measure` (use a new wallet name). Which leaf did the wallet use, and how long is the control block?
3. **Hide the "no key path" signal.** Using `H` directly tells the world there is no key path. BIP341 suggests using H + r·G with a random r instead. Explain why this hides the signal and what you must keep to prove it later.
4. **Your next step.** Read [After the cohort](../../after-the-cohort.md) and pick one first contribution to try in the next month.
