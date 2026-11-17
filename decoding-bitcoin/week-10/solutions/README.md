# Week 10 solutions

[Week 10 overview](../README.md) · [Exercises](../exercises/README.md) · [Syllabus](../../README.md) · [After the cohort](../../after-the-cohort.md)

Try the questions and exercises yourself first. These answers show the key facts a strong participant would bring to the final session.

---

## Discussion questions

### 1. What is a tapleaf and a tapbranch? How do they combine into the Merkle root?

A **tapleaf** is one script in the tree, together with its leaf version (`0xc0` for tapscript). Its hash is:

`TapLeaf hash = tagged_hash("TapLeaf", leaf_version || compact_size(script length) || script)`

A **tapbranch** joins two child hashes (leaves or other branches):

`TapBranch hash = tagged_hash("TapBranch", smaller || larger)`

The two children are sorted by byte value before hashing, so a proof does not need to say "left" or "right". You keep combining pairs until one hash is left: the **Merkle root**. The root goes into the tweak: t = tagged_hash("TapTweak", P || root), and Q = P + t·G.

The tree does not need to be balanced. Scripts you expect to use more often can sit closer to the root, so their proofs are shorter and cheaper. The tree can be up to 128 levels deep.

### 2. What is in a control block, and what does it prove?

A control block is the last witness item of a script-path spend (before any annex). It has:

1. **One byte:** the leaf version (`0xc0` for tapscript) combined with the **parity bit** of the output key Q's y coordinate. So it is `c0` or `c1` for tapscript.
2. **32 bytes:** the internal key P.
3. **0 to 128 hashes of 32 bytes:** the Merkle path, the sibling hashes from the leaf up to the root.

Size: 33 + 32·m bytes, where m is the depth of the leaf.

It proves that **the script being run was committed in the output**. The verifier hashes the revealed script into a TapLeaf hash, combines it with each path hash to get the root, computes t from P and the root, and checks that P + t·G equals the Q in the scriptPubKey, with the right parity. If it matches, the script is genuine and the node runs it with the rest of the witness as input.

### 3. Why does a script-path spend only reveal the one script that was used?

Because the output commits only to the **Merkle root** of the tree, not to the full list of scripts. To prove one leaf is in the tree, you need only that leaf and the sibling hashes on its path to the root. Every other leaf appears, at most, as a 32-byte hash that reveals nothing about its content. The verifier never needs the other scripts, because it only checks that the hashes add up to the committed root.

Compare P2SH and P2WSH: the whole script is hashed as one blob, so spending reveals all of it, including `OP_IF` branches that were never used. In Taproot, each alternative can be its own leaf. A spend shows that a script path was used, the depth of the leaf (from the control block length), and that one script. The other conditions stay private, and if the key path is used, even the existence of the tree stays hidden.

### 4. What changed in the Taproot sighash (BIP341) compared with segwit v0?

Segwit v0 (BIP143) already fixed quadratic hashing and committed to the amount of the input being signed. BIP341 goes further:

- It commits to the **amounts of all inputs** and the **scriptPubKeys of all inputs**, not just the one being signed. A hardware wallet can now be sure of the total input value, and so the fee, without seeing the full previous transactions. It also knows which inputs are its own.
- It commits to the **spend type**: key path or script path, and whether an annex is present.
- For script-path spends, it commits to the **tapleaf hash** of the script being run, plus the key version and the position of the last executed `OP_CODESEPARATOR`.
- It adds **`SIGHASH_DEFAULT`** (0x00), which signs like `SIGHASH_ALL` with a 64-byte signature and no sighash byte. Undefined sighash types are invalid.
- It uses a **tagged hash** ("TapSighash") with an epoch byte, so these messages can never collide with other hashes.

### 5. Design a script tree for an inheritance wallet. What goes in the key path, and what goes in each leaf?

A good design puts the **most common case in the key path** and the rare, conditional cases in leaves.

- **Key path:** the owner's key (or a MuSig2 key of the owner's two devices). Day-to-day spending looks like any single-sig payment and reveals nothing.
- **Leaf 1:** heir's key plus a relative timelock, for example `and_v(v:pk(HEIR),older(52560))`, about one year of blocks. If the owner stops moving the coins for a year, the heir can claim them.
- **Leaf 2:** a recovery path, for example 2-of-3 of heir, a trusted friend and a lawyer (`multi_a`), after a longer timelock, in case the heir loses their key.

Important details: `older()` is relative and its maximum is 65,535 blocks (about 15 months), so for longer delays use `after()` (CLTV, absolute). The owner must "refresh" by spending to a new output before the timelock ends, or the heir path opens. Put the more likely leaf higher in the tree for a shorter proof. Write the plan down for the heir, including the descriptor, or they cannot find or spend the coins.

### 6. What's your next step after this cohort: a Code Orange program, a project to contribute to, or a review club?

This is a personal question, so there is no model answer, but a strong answer is **specific and small enough to start this week**. For example:

- "I will join the next Code Orange program on ... and help newer students with the regtest labs."
- "I will attend the [Bitcoin Core PR Review Club](https://bitcoincore.reviews/) every Wednesday for a month and post one review comment."
- "I will build Bitcoin Core from source (`cmake -B build && cmake --build build -j$(nproc)`), run the tests, and find one documentation fix to submit."
- "I will read the [Bitcoin Optech newsletter](https://bitcoinops.org/en/newsletters/) every week and pick one topic to write a short explainer on."

Weak answers are vague ("learn more about Bitcoin"). See [After the cohort](../../after-the-cohort.md) for paths into Bitcoin Core and first open-source contributions.

---

## Exercise answers

### Exercise 1: Capstone

Your values will differ. A complete write-up has all six items. Check these facts:

- The address prefix matches the network: `bcrt1p` (regtest), `tb1p` (signet and testnet), `bc1p` (mainnet), and it decodes as witness version 1 with a 32-byte program.
- The program is the **tweaked** key Q, not the internal key P.
- A key-path spend has one 64-byte (or 65-byte) witness item. A script-path spend has the script's inputs, then the script, then a control block of 33 + 32·m bytes starting with `c0` or `c1`.
- The txids can be checked with `getrawtransaction <txid> true` on your node (or on a signet explorer).

### Exercise 2: Present in 3 minutes

A good presentation keeps to time, shows one concrete thing (a transaction, a test run, a trace) and ends with a next step.

### Exercise 3: Feedback

No model answer. Specific feedback ("the week 4 weight lab needed a worked example first") helps more than general feedback.

---

## Lab answers

### Lab 1: Inheritance output and script-path spend

**1.1** A compressed public key is 33 bytes: a `02` or `03` prefix byte for the y parity, then the 32-byte x coordinate. `cut -c3-` drops the first 2 hex characters (the prefix), which leaves the x-only key that tapscript uses. `H` is the BIP341 "nothing up my sleeve" point: it was made by hashing a known value, so nobody knows its private key. Using it as the internal key means the key path can never be used, and the output can only be spent through the leaves.

**1.3** It fails with `non-BIP68-final`. The input's `sequence` is 5, which (BIP68) means "not until 5 blocks after the coin confirmed", and the leaf's `OP_CHECKSEQUENCEVERIFY` requires that. The coin has only 1 confirmation. To block the heir forever, the owner must keep spending the coin (through leaf A) to a fresh output before each 5-block window ends. Each new output restarts the relative timelock.

**1.4** Three witness items:

| Item | Size | What it is |
|---|---|---|
| 0 | 64 bytes | The heir's Schnorr signature (`SIGHASH_DEFAULT`, no sighash byte) |
| 1 | 36 bytes | The leaf script |
| 2 | 65 bytes | The control block (33 + one 32-byte path hash, since the tree has two leaves) |

Expected size for 1 input and 1 P2TR output: 94 non-witness bytes and 171 witness bytes (marker and flag 2, item count 1, then 1 + 64, 1 + 36 and 1 + 65), so `weight` = 94 x 4 + 171 = 547 and `vsize` = 137 (136.75 rounded up).

**1.5** The leaf script is `<heir x-only key> OP_CHECKSIGVERIFY 5 OP_CHECKSEQUENCEVERIFY`. In hex: `20`, the 32-byte key, `ad`, `55`, `b2`.

- **First byte:** `c0` or `c1`. It encodes the leaf version (`0xc0`, tapscript) and the parity of Q's y coordinate (the last bit).
- **Bytes 2 to 33:** the internal key, which is `H` (`50929b74...803ac0`).
- **Bytes 34 to 65:** the TapLeaf hash of the other leaf (the owner's `pk(OWNER)` script). It is the only path hash because the tree has two leaves.
- **The owner's key does not appear** anywhere. Leaf A shows up only as its hash inside the control block.

**1.6** It prints `MATCH`. On the way it computes a **TapLeaf** hash of the heir's script, one **TapBranch** hash combining it with the sibling leaf hash (the Merkle root), and a **TapTweak** hash of `H` and the root. Adding the tweak times G to `H` gives your output key. The BIP341 test vector also prints `MATCH`.

### Lab 2: Footprint, Taproot versus P2WSH multisig

**2.1** The witness bytes below include the per-input item count byte. The marker and flag (2 bytes) are counted once per transaction, not per input.

| Spend type | Witness items | Witness bytes | Input weight | Input vbytes |
|---|---|---|---|---|
| P2WSH 2-of-3 | 4: empty dummy, 2 signatures, script | 1 + 1 + 73 + 73 + 106 = **254** | 164 + 254 = **418** | **104.5** |
| P2TR script path, `multi_a` leaf | 5: 2 signatures, 1 empty, script, control block | 1 + 65 + 65 + 1 + 105 + 34 = **271** | 164 + 271 = **435** | **108.75** |
| P2TR key path (MuSig2) | 1: signature | 1 + 65 = **66** | 164 + 66 = **230** | **57.5** |

Notes: the P2WSH script is 105 bytes (OP_2, three 34-byte key pushes, OP_3, OP_CHECKMULTISIG). The `multi_a` leaf is 104 bytes (three 33-byte key pushes, OP_CHECKSIG, two OP_CHECKSIGADD, OP_2, OP_NUMEQUAL). The control block is 33 bytes because the tree has only one leaf.

**2.2** Expected results (1 input, 1 P2TR output, 94 non-witness bytes):

- `ms_wsh`: weight about 630, **vsize about 158**, 4 witness items. (Bitcoin Core makes 71-byte low-R signatures, so it is slightly smaller than the table's 72-byte estimate.)
- `ms_tr`: weight 649, **vsize 163**, 5 witness items.

So the **Taproot script path is a little bigger** than P2WSH for a single 2-of-3 leaf. Schnorr signatures save bytes, but `multi_a` needs a witness item for every key (even unused ones) and the control block adds 33 bytes. Taproot multisig is not automatically smaller: the savings come from the key path.

**MuSig2 key path:** the same transaction would have a 68-byte witness (marker and flag 2, count 1, length 1, signature 64), so weight 376 + 68 = 444 and **vsize 111**, about 30% smaller. It would also look like a single-sig payment. Bitcoin Core does not do it here because MuSig2 needs an interactive two-round protocol between the signers to make one aggregate key and one signature. Our descriptor has no aggregate key at all: the internal key is the unspendable `H`, and the three keys only exist inside the leaf script.

---

## Bonus questions

### 1. Why would you use an unspendable internal key, and why is plain H not ideal?

Use one when there must be **no way to spend without the scripts**, for example when every spend must include a timelock, or when there is no single party (or MuSig2 group) who should be able to spend alone. BIP341 suggests the point H, made by hashing the generator G, so nobody can know its private key.

Using H directly is a visible signal: anyone who sees H in a control block knows there was no key path. BIP341 suggests H + r·G with a random r. The result looks like any other key, so observers cannot tell. The wallet must store r, so it can later prove to a co-signer or auditor that the key path is unspendable.

### 2. What does tapscript (BIP342) change compared with legacy Script?

- Signatures are **Schnorr** (BIP340) and keys are 32-byte x-only.
- **`OP_CHECKMULTISIG` is disabled.** `OP_CHECKSIGADD` replaces it, so each signature check can be verified separately (and batch-verified), with no off-by-one dummy.
- The **10,000-byte script size** and **201-opcode** limits are removed. A per-input **signature budget** (50 plus the witness size) replaces sigops counting. The 520-byte push and 1,000-item stack limits stay.
- **`OP_SUCCESSx`** opcodes: unused opcode numbers that make a script succeed at once. Future soft forks can give them new meanings safely.
- `OP_IF` and `OP_NOTIF` must get exactly empty or `0x01` (MINIMALIF is consensus), which removes a malleability source.
- An empty signature makes `OP_CHECKSIG` push false. A non-empty but invalid signature makes the whole script fail.
