# Facilitator Guide: The Privacy Sessions

How to host one 90-minute session well. The per-session content (story, concept, hands-on, PRs, follow-ups) lives in [SESSIONS.md](./SESSIONS.md). This page covers everything that stays the same from session to session.

---

## Your role

You're a host, not a professor. You need to be one session ahead of the room, have done the hands-on yourself, and be comfortable saying "I don't know, let's read the code." Two facilitators per session is ideal: one drives the screen, the other watches chat and unblocks people.

## The week before

- [ ] Do the session's hands-on end to end on a clean machine. Write down every gotcha
- [ ] Pick 1-2 live PRs for the Review Circle. Good picks are small, privacy-relevant, active in the last month, and have a clear "how would you test this?" angle. For S3 (Review Club), announce the PR a week ahead and ask people to build it
- [ ] Use the live searches in [ISSUE_POOL.md](./ISSUE_POOL.md) to find 3-5 targets for the Proof-of-Work Board, and check each one the morning of the session
- [ ] Post the session announcement with: the topic, what to install, the lab link, and "drop-ins welcome"

## The morning of

- [ ] Re-check that every issue on the board is still open and unclaimed
- [ ] Re-check that the Review Circle PR hasn't merged or changed direction (if it merged, that's fine: review the merged diff and read the discussion that got it there)
- [ ] Fund the signet/regtest wallets you'll use on screen
- [ ] Have the primary text for the Cypherpunk Corner open

## Running the room

| Beat | Your job |
|---|---|
| 🩸 Cold Open | Tell the story and stop. Let the room react before you explain anything |
| 🕳 Rabbit Hole | One analogy, one diagram, then straight to code. 15 min max |
| 🛠 Hands-On | Get everyone to a first success in 10 minutes. Pair stuck people with finished ones. Don't live-debug one person's setup in front of everyone; take it to a breakout |
| 🔍 Review Circle | Participants explain, you ask questions. See the rules below |
| 📜 Cypherpunk Corner | Pick a reader and let the argument happen. Steelman the side nobody takes |
| 🎯 Proof-of-Work Board | Everyone names one concrete follow-up out loud. Write the names down |

## Review Circle rules

These come from the program's [Review Club playbook](https://github.com/code-orange-dev/code-orange-dev/blob/main/privacy-contributor-program/REVIEW_CLUB.md), condensed for a 20-minute slot:

1. **Participants explain, you ask.** "What problem does this solve?" "Where's the test?" "What would break if...?"
2. **Test before you opine.** A build-and-run report beats a guess
3. **Nothing goes upstream on a timer.** Post only what's genuinely useful: a reproduction, a test report with exact steps and platform, or a question the thread hasn't already answered. If nothing qualifies, say so. That's a good outcome too
4. **Never paste your words into someone else's mouth.** Don't dictate comments for participants to post
5. **Separate questions from objections**, and respect each project's norms (read its CONTRIBUTING first)

## Evidence and rewards

- After each session, log for each participant who produced something: what was built/tested/reviewed, links, and the next step. The format is in the program's [CONTRIBUTOR_SCORECARD.md](https://github.com/code-orange-dev/code-orange-dev/blob/main/privacy-contributor-program/CONTRIBUTOR_SCORECARD.md)
- Sats go to **completed proof of work**: a lab at 28/28, a test report someone else can follow, a merged doc fix, a reproduced bug. Never pay per comment or per PR opened. That's how programs end up spamming maintainers
- Merged PRs go on the [PR dashboard](https://github.com/code-orange-dev/PR-tracking-dashboard)
- Within 48 hours, send attendees: what we covered (2 lines), their one follow-up, and the next session date ([community playbook](https://github.com/code-orange-dev/community-playbook))

## Common problems

**"The EC math is too hard."** The SP lab's `secp.py` hides the math behind `a * G` and `P + Q`, so participants only need to know that points add and scalars multiply. For the curious, point them to the [Bitcoin Dojo](../bitcoin-dojo/) weeks 1-2. Draw it on a whiteboard with small numbers first.

**"My build failed."** Keep a pre-built binary or a shared regtest box around. Setup pain belongs in a breakout room, and afterwards it makes a great docs PR.

**"I can't find anything to contribute."** A test report on an open PR is a contribution. So are docs. So is a reproduction of an open bug. [ISSUE_POOL.md](./ISSUE_POOL.md) links live searches and test targets for every session.

**"Bitcoin Core is intimidating."** Start with the SP lab, which uses the exact vectors in `src/test/data/bip352_send_and_receive_vectors.json`. Then read `src/common/bip352.cpp`, which is short. That's a much gentler entry to Core than most.

**"We only have 60 minutes."** Drop the Cypherpunk Corner, assign the Rabbit Hole reading as pre-work, and keep Hands-On + Review Circle.

**"Nobody came back."** Check that the 48-hour follow-up went out, that the hands-on actually worked for newcomers, and that the session time suits your timezones.

## Guest speakers

Builders working on this season's topics. Invite one per month. Offer 30 minutes, share the session plan, and ask them to talk about *what still needs building and testing*.

| Topic | People to ask (verify they're still active) |
|---|---|
| Silent Payments (BIP352) | Josie Baker and Ruben Somsen (BIP authors), Eunovo (Bitcoin Core SP PRs), cygnet3 (rust-silentpayments, Dana), setavenger (BlindBit), nymius (bdk-sp), Craig Raw (Sparrow, Frigate) |
| Payjoin | Dan Gould and the Payjoin Dev Kit team |
| Coin selection | Murch |
| Light clients | Rob Netzke / rustaceanrob (Kyoto), the Floresta maintainers (Vinteum) |
| Network privacy | Vasil Dimov (private broadcast), 0xB10C (peer-observer) |
| CoinSwap | Chris Belcher and the openswap team |

## After the season

- Run S12 as a sprint, then hold a retro: which sessions produced proof of work, which labs broke, and which PRs got reviewed
- Record what people actually shipped (with links) in the program's tracking
- Invite repeat contributors into the Review Club and the [fellowship](https://github.com/code-orange-dev/fellowships) pipeline
- Measure retention at 3, 6 and 12 months, per the program's [MEASUREMENT.md](https://github.com/code-orange-dev/code-orange-dev/blob/main/privacy-contributor-program/MEASUREMENT.md)

---

*Code Orange Dev School | [codeorange.dev](https://codeorange.dev) | CC0 1.0 Universal*
