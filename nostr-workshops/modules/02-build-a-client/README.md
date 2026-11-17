# Module 02: Building a Nostr Client from Scratch

| | |
|---|---|
| **Duration** | 3 hours |
| **Level** | Beginner to intermediate (some JavaScript and HTML helps) |
| **You build** | A working browser client: live global feed, profile names, log in, post, reply, like, follow, and a Following feed |
| **Main NIPs** | [NIP-01](https://github.com/nostr-protocol/nips/blob/master/01.md), [NIP-07](https://github.com/nostr-protocol/nips/blob/master/07.md), [NIP-10](https://github.com/nostr-protocol/nips/blob/master/10.md), [NIP-25](https://github.com/nostr-protocol/nips/blob/master/25.md), [NIP-02](https://github.com/nostr-protocol/nips/blob/master/02.md), [NIP-19](https://github.com/nostr-protocol/nips/blob/master/19.md) |

[Back to the workshop series](../../README.md)

---

## What participants build

A single-page Nostr client in plain JavaScript (no framework), about 200 lines. It:

1. Streams the latest notes from three public relays.
2. Shows display names by fetching kind 0 profiles in batches.
3. Logs in with a NIP-07 browser extension, or falls back to a throwaway key for the workshop.
4. Posts notes, replies (NIP-10 threading tags) and likes (NIP-25 reactions).
5. Follows people (kind 3 contact list) and shows a Following feed.

Module 01 is helpful but not required. Concepts are recapped below.

## Prerequisites

- A laptop with a modern browser (Chrome, Firefox, Brave or Safari).
- [Node.js](https://nodejs.org) 20 or newer, for the Vite dev server.
- A code editor.
- Optional: a NIP-07 signer extension such as [nos2x](https://github.com/fiatjaf/nos2x) or [Alby](https://getalby.com). **Load it with a throwaway key, not your real one.**

## Safety rules

- Never paste a real `nsec` into a website, including the one you build today.
- The fallback login stores a throwaway key in the browser's `localStorage`. That is fine for a workshop and wrong for real users. We talk about why.
- The Follow button replaces your whole kind 3 follow list. Use a throwaway key. If you use a real key and the relays have an old copy of your list, you can lose your follows.

## Learning goals

After this module, participants can:

- Open subscriptions with filters and handle live events after `EOSE`.
- Explain why clients batch profile lookups and de-duplicate events from several relays.
- Sign events through NIP-07 (`window.nostr.getPublicKey()` and `window.nostr.signEvent()`) without ever touching the secret key.
- Build correct reply tags (NIP-10 `root` and `reply` markers) and reaction events (NIP-25 kind 7).
- Read and update a replaceable event (kind 3) safely.
- Render untrusted content safely (`textContent`, never `innerHTML`).

## Facilitator run sheet

| Time | Block | Notes |
|---|---|---|
| 0:00 | Welcome and demo | 10 min. Show the finished client. Read the safety rules. |
| 0:10 | How clients work | 15 min. Filters, subscriptions, `EOSE`, several relays, de-duplication. Recap keys and events for newcomers. |
| 0:25 | Step 1: scaffold the project | 15 min. Vite project running in every browser. |
| 0:40 | Steps 2 and 3: feed and profiles | 30 min. Biggest step. Pair people up. |
| 1:10 | Break | 10 min. |
| 1:20 | Step 4: log in and post | 25 min. Show NIP-07 with an extension on the projector. |
| 1:45 | Step 5: replies and likes | 25 min. Draw a thread on the board with root and reply markers. |
| 2:10 | Step 6: follow and Following feed | 20 min. Stress the replaceable-event warning. |
| 2:30 | Vibe coding extension | 20 min. Each pair picks one prompt. |
| 2:50 | Demos and discussion | 10 min. Two or three pairs show what they added. |

**Total: 3 hours.**

Facilitator prep: build the client once on the day. Test that all three relays respond from the venue. Keep a finished copy of `src/main.js` to share if someone falls far behind.

---

## How a client works (recap)

- A client is just a program that holds WebSocket connections to some relays.
- It sends `REQ` with a filter like `{ kinds: [1], limit: 30 }`. Relays send stored matches, then `EOSE`, then new matches live.
- The same event often arrives from several relays. Clients de-duplicate by `id`.
- Notes only contain the author's pubkey. To show a name, the client fetches the author's kind 0 profile, which is a separate event.
- To post, the client builds an event template and asks a signer to sign it. The signer can be a key in memory, a browser extension (NIP-07) or a remote bunker (NIP-46, see Module 05).

---

## Hands-on guide

### Step 1: Scaffold the project

```bash
npm create vite@latest my-nostr-client -- --template vanilla
cd my-nostr-client
npm install
npm install nostr-tools@2
```

Delete `src/counter.js` and any files under `src/assets/` you do not need. Replace `index.html` with:

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>My Nostr Client</title>
  </head>
  <body>
    <header>
      <h1>My Nostr Client</h1>
      <span id="whoami">Not logged in</span>
      <button id="login">Log in</button>
    </header>
    <section id="composer" hidden>
      <textarea id="text" rows="3" placeholder="Write a note"></textarea>
      <button id="post">Post</button>
    </section>
    <nav>
      <button id="tab-global">Global</button>
      <button id="tab-following">Following</button>
    </nav>
    <main id="feed"></main>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>
```

Replace `src/style.css` with:

```css
body { font-family: system-ui, sans-serif; max-width: 640px; margin: 0 auto; padding: 16px; }
header, nav { display: flex; gap: 8px; align-items: center; margin-bottom: 12px; }
header h1 { font-size: 1.2rem; margin-right: auto; }
textarea { width: 100%; box-sizing: border-box; }
article { border-bottom: 1px solid #ddd; padding: 10px 0; }
article .author { font-weight: 600; }
article time { color: #777; font-size: 0.8rem; margin-left: 8px; }
article p { white-space: pre-wrap; word-break: break-word; }
article footer { display: flex; gap: 6px; }
```

Start the dev server and open the URL it prints (usually `http://localhost:5173`):

```bash
npm run dev
```

### Step 2: Create the signer helper

Create `src/signer.js`. It returns an object with a `pubkey` and a `sign()` function, so the rest of the app does not care where the key lives.

```js
// src/signer.js
import { generateSecretKey, getPublicKey, finalizeEvent } from 'nostr-tools/pure'
import { bytesToHex, hexToBytes } from 'nostr-tools/utils'

// Returns { pubkey, sign(template), method }
export async function getSigner() {
  // NIP-07: a browser extension holds the key and signs for us
  if (window.nostr) {
    const pubkey = await window.nostr.getPublicKey()
    return { pubkey, sign: (t) => window.nostr.signEvent(t), method: 'NIP-07' }
  }

  // Fallback: a throwaway key stored in this browser only.
  // Fine for a workshop. Never do this with a key you care about.
  let hex = localStorage.getItem('workshop-throwaway-key')
  if (!hex) {
    hex = bytesToHex(generateSecretKey())
    localStorage.setItem('workshop-throwaway-key', hex)
  }
  const sk = hexToBytes(hex)
  return { pubkey: getPublicKey(sk), sign: async (t) => finalizeEvent(t, sk), method: 'throwaway key' }
}
```

### Step 3: The feed and profiles

Replace `src/main.js` with this. Read the comments together before running it.

```js
// src/main.js
import './style.css'
import { SimplePool } from 'nostr-tools/pool'
import * as nip19 from 'nostr-tools/nip19'
import { getSigner } from './signer.js'

const RELAYS = ['wss://relay.damus.io', 'wss://nos.lol', 'wss://relay.primal.net']
const pool = new SimplePool()
const feedEl = document.querySelector('#feed')

const profiles = new Map()    // pubkey -> parsed kind 0 content
const requested = new Set()   // pubkeys we already asked for
const seen = new Set()        // event ids already on screen
let noteActions = () => []    // buttons under each note, filled in later
let currentSub = null

function shortKey(pubkey) {
  return nip19.npubEncode(pubkey).slice(0, 14) + '...'
}

function displayName(pubkey) {
  const p = profiles.get(pubkey)
  return p?.display_name || p?.name || shortKey(pubkey)
}

function renderNote(event) {
  if (seen.has(event.id)) return
  seen.add(event.id)

  const el = document.createElement('article')
  el.dataset.pubkey = event.pubkey
  el.dataset.createdAt = event.created_at

  const author = document.createElement('span')
  author.className = 'author'
  author.textContent = displayName(event.pubkey)

  const time = document.createElement('time')
  time.textContent = new Date(event.created_at * 1000).toLocaleString()

  // textContent, never innerHTML: note content is untrusted input
  const body = document.createElement('p')
  body.textContent = event.content

  const footer = document.createElement('footer')
  footer.append(...noteActions(event))

  el.append(author, time, body, footer)

  // Keep the newest notes at the top
  const older = [...feedEl.children].find((c) => Number(c.dataset.createdAt) < event.created_at)
  feedEl.insertBefore(el, older || null)

  requestProfile(event.pubkey)
}

// Profiles (kind 0): collect pubkeys for 300 ms, then fetch them in one query
let profileTimer = null
function requestProfile(pubkey) {
  if (requested.has(pubkey)) return
  requested.add(pubkey)
  clearTimeout(profileTimer)
  profileTimer = setTimeout(loadProfiles, 300)
}

const loadedAt = new Map()
async function loadProfiles() {
  const authors = [...requested].filter((pk) => !loadedAt.has(pk))
  if (authors.length === 0) return
  const events = await pool.querySync(RELAYS, { kinds: [0], authors })
  for (const e of events) {
    if ((loadedAt.get(e.pubkey) || 0) >= e.created_at) continue // keep the newest
    try {
      profiles.set(e.pubkey, JSON.parse(e.content))
      loadedAt.set(e.pubkey, e.created_at)
    } catch {
      // bad JSON in someone's profile: ignore it
    }
  }
  for (const el of feedEl.querySelectorAll('article')) {
    el.querySelector('.author').textContent = displayName(el.dataset.pubkey)
  }
}

function showFeed(filter) {
  currentSub?.close()
  feedEl.replaceChildren()
  seen.clear()
  currentSub = pool.subscribe(RELAYS, filter, {
    onevent: renderNote,
    oneose: () => console.log('caught up with stored events, now live'),
  })
}

document.querySelector('#tab-global').onclick = () => showFeed({ kinds: [1], limit: 30 })
showFeed({ kinds: [1], limit: 30 })
```

Save. The browser reloads and notes start to stream in. Names replace the `npub1...` placeholders a moment later.

Talk about it:

- Why is `seen` needed? (The same note arrives from up to three relays.)
- Why batch profiles instead of one query per note? (Relays limit open subscriptions. Thirty queries for thirty notes is rude and slow.)
- Why does the app keep the profile with the highest `created_at`? (Kind 0 is replaceable. Relays may hold old versions.)

### Step 4: Log in and post

Add this to the **end** of `src/main.js`:

```js
// ---- Step 4: log in and post ----
let me = null

document.querySelector('#login').onclick = async () => {
  me = await getSigner()
  requestProfile(me.pubkey)
  document.querySelector('#whoami').textContent = `${shortKey(me.pubkey)} (${me.method})`
  document.querySelector('#composer').hidden = false
}

async function publish(template) {
  const event = await me.sign({
    created_at: Math.floor(Date.now() / 1000),
    tags: [],
    ...template,
  })
  const results = await Promise.allSettled(pool.publish(RELAYS, event))
  const ok = results.filter((r) => r.status === 'fulfilled').length
  console.log(`published kind ${event.kind} to ${ok}/${RELAYS.length} relays`, event)
  return event
}

document.querySelector('#post').onclick = async () => {
  const textEl = document.querySelector('#text')
  const content = textEl.value.trim()
  if (!content) return
  const event = await publish({ kind: 1, content })
  renderNote(event)
  textEl.value = ''
}
```

Click **Log in**. With a NIP-07 extension installed, the extension asks for permission. Without one, you get a throwaway key. Post a note, then open the browser console to see the signed event and how many relays accepted it.

Notice that with NIP-07 the page never sees the secret key. It only sees the public key and signed events.

### Step 5: Replies and likes

Add this to the end of `src/main.js`:

```js
// ---- Step 5: replies (NIP-10) and reactions (NIP-25) ----
function button(label, onclick) {
  const b = document.createElement('button')
  b.textContent = label
  b.onclick = async () => {
    if (!me) return alert('Log in first')
    await onclick(b)
  }
  return b
}

noteActions = (event) => [
  button('Reply', async () => {
    const content = prompt('Your reply')
    if (!content) return
    const root = event.tags.find((t) => t[0] === 'e' && t[3] === 'root')
    const tags = root
      ? [['e', root[1], root[2] || '', 'root'], ['e', event.id, '', 'reply']]
      : [['e', event.id, '', 'root']]
    tags.push(['p', event.pubkey])
    await publish({ kind: 1, content, tags })
  }),
  button('Like', async (b) => {
    await publish({
      kind: 7,
      content: '+',
      tags: [['e', event.id], ['p', event.pubkey], ['k', String(event.kind)]],
    })
    b.disabled = true
  }),
]
```

Save. The page reloads and every note now has **Reply** and **Like** buttons. The reload logs you out, so click **Log in** again (with the throwaway key you get the same key back from `localStorage`).

How the reply tags work (NIP-10):

- Replying to a top-level note: one `e` tag with the note id and the marker `root`.
- Replying to a reply: keep the thread's `root` tag and add an `e` tag for the note you answer, marked `reply`.
- A `p` tag for the author you answer, so their client can notify them.

A like is a kind 7 event with content `+`, an `e` tag for the note and a `p` tag for its author (NIP-25).

### Step 6: Follow people and a Following feed

Add this to the end of `src/main.js`:

```js
// ---- Step 6: follow list (kind 3) and a Following feed ----
async function getFollows() {
  const list = await pool.get(RELAYS, { kinds: [3], authors: [me.pubkey] })
  return list
}

const baseActions = noteActions
noteActions = (event) => [
  ...baseActions(event),
  button('Follow', async (b) => {
    const list = await getFollows()
    const tags = list ? list.tags : []
    if (!tags.some((t) => t[0] === 'p' && t[1] === event.pubkey)) {
      // Kind 3 replaces the whole list, so we must re-send every existing tag
      await publish({ kind: 3, content: list?.content || '', tags: [...tags, ['p', event.pubkey]] })
    }
    b.textContent = 'Following'
    b.disabled = true
  }),
]

document.querySelector('#tab-following').onclick = async () => {
  if (!me) return alert('Log in first')
  const list = await getFollows()
  const follows = list ? list.tags.filter((t) => t[0] === 'p').map((t) => t[1]) : []
  if (follows.length === 0) return alert('You do not follow anyone yet')
  showFeed({ kinds: [1], authors: follows, limit: 50 })
}
```

Follow a few people (or your neighbours' throwaway keys), then click **Following**.

Discuss the danger here: kind 3 is replaceable. Every update must contain the full list. If a relay hands you an old list, you overwrite newer follows. Real clients compare `created_at` across all relays and warn before publishing a much shorter list.

You now have a working Nostr client.

---

## Vibe coding prompts

Pick one. Paste `src/main.js` along with the prompt. Never paste a real `nsec`.

1. "Add a profile view: when I click an author name, show their kind 0 picture, name and about, and only their notes."
2. "Show reply counts and like counts under each note. Use one batched query for kind 1 and kind 7 events with an `#e` filter for all visible note ids."
3. "Render `nostr:npub1...` and `nostr:note1...` mentions in note content as links (NIP-21 and NIP-27), and show image URLs as images. Keep it safe: no `innerHTML` with raw content."
4. "Use NIP-65: after login, fetch my kind 10002 relay list and use those relays for publishing instead of the hard-coded ones."
5. "Add a thread view: clicking a note loads every kind 1 event that tags it with `#e`, and indents replies using the NIP-10 root and reply markers."
6. "Add infinite scroll: when I reach the bottom, query older notes with `until` set to the oldest `created_at` on screen."

Check what the AI wrote against the NIP it claims to implement. Watch for invented tags and for code that uses `innerHTML` with note content.

## Discussion questions

1. Our app trusts three hard-coded relays. What breaks if one of them goes down or starts censoring? How does NIP-65 (the "outbox model") fix this?
2. Why is storing a secret key in `localStorage` dangerous? What attacks does NIP-07 protect against, and which does it not?
3. Kind 3 follow lists are replaceable. What other data would you want to be replaceable? What would you never want to be?
4. Notes are untrusted input from strangers. What could go wrong if we used `innerHTML`?
5. A "like" is a public signed event. What does that mean for privacy?

## Common problems and fixes

| Problem | Fix |
|---|---|
| Blank page, error about `nostr-tools/pool` | Run `npm install nostr-tools@2` inside the project folder, then restart `npm run dev`. |
| Feed stays empty | Open the console. If every relay fails, the network may block WebSockets. Try a phone hotspot, or change `RELAYS`. |
| Names never appear | Some people have no kind 0 on these relays. That is normal. If no names appear at all, check the console for errors in `loadProfiles`. |
| Login button does nothing with an extension installed | Some extensions inject `window.nostr` a moment after the page loads. Reload the page and wait a second before clicking. Check the extension allows this site. |
| Post shows `0/3 relays` | Relays may reject brand new keys or rate-limit. Read the rejection in the console. Try a different relay. |
| Reply and Like buttons missing | Check that Step 5 assigns `noteActions = ...` without `let` in front. Writing `let noteActions` a second time is a syntax error. |
| `SyntaxError: Identifier 'x' has already been declared` | You pasted a step twice. Each step's code goes in once, at the end of the file. |
| Old tutorials pass an array of filters | In current nostr-tools v2, `pool.subscribe(relays, filter, params)` takes one filter object. |

## Resources

- [NIP-01: Basic protocol](https://github.com/nostr-protocol/nips/blob/master/01.md)
- [NIP-02: Follow list](https://github.com/nostr-protocol/nips/blob/master/02.md) (kind 3)
- [NIP-07: `window.nostr` for web browsers](https://github.com/nostr-protocol/nips/blob/master/07.md)
- [NIP-10: Text notes and threads](https://github.com/nostr-protocol/nips/blob/master/10.md)
- [NIP-19: bech32 entities](https://github.com/nostr-protocol/nips/blob/master/19.md)
- [NIP-21: `nostr:` URI scheme](https://github.com/nostr-protocol/nips/blob/master/21.md)
- [NIP-25: Reactions](https://github.com/nostr-protocol/nips/blob/master/25.md)
- [NIP-65: Relay list metadata](https://github.com/nostr-protocol/nips/blob/master/65.md)
- [nostr-tools](https://github.com/nbd-wtf/nostr-tools)
- [Vite](https://vite.dev)

Previous: [Module 01](../01-nostr-basics/README.md) | Next: [Module 03: Lightning Integration: Zaps and NWC](../03-zaps-and-nwc/README.md)
