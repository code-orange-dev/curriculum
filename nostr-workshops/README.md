# Vibe Coding on Nostr - Monthly Workshop Series

> **Monthly hands-on sessions exploring Bitcoin-adjacent open-source development.**

[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-orange.svg)](https://creativecommons.org/publicdomain/zero/1.0/)

**Contents:** [Overview](#overview) | [Workshop Modules](#workshop-modules) | [How to run a session](#how-to-run-a-session) | [Format](#format) | [License](#license)

---

## Overview

Vibe Coding on Nostr is a monthly workshop series where participants build on Nostr, integrate Lightning payments, and contribute to the broader FOSS ecosystem around Bitcoin. Each session is standalone - attend any session without prerequisites.

## Workshop Modules

Each module in `modules/` is a self-contained workshop:

| Module | Topic | Duration |
|--------|-------|----------|
| 01 | [Nostr Basics: Keys, Relays, and NIPs](./modules/01-nostr-basics/README.md) | 2 hours |
| 02 | [Building a Nostr Client from Scratch](./modules/02-build-a-client/README.md) | 3 hours |
| 03 | [Lightning Integration: Zaps and NWC](./modules/03-zaps-and-nwc/README.md) | 2 hours |
| 04 | [Running Your Own Relay](./modules/04-run-a-relay/README.md) | 2 hours |
| 05 | [Nostr for Identity and Authentication](./modules/05-identity-and-auth/README.md) | 2 hours |
| 06 | [Building on NIP-90 (Data Vending Machines)](./modules/06-data-vending-machines/README.md) | 3 hours |

Every module has the same parts: what participants build, prerequisites, learning goals, a facilitator run sheet, a step-by-step hands-on guide with working code, vibe coding prompts, discussion questions, common problems and fixes, and links to the exact NIPs.

The code uses JavaScript with the [nostr-tools](https://github.com/nbd-wtf/nostr-tools) library and the [`nak`](https://github.com/fiatjaf/nak) command-line tool. Module 04 also uses Go to build a relay.

## How to run a session

**The week before**

- Pick the module and do its hands-on guide yourself, start to finish, on a clean machine. Write down every snag.
- Post the announcement with the topic, what to install (each module lists it under "Prerequisites"), and "drop-ins welcome".
- For Module 03 and the payment step of Module 06, check which Lightning wallets with Nostr Wallet Connect work well for your group, and bring a few sats to help people who arrive with an empty wallet.

**On the day**

- Test the public relays used in the module from the venue Wi-Fi. If WebSockets are blocked or slow, run `nak serve` on your laptop and give everyone `ws://<your-ip>:10547` as their relay.
- Start every session with the module's safety rules, out loud: **never paste a real `nsec` into a website, a chat, or an AI assistant; use throwaway keys; use test wallets and small amounts for anything with sats.**
- Follow the run sheet in the module. The times add up to the session length. Get everyone to a first success in the first 30 minutes.
- Pair people up. Put someone who is stuck next to someone who is done. Take long setup problems to a side table instead of debugging one laptop on the projector.

**The vibe coding block**

- Each module ends with prompts participants give to an AI assistant to extend what they built.
- The rules: paste code, never keys or wallet connection strings. Run what the AI writes, read it, and check it against the NIP it claims to implement. The NIP is the source of truth, not the AI.
- Finish with two or three short demos of what people added.

**Afterwards**

- Share the module link and one follow-up idea with attendees.
- If something in a module was wrong or confusing, fix it in this repo. That is a great first contribution, from you or from a participant.

## Format

- Monthly in-person sessions at Bitcoin House Bali (or remote)
- 2-3 hours per session
- Laptop required
- All skill levels welcome

## License

CC0 1.0 Universal. Public domain.
