#!/usr/bin/env python3
"""
Session 2: how expensive is scanning?

A silent payment receiver must do one ECDH (a scalar multiplication) for
EVERY eligible transaction on the chain, because any of them might pay you.
This script times your scan() on synthetic transactions and extrapolates.

    python3 scan_benchmark.py            # uses your receive.py if implemented
    python3 scan_benchmark.py 500        # benchmark 500 transactions

Python is ~100-1000x slower than libsecp256k1, so treat the result as an
upper bound - then ask what a phone on a data plan would pay even at C speed.
"""

import importlib.util
import secrets
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from secp import G, N  # noqa: E402

# Rough order of magnitude, not a measurement: check a block explorer or an
# indexer's stats for today's number and plug it in.
ELIGIBLE_TXS_PER_DAY = 300_000


def load_scan():
    for folder, label in ((HERE, "your receive.py"), (HERE / "solutions", "the reference solution")):
        spec = importlib.util.spec_from_file_location("r", folder / "receive.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        k = secrets.randbelow(N - 1) + 1
        if mod.compute_tweak(k * G, 1) is not None and mod.scan(k, k * G, k * G, []) is not None:
            return mod, label
    raise SystemExit("no scan() implementation found")


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    mod, label = load_scan()
    print(f"Benchmarking {label} on {n} synthetic transactions...")

    b_scan = secrets.randbelow(N - 1) + 1
    B_spend = (secrets.randbelow(N - 1) + 1) * G
    # Each tx: a random tweak (what an indexer would serve) + 2 random outputs.
    txs = [((secrets.randbelow(N - 1) + 1) * G,
            [((secrets.randbelow(N - 1) + 1) * G).to_xonly() for _ in range(2)])
           for _ in range(n)]

    start = time.perf_counter()
    for tweak, outputs in txs:
        mod.scan(b_scan, B_spend, tweak, outputs)
    per_tx = (time.perf_counter() - start) / n

    day = per_tx * ELIGIBLE_TXS_PER_DAY
    print(f"  {per_tx * 1000:.2f} ms per transaction")
    print(f"  ~{day / 60:.0f} min to scan one day of chain (assuming {ELIGIBLE_TXS_PER_DAY:,} eligible txs/day)")
    print(f"  ~{day * 365 / 3600:.0f} hours to catch up after a year offline")
    print("\nNow discuss: who should do this work - your phone, your node, or a server?")
    print("And what does each option reveal about you?")


if __name__ == "__main__":
    main()
