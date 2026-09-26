#!/usr/bin/env python3
"""
Grade Week 4 (serialisation & transactions).

    python3 week-04/check.py              # grades exercises/transactions.py
    python3 week-04/check.py --solution   # grades the reference solution

The transactions are real mainnet transactions (data/transactions.json).
Your parser and serializer pass only if you reproduce their real txids,
byte for byte.
"""

import json
import sys
from io import BytesIO
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "lib"))
from dojo import need, run_checks, load_week  # noqa: E402

m = load_week(__file__, "transactions.py", "--solution" in sys.argv)
TXS = json.loads((HERE.parent / "data" / "transactions.json").read_text())
P2PKH, B170 = TXS["p2pkh_250000"], TXS["block170"]


def parse(hex_):
    return need(m.Tx.parse(BytesIO(bytes.fromhex(hex_))), "Tx.parse")


def varint_read():
    for raw, want in (("64", 100), ("fdff00", 255), ("fd2b02", 555), ("fe7f110100", 70015),
                      ("ff6dc7ed3e60100000", 18005558675309)):
        got = need(m.read_varint(BytesIO(bytes.fromhex(raw))), "read_varint")
        assert got == want, f"{raw} should read as {want}, got {got}"


def varint_encode():
    for n, want in ((100, "64"), (255, "fdff00"), (555, "fd2b02"), (70015, "fe7f110100"),
                    (18005558675309, "ff6dc7ed3e60100000")):
        got = need(m.encode_varint(n), "encode_varint").hex()
        assert got == want, f"{n} should encode as {want}, got {got}"


def parse_fields():
    tx = parse(P2PKH["hex"])
    assert tx.version == 1, f"version should be 1, got {tx.version}"
    assert len(tx.tx_ins) == 1 and len(tx.tx_outs) == 2, "expected 1 input and 2 outputs"
    assert [o.amount for o in tx.tx_outs] == [453653000, 5258944500], \
        f"output amounts wrong: {[o.amount for o in tx.tx_outs]} (little-endian!)"
    assert tx.tx_ins[0].prev_tx.hex().startswith("6f5017"), \
        "prev_tx should be shown big-endian: reverse the 32 bytes you read"
    assert tx.tx_ins[0].prev_index == 1 and tx.locktime == 0


def roundtrip():
    tx = parse(P2PKH["hex"])
    got = need(tx.serialize(), "Tx.serialize").hex()
    assert got == P2PKH["hex"], "serialize(parse(raw)) must give back the exact raw bytes"


def txid_p2pkh():
    got = need(parse(P2PKH["hex"]).id(), "Tx.id")
    assert got == P2PKH["txid"], f"got {got}, want the real txid {P2PKH['txid']}"


def txid_block170():
    got = need(parse(B170["hex"]).id(), "Tx.id")
    assert got == B170["txid"], f"got {got}, want {B170['txid']}"


def fee():
    got = need(parse(P2PKH["hex"]).fee([P2PKH["prevout_value"]]), "Tx.fee")
    assert got == P2PKH["fee"], f"fee should be {P2PKH['fee']} sats, got {got}"
    assert parse(B170["hex"]).fee([B170["prevout_value"]]) == 0, "Satoshi's payment to Hal paid no fee"


run_checks("Bitcoin Dojo - Week 4: Serialisation & Transactions", [
    ("read_varint (Programming Bitcoin values)", varint_read),
    ("encode_varint", varint_encode),
    ("Parse a real 2013 transaction: fields", parse_fields),
    ("Round trip: serialize(parse(raw)) == raw", roundtrip),
    ("txid of the block 250,000 transaction", txid_p2pkh),
    ("txid of Satoshi's payment to Hal Finney (block 170)", txid_block170),
    ("Fee = inputs - outputs", fee),
]) or sys.exit(1)
