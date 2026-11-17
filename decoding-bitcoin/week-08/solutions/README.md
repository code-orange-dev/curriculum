# Week 8 solutions

[Week 8 overview](../README.md) · [Exercises](../exercises/README.md) · [Syllabus](../../README.md)

Try the project and the questions yourself first. This is project week, so many answers depend on your own code. The answers below describe what a strong answer looks like and give the Bitcoin facts you should be able to compare against.

---

## Discussion questions

### 1. How did you represent the stack and opcodes in your code? What would you change next time?

A strong design stores every stack item as a **byte array**, because that is what Bitcoin does. Numbers are only a view of those bytes: an opcode like `OP_ADD` decodes its inputs as Script numbers, does the maths, and encodes the result back to bytes. Teams that stored Python integers or JavaScript numbers often hit bugs later, for example with `OP_EQUAL` (which compares bytes, not values) or with negative zero.

For opcodes, a lookup table (a dictionary or `match` from opcode name or byte to a handler function) is easier to extend and test than one long `if/else` chain. Conditionals are the exception: `OP_IF`, `OP_ELSE` and `OP_ENDIF` must be handled before the "am I in a skipped branch?" check, so they usually sit outside the table.

Good "next time" answers: parse raw hex instead of `asm` text, keep a separate execution-state stack for conditionals from the start, and make `OP_CHECKSIG` a pluggable function so a real signature check can replace the stub.

### 2. How does your stack treat true and false? Compare it with how Bitcoin Script does.

In Bitcoin Script a stack item is **false** if it is an empty byte array, if every byte is zero, or if it is "negative zero" (all zero bytes except the last one, which is `0x80`). **Everything else is true.** So `<00>`, `<0000>` and `<80>` are all false, while `<01>`, `<81>` (which is -1) and any 32-byte hash are true.

`OP_0` pushes an empty array, not the byte `0x00`. Comparison opcodes like `OP_EQUAL` push `0x01` for true and an empty array for false.

A common bug is to treat "false" as "equals the byte 0x00", so `OP_0` looks true, or to treat negative zero as true. Another is to use the host language's idea of truth: in Python, `b"\x00"` is truthy because it is a non-empty bytes object, but in Bitcoin Script it is false. The fix is one small `is_true(bytes)` function used by `OP_IF`, `OP_VERIFY`, `OP_NOT` and the final result check.

### 3. Which opcode was hardest to implement, and why?

There is no single right answer, but strong answers usually name one of these and explain the subtle part:

- **`OP_IF` / `OP_ELSE` / `OP_ENDIF`:** you need a stack of booleans, one per open `OP_IF`. An opcode runs only if every entry is true. Nested branches and "unbalanced `OP_IF`" errors are easy to get wrong.
- **Number encoding:** Script numbers are little-endian with a sign bit in the most significant bit of the last byte. 127 is `7f`, but 128 is `8000` (an extra byte so the sign bit stays clear), -1 is `81`, -128 is `8080`. Numeric inputs to maths opcodes are limited to 4 bytes.
- **`OP_CHECKMULTISIG`:** the order of pops, the rule that signatures must match keys in order, and the extra dummy item it pops (see Bonus question 1).
- **`OP_CHECKSIG`:** real checking needs the transaction, a sighash and ECDSA or Schnorr, which is far beyond a stack machine. Most teams used a stub, which is fine.

### 4. How does your implementation handle a script that fails halfway through?

Bitcoin stops at the **first** failure and the whole script is invalid. There is no "partial success": the spending transaction is rejected. Failure can come from a `...VERIFY` opcode finding false, `OP_RETURN`, a stack underflow, an unknown or disabled opcode, a number that is too long, an unbalanced `OP_IF`, or a limit being exceeded. Separately, a script that runs to the end can still fail the final check: the stack must be non-empty and the top item true. (For segwit and tapscript, the clean-stack rule also requires exactly one item left.)

A good implementation raises an exception or returns an error value as soon as a rule breaks, and includes the reason (for example "OP_EQUALVERIFY failed at step 6"). It never crashes on bad input like popping an empty stack. Since a script has no side effects outside its own stack, stopping early is always safe: there is nothing to undo.

### 5. What limits (stack size, script size, opcode count) did you add, and why does Bitcoin have them?

Every full node must run every script, so a script must not be able to use unbounded CPU or memory. For legacy and segwit v0 scripts the main limits are:

| Limit | Value |
|---|---|
| Size of one pushed item | 520 bytes |
| Items on stack + altstack | 1,000 |
| Non-push opcodes per script | 201 |
| Script size | 10,000 bytes |
| Number operands for maths | 4 bytes |

Script also has **no loops and no jumps backwards**, so running time is bounded by script length. Signature checks are the expensive part, so they are also limited by "sigops" counting at the block level. Tapscript (week 10) drops the 201-opcode and 10,000-byte limits and instead gives each input a signature-checking budget based on its witness size. The 520-byte and 1,000-item limits stay.

A strong answer says which of these the team added, shows one test that hits a limit, and connects the limit to denial-of-service protection.

### 6. Which test cases best convinced you that your stack is correct?

The most convincing tests are the ones that **fail for a subtle reason**, because a buggy interpreter often passes the happy path by luck. Good examples from the exercise table:

- `OP_1 OP_VERIFY` fails because the stack is empty at the end, not because anything was false.
- `<80>` and `<0000>` fail because they are false, even though they are not empty.
- `OP_5 OP_3 OP_SUB OP_2 OP_EQUAL` passes only if the operand order is right.
- `OP_0 OP_IF OP_RETURN OP_ENDIF OP_1` passes only if skipped branches really do nothing.
- The three P2PKH cases: one passes, one fails at `OP_EQUALVERIFY`, one fails at `OP_CHECKSIG`.

Even better: tests taken from Bitcoin Core's `script_tests.json`, because they come from the real implementation, and tests compared against `decodescript` output.

---

## Exercise answers

### Exercise 1: Build the stack project

There is no single correct repository. A complete answer has: the 7 milestones working, all 22 test cases from the table passing, a README that explains how to run the tests, and the trace from Exercise 2.

Expected results for the stretch test in [Stretch goals](../exercises/README.md#stretch-goals) item 1: `OP_1 OP_0 OP_IF OP_0 OP_ELSE OP_1 OP_IF OP_1 OP_ENDIF OP_ENDIF` leaves `[01, 01]`, so it PASSES (top is true).

Below is a short reference interpreter in Python, so you can compare approaches after you have written your own. It passes all 22 test cases in the exercises. It reads `asm`-style text, uses bytes for every stack item, and stubs `OP_CHECKSIG`.

<details>
<summary>Reference interpreter (Python, about 120 lines)</summary>

```python
import hashlib

class ScriptError(Exception):
    pass

def hash160(b):
    return hashlib.new("ripemd160", hashlib.sha256(b).digest()).digest()

def encode_num(n):
    if n == 0:
        return b""
    out, neg, n = bytearray(), n < 0, abs(n)
    while n:
        out.append(n & 0xFF)
        n >>= 8
    if out[-1] & 0x80:
        out.append(0x80 if neg else 0x00)
    elif neg:
        out[-1] |= 0x80
    return bytes(out)

def decode_num(b):
    if len(b) > 4:
        raise ScriptError("number too long")
    if not b:
        return 0
    n = int.from_bytes(b, "little")
    if b[-1] & 0x80:  # sign bit set
        return -(n & ~(0x80 << (8 * (len(b) - 1))))
    return n

def is_true(b):
    for i, byte in enumerate(b):
        if byte != 0:
            # negative zero (0x80 in the last byte, zeros elsewhere) is false
            return not (i == len(b) - 1 and byte == 0x80)
    return False

def run(script, stack=None, checksig=lambda sig, pub: sig == b"valid-sig"):
    stack = [] if stack is None else stack
    exec_stack = []          # one bool per open OP_IF
    def pop():
        if not stack:
            raise ScriptError("stack underflow")
        return stack.pop()
    for tok in script.split():
        executing = all(exec_stack)
        if tok in ("OP_IF", "OP_NOTIF"):
            val = False
            if executing:
                val = is_true(pop())
                if tok == "OP_NOTIF":
                    val = not val
            exec_stack.append(val)
            continue
        if tok == "OP_ELSE":
            if not exec_stack:
                raise ScriptError("OP_ELSE without OP_IF")
            exec_stack[-1] = not exec_stack[-1]
            continue
        if tok == "OP_ENDIF":
            if not exec_stack:
                raise ScriptError("OP_ENDIF without OP_IF")
            exec_stack.pop()
            continue
        if not executing:
            continue
        if tok.startswith("<") and tok.endswith(">"):
            stack.append(bytes.fromhex(tok[1:-1]))
        elif tok == "OP_0":
            stack.append(b"")
        elif tok == "OP_1NEGATE":
            stack.append(encode_num(-1))
        elif tok.startswith("OP_") and tok[3:].isdigit() and 1 <= int(tok[3:]) <= 16:
            stack.append(encode_num(int(tok[3:])))
        elif tok == "OP_DUP":
            x = pop(); stack += [x, x]
        elif tok == "OP_DROP":
            pop()
        elif tok == "OP_SWAP":
            b, a = pop(), pop(); stack += [b, a]
        elif tok in ("OP_ADD", "OP_SUB"):
            b, a = decode_num(pop()), decode_num(pop())
            stack.append(encode_num(a + b if tok == "OP_ADD" else a - b))
        elif tok == "OP_NOT":
            stack.append(encode_num(1 if decode_num(pop()) == 0 else 0))
        elif tok in ("OP_EQUAL", "OP_EQUALVERIFY"):
            ok = pop() == pop()
            if tok == "OP_EQUALVERIFY":
                if not ok:
                    raise ScriptError("OP_EQUALVERIFY failed")
            else:
                stack.append(encode_num(1 if ok else 0))
        elif tok == "OP_VERIFY":
            if not is_true(pop()):
                raise ScriptError("OP_VERIFY failed")
        elif tok == "OP_RETURN":
            raise ScriptError("OP_RETURN")
        elif tok == "OP_SHA256":
            stack.append(hashlib.sha256(pop()).digest())
        elif tok == "OP_HASH160":
            stack.append(hash160(pop()))
        elif tok == "OP_CHECKSIG":
            pub, sig = pop(), pop()
            stack.append(encode_num(1 if checksig(sig, pub) else 0))
        else:
            raise ScriptError(f"unknown opcode {tok}")
    if exec_stack:
        raise ScriptError("unbalanced OP_IF")
    return stack

def verify(script):
    try:
        stack = run(script)
    except ScriptError as e:
        return f"FAIL ({e})"
    return "PASS" if stack and is_true(stack[-1]) else "FAIL (false or empty stack)"
```

Note: `hashlib.new("ripemd160")` needs an OpenSSL build that still offers RIPEMD-160. If your Python raises `unsupported hash type`, use a small pure-Python RIPEMD-160 or a library such as `pycryptodome`.

</details>

### Exercise 2: Trace a P2PKH script

Top of the stack is on the right. `SIG` = `valid-sig`, `PUB` = `0279be66..1798`, `PKH` = `751e76e8..3bd6`.

| Step | Opcode | Stack after |
|---|---|---|
| 1 | push `SIG` (scriptSig) | `[SIG]` |
| 2 | push `PUB` (scriptSig) | `[SIG, PUB]` |
| 3 | `OP_DUP` | `[SIG, PUB, PUB]` |
| 4 | `OP_HASH160` | `[SIG, PUB, PKH]` |
| 5 | push `<751e76e8..3bd6>` | `[SIG, PUB, PKH, PKH]` |
| 6 | `OP_EQUALVERIFY` | `[SIG, PUB]` |
| 7 | `OP_CHECKSIG` | `[01]` |

Result: PASS, one true item left.

- **Wrong public key:** fails at step 6. The HASH160 of the wrong key does not match the hash in the scriptPubKey, so `OP_EQUALVERIFY` stops the script.
- **Wrong signature:** passes step 6 (the key is right) but step 7 pushes an empty array (false). The script runs to the end and then fails the final "top must be true" check.

Note: in real Bitcoin (since 2010) the scriptSig and scriptPubKey run as two separate scripts that share the stack, not as one joined script. For this exercise the result is the same.

### Exercise 3: Review another group's project

Any specific, kind, actionable comment counts. Weak: "Looks good." Strong: "Test case 5 (`<80>`) returns PASS in your code because `is_true` only checks for `0x00` bytes. Negative zero should be false. Suggested fix: ..."

---

## Lab answers

### Lab 1: `decodescript`

**1.1** `0x51` = `OP_1`, `0x52` = `OP_2`, `0x93` = `OP_ADD`, `0x53` = `OP_3`, `0x87` = `OP_EQUAL`. The `asm` is `1 2 OP_ADD 3 OP_EQUAL` and the `type` is `nonstandard`. Bitcoin Core prints `OP_1` to `OP_16` as plain numbers, and it also prints small data pushes (4 bytes or less) as decimal numbers. So if your parser reads `asm`, it cannot tell `OP_1` apart from a one-byte push of `0x01`. That is one reason to parse raw hex.

**1.2** `type` is `pubkeyhash`. The `asm` is `OP_DUP OP_HASH160 751e76e8199196d454941c45d1b3a323f1433bd6 OP_EQUALVERIFY OP_CHECKSIG`. Byte `0x14` (20 in decimal) is a push opcode: "push the next 20 bytes". `asm` shows the pushed data instead of the push opcode. Bitcoin Core also shows the matching regtest `address`.

**1.3** `asm`: `1 OP_IF 2 OP_ELSE 3 OP_ENDIF 2 OP_EQUAL`. This is test case 15, so it should PASS.

**1.4** `type` is `nulldata`. The data `68656c6c6f20776f726c64` is ASCII for `hello world` (11 bytes, which is the `0x0b` push). `OP_RETURN` makes the script fail immediately, so no input can ever satisfy it. Nodes know this and drop such outputs from their UTXO set.

### Lab 2: Timelock with `OP_NOTIF`

**2.2** It is a P2WSH address: `bcrt1q...`, 64 characters on regtest, longer than a P2WPKH address because the witness program is a 32-byte SHA256 of the script instead of a 20-byte key hash. `older(5)` compiles to `5 OP_CHECKSEQUENCEVERIFY`.

**2.4** `sendrawtransaction` fails with `non-BIP68-final`. The input's `sequence` of 5 asks for a relative timelock of 5 blocks (BIP68), and `OP_CHECKSEQUENCEVERIFY` (BIP112) makes the script check that the sequence is at least 5. The funding output only has 1 confirmation, so BIP68 says the transaction cannot be in the next block yet. (If you get a different error, check that `TXID` and `VOUT` are set, that `listunspent` in the `csv` wallet shows the coin, and that `finalizepsbt` returned `"complete": true`.)

**2.5** After 5 more blocks it is accepted. The witness is:

1. A DER signature by key B (71 bytes, now and then 70, ending in `01` for SIGHASH_ALL). Bitcoin Core grinds for a short `r` value, so you will rarely see 72.
2. An empty item. This is the "dissatisfaction" for key A: an empty signature makes `<A> OP_CHECKSIG` push false without failing the script.
3. The witness script.

**2.6** The `asm` is:

```
<A> OP_CHECKSIG OP_IFDUP OP_NOTIF <B> OP_CHECKSIGVERIFY 5 OP_CHECKSEQUENCEVERIFY OP_ENDIF
```

Trace, starting from `[sigB, <empty>]`:

| Opcode | Stack after | Note |
|---|---|---|
| push `<A>` | `[sigB, <empty>, A]` | |
| `OP_CHECKSIG` | `[sigB, <empty>]` | Empty signature, so false (no failure) |
| `OP_IFDUP` | `[sigB, <empty>]` | Top is false, so no copy |
| `OP_NOTIF` | `[sigB]` | Pops false, so the NOTIF branch runs |
| push `<B>` | `[sigB, B]` | |
| `OP_CHECKSIGVERIFY` | `[]` | Valid signature, nothing pushed |
| push `5` | `[05]` | |
| `OP_CHECKSEQUENCEVERIFY` | `[05]` | Sequence 5 >= 5, passes, leaves its argument |
| `OP_ENDIF` | `[05]` | |

One true item is left, so the script passes (and it meets the segwit clean-stack rule).

---

## Bonus questions (stretch goals)

### 1. Why does `OP_CHECKMULTISIG` need an extra `OP_0`, and why is it still there?

The original implementation pops one more item than it should. To spend an M-of-N multisig you must put an extra dummy item at the bottom of the scriptSig or witness, which is why multisig spends start with `OP_0`. Fixing the bug would change which scripts are valid. Old nodes would reject spends that new nodes accept, so it would need a hard fork, and every existing multisig output would still need the old behaviour anyway. Instead, the dummy became a malleability risk (anyone could change it without breaking the signature), so BIP147 (NULLDUMMY) made a non-empty dummy invalid as part of the segwit soft fork. Tapscript removes `OP_CHECKMULTISIG` entirely and uses `OP_CHECKSIGADD` instead.

### 2. What is the difference between `OP_CHECKLOCKTIMEVERIFY` and `OP_CHECKSEQUENCEVERIFY`?

`OP_CHECKLOCKTIMEVERIFY` (BIP65) is an **absolute** timelock: it checks the transaction's `nLockTime` against a block height or time, for example "not before block 900,000". `OP_CHECKSEQUENCEVERIFY` (BIP112) is a **relative** timelock: it checks the input's `nSequence` (BIP68), for example "not until 5 blocks after the coin was confirmed". Both only check a field of the spending transaction. The field itself is what consensus enforces. Both leave their argument on the stack, so scripts usually add `OP_DROP` afterwards (miniscript avoids the drop by placing the check last, as in Lab 2).
