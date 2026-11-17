"""
Week 3 lab: take a raw transaction apart, byte by byte. REFERENCE SOLUTION.

Try exercises/parse_tx.py first!
"""

import hashlib
from io import BytesIO


def hash256(b: bytes) -> bytes:
    return hashlib.sha256(hashlib.sha256(b).digest()).digest()


def read_compact_size(s) -> int:
    first = s.read(1)[0]
    if first < 0xFD:
        return first
    size = {0xFD: 2, 0xFE: 4, 0xFF: 8}[first]
    return int.from_bytes(s.read(size), "little")


def encode_compact_size(n: int) -> bytes:
    if n < 0xFD:
        return bytes([n])
    if n <= 0xFFFF:
        return b"\xfd" + n.to_bytes(2, "little")
    if n <= 0xFFFFFFFF:
        return b"\xfe" + n.to_bytes(4, "little")
    return b"\xff" + n.to_bytes(8, "little")


def parse_tx(raw: bytes) -> dict:
    s = BytesIO(raw)
    tx = {"version": int.from_bytes(s.read(4), "little"), "segwit": False}
    count = read_compact_size(s)
    if count == 0:  # marker 0x00, then flag 0x01
        assert s.read(1) == b"\x01", "bad segwit flag"
        tx["segwit"] = True
        count = read_compact_size(s)
    tx["inputs"] = []
    for _ in range(count):
        prev = s.read(32)[::-1].hex()  # stored little-endian, shown reversed
        vout = int.from_bytes(s.read(4), "little")
        script_sig = s.read(read_compact_size(s)).hex()
        sequence = int.from_bytes(s.read(4), "little")
        tx["inputs"].append({"txid": prev, "vout": vout, "script_sig": script_sig,
                             "sequence": sequence, "witness": []})
    tx["outputs"] = []
    for _ in range(read_compact_size(s)):
        value = int.from_bytes(s.read(8), "little")
        spk = s.read(read_compact_size(s)).hex()
        tx["outputs"].append({"value": value, "script_pubkey": spk})
    if tx["segwit"]:
        for txin in tx["inputs"]:
            txin["witness"] = [s.read(read_compact_size(s)).hex() for _ in range(read_compact_size(s))]
    tx["locktime"] = int.from_bytes(s.read(4), "little")
    assert s.read() == b"", "extra bytes after locktime"
    return tx


def strip_witness(raw: bytes) -> bytes:
    """The transaction without marker, flag and witness: what the txid commits to."""
    tx = parse_tx(raw)
    out = tx["version"].to_bytes(4, "little") + encode_compact_size(len(tx["inputs"]))
    for i in tx["inputs"]:
        sig = bytes.fromhex(i["script_sig"])
        out += bytes.fromhex(i["txid"])[::-1] + i["vout"].to_bytes(4, "little")
        out += encode_compact_size(len(sig)) + sig + i["sequence"].to_bytes(4, "little")
    out += encode_compact_size(len(tx["outputs"]))
    for o in tx["outputs"]:
        spk = bytes.fromhex(o["script_pubkey"])
        out += o["value"].to_bytes(8, "little") + encode_compact_size(len(spk)) + spk
    return out + tx["locktime"].to_bytes(4, "little")


def txid(raw: bytes) -> str:
    return hash256(strip_witness(raw))[::-1].hex()


def wtxid(raw: bytes) -> str:
    return hash256(raw)[::-1].hex()
