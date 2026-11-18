# Workshop: Ecash for Everyday Payments (Cashu and Fedimint)

| | |
|---|---|
| **Length** | 2 hours |
| **Level** | Beginner |
| **Audience** | Mostly non-developers and beginner developers |
| **Main tools** | [Cashu](https://docs.cashu.space) wallets (Minibits, Nutstash, cashu.me), a test mint or a Nutshell mint run by the host, [Fedimint](https://fedimint.org) for the federation part |

[Back to all workshops](../README.md)

---

## What participants leave with

1. A Cashu wallet on their phone or browser, with test ecash in it.
2. Experience sending and receiving ecash as a text token or QR code, including "offline style" payments.
3. A clear picture of the trade-off: ecash is private and simple, but **the mint holds the bitcoin**. You trust the mint.
4. The difference between a single Cashu mint and a Fedimint federation run by several guardians.
5. Their own rule for how much to keep in ecash (a pocket wallet, not savings).

## Who this is for

People who use Lightning wallets, or want an easy and private way to pay small amounts. Community organizers who might run a mint for their village, school or event. No coding needed. The optional mint setup is for the host or curious developers.

## Materials and hardware

| Item | How many | Rough cost | Notes |
|---|---|---|---|
| Phone with a Cashu wallet, or a laptop with a browser | 1 per person | Free | Minibits (phone app), or a browser wallet such as cashu.me or Nutstash. |
| A **test mint** | 1 | Free | A public test mint that gives free fake sats (see the [Cashu docs](https://docs.cashu.space) for the current one), or a Nutshell mint the host runs with a fake Lightning backend. |
| Host laptop with Docker or Python | 1 | | Only if the host runs their own Nutshell mint. |
| A Fedimint test federation, or a Fedi app demo | 1 | Free | Optional. Check [fedimint.org](https://fedimint.org) for a current test federation, often on signet or mutinynet. |
| A small amount of real sats in a Lightning wallet | Host only | USD 5 | Optional, to show minting real ecash from a real mint at the end. |
| Printed QR codes with test tokens | 10 to 20 | Free | Fun for a "treasure hunt" (see Step 5). |
| Projector or big screen | 1 | | |

## Before the session (host checklist)

- [ ] Choose the mint for the session:
  - **Public test mint:** no setup, invoices are "paid" automatically with fake sats. Check it is online on the day.
  - **Your own Nutshell mint with a fake backend:** full control, and you can show the mint side. See Step 6.
- [ ] Install the wallets you will show and add the test mint to each. Mint, send and receive once.
- [ ] Check the wallets work on both Android and iPhone, or have the browser wallets ready as a backup.
- [ ] Prepare 10 to 20 small test tokens and print them as QR codes for the treasure hunt.
- [ ] Optional: prepare a Fedimint demo (a test federation joined in a Fedimint wallet such as the Fedi app).
- [ ] Prepare the trust slide: "Who holds the bitcoin?" for a bank, a custodial Lightning wallet, a Cashu mint, a Fedimint federation, and self-custody.

## Run sheet

| Time | Block | Notes |
|---|---|---|
| 0:00 | Welcome and safety rules | 10 min. |
| 0:10 | What ecash is | 20 min. Blind signatures with the envelope and carbon paper story. Who holds the bitcoin? |
| 0:30 | Hands-on 1: install a wallet and add the mint | 15 min. Steps 1 and 2. |
| 0:45 | Hands-on 2: mint, send, receive | 20 min. Steps 3 and 4. |
| 1:05 | Treasure hunt | 10 min. Step 5. Claim printed tokens before someone else does. |
| 1:15 | Host demo: run a mint | 15 min. Step 6. Optional, for mixed rooms. |
| 1:30 | Fedimint and the custody trade-off | 15 min. Step 7. |
| 1:45 | Discussion and wrap-up | 15 min. Discussion questions. Melt test tokens or let them expire. |

**Total: 2 hours.**

---

## Concepts in five minutes

**Ecash is a bearer token.** Like a banknote: whoever holds the token can spend it. In Cashu, a token is just a piece of text (it starts with `cashuA` or `cashuB`) or a QR code. You can send it in any chat app.

**The mint.** You pay the mint some bitcoin (usually over Lightning). The mint gives you ecash tokens worth the same amount. Later you can give the tokens back and the mint pays a Lightning invoice for you ("melt").

**Blind signatures make it private.** When you get tokens, the mint signs them without seeing them, like signing through an envelope with carbon paper. Later, when someone spends the token, the mint knows it signed it, but not for whom. So the mint cannot link who paid whom.

**But the mint holds the bitcoin.** This is the big trade-off. If the mint disappears, is hacked or turns bad, your tokens are worth nothing. Ecash is custodial. It is great for small amounts and privacy, not for savings.

**Fedimint** spreads the trust. Instead of one mint operator, a group of "guardians" (for example 4 people in a community) run the mint together. A majority must agree to move the bitcoin. One bad or lost guardian is not enough to steal or stop it.

**Double spending.** Sending a token is just sending text. Until the receiver "claims" it (swaps it at the mint for new tokens), the sender could still spend it. So for real payments, claim tokens as soon as you get them.

| Who holds the bitcoin? | Privacy from the operator | Trust needed |
|---|---|---|
| Custodial Lightning wallet | Low: they see every payment | One company |
| Cashu mint | High: blind signatures | One mint operator |
| Fedimint federation | High: blind signatures | A majority of guardians |
| Your own wallet (self-custody) | Depends on your habits | Only yourself |

## Safety rules (read these out loud)

- **Test sats only today.** Test ecash has no value.
- **An ecash token is cash.** Whoever sees the token text or QR code first can claim it. Do not post real tokens in public.
- **Wallet seeds:** some Cashu wallets show a seed phrase to restore your tokens. **Never photograph it and never type it into a website.** Write it on paper.
- **Do not use a real mint you do not know.** Anyone can start a mint. Only put in what you can afford to lose.

---

## Hands-on guide

### Step 1: Install a wallet

Pick one:

- **Minibits:** a phone app. Install it from your app store or the links on its website.
- **cashu.me:** a browser wallet. Open it in your phone browser and "add to home screen" so it works like an app.
- **Nutstash:** another browser wallet.

Create a new wallet. If the app shows a seed phrase, write it on paper. (Today it only protects test sats.)

### Step 2: Add the test mint

1. Find the mints section in the wallet.
2. Add the test mint URL from the whiteboard.
3. The wallet shows the mint's name and info.

**Check:** the mint appears in your list, with a balance of 0.

### Step 3: Mint test ecash

1. Choose to receive or "top up" from the mint over Lightning. Enter an amount, for example 1,000 sats.
2. The wallet shows a Lightning invoice.
3. On a test mint with a fake backend, the invoice is marked paid automatically after a moment. (On a real mint you would pay it from a Lightning wallet.)

**Check:** your balance shows 1,000 test sats.

### Step 4: Send and receive

1. Choose **Send** and pick **ecash** (not Lightning). Enter 100 sats.
2. The wallet shows a token as a QR code and as text starting with `cashu...`.
3. Your neighbour scans the QR code (or you paste the text into a chat to them).
4. Your neighbour's wallet **claims** the token. Their balance goes up by 100.
5. Try it the other way round.

Now look at the token text together. It is long because it holds the mint URL and the signed secrets. Some wallets can decode it to show what is inside.

**Try this:** send a token, but do not let anyone claim it. Then try to claim it twice from two phones. Only the first one works. That is the mint stopping a double spend.

### Step 5: Treasure hunt

The host has hidden printed QR codes with small test tokens around the room. Find one, scan it, claim it. Whoever claims first gets it. If you scan one and it says "already spent", someone was faster.

This shows how bearer tokens work: a QR code on paper is money, and only the first claim counts.

### Step 6: Host demo: run a Nutshell mint

Show this on the projector. Developers can follow along.

[Nutshell](https://github.com/cashubtc/nutshell) is a Cashu mint and wallet written in Python. For a workshop, run it with the **FakeWallet** Lightning backend, which "pays" every invoice with fake sats.

The main settings are environment variables. Check the Nutshell README for the current names and the Docker command:

```
MINT_BACKEND_BOLT11_SAT=FakeWallet
MINT_LISTEN_HOST=0.0.0.0
MINT_LISTEN_PORT=3338
MINT_PRIVATE_KEY=<a long random string, never reuse it>
```

Then:

1. Start the mint (with Docker, or with Python as in the README).
2. Open `http://<your-laptop-ip>:3338/v1/info` in a browser. You see the mint's info as JSON.
3. Add the mint URL in a wallet and mint some fake sats.
4. Show the mint's log: it signs blinded messages. It never sees who later spends them.

Browser wallets on `https://` pages may refuse a mint on plain `http://`. If that happens, use a phone app wallet, or put the mint behind HTTPS.

**Never run a FakeWallet mint on a public address and call it real.** It creates sats from nothing.

### Step 7: Fedimint and the trust question

1. Show [fedimint.org](https://fedimint.org) and a Fedimint wallet joined to a test federation (if you prepared one). Show the list of guardians.
2. Draw the difference on the board:
   - Cashu: one operator holds the bitcoin.
   - Fedimint: several guardians hold it together, and a majority must agree.
3. Ask: who in your community would you trust as a guardian? Would you be a guardian?

---

## Discussion questions

1. Where would ecash make sense in your life? Where would it not?
2. How much would you keep in a mint you do not run yourself?
3. What happens if a mint disappears? How is that like a bank or a custodial wallet? How is it different?
4. Ecash tokens are just text, so they can travel in any chat app, even over Bluetooth. What does that make possible?
5. Would your community run a Fedimint? Who would be the guardians, and what would happen if two of them moved away?

## Common problems and fixes

| Problem | Fix |
|---|---|
| Wallet cannot reach the mint | Check the URL (https vs http, the port, no extra slash). Check the mint is online. |
| Browser wallet refuses the host's mint | Mixed content: an https page talking to an http mint. Use a phone app or put the mint behind HTTPS. |
| Invoice never gets paid on the test mint | The mint's fake backend may be off, or you are on a real mint by mistake. Check the mint URL. |
| Token says "already spent" | Someone claimed it first, or you claimed it already. |
| Neighbour's wallet does not know the mint | Most wallets ask to add the mint when you receive a token from a new mint. Accept it (for test mints only). |
| Balance looks wrong after restore | Some wallets need you to restore from the seed and then re-scan each mint. Check the wallet's restore option. |

## Safety notes

- **Ecash is custodial.** Treat a mint like a wallet run by someone else. Keep small amounts only.
- Claim tokens you receive right away, so the sender cannot spend them again.
- Back up the wallet seed if your wallet has one, on paper. Never photograph it or type it into a website.
- Prefer mints run by people you know, or federations with guardians you trust.
- Do not lose the token text before it is claimed. If you send a token and the receiver never claims it, you can usually take it back (reclaim) from your wallet's history.

## Further resources

- [Cashu docs](https://docs.cashu.space): how Cashu works, wallets and mints
- [Nutshell](https://github.com/cashubtc/nutshell): the Python mint and wallet used in Step 6
- [Fedimint](https://fedimint.org): federated ecash, guardians and how to run a federation
- Recap of a past session: [Sovereign Bitcoiner Workshop: White Noise, Private Chats on Nostr](https://codeorange.dev/session-notes/2026-11-11-sovereign-bitcoiner-workshop) (ecash tokens as text inside chat apps)
- Recap of a past session: [Sovereign Bitcoiner Workshop: Why Privacy Matters](https://codeorange.dev/session-notes/2026-10-14-sovereign-bitcoiner-workshop) (ecash and Fedimint as a privacy layer)
- For developers: the [Privacy Track](../../privacy-track/README.md) has a session on Cashu and Fedimint
- Related workshops: [Accept bitcoin with BTCPay Server](../btcpay/README.md) and [Nostr and private group chats](../nostr/README.md)
