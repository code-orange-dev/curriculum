#!/usr/bin/env python3
"""
Grade the week 3 lab (parse a raw transaction byte by byte).

    python3 week-03/check.py              # grades exercises/parse_tx.py
    python3 week-03/check.py --solution   # grades the reference solution

Run it from the decoding-bitcoin/ folder. The transactions are real mainnet
transactions (data/transactions.json): you pass only if you reproduce their
real txids, byte for byte.
"""

import sys
from io import BytesIO
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
from labkit import TXS, load_lab, run_checks  # noqa: E402

m = load_lab(__file__, "parse_tx.py", "--solution" in sys.argv)
LEGACY, SEGWIT, B170 = TXS["p2pkh_250000"], TXS["p2wpkh_800000"], TXS["block170"]


def compact_size():
    for raw, want in (("64", 100), ("fdff00", 255), ("fd2b02", 555), ("fe7f110100", 70015),
                      ("ff6dc7ed3e60100000", 18005558675309)):
        got = m.read_compact_size(BytesIO(bytes.fromhex(raw)))
        assert got == want, f"{raw} should read as {want}, got {got}"


def legacy_fields():
    tx = m.parse_tx(bytes.fromhex(LEGACY["hex"]))
    assert tx["version"] == 1, f"version should be 1, got {tx['version']}"
    assert tx["segwit"] is False, "a legacy transaction has no marker and flag"
    assert len(tx["inputs"]) == 1 and len(tx["outputs"]) == 2, "expected 1 input and 2 outputs"
    assert tx["inputs"][0]["txid"].startswith("6f5017"), "show the input's txid reversed (big-endian)"
    assert tx["inputs"][0]["vout"] == 1, "vout should be 1"
    assert [o["value"] for o in tx["outputs"]] == [453653000, 5258944500], \
        f"output values wrong: {[o['value'] for o in tx['outputs']]} (little-endian!)"
    assert tx["locktime"] == 0


def segwit_fields():
    tx = m.parse_tx(bytes.fromhex(SEGWIT["hex"]))
    assert tx["version"] == 2 and tx["segwit"] is True, "version 2, with marker 0x00 and flag 0x01"
    i = tx["inputs"][0]
    assert i["script_sig"] == "", "a native segwit input has an EMPTY script_sig"
    assert i["sequence"] == 0xFFFFFFFD, f"sequence should be 0xfffffffd (RBF signalled), got {hex(i['sequence'])}"
    assert len(i["witness"]) == 2, "P2WPKH witness has 2 items: signature and public key"
    assert i["witness"][1].startswith("02") and len(i["witness"][1]) == 66, "second item is a 33-byte compressed pubkey"
    assert all(o["script_pubkey"].startswith("0014") for o in tx["outputs"]), "both outputs are P2WPKH (0x00 0x14 <20 bytes>)"
    assert sum(o["value"] for o in tx["outputs"]) == 20097464


def txids():
    for t in (LEGACY, B170, SEGWIT):
        got = m.txid(bytes.fromhex(t["hex"]))
        assert got == t["txid"], f"txid of block {t['block']} tx should be {t['txid'][:16]}..., got {str(got)[:16]}..."


def wtxid_differs():
    raw = bytes.fromhex(SEGWIT["hex"])
    assert m.wtxid(raw) != m.txid(raw), "for a segwit transaction, wtxid and txid must differ"
    legacy = bytes.fromhex(LEGACY["hex"])
    assert m.wtxid(legacy) == m.txid(legacy), "for a legacy transaction, wtxid == txid"


ok = run_checks("Week 3 lab: inside a transaction", [
    ("read_compact_size", compact_size),
    ("parse a legacy transaction (block 250000)", legacy_fields),
    ("parse a segwit transaction (block 800000)", segwit_fields),
    ("txid matches the real one (3 transactions)", txids),
    ("wtxid vs txid", wtxid_differs),
])
sys.exit(0 if ok or "--solution" not in sys.argv else 1)
