# Coin Selection Lab (S5)

Implement four coin-selection strategies (largest-first, branch-and-bound, privacy-optimized, random), run them against realistic UTXO sets, and score each one on fees *and* privacy.

```bash
python3 coin_selection_simulator.py
```

The challenge: beat branch-and-bound on privacy without paying much more in fees. Then compare what you built with Bitcoin Core (BnB, CoinGrinder, Knapsack and SRD, picking the lowest waste) and [BDK's coin selection](https://github.com/bitcoindevkit/bdk_wallet).

No dependencies. Python 3.8+.
