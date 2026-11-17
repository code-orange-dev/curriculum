# Week 8 notes

[Week 8 overview](../README.md) · [Exercises](../exercises/README.md) · [Solutions](../solutions/README.md) · [Slides](../slides/slides.md)

Project week: build a Bitcoin Script stack machine in pairs or small groups, then demo it.

## Key ideas

- **Script is a tiny stack language.** A script is a list of opcodes and data pushes. The interpreter reads them left to right and changes one stack. There are no loops and no backward jumps, so a script always finishes, and its running time is limited by its length.
- **Every stack item is a byte array.** Numbers, booleans, keys and hashes are all bytes on the stack. Opcodes that do maths decode the bytes as a Script number first. `OP_EQUAL` compares bytes, not numeric values.
- **Script numbers have their own encoding.** They are little-endian with a sign bit in the top bit of the last byte. Zero is the empty array, -1 is `0x81`, 128 needs two bytes (`0x8000`). Maths opcodes only accept inputs of up to 4 bytes.
- **False has three shapes.** An empty array, all-zero bytes, or negative zero (`0x80` at the end) are false. Everything else is true.
- **The final rule.** A script passes only if nothing failed along the way and the stack ends non-empty with a true top item. Segwit and tapscript add a clean-stack rule: exactly one item must be left.
- **Conditionals need a second stack.** `OP_IF`, `OP_NOTIF`, `OP_ELSE` and `OP_ENDIF` push and pop true/false entries on an execution stack. Opcodes only run when every entry is true.
- **Limits protect nodes.** Every node runs every script, so Bitcoin caps push size (520 bytes), stack size (1,000 items), opcode count (201 non-push opcodes) and script size (10,000 bytes) for legacy and segwit v0 scripts.
- **Testing is the real skill.** The most valuable tests check subtle failures: an empty stack at the end, negative zero, operand order, skipped branches.

## Common mix-ups

| Mix-up | Correction |
|---|---|
| "`OP_0` pushes the byte `0x00`." | `OP_0` pushes an **empty** byte array. Both are false, but they are different bytes, so `OP_0 <00> OP_EQUAL` is false. |
| "If no opcode failed, the script passed." | The final check still applies: the stack must be non-empty and the top true. `OP_1 OP_VERIFY` fails. |
| "`OP_SUB` computes top minus second." | It computes **second minus top**: `OP_5 OP_3 OP_SUB` is 2. The first value pushed is the left operand. |
| "Opcodes in a skipped branch are ignored completely." | Mostly, but `OP_IF`/`OP_ELSE`/`OP_ENDIF` still count for nesting, and disabled opcodes like `OP_CAT` fail the script even in a skipped branch. |
| "`OP_CHECKSEQUENCEVERIFY` removes its argument." | CLTV and CSV leave their argument on the stack. That is why scripts often follow them with `OP_DROP`. |
| "`OP_CHECKMULTISIG` pops exactly M sigs and N keys." | It pops one extra item. The dummy must be empty (BIP147). |

## Session plan

| Time | Block | Who | Notes |
|---|---|---|---|
| 0:00 to 0:05 | Welcome and roles | Facilitator | Confirm roles and question owners. Check every group posted a repo link. |
| 0:05 to 0:15 | Opening question | Facilitator, everyone | "What did you only really understand once you built it?" One sentence each. |
| 0:15 to 0:45 | Group demos | Each group, Devil's advocate | About 5 minutes per group. Devil's advocate asks "what input breaks it?" |
| 0:45 to 1:10 | Question round | Question owners | 6 questions, about 4 minutes each. Others add, then move on. |
| 1:10 to 1:20 | Exercise walkthrough | Exercise driver | P2PKH trace (test case 20) in trace mode. Ask where it fails with a wrong key or signature. |
| 1:20 to 1:30 | Wrap-up and next week | Facilitator, Summariser | Week 9 lessons, new roles, pair groups for code review. |

## Facilitator tips

**Before the session**

- Check that every group has posted a repository link on Discord. Message groups that have not.
- Run one group's tests yourself if you can, so you know what a working demo looks like.
- Agree a demo order and post it, so groups are ready to share their screen.
- Pair groups for Exercise 3 (code review) if they have not paired themselves.

**Where people get stuck**

- **Bytes versus integers.** Groups that store numbers as integers break on `OP_EQUAL` and negative zero. Point them to the true/false table in the slides.
- **Operand order for `OP_SUB`.** Ask them to trace `OP_5 OP_3 OP_SUB` on paper.
- **Conditionals.** Many first versions skip `OP_ELSE` and `OP_ENDIF` inside a skipped branch, which breaks nesting.
- **Scope creep.** Some groups try to implement real ECDSA. Encourage a stub for `OP_CHECKSIG` and more tests instead.
- **Groups that did not finish.** A half-finished project with honest notes is still a good demo. Ask them to show what works and what they learned.

## Glossary

| Term | Meaning |
|---|---|
| Stack machine | A program that runs instructions which push to and pop from a stack. Bitcoin Script is one. |
| Opcode | One instruction in Script, stored as one byte (for example `0x76` is `OP_DUP`). |
| Data push | An opcode that puts bytes on the stack (`OP_0`, `OP_1` to `OP_16`, direct pushes, `OP_PUSHDATA1/2/4`). |
| Script number | A stack item read as a little-endian, sign-magnitude integer. |
| Negative zero | The byte `0x80` (or zeros ending in `0x80`). It counts as false. |
| Execution stack | The interpreter's list of open `OP_IF` branches and whether each is active. |
| `...VERIFY` | Opcodes that fail the script at once if the result is false (`OP_VERIFY`, `OP_EQUALVERIFY`, `OP_CHECKSIGVERIFY`). |
| Clean stack | The segwit and tapscript rule that exactly one item must remain at the end. |
| Altstack | A second stack, reached with `OP_TOALTSTACK` and `OP_FROMALTSTACK`. |
| Disabled opcode | An opcode such as `OP_CAT` or `OP_MUL` that was switched off in 2010 and fails the script if present. |
| Miniscript | A structured way to write Bitcoin Script policies that tools can analyse and compile. |

## Further resources

- [Bitcoin Core `interpreter.cpp`](https://github.com/bitcoin/bitcoin/blob/master/src/script/interpreter.cpp): the real Script interpreter. Search for `EvalScript`.
- [Bitcoin Core `script_tests.json`](https://github.com/bitcoin/bitcoin/blob/master/src/test/data/script_tests.json): hundreds of script test vectors.
- [Programming Bitcoin, chapter 6: Script](https://github.com/jimmysong/programmingbitcoin/blob/master/ch06.asciidoc): builds a Script interpreter in Python, step by step.
- [Mastering Bitcoin](https://github.com/bitcoinbook/bitcoinbook): the chapters on transactions and authorization explain Script and timelocks.
- [learnmeabitcoin: Script](https://learnmeabitcoin.com/technical/script/): a visual guide to opcodes.
- [Bitcoin Wiki: Script](https://en.bitcoin.it/wiki/Script): the list of opcodes with their byte values.
- [Bitcoin Optech: Miniscript](https://bitcoinops.org/en/topics/miniscript/) and [Timelocks](https://bitcoinops.org/en/topics/timelocks/).
- [BIP65 (CLTV)](https://github.com/bitcoin/bips/blob/master/bip-0065.mediawiki), [BIP68 (relative lock-time)](https://github.com/bitcoin/bips/blob/master/bip-0068.mediawiki), [BIP112 (CSV)](https://github.com/bitcoin/bips/blob/master/bip-0112.mediawiki), [BIP147 (NULLDUMMY)](https://github.com/bitcoin/bips/blob/master/bip-0147.mediawiki).
