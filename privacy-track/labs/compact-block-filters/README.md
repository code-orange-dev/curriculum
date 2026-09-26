# Compact Block Filters Lab (S7)

Build a simplified BIP158 filter from scratch: hash elements into a range, Golomb-Rice encode the sorted deltas, match queries against the filter, and measure false positives. Then see how an SP light client uses filters to fetch only the blocks it needs (tie-in to S2).

```bash
python3 compact_block_filters.py
```

**Simplification:** real BIP158 hashes with SipHash-2-4 keyed by the block hash. This lab substitutes a SHA256-based hash so there's nothing to install. The parameters (P = 19, M = 784931) and the Golomb-Rice coding match the spec. Read [BIP158](https://github.com/bitcoin/bips/blob/master/bip-0158.mediawiki) for the exact construction, and [Kyoto](https://github.com/2140-dev/kyoto) for a production client.

No dependencies. Python 3.8+.
