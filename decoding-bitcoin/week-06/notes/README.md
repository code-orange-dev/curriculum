# Week 6 notes

Notes for [week 6: Script basics](../README.md). For the full course plan, see the [syllabus](../../README.md).

## Key ideas

- **Script is a small stack language.** A script is a list of items read left to right. Data items are pushed onto a stack. Opcodes pop their inputs from the top of the stack and push their results. There are no variables and no loops.
- **Every output has a lock, every input has a key.** The scriptPubKey in an output says what is needed to spend it. The scriptSig in the spending input provides it. A node runs the scriptSig first, then the scriptPubKey on the resulting stack. The spend is valid if nothing fails and the top item is true (non-zero).
- **P2PK is the simplest lock.** `<pubkey> OP_CHECKSIG`. The spender only provides a signature. It was used for early coinbase rewards, including the coins in block 9 that paid the first person-to-person transaction in block 170.
- **P2PKH hides the key behind a hash.** `OP_DUP OP_HASH160 <pkh> OP_EQUALVERIFY OP_CHECKSIG`. The spender provides a signature and the public key. The output is smaller, the address is short and has a checksum, and the public key stays private until the coin is spent.
- **Script is deliberately limited.** No loops, size limits and opcode limits keep the cost of checking every script small and predictable. Every full node runs every script, so this protects the whole network.
- **Some opcodes were removed.** In 2010, opcodes such as `OP_CAT` and `OP_MUL` were disabled after bugs and risks were found. Removing features is a soft fork. Adding them back takes much longer.
- **Output types have fixed patterns.** You can tell P2PK, P2PKH, P2SH, P2WPKH, P2WSH and P2TR apart from the first bytes of the scriptPubKey alone.

## Common mix-ups

| Mix-up | Correction |
|---|---|
| "The scriptSig and scriptPubKey are joined into one script." | They were before 2010. Today the scriptSig runs first, then the scriptPubKey runs separately on the same stack. |
| "An address is a public key." | A P2PKH address is a Base58Check encoding of a version byte and the 20-byte HASH160 of a public key. P2PK has no address at all. |
| "A script succeeds if it runs to the end." | It must also end with a non-zero item on top. An empty stack, or false on top, means failure. |
| "OP_EQUALVERIFY and OP_EQUAL do the same thing." | `OP_EQUAL` pushes true or false. `OP_EQUALVERIFY` stops the script immediately if the items are not equal and leaves nothing. |
| "`decodescript` checks whether a script is valid." | It only parses bytes into opcodes. It does not run the script. |
| "Disabled opcodes are fine in a branch that does not run." | A script containing a disabled opcode fails anywhere, even in an unexecuted `OP_IF` branch. |

## Session plan

| Time | Block | Who | Notes |
|---|---|---|---|
| 0:00 to 0:05 | Welcome and roles | Facilitator | Confirm roles. Ask people to have pen and paper ready. |
| 0:05 to 0:15 | Opening question | Facilitator, everyone | "Why a tiny stack language?" Silent minute first. |
| 0:15 to 0:25 | Concept recap | Facilitator | Slides: stack machine, lock and key, P2PK, P2PKH, limits. |
| 0:25 to 1:05 | Question round | Question owners | About 6 minutes per question. Owners of questions 1 and 4 draw the stack. |
| 1:05 to 1:20 | Exercise walkthrough | Exercise driver | Lab steps 1, 2 and 4. Trace the real P2PKH spend together. |
| 1:20 to 1:27 | Wrap-up and next week | Facilitator, Summariser | 3 takeaways. Assign week 7 questions and roles. |
| 1:27 to 1:30 | Buffer and close | Facilitator | Overrun or open questions. |

## Facilitator tips

Before the session:

- Run lab steps 1 to 5 on a fresh regtest node.
- Prepare a shared place for stack traces (a Discord thread, a shared document or the screen share). Traces are much easier to follow when written down.
- Look up block 9 and block 170 on mempool.space yourself, so you can show them if someone could not find them.

Where people get stuck:

- **Top of the stack.** People draw it on the left or the right and then get confused. Agree on one direction at the start (the slides use "top on the right").
- **Byte vs opcode.** `14` in a P2PKH script is not an opcode name, it means "push the next 20 bytes". Push opcodes `01` to `4b` push that many bytes.
- **RIPEMD160 missing.** On some systems with OpenSSL 3, Python's `hashlib.new('ripemd160')` fails. The lab shows an `openssl` command with the legacy provider as a fallback.
- **Small numbers in asm.** Bitcoin Core shows `OP_2` as `2` in asm, and mempool.space shows `OP_PUSHNUM_2`. Same opcode, different display.
- **Running P2PKH in the wrong order.** Remind people that the scriptSig items are pushed first, so the signature is at the bottom.

## Glossary

- **Stack:** a last-in, first-out list. Script pushes items on top and opcodes pop from the top.
- **Opcode:** a one-byte instruction, such as `OP_DUP` (0x76) or `OP_CHECKSIG` (0xac).
- **Push opcode:** a byte from 0x01 to 0x4b that means "push the next N bytes". `OP_PUSHDATA1/2/4` push longer data.
- **scriptPubKey (locking script):** the script in an output that sets the spending condition.
- **scriptSig (unlocking script):** the script in an input that provides the data to meet the condition.
- **P2PK:** Pay to Public Key. `<pubkey> OP_CHECKSIG`.
- **P2PKH:** Pay to Public Key Hash. `OP_DUP OP_HASH160 <pkh> OP_EQUALVERIFY OP_CHECKSIG`.
- **HASH160:** RIPEMD160 of SHA256. Produces 20 bytes.
- **Base58Check:** the encoding for legacy addresses. It adds a version byte and a 4-byte checksum.
- **Compressed / uncompressed public key:** 33 bytes (`02`/`03` + x) or 65 bytes (`04` + x + y).
- **Turing complete:** able to compute anything a general computer can, which requires loops or recursion. Script is not.
- **Disabled opcode:** an opcode that makes any script containing it fail, such as `OP_CAT` since 2010.

## Further resources

- [Bitcoin Wiki: Script](https://en.bitcoin.it/wiki/Script) (full opcode table)
- [learnmeabitcoin: Transaction structure](https://learnmeabitcoin.com/technical/transaction/)
- [Mastering Bitcoin](https://github.com/bitcoinbook/bitcoinbook), the chapter on authorization and authentication (Script)
- [Programming Bitcoin](https://github.com/jimmysong/programmingbitcoin), chapter 6 (Script)
- [mempool.space](https://mempool.space) for looking up blocks 9 and 170 and decoding real scripts
- [Bitcoin Core RPC reference](https://developer.bitcoin.org/reference/rpc/) (`decodescript`, `getaddressinfo`, `generatetodescriptor`)
