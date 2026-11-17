# Module 05: Nostr for Identity and Authentication

| | |
|---|---|
| **Duration** | 2 hours |
| **Level** | Intermediate (JavaScript and basic HTTP) |
| **You build** | A small Node.js server with a NIP-05 identity endpoint and a "Log in with Nostr" API (NIP-98), plus scripts that sign through a remote bunker (NIP-46) and authenticate to a relay (NIP-42) |
| **Main NIPs** | [NIP-05](https://github.com/nostr-protocol/nips/blob/master/05.md), [NIP-07](https://github.com/nostr-protocol/nips/blob/master/07.md), [NIP-98](https://github.com/nostr-protocol/nips/blob/master/98.md), [NIP-46](https://github.com/nostr-protocol/nips/blob/master/46.md), [NIP-42](https://github.com/nostr-protocol/nips/blob/master/42.md) |

[Back to the workshop series](../../README.md)

---

## What participants build

1. **NIP-05:** a `/.well-known/nostr.json` endpoint that maps `name@yourdomain` to a pubkey.
2. **NIP-98:** an HTTP API that knows who you are from a signed Nostr event in the `Authorization` header. No passwords, no email, no OAuth provider. It includes a browser login page that signs with a NIP-07 extension, and a command-line client.
3. **NIP-46:** a script that signs events with a key held by a separate "bunker" process, so the app never sees the secret key.
4. **NIP-42:** a script that authenticates to a relay that requires login.

## Prerequisites

- A laptop with [Node.js](https://nodejs.org) 20 or newer.
- The [`nak`](https://github.com/fiatjaf/nak) CLI ([releases page](https://github.com/fiatjaf/nak/releases), or `go install github.com/fiatjaf/nak@latest`).
- Optional: a NIP-07 browser extension such as [nos2x](https://github.com/fiatjaf/nos2x) or [Alby](https://getalby.com), **loaded with a throwaway key**.
- Optional: a domain you control, to try NIP-05 for real after the workshop.

## Safety rules

- Use throwaway keys only. Never paste a real `nsec` into a website, a terminal on a shared screen, or an AI chat.
- `nak bunker` prints the secret key it uses in its startup output (so you can restart it). Do not run it with a real key while screen sharing.
- A `bunker://` URL with a `secret` lets an app connect to your signer. Treat it like a one-time password.

## Learning goals

After this module, participants can:

- Explain the difference between a Nostr identity (the key) and the names, domains and signers around it.
- Serve and verify a NIP-05 identifier, and explain what it does and does not prove.
- Build passwordless login for a web API with NIP-98 (kind 27235), including URL, method, time window and replay checks.
- Explain where a key can live: in the app, in a browser extension (NIP-07), or in a remote signer (NIP-46).
- Handle a relay that requires NIP-42 `AUTH` (kind 22242).

## Facilitator run sheet

| Time | Block | Notes |
|---|---|---|
| 0:00 | Welcome and safety | 10 min. Read the safety rules. |
| 0:10 | Concepts: the key is the identity | 15 min. Draw the map of the five NIPs below. |
| 0:25 | Steps 1 and 2: NIP-05 | 20 min. Serve `nostr.json` locally. Show a real NIP-05 lookup with `curl`. |
| 0:45 | Steps 3 and 4: NIP-98 login | 25 min. Browser login with an extension on the projector, then the CLI client. |
| 1:10 | Step 5: NIP-46 bunker | 20 min. Pairs: one runs the bunker, the other runs the app. |
| 1:30 | Step 6: NIP-42 relay AUTH | 10 min. |
| 1:40 | Vibe coding extension | 10 min. |
| 1:50 | Discussion and wrap-up | 10 min. |

**Total: 2 hours.**

Facilitator prep: install a NIP-07 extension with a throwaway key in your demo browser. Run every step once on the venue network. If the network blocks WebSockets, run `nak serve` on your laptop and have everyone use `ws://<your-ip>:10547` as the relay in Steps 5 and 6.

---

## Concepts: the key is the identity

On Nostr your identity is your public key. Everything else is a convenience around it:

| Need | NIP | What it does |
|---|---|---|
| A human-readable name | NIP-05 | `alice@example.com` points to a pubkey through `https://example.com/.well-known/nostr.json?name=alice` |
| Sign in a web page without giving it your key | NIP-07 | A browser extension exposes `window.nostr.getPublicKey()` and `window.nostr.signEvent()` |
| Sign from another device or server | NIP-46 | A "bunker" holds the key and signs on request, over encrypted Nostr messages |
| Log in to an HTTP API | NIP-98 | Send a signed kind 27235 event in the `Authorization` header |
| Log in to a relay | NIP-42 | The relay sends a challenge, the client answers with a signed kind 22242 event |

Note what NIP-05 does **not** do. It does not prove you are a person, or that you own a brand. It proves that whoever controls `example.com` says this pubkey is `alice`. The key is still the identity. If the domain owner changes the file, clients should stop showing the name.

---

## Hands-on guide

### Step 0: Project setup

```bash
mkdir nostr-identity && cd nostr-identity
npm init -y
npm pkg set type=module
npm install nostr-tools@2 ws
```

Create `lib.js`:

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

Make a throwaway key and note its hex pubkey:

```bash
SK=$(nak key generate)
nak key public $SK               # hex pubkey, used in server.js
export NSEC=$(nak encode nsec $SK)
```

### Step 1: The identity server

This one file serves NIP-05 and a NIP-98 protected API. Create `server.js`:

```js
// server.js
import http from 'node:http'
import * as nip98 from 'nostr-tools/nip98'
import * as nip19 from 'nostr-tools/nip19'

const PORT = 3000
// The exact public URL clients use. It must match the "u" tag they sign.
const PUBLIC_URL = process.env.PUBLIC_URL || `http://localhost:${PORT}`

// NIP-05: name -> hex pubkey. Put your own throwaway pubkey here.
const NAMES = {
  _: 'replace-with-your-hex-pubkey', // _ means name@domain shows as just domain
  alice: 'replace-with-your-hex-pubkey',
}

const seenAuthEvents = new Set() // event ids already used, to block replays

const page = `<!doctype html>
<html><head><meta charset="utf-8"><title>Log in with Nostr</title></head>
<body>
  <h1>Log in with Nostr</h1>
  <button id="login">Log in with my extension (NIP-07)</button>
  <pre id="out"></pre>
  <script>
    document.querySelector('#login').onclick = async () => {
      if (!window.nostr) return alert('Install a NIP-07 extension first')
      const url = location.origin + '/api/me'
      // NIP-98: sign a kind 27235 event that names the URL and method
      const event = await window.nostr.signEvent({
        kind: 27235,
        created_at: Math.floor(Date.now() / 1000),
        tags: [['u', url], ['method', 'GET']],
        content: '',
      })
      const res = await fetch(url, { headers: { Authorization: 'Nostr ' + btoa(JSON.stringify(event)) } })
      document.querySelector('#out').textContent = res.status + ' ' + await res.text()
    }
  </script>
</body></html>`

function send(res, status, body, type = 'application/json') {
  res.writeHead(status, { 'Content-Type': type, 'Access-Control-Allow-Origin': '*' })
  res.end(typeof body === 'string' ? body : JSON.stringify(body))
}

http.createServer(async (req, res) => {
  const url = new URL(req.url, PUBLIC_URL)

  // NIP-05 lookup: GET /.well-known/nostr.json?name=alice
  if (url.pathname === '/.well-known/nostr.json') {
    const name = url.searchParams.get('name')
    const names = name ? (NAMES[name] ? { [name]: NAMES[name] } : {}) : NAMES
    return send(res, 200, { names })
  }

  // Protected API: needs a valid NIP-98 Authorization header
  if (url.pathname === '/api/me') {
    try {
      const header = req.headers.authorization
      await nip98.validateToken(header, PUBLIC_URL + req.url, req.method) // throws if invalid
      const event = await nip98.unpackEventFromToken(header)
      if (seenAuthEvents.has(event.id)) throw new Error('this auth event was already used')
      seenAuthEvents.add(event.id)
      return send(res, 200, { hello: nip19.npubEncode(event.pubkey) })
    } catch (err) {
      return send(res, 401, { error: err.message })
    }
  }

  if (url.pathname === '/') return send(res, 200, page, 'text/html')
  send(res, 404, { error: 'not found' })
}).listen(PORT, () => console.log(`listening on ${PUBLIC_URL}`))
```

Put your hex pubkey into `NAMES`, then start it:

```bash
node server.js
```

### Step 2: NIP-05 identifiers

In a second terminal:

```bash
curl 'http://localhost:3000/.well-known/nostr.json?name=alice'
```

You get `{"names":{"alice":"<your hex pubkey>"}}`. That is all NIP-05 is. To use it for real:

1. Serve the same JSON at `https://yourdomain/.well-known/nostr.json` over **HTTPS**.
2. Send the header `Access-Control-Allow-Origin: *`, or web clients cannot read it.
3. Put `"nip05": "alice@yourdomain"` in your kind 0 profile.

Clients then fetch the file, check the pubkey matches the profile's author, and show a checkmark. Look at a real one: pick someone in a Nostr app who shows a NIP-05 name, then:

```bash
curl 'https://<their domain>/.well-known/nostr.json?name=<their name>'
nak decode <name>@<domain>
```

Optional relay hints can go in a `relays` object in the same file, keyed by pubkey. See NIP-05.

### Step 3: Log in with Nostr in the browser (NIP-98 with NIP-07)

Open `http://localhost:3000` in the browser that has your NIP-07 extension. Click the button. The extension asks you to sign a kind 27235 event. The page sends it to `/api/me` and shows:

```
200 {"hello":"npub1..."}
```

What the server checked, in `nip98.validateToken`:

- The signature is valid.
- The kind is 27235.
- `created_at` is within about 60 seconds of now.
- The `u` tag equals the exact URL requested.
- The `method` tag equals the HTTP method.

And our own extra check: the same event cannot be used twice (replay protection).

No extension? Do Step 4 instead. It does the same thing from the command line.

### Step 4: Log in from the command line

```js
// client.js
import { finalizeEvent } from 'nostr-tools/pure'
import * as nip98 from 'nostr-tools/nip98'
import { loadSecretKey } from './lib.js'

const sk = loadSecretKey()
const url = process.env.API_URL || 'http://localhost:3000/api/me'

const header = await nip98.getToken(url, 'GET', (e) => finalizeEvent(e, sk), true)
console.log('Authorization:', header.slice(0, 60) + '...')

const first = await fetch(url, { headers: { Authorization: header } })
console.log('first try:', first.status, await first.text())

const replay = await fetch(url, { headers: { Authorization: header } })
console.log('replay:   ', replay.status, await replay.text())

const none = await fetch(url)
console.log('no header:', none.status, await none.text())
```

```bash
node client.js
```

Expected output: `200` for the first try, `401 ... already used` for the replay, `401 Missing token` with no header. `nak` can do the same: `nak curl` adds a NIP-98 header to a normal `curl` call (run `nak curl --help`).

Talk about it: this login needs no database of users and no passwords. What does the server need to store, and what does it still need to decide on its own (for example, which pubkeys are admins)?

### Step 5: Remote signing with a bunker (NIP-46)

With NIP-46 the secret key lives in a separate signer (the "bunker"): a phone app, a hardware device, a server, or here, `nak`. Apps get a `bunker://` URL and ask the bunker to sign over encrypted Nostr messages.

Work in pairs. **Person A** runs the bunker with a throwaway key:

```bash
nak bunker --sec $(nak key generate) wss://nos.lol
```

It prints a line starting with `bunker://...`. Person A sends that line to Person B. (Any relay works. If the venue blocks outside relays, use the facilitator's `ws://<ip>:10547`.)

**Person B** runs the app side:

```js
// bunker.js
import { generateSecretKey } from 'nostr-tools/pure'
import { BunkerSigner, parseBunkerInput } from 'nostr-tools/nip46'
import { SimplePool } from 'nostr-tools/pool'
import * as nip19 from 'nostr-tools/nip19'
import './lib.js' // WebSocket for Node

// Usage: node bunker.js "bunker://..."
const pointer = await parseBunkerInput(process.argv[2])
if (!pointer) throw new Error('not a valid bunker:// URL')

// This app gets its own key. It only talks to the bunker, it never holds the user's key.
const clientSk = generateSecretKey()
const pool = new SimplePool()
const signer = BunkerSigner.fromBunker(clientSk, pointer, { pool })

await signer.connect()
const pubkey = await signer.getPublicKey()
console.log('connected as', nip19.npubEncode(pubkey))

const event = await signer.signEvent({
  kind: 1,
  created_at: Math.floor(Date.now() / 1000),
  tags: [],
  content: 'Signed by a remote bunker (NIP-46)',
})
console.log('signed event:', event.id, 'by', event.pubkey === pubkey ? 'the right key' : 'WRONG KEY')

await signer.close()
pool.close(pointer.relays)
```

```bash
node bunker.js "bunker://..."
```

Person A watches the bunker log each request. Swap roles. Note: `nak` itself can use a bunker as its signer: `nak event --sec "bunker://..." -c "hi" wss://nos.lol`.

Discuss: the app holds `clientSk`, a key that is only good for talking to the bunker. If the app is hacked, what can the attacker do? How would you revoke access?

### Step 6: Relays that require login (NIP-42)

Start a local relay that requires `AUTH`:

```bash
nak serve --auth --port 10548
```

```js
// auth.js
import { SimplePool } from 'nostr-tools/pool'
import { finalizeEvent } from 'nostr-tools/pure'
import { loadSecretKey } from './lib.js'

const sk = loadSecretKey()
const RELAY = process.env.RELAY || 'ws://localhost:10548'
const pool = new SimplePool()
const note = (content) =>
  finalizeEvent({ kind: 1, created_at: Math.floor(Date.now() / 1000), tags: [], content }, sk)

// 1. Without AUTH: the relay refuses with "auth-required: ..."
const [first] = await Promise.allSettled(pool.publish([RELAY], note('no auth')))
console.log('without AUTH:', first.status, first.reason?.message || '')

// 2. With AUTH: on "auth-required", sign the relay's challenge as a kind 22242 event
const onauth = async (authTemplate) => {
  console.log('signing AUTH event, challenge =', authTemplate.tags.find((t) => t[0] === 'challenge')[1])
  return finalizeEvent(authTemplate, sk)
}
const [second] = await Promise.allSettled(pool.publish([RELAY], note('hello, authenticated'), { onauth }))
console.log('with AUTH:', second.status, second.reason?.message || '')

// 3. This connection is now authenticated, so reading works too
const events = await pool.querySync([RELAY], { kinds: [1], limit: 5 })
console.log('read back', events.length, 'event(s)')
pool.close([RELAY])
```

```bash
node auth.js
```

Expected: `rejected auth-required: ...`, then the challenge, then `fulfilled`, then `read back 1 event(s)`. The kind 22242 AUTH event is never stored or forwarded. It only proves to this relay, on this connection, which key you control. Relays use it for paid access, private groups and direct-message privacy.

---

## Vibe coding prompts

Paste the file you are changing. Never paste a real `nsec`.

1. "Turn `server.js` into a tiny members-only notes API: `POST /api/notes` saves a note for the authenticated pubkey (NIP-98 with a `payload` hash of the JSON body), and `GET /api/notes` returns only that pubkey's notes."
2. "Add NIP-05 self-registration to `server.js`: an authenticated `POST /api/register` with `{ name }` adds `name -> pubkey` to `NAMES` and saves it to a JSON file. Reject names that are taken or not lowercase a-z, 0-9, dash, dot and underscore."
3. "Write a browser page that logs in with a `bunker://` URL using `BunkerSigner` from nostr-tools, as an alternative to NIP-07."
4. "Write `verify-nip05.js`: given `name@domain`, fetch `nostr.json`, fetch the pubkey's kind 0 profile from relays, and report whether the profile's `nip05` field matches. Use `nostr-tools/nip05`."
5. "Explain the `nostrconnect://` flow in NIP-46, where the app shows a QR code and the signer connects to it. Then write it with `BunkerSigner.fromURI`."

## Discussion questions

1. NIP-05 names depend on DNS and a web server. Is that a step back toward central control? What happens if the domain owner changes the file?
2. Compare NIP-98 login with "Sign in with Google". What do you gain? What do you lose (account recovery, for example)?
3. Where should a normal user's key live: in an extension, a phone signer app, a hardware device, or a hosted bunker? What are the trade-offs?
4. NIP-42 lets a relay know who is reading. Is that good or bad for privacy? When is it worth it?
5. If keys can never be rotated, how should Nostr handle a stolen key? What ideas have people proposed?

## Common problems and fixes

| Problem | Fix |
|---|---|
| `401 url tag invalid` | The URL you signed is not exactly the URL the server checks. Behind a proxy or with a different host name, set `PUBLIC_URL` to the address clients really use, including `https://` and port. |
| `401 created_at timestamp invalid` | Your computer clock is off by more than a minute, or the token is old. Sync your clock and sign a fresh event. |
| `401 method tag invalid` | You signed `GET` but sent `POST` (or the other way round). |
| Browser login: "Install a NIP-07 extension first" | No extension, or it has not loaded yet. Reload, check the extension allows `localhost`, or use `client.js`. |
| NIP-05 works with curl but not in Nostr apps | Use HTTPS, add `Access-Control-Allow-Origin: *`, and check the pubkey is **hex**, not npub. On GitHub Pages, add an empty `.nojekyll` file so the `.well-known` folder is published. |
| `bunker.js` hangs on `connect()` | Both sides must reach the same relay. Check the `relay=` in the bunker URL, and that the bunker is still running. |
| `Error: unauthorized` when a second person uses the same `bunker://` URL | The `secret` in the URL is single-use: the first app that connects claims it. Restart the bunker to get a fresh URL. |
| `auth.js` never authenticates | The relay may send `AUTH` only when needed. Pass `onauth` to `publish` or `subscribe` as shown. `automaticallyAuth` in the pool options only answers challenges the relay sends on connect. |

## Resources

- [NIP-05: Mapping Nostr keys to DNS-based internet identifiers](https://github.com/nostr-protocol/nips/blob/master/05.md)
- [NIP-07: `window.nostr` capability for web browsers](https://github.com/nostr-protocol/nips/blob/master/07.md)
- [NIP-98: HTTP Auth](https://github.com/nostr-protocol/nips/blob/master/98.md) (kind 27235)
- [NIP-46: Nostr Remote Signing](https://github.com/nostr-protocol/nips/blob/master/46.md) (`bunker://` and `nostrconnect://`)
- [NIP-42: Authentication of clients to relays](https://github.com/nostr-protocol/nips/blob/master/42.md) (kind 22242)
- [nostr-tools](https://github.com/nbd-wtf/nostr-tools) (`nip05`, `nip46`, `nip98` helpers)
- [nak](https://github.com/fiatjaf/nak) (`nak bunker`, `nak serve --auth`, `nak curl`)
- [nos2x](https://github.com/fiatjaf/nos2x) (minimal NIP-07 browser extension)

Previous: [Module 04](../04-run-a-relay/README.md) | Next: [Module 06: Building on NIP-90 (Data Vending Machines)](../06-data-vending-machines/README.md)
