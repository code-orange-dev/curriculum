#!/usr/bin/env python3
"""
Grade the week 4 lab (weight, vsize, fees).

    python3 week-04/check.py              # grades exercises/fees.py
    python3 week-04/check.py --solution   # grades the reference solution

Run it from the decoding-bitcoin/ folder. Checked against real mainnet
transactions (data/transactions.json).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
from labkit import TXS, load_lab, run_checks  # noqa: E402

m = load_lab(__file__, "fees.py", "--solution" in sys.argv)
LEGACY, SEGWIT = TXS["p2pkh_250000"], TXS["p2wpkh_800000"]
L, S = bytes.fromhex(LEGACY["hex"]), bytes.fromhex(SEGWIT["hex"])


def weights():
    assert m.weight(L) == 4 * len(L), f"a legacy tx has no witness: weight = 4 x size = {4 * len(L)}, got {m.weight(L)}"
    assert m.weight(S) == int(SEGWIT["weight"]), f"segwit tx weight should be {SEGWIT['weight']}, got {m.weight(S)}"


def vsizes():
    assert m.vsize(L) == len(L), f"legacy vsize = size = {len(L)}, got {m.vsize(L)}"
    assert m.vsize(S) == 141, f"561 / 4 = 140.25, rounded up = 141, got {m.vsize(S)}"
    assert isinstance(m.vsize(S), int), "vsize should be a whole number"


def fees():
    for t, raw in ((LEGACY, L), (SEGWIT, S)):
        got = m.fee([int(t["prevout_value"])], raw)
        assert got == int(t["fee"]), f"fee of the block {t['block']} tx should be {t['fee']} sats, got {got}"


def rates():
    assert m.fee_rate(28200, 141) == 200.0, f"28200 sats / 141 vB = 200.0 sat/vB, got {m.fee_rate(28200, 141)}"
    assert m.fee_rate(10000, len(L)) == round(10000 / len(L), 1)


def estimate():
    got = m.estimate_p2wpkh_vsize(1, 2)
    assert got == 141, f"1-in 2-out P2WPKH should come out at about 141 vB (the real one is 141), got {got}"
    assert m.estimate_p2wpkh_vsize(2, 2) == 209, f"2-in 2-out should be 209 vB, got {m.estimate_p2wpkh_vsize(2, 2)}"
    assert m.estimate_p2wpkh_vsize(1, 1) == 110, f"1-in 1-out should be 110 vB, got {m.estimate_p2wpkh_vsize(1, 1)}"


ok = run_checks("Week 4 lab: weight, vsize and fees", [
    ("weight (legacy and segwit)", weights),
    ("vsize rounds up", vsizes),
    ("fee = inputs - outputs (real transactions)", fees),
    ("fee rate in sat/vB", rates),
    ("estimate a P2WPKH transaction's vsize", estimate),
])
sys.exit(0 if ok or "--solution" not in sys.argv else 1)
