# Curated Issue Pool

**The source of contribution targets for the Privacy Sessions.** Participants pick from here instead of hunting randomly across GitHub. That's the guardrail that keeps us useful to maintainers rather than noisy.

> **Rule:** if an issue isn't in this file (or a curator hasn't just verified it), it isn't a session target.

**Last full verification: 2026-09-26.** Re-verify weekly and on the morning of any session.

---

## Two kinds of target

- **BUILD**: an open issue with no active PR. You can claim it (comment first) and work on it
- **TEST**: an issue that already has an open PR. Don't open a competing PR. Build the PR, run it, and post a useful test report if one's missing. For newcomers this is often the *better* contribution

## How an issue earns a spot

1. **Open**, verified within the last 7 days
2. **Wanted**: labeled `good first issue` / `help wanted`, or confirmed welcome by a maintainer
3. **Scoped**: plausible to finish in or shortly after a session
4. **Not claimed**: for BUILD, no assignee and no open PR. Otherwise it goes in as TEST

Stale entries get marked `RETIRED` (don't delete them; the history is useful). Aim for 3-6 live entries per repo.

---

## Live pool

### Silent Payments (S1-S3)

| Issue | Type | Why it fits | Status |
|---|---|---|---|
| [shroud#132](https://github.com/CypherCommons/shroud/issues/132) Unit tests for the Rust BIP-352 scanner | BUILD | The SP lab teaches exactly what to test, and the official vectors are the test data. A previous attempt (#133) was closed, so read why first | LIVE |
| [shroud#156](https://github.com/CypherCommons/shroud/issues/156) SP UTXOs spent elsewhere never detected | BUILD | A real wallet bug; reproduce it on signet first. Community project (Chaitika) | LIVE |
| [bdk-sp#55](https://github.com/bitcoindevkit/bdk-sp/issues/55) False "bad tweak" when intermediate key sum hits zero | BUILD | This is lab vector 27, and the BIP fix already landed ([bips#2142](https://github.com/bitcoin/bips/pull/2142)) | LIVE |
| [rust-silentpayments#32](https://github.com/cygnet3/rust-silentpayments/issues/32) Add reference to code examples | BUILD | Docs, a gentle first PR | LIVE |
| [rust-silentpayments#109](https://github.com/cygnet3/rust-silentpayments/issues/109) Duplicate `calculate_ecdh_shared_secret()` | BUILD | Small refactor; ask the maintainer which copy should stay | LIVE |
| [danawallet#434](https://github.com/cygnet3/danawallet/issues/434) Button overlap in 3-button navigation | BUILD | Labeled `quick win`, Flutter UI | LIVE |
| [danawallet#403](https://github.com/cygnet3/danawallet/issues/403) Padding when keyboard is open | BUILD | Flutter UI, small | LIVE |
| [danawallet#466](https://github.com/cygnet3/danawallet/issues/466) Output-ambiguity recognition | BUILD (advanced) | Research + code. Only for people who finished the labels stretch | LIVE |
| [blindbit-oracle#58](https://github.com/setavenger/blindbit-oracle/issues/58) GetFullBlock drops outpoints | TEST | Open fix in [#60](https://github.com/setavenger/blindbit-oracle/pull/60): build it and test against signet | LIVE |
| [blindbit-oracle#36](https://github.com/setavenger/blindbit-oracle/issues/36) Add debug info endpoint | BUILD | Go, self-contained | LIVE |
| [bitcoin#36338](https://github.com/bitcoin/bitcoin/pull/36338) P2PKH pubkey extraction from malleated scriptSig | TEST / review | S1's Review Circle PR. Build it, run `bip352_tests` | LIVE |

### Coin selection & wallet (S4-S5)

| Issue | Type | Why it fits | Status |
|---|---|---|---|
| [bdk_wallet#543](https://github.com/bitcoindevkit/bdk_wallet/issues/543) Missing MAX_STANDARD_TX_WEIGHT check | TEST | Fix open in [#544](https://github.com/bitcoindevkit/bdk_wallet/pull/544) | LIVE |
| [bdk_wallet#46](https://github.com/bitcoindevkit/bdk_wallet/issues/46) Network consistency between genesis and descriptors | TEST | Fix open in [#520](https://github.com/bitcoindevkit/bdk_wallet/pull/520) | LIVE |
| [bdk_wallet#187](https://github.com/bitcoindevkit/bdk_wallet/issues/187) Return feerate from tx construction | TEST | Fix open in [#380](https://github.com/bitcoindevkit/bdk_wallet/pull/380) | LIVE |

### Payjoin (S6)

| Issue | Type | Why it fits | Status |
|---|---|---|---|
| [rust-payjoin#865](https://github.com/payjoin/rust-payjoin/issues/865) `cargo doc` improvements (tracking) | BUILD | Many small doc items; claim one item in a comment | LIVE |
| [rust-payjoin#551](https://github.com/payjoin/rust-payjoin/issues/551) Preserve privacy for >2-output txs | BUILD (advanced) | Real privacy logic. A previous attempt (#1837) closed, so read it first | LIVE |
| [rust-payjoin#1300](https://github.com/payjoin/rust-payjoin/issues/1300) .gitignore organization | - | A PR exists on a fork; check with the maintainers before touching it | CHECK |

### Light clients & nodes (S7)

| Issue | Type | Why it fits | Status |
|---|---|---|---|
| [Floresta#799](https://github.com/getfloresta/Floresta/issues/799) Document all floresta-cli RPC endpoints | BUILD | Tracking issue with several merged PRs; pick an endpoint that's still undocumented | LIVE |
| [Floresta#1014](https://github.com/getfloresta/Floresta/issues/1014) Deny dangerous `as` casts | BUILD | Rust hygiene, split into small PRs | LIVE |
| [Floresta#1308](https://github.com/getfloresta/Floresta/issues/1308) config.toml parsed three times | - | A fork PR exists; ask before starting | CHECK |
| [kyoto](https://github.com/2140-dev/kyoto/issues) | - | No beginner-labeled issues right now. Use Kyoto for reading and testing, and ask a maintainer (sourcing playbook below) | SOURCING |

### Network privacy (S8)

| Issue | Type | Why it fits | Status |
|---|---|---|---|
| [peer-observer#182](https://github.com/peer-observer/peer-observer/issues/182) Metric for unsolicited/unannounced txs | BUILD | `good first issue`, a clear spec | LIVE |
| [peer-observer#336](https://github.com/peer-observer/peer-observer/issues/336) log-extractor: parse debug.log | BUILD | `help wanted`, bigger but well-bounded | LIVE |
| [peer-observer#396](https://github.com/peer-observer/peer-observer/issues/396) Sequence diagrams in websocket-tool | BUILD | Front-end-ish, visual | LIVE |
| Bitcoin Core private-broadcast follow-ups ([#34322](https://github.com/bitcoin/bitcoin/pull/34322), [#34533](https://github.com/bitcoin/bitcoin/pull/34533), [#36330](https://github.com/bitcoin/bitcoin/pull/36330)) | TEST / review | Test with Tor/I2P on your platform, report exact steps | LIVE |

### CoinJoin, swaps, Lightning, ecash (S9-S11)

| Issue | Type | Why it fits | Status |
|---|---|---|---|
| [joinmarket-clientserver good first issues](https://github.com/JoinMarket-Org/joinmarket-clientserver/issues?q=is%3Aopen+label%3A%22good+first+issue%22) | BUILD | 20+ labeled, but many are years old. Confirm an issue is still wanted before starting | SOURCING |
| [openswap#1021](https://github.com/citadel-foss/openswap/issues/1021) Derive minimum swap amount instead of hardcoding | BUILD | Scoped; confirm with maintainers | CHECK |
| [openswap#1037](https://github.com/citadel-foss/openswap/issues/1037) Human-readable maker names | BUILD | Scoped UX feature | CHECK |
| LDK / ldk-node / Core Lightning offers, cdk, Fedimint | - | No verified beginner targets yet. Source via maintainers before S10/S11 | SOURCING |

---

## The maintainer-DM sourcing playbook

This is how "we know a few maintainers" becomes a warm issue pipeline, and it's Code Orange's real long-term asset.

**The goal:** a handful of maintainers who think of Code Orange as *"the program that sends me prepared contributors"* and occasionally point us at work they'd actually like help with.

**The opening DM (adapt it per person):**
> Hey [name] - I help run Code Orange's Bitcoin Privacy Sessions. We teach [topic] hands-on, and participants build and test real PRs before they ever open their own (they run a build/test/CONTRIBUTING checklist first - we're careful not to add noise). Are there a few issues, or PRs that need testing, where outside help would genuinely be welcome? We'll only point people at things you actually want touched.

**Why it works:** it leads with respect for their time, signals that we have a quality floor, and asks them to *pull* work toward us instead of us pushing PRs at them. Offering *testing* is often the most welcome thing we can offer.

**After the first merge or useful test report:** send a short thank-you and ask "anything else in this vein?" That loop is the whole game.

**Priority for this season:** Silent Payments (cygnet3, setavenger, nymius, the Shroud team), Kyoto, openswap, and the LN/ecash repos for S10-S11.

**Per-repo checklist:**
- [ ] Identify 1-2 active maintainers (recent commits / reviews)
- [ ] Send the opening DM and log the response below
- [ ] Link their CONTRIBUTING.md in the table
- [ ] Watch their `good first issue` / `help wanted` labels

### Maintainer contact log

| Date | Repo | Maintainer | Response / issues flagged |
|---|---|---|---|
| | | | |

---

## Outcomes log

Record everything here: merged PRs, useful test reports, reproduced bugs. It's how we report proof of work and spot which repos are working for us.

| Date | Repo | Link | Contributor | Type (PR / test / review / repro) | Outcome |
|---|---|---|---|---|---|
| | | | | | |
