# Week 5 notes

Notes for [week 5: Signing and the transaction exercises](../README.md). For the full course plan, see the [syllabus](../../README.md).

## Key ideas

- **A signature signs a message, not "the transaction".** The message is the sighash: a 32-byte hash built from a modified copy of the spending transaction. The signature cannot be inside the data it signs, so signatures are left out when the sighash is computed.
- **Three sighash algorithms exist.** Legacy inputs use the original algorithm. Segwit v0 inputs use BIP143, which adds the spent amount and avoids quadratic hashing. Taproot inputs use BIP341, which commits to the amounts and scriptPubKeys of all inputs and uses tagged hashes.
- **The sighash flag chooses what is fixed.** ALL fixes every input and output. NONE leaves the outputs open. SINGLE fixes only the output at the same index. ANYONECANPAY fixes only the signer's own input, so others can add inputs. The flag is the last byte of the signature (taproot may leave it out, which means DEFAULT).
- **Where the signature lives depends on the output type.** Legacy inputs carry it in the scriptSig, which is part of the txid. Segwit and taproot inputs carry it in the witness, which is not part of the txid and is discounted in weight.
- **The nonce is as secret as the key.** Reusing an ECDSA or Schnorr nonce with the same key reveals the private key. Bitcoin Core makes nonces deterministically (RFC 6979 for ECDSA), so signing the same message twice gives the same signature.
- **Signing can happen away from the network.** A PSBT (BIP174) carries an unsigned transaction plus the UTXOs, scripts and key paths a signer needs. A hardware wallet checks the amounts, shows the outputs on its own screen and returns only signatures.

## Common mix-ups

| Mix-up | Correction |
|---|---|
| "The signature signs the whole raw transaction." | It signs the sighash, a hash of a modified copy. Which parts are included depends on the input type and the sighash flag. |
| "Signing a segwit transaction changes its txid." | No. The witness is not part of the txid. Signing changes the wtxid. Signing a legacy transaction does change the txid. |
| "SIGHASH_NONE means the signature commits to nothing." | It still commits to all inputs (unless combined with ANYONECANPAY). It leaves only the outputs open. |
| "Deterministic nonces are less secure than random ones." | They are safer in practice. A deterministic nonce is different for every message and does not depend on a good random number generator. |
| "A PSBT is a special kind of transaction on chain." | A PSBT is a file format for passing a transaction between wallets before it is complete. The chain only ever sees the final extracted transaction. |
| "The hardware wallet trusts what the computer shows." | The device checks amounts and change paths itself and shows the outputs on its own screen. The user should confirm there, not on the computer. |

## Session plan

| Time | Block | Who | Notes |
|---|---|---|---|
| 0:00 to 0:05 | Welcome and roles | Facilitator | Confirm Summariser, Devil's advocate, Exercise driver. |
| 0:05 to 0:15 | Opening question | Facilitator, everyone | "What exactly does a signature prove?" One minute of silent thinking first. |
| 0:15 to 0:25 | Concept recap | Facilitator | Slides: sighash, flags, amount commitment, signature location, nonce, PSBT. Keep it short. |
| 0:25 to 1:05 | Question round | Question owners | About 6 minutes per question. Owner explains, one follow-up, Devil's advocate pushes back. |
| 1:05 to 1:20 | Exercise walkthrough | Exercise driver | Lab steps 1 to 3: sign, compare txids, try other sighash flags. |
| 1:20 to 1:27 | Wrap-up and next week | Facilitator, Summariser | Summariser reads back 3 takeaways. Assign week 6 questions and roles. |
| 1:27 to 1:30 | Buffer and close | Facilitator | Use for overrun or open questions. |

## Facilitator tips

Before the session:

- Run lab steps 0 to 3 yourself on a fresh regtest node so you can help with errors.
- Check that people have accepted the GitHub Classroom assignment. Some need help with git or with the test runner.
- Make sure the Exercise driver has `jq` installed and a running regtest node.

Where people get stuck:

- **"Fee estimation failed. Fallbackfee is disabled."** Regtest has no fee history. Start `bitcoind` with `-fallbackfee=0.0001` or pass `fee_rate` to the command.
- **Wallet already exists.** If they used regtest in earlier weeks, use `loadwallet` instead of `createwallet`, or pick new wallet names.
- **Multiple wallets loaded.** Every wallet command needs `-rpcwallet=<name>`, including `-generate`.
- **Confusing txid and wtxid.** Have them print both (`.txid` and `.hash` in `decoderawtransaction`) before and after signing.
- **The nonce math.** Do not let the question round turn into an algebra lesson. The key point is "same nonce twice leaks the key".
- **Sighash in taproot.** Some people will find 64-byte signatures with no flag byte. That is SIGHASH_DEFAULT, which behaves like ALL.

## Glossary

- **Sighash (signature hash):** the 32-byte message that a private key signs for one input.
- **Sighash flag / sighash type:** the byte that says which inputs and outputs the signature covers.
- **SIGHASH_ALL, NONE, SINGLE:** cover all outputs, no outputs, or only the output at the same index.
- **ANYONECANPAY:** modifier (0x80) that covers only the signer's own input.
- **SIGHASH_DEFAULT:** taproot only. No flag byte is added, and it covers the same data as ALL.
- **scriptCode:** the script placed into the sighash for the input being signed, usually the previous output's script.
- **DER:** the encoding used for ECDSA signatures in Bitcoin (strict DER is required since BIP66).
- **Nonce (k):** a one-time secret number used to make each signature.
- **RFC 6979:** a standard for making ECDSA nonces deterministically from the key and the message.
- **Witness:** the per-input data (signatures, keys, scripts) stored outside the txid in segwit transactions.
- **PSBT:** Partially Signed Bitcoin Transaction (BIP174). A format for passing an incomplete transaction between wallets and signers.
- **Quadratic hashing:** the legacy problem where each input re-hashes most of the transaction, so the total work grows with the square of the number of inputs.

## Further resources

- [BIP 143: Transaction signature verification for version 0 witness program](https://github.com/bitcoin/bips/blob/master/bip-0143.mediawiki)
- [BIP 341: Taproot](https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki) (see the "Signature validation rules" section for the taproot sighash)
- [BIP 340: Schnorr signatures](https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki) (see the nonce generation section)
- [BIP 174: PSBT](https://github.com/bitcoin/bips/blob/master/bip-0174.mediawiki)
- [Bitcoin Optech: PSBTs](https://bitcoinops.org/en/topics/psbt/)
- [Bitcoin Optech: Segregated Witness](https://bitcoinops.org/en/topics/segregated-witness/)
- [Bitcoin Core RPC reference](https://developer.bitcoin.org/reference/rpc/) (`signrawtransactionwithwallet`, `walletprocesspsbt`, `combinepsbt`, `finalizepsbt`)
- [Mastering Bitcoin](https://github.com/bitcoinbook/bitcoinbook), the chapter on digital signatures
- [Programming Bitcoin](https://github.com/jimmysong/programmingbitcoin), chapter 3 (elliptic curve cryptography and signing)
- [HWI: Hardware Wallet Interface](https://github.com/bitcoin-core/HWI)
