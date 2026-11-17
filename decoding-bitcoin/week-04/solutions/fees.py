"""
Week 4 lab: weight, virtual size and fees. REFERENCE SOLUTION.

Try exercises/fees.py first!
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from txparse import parse_tx, strip_witness  # noqa: E402,F401  (PROVIDED)


def weight(raw: bytes) -> int:
    return len(strip_witness(raw)) * 3 + len(raw)


def vsize(raw: bytes) -> int:
    return (weight(raw) + 3) // 4


def fee(input_values: list, raw: bytes) -> int:
    return sum(input_values) - sum(o["value"] for o in parse_tx(raw)["outputs"])


def fee_rate(fee_sats: int, vsize_vb: int) -> float:
    return round(fee_sats / vsize_vb, 1)


def estimate_p2wpkh_vsize(n_in: int, n_out: int) -> int:
    base = 10 + 41 * n_in + 31 * n_out  # version 4, counts 1+1, locktime 4; input 41; output 31
    witness = 2 + 108 * n_in            # marker + flag; per input: item count 1, sig 1+72, pubkey 1+33
    return (base * 4 + witness + 3) // 4
