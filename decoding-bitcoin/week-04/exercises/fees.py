"""
Week 4 lab: weight, virtual size and fees.

Fill in every function marked TODO, then grade it from the decoding-bitcoin/ folder:

    python3 week-04/check.py

Rules you need (BIP141):

    weight = (size without witness) * 3 + (full size)
           = non-witness bytes * 4 + witness bytes * 1
    vsize  = weight / 4, rounded UP
    fee    = sum of input values - sum of output values   (it is never written in the transaction!)

parse_tx and strip_witness are PROVIDED (they are the week 3 lab).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from txparse import parse_tx, strip_witness  # noqa: E402,F401  (PROVIDED)


def weight(raw: bytes) -> int:
    # TODO: use strip_witness(raw) and len(raw)
    raise NotImplementedError


def vsize(raw: bytes) -> int:
    # TODO: weight / 4, rounded up (integers only: no floats)
    raise NotImplementedError


def fee(input_values: list, raw: bytes) -> int:
    # TODO: input_values are the amounts (sats) of the outputs being spent; subtract the outputs of raw (parse_tx)
    raise NotImplementedError


def fee_rate(fee_sats: int, vsize_vb: int) -> float:
    # TODO: sats per vbyte, rounded to 1 decimal
    raise NotImplementedError


def estimate_p2wpkh_vsize(n_in: int, n_out: int) -> int:
    # TODO: estimate the vsize of a P2WPKH transaction with n_in inputs and n_out P2WPKH outputs. Count bytes: overhead (version, counts, locktime), each input (txid, vout, empty script_sig, sequence), each output (value, script length, 22-byte script), then the witness (marker, flag, and per input: item count, a 72-byte signature and a 33-byte pubkey, each with a length byte). Assume the worst-case 72-byte signature.
    raise NotImplementedError
