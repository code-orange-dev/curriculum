# Network Privacy Lab (S8): Wiretap Yourself

Three experiments on your own Bitcoin Core node: see what BIP324 hides from your ISP, broadcast a transaction without revealing your IP, and measure how many of your peers sit on the same network operator.

**Needs:** Bitcoin Core **31.0 or later**, [Tor](https://www.torproject.org/download/) running locally (SOCKS on `127.0.0.1:9050`), `jq`, and Wireshark (or `tcpdump`). Everything below uses **signet** (P2P port 38333), with funds from a signet faucet.

> Facilitators: run it end to end the day before. Signet has far fewer Tor/I2P peers than mainnet, so private broadcast can take a while to find one. If it stalls, that's worth discussing in its own right.

## 0. Setup

`~/.bitcoin/bitcoin.conf` (on macOS: `~/Library/Application Support/Bitcoin/bitcoin.conf`):

```ini
signet=1
[signet]
proxy=127.0.0.1:9050     # reach onion peers through Tor
listenonion=1
```

```bash
bitcoind -daemon
alias bcli='bitcoin-cli -signet'
bcli getnetworkinfo | jq '.networks[] | {name, reachable}'
```

`onion` should be `reachable: true`. If it isn't, fix Tor before going further, because experiments 2 and 3 depend on it.

## 1. BIP324: what does your ISP see?

```bash
bcli getpeerinfo | jq -r '.[] | [.addr, .network, .transport_protocol_type] | @tsv'
```

`v2` means the connection is encrypted (BIP324, on by default since Core 27). `v1` means plaintext.

**Capture both:**
1. Start Wireshark on your network interface with the filter `tcp.port == 38333`. Leave it running for a minute. Pick a `v2` peer and look at the payload: it's random-looking bytes, with no `version`, `inv` or `tx` strings
2. Restart with `-v2transport=0` (`bcli stop`, then `bitcoind -daemon -v2transport=0`) and capture again. Now look for the ASCII message names (`version`, `inv`, `tx`) in plaintext. Anyone on the path can read which transactions you announce
3. Restart without the flag afterwards

**Discuss:** BIP324 hides message contents from the *network path*. What does it *not* hide from the peer you're talking to? And what can your ISP still learn from traffic timing and volume?

## 2. Private broadcast: send without revealing your IP

In Core 31, `-privatebroadcast` applies to the **`sendrawtransaction` RPC only**. Wallet sends are unaffected. So we build the transaction in the wallet but broadcast it ourselves.

```bash
bcli stop && bitcoind -daemon -privatebroadcast=1
bcli createwallet s8            # skip if you already have a funded signet wallet
bcli -rpcwallet=s8 getnewaddress   # fund this from a signet faucet, wait for 1 confirmation

# Build and sign, but don't broadcast or add to the wallet:
HEX=$(bcli -rpcwallet=s8 -named send \
      outputs='[{"'$(bcli -rpcwallet=s8 getnewaddress)'": 0.0001}]' \
      add_to_wallet=false fee_rate=2 | jq -r .hex)

bcli sendrawtransaction "$HEX"
bcli getprivatebroadcastinfo
```

Watch `getprivatebroadcastinfo` until the transaction leaves the queue, then find it on a signet explorer.

**What happened:** Core opened a fresh, short-lived connection to a Tor or I2P peer, handed over this one transaction, and closed the connection. The transaction didn't go into your own mempool first. Recipients never see your IP, and two transactions you broadcast this way can't be linked by connection.

**Discuss:** why one connection per transaction? What would an observer learn if you broadcast your wallet's transactions normally, from the same IP, for a year?

## 3. ASmap: how surrounded are you?

An eclipse attacker who controls one big hosting provider can fill many of your peer slots. First count the operators among your current peers.

**Before**, look up each IPv4/IPv6 peer's AS with Team Cymru's public whois:

```bash
bcli getpeerinfo | jq -r '.[] | select(.network=="ipv4" or .network=="ipv6") | .addr' \
  | sed -E 's/^\[?([^]]+)\]?:[0-9]+$/\1/' \
  | while read ip; do whois -h whois.cymru.com " -v $ip" | tail -1; done
```

Count how many peers share an AS.

**After**, restart with the asmap data embedded in Core 31 (it's off by default):

```bash
bcli stop && bitcoind -daemon -asmap=1
# wait a few minutes for outbound connections to fill
bcli getpeerinfo | jq -r '.[] | .mapped_as // "none"' | sort | uniq -c | sort -rn
```

With asmap on, Core buckets peers by AS instead of by IP range, and `getpeerinfo` shows each peer's `mapped_as`.

**Discuss:** compare the diversity before and after. Why is asmap off by default? (Think about who produces the map, how it goes stale, and whether every node should use the same one.)

## Proof of work (pick one)

- Write up your AS-diversity numbers from before and after, as a short guide for your community
- Test an open private-broadcast follow-up PR on your platform and post a precise test report (see [how to find one](../../ISSUE_POOL.md) and the [PR checklist](../../PR_CHECKLIST.md))
- Take a [peer-observer](https://github.com/peer-observer/peer-observer) beginner issue

## References

- [Bitcoin Core 31.0 release notes](https://bitcoincore.org/en/releases/31.0/): `-privatebroadcast`, embedded asmap
- [BIP324](https://github.com/bitcoin/bips/blob/master/bip-0324.mediawiki) · [Core `doc/tor.md`](https://github.com/bitcoin/bitcoin/blob/master/doc/tor.md)
- [Optech: Eclipse attacks](https://bitcoinops.org/en/topics/eclipse-attacks/)
