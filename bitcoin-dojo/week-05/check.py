#!/usr/bin/env python3
"""
Grade Week 5 (Script & transaction validation).

    python3 week-05/check.py              # grades exercises/script_lab.py
    python3 week-05/check.py --solution   # grades the reference solution

The headline check verifies the ECDSA signature of a REAL mainnet transaction
from block 250,000. It only passes if your sighash, your ECDSA verify and your
Script interpreter are all correct.
"""

import json
import sys
from io import BytesIO
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "lib"))
from dojo import G, N, hash160, hash256, need, run_checks, load_week  # noqa: E402

m = load_week(__file__, "script_lab.py", "--solution" in sys.argv)
REAL = json.loads((HERE.parent / "data" / "transactions.json").read_text())["p2pkh_250000"]
TX = m.Tx.parse(BytesIO(bytes.fromhex(REAL["hex"])))
SPK = bytes.fromhex(REAL["prevout_script_pubkey"])
SIG, SEC = m.parse_script(TX.tx_ins[0].script_sig)


def _der(r, s):
    def enc(n):
        b = n.to_bytes(32, "big").lstrip(b"\x00")
        return b"\x02" + bytes([len(b) + (b[0] >= 0x80)]) + (b"\x00" if b[0] >= 0x80 else b"") + b
    body = enc(r) + enc(s)
    return b"\x30" + bytes([len(body)]) + body


def _sign(secret, z, k):
    """Test-only ECDSA signing with a fixed nonce. NEVER reuse k in real life."""
    r = (k * G).x % N
    s = (z + r * secret) * pow(k, N - 2, N) % N
    return _der(r, min(s, N - s)) + b"\x01"


def _sec(point):
    return (b"\x02" if point.y % 2 == 0 else b"\x03") + point.x.to_bytes(32, "big")


def real_sighash():
    z = need(m.sig_hash(TX, 0, SPK), "sig_hash")
    assert isinstance(z, int) and z.bit_length() > 200, "sig_hash should return the hash as a big integer"
    assert hash160(SEC) == SPK[3:23], "sanity: the key in scriptSig matches the prevout's hash"


def real_signature():
    z = need(m.sig_hash(TX, 0, SPK), "sig_hash")
    from dojo import parse_der, Point
    r, s = parse_der(SIG[:-1])
    ok = need(m.verify(z, r, s, Point.from_sec(SEC)), "verify")
    assert ok is True, "the real 2013 signature should verify (check sig_hash and verify)"


def tampered_fails():
    z = need(m.sig_hash(TX, 0, SPK), "sig_hash")
    from dojo import parse_der, Point
    r, s = parse_der(SIG[:-1])
    assert need(m.verify(z + 1, r, s, Point.from_sec(SEC)), "verify") is False, \
        "changing the message by 1 must make verification fail"


def p2pkh_script():
    z = m.sig_hash(TX, 0, SPK)
    ok = need(m.evaluate(TX.tx_ins[0].script_sig, SPK, z), "evaluate")
    assert ok is True, "scriptSig + scriptPubKey of the real transaction should evaluate to true"


def p2pkh_wrong_key():
    z = m.sig_hash(TX, 0, SPK)
    wrong = SPK[:3] + bytes(20) + SPK[23:]
    assert need(m.evaluate(TX.tx_ins[0].script_sig, wrong, z), "evaluate") is False, \
        "OP_EQUALVERIFY must fail when the pubkey hash doesn't match"


def multisig():
    z = int.from_bytes(hash256(b"Code Orange 2-of-3"), "big")
    keys = [11, 22, 33]
    redeem = bytes([0x52]) + b"".join(b"\x21" + _sec(k * G) for k in keys) + bytes([0x53, 0xAE])
    s1, s3 = _sign(11, z, 1001), _sign(33, z, 1003)
    push = lambda b: bytes([len(b)]) + b
    good = b"\x00" + push(s1) + push(s3)
    assert need(m.evaluate(good, redeem, z), "evaluate") is True, "2-of-3 with keys 1 and 3 should pass"
    bad = b"\x00" + push(s1) + push(_sign(44, z, 1004))
    assert m.evaluate(bad, redeem, z) is False, "a signature from a key not in the script must fail"
    swapped = b"\x00" + push(s3) + push(s1)
    assert m.evaluate(swapped, redeem, z) is False, "signatures must be in the same order as the keys"


def multisig_dummy():
    z = int.from_bytes(hash256(b"off by one"), "big")
    redeem = bytes([0x51]) + b"\x21" + _sec(11 * G) + bytes([0x51, 0xAE])
    sig = _sign(11, z, 777)
    no_dummy = bytes([len(sig)]) + sig
    try:
        result = need(m.evaluate(no_dummy, redeem, z), "evaluate")
    except IndexError:
        result = False
    assert result is False, "without the extra dummy element, OP_CHECKMULTISIG must fail (the off-by-one)"


run_checks("Bitcoin Dojo - Week 5: Script & Transaction Validation", [
    ("Legacy sighash of a real 2013 transaction", real_sighash),
    ("ECDSA: the real mainnet signature verifies", real_signature),
    ("ECDSA: a tampered message fails", tampered_fails),
    ("Script: P2PKH evaluates to true", p2pkh_script),
    ("Script: wrong pubkey hash fails", p2pkh_wrong_key),
    ("Script: 2-of-3 OP_CHECKMULTISIG", multisig),
    ("Script: the OP_CHECKMULTISIG off-by-one", multisig_dummy),
]) or sys.exit(1)
