# Week 5 solutions

Model answers for [week 5](../README.md). Try the questions and the [exercises](../exercises/README.md) yourself first. These answers are one good way to explain each idea, not the only way.

## Discussion questions

### 1. What is the sighash, and why not sign the whole raw transaction?

The sighash is the 32-byte message digest that the private key actually signs. It is built from a modified copy of the spending transaction, then hashed (double SHA-256).

You cannot sign the raw transaction as it will be broadcast, because the signature itself goes inside that transaction. The signature would have to sign itself, which is circular. So the algorithm leaves the signatures out and fills in other data instead.

For legacy inputs, the signer blanks every scriptSig, puts the previous output's script (the "scriptCode") in the input being signed, appends the 4-byte sighash type and hashes the result. Segwit v0 inputs use a new algorithm from BIP143. It hashes the prevouts, sequences and outputs once and reuses those hashes for every input, and it includes the amount being spent. Taproot (BIP341) goes further and commits to the amounts and scriptPubKeys of all inputs.

The sighash flag at the end of the signature tells the verifier which parts of the transaction were included.

### 2. ALL, NONE, SINGLE, and when to use ANYONECANPAY

- **SIGHASH_ALL (0x01):** signs all inputs and all outputs. Nobody can change anything without breaking the signature. Almost every wallet uses this.
- **SIGHASH_NONE (0x02):** signs all inputs but no outputs. "I agree to spend these coins, anyone may decide where they go." Dangerous on its own.
- **SIGHASH_SINGLE (0x03):** signs all inputs and only the output with the same index as this input. Other outputs can change. In legacy signing, if there is no output at that index, the sighash becomes the number 1, a famous bug that can let anyone spend the coin.

**ANYONECANPAY (0x80)** is combined with one of the above. It signs only the current input, so other people can add inputs.

Uses: `ALL|ANYONECANPAY` for crowdfunding. The outputs are fixed (pay the project) and anyone can add an input, but the transaction is only valid once the inputs cover the target. `SINGLE|ANYONECANPAY` makes a signed offer: "my input pays for exactly this output to me". Ordinals and other marketplaces use it, so a buyer can add their own inputs and outputs to complete the trade.

### 3. Why does a segwit signature commit to the amount, and what did that fix?

A legacy signature does not include the value of the coin being spent. The value lives in the previous transaction. To know the fee for sure, an offline signer, such as a hardware wallet, had to receive and hash the full previous transaction for every input. That is slow and heavy for small devices.

If a signer skipped that step, an attacker on the computer could lie about the input amounts. The device would then sign a transaction whose real fee was much larger than it showed, and the extra would go to miners.

BIP143 puts the amount into the sighash. If the amount the signer was told is wrong, the signature is invalid. BIP143 also fixed **quadratic hashing**: in legacy signing, each input re-hashes nearly the whole transaction, so the work grows with inputs squared. BIP143 hashes the shared parts once.

One gap remained. A segwit v0 signature commits only to its own input's amount, so a 2020 attack used two signing sessions to trick wallets. Many hardware wallets went back to asking for full previous transactions. Taproot (BIP341) closes this by committing to the amounts and scriptPubKeys of all inputs.

### 4. What happens if the same nonce signs two messages with the same key?

The private key leaks. Anyone can calculate it from the two signatures.

In ECDSA, a signature is `(r, s)` where `r` comes from the nonce point `k·G` and `s = k⁻¹(z + r·d) mod n`. Here `z` is the message hash and `d` is the private key. If two signatures use the same `k`, they share the same `r`. Then:

- `k = (z1 − z2) / (s1 − s2)`
- `d = (s1·k − z1) / r`

All of these values are public or easy to compute. The same problem exists for Schnorr, where `s = k + e·d`: two equations, two unknowns, solved.

This has happened in real life: the Sony PlayStation 3 signing key, and Android Bitcoin wallets in 2013 that used a broken random number generator. Even nonces that are only slightly biased or related can leak the key with enough signatures.

That is why Bitcoin Core uses deterministic nonces (RFC 6979) for ECDSA: the nonce is derived from the key and the message. BIP340 nonces for Schnorr are derived in a similar way, with optional extra randomness.

### 5. Where does the signature live in a legacy input versus a segwit input?

**Legacy (P2PKH, P2SH):** the signature is in the input's **scriptSig**, usually followed by the public key (P2PKH) or by other data and the redeem script (P2SH). The scriptSig is part of the data hashed for the txid. That is why a third party could change how a signature is encoded and change the txid (malleability).

**Native segwit (P2WPKH, P2WSH, P2TR):** the scriptSig is **empty**. The signature and other spending data go in the input's **witness**, which is serialized after the outputs and before the locktime, after a marker and flag (`00 01`). The witness is not part of the txid, only of the wtxid. Witness bytes count as 1 weight unit instead of 4, so they are cheaper.

**Nested segwit (P2SH-P2WPKH):** the scriptSig holds only a push of the witness program, and the signature is still in the witness.

You can see this in lab steps 1 and 4: the segwit input has `txinwitness` and an empty scriptSig, and the legacy input has everything in `scriptSig`.

### 6. How can a hardware wallet sign without showing the private key to your computer?

The private key is created on the device and never leaves it. The computer is only used to build the transaction and talk to the network.

1. The computer's wallet software (which knows only xpubs) builds an unsigned transaction, usually as a PSBT. It adds the data the device needs: the UTXOs being spent (amounts and scripts), and the derivation paths of the device's keys.
2. The PSBT goes to the device over USB, Bluetooth, QR code or an SD card.
3. The device checks it. It works out the fee from the input amounts and uses the derivation paths to recognise its own change outputs. It shows the destination addresses and amounts **on its own screen**.
4. The user confirms with a button on the device.
5. The device computes the sighash, signs inside its secure chip, and sends back only the signatures.

The computer could be full of malware and still not get the key. The thing to trust is the device screen: always check the address and amount there, not on the computer.

## Core exercises

### 1. Transaction exercises

We do not publish answers to the Decoding Bitcoin exercises. The GitHub Classroom repository comes with tests, and passing tests is the goal. If you are stuck, the most common problems are:

- Byte order. Txids are shown big-endian but stored little-endian in the raw transaction. Amounts, version and locktime are little-endian.
- CompactSize integers. `fd` means "the next 2 bytes are the length", `fe` means 4 bytes, `ff` means 8 bytes.
- Forgetting the segwit marker and flag (`00 01`) when parsing, or including them when computing the txid.

### 2. Pair review

There is no single answer. A good review comment is specific, kind and actionable. For example: "This parses the varint only when it is less than 0xfd. A transaction with 253 inputs would break. Can you handle `fd`, `fe` and `ff` too?" A comment like "looks good" does not help your partner learn.

### 3. Non-ALL sighash in the wild

The answer depends on the transaction you find. A correct answer has:

- A txid and input index where the signature does not end in `01` (or, for taproot, a 65-byte signature whose last byte is not `01`, or a 64-byte one, which means DEFAULT and behaves like ALL).
- The right flag from the table in the exercise.
- A correct explanation. For example, for `83` (SINGLE|ANYONECANPAY): "The seller signed only their own input and the output that pays them. The buyer could then add inputs to pay and an output to receive the item, without needing the seller to sign again."

## Lab answers

**Step 0.** Coinbase outputs can only be spent after 100 more blocks (coinbase maturity). After 101 blocks, only the first block's 50 BTC reward is mature, so the balance is 50 BTC. Regtest pays 50 BTC per block, halving every 150 blocks.

**Step 1.**

- Before signing, `scriptSig` is empty (`"asm": "", "hex": ""`) and there is no `txinwitness` field.
- After signing, `txinwitness` has 2 items: a DER-encoded ECDSA signature (usually 71 or 72 bytes, shown as about 142 hex characters) and a 33-byte compressed public key starting with `02` or `03`. The signature ends with `01`, which is SIGHASH_ALL.
- The `txid` is the **same** before and after signing, because the witness is not part of the txid. The `hash` (wtxid) changes, because it includes the witness.

**Step 2.** The two results are identical. Bitcoin Core makes the nonce from the private key and the sighash (RFC 6979), so the same key and the same message always give the same signature. This is safe because a different message gives a different nonce. It removes the risk of a bad random number generator reusing a nonce.

**Step 3.** The last bytes are `01`, `02` and `83`. The whole signature is different because the sighash flag changes which parts of the transaction go into the message that is signed, and the flag byte itself is part of that message. Different message, different nonce, different signature.

With `NONE`, the outputs are not signed. Anyone who sees the transaction before it confirms can replace the outputs and send the coin to themselves. The signature stays valid. (Stretch task 1 proves it.)

**Step 4.** Regtest legacy (P2PKH) addresses start with `m` or `n`. The signature and public key are in `scriptSig` (asm like `3044...[ALL] 02ab...`), and there is no `txinwitness`. The txid **changes** after signing, because the scriptSig is part of the txid.

In `getrawtransaction`, the legacy spend has `size == vsize` and `weight == 4 × size` (no witness). For one input and one P2WPKH output it is about 188 vbytes. The segwit spend is about 110 vbytes, because about 107 bytes of signature and public key are in the witness and count only one quarter. Small differences of 1 byte are normal: signature length varies.

**Step 5.** The PSBT input has `witness_utxo` (amount and scriptPubKey of the coin), usually also `non_witness_utxo` (the full previous transaction), and `bip32_derivs` (which key, by fingerprint and path, can sign). The signer needs the amount because the BIP143 sighash commits to it, and to show the user the real fee. Before signing, `analyzepsbt` says the next role is `signer`.

After `walletprocesspsbt` with `finalize=false`, the input has a `partial_signatures` entry (pubkey → signature) and `analyzepsbt` says `finalizer`. `finalizepsbt` turns the partial signature into the final witness, then extracts the network transaction. Roles: `walletcreatefundedpsbt` was **Creator** and **Updater**, `walletprocesspsbt` was **Signer**, `finalizepsbt` was **Finalizer** and **Extractor**.

**Step 6.** After Alice processes the PSBT, her input is final (`is_final: true`, because `walletprocesspsbt` finalizes by default) and Bob's still needs a signer (`next: updater` or `signer`, as Alice's wallet knows nothing about Bob's coin). After `combinepsbt`, both inputs are final.

The fee is `1 + 1 − 1.9999 = 0.0001 BTC = 10,000 sats`. That is about 56 sat/vB for this roughly 178 vbyte transaction (two P2WPKH inputs, one output). High, but fine on regtest.

Bob cannot change the output. Alice used SIGHASH_ALL, which commits to every input and every output. Any change invalidates her signature, and Bob cannot make a new one without her key.

## Stretch answers

1. The `NONE` transaction with a swapped output is accepted by `sendrawtransaction`: the outputs were never signed. The `ALL` transaction with a swapped output is rejected with a script verification error (the exact message depends on the version, often `mandatory-script-verify-flag-failed`).
2. The emulator shows each output address and amount (and the fee) and waits for a button press. Change to its own keys is usually hidden or marked, because it recognises the derivation path in the PSBT.
3. In `SignatureHash`, the `sigversion == SigVersion::WITNESS_V0` branch implements BIP143. `hashPrevouts`, `hashSequence` and `hashOutputs` are computed once in `PrecomputedTransactionData` and reused for every input. This makes signature hashing linear in the size of the transaction instead of quadratic.

## Bonus questions

These are assessment questions from the earlier version of this course.

### PSBT roles: why are they separated?

BIP174 defines six roles:

- **Creator:** makes the unsigned transaction (inputs and outputs).
- **Updater:** adds the data signers need: UTXOs, redeem or witness scripts, derivation paths.
- **Signer:** checks the transaction and adds partial signatures for the keys it holds.
- **Combiner:** merges several PSBTs for the same transaction into one.
- **Finalizer:** turns the partial signatures into the final scriptSig or witness.
- **Extractor:** pulls out the complete network transaction for broadcast.

They are separate because, in practice, they run on different machines owned by different people. A watch-only coordinator can create and update. Several hardware wallets, in different places, sign in parallel. Anyone can combine and finalize. Each piece of software only needs to do one job. Signers never need to talk to each other or to the network. One wallet can do all six jobs, as you saw in lab step 5.

### How do PSBTs improve security for hardware wallets and air-gapped signing?

Before PSBTs, every wallet and every device had its own format for "please sign this". PSBT gives them one standard format, so a device can work with any coordinator software.

A PSBT carries everything an offline signer needs to make a **safe** decision without trusting the online computer:

- The UTXO data, so the signer knows the input amounts and can compute the real fee. For segwit, the amount is also committed in the signature.
- Derivation paths, so it can confirm that change outputs really go back to its own keys.
- Scripts, so it knows exactly what it is signing for.

The file can move by QR code or SD card, so the signing device never touches a network. The private keys stay offline. The online machine only sees PSBTs and signatures, which are useless to an attacker on their own.
