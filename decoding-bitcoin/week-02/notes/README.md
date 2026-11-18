# Week 2 notes

[Week 2 overview](../README.md) · [Exercises](../exercises/README.md) · [Solutions](../solutions/README.md) · [Slides](../slides/slides.md)

## Key ideas

- **Wallets build, nodes verify.** The wallet does the creative work: choosing coins, making outputs, signing. Nodes only check. Every node checks every transaction itself, first when it arrives and again when it appears in a block.

- **Each node has its own mempool.** The mempool is a node's private list of valid transactions that are not in a block yet. Nodes hear about transactions at different times, have different limits and policies, and may see conflicting transactions in a different order. So mempools are similar but never guaranteed to be the same. Only the blockchain is agreed on.

- **Confirmation is about probability.** A transaction in a block has 1 confirmation. A reorg can still remove that block. Every block mined on top makes that much harder. There is no moment when a payment becomes final in a mathematical sense. Each receiver decides how many confirmations are enough for the amount at risk.

- **Reorgs are normal at small depth.** When two miners find blocks at nearly the same time, nodes briefly disagree. The next block settles it, and the losing block's transactions go back to the mempool. Deep reorgs need a lot of hashrate, and that is what an attacker would need for a double spend.

- **Outputs are spent whole.** You cannot spend part of a UTXO. A payment spends whole coins and creates new ones: the payment, a change output back to yourself, and whatever is left over is the fee.

- **A transaction is a short list of parts.** Version, inputs, outputs and locktime (plus marker, flag and witness for segwit). There is no sender field, no fee field and no input amount. An input only names an outpoint (`txid:vout`), and nodes look up the rest in their UTXO set.

- **Proof of ownership is a script check.** To spend an output, the input must provide data (usually a signature and public key) that makes the output's locking script succeed. That, plus the outpoint being unspent, is all a node needs.

## Common mix-ups

| Mix-up | Correction |
|---|---|
| "The mempool" is one global list. | Every node has its own. mempool.space shows the mempool of mempool.space's nodes. |
| A transaction with 1 confirmation is final. | It can be removed by a reorg. Confirmations reduce risk; they never make it zero. |
| The fee is a field in the transaction. | The fee is inputs minus outputs. Nobody writes it down. |
| An input contains the amount being spent. | An input only names the outpoint. The amount is in the previous transaction's output. |
| Change goes back into the same output. | The old output is completely spent. Change is a brand new output, usually to a new address. |
| `sendrawtransaction` needs your wallet. | A signed transaction needs no secrets to broadcast. Any node can relay it. |

## Session plan

| Time | Block | Who | Notes |
|---|---|---|---|
| 0:00-0:05 | Welcome and roles | Facilitator | Confirm roles and question owners |
| 0:05-0:15 | Opening question | Facilitator | "When is a payment final, and who decides?" Push for specifics |
| 0:15-0:30 | Concepts | Facilitator | Slides 5-9: lifecycle, mempool, reorgs, change, parts of a transaction |
| 0:30-1:05 | Question round | Question owners, devil's advocate | 6 questions, about 6 minutes each: 2-3 minutes explaining, then discussion |
| 1:05-1:20 | Exercise walkthrough | Exercise driver | Lab steps 7-10: manual transaction, forgotten-change mistake, child transaction |
| 1:20-1:27 | Takeaways | Summariser | Read back 3 takeaways, collect open questions |
| 1:27-1:30 | Before next Monday | Facilitator | Week 3 lessons, assign roles and questions |

## Facilitator tips

Before the session:

- Run the lab yourself on a fresh regtest chain, so you know the output and the errors.
- Check that the exercise driver has a working node and has done steps 1 to 6 already, so the walkthrough starts at step 7.
- Have mempool.space open to show projected blocks and a transaction going from unconfirmed to confirmed.
- Try the Reorg Calculator with 10% hashrate and note the numbers it shows, since it may use a different formula from the whitepaper.

Where people get stuck:

- **"Fee estimation failed. Fallbackfee is disabled."** The node needs `-fallbackfee=0.0001`. Restart `bitcoind` with it.
- **"Multiple wallets are loaded. Please select which wallet to use..."** (error code -19; before v29 the message was "Wallet file not specified"). With two wallets loaded, every wallet command needs `-rpcwallet=alice` or `-rpcwallet=bob`, including `-generate`.
- **Shell quoting.** The JSON for `createrawtransaction` is easy to break. Have people `echo "$INPUTS"` and `echo "$OUTPUTS"` to see what they built. Amounts must be numbers (no quotes), and txids must be in quotes.
- **Wrong change amount.** If inputs minus outputs is negative, signing works but `testmempoolaccept` fails with an error about values (`bad-txns-in-belowout`). Check the arithmetic.
- **Choosing an immature coinbase.** `listunspent` only lists spendable coins, but if someone copies a txid from `getblock`, the spend fails as premature. Use `listunspent`.
- **Thinking the mempool is global.** Stretch task B (two nodes) is a nice quick demo if the group is curious.

## Glossary

- **Mempool:** a node's set of valid, unconfirmed transactions.
- **Relay:** passing a transaction or block on to peers.
- **Policy:** a node's own rules for what it accepts and relays (fee minimums, standard scripts). Stricter than consensus, and can differ between nodes.
- **Consensus rules:** rules every node must apply to blocks. Breaking them makes a block invalid.
- **Confirmation:** a transaction has N confirmations when its block and N-1 blocks on top of it are in the chain.
- **Reorg (chain reorganisation):** switching to a different chain with more work, which disconnects blocks at the tip.
- **Double spend:** two transactions that spend the same coin. Only one can confirm.
- **Outpoint:** a reference to an output: `txid:vout`.
- **Change output:** an output that returns the leftover value to the sender.
- **scriptPubKey (locking script):** the condition in an output that must be met to spend it.
- **scriptSig / witness (unlocking data):** the data in an input that meets the condition.
- **Locktime:** the earliest block height or time a transaction can be included in a block.

## Further resources

- [Bitcoin whitepaper](https://bitcoin.org/bitcoin.pdf), section 11, "Calculations": the attacker catch-up probabilities behind the Reorg Calculator.
- [learnmeabitcoin: Transaction](https://learnmeabitcoin.com/technical/transaction/): the parts of a transaction with diagrams.
- [Mastering Bitcoin](https://github.com/bitcoinbook/bitcoinbook): the chapter on transactions.
- [Learning Bitcoin from the Command Line](https://github.com/BlockchainCommons/Learning-Bitcoin-from-the-Command-Line): chapter 4 covers sending transactions, including raw transactions, with `bitcoin-cli`.
- [Bitcoin Core RPC reference: createrawtransaction](https://developer.bitcoin.org/reference/rpc/createrawtransaction.html) and [getmempoolentry](https://developer.bitcoin.org/reference/rpc/getmempoolentry.html). These pages are for an older version; `bitcoin-cli help <command>` shows the current help.
- [mempool.space](https://mempool.space): live view of mempools and blocks.
