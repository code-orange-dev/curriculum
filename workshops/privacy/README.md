# Workshop: Bitcoin Privacy in Practice

| | |
|---|---|
| **Length** | 2.5 hours |
| **Level** | Beginner to intermediate, mixed rooms welcome |
| **Audience** | Bitcoin users and developers together |
| **Main tools** | [Sparrow Wallet](https://sparrowwallet.com) (labels, UTXOs, coin control) on testnet or signet, [mempool.space](https://mempool.space), Tor, PayJoin and Silent Payments wallets for the demo |

[Back to all workshops](../README.md)

---

## What participants leave with

1. A simple threat model for their own bitcoin: who are they hiding from, and how much effort will they spend?
2. The ability to read a transaction on a block explorer the way chain analysis does, and spot the change output.
3. Hands-on practice with **labels**, the **UTXO list**, **freezing** coins and **coin control** in Sparrow.
4. An understanding of three newer tools: **PayJoin**, **Silent Payments** and **Tor**, and which wallets support them.
5. A short list of habits to start tomorrow.

## Who this is for

Anyone who holds bitcoin in a self-custody wallet. Developers are welcome: give them the bonus tasks and point them to the [Privacy Track](../../privacy-track/README.md).

## Materials and hardware

| Item | How many | Rough cost | Notes |
|---|---|---|---|
| Laptop with [Sparrow Wallet](https://sparrowwallet.com/download/) | 1 per person or per pair | Free | On testnet4 or signet. |
| Test coins | About 0.01 test BTC per person, sent as **3 to 5 separate payments** | Free | Several small UTXOs make coin control interesting. |
| Host phone with a PayJoin wallet and a Silent Payments wallet | 1 | Free | For the live demos. Check [payjoin.org](https://payjoin.org) and [silentpayments.xyz](https://silentpayments.xyz) for current wallets. |
| A few thousand real sats | Host only | Under USD 5 | Only if you demo PayJoin or Silent Payments live on mainnet. Many of these wallets do not support test networks. |
| Printed "spot the change" transactions | 1 set per table | Free | 3 or 4 transactions from mempool.space (see Step 2). |
| Projector or big screen | 1 | | |

## Before the session (host checklist)

- [ ] Fill a faucet wallet in Sparrow on the chosen test network. Plan to send **each person 3 to 5 separate payments** of different sizes, with a few minutes between them.
- [ ] Pick 3 or 4 real mainnet transactions on mempool.space to read together: one simple payment with change, one with a round-number payment, one PayJoin (if you have one) and one CoinJoin. Do not use transactions that could identify anyone in the room.
- [ ] Test the PayJoin demo end to end, with the real wallets you will use. Past sessions found that PayJoin sometimes quietly falls back to a normal payment, so check the result on mempool.space.
- [ ] Test the Silent Payments demo: show a `sp1...` address, send to it, and receive.
- [ ] Check Sparrow can connect over Tor from the venue network (or bring a hotspot).
- [ ] Do the hands-on guide once, start to finish.

## Run sheet

| Time | Block | Notes |
|---|---|---|
| 0:00 | Welcome and safety rules | 10 min. |
| 0:10 | Why privacy? A story and a threat model | 20 min. The carpet story. The four threat model questions. |
| 0:30 | Hands-on 1: read a transaction like an analyst | 20 min. Steps 1 and 2. Spot the change. |
| 0:50 | Hands-on 2: labels and the UTXO list | 20 min. Steps 3 and 4. |
| 1:10 | Break | 10 min. |
| 1:20 | Hands-on 3: coin control and freezing | 25 min. Steps 5 and 6. |
| 1:45 | PayJoin demo | 15 min. Step 7. |
| 2:00 | Silent Payments and Tor | 15 min. Steps 8 and 9. |
| 2:15 | Your privacy habits and wrap-up | 15 min. Step 10. Discussion questions. |

**Total: 2 hours 30 minutes.**

---

## Concepts in five minutes

**Bitcoin is public on purpose.** Every transaction is on the blockchain forever, so anyone can check the supply. Privacy is added on top, with good habits and tools.

**The carpet story** (from a past session). Someone bought a carpet with bitcoin and looked up the payment on a block explorer. They could see that the seller's wallet held a whole bitcoin. Now a stranger knew what the seller looked like, where they lived, and how much they had.

**UTXOs.** Your wallet does not hold "a balance". It holds separate coins (UTXOs, unspent transaction outputs), each from a payment you received. When you spend, the wallet picks some coins as inputs, pays the receiver, and sends the rest back to you as **change**.

**How chain analysis guesses:**

1. **All inputs belong to one person.** If two coins are spent together, they are probably owned by the same wallet.
2. **The change is the odd one.** The payment is often a round number in local money. The change is the leftover, often the bigger, non-round output, or the one with the same address type as the inputs.
3. **Address reuse links everything.** Using the same address twice links those payments forever.

**Labels and coin control fight this.** If you know where each coin came from (labels), you can choose which coins to spend together (coin control), and keep some apart (freeze).

**PayJoin** breaks guess number 1. The receiver adds one of their own coins to the payment. The transaction looks normal, but the inputs no longer all belong to one person, and the amounts no longer show the real payment.

**Silent Payments** let you share one public address (it starts with `sp1`) for donations or invoices, and every payer still sends to a new, unlinkable address on the blockchain. No address reuse, no server needed.

**Tor** hides your IP address from the server your wallet talks to, and from the Bitcoin network when your node broadcasts.

**Threat model: four questions.** Who am I protecting against? How likely is it? How bad is failure? How much effort will I spend?

## Safety rules (read these out loud)

- **Test coins only for the hands-on part.** The host shows real-money demos on their own phone.
- **Never type a real seed phrase into a laptop or website.**
- **Never photograph seed words.**
- **Do not look up your own real addresses on a public explorer on the venue Wi-Fi.** The explorer learns your IP and which addresses you care about. Use your own node, or Tor.
- Do not share real transaction IDs of people in the room.

---

## Hands-on guide

### Step 1: Set up Sparrow on the test network

1. Open Sparrow and restart it on **testnet4** or **signet** (Tools menu), the one the host picked.
2. Make a new single-signature, native segwit wallet with a new seed. Write the seed on paper (it is a throwaway).
3. Give the host 3 receive addresses (Receive tab, then "Get Next Address" each time). The host sends a payment to each one.

While the coins arrive, do Step 2.

### Step 2: Spot the change

On the projector (or on printed sheets), look at the host's chosen transactions on [mempool.space](https://mempool.space). For each one, the tables decide:

1. Which output is the payment and which is the change? Why?
2. Can you guess the payment in local money? (Convert with the price on that day.)
3. Do all inputs belong to one person? How sure are you?

Then show a PayJoin and a CoinJoin. Which guesses fail now?

### Step 3: Label everything

1. In Sparrow, open the **Transactions** tab. Each incoming payment has an empty **Label** column.
2. Double-click and label each one with where it came from: `Faucet - payment 1`, `Bought from friend`, `Salary`, `Exchange with ID`.
3. Open the **Addresses** tab. Label receive addresses before you share them: "Given to a friend for the bike".

Labels are for you, not for the blockchain. They live in your wallet file. Sparrow can export and import labels in a standard format (BIP 329), so they move with you to another wallet.

### Step 4: Read your UTXO list

1. Open the **UTXOs** tab. You see each coin separately, with its amount, label and address.
2. Ask: which of these coins came from an exchange that knows your name (a "KYC" coin)? Which came from a private trade?
3. Ask: if you spent all of them in one transaction, what would the receiver learn about you?

### Step 5: Freeze a coin

1. In the UTXOs tab, right-click one coin (pretend it is your KYC exchange coin) and **freeze** it.
2. Try to send an amount bigger than your unfrozen coins. Sparrow will not use the frozen coin.

Freezing is useful for: coins you want to keep separate, very small "dust" coins that someone sent to track you, and coins you plan to spend later in a special way.

### Step 6: Coin control: choose your inputs

1. In the UTXOs tab, select **one** coin and choose **Send Selected**.
2. Pay a small amount to the host's address.
3. Look at the transaction before signing: one input, one payment, one change output.
4. Label the change output (Sparrow shows it in the transaction view). For example: `Change from paying host - came from payment 2`.
5. Sign and broadcast.

Now look at the transaction on mempool.space. What does the world see? What does the host (the receiver) now know about you?

**Bonus:** make a transaction that spends the whole coin with no change (choose an amount that uses the full coin, minus the fee). No change means nothing to track.

### Step 7: PayJoin demo (host)

1. The host shows a PayJoin-capable receiving wallet and its payment link. A PayJoin link is a normal `bitcoin:` link with an extra `pj=` part.
2. Pay it from a second wallet that supports sending PayJoin.
3. Open the transaction on mempool.space. Count inputs and outputs. Is the real amount visible?

Notes for the host, from past sessions:

- Some wallets support PayJoin version 2 (no server needed by the receiver). Others, including Sparrow, can only send version 1. Sender and receiver need a version in common.
- If a PayJoin fails, some wallets quietly send a normal payment instead. Always check the result.
- Some wallets need a minimum amount, and the receiver needs confirmed coins of their own.

### Step 8: Silent Payments demo (host)

1. Show a Silent Payments address (`sp1...`) in a wallet that supports it.
2. Send to it twice from another wallet that can send to Silent Payments.
3. On mempool.space, show that the two payments went to two different normal-looking addresses, with no link to the `sp1` address.
4. Explain the cost: the receiving wallet must scan the blockchain to find its payments, which takes more work than a normal wallet.

See [silentpayments.xyz](https://silentpayments.xyz) for the current list of wallets that send and receive.

### Step 9: Tor

1. In Sparrow's server settings, show the option to use a Tor proxy, and connecting to an Electrum server on a `.onion` address.
2. Explain: without Tor, the server your wallet uses sees your IP address and every address in your wallet. With your own node and Tor, nobody else sees either.
3. Mention Tor Browser for looking up transactions on block explorers.

### Step 10: Pick your habits

Each person writes 3 habits they will start this week. Ideas:

- A new address for every payment. Never reuse.
- Label every coin when it arrives.
- Keep KYC coins and non-KYC coins in separate wallets, or at least never spend them together.
- Use coin control for any payment where the receiver might care who you are.
- Connect your wallet to your own node, over Tor.
- Use PayJoin when both sides support it.
- Share a Silent Payments address instead of a reused donation address.

---

## Discussion questions

1. Who are you protecting your bitcoin privacy from? A thief, a nosy neighbour, a company, a government? Does the answer change your tools?
2. "I have nothing to hide." What would you say to a friend who says this?
3. Is it fair that the receiver of a PayJoin learns a little about your coins? When would you not use PayJoin?
4. Exchanges ask for ID. How does that follow your coins after you withdraw?
5. How much effort will you really spend? Which habit gives the most privacy for the least work?

## Common problems and fixes

| Problem | Fix |
|---|---|
| Only one UTXO arrived | The host sent one payment. Ask for more, or send yourself a payment to a new address to split a coin. |
| "Send Selected" does not appear | Select the coin row first in the UTXOs tab, then use the button at the bottom or the right-click menu. |
| Frozen coin still spent | It was not frozen, or another coin was frozen. Check the frozen icon in the UTXOs tab. |
| Labels disappeared | Labels are stored in the wallet file. If you made a new wallet from the seed, the labels are not there. Export labels and import them. |
| PayJoin turned into a normal payment | Version mismatch, an amount below the wallet's minimum, or the receiver had no confirmed coins. Check on mempool.space. |
| Tor connection slow | Normal. Give it a minute. |

## Safety notes

- Privacy is layers. No single tool makes you private. Combine good habits with your own node, Tor, PayJoin, Silent Payments and, for small amounts, ecash or Lightning.
- One PayJoin does not fix coins that are already linked to you.
- Block explorers and wallet servers learn what you look up. Use your own node or Tor.
- Do not talk about your holdings in public, online or offline. That is the biggest leak of all.

## Further resources

- [Sparrow Wallet docs](https://sparrowwallet.com/docs/): coin control, labels, connecting to your own node
- [payjoin.org](https://payjoin.org): how PayJoin works and which wallets support it
- [silentpayments.xyz](https://silentpayments.xyz): how Silent Payments work and which wallets support them
- [Bitcoin Optech: PayJoin](https://bitcoinops.org/en/topics/payjoin/), [Silent Payments](https://bitcoinops.org/en/topics/silent-payments/), [coin selection](https://bitcoinops.org/en/topics/coin-selection/), [CoinJoin](https://bitcoinops.org/en/topics/coinjoin/)
- [Protect your privacy on bitcoin.org](https://bitcoin.org/en/protect-your-privacy)
- [mempool.space](https://mempool.space): block explorer, also available to run on your own node
- Recap of a past session: [Sovereign Bitcoiner Workshop: Why Privacy Matters](https://codeorange.dev/session-notes/2026-10-14-sovereign-bitcoiner-workshop)
- Recap of a past session: [Privacy Track: How PayJoin Works](https://codeorange.dev/session-notes/2026-10-06-privacy-track)
- Recap of a past session: [Privacy Track: PayJoin v2, tested live](https://codeorange.dev/session-notes/2026-10-20-privacy-track)
- For developers: the [Privacy Track](../../privacy-track/README.md), with labs on [chain analysis](../../privacy-track/labs/chain-analysis/README.md), [coin selection](../../privacy-track/labs/coin-selection/README.md), [PayJoin](../../privacy-track/labs/payjoin/README.md) and [Silent Payments](../../privacy-track/labs/silent-payments/README.md)
- Related workshops: [Run your own node](../nodes/README.md) and [Ecash for everyday payments](../ecash/README.md)
