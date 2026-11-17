# Workshop: Build a 2-of-3 Multisig Wallet

| | |
|---|---|
| **Length** | 2.5 hours |
| **Level** | Beginner (you have sent and received bitcoin before) |
| **Audience** | Mostly non-developers and beginner developers |
| **Main tools** | [Sparrow Wallet](https://sparrowwallet.com), hardware wallets from different makers (or Sparrow hot wallets on testnet), [Nunchuk](https://nunchuk.io) for the restore |

[Back to all workshops](../README.md)

---

## What participants leave with

1. A working 2-of-3 multisig wallet on testnet or signet, built in Sparrow.
2. Experience signing one transaction with two different keys and passing a PSBT between them.
3. A printed or handwritten backup plan: where each seed goes, and where the wallet file (output descriptor) goes.
4. Proof that the backup works: the same wallet rebuilt in a second app from the descriptor.
5. A clear idea of their next step. For most people that is one hardware wallet first, then a passphrase, then multisig.

## Who this is for

People who already hold a little bitcoin, or want to, and worry about losing it. No coding needed. If someone has never sent bitcoin, pair them with a helper for the first 20 minutes.

## Materials and hardware

| Item | How many | Rough cost | Notes |
|---|---|---|---|
| Laptop with [Sparrow Wallet](https://sparrowwallet.com/download/) | 1 per person or per pair | Free | Windows, macOS or Linux. Sparrow is desktop only. |
| Hardware wallets from 2 or 3 different makers | 1 set for the host demo | USD 60 to 250 each | For example a Trezor, a BitBox02, a Blockstream Jade, a Coldcard. Bought straight from the maker. |
| Spare hardware wallets for participants | Optional | Same as above | Only for testnet use. Wipe them at the end. |
| USB cables (USB-C and micro-USB) | A few spare | USD 3 to 5 each | Bad cables cause most "device not found" problems. |
| microSD cards and a reader | 1 or 2 | USD 5 to 10 | Only if you show an air-gapped signer. |
| Seed backup cards (paper) | 3 per person | Free | Print them. Collect and shred the test ones at the end. |
| Projector or big screen | 1 | | For the live demo. |
| Test coins (testnet4 or signet) | About 0.01 test BTC per person | Free | Collect from a faucet before the day. |

Hardware wallets are optional for participants. Everyone can build the same wallet with three Sparrow software keys on testnet. The host demo with real devices shows how it looks in real life.

## Before the session (host checklist)

- [ ] Install the latest Sparrow on your demo laptop. Verify the download using the steps on the Sparrow download page.
- [ ] Decide on the network: **testnet4** or **signet**. Everyone must use the same one. Sparrow can restart on these networks from its menu (look for a "Restart in" option under Tools).
- [ ] Make one "faucet wallet" in Sparrow on that network and fill it with test coins. You will send coins from it to each participant. Public faucets are slow and often empty, so do this days before.
- [ ] Update the firmware on your demo hardware wallets and make sure each one can connect to Sparrow on test networks. Some devices need a setting to allow testnet.
- [ ] Do the whole hands-on guide once, start to finish, on a clean laptop. Write down every snag.
- [ ] Check that Sparrow can connect to a public server from the venue Wi-Fi. If not, bring a phone hotspot.
- [ ] Print the seed cards and the backup plan worksheet (a table with 3 rows: key, where the seed lives, where a copy of the wallet file lives).
- [ ] Send the "what to install" message: Sparrow from the official site only. **There is no Sparrow mobile app.** A "Sparrow" app on a phone is a scam.

## Run sheet

| Time | Block | Notes |
|---|---|---|
| 0:00 | Welcome and safety rules | 10 min. Read the safety rules out loud. Ask who holds bitcoin on an exchange, a phone wallet, a hardware wallet. |
| 0:10 | Why multisig? | 20 min. Single points of failure. The supply chain story: what if your one device brand has a bug? 2-of-3 explained with three house keys. |
| 0:30 | Live demo by the host | 20 min. Build a 2-of-3 from three different hardware wallets. Show the descriptor. |
| 0:50 | Setup check | 10 min. Everyone opens Sparrow on the test network and connects to a server. |
| 1:00 | Hands-on 1: make three keys and the wallet | 25 min. Steps 1 to 3. |
| 1:25 | Break | 5 min. Host sends test coins while people stretch. |
| 1:30 | Hands-on 2: receive and spend with two keys | 25 min. Steps 4 and 5. |
| 1:55 | Hands-on 3: back up and restore elsewhere | 20 min. Steps 6 and 7. |
| 2:15 | Discussion and backup plan | 10 min. Fill in the worksheet. Discussion questions. |
| 2:25 | Wrap-up | 5 min. Wipe test devices, shred test seed cards, share links. |

**Total: 2 hours 30 minutes.**

---

## Concepts in five minutes

**A single-signature wallet** has one seed. Whoever has the seed has the coins. Lose it and the coins are gone.

**A 2-of-3 multisig wallet** has three keys. Any two can spend. So:

- Lose one key: you still have two and can move the coins.
- A thief steals one key: it is not enough to spend.
- One hardware wallet brand has a bug: your other two keys still protect you.

**The output descriptor (wallet file)** is the blueprint. It lists the three public keys (xpubs), their fingerprints and paths, and the rule "2 of 3". You need it to rebuild the wallet. Two seeds alone are not enough to find your coins easily.

> The wallet file matters as much as the keys.

Anyone who finds the descriptor can see your balance and history, but cannot spend. So keep copies of it in many places, and keep each seed in a different place.

**A PSBT** (partially signed bitcoin transaction) is a transaction that is passed around for signatures. Key 1 signs, then key 2 signs, then you broadcast.

## Safety rules (read these out loud)

- **Never type a real seed phrase into a laptop, a website, a chat or an AI assistant.** Real seeds go only into a hardware wallet.
- **Today we use test coins only.** Test coins have no value. Every seed made today is a throwaway.
- **Never photograph seed words.** Not even test ones. It builds a bad habit, and photos sync to the cloud.
- **Do not reuse a device you hold real bitcoin on** for this workshop unless you know exactly what you are doing. Use a spare or software keys.
- Buy hardware wallets straight from the maker, never from a reseller or a marketplace.

---

## Hands-on guide

### Step 0: Open Sparrow on the test network

1. Open Sparrow.
2. Use the Tools menu to restart Sparrow in **testnet4** or **signet** (the one the host picked). The window title and the status bar now show the network name.
3. Go to the server settings (Preferences, then Server). Choose a **public server** for now and press "Test connection". You should see a green check.

**Check:** the bottom right corner of Sparrow shows a connected icon.

### Step 1: Make three keys

You need three keystores. Pick one path:

**Path A: three software keys (everyone can do this).**

You will make the three seeds inside the multisig wallet in Step 2. Have seed cards A, B and C ready. Each time Sparrow shows new words, write them on the next card by hand and confirm them.

In real life each key would live on its own hardware wallet, in a different place. Three software keys on one laptop are only for learning.

**Path B: hardware wallets (host demo, or helpers with spare devices).**

1. Set up each device as new. Write each seed on its own card.
2. Keep the devices ready. You will connect them in Step 2.

### Step 2: Build the multisig wallet

1. File, then New Wallet. Name it `family-vault`.
2. Policy type: **Multi Signature**. Move the slider to **2 of 3**.
3. Script type: **Native Segwit (P2WSH)**.
4. You now see three keystore tabs. For each one:
   - **Software key:** choose "New or Imported Software Wallet", generate a new 12-word seed, write it on the card and confirm it. (On a test network, with a throwaway seed, this is fine. With real coins you would never make or type a seed on a laptop.)
   - **Hardware wallet over USB:** plug in, unlock with the PIN, choose "Connected Hardware Wallet", Scan, then Import Keystore.
   - **Air-gapped signer (for example a Coldcard over microSD, or a QR signer):** export the multisig keystore on the device, then choose "Airgapped Hardware Wallet" in Sparrow and load the file or scan the QR code.
5. Look at the derivation path of each key. On a test network a native segwit multisig path ends like `m/48'/1'/0'/2'`. On mainnet the `1'` is a `0'`. This comes from [BIP 48](https://github.com/bitcoin/bips/blob/master/bip-0048.mediawiki).
6. Press **Apply**. Set a password for the wallet file if asked.

**Check:** the Receive tab shows an address that starts with `tb1q` (testnet and signet) and is longer than a normal single-sig address.

### Step 3: Look at the descriptor

1. Open the wallet Settings tab. Find the output descriptor box.
2. Read it together. Point out:
   - `wsh(sortedmulti(2,...))`: "witness script, 2 of these keys".
   - Three `[fingerprint/path]xpub` parts, one per key.
3. Ask: "Could a stranger spend with this?" (No.) "Could a stranger see your balance with this?" (Yes.)

### Step 4: Receive test coins

1. Go to the Receive tab and show the QR code or copy the address.
2. The host sends test coins from the faucet wallet. One payment per person.
3. Watch it appear in the Transactions tab. On signet a block comes about every 10 minutes, so it may stay unconfirmed for a while. That is fine.

**Tip:** while waiting, check the address on [mempool.space](https://mempool.space) using its signet or testnet4 view.

### Step 5: Spend with two keys

1. Go to the Send tab. Pay a small amount to an address the host gives you (or back to the faucet wallet).
2. Press **Create Transaction**. You now have an unsigned PSBT.
3. Press **Sign**. Sparrow asks which keystore signs. Sign with key A.
4. Sign again with key B. The status now shows 2 of 2 needed signatures.
5. Press **Broadcast**.

With hardware wallets, the device shows the address and amount. **Read them on the device screen before you approve.** That screen is the one you can trust. For an air-gapped device, save the PSBT to the microSD card (or show it as a QR code), sign on the device, and load the signed file back into Sparrow.

**Check:** the transaction appears in the Transactions tab and on mempool.space.

### Step 6: Back up the wallet file

1. In the wallet Settings, use Export. Save the descriptor (or a BSMS file, or the PDF with a QR code).
2. Fill in the backup plan worksheet:

| Key | Where the seed lives | Where a copy of the wallet file lives |
|---|---|---|
| A | Home | Home, with seed A |
| B | Family member's house | With seed B |
| C | Safe deposit box or office | With seed C |

Each place has one seed plus a copy of the wallet file. Any two places together can spend and rebuild everything.

### Step 7: Restore in a second app

This proves the backup works. Do it now, while the stakes are low.

1. Install [Nunchuk](https://nunchuk.io) (desktop or phone), set to the same test network if the app supports it. If not, do this step in a second Sparrow wallet instead: File, then New Wallet, then import the descriptor.
2. Choose to recover or import an existing wallet using a descriptor or BSMS file.
3. Load the file you exported in Step 6.
4. **Check:** the first receive address in the new app matches the first address in Sparrow, and the balance matches.

A past session found that importing the raw descriptor text needed manual edits in some apps, while the exported file worked first time. If one format fails, try the other.

---

## Discussion questions

1. Where would you keep three keys so that one fire, one flood or one burglar cannot take two of them?
2. What happens to your bitcoin if you die tomorrow? Who would find the keys, and would they know what to do?
3. Why use three different hardware wallet makers? What does that protect against?
4. Is 2-of-3 always better than one hardware wallet with a good backup? When is it too complex?
5. Your descriptor shows your balance to whoever finds it. Is that a problem for you?

## Common problems and fixes

| Problem | Fix |
|---|---|
| Sparrow does not see the hardware wallet | Try another USB cable (many are charge-only). Unlock the device first. Close other wallet apps (Ledger Live, Trezor Suite) that may hold the USB connection. On Linux you may need udev rules: Sparrow's docs explain it. |
| Device refuses to work on testnet | Some devices need a testnet or "advanced" setting turned on. Others do not support signet. Use software keys for that keystore. |
| Different paths on different keys | Every key must use the multisig path (`m/48'/.../2'`). If one shows `m/84'/...`, it was imported as single-sig. Remove it and import it again from the multisig tab. |
| Test coins never arrive | Check that everyone is on the same network (testnet4 vs signet vs old testnet3). Check the address prefix. |
| "Not enough signatures" when broadcasting | You signed with only one key. Sign again with a second keystore. |
| Restored wallet shows a different address | The script type or key order differs, or one key is wrong. Re-import from the exported file, not by retyping. |
| Unconfirmed for a long time | Normal on test networks. Move on and check later. |

## Safety notes for the real world

- **Climb one step at a time:** a phone wallet with a small amount to practise, then one hardware wallet, then a passphrase, then multisig.
- **The most likely way to lose bitcoin is your own mistake,** not a hacker. Test your restore with a small amount before you move savings.
- **Seeds are written on paper or metal, never typed into a computer.** In real multisig, each seed lives only in its hardware wallet and on its backup.
- Keep each seed in a different place. Keep a copy of the wallet file with each seed.
- Write simple instructions for your family. Do not write the seeds into those instructions.
- At the end of this workshop, wipe any shared test devices and shred the test seed cards.

## Further resources

- [Sparrow Wallet docs](https://sparrowwallet.com/docs/): the multisig and best-practice guides
- [Nunchuk](https://nunchuk.io): multisig wallet for desktop and phone, good for restoring and for inheritance planning
- [BIP 48: multisig derivation paths](https://github.com/bitcoin/bips/blob/master/bip-0048.mediawiki)
- [Bitcoin Optech: output script descriptors](https://bitcoinops.org/en/topics/output-script-descriptors/)
- [Bitcoin Optech: PSBT](https://bitcoinops.org/en/topics/psbt/)
- [Choose your wallet on bitcoin.org](https://bitcoin.org/en/choose-your-wallet)
- [mempool.space](https://mempool.space): block explorer with signet and testnet4 views
- Recap of a past session: [Self-Custody Workshop: Build a Multi-vendor Multisig](https://codeorange.dev/session-notes/2026-10-16-self-custody-workshop)
- Next workshops: [Run your own node](../nodes/README.md) so your multisig talks to your own server, and [Bitcoin privacy in practice](../privacy/README.md)
