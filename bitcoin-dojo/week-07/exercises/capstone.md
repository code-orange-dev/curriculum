# Week 7 Capstone: Verify Your Own Transaction

Everything you built in six weeks, pointed at a transaction **you** made.

## 1. Make a transaction

On **signet**, with any wallet (Sparrow, Bitcoin Core, BlueWallet...): receive some coins from a signet faucet, then send some to a second address you control. Use a native segwit (P2WPKH, `tb1q...`) wallet, since your Week 6 code handles that.

Get the raw hex, the txid, and each input's previous output (script and amount). For example, from `https://mempool.space/signet/api/tx/<txid>/hex` and `https://mempool.space/signet/api/tx/<txid>`.

## 2. Verify it with your own code

Write `verify_my_tx.py` that, using only your Week 3-6 code:

1. parses the transaction (Week 6 `parse_segwit`)
2. checks your computed txid matches the explorer's
3. computes the weight and vsize, and the fee rate in sat/vB
4. for **every input**, computes the BIP143 sighash and verifies the signature in its witness (Week 5 `verify`)
5. prints the P2WPKH address of each input's public key (Week 3) and checks it matches the explorer

If every signature verifies, you have independently validated a real Bitcoin transaction with code you wrote. That's what a full node does, billions of times over.

## 3. Present it (graduation call, 5 minutes)

- Your transaction, and what each part of the hex means
- One concept from the course that changed how you understand Bitcoin
- Your vibe-coded explainer website
- Your next step (below)

## 4. Next step: pick one

- **Keep building on these exact skills:** the [Privacy Track](../../../privacy-track/) Silent Payments lab uses the same curve math, tagged hashes and taproot keys. It's graded against the official BIP352 test vectors.
- **Go deeper on transactions:** [rawBit](../../../rawbit/) or [Decoding Bitcoin](../../../decoding-bitcoin/)
- **Contribute:** find a current beginner issue with the Privacy Track's [live searches](../../../privacy-track/ISSUE_POOL.md) and run the [PR checklist](../../../privacy-track/PR_CHECKLIST.md) before submitting
