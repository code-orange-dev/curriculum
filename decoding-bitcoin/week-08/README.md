# Week 08: Project: build your own Bitcoin stack

[← Week 7](../week-07/) · [Syllabus](../README.md) · [Week 9 →](../week-09/)

> Part of the [Decoding Bitcoin syllabus](../README.md#week-8-project-build-your-own-bitcoin-stack). Lessons are on [Decoding Bitcoin](https://bitcoindevs.xyz/decoding) by The Bitcoin Dev Project; this folder is Code Orange's study guide for the week.

**Opening question:** What did you only really understand once you had to build it yourself?

A bigger hands-on build that brings together everything so far: implement a Bitcoin Script stack machine. Work in pairs or small groups and demo it on Monday.

## Lessons (on Decoding Bitcoin)

- [Project: Build your own bitcoin Stack](https://bitcoindevs.xyz/decoding/project)

## Discussion questions

Each participant owns one question and comes ready to explain it. Model answers are in [`solutions/`](solutions/README.md), so try first.

1. How did you represent the stack and opcodes in your code? What would you change next time?
2. How does your stack treat true and false? Compare it with how Bitcoin Script does.
3. Which opcode was hardest to implement, and why?
4. How does your implementation handle a script that fails halfway through?
5. What limits (stack size, script size, opcode count) did you add, and why does Bitcoin have them?
6. Which test cases best convinced you that your stack is correct?

## Exercises

1. Build the Bitcoin stack project. Push your code to GitHub and share the link on Discord. ([Stack project](https://bitcoindevs.xyz/decoding/project))
2. Run a P2PKH script (with dummy keys) through your stack and show each step.
3. Review another group's project and leave them one helpful comment.

More hands-on work, including bitcoin-cli labs on regtest, is in [`exercises/`](exercises/README.md).

## What's in this folder

| Folder | What it holds |
|---|---|
| [`exercises/`](exercises/README.md) | Hands-on exercises for this week |
| [`solutions/`](solutions/README.md) | Model answers to the questions and exercises (try them first!) |
| [`slides/`](slides/slides.md) | Facilitator slides for the session ([how to present them](../README.md#presenting-the-slides)) |
| [`notes/`](notes/README.md) | Key ideas, common mix-ups, a session plan and extra resources |
