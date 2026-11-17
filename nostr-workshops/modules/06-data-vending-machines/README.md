# Module 06: Building on NIP-90 (Data Vending Machines)

| | |
|---|---|
| **Duration** | 3 hours |
| **Level** | Intermediate to advanced (comfortable with async JavaScript; Module 03 helps for the payment step) |
| **You build** | A working Data Vending Machine (DVM) that takes jobs from Nostr, does work, and publishes results, plus a customer script, NIP-89 discovery, and optional Lightning payment |
| **Main NIPs** | [NIP-90](https://github.com/nostr-protocol/nips/blob/master/90.md) (DVMs), [NIP-89](https://github.com/nostr-protocol/nips/blob/master/89.md) (handler announcements), [NIP-47](https://github.com/nostr-protocol/nips/blob/master/47.md) (NWC, for payments) |

[Back to the workshop series](../../README.md)

---

## What participants build

1. `dvm.js`: a service that listens for **kind 5001** (summarization) job requests, sends **kind 7000** status feedback, and publishes **kind 6001** results. It announces itself with a NIP-89 **kind 31990** event.
2. `customer.js`: sends a job and prints feedback and results from any DVM that answers.
3. Optional: a paid mode. The DVM asks for sats with a Lightning invoice (made through NWC) and only works after it is paid. The customer pays automatically through NWC.

The summarizer is deliberately simple (first two sentences plus a word count). The point is the protocol. In the vibe coding block you swap in something smarter, such as a local language model.

## Prerequisites

- A laptop with [Node.js](https://nodejs.org) 20 or newer.
- The [`nak`](https://github.com/fiatjaf/nak) CLI ([releases page](https://github.com/fiatjaf/nak/releases), or `go install github.com/fiatjaf/nak@latest`).
- For the optional payment step: a Lightning wallet with **Nostr Wallet Connect** and a few hundred sats. See [Module 03](../03-zaps-and-nwc/README.md).

## Safety rules

- Use throwaway keys for both the DVM and the customer. Never paste a real `nsec` anywhere.
- Job requests and results are public events by default. Do not send private data to a DVM.
- Your DVM processes input from strangers. Never run job input as code, never fetch arbitrary URLs from your server without limits, and cap input size.
- For paid jobs, use a test wallet with a small budget. NWC connection strings are secrets.

## Learning goals

After this module, participants can:

- Explain the NIP-90 job market: customers post requests (kinds 5000-5999), service providers answer with results (kinds 6000-6999, request kind + 1000) and feedback (kind 7000).
- Read and build the standard job tags: `i` (input with type `text`, `event`, `url` or `job`), `output`, `param`, `bid`, `relays`, `p`.
- Write a DVM that de-duplicates jobs, respects a targeted `p` tag, reports status, and handles errors.
- Make a DVM discoverable with a NIP-89 kind 31990 announcement.
- Add a payment step with `payment-required` feedback and an `amount` tag carrying a bolt11 invoice.

## Facilitator run sheet

| Time | Block | Notes |
|---|---|---|
| 0:00 | Welcome and safety | 10 min. Show the finished DVM answering a job on the projector. |
| 0:10 | Concepts: the DVM market | 20 min. Draw the flow below. Show the job kinds list. |
| 0:30 | Step 1: be a customer with `nak` | 15 min. Everyone sends a job to the facilitator's running DVM. |
| 0:45 | Steps 2 and 3: build the DVM | 40 min. The main build. Pair people up. |
| 1:25 | Break | 10 min. |
| 1:35 | Step 4: the customer script, swap DVMs | 20 min. Everyone's DVM answers everyone's jobs. Then target one DVM with `p`. |
| 1:55 | Step 5: discovery with NIP-89 | 15 min. List every DVM in the room. |
| 2:10 | Step 6: paid jobs (optional) | 20 min. Pairs with a funded wallet try it. Others watch the facilitator demo. |
| 2:30 | Vibe coding extension | 20 min. |
| 2:50 | Demos and discussion | 10 min. |

**Total: 3 hours.**

Facilitator prep: run your own DVM before the session starts and keep it running. Post a test job to it from the venue network. When the whole room runs DVMs on the same public relays, every DVM answers every job. That is fun for a few minutes and then noisy, so in Step 4 move people to targeted jobs (`DVM=npub1...`). If public relays rate-limit the room, run `nak serve` on your laptop and give everyone `RELAYS=ws://<your-ip>:10547`.

---

## Concepts: how a DVM works

```
Customer                         Relays                         DVM (service provider)
   |                               |                                   |
   | kind 5001 job request ------->|---------------------------------->| (subscribed to kind 5001)
   |   i: input, output: mime,     |                                   |
   |   relays, bid, p (optional)   |                                   |
   |                               |<-- kind 7000 feedback ------------|  status: processing
   |<------------------------------|    (or payment-required + invoice)|
   |                               |                                   |  ...does the work...
   |                               |<-- kind 6001 result --------------|
   |<------------------------------|    content: output                |
   |                               |    tags: request, e, p, i         |
```

- **Job request (kinds 5000-5999).** Each kind is a type of job. Examples: 5000 text extraction, 5001 summarization, 5002 translation, 5050 text generation, 5100 image generation, 5300 content discovery. The registry lives in the [data-vending-machines](https://github.com/nostr-protocol/data-vending-machines) repo.
- **Input tag `i`.** `["i", "<data>", "<type>", "<relay>", "<marker>"]`. The type is `text` (the data itself), `event` (an event id to fetch), `url` (a URL to fetch) or `job` (the output of another job, which lets you chain DVMs).
- **Other request tags.** `output` (wanted MIME type), `param` (job-specific settings), `bid` (max millisats the customer will pay), `relays` (where to publish answers), `p` (only this DVM should answer).
- **Result (request kind + 1000).** Kind 6001 for a 5001 job. It carries the original request in a `request` tag, plus `e` (job id), `p` (customer) and the `i` tags. The output goes in `content`.
- **Feedback (kind 7000).** A `status` tag: `payment-required`, `processing`, `error`, `success` or `partial`. An `amount` tag can carry a price in millisats and a bolt11 invoice.
- **Anyone can be a DVM.** Many DVMs can answer the same job. The customer picks the result they like. This is an open market, not an API with one provider.

---

## Hands-on guide

### Step 0: Project setup

```bash
mkdir my-dvm && cd my-dvm
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

You need two throwaway keys: one for the DVM and one for the customer. Use two terminal windows:

```bash
# terminal 1 (DVM)
export NSEC=$(nak encode nsec $(nak key generate))

# terminal 2 (customer)
export NSEC=$(nak encode nsec $(nak key generate))
```

### Step 1: Be a customer with `nak`

Before building, send a job by hand to the facilitator's DVM (or any DVM that handles kind 5001):

```bash
nak event --sec $NSEC -k 5001 \
  -t 'i=Nostr is a simple protocol. Users sign events with keys. Relays store and forward events. Clients show them.;text' \
  -t output=text/plain \
  wss://nos.lol
```

Copy the `id` from the output, wait a few seconds, then look for answers:

```bash
nak req -k 6001 -k 7000 -e <job id> wss://nos.lol
```

You see kind 7000 feedback and a kind 6001 result. In `nak`, `-t name="a;b"` makes a tag with several values: here `["i", "<text>", "text"]`.

### Step 2: Write the DVM

Create `dvm.js`:

```js
// dvm.js
import { SimplePool } from 'nostr-tools/pool'
import { finalizeEvent, getPublicKey } from 'nostr-tools/pure'
import * as nip19 from 'nostr-tools/nip19'
import { RELAYS, loadSecretKey } from './lib.js'

const JOB_KIND = 5001            // NIP-90 job kind for summarization
const RESULT_KIND = JOB_KIND + 1000
const sk = loadSecretKey()
const pk = getPublicKey(sk)
const pool = new SimplePool()
const seen = new Set()
const PRICE_SATS = Number(process.env.PRICE_SATS || 0) // 0 = free

const now = () => Math.floor(Date.now() / 1000)
const sign = (template) => finalizeEvent({ created_at: now(), ...template }, sk)

async function publish(event, relays = RELAYS) {
  const results = await Promise.allSettled(pool.publish(relays, event))
  return results.some((r) => r.status === 'fulfilled')
}

// The actual work. Swap this for something smarter later.
function summarize(text) {
  const sentences = text.replace(/\s+/g, ' ').trim().split(/(?<=[.!?])\s+/)
  const words = text.split(/\s+/).filter(Boolean).length
  const summary = sentences.slice(0, 2).join(' ')
  return `${summary}${sentences.length > 2 ? ' ...' : ''}\n\n(${words} words, ${sentences.length} sentences)`
}

// Turn the job's "i" tag into plain text
async function resolveInput(job) {
  const input = job.tags.find((t) => t[0] === 'i')
  if (!input) throw new Error('job has no "i" input tag')
  const [, value, type, relayHint] = input
  if (type === 'text') return value
  if (type === 'event') {
    const relays = relayHint ? [relayHint, ...RELAYS] : RELAYS
    const event = await pool.get(relays, { ids: [value] })
    if (!event) throw new Error('could not find the input event')
    return event.content
  }
  throw new Error(`input type "${type}" is not supported`)
}

function feedback(job, status, info, relays, extraTags = []) {
  return publish(sign({
    kind: 7000,
    content: '',
    tags: [['status', status, info], ['e', job.id], ['p', job.pubkey], ...extraTags],
  }), relays)
}

// Optional (Step 6): ask for payment first. Needs NWC_URL and nwc.js from Module 03.
async function getPaid(job, relays) {
  const { nwcRequest } = await import('./nwc.js')
  const msats = PRICE_SATS * 1000
  const { invoice, payment_hash } = await nwcRequest(process.env.NWC_URL, 'make_invoice', {
    amount: msats,
    description: `DVM job ${job.id.slice(0, 8)}`,
  })
  await feedback(job, 'payment-required', `${PRICE_SATS} sats please`, relays, [['amount', String(msats), invoice]])
  for (let i = 0; i < 100; i++) { // poll for about 5 minutes
    await new Promise((r) => setTimeout(r, 3000))
    const status = await nwcRequest(process.env.NWC_URL, 'lookup_invoice', { payment_hash })
    if (status.settled_at || status.state === 'settled') return
  }
  throw new Error('invoice was not paid in time')
}

async function handleJob(job) {
  if (seen.has(job.id)) return
  seen.add(job.id)

  // If the customer named a specific DVM with a "p" tag, only that DVM should answer
  const target = job.tags.find((t) => t[0] === 'p')?.[1]
  if (target && target !== pk) return

  // Answer on the relays the customer asked for, plus our own
  const asked = job.tags.find((t) => t[0] === 'relays')?.slice(1) || []
  const relays = [...new Set([...asked, ...RELAYS])]

  console.log('job', job.id.slice(0, 8), 'from', nip19.npubEncode(job.pubkey).slice(0, 16) + '...')

  try {
    if (PRICE_SATS > 0) await getPaid(job, relays)
    await feedback(job, 'processing', 'summarizing now', relays)
    const output = summarize(await resolveInput(job))
    await publish(sign({
      kind: RESULT_KIND,
      content: output,
      tags: [
        ['request', JSON.stringify(job)],
        ['e', job.id],
        ['p', job.pubkey],
        ...job.tags.filter((t) => t[0] === 'i'),
      ],
    }), relays)
    console.log('  done')
  } catch (err) {
    await feedback(job, 'error', err.message, relays)
    console.log('  failed:', err.message)
  }
}

// NIP-89: tell clients this DVM exists and which job kind it handles
await publish(sign({
  kind: 31990,
  content: JSON.stringify({ name: 'Workshop Summarizer', about: 'Summarizes text or a note.' }),
  tags: [['d', 'workshop-summarizer'], ['k', String(JOB_KIND)]],
}))

pool.subscribe(RELAYS, { kinds: [JOB_KIND], since: now() }, { onevent: handleJob })
console.log('DVM running as', nip19.npubEncode(pk))
console.log('listening for kind', JOB_KIND, 'jobs on', RELAYS.join(', '))
```

Walk through the important choices:

- `since: now()` means the DVM ignores old jobs from before it started.
- `seen` stops double work when the same job arrives from several relays.
- A job with a `p` tag for another DVM is ignored. That is how customers pick a provider.
- The DVM answers on the relays the customer listed in the `relays` tag.
- Every failure becomes a kind 7000 `error` feedback, so the customer is never left guessing.

### Step 3: Run it

In terminal 1:

```bash
node dvm.js
```

Note the `npub` it prints. Repeat the `nak` job from Step 1. Your DVM logs `job ... done`, and `nak req` now shows your result too.

### Step 4: The customer script

Create `customer.js`:

```js
// customer.js
import { SimplePool } from 'nostr-tools/pool'
import { finalizeEvent } from 'nostr-tools/pure'
import * as nip19 from 'nostr-tools/nip19'
import { RELAYS, loadSecretKey } from './lib.js'

// Usage:
//   node customer.js "some long text to summarize"
//   node customer.js note1...            (summarize an existing note)
//   DVM=npub1... node customer.js "..."  (ask one specific DVM)
const arg = process.argv[2]
const sk = loadSecretKey()
const pool = new SimplePool()

const input = arg.startsWith('note1')
  ? ['i', nip19.decode(arg).data, 'event', RELAYS[0]]
  : ['i', arg, 'text']

const tags = [input, ['output', 'text/plain'], ['relays', ...RELAYS]]
if (process.env.DVM) tags.push(['p', nip19.decode(process.env.DVM).data])

const job = finalizeEvent({ kind: 5001, created_at: Math.floor(Date.now() / 1000), tags, content: '' }, sk)

// Optional (Step 6): pay a payment-required invoice with NWC (needs nwc.js from Module 03)
async function pay(feedbackEvent) {
  const [, msats, invoice] = feedbackEvent.tags.find((t) => t[0] === 'amount') || []
  if (!invoice) return console.log('DVM wants payment but sent no invoice')
  if (!process.env.NWC_URL) return console.log(`pay ${Number(msats) / 1000} sats by hand:\n${invoice}`)
  const { nwcRequest } = await import('./nwc.js')
  await nwcRequest(process.env.NWC_URL, 'pay_invoice', { invoice })
  console.log(`paid ${Number(msats) / 1000} sats`)
}

const timer = setTimeout(() => { console.log('no result after 120 s'); process.exit(1) }, 120_000)

const sub = pool.subscribe(RELAYS, { kinds: [6001, 7000], '#e': [job.id] }, {
  onevent: (e) => {
    const who = nip19.npubEncode(e.pubkey).slice(0, 16) + '...'
    if (e.kind === 7000) {
      const [, status, info] = e.tags.find((t) => t[0] === 'status') || []
      console.log(`feedback from ${who}: ${status} ${info || ''}`)
      if (status === 'error') process.exit(1)
      if (status === 'payment-required') pay(e)
      return
    }
    console.log(`result from ${who}:\n${e.content}`)
    clearTimeout(timer)
    sub.close()
    pool.close(RELAYS)
  },
  oneose: async () => {
    // Subscribed first, so we will not miss a fast answer. Now send the job.
    await Promise.allSettled(pool.publish(RELAYS, job))
    console.log('job sent:', job.id)
  },
})
```

In terminal 2:

```bash
node customer.js "Nostr is a simple protocol. Users sign events with keys. Relays store and forward events. Clients show them."
node customer.js note1...                       # summarize a real note
DVM=npub1...yourdvm node customer.js "Only my DVM should answer this. Everyone else should stay quiet."
```

The script exits after the first result. With the whole room's DVMs online, the first answer could come from anyone. Try the `DVM=` form with a neighbour's DVM npub, and watch only their terminal react.

### Step 5: Discovery with NIP-89

Your DVM published a kind 31990 announcement when it started. Find every summarization DVM on the relays:

```bash
nak req -k 31990 -t k=5001 wss://nos.lol
```

Each result's `content` is a JSON object with `name` and `about`, and its `pubkey` is the DVM to put in a `p` tag. Clients use these announcements to show users a menu of providers for each job kind.

### Step 6: Paid jobs (optional)

Copy `nwc.js` from [Module 03, Step 2](../03-zaps-and-nwc/README.md#step-2-a-tiny-nwc-client) into this folder. The DVM needs a wallet connection with permission to **make and look up invoices**. The customer needs one with permission to **pay invoices** and a small budget.

```bash
# terminal 1 (DVM): charge 5 sats per job
export NWC_URL='nostr+walletconnect://...'   # receive-only connection
PRICE_SATS=5 node dvm.js

# terminal 2 (customer)
export NWC_URL='nostr+walletconnect://...'   # spending connection with a small budget
node customer.js "Paid jobs work. The DVM asks for sats first. Then it does the work."
```

Expected customer output:

```
job sent: ...
feedback from npub1...: payment-required 5 sats please
paid 5 sats
feedback from npub1...: processing summarizing now
result from npub1...:
Paid jobs work. The DVM asks for sats first. ...
```

Without `NWC_URL` on the customer side, the script prints the invoice so you can pay it from any wallet app.

Discuss the trust model: the customer pays first and hopes the DVM delivers. What could reduce that risk? (Small amounts, reputation, paying after a partial result, or the `bid` tag to cap the price.)

---

## Vibe coding prompts

Paste `dvm.js` with the prompt. Never paste your `nsec` or NWC string.

1. "Replace `summarize()` with a call to a local language model through Ollama's HTTP API on `localhost:11434`. Keep a 4,000 character input limit and send `error` feedback if the model is not running."
2. "Turn my DVM into a kind 5002 translation DVM. Read the target language from a `param` tag like `['param', 'language', 'es']`, and reply with an error if it is missing."
3. "Add support for the `url` input type: fetch the page with a 5 second timeout and a 200 KB limit, only allow `https://`, strip HTML tags, then summarize. Explain the security risks of fetching URLs for strangers."
4. "Add job chaining: support input type `job`, which means 'use the content of the kind 6xxx result for this job id'. Wait for that result if it does not exist yet."
5. "Build a kind 5300 content discovery DVM: return a JSON array of `['e', id]` tags for the 10 most-zapped notes of the last 24 hours, using kind 9735 receipts."
6. "Add a web page to my Module 02 client that lists kind 31990 DVM announcements for kind 5001, lets me pick one, sends a job with a `p` tag, and shows feedback and the result live."

Check the AI's work against NIP-90: result kind must be request kind + 1000, feedback is kind 7000, and the result must carry the `request`, `e` and `p` tags.

## Discussion questions

1. Many DVMs can answer the same job. How should a customer pick between them: price, speed, reputation, web of trust?
2. Job requests are public. What kinds of jobs should never go to a DVM like this? What does NIP-90 suggest for encrypted jobs?
3. Pay first or deliver first? How would you design payment so neither side can easily cheat?
4. A DVM can be a script, a GPU farm, or a human. What changes if the service provider is a person?
5. How is a DVM market different from calling a normal paid API? What is gained by putting jobs on relays?

## Common problems and fixes

| Problem | Fix |
|---|---|
| DVM never sees jobs | Check both scripts use the same `RELAYS`. Check the job kind matches `JOB_KIND`. Remember `since: now()`: jobs sent before the DVM started are ignored. |
| Customer gets results from strangers | That is the open market working. Use `DVM=npub1...` to target one DVM. |
| Customer hangs, DVM shows `done` | The customer listens on its `RELAYS`. Make sure the DVM publishes to the relays in the job's `relays` tag (the code does this) and that one relay is shared. |
| `error could not find the input event` | The note is not on the relays the DVM checks. Pass a relay hint in the `i` tag, or use a note that lives on the shared relays. |
| Publishing starts failing with `rate-limited` | A whole room on one public relay looks like spam. Use the facilitator's local relay (`nak serve`) and set `RELAYS` to it. |
| `Cannot find module './nwc.js'` | Only needed for Step 6. Copy `nwc.js` from Module 03, or leave `PRICE_SATS` unset and do not set `NWC_URL`. |
| DVM says `invoice was not paid in time` | The customer did not pay within about 5 minutes, or the wallet's `lookup_invoice` result has a different shape. Log the result and check your wallet's NWC support. |
| `nak req` returns nothing | Results may take a few seconds. Run it again. Make sure you use the job `id`, not the `note1` string. |

## Resources

- [NIP-90: Data Vending Machine](https://github.com/nostr-protocol/nips/blob/master/90.md) (kinds 5000-5999, 6000-6999, 7000)
- [Data Vending Machine job kinds registry](https://github.com/nostr-protocol/data-vending-machines)
- [NIP-89: Recommended application handlers](https://github.com/nostr-protocol/nips/blob/master/89.md) (kind 31990)
- [NIP-47: Nostr Wallet Connect](https://github.com/nostr-protocol/nips/blob/master/47.md) (`make_invoice`, `lookup_invoice`, `pay_invoice`)
- [NIP-57: Lightning zaps](https://github.com/nostr-protocol/nips/blob/master/57.md) (another way to pay a DVM)
- [nostr-tools](https://github.com/nbd-wtf/nostr-tools)
- [nak](https://github.com/fiatjaf/nak)

Previous: [Module 05](../05-identity-and-auth/README.md) | [Back to the workshop series](../../README.md)
