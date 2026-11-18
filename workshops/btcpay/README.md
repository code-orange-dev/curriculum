# Workshop: Accept Bitcoin with BTCPay Server

| | |
|---|---|
| **Length** | 2.5 hours |
| **Level** | Beginner |
| **Audience** | Shop owners, freelancers, community organizers, beginner developers |
| **Main tools** | [BTCPay Server](https://btcpayserver.org) (a test instance, a demo server or a third-party host), [Sparrow Wallet](https://sparrowwallet.com) or a phone wallet, the Point of Sale app |

[Back to all workshops](../README.md)

---

## What participants leave with

1. Their own BTCPay Server store, with a wallet they control connected to it.
2. A working Point of Sale (keypad or product list) they can open on a phone or tablet at a counter.
3. A paid test invoice, seen from both sides: the customer paying and the shop receiving.
4. An understanding of on-chain vs Lightning payments in a shop, and a plan for where to run BTCPay for real.

## Who this is for

Small business owners, cafe and market sellers, freelancers, event organizers and beginner developers. No coding. If people run a shop, ask them to bring a photo of their price list.

## Materials and hardware

| Item | How many | Rough cost | Notes |
|---|---|---|---|
| A BTCPay Server instance on **testnet** (or signet) that the host controls | 1 | Free to USD 20 per month | Self-hosted on a cheap VPS, on a home node ([Umbrel](https://umbrel.com) or [Start9](https://start9.com)), or BTCPay's public demo server. See "Before the session". |
| Laptop or tablet | 1 per person or per pair | | Any browser. A phone works for the shop side but is cramped for setup. |
| A phone with a wallet that works on the same test network | 1 per person | Free | To play the customer. Or use Sparrow on a laptop. |
| Test coins | About 0.005 test BTC per person | Free | Host fills a faucet wallet before the day and pays invoices from it, or sends coins to people's "customer" wallets. |
| Optional: a small amount of real sats for a Lightning demo | 1 host wallet | USD 5 | Only if the host's own BTCPay has Lightning on mainnet. |
| Optional: cheap tablet and stand | 1 | USD 80 to 150 | To show a real counter setup. |
| Projector or big screen | 1 | | |

## Before the session (host checklist)

- [ ] **Choose where the stores live.** Three options, best first:
  1. Your own BTCPay Server set to testnet or signet. You create an account for each participant, or turn on public sign-ups for the day only.
  2. BTCPay's public demo server (linked from [btcpayserver.org](https://btcpayserver.org)). Fast to start. Check on the day which networks it offers, and that it is up.
  3. A third-party BTCPay host. Fine for a later real shop. Read their terms: some hosts can see your store data.
- [ ] Do the whole hands-on guide once on the chosen instance, start to finish, including paying an invoice.
- [ ] Fill a "faucet wallet" with test coins on the same network as BTCPay. Public faucets are slow, so do it days before.
- [ ] Decide on Lightning. Lightning needs a Lightning node connected to BTCPay. On a demo server it may not be available. If you cannot show Lightning live with test coins, show it from your own mainnet store with a few hundred sats.
- [ ] Prepare a sample menu (for example a small coffee shop: 5 items with prices in your local currency).
- [ ] Write the server URL and any sign-up code on the whiteboard.

## Run sheet

| Time | Block | Notes |
|---|---|---|
| 0:00 | Welcome and safety rules | 10 min. Who already accepts digital payments? Which ones? What fees do they pay? |
| 0:10 | How BTCPay works | 20 min. Self-hosted, no middleman, no fees to BTCPay, payments go straight to your wallet. On-chain vs Lightning. |
| 0:30 | Hands-on 1: account, store and wallet | 30 min. Steps 1 to 3. |
| 1:00 | Hands-on 2: first invoice | 15 min. Step 4. Pay it from a test wallet. |
| 1:15 | Break | 10 min. |
| 1:25 | Hands-on 3: Point of Sale app | 30 min. Steps 5 and 6. Build your menu. Sell to your neighbour. |
| 1:55 | Lightning demo | 15 min. Step 7. Host shows a Lightning invoice paid in seconds. |
| 2:10 | Reports, refunds, and running it for real | 10 min. Step 8. |
| 2:20 | Discussion and wrap-up | 10 min. Discussion questions. |

**Total: 2 hours 30 minutes.**

---

## Concepts in five minutes

**BTCPay Server** is free, open-source software that makes invoices for bitcoin payments. It watches the blockchain (and a Lightning node, if you add one) and marks invoices as paid. It does not hold your coins: payments go straight to your wallet.

**Your wallet, their invoice.** For on-chain payments, you give BTCPay your wallet's **xpub** (the public key that makes addresses), not your seed. BTCPay then makes a fresh address for every invoice. It can see payments, but cannot spend.

**Hot wallet option.** BTCPay can also create a wallet on the server ("hot wallet"). Easier for features like refunds and PayJoin, but the keys sit on the server. Only use it on a server you run and trust, and with small amounts.

**On-chain vs Lightning:**

| | On-chain | Lightning |
|---|---|---|
| Speed | Minutes to an hour for confirmation | Seconds |
| Fees | Higher, depends on the network | Very low |
| Good for | Larger amounts | Coffee, snacks, tips |
| What the shop needs | Just a wallet | A Lightning node (or a connected Lightning service), with channels and liquidity |

**Point of Sale (PoS) app.** A BTCPay app that turns your store into a keypad or product menu on a tablet or phone at the counter. The customer scans a QR code and pays.

## Safety rules (read these out loud)

- **Test coins only today.** Test coins have no value.
- **Never type a seed phrase into BTCPay or any website.** To connect a wallet, use the xpub or a hardware wallet. If the host asks you to make a hot wallet on the test server for practice, that seed is a throwaway.
- **Never photograph seed words**, not even test ones.
- A store's API keys and Lightning connection strings are like passwords. Do not share them in a chat.

---

## Hands-on guide

### Step 1: Create an account and a store

1. Open the BTCPay URL from the whiteboard. Register an account (use any email-like name for a test server).
2. Create a store. Give it a name (for example `Warung Kopi Test`) and set the **default currency** to your local currency.
3. Pick a price source (the default is fine).

**Check:** you see the store dashboard with a list of setup steps.

### Step 2: Make a test wallet to receive

Pick one:

- **Sparrow on a laptop:** restart Sparrow on the same test network as BTCPay (from the Tools menu). Make a new single-signature wallet with a new seed. Write the seed on paper (or skip writing it: it is a throwaway). In the wallet Settings tab, copy the **xpub** (it may show as `tpub` or `vpub` on test networks).
- **Hot wallet on the test server:** in BTCPay, choose to create a new wallet. This is quick and fine for practice. Do not do this with real money on a server you do not run.

### Step 3: Connect the wallet to the store

1. In the store menu, open **Wallets**, then **Bitcoin**.
2. Choose to connect an existing wallet. Paste the xpub (or follow the steps for a new hot wallet).
3. BTCPay shows the first few addresses. **Compare them with the first receive addresses in Sparrow.** They must match.
4. Confirm.

**Check:** the store's Bitcoin wallet shows as set up.

### Step 4: Make and pay your first invoice

1. Open **Invoices** and create a new invoice for a small amount in local currency (for example 25,000 IDR).
2. Open the checkout page. You see a QR code, the amount in BTC, and a timer (invoices expire, often after 15 minutes, so the exchange rate is fair).
3. Pay it: scan with your test wallet, or ask the host to pay from the faucet wallet.
4. Watch the status change: **Processing** (seen, not yet confirmed) and later **Settled** (confirmed).

**Check:** the payment appears in your Sparrow wallet too. The money went straight to you.

### Step 5: Build a Point of Sale

1. In the store menu, find the apps section and create a new **Point of Sale** app.
2. Choose a style:
   - **Product list:** a menu with items and prices. Good for a cafe.
   - **Keypad:** type any amount. Good for a market stall.
   - **Print display:** a page you can print with a QR code per item.
3. Add 3 to 5 items from your sample menu. Add a picture if you like. Turn on tips if you want.
4. Save, then **View** the app. Open the same link on your phone.

### Step 6: Sell to your neighbour

1. Swap phones or laptops with your neighbour.
2. Your neighbour picks an item in your PoS and pays with their test wallet.
3. Watch the invoice arrive in your store's Invoices list.

Talk about it: what would a real customer see? What if they underpay? (BTCPay marks the invoice as partially paid, and the customer can pay the rest.)

### Step 7: Lightning demo (host)

1. The host opens their own store with Lightning connected (on the test server if it has Lightning, or on mainnet with a few hundred sats).
2. Make a small invoice and pay it from a Lightning wallet on a phone. It settles in seconds.
3. Show where Lightning is configured in the store settings. Explain the options: BTCPay's own Lightning node on the same server (LND or Core Lightning), or connecting an external node.
4. Explain liquidity in one sentence: to receive over Lightning, your node needs "inbound" capacity in its channels.

### Step 8: Reports and running it for real

Show, without doing:

- **Reporting:** export invoices for your bookkeeping.
- **Refunds:** BTCPay can create a refund link for an invoice.
- **Users and roles:** add a cashier who can use the PoS but not change settings.
- **PayJoin:** a hot wallet store can receive PayJoin payments, which improves privacy for both sides.
- **Where to run it for real:**

| Option | Rough cost | Trade-off |
|---|---|---|
| On your home node (Umbrel, Start9) | Hardware you already have | Must stay online. Public access is through Tor or a tunnel. |
| A VPS you rent | USD 10 to 25 per month | You maintain it. Needs enough disk for a pruned node or more. |
| A third-party host | Varies | Quick, but the host can see your store data. |

---

## Discussion questions

1. Would your customers pay with bitcoin today? What would make them start?
2. Card fees are often 1 to 3 percent. What does BTCPay cost you instead (server, time, learning)?
3. Would you keep the bitcoin, or change some to local currency to pay suppliers? How?
4. What are the risks of a hot wallet on a server? When is it worth it?
5. What does your local tax law say about accepting bitcoin? Who could you ask?

## Common problems and fixes

| Problem | Fix |
|---|---|
| Invoice never shows "Processing" | The paying wallet is on a different network than BTCPay (signet vs testnet4 vs testnet3). Check the address prefix and the server's network. |
| Addresses in BTCPay and Sparrow do not match | Wrong xpub, or a different script type (for example `vpub` vs `tpub`). Copy the xpub again from the wallet Settings. |
| Invoice expired before paying | Make a new invoice. In store settings you can make the expiry longer. |
| Paid but still "Processing" | On-chain needs confirmations. Test networks can be slow. This is normal. |
| Lightning option missing at checkout | No Lightning node is connected to the store, or the node is not synced. |
| Demo server is down or full | Have a second option ready (your own test instance, or pair people on one store). |

## Safety notes

- Connect your real store to a wallet you control with an xpub, ideally from a hardware wallet. Your seed never touches the server.
- Keep a backup of the store settings and of anything BTCPay tells you to back up (for example a hot wallet seed or Lightning node backup).
- Lightning on your server is a hot wallet. Keep only what you need for daily trade, and move the rest to cold storage.
- Update BTCPay Server regularly from official sources.
- A third-party host can see your sales. Run your own when you are ready.

## Further resources

- [BTCPay Server](https://btcpayserver.org) and the [BTCPay Server docs](https://docs.btcpayserver.org): setup, Point of Sale, Lightning, deployment options
- [Sparrow Wallet docs](https://sparrowwallet.com/docs/): finding your xpub
- [Umbrel](https://umbrel.com) and [Start9](https://start9.com): run BTCPay Server at home with one click
- [payjoin.org](https://payjoin.org): what PayJoin is and which wallets support it
- [mempool.space](https://mempool.space): check a payment and current fees
- Recap of a past session: [Agentic Engineering & Coding Workshop](https://codeorange.dev/session-notes/2026-10-21-agentic-engineering) (BTCPay Server on an Umbrel running a tip button)
- Recap of a past session: [Privacy Track: How PayJoin Works](https://codeorange.dev/session-notes/2026-10-06-privacy-track) (BTCPay Server as a PayJoin receiver)
- Related workshops: [Run your own node](../nodes/README.md) and [Ecash for everyday payments](../ecash/README.md)
