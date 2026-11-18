# Workshop: Run Your Own Bitcoin Node

| | |
|---|---|
| **Length** | 2.5 hours |
| **Level** | Beginner |
| **Audience** | Mostly non-developers and beginner developers |
| **Main tools** | [Bitcoin Core](https://bitcoincore.org), a node box such as [Umbrel](https://umbrel.com) or [Start9](https://start9.com), an Electrum server app, [Sparrow Wallet](https://sparrowwallet.com) |

[Back to all workshops](../README.md)

---

## What participants leave with

1. A clear answer to "why run a node?": you check the rules yourself and stop telling a stranger's server about your addresses.
2. Bitcoin Core installed on their own laptop, running on **signet** with pruning on, plus a few commands they can run in the console.
3. Sparrow Wallet connected to a real node through an Electrum server, over the local network or over Tor.
4. A shopping list and a plan for a home node (hardware, disk size, how long the first sync takes).

## Who this is for

Anyone who uses a Bitcoin wallet and wants to stop trusting someone else's server. No coding needed. Comfort with installing apps helps. A few commands are typed, and helpers walk the room.

## Materials and hardware

| Item | How many | Rough cost | Notes |
|---|---|---|---|
| Laptop with 20 GB free disk space | 1 per person or per pair | | For Bitcoin Core on signet with pruning. |
| A **fully synced** demo node (Umbrel, Start9, or a mini PC with Bitcoin Core) | 1, brought by the host | USD 300 to 700 | Mini PC (or Umbrel Home / Start9 server) with a 2 TB SSD. Sync it at home before the day. |
| Electrum server app on the demo node (Electrs or Fulcrum) | 1 | Free | Install from the node's app store. Let it finish indexing before the day. |
| Small travel router or reliable Wi-Fi | 1 | USD 30 to 60 | Participants connect to the demo node on the same network. |
| Projector or big screen | 1 | | |
| Printed "node shopping list" | 1 per person | | See the table in the hands-on guide. |

**Why the host brings a synced node:** the first full sync of mainnet downloads the whole blockchain, which is several hundred GB and growing. It takes from many hours to over a week, depending on the hardware. It cannot happen in a 2.5 hour workshop.

## Before the session (host checklist)

- [ ] Sync your demo node fully at home, including the Electrum server index. Check it again the day before.
- [ ] Note the demo node's local address (for example `umbrel.local` or an IP like `192.168.1.50`) and the Electrum server port shown in the app (often `50001` for plain TCP).
- [ ] Note the Electrum server's **Tor .onion address**, shown in the Electrum server app's connect screen on Umbrel or in the service's interfaces on Start9.
- [ ] Test from another laptop: connect Sparrow to the demo node over the LAN and over Tor.
- [ ] Download the current Bitcoin Core installers for Windows, macOS and Linux from [bitcoincore.org](https://bitcoincore.org/en/download/) to a USB stick, in case the venue internet is slow.
- [ ] Check that the venue Wi-Fi lets laptops talk to each other. Many guest networks block this ("client isolation"). If so, use your own travel router.
- [ ] Prepare a shared text file with the commands from this guide, so people can copy them.

## Run sheet

| Time | Block | Notes |
|---|---|---|
| 0:00 | Welcome and safety rules | 10 min. Ask: whose wallet talks to whose server today? |
| 0:10 | What a node does | 20 min. Downloads every block, checks every rule, keeps the UTXO set, shares blocks with peers. Show the 21 million check. |
| 0:30 | Tour of the demo node | 15 min. Umbrel or Start9 dashboard: sync status, peers, disk use, apps. |
| 0:45 | Hands-on 1: install Bitcoin Core on signet with pruning | 30 min. Steps 1 to 3. |
| 1:15 | Break | 10 min. Let the signet sync run. |
| 1:25 | Hands-on 2: talk to your node | 20 min. Step 4. Console commands. |
| 1:45 | Hands-on 3: connect a wallet to a node | 25 min. Steps 5 and 6. LAN first, then Tor. |
| 2:10 | Planning your home node | 10 min. Step 7. Hardware, disk, power, time. |
| 2:20 | Discussion and wrap-up | 10 min. Discussion questions. |

**Total: 2 hours 30 minutes.**

---

## Concepts in five minutes

**A node** is software that downloads every block and checks every rule by itself: no coins from nothing, no double spends, valid signatures, the supply schedule. If a block breaks a rule, your node rejects it, no matter who mined it.

**Your wallet needs a server.** A phone or desktop wallet asks a server "do these addresses have coins?". If that server belongs to someone else, they learn your addresses, your balance and often your IP address. With your own node, you ask yourself.

**Pruning.** A pruned node still downloads and checks every block, then deletes old block files to save space. It keeps what it needs to check new blocks and follow your wallet. You can prune down to about 550 MB of block files. The trade-off: a pruned node cannot serve old blocks to others, and some apps (like an Electrum server) need the full chain.

**Electrum server.** Bitcoin Core does not answer "which transactions touch this address?" quickly. An Electrum server (Electrs or Fulcrum) builds that index on top of your node, so wallets like Sparrow, BlueWallet or Nunchuk can use it.

**Tor** hides your IP address. Connecting your wallet to your node over Tor works from anywhere, without opening ports on your home router.

**Signet** is a test network. Coins have no value, and the chain is much smaller than mainnet, so a laptop can sync it in a workshop.

## Safety rules (read these out loud)

- **We use signet today.** No real coins, no real seeds.
- **Never type a real seed phrase into a laptop or website** to "connect" a wallet to a node. A wallet connects to a node with an address and port, never with your seed.
- Only download Bitcoin Core from [bitcoincore.org](https://bitcoincore.org). Search ads for "Bitcoin Core download" can lead to fake sites.
- The node's Tor address and any connection string or password are private. Do not post them in a public chat.

---

## Hands-on guide

### Step 1: Install Bitcoin Core

1. Download Bitcoin Core for your system from [bitcoincore.org/en/download](https://bitcoincore.org/en/download/) (or from the host's USB stick).
2. Optional, for the curious: verify the download with the SHA256SUMS file. The download page explains how.
3. Install it. **Do not start it yet** if it would start on mainnet. We set signet first.

### Step 2: Set signet and pruning

Create a file called `bitcoin.conf` in the Bitcoin data folder:

| System | Data folder |
|---|---|
| Windows | `%LOCALAPPDATA%\Bitcoin\` (older versions used `%APPDATA%\Bitcoin\`) |
| macOS | `~/Library/Application Support/Bitcoin/` |
| Linux | `~/.bitcoin/` |

Put these lines in it:

```
signet=1
prune=550
server=1
```

`signet=1` runs on signet. `prune=550` keeps about 550 MB of block files. `server=1` lets `bitcoin-cli` talk to the node.

If someone prefers clicks: start Bitcoin Core with the GUI, and on the first-run screen choose a custom data folder and tick "Limit block chain storage" (pruning). To start on signet from the GUI, start it with the `-signet` option, or use the config file above.

### Step 3: Start the node and watch it sync

1. Start Bitcoin Core (the GUI `bitcoin-qt`, or `bitcoind` in a terminal).
2. The GUI shows a progress bar with "blocks remaining". The window title says `[signet]`.
3. While it syncs, the host explains what is happening: download block, check proof of work, check every transaction, update the UTXO set.

**Check:** the progress bar moves and the peer count (bottom right of the GUI) is more than zero.

### Step 4: Talk to your node

Open the console: in the GUI, Window, then Console. Or in a terminal use `bitcoin-cli -signet`.

```
getblockchaininfo
```

Look for `chain` (should be `signet`), `blocks`, `headers`, `verificationprogress` and `pruned` (should be `true`).

```
getnetworkinfo
getpeerinfo
```

How many peers do you have? Are any of them on Tor (`onion`)?

```
getblockhash 1000
getblock <paste the hash>
```

You just read block 1000 from your own copy. Nobody else told you what is in it.

```
gettxoutsetinfo
```

This can take a minute. `total_amount` is the total coins in existence on this chain, counted by your own node. On mainnet this is how you check the 21 million cap yourself.

If `gettxoutsetinfo` is slow, run it once on the host's synced mainnet node and show the result on screen.

### Step 5: Connect Sparrow to the demo node over the local network

1. Install [Sparrow Wallet](https://sparrowwallet.com/download/) if you do not have it. Restart it on signet or stay on mainnet, depending on the host's demo node. (A mainnet node is fine here: we only connect and look, we send nothing.)
2. Open Sparrow's server settings (Preferences, then Server).
3. Choose **Private Electrum** server.
4. Enter the demo node's local address and port, for example `umbrel.local` and `50001`. Leave SSL off for plain TCP on the local network.
5. Press **Test connection**.

**Check:** Sparrow shows a green check and the server version. The status bar icon shows you are connected to a private server.

Ask the room: "When you load a wallet now, who learns your addresses?" (Only the demo node, which in real life is your own box at home.)

### Step 6: Connect over Tor

1. In the same server settings, replace the address with the Electrum server's **.onion address** from the host.
2. Sparrow can reach .onion addresses through its built-in Tor support. If it asks about a proxy, leave the proxy off and let Sparrow use its own Tor, or point it to a Tor proxy you run (for example Tor Browser on port `9150`).
3. Press **Test connection**. Tor is slower. Give it up to a minute.

**Check:** a green check with the .onion address. This works from anywhere in the world, with no open ports on the home router.

Mobile wallets can do the same. For example, a phone wallet with an Electrum server setting can use the .onion address while the phone runs a Tor app (Orbot on Android).

### Step 7: Plan your home node

Fill in this table together:

| Option | Rough cost | Good for | Trade-offs |
|---|---|---|---|
| Bitcoin Core on your everyday laptop, pruned | Free | Learning, checking rules | Only runs when the laptop is on. Pruned, so no Electrum server. |
| Old laptop or mini PC with a 2 TB SSD, Bitcoin Core plus Electrs | USD 150 to 400 | Cheap, always on | You install and update things yourself. |
| [Umbrel](https://umbrel.com) on your own mini PC, or an Umbrel Home | USD 300 to 700 | One-click apps: Electrum server, Lightning, BTCPay Server, mempool | Trust the Umbrel app store for updates. |
| [Start9](https://start9.com) server or StartOS on your own hardware | USD 300 to 700 | One-click services, strong focus on Tor and backups | Same as above, different app store. |

Things to plan for:

- **Disk:** at least 2 TB SSD for a full (unpruned) node with an Electrum server. Not a spinning hard disk: it makes the first sync very slow.
- **Time:** the first sync can take from a day to more than a week on small hardware.
- **Power:** a mini PC uses roughly 10 to 30 watts. Plan for power cuts with a small UPS if they are common where you live.
- **Internet:** the first sync downloads several hundred GB. After that, it is a few GB per day or less, depending on how many peers you serve.

---

## Discussion questions

1. Before today, whose server did your wallet ask about your balance? What could that server learn about you?
2. If a mining pool made a block with 100 extra bitcoin in it, what would your node do?
3. Is a pruned node "less of a node"? What can it do, and what can it not do?
4. Who in your family or community could share one home node? What are the trust trade-offs?
5. Umbrel and Start9 make things easy by running an app store. What do you trust when you install an app from it?

## Common problems and fixes

| Problem | Fix |
|---|---|
| Bitcoin Core started syncing mainnet by mistake | Close it. Add `signet=1` to `bitcoin.conf` in the right folder, or start with `-signet`. Delete the mainnet `blocks` and `chainstate` folders if space is short. |
| `bitcoin.conf` is ignored | The file is in the wrong folder or saved as `bitcoin.conf.txt` (Windows hides extensions). In the GUI, Settings, then Options, shows a button to open the config file. |
| `bitcoin-cli` says it cannot connect | The node is not running, or `server=1` is missing, or you forgot `-signet`. |
| Zero peers | Venue firewall blocks port 38333 (signet) or outgoing connections. Try a phone hotspot. |
| Sparrow cannot reach `umbrel.local` | The laptop and node are not on the same network, or the network blocks device-to-device traffic. Use the node's IP address, or the travel router. |
| Sparrow connection test fails on the right address | The Electrum server is still indexing. Check its app page on the node. |
| Tor connection times out | Tor can take a minute to start. Try again. Check the .onion address was copied exactly. |
| Laptop disk fills up | Check `prune=550` is set. Pruning only applies to the active network's folder. |

## Safety notes

- A node never needs your seed. Anything that asks for your seed to "sync" or "connect to a node" is a scam.
- Keep your node's software up to date, but update from the official sources only.
- If you expose your node to the internet without Tor, your IP address is linked to "this person runs a Bitcoin node". Tor avoids that.
- A node with a Lightning wallet or BTCPay Server on it holds hot keys. Back up what each app tells you to back up, and treat that box like a wallet.

## Further resources

- [Bitcoin Core](https://bitcoincore.org) and its [download page](https://bitcoincore.org/en/download/)
- [Running a full node on bitcoin.org](https://bitcoin.org/en/full-node): requirements and settings, including pruning
- [Umbrel](https://umbrel.com) and [Start9](https://start9.com): node operating systems with app stores
- [Sparrow Wallet docs](https://sparrowwallet.com/docs/): includes a guide on connecting Sparrow to your own node
- [mempool.space](https://mempool.space): also available as an app to run on your own node
- [Bitcoin Optech: anonymity networks](https://bitcoinops.org/en/topics/anonymity-networks/): Tor and I2P for Bitcoin nodes
- Recap of a past session: [Sovereign Bitcoiner Workshop: Why Privacy Matters](https://codeorange.dev/session-notes/2026-10-14-sovereign-bitcoiner-workshop) (your own node behind Tor as one layer of privacy)
- Recap of a past session: [Agentic Engineering & Coding Workshop](https://codeorange.dev/session-notes/2026-10-21-agentic-engineering) (an Umbrel running BTCPay Server for a tip button)
- For developers: the [Privacy Track network privacy lab](../../privacy-track/labs/network-privacy/README.md) and the [compact block filters lab](../../privacy-track/labs/compact-block-filters/README.md)
- Next workshops: [Accept bitcoin with BTCPay Server](../btcpay/README.md) runs on a node like this one, and [Build a 2-of-3 multisig](../multisig/README.md)
