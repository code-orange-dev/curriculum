# Contributing to this Curriculum

> This curriculum is CC0-licensed. You can use it, modify it, translate it, and redistribute it without restriction. Here's how to contribute improvements back.

---

## How to Contribute

### Fix an error

If you find a technical error (wrong BIP reference, incorrect code, broken link), open an issue or submit a PR directly. Technical accuracy is the highest priority.

### Improve an exercise

The exercises are designed to be challenging but achievable. If you completed one and found it too easy, too hard, or unclear, submit a PR with improvements. Include a note explaining what you changed and why.

### Add a new lab

New labs are welcome, especially:
- A wallet-fingerprinting lab built on **real** transaction hex from the S4 fingerprint table (not invented wallet behavior)
- A payjoin lab that runs against `payjoin-cli` on regtest
- Rust versions of the Python labs
- Season Two topics (see [SESSIONS.md](./SESSIONS.md))

### Translate the curriculum

If you want to translate this curriculum into another language, create a new directory (e.g., `translations/id/` for Indonesian, `translations/th/` for Thai) and translate the READMEs. Exercise code comments should also be translated; the code itself stays in English.

### Add reference implementations

Solutions live next to their lab in `labs/<lab>/solutions/`. If the lab has a grader (like `labs/silent-payments/run_vectors.py`), your solution must pass it.

---

## Style Guide

### Writing

- Write in clear, direct English. Avoid jargon unless you define it.
- Use second person ("you") for exercises and instructions.
- Use present tense for descriptions ("Silent Payments use ECDH") and imperative for instructions ("Implement the function").
- Keep sentences short. One idea per sentence.
- When referencing a BIP, always link to the specification.

### Code

- Python exercises: Python 3.8+, minimal dependencies, clear docstrings, type hints
- Rust exercises: stable Rust, idiomatic style, well-commented
- All exercises must include: clear instructions, type signatures, test cases, and reflection questions
- Never include complete solutions in the exercise files: only hints, pseudocode and tests. Solutions go in `solutions/`

### File structure

```
privacy-track/
├── README.md, SESSIONS.md       # overview and the 12 session plans
├── FACILITATOR_GUIDE.md         # how to run any session
├── ISSUE_POOL.md, PR_CHECKLIST.md
├── labs/<topic>/
│   ├── README.md                # what you build, how to run it
│   ├── *.py                     # exercise files with YOUR CODE HERE markers
│   └── solutions/               # reference implementations (optional)
└── resources/                   # glossary, reading list
```

### Accuracy rules

- Every factual claim about a wallet, BIP or PR should be checkable. Link the source
- Prefer official test vectors over hand-made test data. When a lab simplifies the spec, say so in its README
- Exercise files must run without errors when nothing is implemented yet (skip unimplemented parts gracefully)

---

## Review Process

1. Submit a PR with a clear description of what you changed
2. A maintainer will review for technical accuracy and pedagogical clarity
3. If the change affects an exercise, the reviewer will attempt the exercise to verify it works
4. Merged PRs will be credited in the commit history and (optionally) in the README

---

## Code of Conduct

Be kind, be accurate, be helpful. This curriculum exists to make Bitcoin privacy better for everyone. Contributions that further that goal are welcome regardless of the contributor's background or experience level.

---

*Code Orange Dev School | [codeorange.dev](https://codeorange.dev) | CC0 1.0 Universal*
