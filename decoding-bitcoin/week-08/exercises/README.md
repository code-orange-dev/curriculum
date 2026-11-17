# Week 8 exercises

[Week 8 overview](../README.md) · [Solutions](../solutions/README.md) · [Syllabus](../../README.md)

This is project week. Work in pairs or small groups of three. You will build a small Bitcoin Script interpreter (a "stack machine"), test it, and demo it on Monday. The lesson for the week is [Project: Build your own bitcoin Stack](https://bitcoindevs.xyz/decoding/project) on Decoding Bitcoin. Read it first, then use this page as a plan.

Any language is fine. Python, JavaScript, Rust, Go and C++ all work well. Keep it small: a clear 200-line interpreter with good tests beats a big one that nobody can read.

---

## Exercise 1: Build the stack project

Build the project from the [Stack project](https://bitcoindevs.xyz/decoding/project) lesson. Push your code to a public GitHub repository and share the link on Discord before Monday.

### Suggested milestone plan

Treat each milestone as one small pull request (or one commit) with its own tests. If you only reach milestone 5, that is still a good demo.

| # | Milestone | Done when |
|---|---|---|
| 1 | **Stack and pushes.** A stack type, `OP_0`, `OP_1` to `OP_16`, `OP_1NEGATE`, and pushing raw bytes. | `OP_2 OP_3` leaves two items on the stack. |
| 2 | **Stack operations.** `OP_DUP`, `OP_DROP`, `OP_SWAP` (add `OP_OVER`, `OP_ROT` if you like). | Popping from an empty stack gives a clear error, not a crash. |
| 3 | **Numbers and maths.** Decode stack items as Script numbers (little-endian, sign bit in the top byte). `OP_ADD`, `OP_SUB`, `OP_NOT`. | `OP_3 OP_5 OP_SUB` gives -1, stored as the byte `0x81`. |
| 4 | **Comparison and failure.** `OP_EQUAL`, `OP_EQUALVERIFY`, `OP_VERIFY`, `OP_RETURN`. A script result is PASS or FAIL with a reason. | A failing `OP_VERIFY` stops the script at once. |
| 5 | **Final result rule.** After the last opcode, PASS only if the stack is not empty and the top item is true. | `OP_1 OP_VERIFY` fails (empty stack at the end). |
| 6 | **Hashing and P2PKH.** `OP_SHA256`, `OP_HASH160`, and an `OP_CHECKSIG` stub (see below). | The P2PKH test cases below pass and fail as expected. |
| 7 | **Conditionals.** `OP_IF`, `OP_NOTIF`, `OP_ELSE`, `OP_ENDIF`, including nesting. | Unbalanced `OP_IF` fails. Opcodes in a skipped branch do not run. |

**About `OP_CHECKSIG`:** real signature checking needs the transaction and elliptic curve code. For this project a stub is fine: for example, "the signature is valid if it equals the bytes `valid-sig`". Make the stub a function you can swap out later.

**Write down** in your repository README:

- How you represent a stack item (bytes? integers? both?) and why.
- Which opcodes you support.
- How to run your tests with one command.

### Test cases

Write these as automated tests. The notation is the same as Bitcoin Core's `asm` output, with `<hex>` meaning "push these bytes". PASS means the script ends with a non-empty stack and a true top item.

| # | Script | Expected | What it checks |
|---|---|---|---|
| 1 | `OP_1 OP_2 OP_ADD OP_3 OP_EQUAL` | PASS | Basic maths and equality |
| 2 | `OP_2 OP_3 OP_ADD OP_6 OP_EQUAL` | FAIL (top is false) | A false result is a failure |
| 3 | `OP_1 OP_VERIFY` | FAIL (empty stack) | `OP_VERIFY` consumes its item |
| 4 | `OP_0` | FAIL (top is false) | `OP_0` pushes an empty byte array |
| 5 | `<80>` | FAIL (top is false) | Negative zero is false |
| 6 | `<0000>` | FAIL (top is false) | Any all-zero bytes are false |
| 7 | `OP_1NEGATE OP_1 OP_ADD OP_NOT` | PASS | Negative numbers, `OP_NOT` |
| 8 | `OP_ADD` | FAIL (stack underflow) | Not enough items |
| 9 | `OP_1 OP_RETURN` | FAIL (`OP_RETURN`) | `OP_RETURN` always fails |
| 10 | `OP_5 OP_3 OP_SUB OP_2 OP_EQUAL` | PASS | Operand order: 5 - 3, not 3 - 5 |
| 11 | `OP_3 OP_5 OP_SUB OP_1NEGATE OP_1NEGATE OP_ADD OP_EQUAL` | PASS | -2 is encoded as `0x82` |
| 12 | `OP_1NEGATE <81> OP_EQUAL` | PASS | -1 and the byte `0x81` are the same thing |
| 13 | `OP_16 <10> OP_EQUAL` | PASS | `OP_16` pushes the byte `0x10` |
| 14 | `<616263> OP_SHA256 <ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad> OP_EQUAL` | PASS | SHA256 of "abc" |
| 15 | `OP_1 OP_IF OP_2 OP_ELSE OP_3 OP_ENDIF OP_2 OP_EQUAL` | PASS | IF branch taken |
| 16 | `OP_0 OP_IF OP_2 OP_ELSE OP_3 OP_ENDIF OP_3 OP_EQUAL` | PASS | ELSE branch taken |
| 17 | `OP_0 OP_IF OP_RETURN OP_ENDIF OP_1` | PASS | A skipped `OP_RETURN` does nothing |
| 18 | `OP_1 OP_IF OP_2` | FAIL (unbalanced `OP_IF`) | Every `OP_IF` needs an `OP_ENDIF` |
| 19 | `OP_2 OP_SWAP` | FAIL (stack underflow) | `OP_SWAP` needs two items |

**P2PKH test cases.** These use a dummy key: the public key for private key `1`, which is the generator point G. Everyone knows this private key, so never send real coins to it.

- `SIG` = `<76616c69642d736967>` (the ASCII bytes `valid-sig`, accepted by the stub)
- `PUB` = `<0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798>`
- HASH160 of `PUB` = `751e76e8199196d454941c45d1b3a323f1433bd6`

| # | Script (scriptSig then scriptPubKey) | Expected |
|---|---|---|
| 20 | `SIG PUB OP_DUP OP_HASH160 <751e76e8199196d454941c45d1b3a323f1433bd6> OP_EQUALVERIFY OP_CHECKSIG` | PASS |
| 21 | Same, but the hash is `<0000000000000000000000000000000000000000>` | FAIL at `OP_EQUALVERIFY` |
| 22 | Same as 20, but `SIG` is replaced by `<00>` | FAIL (top is false after `OP_CHECKSIG`) |

More test vectors: Bitcoin Core keeps hundreds of script tests in [`script_tests.json`](https://github.com/bitcoin/bitcoin/blob/master/src/test/data/script_tests.json). Pick five that use only opcodes you support and add them to your suite.

---

## Exercise 2: Trace a P2PKH script through your stack

Use test case 20 above. Add a "trace" or "debug" mode to your interpreter that prints the stack after every opcode. Run test 20 and paste the output into your repository README.

**Write down:**

1. The stack after each of the 7 steps (2 pushes from the scriptSig, 5 opcodes from the scriptPubKey).
2. The step where the script would fail if someone used the wrong public key.
3. The step where it would fail if the signature was wrong.

Tip: print the top of the stack on the right, and shorten long items, for example `0279be66..`.

---

## Exercise 3: Review another group's project

Pick a group that is not yours (the Facilitator can pair groups on Discord). Read their code and leave one helpful comment, for example as a GitHub issue or a review comment.

A helpful comment is specific and kind. Some ideas:

- A test case from the table above that their code gets wrong.
- A place where an error is swallowed or the program could crash.
- A naming or structure change that would make the code easier to read.

**Write down:** the link to your comment, and one idea you want to copy from their code.

---

## Hands-on lab (bitcoin-cli, regtest)

These labs use Bitcoin Core as the "reference answer" for your interpreter. You need Bitcoin Core 28 or newer, and `jq` for reading JSON. If you have not set up regtest yet, see [Week 1: Bitcoin Core CLI](../../week-01/exercises/bitcoin_core_cli.md).

### Setup

```bash
# -txindex=1 lets getrawtransaction find confirmed transactions
bitcoind -regtest -daemon -txindex=1

# Create a wallet (or load it if you made it in an earlier week)
bitcoin-cli -regtest -named createwallet wallet_name=lab || bitcoin-cli -regtest loadwallet lab

# Mine 101 blocks so the first coinbase (50 BTC on regtest) is spendable
bitcoin-cli -regtest -rpcwallet=lab -generate 101
bitcoin-cli -regtest -rpcwallet=lab getbalance
```

If your node is already running without `-txindex`, stop it with `bitcoin-cli -regtest stop` and start it again with the command above.

### Lab 1: Check your parser with `decodescript`

`decodescript` takes raw script hex and shows the opcodes. Use it to check that your interpreter reads bytes the same way Bitcoin Core does.

**1.1** A simple maths script:

```bash
bitcoin-cli -regtest decodescript 5152935387
```

**Question:** Which opcode is each byte? (`0x51`, `0x52`, `0x93`, `0x53`, `0x87`.) What does the `asm` field show for `OP_1`, and why might that confuse a parser that reads `asm`?

**1.2** A P2PKH scriptPubKey for the dummy key from the test cases:

```bash
bitcoin-cli -regtest decodescript 76a914751e76e8199196d454941c45d1b3a323f1433bd688ac
```

**Question:** What is the `type`? What does the byte `0x14` mean, and why is it not an opcode name in the `asm`?

**1.3** A conditional script:

```bash
bitcoin-cli -regtest decodescript 5163526753685287
```

**Question:** Write out the `asm`. Run the same script in your interpreter. Does it PASS?

**1.4** An `OP_RETURN` output:

```bash
bitcoin-cli -regtest decodescript 6a0b68656c6c6f20776f726c64
```

**Question:** What is the `type`? Decode the data bytes as ASCII. Why can an output with this script never be spent?

### Lab 2: A real timelock with `OP_NOTIF` (old Week 3, exercise 3)

You will lock coins to a script with two ways to spend: key A at any time, or key B after 5 blocks. You will write the policy as a [miniscript](https://bitcoinops.org/en/topics/miniscript/) descriptor and let Bitcoin Core compile it to Script. Then you will spend with key B, which forces the timelock branch.

**2.1** Get two keys. Key A is a public key only. The new wallet will not have its private key. Key B comes from the `lab` wallet's master private key.

```bash
APUB=$(bitcoin-cli -regtest -rpcwallet=lab getaddressinfo "$(bitcoin-cli -regtest -rpcwallet=lab getnewaddress)" | jq -r .pubkey)
XPRV=$(bitcoin-cli -regtest -rpcwallet=lab listdescriptors true | jq -r '.descriptors[].desc' | grep -o 'tprv[[:alnum:]]*' | head -1)
echo "$APUB"
```

**2.2** Build the descriptor, add its checksum, and derive the address:

```bash
DESC="wsh(or_d(pk($APUB),and_v(v:pk($XPRV/1002/0),older(5))))"
DESC="$DESC#$(bitcoin-cli -regtest getdescriptorinfo "$DESC" | jq -r .checksum)"
ADDR=$(bitcoin-cli -regtest deriveaddresses "$DESC" | jq -r '.[0]')
echo "$ADDR"
```

**Question:** What kind of address is this (look at the prefix and length)? `older(5)` becomes which opcode?

**2.3** Make a blank wallet that only knows this descriptor, then fund the address:

```bash
bitcoin-cli -regtest -named createwallet wallet_name=csv blank=true
bitcoin-cli -regtest -rpcwallet=csv importdescriptors "[{\"desc\":\"$DESC\",\"timestamp\":\"now\"}]"

TXID=$(bitcoin-cli -regtest -rpcwallet=lab sendtoaddress "$ADDR" 1)
bitcoin-cli -regtest -rpcwallet=lab -generate 1
VOUT=$(bitcoin-cli -regtest getrawtransaction "$TXID" true | jq ".vout[] | select(.scriptPubKey.address==\"$ADDR\") | .n")
bitcoin-cli -regtest -rpcwallet=csv listunspent
```

**2.4** Build a spend with `sequence` set to 5 (a relative timelock of 5 blocks), sign it with the `csv` wallet, and try to broadcast it straight away:

```bash
DEST=$(bitcoin-cli -regtest -rpcwallet=lab getnewaddress)
PSBT=$(bitcoin-cli -regtest -named createpsbt \
  inputs="[{\"txid\":\"$TXID\",\"vout\":$VOUT,\"sequence\":5}]" \
  outputs="[{\"$DEST\":0.9999}]")
SIGNED=$(bitcoin-cli -regtest -rpcwallet=csv walletprocesspsbt "$PSBT" | jq -r .psbt)
HEX=$(bitcoin-cli -regtest finalizepsbt "$SIGNED" | jq -r .hex)
bitcoin-cli -regtest sendrawtransaction "$HEX"
```

**Question:** What error do you get? Which rule (and which BIP) causes it?

**2.5** Mine 5 more blocks and try again:

```bash
bitcoin-cli -regtest -rpcwallet=lab -generate 5
SPEND=$(bitcoin-cli -regtest sendrawtransaction "$HEX")
bitcoin-cli -regtest getrawtransaction "$SPEND" true | jq '.vin[0].txinwitness'
```

**Question:** The witness has three items. What is each one? Why is the middle one empty?

**2.6** Decode the last witness item (the witness script):

```bash
WS=$(bitcoin-cli -regtest getrawtransaction "$SPEND" true | jq -r '.vin[0].txinwitness[2]')
bitcoin-cli -regtest decodescript "$WS"
```

**Question:** Write out the `asm`. Trace it by hand (or in your interpreter, with a stub for `OP_CHECKSIG`, `OP_CHECKSIGVERIFY` and `OP_CHECKSEQUENCEVERIFY`), starting from the stack `[sigB, <empty>]`. What is left on the stack at the end?

---

## Stretch goals

Pick any of these once the core milestones work.

1. **Nested conditionals.** Support `OP_IF` inside `OP_IF`. Test: `OP_1 OP_0 OP_IF OP_0 OP_ELSE OP_1 OP_IF OP_1 OP_ENDIF OP_ENDIF`. What should this leave on the stack?
2. **`OP_CHECKMULTISIG` with the off-by-one bug.** Implement it the way Bitcoin does: pop N, N keys, M, M signatures, then **one extra item**. Under BIP147 (NULLDUMMY) the extra item must be an empty byte array. Tests:
   - `OP_0 SIG_A SIG_B OP_2 PK_A PK_B PK_C OP_3 OP_CHECKMULTISIG` should PASS (with a stub that accepts any matching sig).
   - The same script without the leading `OP_0` should FAIL (stack underflow).
   - The same script with `OP_1` instead of `OP_0` should FAIL (dummy not empty).
3. **Timelocks.** Add a small "transaction context" (locktime, input sequence, tx version) and implement `OP_CHECKLOCKTIMEVERIFY` (BIP65) and `OP_CHECKSEQUENCEVERIFY` (BIP112). Note that both leave their argument on the stack, which is why you usually see them followed by `OP_DROP`. Test with the witness script from Lab 2.
4. **Limits.** Enforce the legacy limits: 520 bytes per pushed item, 1,000 items on the stack and altstack together, 201 non-push opcodes, 10,000 bytes of script, 4-byte number operands. Write one failing test for each.
5. **Read raw hex, not `asm`.** Parse script bytes directly, including `OP_PUSHDATA1`, `OP_PUSHDATA2` and `OP_PUSHDATA4`. Check your parser against `decodescript` from Lab 1.
6. **Disabled opcodes.** `OP_CAT`, `OP_MUL` and others are disabled. In Bitcoin they make a script fail even inside a branch that is not executed. Add a test for that.

---

## Demo checklist (Monday)

Each group gets about 5 minutes. Before the session, check that you can:

- [ ] Show the repository link (already posted on Discord).
- [ ] Run the full test suite with one command, live.
- [ ] Show the P2PKH trace from Exercise 2, step by step.
- [ ] Show one failing script and the error your code gives.
- [ ] Name the hardest opcode and say why in one sentence.
- [ ] Say one thing you would change if you started again.
- [ ] Keep it to 5 minutes. Practise once with a timer.
