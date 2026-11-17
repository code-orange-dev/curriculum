# Workshop: Nostr and Private Group Chats with White Noise

| | |
|---|---|
| **Length** | 2 hours |
| **Level** | Beginner, mixed rooms welcome |
| **Audience** | Non-developers and developers together |
| **Main tools** | A Nostr client ([Primal](https://primal.net), Damus on iPhone, or Amethyst on Android), [White Noise](https://whitenoise.chat), [njump.me](https://njump.me) |

[Back to all workshops](../README.md)

---

## What participants leave with

1. A Nostr identity (a key pair), with a profile, following a few people, on a client they like.
2. An understanding of keys, relays and clients, and why there is no "forgot password" on Nostr.
3. A private White Noise group chat with their table, end-to-end encrypted, with no phone number and no company server.
4. A simple way to check that an npub really belongs to a friend.
5. For developers: a path into the [Vibe Coding on Nostr modules](../../nostr-workshops/README.md).

## Who this is for

Anyone with a smartphone. People who use WhatsApp, Telegram or Signal and wonder what else is possible. Developers are welcome: give them the bonus tasks and point them to the developer modules.

## Materials and hardware

| Item | How many | Rough cost | Notes |
|---|---|---|---|
| Smartphone (Android or iPhone) | 1 per person | | Most of the workshop happens on phones. |
| Laptop | Optional | | For the web client and for developers. |
| Good Wi-Fi | 1 | | Nostr apps talk to many relays at once. |
| Printed QR code of the host's npub | 5 to 10 | Free | So people can follow the host and test a chat. |
| Paper and pens | 1 per person | Free | For writing down the nsec backup. |
| Projector or big screen | 1 | | |

## Before the session (host checklist)

- [ ] Install the client apps you will show and White Noise on your own phone. Use a **workshop identity**, not your personal one.
- [ ] Check the current download links on [whitenoise.chat](https://whitenoise.chat). White Noise is new, and how to install it changes (app stores, test builds, Zapstore on Android).
- [ ] Create a test group in White Noise with a second phone. Send messages and a photo. Note any snags.
- [ ] Make sure your workshop npub has a profile picture and name, and print its QR code.
- [ ] Decide on default relays. The apps' defaults are usually fine. Have 2 or 3 extra public relays on the whiteboard in case one is down.
- [ ] Prepare the comparison table from Concepts on a slide.

## Run sheet

| Time | Block | Notes |
|---|---|---|
| 0:00 | Welcome and safety rules | 10 min. Ask who uses Telegram, WhatsApp, Signal. What could stop them working? |
| 0:10 | Nostr in ten minutes | 15 min. Keys, events, relays, clients. Draw it. |
| 0:25 | Hands-on 1: create your identity | 20 min. Steps 1 and 2. Back up the nsec on paper. |
| 0:45 | Hands-on 2: post, follow, look under the hood | 15 min. Step 3. Find yourself on njump.me. |
| 1:00 | Break | 5 min. |
| 1:05 | Why private chat is hard | 10 min. The server in the middle, key exchange, metadata. |
| 1:15 | Hands-on 3: White Noise groups | 30 min. Steps 4 to 6. One group per table. |
| 1:45 | Discussion and wrap-up | 15 min. Discussion questions. Point developers to the developer modules. |

**Total: 2 hours.**

---

## Concepts in five minutes

**Keys are your account.** On Nostr you have a key pair. The public key (`npub...`) is your identity, like a username anyone can see. The secret key (`nsec...`) proves it is you. There is no company, no email, no password reset. Lose the nsec and the account is gone. Leak it and someone else can be you forever.

**Events.** Everything you do (a post, a like, a profile update) is a small message called an event, signed with your nsec.

**Relays** are simple servers that store and pass on events. You use several at once. If one blocks you or goes down, the others still carry your posts. Anyone can run a relay.

**Clients** are the apps: Primal, Damus (iPhone), Amethyst (Android) and many more. They all read the same events, so you can switch apps and keep your followers.

**Private chat needs something in the middle.** Phones are often offline, so something must hold your message until your friend comes online. The question is: who runs it, and what can it see?

| App | End-to-end encrypted by default | What sits in the middle | One off switch? |
|---|---|---|---|
| Telegram | No, only "secret chats" | Telegram's servers | Yes |
| WhatsApp | Yes | Meta's servers | Yes |
| Signal | Yes | Signal's servers | Yes |
| White Noise | Yes (MLS) | Nostr relays you can choose | No |

**White Noise** uses MLS (Messaging Layer Security, a standard made for group chats) to agree on keys and encrypt messages. The Marmot protocol puts MLS on top of Nostr. Relays carry the encrypted messages, and Blossom servers hold encrypted photos and files. No phone number needed.

**Metadata matters.** Older Nostr direct messages hide the text but show who messaged whom and when. Newer designs ("gift wrap") hide that too. White Noise is designed to hide much of this metadata, but private messaging on Nostr is still young and still improving.

## Safety rules (read these out loud)

- **Never paste your nsec into a website, a chat or an AI assistant.** Your nsec is your whole identity.
- **Write the nsec on paper.** Do not screenshot it or photograph it. Photos sync to the cloud.
- **Everything you post publicly on Nostr is public and very hard to delete.** Think before you post.
- **Today is practice.** If you want, make a throwaway identity now and a "real" one later at home.
- Check that an npub really belongs to your friend before you share secrets with it (see Step 6).

---

## Hands-on guide

### Step 1: Install a client

Pick one:

- **Primal** (Android, iPhone and web): easy start, built-in wallet features.
- **Damus** (iPhone).
- **Amethyst** (Android): many features.

Install from the official app store or the project's own website.

### Step 2: Create your identity

1. Choose "create account" (not "log in").
2. Pick a name and, if you like, a picture and a short bio.
3. Find the place in settings where the app shows your keys. Copy your **npub** and share it freely.
4. Find your **nsec** (sometimes called "private key" or "secret key"). **Write it on paper.** Double-check every character.

Some apps support a "signer" app instead of holding your nsec, for example Amber on Android. That is safer for real use. Mention it, but keep today simple.

**Check:** you can see your own profile with your name.

### Step 3: Post, follow, and look under the hood

1. Scan the host's QR code and follow them. Follow your neighbours.
2. Post a short public note: "Hello from the Nostr workshop!"
3. Open [njump.me](https://njump.me) in a browser and paste your npub. You see your profile and note **outside** your app. This proves the data lives on relays, not inside one app.
4. In your app's settings, find the relay list. How many relays are you using? Add one from the whiteboard.

**Bonus for developers:** look at the raw event JSON (some clients can show it, or use the `nak` tool from the [Nostr basics module](../../nostr-workshops/modules/01-nostr-basics/README.md)). Find the `pubkey`, `kind`, `content` and `sig` fields.

### Step 4: Set up White Noise

1. Install White Noise using the links on [whitenoise.chat](https://whitenoise.chat).
2. Sign in. You can create a new identity, or use the one from Step 2. If you log in with your nsec, type it only into the app, never into a website.
3. Open the app once and let it finish setting up. In the background it publishes the information other people need to add you to a chat.

### Step 5: Make a group chat for your table

1. One person per table creates a new group.
2. Add the others by their npub (scan their QR code, or search).
3. Everyone sends a message and, if they want, a photo.
4. Try: one person turns off Wi-Fi and mobile data, the others send messages, then that person comes back online. Do the messages arrive?

**Check:** everyone at the table sees all messages.

### Step 6: Check that a key is really your friend's

1. Two people compare their npubs face to face: read the first 8 and last 8 characters out loud, or scan each other's QR codes.
2. Talk about it: a chat can be perfectly encrypted, but to the wrong person. Signal and WhatsApp let you compare a "safety number". On Nostr, the question is "is this npub really my friend's?"
3. Ask: how would you check an npub you got from a stranger online? (A second channel: in person, a phone call, their website.)

---

## Discussion questions

1. Which chat apps does your family use? What would happen if that app were blocked in your country tomorrow?
2. Why is it hard to switch off a chat that runs over many relays anyone can run?
3. No phone number, no email, no password reset. Is that freedom or risk? Both?
4. What metadata does your current chat app see: who, when, how often, where?
5. White Noise is young software. What would make you trust it more? (Audits, time, open source, people you know using it.)

## Common problems and fixes

| Problem | Fix |
|---|---|
| Cannot add a friend to a White Noise group | Your friend must open White Noise at least once first, so the app publishes what others need to invite them. Ask them to open the app, wait a minute, then try again. |
| Group messages do not arrive | Check both phones are online and using some of the same relays. Give it a minute. Restart the app. |
| Profile not showing on njump.me | Your app may not have published to the relays njump checks yet. Wait, or add a popular relay. |
| "Logged out" and nsec not written down | The account is gone. Make a new one. This is why we write it down. |
| App asks for a signer | Choose the option to create a key in the app instead, or install a signer app if you know how. |
| Photo will not send | The media server may be busy. Try a smaller photo, or try later. |

## Safety notes

- Your nsec is your identity. Keep it on paper, in a password manager, or in a signer app. Never in a screenshot.
- If you think your nsec has leaked, make a new identity and tell your followers. There is no way to change the key of an old account.
- Public Nostr posts are public forever. Private White Noise chats are encrypted, but your phone can still be lost or seized: use a screen lock.
- Some apps in the Nostr world are new and change fast. Install them from official sources and keep them updated.

## Further resources

- [Nostr NIPs](https://github.com/nostr-protocol/nips): the specifications, like BIPs for Nostr
- [NIP-59: Gift wrap](https://github.com/nostr-protocol/nips/blob/master/59.md): hides who sent a message and when
- [White Noise](https://whitenoise.chat): private group chats on Nostr
- [njump.me](https://njump.me): view any Nostr profile or note in a browser
- Clients: [Primal](https://primal.net), [Damus](https://damus.io), [Amethyst](https://github.com/vitorpamplona/amethyst)
- Recap of a past session: [Sovereign Bitcoiner Workshop: White Noise, Private Chats on Nostr](https://codeorange.dev/session-notes/2026-11-11-sovereign-bitcoiner-workshop)
- For developers: [Vibe Coding on Nostr](../../nostr-workshops/README.md), six hands-on modules, starting with [Nostr Basics: Keys, Relays, and NIPs](../../nostr-workshops/modules/01-nostr-basics/README.md) and [Running Your Own Relay](../../nostr-workshops/modules/04-run-a-relay/README.md)
- Related workshops: [Ecash for everyday payments](../ecash/README.md) (ecash tokens are text, so they fit in a chat) and [Bitcoin privacy in practice](../privacy/README.md)
