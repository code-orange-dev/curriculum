# Week 9 exercises

[Week 9 overview](../README.md) · [Solutions](../solutions/README.md) · [Syllabus](../../README.md)

This week starts Taproot. You will look at real Taproot spends, decode a `bc1p` address, and make and spend your own P2TR output on regtest. Read the four lessons in the [week overview](../README.md) first.

---

## Exercise 1: Compare a P2TR key-path spend with a P2WPKH spend

Use [mempool.space](https://mempool.space).

1. Open a recent block and find a transaction whose input is labelled **P2TR** (Taproot). Open the transaction and show the details (the "Details" button shows witness data).
2. Look at the input's **witness**. Count the items and the length of each in bytes (2 hex characters = 1 byte).
3. Decide whether it is a key-path spend or a script-path spend. A key-path spend has exactly one witness item of 64 or 65 bytes. A script-path spend has several items, and the last one (the control block) starts with `c0` or `c1`.
4. Now find a transaction with a **P2WPKH** input (`bc1q...`, 42 characters) and look at its witness in the same way.

**Write down** for each input:

| | P2TR key path | P2WPKH |
|---|---|---|
| Number of witness items | | |
| Size of each item (bytes) | | |
| Does the witness include a public key? | | |
| Transaction id you used | | |

**Question:** Where is the public key for the P2TR spend, if it is not in the witness?

---

## Exercise 2: Decode a `bc1p` address

Take this address from the BIP86 test vectors (it belongs to a well-known test seed, so never send coins to it):

```
bc1p5cyxnuxmeuwuvkwfem96lqzszd02n6xdcjrs20cac6yqjjwudpxqkedrcr
```

1. Split it into the human-readable part, the separator `1`, and the data part.
2. Look up the first data character in the bech32 character set `qpzry9x8gf2tvdw0s3jn54khce6mua7l` (`q` = 0, `p` = 1, `z` = 2, ...). That number is the **witness version**.
3. Run the decoder below to get the witness program and check which checksum (bech32 or bech32m) is valid.
4. Write the scriptPubKey for this address in hex.

```python
# decode_addr.py: decode a segwit address (bech32 or bech32m). Learning code only.
import sys

CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"
BECH32_CONST, BECH32M_CONST = 1, 0x2BC830A3

def polymod(values):
    gen = [0x3B6A57B2, 0x26508E6D, 0x1EA119FA, 0x3D4233DD, 0x2A1462B3]
    chk = 1
    for v in values:
        top = chk >> 25
        chk = (chk & 0x1FFFFFF) << 5 ^ v
        for i in range(5):
            chk ^= gen[i] if (top >> i) & 1 else 0
    return chk

addr = sys.argv[1].lower()
hrp, data = addr.rsplit("1", 1)
values = [CHARSET.index(c) for c in data]
check = polymod([ord(c) >> 5 for c in hrp] + [0] + [ord(c) & 31 for c in hrp] + values)
kind = {BECH32_CONST: "bech32", BECH32M_CONST: "bech32m"}.get(check, "INVALID checksum")

version = values[0]
acc = bits = 0
program = bytearray()
for v in values[1:-6]:            # drop version and the 6 checksum characters
    acc = (acc << 5) | v
    bits += 5
    while bits >= 8:
        bits -= 8
        program.append((acc >> bits) & 0xFF)

print("hrp:", hrp)
print("checksum:", kind)
print("witness version:", version)
print("program (%d bytes): %s" % (len(program), program.hex()))
```

```bash
python3 decode_addr.py bc1p5cyxnuxmeuwuvkwfem96lqzszd02n6xdcjrs20cac6yqjjwudpxqkedrcr
python3 decode_addr.py bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4
```

**Write down:** the witness version, the program length, the program in hex, the checksum type, and the full scriptPubKey. Do the same for the `bc1q` address and compare.

**Question:** Why does every mainnet Taproot address start with `bc1p`, and every native segwit v0 address with `bc1q`?

---

## Exercise 3: Explain the taproot tweak without maths

Write 3 to 6 sentences that explain the taproot tweak to someone who has never seen elliptic curves. Post it on Discord and read at least two other explanations.

A good explanation answers:

- What do you start with (an "internal" key, and maybe a set of scripts)?
- What does the tweak do to the key?
- Why can the owner still sign with the tweaked key?
- Why does nobody else learn whether there were scripts hidden inside?

Analogies are welcome (a sealed envelope, a fingerprint, a lock that has a hidden second keyhole). Say where your analogy breaks down.

---

## Hands-on lab (bitcoin-cli, regtest)

> Tested on Bitcoin Core 29.0 (regtest), November 2026.

You need Bitcoin Core 28 or newer and `jq`. If you have not set up regtest yet, see [Week 1: Bitcoin Core CLI](../../week-01/exercises/bitcoin_core_cli.md).

### Setup

```bash
# -fallbackfee lets sendtoaddress pay a fee on a fresh regtest chain with no fee history
bitcoind -regtest -daemon -txindex=1 -fallbackfee=0.0001
bitcoin-cli -regtest -named createwallet wallet_name=lab || bitcoin-cli -regtest loadwallet lab
bitcoin-cli -regtest -rpcwallet=lab -generate 101
```

If your node is already running without `-txindex` or `-fallbackfee`, run `bitcoin-cli -regtest stop`, wait a few seconds, and start it again with the command above.

### Lab 1: Create a P2TR address and look inside (old Week 5, exercise 1)

**1.1** Create a new wallet and a Taproot address:

```bash
bitcoin-cli -regtest -named createwallet wallet_name=taproot
TR=$(bitcoin-cli -regtest -rpcwallet=taproot getnewaddress "" bech32m)
echo "$TR"
```

**Question:** What does the address start with? How long is it?

**1.2** Look at the address details:

```bash
bitcoin-cli -regtest -rpcwallet=taproot getaddressinfo "$TR" | jq '{scriptPubKey, witness_version, witness_program, desc, hdkeypath}'
```

**Question:** What is the `witness_version`? How many bytes is the `witness_program`? What derivation path does the wallet use, and which BIP defines it?

**1.3** Compare the key inside `desc` with the `witness_program`:

```bash
INTERNAL=$(bitcoin-cli -regtest -rpcwallet=taproot getaddressinfo "$TR" | jq -r .desc | sed -E 's/.*\]([0-9a-f]{64})\).*/\1/')
PROGRAM=$(bitcoin-cli -regtest -rpcwallet=taproot getaddressinfo "$TR" | jq -r .witness_program)
echo "internal key:   $INTERNAL"
echo "witness program: $PROGRAM"
```

**Question:** Are they the same? If not, what is the relationship between them?

**1.4** Decode the scriptPubKey:

```bash
bitcoin-cli -regtest decodescript "$(bitcoin-cli -regtest -rpcwallet=taproot getaddressinfo "$TR" | jq -r .scriptPubKey)"
```

**Question:** What are the first two bytes of the scriptPubKey, and what do they mean? What `type` does Bitcoin Core report?

### Lab 2: Fund it and spend with the key path (old Week 5, exercise 2)

**2.1** Send 1 BTC from `lab` to the Taproot address and confirm it:

```bash
FUND=$(bitcoin-cli -regtest -rpcwallet=lab sendtoaddress "$TR" 1)
bitcoin-cli -regtest -rpcwallet=lab -generate 1
bitcoin-cli -regtest -rpcwallet=taproot listunspent | jq '.[] | {address, amount, desc}'
```

**2.2** Spend part of it to another Taproot address. The `taproot` wallet signs with the key path automatically.

```bash
DEST=$(bitcoin-cli -regtest -rpcwallet=lab getnewaddress "" bech32m)
SPEND=$(bitcoin-cli -regtest -rpcwallet=taproot -named sendtoaddress address="$DEST" amount=0.5 fee_rate=2)
bitcoin-cli -regtest -rpcwallet=lab -generate 1
bitcoin-cli -regtest getrawtransaction "$SPEND" true | jq '{size, vsize, weight, witness: .vin[0].txinwitness, outputs: [.vout[] | .scriptPubKey.type]}'
```

**Question:** How many witness items are there, and how many bytes is each? Is there a sighash byte at the end of the signature?

**Question:** What are the `vsize` and `weight`? Check them by hand: weight = (non-witness bytes x 3) + total bytes, and vsize = weight / 4, rounded up.

### Lab 3: Compare with a P2WPKH spend

Repeat Lab 2 with a native segwit v0 address:

```bash
bitcoin-cli -regtest -named createwallet wallet_name=segwit
WPKH=$(bitcoin-cli -regtest -rpcwallet=segwit getnewaddress "" bech32)
bitcoin-cli -regtest -rpcwallet=lab sendtoaddress "$WPKH" 1
bitcoin-cli -regtest -rpcwallet=lab -generate 1
DEST2=$(bitcoin-cli -regtest -rpcwallet=lab getnewaddress "" bech32)
SPEND2=$(bitcoin-cli -regtest -rpcwallet=segwit -named sendtoaddress address="$DEST2" amount=0.5 fee_rate=2)
bitcoin-cli -regtest -rpcwallet=lab -generate 1
bitcoin-cli -regtest getrawtransaction "$SPEND2" true | jq '{size, vsize, weight, witness: .vin[0].txinwitness, outputs: [.vout[] | .scriptPubKey.type]}'
```

**Question:** Fill in this table. Which input is smaller? Which output is smaller? Which whole transaction is smaller, and why?

| | P2TR (Lab 2) | P2WPKH (Lab 3) |
|---|---|---|
| Witness items | | |
| Signature size | | |
| Transaction vsize | | |
| Output scriptPubKey size | | |

### Lab 4: Compute the tweak yourself

Use this script to compute a BIP86 output key from an internal key. It uses only the Python standard library.

```python
# tweak.py: compute a BIP86 Taproot output key from an internal key.
# For learning only. This code is slow and not safe for real keys.
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
    # BIP340: the point with this x coordinate and an even y
    y = pow((x**3 + 7) % p, (p + 1) // 4, p)
    return (x, y if y % 2 == 0 else p - y)

def tagged_hash(tag, msg):
    t = hashlib.sha256(tag.encode()).digest()
    return hashlib.sha256(t + t + msg).digest()

internal = bytes.fromhex(sys.argv[1])            # 32-byte x-only internal key P
P = lift_x(int.from_bytes(internal, "big"))
t = int.from_bytes(tagged_hash("TapTweak", internal), "big")   # no script tree
Q = add(P, mul(G, t))                             # Q = P + t*G
print("output key:", Q[0].to_bytes(32, "big").hex())
print("parity (y is odd):", Q[1] % 2)
```

**4.1** Check it against the BIP86 test vector from Exercise 2:

```bash
python3 tweak.py cc8a4bc64d897bddc5fbc2f670f7a8ba0b386779106cf1223c6fc5d7cd6fc115
```

**Question:** Does the output key match the witness program you decoded from `bc1p5cyx...` in Exercise 2?

**4.2** Now run it on the internal key from your own wallet (Lab 1.3):

```bash
python3 tweak.py "$INTERNAL"
```

**Question:** Does the output match your `witness_program`? What does the parity line tell you, and where would a script-path spend need that bit?

---

## Stretch tasks

1. **Sighash flags.** Bitcoin Core signs Taproot inputs with `SIGHASH_DEFAULT`, which gives a 64-byte signature. Use `walletcreatefundedpsbt` and `walletprocesspsbt` with `sighashtype` set to `ALL` and compare the signature length.
2. **Annex hunting.** BIP341 reserves a witness item starting with `0x50` as the "annex". Read the BIP and explain how a node tells an annex apart from a signature.
3. **Schnorr by hand.** Read the [BIP340 reference code](https://github.com/bitcoin/bips/blob/master/bip-0340/reference.py) and run its test vectors. Find the line that makes the nonce point R have an even y coordinate.
4. **Old Week 5 assessment questions.** Answer the two Bonus questions in the [solutions](../solutions/README.md#bonus-questions) in writing before you read the model answers.
