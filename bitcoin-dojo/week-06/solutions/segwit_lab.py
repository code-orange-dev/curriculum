"""
Bitcoin Dojo - Week 6 REFERENCE SOLUTION: SegWit & Advanced Transactions
(Programming Bitcoin, Chapters 13, plus BIP141/143)

Grade it:  python3 week-06/check.py --solution
"""

import importlib.util
import sys
from io import BytesIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "lib"))
from dojo import hash256  # noqa: E402

# PROVIDED: the Week 4 reference parser pieces.
_spec = importlib.util.spec_from_file_location("week4", ROOT / "week-04" / "solutions" / "transactions.py")
_w4 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_w4)
Tx, TxIn, TxOut, read_varint, encode_varint = _w4.Tx, _w4.TxIn, _w4.TxOut, _w4.read_varint, _w4.encode_varint


def parse_segwit(raw: bytes):
    s = BytesIO(raw)
    version = int.from_bytes(s.read(4), "little")
    marker, flag = s.read(2)
    if (marker, flag) != (0, 1):
        raise ValueError("not a segwit transaction")
    tx_ins = [TxIn.parse(s) for _ in range(read_varint(s))]
    tx_outs = [TxOut.parse(s) for _ in range(read_varint(s))]
    witnesses = [[s.read(read_varint(s)) for _ in range(read_varint(s))] for _ in tx_ins]
    locktime = int.from_bytes(s.read(4), "little")
    return Tx(version, tx_ins, tx_outs, locktime), witnesses


def txid(tx) -> str:
    return hash256(tx.serialize())[::-1].hex()


def wtxid(raw: bytes) -> str:
    return hash256(raw)[::-1].hex()


def weight(tx, raw: bytes) -> int:
    base = len(tx.serialize())
    return base * 3 + len(raw)


def vsize(w: int) -> int:
    return (w + 3) // 4


def bip143_sighash_p2wpkh(tx, input_index: int, pubkey_hash: bytes, amount: int) -> int:
    hash_prevouts = hash256(b"".join(i.prev_tx[::-1] + i.prev_index.to_bytes(4, "little") for i in tx.tx_ins))
    hash_sequence = hash256(b"".join(i.sequence.to_bytes(4, "little") for i in tx.tx_ins))
    hash_outputs = hash256(b"".join(o.serialize() for o in tx.tx_outs))
    txin = tx.tx_ins[input_index]
    script_code = b"\x19\x76\xa9\x14" + pubkey_hash + b"\x88\xac"
    preimage = (tx.version.to_bytes(4, "little") + hash_prevouts + hash_sequence
                + txin.prev_tx[::-1] + txin.prev_index.to_bytes(4, "little")
                + script_code + amount.to_bytes(8, "little") + txin.sequence.to_bytes(4, "little")
                + hash_outputs + tx.locktime.to_bytes(4, "little") + (1).to_bytes(4, "little"))
    return int.from_bytes(hash256(preimage), "big")


def describe_locktime(n: int):
    if n == 0:
        return ("none", 0)
    return ("height", n) if n < 500_000_000 else ("time", n)


def script_num(n: int) -> bytes:
    out = b""
    while n:
        out += bytes([n & 0xFF])
        n >>= 8
    if out and out[-1] & 0x80:
        out += b"\x00"
    return out


def cltv_p2pkh_script(height: int, pubkey_hash: bytes) -> bytes:
    h = script_num(height)
    return (bytes([len(h)]) + h + b"\xb1\x75"          # <height> OP_CHECKLOCKTIMEVERIFY OP_DROP
            + b"\x76\xa9\x14" + pubkey_hash + b"\x88\xac")  # then a normal P2PKH
