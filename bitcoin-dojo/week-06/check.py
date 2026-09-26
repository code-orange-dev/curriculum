#!/usr/bin/env python3
"""
Grade Week 6 (SegWit & advanced transactions).

    python3 week-06/check.py              # grades exercises/segwit_lab.py
    python3 week-06/check.py --solution   # grades the reference solution

Uses a REAL native-segwit transaction from block 800,000 (data/transactions.json):
your txid, weight and BIP143 signature hash have to match reality.
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "lib"))
from dojo import Point, hash160, need, parse_der, run_checks, load_week  # noqa: E402

m = load_week(__file__, "segwit_lab.py", "--solution" in sys.argv)
REAL = json.loads((HERE.parent / "data" / "transactions.json").read_text())["p2wpkh_800000"]
RAW = bytes.fromhex(REAL["hex"])

sys.path.insert(0, str(HERE.parent / "week-05" / "solutions"))
from script_lab import verify  # noqa: E402  (reference ECDSA from Week 5)


def parsed():
    return need(m.parse_segwit(RAW), "parse_segwit")


def parse():
    tx, witnesses = parsed()
    assert len(tx.tx_ins) == 1 and len(tx.tx_outs) == 2, "expected 1 input, 2 outputs"
    assert [o.amount for o in tx.tx_outs] == [671958, 19425506], f"amounts: {[o.amount for o in tx.tx_outs]}"
    assert len(witnesses) == 1 and len(witnesses[0]) == 2, "one witness stack with 2 items (signature, pubkey)"
    assert tx.tx_ins[0].script_sig == b"", "native segwit inputs have an EMPTY scriptSig"


def txid_matches():
    tx, _ = parsed()
    got = need(m.txid(tx), "txid")
    assert got == REAL["txid"], f"got {got}, want {REAL['txid']} (txid excludes witness data!)"


def wtxid_differs():
    tx, _ = parsed()
    w = need(m.wtxid(RAW), "wtxid")
    assert w != m.txid(tx) and len(w) == 64, "wtxid hashes the full serialization, so it differs from txid"


def weight_matches():
    tx, _ = parsed()
    w = need(m.weight(tx, RAW), "weight")
    assert w == REAL["weight"], f"weight should be {REAL['weight']} WU, got {w}"
    assert need(m.vsize(w), "vsize") == 141, f"vsize should be ceil(561/4) = 141, got {m.vsize(w)}"


def bip143_signature():
    tx, witnesses = parsed()
    sig, sec = witnesses[0]
    pkh = bytes.fromhex(REAL["prevout_script_pubkey"])[2:]
    assert hash160(sec) == pkh, "sanity: witness pubkey matches the prevout"
    z = need(m.bip143_sighash_p2wpkh(tx, 0, pkh, REAL["prevout_value"]), "bip143_sighash_p2wpkh")
    r, s = parse_der(sig[:-1])
    assert verify(z, r, s, Point.from_sec(sec)), \
        "the real signature doesn't verify against your sighash: check field order and the amount"


def locktimes():
    assert need(m.describe_locktime(0), "describe_locktime") == ("none", 0)
    assert m.describe_locktime(800000) == ("height", 800000)
    assert m.describe_locktime(1700000000) == ("time", 1700000000), "values >= 500,000,000 are UNIX times"


def cltv():
    pkh = bytes(range(20))
    got = need(m.cltv_p2pkh_script(800000, pkh), "cltv_p2pkh_script").hex()
    want = "0300350cb17576a914" + pkh.hex() + "88ac"
    assert got == want, f"got {got}\n        want {want} (800000 = 0x0c3500, little-endian script number)"
    got = m.cltv_p2pkh_script(128, pkh).hex()
    assert got.startswith("028000b175"), "128 = 0x80 needs a 0x00 sign byte: 8000"


run_checks("Bitcoin Dojo - Week 6: SegWit & Advanced Transactions", [
    ("Parse a real segwit transaction (block 800,000)", parse),
    ("txid matches mainnet (witness excluded)", txid_matches),
    ("wtxid differs from txid", wtxid_differs),
    ("Weight and vsize match mainnet", weight_matches),
    ("BIP143 sighash: the real signature verifies", bip143_signature),
    ("nLockTime: height vs time", locktimes),
    ("Build a CLTV-locked P2PKH script", cltv),
]) or sys.exit(1)
