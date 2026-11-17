# Workshop: Mine Bitcoin at Home with a Bitaxe

| | |
|---|---|
| **Length** | 2 hours |
| **Level** | Beginner |
| **Audience** | Mostly non-developers and beginner developers |
| **Main tools** | The [Bitaxe](https://bitaxe.org) open-source miner and its web interface (AxeOS), a mining pool, [mempool.space](https://mempool.space) |

[Back to all workshops](../README.md)

---

## What participants leave with

1. A Bitaxe set up and hashing, on Wi-Fi, pointed at a pool, with their own payout address.
2. A simple picture of mining: guess a number, check the hash, repeat billions of times. What "hashrate" and "difficulty" mean.
3. Their own numbers: hashrate, power use in watts, cost per month in local currency, and the real odds of finding a block solo.
4. A clear view of pool mining vs solo ("lottery") mining, and why home mining matters for decentralization.

## Who this is for

Curious people with no mining or electronics background. If you can set up a Wi-Fi router, you can set up a Bitaxe. No coding.

## Materials and hardware

| Item | How many | Rough cost | Notes |
|---|---|---|---|
| Bitaxe (for example a Gamma, Supra or Ultra model) | 1 per group of 3 to 5 | USD 100 to 250 each | Buy from a seller listed by the Bitaxe project. Hashrate differs by model, from about 0.5 to over 1 TH/s. |
| Power supply for each Bitaxe | 1 per Bitaxe | USD 10 to 25 | 5 V DC with the barrel plug and amps the maker asks for. A weak supply is the top cause of crashes. |
| Power strip with enough sockets | 2 or 3 | USD 10 each | Check the venue's circuit can take the total load (it is small: a few Bitaxes use under 100 W). |
| Wi-Fi network on **2.4 GHz** with a simple password | 1 | | The Bitaxe does not join 5 GHz networks or captive portals (login pages). A travel router is the safest choice. |
| Phones or laptops to configure the Bitaxe | 1 per group | | Any device with a browser. |
| Optional: plug-in power meter | 1 or 2 | USD 10 to 20 | Lets people see real watts at the wall. |
| Optional: infrared thermometer | 1 | USD 15 | Fun for the heat block. |
| Optional: a large ASIC miner photo or video | | | To compare size, noise and power. |

## Before the session (host checklist)

- [ ] Unbox and power on every Bitaxe at home. Update each one to the latest stable AxeOS firmware from the Bitaxe project.
- [ ] Set up the travel router: 2.4 GHz, WPA2, short simple network name and password, no login page.
- [ ] Choose a pool for the session (see Step 3). Test each Bitaxe on it from your home network.
- [ ] Prepare a sheet with: Wi-Fi name and password, pool address and port, and how to write the worker name.
- [ ] Make a receive address for each group in a wallet you control, in case people do not bring one. (With a solo pool, a found block would pay this address, so use a wallet whose seed you hold safely.)
- [ ] Look up the local electricity price per kWh so the room can do the math.
- [ ] Check the network hashrate and difficulty on [mempool.space](https://mempool.space) the day before. Write them on the whiteboard.

## Run sheet

| Time | Block | Notes |
|---|---|---|
| 0:00 | Welcome and safety rules | 10 min. Power, heat, and "your seed stays at home". |
| 0:10 | What mining is | 20 min. The guessing game with dice (see Concepts). Blocks, hashes, the target, the reward. |
| 0:30 | Hands-on 1: power up and join Wi-Fi | 20 min. Steps 1 and 2. |
| 0:50 | Hands-on 2: point it at a pool | 20 min. Steps 3 and 4. |
| 1:10 | Break | 5 min. Let the miners settle and warm up. |
| 1:15 | Hands-on 3: read the numbers | 20 min. Step 5. Hashrate, shares, best difficulty, temperature, watts. |
| 1:35 | Odds, costs and heat | 15 min. Step 6. Work out the lottery odds and the monthly power cost together. |
| 1:50 | Discussion and wrap-up | 10 min. Discussion questions. Power down safely. |

**Total: 2 hours.**

---

## Concepts in five minutes

**Mining is guessing.** A miner takes a block template (a list of transactions plus a header), changes a small number called the nonce, and hashes the header with SHA-256. If the hash is below a target number, the block is valid. If not, change the nonce and try again.

**The dice game.** Give everyone a pair of dice. "To win, roll under 4." Everyone rolls. Someone wins fast. Now "roll under 3". It takes longer. That is difficulty: a lower target means more guesses on average.

**Hashrate** is guesses per second. A Bitaxe does around a trillion hashes per second (about 1 TH/s, depending on the model). The whole Bitcoin network does about a billion times more, around 1,000 EH/s (1 ZH/s). Check the live number on mempool.space.

**Difficulty adjustment.** Every 2016 blocks (about two weeks), the network changes the target so that blocks keep coming about every 10 minutes on average. More miners join: it gets harder. Miners leave: it gets easier.

**Block reward.** The miner who finds a block gets the subsidy (3.125 BTC since the 2024 halving) plus all the fees in that block.

**Pool mining.** Many miners work together and share rewards. The pool gives each miner easier "shares" to find. Shares prove how much work you did. When anyone in the pool finds a block, rewards are split by work. Steady small payouts, but a Bitaxe's share is tiny.

**Solo (lottery) mining.** You keep the whole reward if you find a block, and nothing otherwise. With a Bitaxe the chance is very small, but it is not zero. Small solo miners have found blocks.

**Why it matters.** Pools (and the people who run them) choose which transactions go into blocks. More people mining at home, and new protocols such as Stratum V2 that let miners build their own block templates, spread that power out.

## Safety rules (read these out loud)

- **Use the right power supply.** Wrong voltage can kill the board. Plug in the power supply last.
- **The heatsink gets hot.** Do not touch it while running. Keep the fan clear. Do not cover the Bitaxe.
- **Keep drinks away** from the miners and power strips.
- **Never type your seed phrase into the Bitaxe or any pool website.** A pool only needs a receive address. Nothing in mining ever needs your seed.
- Do not leave a miner running unattended on a table where people pass, or on carpet or paper.

---

## Hands-on guide

### Step 1: Power up

1. Place the Bitaxe on a hard flat surface with space around it.
2. Connect the power supply to the Bitaxe, then plug the supply into the wall.
3. The screen lights up. On first boot it shows that it is in setup mode and the name of its own Wi-Fi hotspot (something like `Bitaxe_XXXX`).

### Step 2: Join the Wi-Fi

1. On your phone or laptop, join the Bitaxe's hotspot.
2. A setup page should open. If not, open a browser and go to the address shown on the Bitaxe screen (often `192.168.4.1`).
3. Enter the workshop Wi-Fi name and password. Save. The Bitaxe restarts and joins the network.
4. The screen now shows its new IP address on the workshop network. Write it down.
5. Rejoin the workshop Wi-Fi on your phone or laptop, and open that IP address in a browser. You see the AxeOS dashboard.

**Check:** the dashboard loads and shows a hashrate (it may say zero until the pool is set).

### Step 3: Choose a pool

Two kinds of pool are good for a workshop:

- **A solo pool** (for example `solo.ckpool.org` or `public-pool.io`). If your Bitaxe finds a block, almost the whole reward goes to your address. Usually you write your Bitcoin address as the username.
- **A shared pool** that pays small amounts, often over Lightning. Good for showing steady payouts, but the payout from one Bitaxe in two hours is close to zero.

Pool addresses and ports change. Check the pool's own website on the day.

### Step 4: Enter the pool settings

In AxeOS, open the settings page and fill in:

| Field | What to put |
|---|---|
| Stratum URL | The pool address, without `stratum+tcp://` if the form asks for host only |
| Port | The pool's port |
| Stratum user | For most solo pools: `yourBitcoinAddress.workername`, for example `bc1q...xyz.workshop1` |
| Password | Often `x`, unless the pool says otherwise |

Save and restart the Bitaxe.

**Check:** after a minute the dashboard shows accepted shares rising. On the pool's website, search for your address and see your worker online.

### Step 5: Read the numbers

Walk through the dashboard together:

| Number | What it means |
|---|---|
| Hashrate | Guesses per second (GH/s or TH/s). |
| Shares accepted / rejected | Work the pool has counted. A few rejects are normal. Many means a bad connection. |
| Best difficulty | The "best" hash your miner has found so far, as a difficulty number. Compare it with the network difficulty on mempool.space. You need to reach the network difficulty to find a block. |
| ASIC temperature | Usually fine below about 65 to 70 C. Check the maker's guidance. |
| Power (W) | Watts the board reports. A plug-in meter at the wall shows a bit more (supply losses). |
| Efficiency (J/TH) | Energy per trillion hashes. Lower is better. |

Groups write their numbers on the whiteboard. Whose best difficulty is highest by the end?

### Step 6: Do the math together

**Lottery odds.** With your hashrate `h` and network hashrate `H`:

```
chance per block  = h / H
blocks per day    = about 144
chance per day    = about 144 x h / H
```

Example: a 1.2 TH/s Bitaxe against a 1,000 EH/s network:

```
h / H = 1.2e12 / 1e21 = 1.2e-9 per block
per year: 1.2e-9 x 52,560 blocks = about 0.00006, or about 1 in 16,000
```

Use today's numbers from mempool.space. The answer changes as the network grows.

**Power cost.** With power `P` watts and price `p` per kWh:

```
kWh per month = P x 24 x 30 / 1000
cost per month = kWh per month x p
```

Example: 18 W uses about 13 kWh per month. At a home price of around IDR 1,450 per kWh, that is about IDR 19,000 per month. Use your local price.

**Heat.** Every watt a miner uses becomes heat. A Bitaxe gives off about as much heat as a bright light bulb. A large ASIC miner gives off as much as a big electric heater, 3,000 W or more, plus loud fans. In cold countries people heat rooms with miners. In the tropics, heat and noise are a real cost: plan for airflow.

---

## Discussion questions

1. Would you rather have a tiny steady payout, or a tiny chance of a big one? Why?
2. If a few big pools build most block templates, what could they do? What could they not do, because of nodes?
3. Where in your country is power cheap or wasted (hydro, flared gas, unused solar)? Could mining use it?
4. A Bitaxe will very likely never find a block. Is it still worth running? Why do people do it?
5. What would make home mining easier or more common in your community?

## Common problems and fixes

| Problem | Fix |
|---|---|
| Bitaxe does not join the Wi-Fi | It needs 2.4 GHz and no login page. Check the password (case matters). Use the travel router. |
| Cannot open the dashboard | Your phone or laptop is on a different network, or still on the Bitaxe hotspot. Use the IP shown on the Bitaxe screen. |
| Hashrate zero, no shares | Wrong pool address or port, or `stratum+tcp://` typed where it should not be. Check the pool's website for the exact values. |
| Many rejected shares | Weak Wi-Fi. Move the Bitaxe closer to the router. |
| Restarts on its own | Weak power supply or a loose plug. Use the supply the maker recommends. Do not overclock in a workshop. |
| Runs very hot | Fan blocked, room hot, or overclocked. Return to default settings and give it space. |
| Pool shows no worker | The username must match what the pool expects. For solo pools, usually a valid address, with an optional `.name` on the end. |

## Safety notes

- Mining hardware only needs a **receive address**. Never enter a seed phrase anywhere in mining.
- For solo mining, use an address from a wallet you have backed up properly. If you ever do find a block, that address gets the reward.
- Do not overclock in a shared space. It raises heat and the risk of failure.
- Before buying a big ASIC miner, work out power, heat and noise first. Many people underestimate all three.
- Unplug miners at the end of the session before packing them.

## Further resources

- [Bitaxe](https://bitaxe.org) and the [Bitaxe project on GitHub](https://github.com/bitaxeorg): hardware designs, AxeOS firmware and the list of sellers
- [mempool.space mining dashboard](https://mempool.space/mining): network hashrate, difficulty and pool shares
- [How Bitcoin works on bitcoin.org](https://bitcoin.org/en/how-it-works)
- [The Bitcoin white paper](https://bitcoin.org/bitcoin.pdf), section 4 on proof of work
- Related workshop: [Run your own node](../nodes/README.md), so your miner and your node both check the rules
