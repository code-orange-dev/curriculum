# Module 03: Lightning Integration: Zaps and NWC

| | |
|---|---|
| **Duration** | 2 hours |
| **Level** | Intermediate (comfortable with JavaScript and the basics of Lightning invoices) |
| **You build** | Node.js scripts that read zap receipts, talk to a Lightning wallet over Nostr Wallet Connect, and send a real zap end to end |
| **Main NIPs** | [NIP-57](https://github.com/nostr-protocol/nips/blob/master/57.md) (zaps), [NIP-47](https://github.com/nostr-protocol/nips/blob/master/47.md) (Nostr Wallet Connect) |

[Back to the workshop series](../../README.md)

---

## What participants build

1. `zaps-read.js`: totals all zaps on any note and shows who sent them. No money needed.
2. `nwc.js`: a small Nostr Wallet Connect client (about 50 lines) that sends encrypted requests to a wallet over relays.
3. `balance.js`: reads your wallet balance through NWC.
4. `zap.js`: the full NIP-57 flow. Look up a lightning address, build a zap request, get an invoice, pay it over NWC, and wait for the zap receipt.

## Prerequisites

- A laptop with [Node.js](https://nodejs.org) 20 or newer.
- A Lightning wallet that supports **Nostr Wallet Connect**, with a **small** balance (a few hundred sats is plenty). [Alby Hub](https://github.com/getAlby/hub) is one option. Many mobile and web wallets also offer an NWC connection string. Ask the facilitator which wallets work at this venue.
- Optional: a lightning address on your throwaway profile, so others can zap you.
- Participants without a wallet can still do Steps 1 to 3 and pair up for Step 4.

## Safety rules (money edition)

- **Use a test wallet or a wallet with only a few hundred sats in it.** Never connect your main savings wallet to workshop code.
- An NWC connection string contains a secret. Anyone who has it can spend from your wallet up to its limits. Treat it like a password. Never paste it into an AI chat, a website or a screenshot.
- When you create the NWC connection in your wallet, **set a small budget** (for example 1,000 sats) and an expiry. Revoke it after the workshop.
- Use throwaway Nostr keys, as always. Never paste a real `nsec` anywhere.

## Learning goals

After this module, participants can:

- Describe the NIP-57 zap flow: LNURL lookup, kind 9734 zap request, invoice, payment, kind 9735 zap receipt.
- Explain what `allowsNostr` and `nostrPubkey` mean in an LNURL-pay response, and why the receipt must be signed by `nostrPubkey`.
- Validate a zap receipt instead of trusting it blindly.
- Explain how NIP-47 uses Nostr events (kinds 13194, 23194, 23195) as an encrypted channel between an app and a wallet.
- Pay an invoice from code with a spending budget that the wallet enforces.

## Facilitator run sheet

| Time | Block | Notes |
|---|---|---|
| 0:00 | Welcome and money safety | 10 min. Read the safety rules. Check who has a funded test wallet. Pair up people without one. |
| 0:10 | Concepts: LNURL, the zap flow, NWC | 20 min. Draw the flow diagram below on a whiteboard. |
| 0:30 | Step 1: read zaps | 15 min. No money involved. Everyone runs it on a popular note. |
| 0:45 | Steps 2 and 3: NWC and balance | 15 min. Create a budgeted NWC connection, then read the balance. |
| 1:00 | Step 4: send a zap | 25 min. Zap the facilitator's demo note 21 sats. Watch receipts appear live on the projector. |
| 1:25 | Vibe coding extension | 20 min. |
| 1:45 | Discussion and wrap-up | 15 min. Remind everyone to revoke the NWC connection. |

**Total: 2 hours.**

Facilitator prep:

- Make a demo throwaway profile with a zap-enabled lightning address and post a note to zap. Test one zap to it the day before.
- Bring a small float of sats to help people with empty wallets, or a list of wallets that give a working NWC string quickly.
- Have `zaps-read.js` running against your demo note on the projector during Step 4.

---

## Concepts

### The zap flow (NIP-57)

```
Sender's client                 Recipient's LNURL server            Relays
     |                                    |                            |
 1.  | read recipient kind 0 -> lud16 ----|--------------------------->|
 2.  | GET /.well-known/lnurlp/<name> --->|                            |
     |<-- callback, allowsNostr: true,    |                            |
     |    nostrPubkey, min/maxSendable    |                            |
 3.  | sign kind 9734 zap request         |                            |
     | (NOT published to relays)          |                            |
 4.  | GET callback?amount=..&nostr=<9734>|                            |
     |<-- bolt11 invoice                  |                            |
 5.  | pay invoice (any wallet, or NWC)   |                            |
 6.  |                                    | invoice paid ->            |
     |                                    | sign kind 9735 receipt --->|
     |                                    | with nostrPubkey           |
 7.  | read 9735, check it  <-------------|----------------------------|
```

Key points:

- A **lightning address** like `name@domain` maps to `https://domain/.well-known/lnurlp/name` (LNURL-pay). The profile field is `lud16`.
- The LNURL server must say `"allowsNostr": true` and give a `nostrPubkey`. That key signs the receipts.
- The **zap request** (kind 9734) is signed by the sender and sent to the LNURL server, not to relays. It says who is zapped (`p` tag), what (`e` tag for a note), how much (`amount` in millisats) and where to publish the receipt (`relays`).
- The **zap receipt** (kind 9735) is published by the recipient's server after payment. It carries the `bolt11` invoice and the original zap request in a `description` tag.
- A receipt is a claim, not proof. Check that it is signed by the `nostrPubkey` from the LNURL response and that the amounts match.

### Nostr Wallet Connect (NIP-47)

NWC lets an app control a wallet through Nostr events. The wallet gives you a connection string:

```
nostr+walletconnect://<wallet pubkey>?relay=wss://relay.example&secret=<hex secret key>
```

- The `secret` is a key made just for this app. The app signs requests with it.
- The app sends a **kind 23194** request, encrypted to the wallet, for example `{"method":"pay_invoice","params":{"invoice":"lnbc..."}}`.
- The wallet answers with a **kind 23195** response that references the request with an `e` tag.
- The wallet publishes a **kind 13194** info event listing the methods and encryption it supports.
- The wallet enforces budgets and permissions per connection. Your code never holds the wallet's keys.

---

## Hands-on guide

### Step 0: Project setup

```bash
mkdir zaps && cd zaps
npm init -y
npm pkg set type=module
npm install nostr-tools@2 ws
```

Create `lib.js` (the same helper as in Module 01):

```js
// lib.js
import WebSocket from 'ws'
import { useWebSocketImplementation } from 'nostr-tools/pool'
import * as nip19 from 'nostr-tools/nip19'

// Node 20 has no built-in WebSocket, so we hand one to nostr-tools
useWebSocketImplementation(WebSocket)

export const RELAYS = (process.env.RELAYS || 'wss://relay.damus.io,wss://nos.lol,wss://relay.primal.net').split(',')

export function loadSecretKey() {
  const nsec = process.env.NSEC
  if (!nsec) throw new Error('Set NSEC first: export NSEC=nsec1...')
  const { type, data } = nip19.decode(nsec)
  if (type !== 'nsec') throw new Error('NSEC must start with nsec1')
  return data // Uint8Array
}
```

Make a throwaway key if you do not have one from Module 01:

```bash
node -e "import('nostr-tools/pure').then(p=>import('nostr-tools/nip19').then(n=>console.log(n.nsecEncode(p.generateSecretKey()))))"
export NSEC=nsec1...
```

### Step 1: Read zaps on a note (no money needed)

```js
// zaps-read.js
import { SimplePool } from 'nostr-tools/pool'
import * as nip19 from 'nostr-tools/nip19'
import { getSatoshisAmountFromBolt11 } from 'nostr-tools/nip57'
import { RELAYS } from './lib.js'

// Usage: node zaps-read.js <note1... or nevent1...>
const { type, data } = nip19.decode(process.argv[2])
const noteId = type === 'note' ? data : data.id

const pool = new SimplePool()
const receipts = await pool.querySync(RELAYS, { kinds: [9735], '#e': [noteId] })

let total = 0
for (const r of receipts) {
  const bolt11 = r.tags.find((t) => t[0] === 'bolt11')?.[1]
  const description = r.tags.find((t) => t[0] === 'description')?.[1]
  if (!bolt11 || !description) continue
  const sats = getSatoshisAmountFromBolt11(bolt11)
  const request = JSON.parse(description) // the kind 9734 zap request, signed by the sender
  total += sats
  console.log(`${sats} sats from ${nip19.npubEncode(request.pubkey).slice(0, 16)}... "${request.content}"`)
}
console.log(`${receipts.length} receipts, ${total} sats in total`)
pool.close(RELAYS)
```

Find a popular note in any Nostr app, copy its `note1...` or `nevent1...` id, and run:

```bash
node zaps-read.js note1...
```

Discuss: this script trusts every receipt. Who signed them? What stops someone from publishing fake receipts to make a note look popular? (Answer: nothing, unless you check the receipt's `pubkey` against the recipient's LNURL `nostrPubkey`. Step 4 does that.)

### Step 2: A tiny NWC client

In your wallet, create a new NWC connection (sometimes called "app connection"). Give it a **small budget** and permission to pay invoices and read the balance. Copy the `nostr+walletconnect://...` string and keep it out of chats and screenshots:

```bash
export NWC_URL='nostr+walletconnect://...'
```

Create `nwc.js`:

```js
// nwc.js
import { SimplePool } from 'nostr-tools/pool'
import { finalizeEvent } from 'nostr-tools/pure'
import { nip47 } from 'nostr-tools' // nip47 has no subpath export
import * as nip04 from 'nostr-tools/nip04'
import * as nip44 from 'nostr-tools/nip44'
import { hexToBytes } from 'nostr-tools/utils'
import './lib.js' // sets up WebSocket for Node

// Send one NIP-47 request (kind 23194) and wait for the reply (kind 23195).
export async function nwcRequest(connectionString, method, params = {}) {
  const { pubkey: wallet, relays, secret } = nip47.parseConnectionString(connectionString)
  const sk = hexToBytes(secret) // the app's key, given to us by the wallet
  const pool = new SimplePool()

  // The wallet's info event (kind 13194) says which encryption it supports.
  const info = await pool.get(relays, { kinds: [13194], authors: [wallet] })
  const encryption = info?.tags.find((t) => t[0] === 'encryption')?.[1] || 'nip04'
  const useNip44 = encryption.split(' ').includes('nip44_v2')
  const convKey = useNip44 ? nip44.getConversationKey(sk, wallet) : null
  const encrypt = (text) => (useNip44 ? nip44.encrypt(text, convKey) : nip04.encrypt(sk, wallet, text))
  const decrypt = (text) => (useNip44 ? nip44.decrypt(text, convKey) : nip04.decrypt(sk, wallet, text))

  const tags = [['p', wallet]]
  if (useNip44) tags.push(['encryption', 'nip44_v2'])
  const request = finalizeEvent({
    kind: 23194,
    created_at: Math.floor(Date.now() / 1000),
    tags,
    content: encrypt(JSON.stringify({ method, params })),
  }, sk)

  return new Promise((resolve, reject) => {
    const done = (fn, value) => {
      clearTimeout(timer)
      sub.close()
      pool.close(relays)
      fn(value)
    }
    const timer = setTimeout(() => done(reject, new Error('wallet did not answer in 60 s')), 60_000)

    // Subscribe first, then publish, so we cannot miss a fast reply.
    const sub = pool.subscribe(relays, { kinds: [23195], authors: [wallet], '#e': [request.id] }, {
      onevent: (e) => {
        const res = JSON.parse(decrypt(e.content))
        if (res.error) done(reject, new Error(`${res.error.code}: ${res.error.message}`))
        else done(resolve, res.result)
      },
      oneose: () => pool.publish(relays, request),
    })
  })
}
```

Walk through it together:

- The wallet pubkey, relay list and app secret all come from the connection string.
- NIP-47 now prefers NIP-44 encryption. Older wallets use NIP-04. The wallet's kind 13194 info event tells us which one to use.
- We subscribe for the answer **before** publishing the request, so a fast wallet cannot answer before we listen.

### Step 3: Read your balance

```js
// balance.js
import { nwcRequest } from './nwc.js'

const result = await nwcRequest(process.env.NWC_URL, 'get_balance')
console.log('balance:', Math.floor(result.balance / 1000), 'sats') // NWC amounts are in millisats
```

```bash
node balance.js
```

If you get a `RESTRICTED` or `UNAUTHORIZED` error, the connection does not have permission for `get_balance`. Edit it in your wallet.

### Step 4: Send a zap

```js
// zap.js
import { SimplePool } from 'nostr-tools/pool'
import { finalizeEvent } from 'nostr-tools/pure'
import { makeZapRequest, getSatoshisAmountFromBolt11 } from 'nostr-tools/nip57'
import * as nip19 from 'nostr-tools/nip19'
import { RELAYS, loadSecretKey } from './lib.js'
import { nwcRequest } from './nwc.js'

// Usage: node zap.js <npub1...> <sats> "comment"
const [target, satsArg = '21', comment = 'Zap from a Nostr workshop'] = process.argv.slice(2)
const recipient = nip19.decode(target).data
const msats = Number(satsArg) * 1000
const sk = loadSecretKey()
const pool = new SimplePool()

// 1. Find the recipient's lightning address in their kind 0 profile
const profileEvent = await pool.get(RELAYS, { kinds: [0], authors: [recipient] })
const { lud16 } = JSON.parse(profileEvent?.content || '{}')
if (!lud16) throw new Error('recipient has no lud16 lightning address in their profile')

// 2. Ask their LNURL server if it supports zaps
const [name, domain] = lud16.split('@')
const lnurlp = await (await fetch(`https://${domain}/.well-known/lnurlp/${name}`)).json()
if (!lnurlp.allowsNostr || !lnurlp.nostrPubkey) throw new Error('this lightning address does not support zaps')
if (msats < lnurlp.minSendable || msats > lnurlp.maxSendable) throw new Error('amount out of range')

// 3. Build and sign the zap request (kind 9734). It is NOT published to relays.
const zapRequest = finalizeEvent(
  makeZapRequest({ pubkey: recipient, amount: msats, comment, relays: RELAYS }),
  sk,
)

// 4. Send it to the LNURL callback and get a bolt11 invoice back
const url = new URL(lnurlp.callback)
url.searchParams.set('amount', String(msats))
url.searchParams.set('nostr', JSON.stringify(zapRequest))
const { pr: invoice, reason } = await (await fetch(url)).json()
if (!invoice) throw new Error('no invoice: ' + reason)
// (this helper only understands mainnet 'lnbc' invoices and returns 0 for others)
const invoiceSats = getSatoshisAmountFromBolt11(invoice)
if (invoiceSats && invoiceSats * 1000 !== msats) throw new Error('invoice amount does not match')

// 5. Watch for the zap receipt (kind 9735) that the recipient's server publishes
const since = Math.floor(Date.now() / 1000) - 10
const sub = pool.subscribe(RELAYS, { kinds: [9735], '#p': [recipient], since }, {
  onevent: (receipt) => {
    const description = receipt.tags.find((t) => t[0] === 'description')?.[1]
    if (!description || JSON.parse(description).id !== zapRequest.id) return // someone else's zap
    if (receipt.pubkey !== lnurlp.nostrPubkey) return console.log('receipt from the wrong key, ignoring')
    console.log('zap receipt received:', receipt.id)
    sub.close()
    pool.close(RELAYS)
  },
})

// 6. Pay the invoice: with NWC if configured, otherwise by hand
if (process.env.NWC_URL) {
  const result = await nwcRequest(process.env.NWC_URL, 'pay_invoice', { invoice })
  console.log('paid, preimage:', result.preimage)
} else {
  console.log('Pay this invoice with any Lightning wallet:\n' + invoice)
}
```

Zap the facilitator's demo profile 21 sats:

```bash
node zap.js npub1...facilitator 21 "hello from row 3"
```

You should see `paid, preimage: ...` and then `zap receipt received: ...`. The facilitator's `zaps-read.js` on the projector shows your zap and comment. Without `NWC_URL`, the script prints the invoice so you can pay it from any wallet app.

This version zaps a profile. To zap a note, pass `event: <the note event>` to `makeZapRequest` instead of `pubkey`. It then adds the `e` tag for you.

---

## Vibe coding prompts

Paste the relevant file with the prompt. **Never paste your `nsec` or your NWC connection string.** The scripts read both from environment variables.

1. "Extend `zaps-read.js` to fully validate each receipt: fetch the recipient's LNURL `nostrPubkey`, check the receipt is signed by it, check the `bolt11` amount equals the zap request's `amount` tag, and mark invalid receipts."
2. "Change `zap.js` so it can zap a note: take a `nevent1...`, fetch the event, and build the zap request with `makeZapRequest({ event, ... })`."
3. "Write `leaderboard.js`: subscribe to all kind 9735 receipts tagged with `#t` or `#e` for our workshop notes and keep a live top-10 of zappers in the terminal."
4. "Add a `make_invoice` call to `nwc.js` and write `receive.js` that creates a 100 sat invoice and then polls `lookup_invoice` until it is paid."
5. "Add the zap button from this module to my Module 02 browser client, using `window.nostr` to sign the zap request and showing the invoice as a QR code."

Before you run anything AI-written that spends money: read it, check the amount is in millisats where the spec says millisats, and keep the wallet budget small.

## Discussion questions

1. The recipient's LNURL server signs the zap receipt, not the recipient. What does that mean for trust? Could a server lie about zaps?
2. Zaps are public by default. Who learns what when you zap someone: the relays, the recipient's LNURL server, the whole world? What would a private zap need?
3. NWC puts a spending key for your wallet into an app. How do budgets, expiry and per-app connections limit the damage if the app is hacked?
4. Why does the zap request go to the LNURL server and not to relays? What would go wrong if it went to relays first?
5. How could zaps be used to fight spam, or to pay for services? (Module 06 builds on this.)

## Common problems and fixes

| Problem | Fix |
|---|---|
| `recipient has no lud16` | The profile has no lightning address on these relays. Try another recipient, or add `RELAYS` where their profile lives. |
| `this lightning address does not support zaps` | The LNURL server does not set `allowsNostr`. Plain lightning payments work, zaps do not. Use a provider that supports zaps. |
| `amount out of range` | `minSendable` and `maxSendable` are in millisats. Zap a bigger or smaller amount. |
| `wallet did not answer in 60 s` | Check the relay in the connection string is reachable. Make sure the wallet is online (a self-hosted wallet must be running). Re-copy the connection string. |
| `RESTRICTED`, `QUOTA_EXCEEDED` or `INSUFFICIENT_BALANCE` errors | The connection lacks permission, hit its budget, or the wallet is empty. Fix it in the wallet settings. |
| Paid, but no receipt arrives | The receipt goes to the relays in your zap request. Wait 10 to 20 seconds. Some servers publish slowly or only to some relays. The payment still went through. |
| `invoice amount does not match` with a testnet invoice | `getSatoshisAmountFromBolt11` only reads mainnet `lnbc` invoices and returns 0 for others, so the check is skipped. If it fails on mainnet, do not pay: the server returned the wrong amount. |
| `Package subpath './nip47' is not defined` | Import it from the main package: `import { nip47 } from 'nostr-tools'`. |

## Resources

- [NIP-57: Lightning zaps](https://github.com/nostr-protocol/nips/blob/master/57.md) (kinds 9734 and 9735)
- [NIP-47: Nostr Wallet Connect](https://github.com/nostr-protocol/nips/blob/master/47.md) (kinds 13194, 23194, 23195)
- [NIP-44: Encrypted payloads](https://github.com/nostr-protocol/nips/blob/master/44.md)
- [LNURL specs (LUDs)](https://github.com/lnurl/luds) (LUD-06 pay requests, LUD-16 lightning addresses)
- [nostr-tools](https://github.com/nbd-wtf/nostr-tools) (`nip57`, `nip47`, `nip44` helpers)
- [Alby Hub](https://github.com/getAlby/hub) (self-custodial wallet with NWC)

Previous: [Module 02](../02-build-a-client/README.md) | Next: [Module 04: Running Your Own Relay](../04-run-a-relay/README.md)
