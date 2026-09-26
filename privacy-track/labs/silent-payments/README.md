# Silent Payments Lab (BIP352)

Build a working Silent Payments sender and scanner in plain Python, then check it against the **official BIP352 test vectors**: the same 28 cases Bitcoin Core, libsecp256k1, rust-silentpayments, BDK and every SP wallet test against. When your code passes all of them, it's compatible with real wallets.

No dependencies. Python 3.8+. Works offline.

```bash
cd privacy-track/labs/silent-payments
python3 run_vectors.py send        # Session 1: grade send.py
python3 run_vectors.py receive     # Session 2: grade receive.py
python3 scan_benchmark.py          # Session 2: why do indexers exist?
```

## What's in here

| File | You... | What it is |
|---|---|---|
| `send.py` | **edit** | Session 1: 5 exercises, from address decoding to output creation |
| `receive.py` | **edit** | Session 2: 3 core exercises + 2 stretch (labels, spending) |
| `run_vectors.py` | run | Grades your code case by case and points at the exercise that's wrong |
| `scan_benchmark.py` | run | Times your scanner and scales it up to a day of mainnet |
| `secp.py`, `bech32m.py` | read | Tiny secp256k1 and bech32m, just enough for the lab |
| `txin.py` | read | Which inputs count, and how their keys are pulled from scripts. Worth reading: it's where real implementations disagree (see the malleated-P2PKH vector and [bitcoin/bitcoin#36338](https://github.com/bitcoin/bitcoin/pull/36338)) |
| `solutions/` | peek later | Reference solutions. `--solution` runs them through the grader |
| `vectors/` | - | `send_and_receive_test_vectors.json` from [bitcoin/bips](https://github.com/bitcoin/bips/tree/master/bip-0352) (BSD-2-Clause) |

## Progress looks like this

```
  ✓   1 Simple send: two inputs
  ✓   7 Single recipient: taproot only inputs with even y-values
  ✗   8 Single recipient: taproot only with mixed even/odd y-values
        Exercise 2: a_sum is wrong (did you negate odd-y taproot keys?)
  ·  13 Receiving with labels: label with even parity
        not implemented yet: generate_label()

21/28 vectors passing
```

Add `-v` to see got/expected values when a case fails.

## The bugs everyone hits (read after you're stuck, not before)

1. **Serializing the shared secret as x-only.** `t_k` hashes the **33-byte compressed** point. Using 32 bytes passes zero vectors.
2. **Forgetting taproot negation.** An x-only key means the even-y point. If your taproot private key gives odd y, negate it.
3. **Comparing outputs by position.** The receiver must check `P_k` against **every** output. Senders shuffle outputs, and they should.
4. **Stopping after one match.** One transaction can pay you several times (`k = 0, 1, 2...`).
5. **Sorting outpoints by (txid, vout) as numbers.** BIP352 compares the **serialized** bytes, where the txid is little-endian and vout is little-endian. Vector 5 exists to catch this.

## Safety

This is teaching code: slow and not constant-time. **Never paste real keys into it.** Use signet or regtest for anything on-chain.

## Going further

- [BIP352](https://github.com/bitcoin/bips/blob/master/bip-0352.mediawiki) and its [reference.py](https://github.com/bitcoin/bips/blob/master/bip-0352/reference.py): compare your code line by line
- [libsecp256k1 `silentpayments` module](https://github.com/bitcoin-core/secp256k1) (merged July 2026, PR #1765) and the light-client API follow-up (#1912)
- [Bitcoin Core tracking issue #28536](https://github.com/bitcoin/bitcoin/issues/28536): BIP352 core logic merged in #35301; sending (#35302) and receiving (#32966) in review
- [rust-silentpayments](https://github.com/cygnet3/rust-silentpayments), [bdk-sp](https://github.com/bitcoindevkit/bdk-sp), [BlindBit Oracle](https://github.com/setavenger/blindbit-oracle), [Frigate](https://github.com/sparrowwallet/frigate), [Dana wallet](https://github.com/cygnet3/danawallet), [Shroud](https://github.com/CypherCommons/shroud)
- [Bitcoin Optech: Silent Payments](https://bitcoinops.org/en/topics/silent-payments/): history and news
