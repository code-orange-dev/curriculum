# Standalone Workshops

> **Single-session, hands-on workshops you can run at a meetup, a Bitcoin house, a school or online.**

[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-orange.svg)](https://creativecommons.org/publicdomain/zero/1.0/)

Each workshop stands alone. No other session is needed first. Most are made for non-developers and beginner developers, and every one is safe to run with test coins or tiny amounts.

[Back to the curriculum](../README.md)

---

## The workshops

| Workshop | Length | Level | What people leave with | Guide |
|---|---|---|---|---|
| Build a 2-of-3 multisig wallet | 2.5 h | Beginner | A 2-of-3 multisig on testnet in Sparrow, a two-key spend, a tested backup of the wallet file, and a plan for where each key lives | [multisig](./multisig/README.md) |
| Run your own Bitcoin node | 2.5 h | Beginner | Bitcoin Core running on signet with pruning, Sparrow connected to a real node over the local network and Tor, and a home node shopping list | [nodes](./nodes/README.md) |
| Mine bitcoin at home with a Bitaxe | 2 h | Beginner | A Bitaxe hashing on a pool, a feel for hashrate and difficulty, and their own numbers for odds, power cost and heat | [mining](./mining/README.md) |
| Accept bitcoin with BTCPay Server | 2.5 h | Beginner | A BTCPay store with their own wallet, a Point of Sale app, a paid test invoice, and a plan for running it for real | [btcpay](./btcpay/README.md) |
| Ecash for everyday payments (Cashu and Fedimint) | 2 h | Beginner | A Cashu wallet with test ecash, sending and claiming tokens, and a clear view of the custody trade-off and federations | [ecash](./ecash/README.md) |
| Nostr and private group chats with White Noise | 2 h | Beginner, mixed rooms | A Nostr identity with a backed-up key, a private White Noise group chat, and a way to check a friend's npub | [nostr](./nostr/README.md) |
| Bitcoin privacy in practice | 2.5 h | Beginner to intermediate, mixed rooms | A threat model, labels, frozen coins and coin control in Sparrow, and a first look at PayJoin, Silent Payments and Tor | [privacy](./privacy/README.md) |

## What every guide has

- **At a glance:** length, level, audience and main tools.
- **What participants leave with.**
- **Materials and hardware**, with rough costs in USD.
- **Before the session:** a checklist for the host.
- **Run sheet:** a time table that adds up to the session length.
- **Concepts in five minutes**, to explain the idea before the hands-on part.
- **Safety rules** to read out loud.
- **Hands-on guide**, step by step, with a "Check" after the important steps.
- **Discussion questions**, **common problems and fixes**, **safety notes** and **further resources**, including recaps of past sessions where we have one.

## Suggested order

There is no required order, but these paths work well:

```
For savers:      multisig  ->  nodes  ->  privacy
For shops:       btcpay    ->  nodes  ->  ecash
For the curious: mining    ->  nodes
For chatters:    nostr     ->  ecash  ->  privacy
```

## Rules for every workshop

- **Test coins or tiny amounts only.** Use testnet4, signet or mutinynet, or a few hundred sats on mainnet for a host demo.
- **Never real seed phrases on shared machines.** Real seeds go only into a hardware wallet.
- **Seed words are never photographed and never typed into a website,** not even test ones. Good habits start in practice.
- **Do the whole guide yourself first,** on a clean machine, a few days before. Apps change, and menus move. If a step in a guide is out of date, fix it here: that is a great first contribution.

## Where to go next

- Developers who enjoyed the Nostr workshop: [Vibe Coding on Nostr](../nostr-workshops/README.md), six hands-on developer modules.
- Developers who enjoyed the privacy workshop: the [Privacy Track](../privacy-track/README.md), with labs and real open-source issues.
- People who want a longer course: the [Sovereign Bitcoiner Crash Course](../sovereign-bitcoiner/README.md) puts nodes, BTCPay, multisig and privacy together over several weeks.

## Contributing

Ran one of these workshops? Tell us what worked and what broke. See [CONTRIBUTING.md](../CONTRIBUTING.md). Translations are very welcome.

## License

[CC0 1.0 Universal](../LICENSE). No rights reserved.
