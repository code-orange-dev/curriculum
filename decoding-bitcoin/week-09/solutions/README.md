# Week 9 solutions

[Week 9 overview](../README.md) · [Exercises](../exercises/README.md) · [Syllabus](../../README.md)

Try the questions and exercises yourself first. These answers show the key facts a strong participant would bring to the session.

---

## Discussion questions

### 1. What problems was Taproot designed to solve for privacy, efficiency and flexibility?

**Privacy:** before Taproot, the type of output (single-sig, multisig, P2SH script) was often visible, and spending a P2SH or P2WSH output revealed the whole script, including branches that were never used. With Taproot every output looks the same (a 32-byte key), and the common case, where everyone agrees, is a key-path spend that looks like any single-signature payment.

**Efficiency:** Schnorr signatures are a fixed 64 bytes, smaller than ~71-72 byte DER ECDSA signatures. With key aggregation, an n-of-n multisig needs one key and one signature on-chain. A script-path spend only reveals the one leaf that is used, plus a short Merkle proof. Schnorr also allows batch verification.

**Flexibility:** tapscript has leaf versions and `OP_SUCCESSx` opcodes, so new features can be added later by soft fork. It also removes old limits such as the 10,000-byte script size and the 201-opcode limit.

Taproot (BIP340, 341, 342) activated at block 709,632 in November 2021.

### 2. What is a tweaked public key, and why does P2TR use x-only (32-byte) keys?

The owner starts with an **internal key** P. The output key is Q = P + t·G, where t is a tagged hash ("TapTweak") of P and, if there is a script tree, its Merkle root. With no script tree, BIP86 says to tweak with the hash of P alone. Q goes into the output. Because t is public once you know P (and the tree), the owner can compute the matching private key (d + t) and sign for Q directly. The tweak also **commits** to the scripts: nobody can later add a different script tree, because that would change Q.

**x-only keys:** BIP340 keys and nonces are just the 32-byte x coordinate. The y coordinate is assumed to be the even one, so the usual `02`/`03` prefix byte is dropped. This saves one byte in every output and signature, with no meaningful loss of security. If the real Q has an odd y, the signer negates their key, and for script-path spends the parity bit is stored in the control block.

### 3. Compare Schnorr and ECDSA. What does linearity allow you to do?

Both use the same curve (secp256k1) and the same kind of keys. The signing equations differ:

- **Schnorr (BIP340):** s = k + e·x, where e is a tagged hash of R, P and the message. Verify: s·G = R + e·P.
- **ECDSA:** s = k⁻¹·(z + r·x). The modular inverse makes it non-linear.

Schnorr is **linear**: signatures and keys can be added together. If Alice and Bob add their public keys, they can also produce one combined signature that verifies against the combined key. This enables key aggregation (MuSig2), threshold schemes (FROST), adaptor signatures, and batch verification, where a node checks many signatures faster than one by one.

Other advantages: Schnorr has a simple security proof (under standard assumptions), signatures are a fixed 64 bytes, and BIP340 signatures are not malleable. ECDSA multi-party signing is possible but needs much more complex protocols.

### 4. What is key aggregation (MuSig), and why does it make multisig look like a single-key spend?

Key aggregation combines several public keys into one aggregate key. MuSig2 (BIP327) does this safely: each key is multiplied by a coefficient derived from all the keys, which stops a "rogue key" attack where one participant picks their key to cancel out the others.

To spend, the signers run a two-round protocol: they exchange nonces, then each sends a partial signature. The partial signatures add up to one ordinary 64-byte BIP340 signature for the aggregate key.

On-chain there is **one key and one signature**, exactly like a single-sig key-path spend. Nobody can tell that 2, 3 or 100 people signed. This is an n-of-n scheme. For k-of-n you either use a threshold protocol (FROST) or put several MuSig2 key combinations in Taproot leaves, with the most likely one as the key path.

### 5. Walk through a key-path spend: what is in the witness, and what does a node check?

The witness has **one item**: a BIP340 Schnorr signature. It is 64 bytes for `SIGHASH_DEFAULT`, or 65 bytes if a sighash type byte is added (and that byte must not be `0x00`). If there are two or more items and the last starts with `0x50`, that last item is an annex and is removed first.

The node:

1. Sees the scriptPubKey `OP_1 <32 bytes>`, so this is segwit v1 (Taproot) and the 32 bytes are the output key Q.
2. Sees exactly one witness item, so this is a key-path spend (not a script path).
3. Builds the BIP341 signature message. It commits to the transaction, the amounts and scriptPubKeys of **all** inputs, and the sighash type.
4. Verifies the Schnorr signature against Q.

No script runs, no public key is revealed (Q is already in the output), and nothing shows whether a script tree exists.

### 6. Why did Taproot addresses need bech32m instead of bech32?

Bech32 (BIP173) has a weakness: if an address ends in the character `p`, you can insert or delete `q` characters just before it and the checksum still passes. For segwit v0 this is harmless because the program length must be exactly 20 or 32 bytes, so a changed length is rejected. But future witness versions allow any program length from 2 to 40 bytes, so a typo could create a valid address for a different, possibly unspendable, output.

BIP350 defines **bech32m**: the same format with a different checksum constant (`0x2bc830a3` instead of `1`), which removes this weakness. Witness version 0 keeps bech32; version 1 and above must use bech32m. A decoder checks that the checksum type matches the version, so a v1 address with a bech32 checksum is invalid.

---

## Exercise answers

### Exercise 1: P2TR key path versus P2WPKH

Your transaction ids will differ. A correct table looks like this:

| | P2TR key path | P2WPKH |
|---|---|---|
| Number of witness items | 1 | 2 |
| Size of each item (bytes) | 64 (or 65 with a sighash byte) | about 71-72 (DER signature + sighash byte), then 33 |
| Does the witness include a public key? | No | Yes, a 33-byte compressed key starting `02` or `03` |

**Answer:** For P2TR the public key (the tweaked output key Q) is already in the output's scriptPubKey: `OP_1 <32-byte key>`. P2WPKH outputs only hold a 20-byte hash of the key, so the spender must reveal the key in the witness.

If you found an input with 3 or more items whose last item starts with `c0` or `c1`, that is a script-path spend (week 10).

### Exercise 2: Decode a `bc1p` address

| | `bc1p5cyx...edrcr` | `bc1qw508...f3t4` |
|---|---|---|
| hrp | `bc` | `bc` |
| First data character | `p` = 1 | `q` = 0 |
| Witness version | 1 | 0 |
| Checksum | bech32m | bech32 |
| Program | 32 bytes: `a60869f0dbcf1dc659c9cecbaf8050135ea9e8cdc487053f1dc6880949dc684c` | 20 bytes: `751e76e8199196d454941c45d1b3a323f1433bd6` |
| scriptPubKey | `5120a60869f0dbcf1dc659c9cecbaf8050135ea9e8cdc487053f1dc6880949dc684c` | `0014751e76e8199196d454941c45d1b3a323f1433bd6` |

In the scriptPubKey, `51` is `OP_1` (version 1) and `00` is `OP_0` (version 0). `20` and `14` are push lengths (32 and 20 bytes).

**Answer:** The first character after `bc1` encodes the witness version. In the bech32 character set, `q` is 0 and `p` is 1. So all v0 addresses start `bc1q` and all v1 addresses start `bc1p`. (The `bc1q` example is the P2WPKH address for the dummy key with private key 1, the same key we used in week 8.)

### Exercise 3: Explain the tweak

There is no single answer. A strong one, for example:

> You start with your normal key. If you also want backup spending rules, you write them down and take a fingerprint of the list. You then mix that fingerprint into your key to make a new key, and that new key is what goes on the blockchain. You can still sign with the new key, because you know exactly what was mixed in. Nobody else can tell whether anything was mixed in, or what, unless you choose to reveal the list and prove it matches. Where the analogy breaks: the "mixing" is elliptic curve addition, and even with no backup rules you still mix in a hash of the key itself.

Check that the explanation covers: the internal key, the commitment to scripts, the owner can still sign, and outsiders learn nothing.

---

## Lab answers

### Lab 1: Create a P2TR address

**1.1** It starts with `bcrt1p` (regtest's hrp is `bcrt`). It is 64 characters long on regtest (62 on mainnet), because the program is 32 bytes.

**1.2** `witness_version` is 1 and `witness_program` is 32 bytes (64 hex characters). `hdkeypath` is `m/86h/1h/0h/0/N`. This is the BIP86 path: purpose 86, coin type 1 (all test networks), account 0, receive chain 0, address index N.

**1.3** They are **different**. The key in `desc` (inside `tr(...)`) is the internal key P. The witness program is the tweaked output key Q = P + t·G with t = tagged_hash("TapTweak", P). Lab 4 proves this.

**1.4** The scriptPubKey is `5120` followed by 32 bytes. `0x51` is `OP_1`, which marks witness version 1. `0x20` means "push 32 bytes". Bitcoin Core reports `type` as `witness_v1_taproot` and the `asm` as `1 <32-byte hex>`.

### Lab 2: Key-path spend

**2.2** One witness item of 64 bytes (128 hex characters). There is no sighash byte: Bitcoin Core uses `SIGHASH_DEFAULT`, which behaves like `SIGHASH_ALL` but saves the byte.

If both outputs are P2TR (Bitcoin Core usually picks a Taproot change output when you pay a Taproot address), the numbers are:

- Non-witness bytes: version 4 + input count 1 + input 41 + output count 1 + two outputs 2 x 43 + locktime 4 = **137**
- Witness bytes: marker and flag 2 + item count 1 + length 1 + signature 64 = **68**
- `size` = 205, `weight` = 137 x 3 + 205 = **616**, `vsize` = 616 / 4 = **154**

If your change output is P2WPKH instead, the numbers are 12 vbytes smaller (31-byte output instead of 43).

### Lab 3: P2WPKH comparison

| | P2TR (Lab 2) | P2WPKH (Lab 3) |
|---|---|---|
| Witness items | 1 | 2 |
| Signature size | 64 bytes | about 71 bytes (Bitcoin Core makes low-R signatures, so 70-byte DER + 1 sighash byte is typical) |
| Transaction vsize | 154 | about 141 |
| Output scriptPubKey size | 34 bytes (43 with amount and length) | 22 bytes (31 with amount and length) |

- **Input:** P2TR is smaller, about 57.5 vB versus about 68 vB, because there is no public key in the witness and the signature is shorter.
- **Output:** P2WPKH is smaller, because it holds a 20-byte hash instead of a 32-byte key.
- **Whole transaction:** for this 1-input, 2-output payment, P2WPKH is slightly smaller. Taproot's real savings show up when you spend (each input is cheaper) and above all in multisig and complex scripts, where the key path hides everything.

### Lab 4: Compute the tweak

**4.1** Yes. The script prints `a60869f0dbcf1dc659c9cecbaf8050135ea9e8cdc487053f1dc6880949dc684c`, the same program you decoded from `bc1p5cyx...` in Exercise 2. The parity line prints 1, so this Q has an odd y coordinate.

**4.2** The output key must equal your `witness_program`. The parity bit says whether Q's y coordinate is odd. A key-path spend does not need it (the signer adjusts their private key instead). A script-path spend does: the first byte of the control block is the leaf version (`0xc0`) plus this parity bit, so the control block starts with `c0` or `c1`. The verifier needs it to recompute Q from P and the Merkle root and check it matches the output.

---

## Bonus questions

These are the assessment questions from the old Week 5.

### 1. Explain how Taproot improves privacy. How does the key-path spend make complex scripts indistinguishable from simple payments?

Every P2TR output is just `OP_1 <32-byte key>`. Whether that key belongs to one person, is a MuSig2 aggregate of many people, or hides a tree of scripts, the output looks the same. When the parties agree, they spend with the key path: one 64-byte signature, nothing else. That witness is identical in shape to a single-sig wallet payment, so an observer cannot tell a Lightning channel close, a 3-of-3 company wallet or a normal payment apart.

Even when a script is needed, the script path reveals only the one leaf that was used, plus a Merkle proof. The other leaves stay hidden. Before Taproot, P2SH and P2WSH revealed the full script, including all unused conditions.

Limits: a script-path spend does show that scripts existed, and other on-chain patterns (amounts, timing, address reuse) can still leak information.

### 2. What are Schnorr signatures and how do they enable key aggregation (MuSig2)? Why couldn't this be done with ECDSA?

A Schnorr signature (BIP340) is a pair (R, s) where s = k + e·x and e = hash(R, P, message). It is verified by checking s·G = R + e·P. Because the equation is linear, several signers can, in the simplest picture, add their nonces (R = R1 + R2) and their partial signatures (s = s1 + s2) and get a valid signature for the sum of their keys. The real protocol adds protections: MuSig2 (BIP327) weights each key with a coefficient to stop rogue key attacks, and uses two nonces per signer so it is safe in only two communication rounds. The result is a normal 64-byte signature.

ECDSA's signing equation is s = k⁻¹(z + r·x). The inverse of the nonce k means partial signatures cannot just be added. Multi-party ECDSA exists, but it needs heavy cryptography (multi-party computation or homomorphic encryption) and many rounds, so in practice Bitcoin used `OP_CHECKMULTISIG` with one signature per key, which is bigger and shows everyone that it is a multisig.
