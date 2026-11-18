# Week 6 solutions

Model answers for [week 6](../README.md). Try the questions and the [exercises](../exercises/README.md) yourself first.

## Discussion questions

### 1. Run OP_2 OP_3 OP_ADD OP_5 OP_EQUAL step by step

Script is read left to right. Data and number opcodes push onto the stack. Other opcodes pop their inputs from the top and push their result.

| Step | Item | Stack after (top on the right) |
|---|---|---|
| 1 | `OP_2` | `2` |
| 2 | `OP_3` | `2 3` |
| 3 | `OP_ADD` | `5` (pops 3 and 2, pushes 2+3) |
| 4 | `OP_5` | `5 5` |
| 5 | `OP_EQUAL` | `1` (pops both, pushes 1 because they are equal) |

The script ends with one item, `1`, on top of the stack. Bitcoin treats a non-zero top item as true, so the script succeeds. If we had pushed `OP_6` instead of `OP_5`, `OP_EQUAL` would push an empty byte array (false) and the script would fail.

There are no variables and no memory other than the stack (plus a second "alt stack" that a few opcodes use). Everything the script needs must be pushed first.

### 2. scriptPubKey vs scriptSig, and the order they run in

The **scriptPubKey** (locking script) is in a transaction **output**. It sets the condition for spending, for example "provide a signature for this public key hash". The person paying chooses it, usually by using the receiver's address.

The **scriptSig** (unlocking script) is in the **input** of a later transaction that spends that output. It provides the data that meets the condition, such as a signature and a public key.

To validate, a node runs the **scriptSig first**. Then it runs the **scriptPubKey** on the stack that the scriptSig left behind. The spend is valid if no opcode fails and the top of the stack is true at the end.

Since 2010 the two scripts run separately, sharing only the stack. Before that they were joined into one script, which allowed a bug: a scriptSig of `OP_1 OP_RETURN` ended execution early with true on the stack and could spend almost any coin. For standard relay, the scriptSig must contain only data pushes. In segwit, the scriptSig is empty and the data is in the witness.

### 3. Why did P2PKH replace P2PK?

1. **Shorter addresses with a checksum.** A P2PK "address" would be the whole public key (33 or 65 bytes). P2PKH uses a 20-byte hash, encoded in Base58Check with a 4-byte checksum. That gives a short string that can be typed, printed and checked for typos.
2. **Smaller outputs.** A P2PKH scriptPubKey is 25 bytes. P2PK is 35 bytes (compressed key) or 67 bytes (uncompressed, as in 2009). The sender pays for output size, and every unspent output sits in every node's UTXO set.
3. **The public key stays hidden until you spend.** Only the hash is on chain. If elliptic curve cryptography were ever weakened (for example by a large quantum computer), coins in unspent P2PKH outputs with never-used addresses would have an extra layer of protection.

The cost moves to the spender: a P2PKH scriptSig must include the public key (33 bytes), but a P2PK scriptSig is only the signature.

### 4. Run a P2PKH spend step by step

scriptSig: `<sig> <pubkey>`. scriptPubKey: `OP_DUP OP_HASH160 <pkh> OP_EQUALVERIFY OP_CHECKSIG`.

| Step | Item | Stack after (top on the right) |
|---|---|---|
| 1 | `<sig>` | `sig` |
| 2 | `<pubkey>` | `sig pubkey` |
| 3 | `OP_DUP` | `sig pubkey pubkey` |
| 4 | `OP_HASH160` | `sig pubkey hash160(pubkey)` |
| 5 | `<pkh>` | `sig pubkey hash160(pubkey) pkh` |
| 6 | `OP_EQUALVERIFY` | `sig pubkey` (fails here if the hashes differ) |
| 7 | `OP_CHECKSIG` | `1` (fails, pushes false, if the signature is bad) |

Steps 1 and 2 come from the scriptSig. Then the scriptPubKey runs on that stack.

- Step 6 checks that the provided public key is the one the coin was locked to.
- Step 7 checks that the signature is valid for that key and for this transaction's sighash.

The final `1` means success. `OP_EQUALVERIFY` is `OP_EQUAL` followed by `OP_VERIFY`: it stops the script immediately on failure instead of leaving false on the stack.

### 5. Why is Script deliberately not Turing complete?

Script has no loops and no backward jumps. `OP_IF` and `OP_ELSE` only skip forward. Every script runs at most once through, so the work it can cause is bounded by its length. There are also hard limits: 10,000 bytes per script, 201 non-push opcodes, 520 bytes per stack item and 1,000 items on the stacks.

Every full node must run every script in every block. If scripts could loop, one transaction could make every node work forever, or for a very long time (a denial-of-service attack). Nobody can tell in general whether a program will stop (the halting problem), so you could not reject bad scripts in advance. With Script, the cost of validation is known before it runs. Fees per byte are therefore a fair price for the work.

A simple language is also easier to analyse. Wallets can reason about what a script allows (Miniscript does this). Fewer features means fewer ways for consensus bugs to split the network. Complex logic can still be built off chain and enforced with simple on-chain checks.

### 6. Why disable opcodes in a running system?

In 2010 Satoshi disabled a group of opcodes, including `OP_CAT`, `OP_SUBSTR`, `OP_LEFT`, `OP_RIGHT`, `OP_AND`, `OP_OR`, `OP_XOR`, `OP_INVERT`, `OP_MUL`, `OP_DIV`, `OP_MOD`, `OP_2MUL`, `OP_2DIV`, `OP_LSHIFT` and `OP_RSHIFT`. A script that contains one of them now fails, even in a branch that is not executed.

The reason was safety. Some of these opcodes had bugs or risks that could crash nodes or use up memory. `OP_LSHIFT` could crash a node. `OP_CAT` used repeatedly could build huge stack items. Around the same time, the `OP_RETURN` bug (see question 2) showed that Script had not been reviewed carefully. In a system that holds real money, a bug that crashes every node or lets anyone spend any coin is far worse than losing a feature.

Disabling was also easy to deploy. Making previously valid scripts invalid is a tightening of the rules, so it is a soft fork. Old nodes still accept the new chain. Adding features back needs a careful soft fork. That is why proposals like re-enabling `OP_CAT` take years of discussion.

## Core exercises

### 1. P2PK in block 9 and block 170

- Block 9's coinbase scriptPubKey is 67 bytes: `41` (push the next 65 bytes), a 65-byte public key starting with `04` (`0411db93e1dc...`), then `ac` (`OP_CHECKSIG`). In asm: `OP_PUSHBYTES_65 0411db93...b412a3 OP_CHECKSIG`.
- `04` means an **uncompressed** key: the full x and y coordinates, 32 bytes each. Early Bitcoin used uncompressed keys.
- The block 170 input scriptSig contains only one push: a DER signature of about 71 bytes ending in `01` (SIGHASH_ALL). There is no public key, because the P2PK scriptPubKey already contains it. Execution is `<sig>`, then `<pubkey> OP_CHECKSIG`, leaving true.
- Both outputs of the block 170 transaction are also P2PK (`41 <65-byte key> ac`): 10 BTC to the receiver and 40 BTC back to the sender as change.

### 2. P2PKH stack trace

Your trace should match the 7-step table in discussion question 4, with your real values in place of `sig`, `pubkey` and `pkh`.

- A wrong public key fails at **step 6** (`OP_EQUALVERIFY`), because its HASH160 does not match the hash in the scriptPubKey.
- The right key with a bad signature passes step 6 and fails at **step 7** (`OP_CHECKSIG` pushes false, and the script ends false).
- A valid spend ends with a single true value. The node checks "top of stack is non-zero" and accepts.

### 3. Output types in a recent transaction

The answer depends on the transaction. A correct answer gives each output's type, size and asm. Expected sizes:

| Type | scriptPubKey size |
|---|---|
| P2PKH | 25 bytes |
| P2SH | 23 bytes |
| P2WPKH | 22 bytes |
| P2WSH | 34 bytes |
| P2TR | 34 bytes |
| OP_RETURN | 1 byte plus the data pushes |

P2WPKH is the shortest standard type. P2WSH and P2TR are the longest of the address types (34 bytes), because they carry a 32-byte hash or key. On mempool.space today, most outputs are P2WPKH or P2TR.

## Lab answers

**Step 1.** `asm` is `2 3 OP_ADD 5 OP_EQUAL`. Core shows small numbers as plain digits. The `type` is `nonstandard`, because it does not match any standard template. With `OP_6`, `decodescript` still decodes it without complaint. `decodescript` only parses the bytes into opcodes and shows information about the script (for example its P2SH address). It does **not** execute it, so it cannot tell you whether it would succeed.

**Step 2.** The scriptPubKey is 25 bytes: `76` OP_DUP, `a9` OP_HASH160, `14` push 20 bytes, then the 20-byte public key hash, `88` OP_EQUALVERIFY, `ac` OP_CHECKSIG. Core shows `type: pubkeyhash`.

**Step 3.** The hash matches the 20 bytes between `76a914` and `88ac`. The output stores a hash because it is shorter (20 bytes instead of 33), gives a short address with a checksum, and keeps the public key private until the coin is spent.

**Step 4.** The scriptSig asm is `<signature>[ALL] <pubkey>`. The second item is exactly `$PUB`. `[ALL]` is Core showing that the signature's last byte is `01`, SIGHASH_ALL (week 5). The scriptSig is 106 bytes (212 hex characters): 1 push byte (`47`) + 71 signature bytes + 1 push byte (`21`) + 33 key bytes. Bitcoin Core makes 71-byte signatures; about 1 in 256 is 70 bytes, which makes the scriptSig 105 bytes.

**Step 5.** `type` is `pubkey`, and there is **no** `address` field: P2PK has no standard address format. The script is 35 bytes (`21`, a 33-byte compressed key, `ac`), compared with 67 bytes for the uncompressed keys of 2009. To spend it, the scriptSig would be only `<signature>`. It is shorter than P2PKH because the public key is already in the scriptPubKey.

**Step 6.** Regtest types and prefixes:

| Address | Type in Core | Prefix | scriptPubKey pattern |
|---|---|---|---|
| legacy | `pubkeyhash` | `m` or `n` | `76a914...88ac` |
| p2sh-segwit | `scripthash` | `2` | `a914...87` |
| bech32 | `witness_v0_keyhash` | `bcrt1q` | `0014...` |
| bech32m | `witness_v1_taproot` | `bcrt1p` | `5120...` |

The change is the output whose value is not 0.1 BTC (the wallet adds it at a random position). In our test it was a fifth output of type `witness_v1_taproot`: because one of the payments goes to a taproot address, Bitcoin Core makes the change taproot too.

## Stretch answers

1. Depends on the transaction. For an `OP_RETURN` output: `OP_RETURN` makes the script fail immediately, so the output is provably unspendable. Nodes can leave it out of the UTXO set. It is used to store small amounts of data. For a bare multisig output `OP_1 <key1> <key2> <key3> OP_3 OP_CHECKMULTISIG`, any one of the three keys can spend it (week 7 covers this).
2. `OP_1 OP_2 OP_ADD OP_4 OP_EQUAL`: stack `1`, `1 2`, `3`, `3 4`, then `OP_EQUAL` pushes false. The script runs to the end but **fails** because the top is false. `OP_1 OP_DUP OP_ADD OP_2 OP_EQUALVERIFY`: stack `1`, `1 1`, `2`, `2 2`, then `OP_EQUALVERIFY` passes and leaves an **empty** stack. An empty stack at the end also counts as failure, so a real script would need something after it (such as an `OP_CHECKSIG`).
3. In `EvalScript`, `OP_EQUAL` and `OP_EQUALVERIFY` share one case. After pushing the result, if the opcode is `OP_EQUALVERIFY` it pops the result again and returns an error if it was false. Disabled opcodes are checked near the top of the loop: if the opcode is one of the disabled ones, the function returns `SCRIPT_ERR_DISABLED_OPCODE`, even when inside a branch that is not executed.
4. Uncompressed: 65 bytes (`04` + 32-byte x + 32-byte y). Compressed: 33 bytes (`02` or `03` + 32-byte x). For each x there are only two possible y values on the curve, one even and one odd. `02` means "y is even", `03` means "y is odd", so y can be recomputed.

## Bonus questions

These are assessment questions from the earlier version of this course.

### Explain the difference between scriptPubKey and scriptSig. How do they work together?

The scriptPubKey is the lock on an output. The scriptSig is the key presented later by the input that spends it. The node runs the scriptSig, which pushes data such as a signature and a public key. Then it runs the scriptPubKey on the same stack, and the scriptPubKey checks that data. If nothing fails and the stack ends with a true value on top, the input is valid.

Two details matter. First, the scriptPubKey decides **what** must be proved, and the scriptSig only supplies **evidence**. That is why the scriptSig should contain only data pushes. Second, the signature inside the scriptSig signs the spending transaction (the sighash), so the evidence cannot be copied to a different transaction. In segwit outputs, the same idea holds, but the evidence moves from the scriptSig to the witness, and the scriptPubKey is a short "witness program" that tells the node which template to apply.

See discussion question 2 for the order of execution and the 2010 fix.

### Why is Script intentionally not Turing complete? What are the security implications?

See discussion question 5 for the main answer. The security points in short:

- **Bounded cost.** No loops, so the validation cost of any script is known from its size. No transaction can make nodes run forever. This protects the network from denial-of-service attacks.
- **Predictable outcomes.** A script either succeeds or fails, with no hidden state and no outside data. Every node gets the same answer, which is essential for consensus.
- **Analysable.** Wallets and auditors can work out exactly which keys or conditions can spend a coin. Miniscript relies on this.
- **Smaller attack surface.** Fewer features means fewer chances for a bug that could split the network or let coins be stolen.

The trade-off is expressiveness. Complex contracts must be built from simple pieces (signatures, hashes, timelocks) or moved off chain.
