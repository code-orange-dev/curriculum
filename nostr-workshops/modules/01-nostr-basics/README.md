# Module 01: Nostr Basics: Keys, Relays, and NIPs

| | |
|---|---|
| **Duration** | 2 hours |
| **Level** | Beginner |
| **You build** | A set of small Node.js scripts that create a Nostr identity, sign and publish events, and read them back from relays |
| **Main NIPs** | [NIP-01](https://github.com/nostr-protocol/nips/blob/master/01.md), [NIP-19](https://github.com/nostr-protocol/nips/blob/master/19.md), [NIP-11](https://github.com/nostr-protocol/nips/blob/master/11.md) |

[Back to the workshop series](../../README.md)

---

## What participants build

By the end of the session every participant has:

1. A throwaway Nostr key pair, shown in hex and in `npub` / `nsec` form.
2. A script that signs a profile (kind 0) and a note (kind 1) and publishes them to public relays.
3. A script that reads notes back from relays and checks every signature.
4. A clear picture of what a relay really sees: raw `REQ`, `EVENT` and `EOSE` messages.

## Prerequisites

- A laptop with internet access.
- [Node.js](https://nodejs.org) 20 or newer (`node --version`).
- A terminal and a text editor.
- Optional: the [`nak`](https://github.com/fiatjaf/nak) command-line tool. Download a binary from its [releases page](https://github.com/fiatjaf/nak/releases), or run `go install github.com/fiatjaf/nak@latest` if you have Go.
- No Nostr account needed. We make throwaway keys.

## Safety rules (read these out loud)

- **Never paste a real `nsec` into a website, a chat, or an AI assistant.** Your `nsec` is your whole identity. Anyone who has it can post as you forever. There is no password reset.
- Use the throwaway keys we generate today. Treat them as public.
- Everything you publish to a public relay is public and very hard to delete. Do not post anything you would not put on a billboard.

## Learning goals

After this module, participants can:

- Explain the three parts of Nostr: keys (identity), events (signed data), relays (dumb servers that store and forward).
- Describe the fields of a NIP-01 event (`id`, `pubkey`, `created_at`, `kind`, `tags`, `content`, `sig`) and how the `id` is computed.
- Tell the difference between hex keys and NIP-19 `npub` / `nsec` / `note` / `nevent` / `nprofile` strings.
- Publish to and query from several relays, and explain why one relay is never enough.
- Find and read a NIP when they hit something new.

## Facilitator run sheet

| Time | Block | Notes |
|---|---|---|
| 0:00 | Welcome and safety rules | 10 min. Read the safety rules. Ask who already uses a Nostr app. |
| 0:10 | Concepts: keys, events, relays, NIPs | 20 min. Draw: client signs event, sends to 3 relays, another client reads from 2 of them. Open NIP-01 on screen. |
| 0:30 | Setup check | 10 min. Everyone runs `node --version` and `npm install`. Helpers walk the room. |
| 0:40 | Hands-on 1: keys and NIP-19 | 20 min. Steps 1 and 2. |
| 1:00 | Hands-on 2: sign and publish | 20 min. Steps 3 and 4. Everyone finds their note on njump.me. |
| 1:20 | Hands-on 3: read and see the raw protocol | 15 min. Steps 5 and 6. |
| 1:35 | Vibe coding extension | 15 min. Pick one prompt from the list. Pair up. |
| 1:50 | Discussion and wrap-up | 10 min. Discussion questions. Point to Module 02. |

**Total: 2 hours.**

Facilitator prep: run every step once on the day, because public relays change. Have a backup relay ready (see "Common problems"). If the venue Wi-Fi blocks WebSockets, run `nak serve` on your laptop and give people `ws://<your-ip>:10547`.

---

## Concepts in five minutes

**Keys.** A Nostr identity is a secp256k1 key pair, the same curve Bitcoin uses. The secret key signs. The public key is your identity. Signatures are Schnorr signatures (BIP-340).

**Events.** Everything on Nostr is an event. A note, a profile, a like, a zap receipt: all events. They differ by `kind`:

```json
{
  "id": "<sha256 of the serialized event, hex>",
  "pubkey": "<author public key, hex>",
  "created_at": 1700000000,
  "kind": 1,
  "tags": [["t", "nostrworkshop"]],
  "content": "Hello Nostr!",
  "sig": "<schnorr signature of the id, hex>"
}
```

The `id` is the SHA-256 hash of `[0, pubkey, created_at, kind, tags, content]` serialized as JSON. Change one character and the `id` changes, so the signature no longer matches.

**Relays.** A relay is a WebSocket server. Clients send three main messages:

- `["EVENT", <event>]` to publish. The relay answers `["OK", <id>, true|false, <message>]`.
- `["REQ", <sub id>, <filter>]` to subscribe. The relay sends `["EVENT", <sub id>, <event>]` for each match, then `["EOSE", <sub id>]` (end of stored events), then keeps sending new matches live.
- `["CLOSE", <sub id>]` to stop.

Relays do not talk to each other. Clients pick which relays to use. That is where censorship resistance comes from.

**NIPs.** NIPs (Nostr Implementation Possibilities) are the specs. NIP-01 is the core. Everything else is optional. The full list is at [github.com/nostr-protocol/nips](https://github.com/nostr-protocol/nips).

---

## Hands-on guide

### Step 0: Project setup

```bash
mkdir nostr-basics && cd nostr-basics
npm init -y
npm pkg set type=module
npm install nostr-tools@2 ws
```

Create `lib.js`. Every other script imports it.

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

`RELAYS` can be changed with an environment variable, for example `RELAYS=ws://localhost:10547` for a local test relay.

### Step 1: Generate a key pair

```js
// keys.js
import { generateSecretKey, getPublicKey } from 'nostr-tools/pure'
import * as nip19 from 'nostr-tools/nip19'
import { bytesToHex } from 'nostr-tools/utils'

const sk = generateSecretKey()          // 32 random bytes (Uint8Array)
const pk = getPublicKey(sk)             // hex string, 64 chars

console.log('secret key (hex):', bytesToHex(sk))
console.log('public key (hex):', pk)
console.log('nsec:', nip19.nsecEncode(sk))
console.log('npub:', nip19.npubEncode(pk))

// Round trip: decode the npub back to hex
const { type, data } = nip19.decode(nip19.npubEncode(pk))
console.log(type, data === pk)
```

```bash
node keys.js
```

Copy the `nsec` line and keep it in your terminal session:

```bash
export NSEC=nsec1...   # your throwaway key from keys.js
```

On Windows PowerShell use `$env:NSEC="nsec1..."`.

### Step 2: Understand NIP-19

Hex is what the protocol uses on the wire. NIP-19 strings are for humans. They use bech32 (like Bitcoin `bc1` addresses), so a typo is caught by the checksum, and the prefix tells you what it is:

| Prefix | Contains | Share it? |
|---|---|---|
| `npub` | public key | Yes |
| `nsec` | secret key | **Never** |
| `note` | event id | Yes |
| `nevent` | event id plus relay hints and author | Yes |
| `nprofile` | public key plus relay hints | Yes |

The same with `nak`:

```bash
SK=$(nak key generate)
nak key public $SK
nak encode nsec $SK
nak encode npub $(nak key public $SK)
nak decode npub1...            # paste any npub, nevent or nprofile
```

### Step 3: Sign and publish a profile and a note

```js
// publish.js
import { finalizeEvent, verifyEvent, getPublicKey } from 'nostr-tools/pure'
import { SimplePool } from 'nostr-tools/pool'
import * as nip19 from 'nostr-tools/nip19'
import { RELAYS, loadSecretKey } from './lib.js'

const sk = loadSecretKey()
const pool = new SimplePool()

// Kind 0: profile metadata. The content is a JSON string.
const profile = finalizeEvent({
  kind: 0,
  created_at: Math.floor(Date.now() / 1000),
  tags: [],
  content: JSON.stringify({
    name: 'workshop-' + getPublicKey(sk).slice(0, 6),
    about: 'Throwaway key from a Nostr workshop',
  }),
}, sk)

// Kind 1: a short text note.
const note = finalizeEvent({
  kind: 1,
  created_at: Math.floor(Date.now() / 1000),
  tags: [['t', 'nostrworkshop']],
  content: process.argv[2] || 'Hello Nostr! My first signed event. #nostrworkshop',
}, sk)

console.log('note is valid:', verifyEvent(note))
console.log(JSON.stringify(note, null, 2))

for (const event of [profile, note]) {
  const results = await Promise.allSettled(pool.publish(RELAYS, event))
  results.forEach((r, i) =>
    console.log(`kind ${event.kind} -> ${RELAYS[i]}:`, r.status === 'fulfilled' ? 'ok' : r.reason))
}

console.log('view it:', 'https://njump.me/' + nip19.neventEncode({ id: note.id, relays: RELAYS }))
pool.close(RELAYS)
```

```bash
node publish.js "Hello from the workshop"
```

Open the `njump.me` link. Your note is now readable by any Nostr app. Notice that `finalizeEvent` filled in `pubkey`, `id` and `sig` for you.

The same with `nak`:

```bash
nak event --sec $NSEC -c "hello from nak" wss://nos.lol
nak event --sec $NSEC -k 0 -c '{"name":"nak-test"}' wss://nos.lol
```

### Step 4: Prove that signatures protect content

```js
// tamper.js
import { generateSecretKey, finalizeEvent, verifyEvent } from 'nostr-tools/pure'

const sk = generateSecretKey()
const note = finalizeEvent({
  kind: 1,
  created_at: Math.floor(Date.now() / 1000),
  tags: [],
  content: 'pay Alice 1000 sats',
}, sk)

// Copy through JSON, the way an event arrives from a relay.
const wire = JSON.stringify(note)

const honest = JSON.parse(wire)
console.log('honest copy valid:  ', verifyEvent(honest))

const tampered = JSON.parse(wire)
tampered.content = 'pay Mallory 1000 sats'
console.log('tampered copy valid:', verifyEvent(tampered))
```

```bash
node tamper.js
```

Expected output: `true` then `false`. A relay can drop your events, but it cannot change them without being caught. Ask the room: so what can a malicious relay still do?

### Step 5: Read notes back

```js
// read.js
import { SimplePool } from 'nostr-tools/pool'
import { verifyEvent } from 'nostr-tools/pure'
import * as nip19 from 'nostr-tools/nip19'
import { RELAYS } from './lib.js'

const pool = new SimplePool()
const filter = { kinds: [1], limit: 10 }

// Optional: pass an npub to only read that author's notes
if (process.argv[2]) filter.authors = [nip19.decode(process.argv[2]).data]

const events = await pool.querySync(RELAYS, filter)
events.sort((a, b) => b.created_at - a.created_at)

for (const e of events) {
  const who = nip19.npubEncode(e.pubkey).slice(0, 16)
  const when = new Date(e.created_at * 1000).toISOString()
  console.log(`[${when}] ${who}... valid=${verifyEvent(e)}\n  ${e.content.slice(0, 120)}\n`)
}
pool.close(RELAYS)
```

```bash
node read.js                 # latest notes from everyone
node read.js npub1...        # only one author (try your own, or a neighbour's)
```

The same with `nak`:

```bash
nak req -k 1 -l 5 wss://nos.lol
nak req -k 0 -a <hex pubkey> wss://nos.lol
```

Try other filters: `{ kinds: [1], '#t': ['nostrworkshop'] }` finds every note with the workshop hashtag. Ask everyone to post one and read the whole room's notes.

### Step 6: See the raw protocol

Libraries hide the wire format. Here it is with no library at all:

```js
// raw.js
import WebSocket from 'ws'

const url = process.env.RELAY || 'wss://relay.damus.io'
const ws = new WebSocket(url)

ws.on('open', () => {
  const req = ['REQ', 'my-sub', { kinds: [1], limit: 3 }]
  console.log('>>', JSON.stringify(req))
  ws.send(JSON.stringify(req))
})

ws.on('message', (data) => {
  const msg = JSON.parse(data)
  console.log('<<', JSON.stringify(msg).slice(0, 160))
  if (msg[0] === 'EOSE') {
    ws.send(JSON.stringify(['CLOSE', 'my-sub']))
    ws.close()
  }
})
```

```bash
node raw.js
```

Then look at a relay's information document (NIP-11). It is plain HTTP on the same address:

```bash
curl -H 'Accept: application/nostr+json' https://nos.lol
nak relay wss://nos.lol
```

Look at `supported_nips` and `limitation`. Different relays support different NIPs.

---

## Vibe coding prompts

Give one of these to your AI assistant. Paste your current code with it. **Do not paste your nsec.** The scripts read it from the environment, so the AI never needs it.

1. "Here is my `read.js` that uses nostr-tools. Change it to keep the subscription open with `pool.subscribe` and print new notes with the `#nostrworkshop` tag as they arrive."
2. "Write a script that fetches the kind 0 profile for an npub and prints name, about and picture. Handle missing fields and bad JSON."
3. "Write a script that publishes the same note to 10 relays and prints which ones accepted it, how long each took, and the rejection message for the others."
4. "Write a vanity npub miner: generate keys in a loop until the npub starts with `npub1` plus a 3 letter prefix I choose. Print attempts per second. Explain why each extra letter makes it about 32 times slower."
5. "Explain line by line how nostr-tools computes the event id. Then write my own `computeId(event)` with `@noble/hashes` and check it matches."

After the AI answers: run the code, read it, and check it against the NIP. AI tools often invent tag names or kinds. The NIP is the source of truth.

## Discussion questions

1. If you lose your `nsec`, what happens? If someone steals it, what happens? How is this different from a password?
2. A relay cannot forge your notes. What harm can a relay still do?
3. Why does a client publish to several relays? How does someone else know which relays to read you from? (Look up [NIP-65](https://github.com/nostr-protocol/nips/blob/master/65.md).)
4. Kind 0 is a "replaceable" event. What does that mean, and why is it useful for profiles?
5. Nostr uses the same curve and signature scheme as Bitcoin Taproot. What can you reuse from Bitcoin knowledge here, and what is different?

## Common problems and fixes

| Problem | Fix |
|---|---|
| `ReferenceError: WebSocket is not defined` | You skipped `lib.js` or did not import it. Node 20 needs the `ws` package passed to `useWebSocketImplementation`. |
| `Cannot use import statement outside a module` | Run `npm pkg set type=module`, or rename files to `.mjs`. |
| `Set NSEC first` | Run `export NSEC=nsec1...` in the same terminal window. New terminal windows forget it. |
| Publish shows `connection failure` or times out | That relay is down or blocked on this network. Remove it from `RELAYS`. If all fail, the venue may block WebSockets: use a phone hotspot or the facilitator's local relay. |
| Publish rejected with `blocked:` or `pow:` or `rate-limited:` | Some relays limit new keys or need proof of work. Read the message, then try another relay. |
| `read.js` prints nothing | Some relays return nothing for an empty filter or very old data. Add `limit`, try another relay, or check that your `authors` value is hex (decode the npub first). |
| `verifyEvent` says `true` after I edited an event | nostr-tools caches the result on the object. Make a fresh copy with `JSON.parse(JSON.stringify(event))` before you tamper, as in `tamper.js`. |
| Older tutorials use `relayInit` or `getSignature` | Those are nostr-tools v1 APIs. Use v2: `finalizeEvent`, `verifyEvent`, `SimplePool`. |

## Resources

- [NIP-01: Basic protocol flow](https://github.com/nostr-protocol/nips/blob/master/01.md) (events, kinds 0 and 1, filters, messages)
- [NIP-19: bech32 encoded entities](https://github.com/nostr-protocol/nips/blob/master/19.md) (`npub`, `nsec`, `note`, `nevent`, `nprofile`)
- [NIP-11: Relay information document](https://github.com/nostr-protocol/nips/blob/master/11.md)
- [NIP-65: Relay list metadata](https://github.com/nostr-protocol/nips/blob/master/65.md) (kind 10002)
- [All NIPs](https://github.com/nostr-protocol/nips)
- [nostr-tools](https://github.com/nbd-wtf/nostr-tools) (JavaScript library used in this module)
- [nak](https://github.com/fiatjaf/nak) (Nostr army knife CLI)
- [njump.me](https://njump.me) (view any event or profile in a browser)

Next: [Module 02: Building a Nostr Client from Scratch](../02-build-a-client/README.md)
