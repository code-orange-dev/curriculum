# Week 9: Advanced Taproot & MuSig2

[← Week 8](../week-08/) · [Syllabus](../README.md) · [Week 10 →](../week-10/)

> This week as it appears in the [rawBit Study Cohort syllabus](../README.md#week-9-advanced-taproot--musig2).

**Topics:**
- MuSig2: interactive multi-signature with a single public key
- Taproot script trees: building complex spending conditions
- MAST (Merkelized Abstract Syntax Tree) via Taproot
- Combining Taproot with timelocks for complex contracts
- Tapscript (BIP342): new opcodes for Taproot

**Exercises:**
1. Design a Taproot output with 3 spending conditions in the script tree
2. Build an escrow contract: "Alice+Bob key-path, OR Alice after 1000 blocks, OR Bob+mediator"
3. Calculate the Merkle root of a script tree with 4 leaves

## Status

`exercises/` and `solutions/` are still empty for this week. Build the exercises in [rawBit](https://github.com/rawBit-io/rawbit) and share them, or pick up a [good first issue](https://github.com/code-orange-dev/curriculum/labels/good%20first%20issue) to add them here.
