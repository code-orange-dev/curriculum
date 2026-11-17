# Week 7 solutions

Model answers for [week 7](../README.md). Try the questions and the [exercises](../exercises/README.md) yourself first.

## Discussion questions

### 1. How does P2SH move cost and complexity from sender to receiver?

With bare multisig, the sender must put the whole script into the output: every public key, M, N and `OP_CHECKMULTISIG`. A 2-of-3 with compressed keys is 105 bytes. The sender pays the fee for those bytes, and their wallet must know how to build that script. There is also no short address to share, so the receiver must hand over a long script.

With P2SH, the receiver hashes their script (the redeem script) and gives the sender a normal-looking address starting with `3` (mainnet) or `2` (testnet and regtest). The sender's output is always the same 23-byte pattern, `OP_HASH160 <20-byte hash> OP_EQUAL`, whatever the script is. The sender's wallet does not need to understand multisig at all.

The full script only appears when the receiver spends the coin. The receiver puts the redeem script and the signatures into the scriptSig and pays the fee for those bytes. The party who wants the complex script pays for it. A side benefit: the UTXO set stores only a 20-byte hash instead of all the keys.

### 2. The OP_CHECKMULTISIG off-by-one bug, and why it was never fixed

`OP_CHECKMULTISIG` pops N, the N public keys, M and the M signatures. Then, because of a bug in the original code, it pops **one more** item, and that extra item is not used. If the stack is empty at that point, the script fails. So every multisig spend must push an extra dummy item first. By convention this is `OP_0`, which is why multisig scriptSigs look like `OP_0 <sig1> <sig2>`.

Fixing it so that the extra pop does not happen would be a **hard fork**. Old nodes would expect the extra item and reject spends without it, and new nodes would see a different stack. Every existing multisig spend would have to be re-checked under two sets of rules. The cost of the bug is only one byte per spend, so it is not worth a hard fork.

The dummy did cause a malleability problem: anyone could replace `OP_0` with any other value and change the txid. BIP147 (NULLDUMMY, a soft fork activated with segwit) requires the dummy to be an empty byte array. Tapscript replaces `OP_CHECKMULTISIG` with `OP_CHECKSIGADD`, which has no dummy.

### 3. Why is bare multisig (P2MS) rarely used today?

- **The sender pays for it.** The scriptPubKey holds all the keys. A 2-of-3 is 105 bytes, compared with 23 bytes for P2SH or 34 bytes for P2WSH.
- **No address.** There is no standard address format, so it is hard to ask someone to pay you.
- **Bad for the UTXO set.** Every node stores the full script until it is spent. Many bare multisig outputs are never spent, because they were used to store data rather than to hold money (for example by fake "public keys" that are really data).
- **Privacy.** The keys and the policy are public from the moment the coin is created.
- **Relay limits.** Bitcoin Core only treats bare multisig with up to 3 keys as standard, and node operators can turn off its relay completely.

P2SH (2012) and then P2WSH (2017) gave the same security with none of these problems. P2TR is now the most private option.

### 4. What is the redeem script, and when does it appear on the blockchain?

The redeem script is the real spending condition, for example `OP_2 <pk1> <pk2> <pk3> OP_3 OP_CHECKMULTISIG`. In P2SH, the output stores only the HASH160 of the redeem script, so the condition is hidden.

The redeem script appears on the blockchain **only when the coin is spent**. It is the last data push in the spending input's scriptSig: `OP_0 <sig1> <sig2> <redeemScript>`. The node checks that it hashes to the value in the output, then runs it with the other items on the stack.

Until then, nobody can tell from the chain whether a `3...` address is multisig, a timelock or a single key wrapped in P2SH. Coins that are never spent never reveal their script.

The redeem script is pushed as a single data item, so it is limited to 520 bytes. That allows at most 15 compressed keys in a P2SH multisig. In P2WSH, the same script is called the **witness script** and sits as the last witness item.

### 5. 2-of-3 multisig vs a single key plus a backup

**Single key with a backup** (for example a seed phrase on paper in a second place): there are two copies of the **same** secret.

- Protects against: losing one copy (fire, lost device).
- Does not protect against: theft. Anyone who finds **either** copy can spend everything. More backups make theft more likely.

**2-of-3 multisig:** three **different** keys, any two can spend.

- Protects against: losing one key (two remain) **and** theft of one key (one key cannot spend). It also helps against coercion and insider risk, because no single person can move the funds.
- Costs: more setup and coordination; you must back up the wallet descriptor (all three public keys or xpubs and the policy), not only the seeds; spends are bigger and cost more; and before taproot the multisig policy is visible on chain when you spend.

Multisig removes the single point of failure. Single-key-plus-backup only removes the single point of loss.

### 6. BIP16 as a soft fork: how did old nodes still accept P2SH spends?

A soft fork makes the rules **stricter**. Every block valid under the new rules is still valid under the old rules, so old nodes keep following the chain without upgrading.

An old node sees the P2SH output as `OP_HASH160 <h> OP_EQUAL`. When it is spent with `OP_0 <sig1> <sig2> <redeemScript>`, the old node runs the scriptSig, then the scriptPubKey: it hashes the top item (the redeem script), compares it with `<h>` and gets true. The spend is valid. To an old node, P2SH looks like "anyone who knows a value with this hash can spend".

New nodes add one extra rule. After that check passes, they deserialize the redeem script and run it with the rest of the stack, so the signatures must really be valid. They also require the scriptSig to be push-only. A spend that fails these new checks would be accepted by old nodes, but miners running the new rules will not put it in a block.

BIP16 was activated in April 2012 after enough miners signalled support.

## Core exercises

### 1. P2MS exercises

We do not publish answers to the Decoding Bitcoin exercises. Check your work against these facts:

- Shape: `OP_M <pk1> ... <pkN> OP_N OP_CHECKMULTISIG`. scriptSig: `OP_0 <sig_a> <sig_b> ...` with M signatures.
- A 2-of-3 with compressed keys is `1 + 3 × (1 + 33) + 1 + 1 = 105` bytes. With uncompressed keys it is `1 + 3 × 66 + 2 = 201` bytes.
- The signatures must be in the **same order** as their public keys. `OP_CHECKMULTISIG` walks through the keys once and does not go back.
- The first `OP_0` is the dummy for the off-by-one bug (discussion question 2).

### 2. Redeem script from a real P2SH multisig spend

Depends on the transaction. A correct answer looks like this:

- scriptSig asm: `OP_0 <sig> <sig> <redeemScript>` (for 2-of-N). The first item is `OP_0`, the dummy.
- Redeem script asm, for example: `OP_PUSHNUM_2 <pk1> <pk2> <pk3> OP_PUSHNUM_3 OP_CHECKMULTISIG`. In hex it starts with `52` and ends with `53ae`, so M = 2 and N = 3. 2-of-3 is the most common setup.
- Number of signatures = M.
- HASH160 of the redeem script bytes equals the 20 bytes in the spent output's `a914...87` scriptPubKey. If it does not, check that you hashed the raw bytes (not the hex text) and did not include the push opcode in front of the script.

### 3. 2-of-3 for a small business

There are many good answers. One example:

| Key | Holder | Device | Location | Seed backup |
|---|---|---|---|---|
| A | Owner 1 | Hardware wallet | Owner 1's home | Steel plate in Owner 1's bank safe box |
| B | Owner 2 | Hardware wallet (different brand) | Owner 2's home | Steel plate in Owner 2's bank safe box |
| C | Company (recovery) | Hardware wallet | Office safe, or a trusted lawyer or collaborative custody service | Sealed backup with the lawyer |

- Normal spending: Owner 1 + Owner 2 (keys A and B).
- One owner loses a device: the other owner + key C.
- One owner leaves: move the funds to a new 2-of-3 with a new key. Do not just "take back" the old key, because it may have been copied.
- Fire at the office: keys A and B still work.
- An owner dies: the other owner + key C, following a written plan.

The important extra backup is the **wallet descriptor** (or all three xpubs with their derivation paths and the 2-of-3 policy). With only two seeds and no information about the third public key, you cannot rebuild the script, so you cannot find or spend the coins. Store a copy of the descriptor with every seed backup. It does not let anyone spend, but it affects privacy, so keep it private.

Using different hardware wallet brands avoids a single firmware bug affecting all keys.

## Lab answers

**Step 1.** The square brackets hold the key origin: the fingerprint of the signer's master key and the BIP32 path to this key. A coordinator copies this into PSBTs (`bip32_derivs`), so each signer can see "this key is mine, at this path" and knows which private key to use. Sharing it is safe for funds (it holds only a public key). It does reveal which of your keys are in the multisig, so share it only with your co-signers.

**Step 2.** The legacy (P2SH) address starts with `2`. The bech32 (P2WSH) address starts with `bcrt1q` and is longer than a P2WPKH address (it holds a 32-byte hash). The redeem script is 210 hex characters, so **105 bytes**. Core shows its type as `multisig`.

As a bare multisig scriptPubKey, the output would be those 105 bytes. The P2SH scriptPubKey is 23 bytes (and P2WSH is 34 bytes).

**Step 3.** Yes, `$MS_SH` is the same address as the legacy address from step 2. Same three keys, same order, same M, so same redeem script and same hash. The descriptor's key origins are only metadata for wallets and do not change the script.

The funding output is `OP_HASH160 <20 bytes> OP_EQUAL` with type `scripthash`. No public keys are visible. An observer only learns that this is a P2SH output. They cannot tell that it is multisig. (The other output, also `scripthash`, is the miner's change. Core makes the change the same type as the payment, here P2SH-wrapped segwit, so the change is harder to spot.)

**Step 4.** The coordinator adds the `redeem_script` (the multisig script) and `bip32_derivs` for all three keys (pubkey, fingerprint, path). It also adds the previous transaction (`non_witness_utxo`), which legacy inputs need. Before signing, `analyzepsbt` shows `next: signer` and lists three missing signatures (as key hashes), with `estimated_vsize` 334.

After signer 1 only, the input has one partial signature, and `analyzepsbt` still shows `next: signer` and lists the other two keys as missing (it needs one more of them). After combining signers 1 and 3 it shows `next: finalizer`. Signer 1 cannot finalize because the redeem script needs 2 valid signatures. Signer 2 was not needed because any 2 of the 3 keys are enough. Here signers 1 and 3 signed.

**Step 5.** The scriptSig asm is `0 <sig1>[ALL] <sig3>[ALL] <redeemScript>`:

1. `0`: the dummy for the `OP_CHECKMULTISIG` off-by-one bug. Must be empty (BIP147).
2. and 3. The two signatures, in the same order as their keys appear in the redeem script.
4. The redeem script (105 bytes, starting `52` and ending `53ae`).

Yes, this is the first time the three public keys appear on the blockchain.

`size` equals `vsize` (no witness): 334 bytes (weight 1336) for one input and one P2WPKH output. Signatures can be 1 byte shorter now and then, so you may see 333.

**Step 6.** The scriptSig is empty. The witness has four items: an **empty** item (the dummy, shown as `""`), two signatures, and the witness script (the same 105-byte multisig script).

`vsize` is 146 vbytes (size 336, weight 582), compared with 334 for the P2SH spend. The base part is the same as any segwit input. The roughly 250 bytes of signatures and script are witness data and count at one quarter. That is a saving of about 56 percent of the fee. A signature can be 1 byte shorter, which changes `size` and `weight` by 1 but usually not `vsize`.

## Stretch answers

1. `createmultisig` refuses with `redeemScript exceeds size limit: 547 > 520`. 16 compressed keys make `1 + 16 × 34 + 1 + 1 = 547` bytes. In P2SH, the redeem script is pushed as one data item, and pushes are limited to 520 bytes. 15 keys make 513 bytes, so **15** is the maximum.
2. Core shows `type: multisig` and no `address` field. Bare multisig has no address format.
3. The address changes unless the keys were already in sorted order, because `sortedmulti` sorts the keys by their bytes, and a different order gives a different script and hash. (With random keys there is a 1 in 6 chance for 3 keys that they were already sorted, and then the address stays the same.) Sorted keys (BIP67) mean every participant gets the same address from the same set of keys, whatever order they were entered in. It also simplifies backups: you need the keys and the policy, not the order.
4. `createwallet` with a new name (for example `ms_sh_restored`) and `disable_private_keys=true blank=true`, then `importdescriptors` with the same descriptor and an old `timestamp` (for example `0`), so the wallet rescans and finds the coins. If you already spent the coin in step 4, the balance is 0, but `listtransactions "*" 10 0 true` shows the 1 BTC receive and the spend. With only three seeds, you would also need to know the derivation path used for each key, the script type (`sh`, `wsh`, ...), M, and whether keys were sorted. This is why multisig wallets ask you to back up the descriptor.

## Bonus questions

These are assessment questions from the earlier version of this course.

### Explain how P2SH works. Why was it introduced, and what problem does it solve for the sender?

P2SH (BIP16, 2012) lets a coin be locked to the **hash of a script** instead of the script itself. The output is always `OP_HASH160 <20-byte hash> OP_EQUAL`, shown as an address starting with `3`. To spend, the owner reveals the redeem script and the data it needs (such as signatures). Nodes check that the script hashes to the committed value, then run it.

It was introduced because complex scripts such as multisig were too hard to use. Before P2SH, a sender had to:

- know how to build the receiver's custom script,
- put the whole script in the output and pay the fee for it,
- and copy a long script instead of a short address.

P2SH solves this for the sender. Every payment looks like a normal payment to a short address with a checksum, and costs the same. The receiver, who chose the complex script, pays for it when spending. It also hides the policy until spend time and keeps the UTXO set small. Later, segwit used the same idea for P2WSH, and nested segwit (P2SH-P2WPKH) used P2SH to let old wallets pay new segwit wallets.
