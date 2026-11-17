# Week 1 exercises

[Week 1 overview](../README.md) · [Solutions](../solutions/README.md) · [Syllabus](../../README.md)

Week 1 is an intro week, so nothing here is required before the first session. Do the three core exercises after the session if you can. The hands-on lab sets up the regtest node you will use from week 2 onwards, so try to get it working before week 2.

## Core exercises

### 1. Introduce yourself on Discord

Post a short introduction in the cohort channel on Discord.

Steps:

1. Write 3 to 5 sentences: your background (what you code in, what you work on), why you joined, and one thing you would like to build with Bitcoin.
2. Read at least three other introductions and reply to one of them.

What to write down: the name of one person whose background is different from yours, and one thing you could ask them about later in the cohort.

### 2. Play with the Hash Functions tool

Open the [Hash Functions tool](https://bitcoindevs.xyz/decoding/hash-functions) on Decoding Bitcoin.

Steps:

1. Hash your name with SHA-256. Copy the output.
2. Change one letter of your name (or change a capital to a small letter) and hash it again.
3. Put the two outputs one above the other and count how many hex characters are the same in the same position.
4. Hash the empty string (no input at all). Is the output empty?
5. Hash a very long text (paste a paragraph). How long is the output now?

What to write down:

- How many of the 64 hex characters changed after one small change?
- How long is the output for a short input, the empty input and a long input?
- Can you think of any way to go from the output back to your name, other than guessing?

### 3. Look at a real transaction on mempool.space

Open [mempool.space](https://mempool.space), click a recent block, and then click any transaction in it that has at least two outputs.

Steps:

1. Write down the number of inputs and outputs, and the amount of each.
2. Write down the fee and the fee rate (sat/vB) that mempool.space shows.
3. Add up the inputs and add up the outputs. Subtract. Do you get the fee?
4. Decide which output is probably the change (the money going back to the sender).

What to write down: your guess for the change output and your reason. Clues people use: a round amount is usually the payment; the change often uses the same address type as the inputs; the change is often the "leftover" odd amount.

## Hands-on lab (bitcoin-cli, regtest)

> Tested on Bitcoin Core 29.0 (regtest), November 2026.

The full lab, including how to install Bitcoin Core (release binary or CMake build), is in [`bitcoin_core_cli.md`](bitcoin_core_cli.md). Do at least Exercises 1, 2 and 5 there. The steps below are a short version so you can check your setup quickly.

### Step 1: check your install

```bash
bitcoind -version
bitcoin-cli -version
```

**Question:** Which version do you have? You need v29 or newer for this cohort.

### Step 2: start a regtest node

```bash
bitcoind -regtest -daemon -txindex=1 -fallbackfee=0.0001
bitcoin-cli -regtest getblockchaininfo
```

**Question:** What are `chain`, `blocks` and `difficulty`? Why can your laptop mine blocks on this chain in less than a second?

### Step 3: create a wallet and mine

```bash
bitcoin-cli -regtest createwallet "mywallet"
bitcoin-cli -regtest -generate 101
bitcoin-cli -regtest getbalance
bitcoin-cli -regtest getbalances
```

**Question:** `getbalance` shows 50 BTC, but you mined 101 blocks. Where is the rest? Look at `immature` in `getbalances`.

### Step 4: hashing on the command line

Bitcoin uses SHA-256 a lot, often twice in a row ("double SHA-256" or hash256). Try it yourself:

```bash
echo -n "satoshi" | sha256sum
echo -n "satoshj" | sha256sum
python3 -c "import hashlib; d=hashlib.sha256(b'satoshi').digest(); print(hashlib.sha256(d).hexdigest())"
```

**Question:** Do the first two outputs look related in any way? Why do we need `-n` with `echo`? (Try it without `-n` and compare.)

### Step 5: look at a block header

```bash
bitcoin-cli -regtest getblockheader "$(bitcoin-cli -regtest getbestblockhash)"
```

**Question:** Which fields of the header point to other data (another block, the transactions)? Which hash function links the blocks together?

## Stretch tasks

- Do Exercises 3 and 4 in [`bitcoin_core_cli.md`](bitcoin_core_cli.md) (decode a raw transaction, explore a block).
- Change one bit of an input and count how many of the 256 output bits flip. Do it ten times. You should see close to half (128) every time. This is called the avalanche effect.

  ```bash
  python3 -c "
  import hashlib
  a = hashlib.sha256(b'satoshi').digest()
  b = hashlib.sha256(b'satoshj').digest()
  print(sum(bin(x ^ y).count('1') for x, y in zip(a, b)), 'of 256 bits differ')
  "
  ```
- Read section 1 and section 2 of the [Bitcoin whitepaper](https://bitcoin.org/bitcoin.pdf). How does its definition of "an electronic coin" match what you saw on mempool.space?
- Try the optional [Interactive Developer Roadmap](https://bitcoindevs.xyz/decoding/interactive-roadmap) and pick one topic you want to understand by week 10.
