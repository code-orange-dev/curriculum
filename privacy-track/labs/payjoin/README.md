# Payjoin Lab (S6): Paying Together

Do an async payjoin (BIP77) between two wallets, then play the chain analyst and catch the common-input heuristic getting it wrong.

**Needs:** Docker, [`nigiri`](https://github.com/vulpemventures/nigiri) (one-command regtest), Rust/`cargo`, `jq`.

## 1. Do the payjoin

Follow the official [payjoin-cli Quick Start](https://github.com/payjoin/rust-payjoin/tree/master/payjoin-cli#quick-start). It's maintained upstream, so it stays current. In short:

1. `nigiri start`, then create and fund two wallets: `sender` and `receiver`
2. `cargo install payjoin-cli`, and write a `config.toml` for each side
3. In `receiver/`: `payjoin-cli receive 10000`, which prints a BIP21 URI with a `pj=` parameter
4. In `sender/`: `payjoin-cli send "<that URI>" --fee-rate 1`
5. Mine a block: `nigiri rpc generatetoaddress 1 $(nigiri rpc -rpcwallet=sender getnewaddress)`

Work in pairs: one person runs the receiver, the other the sender, then swap. With v2 the receiver can go offline between steps 3 and 4. Try it and see.

## 2. Find the transaction

```bash
TXID=$(nigiri rpc -rpcwallet=receiver listtransactions "*" 1 | jq -r '.[0].txid')
nigiri rpc getrawtransaction "$TXID" true | jq '{vin: [.vin[] | {txid, vout}], vout: [.vout[] | {value, address: .scriptPubKey.address}]}'
```

## 3. Play analyst: apply the common-input heuristic

The analyst's rule: *all inputs belong to the payer*. Test it. For each input, find which wallet owned the coin it spent:

```bash
for row in $(nigiri rpc getrawtransaction "$TXID" true | jq -r '.vin[] | "\(.txid):\(.vout)"'); do
  prev=${row%:*}; n=${row#*:}
  addr=$(nigiri rpc getrawtransaction "$prev" true | jq -r ".vout[$n].scriptPubKey.address")
  for w in sender receiver; do
    [ "$(nigiri rpc -rpcwallet=$w getaddressinfo "$addr" | jq -r .ismine)" = "true" ] && echo "input $row -> $w"
  done
done
```

You should see at least one input from **each** wallet. An analyst applying the heuristic would lump the receiver's coin in with the sender's.

**Then answer, in pairs:**
1. Which output is the payment and which is change? Could an outsider tell? (Hint: the receiver's output now includes their own input's value, so the "payment amount" on-chain is wrong too)
2. Compare with a normal send between the same two wallets. What would the analyst conclude there?
3. Payjoin helps even people who never use it. Why? (What happens to the heuristic's reliability across the whole chain once some share of transactions are payjoins?)
4. What does the payjoin directory learn? What does the OHTTP relay learn? Why use both?

## 4. Bonus: run the S4 lab on it

Feed this transaction's shape into your `apply_cioh` and `detect_change_output` from the [chain-analysis lab](../chain-analysis/). Does your own analyst code get fooled?

## Proof of work (pick one)

- A rust-payjoin beginner issue ([how to find one](../../ISSUE_POOL.md)). Docs count
- Something in the quick start confused you? Fix the docs upstream, following the [PR checklist](../../PR_CHECKLIST.md)
- Test an open rust-payjoin PR on your platform and post a precise test report

## References

- [BIP77: Async Payjoin](https://github.com/bitcoin/bips/blob/master/bip-0077.md) · [BIP78](https://github.com/bitcoin/bips/blob/master/bip-0078.mediawiki)
- [payjoin.org](https://payjoin.org): how it works, and which wallets support it
