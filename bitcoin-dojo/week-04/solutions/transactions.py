"""
Bitcoin Dojo - Week 4 REFERENCE SOLUTION: Serialisation & Transactions
(Programming Bitcoin, Chapter 5)

Grade it:  python3 week-04/check.py --solution
"""

import sys
from io import BytesIO
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from dojo import hash256  # noqa: E402


def read_varint(s: BytesIO) -> int:
    i = s.read(1)[0]
    if i == 0xFD:
        return int.from_bytes(s.read(2), "little")
    if i == 0xFE:
        return int.from_bytes(s.read(4), "little")
    if i == 0xFF:
        return int.from_bytes(s.read(8), "little")
    return i


def encode_varint(i: int) -> bytes:
    if i < 0xFD:
        return bytes([i])
    if i < 0x10000:
        return b"\xfd" + i.to_bytes(2, "little")
    if i < 0x100000000:
        return b"\xfe" + i.to_bytes(4, "little")
    return b"\xff" + i.to_bytes(8, "little")


class TxIn:
    def __init__(self, prev_tx: bytes, prev_index: int, script_sig: bytes, sequence: int):
        self.prev_tx = prev_tx          # 32 bytes, as displayed (big-endian)
        self.prev_index = prev_index
        self.script_sig = script_sig    # raw script bytes (without length prefix)
        self.sequence = sequence

    @classmethod
    def parse(cls, s: BytesIO) -> "TxIn":
        prev_tx = s.read(32)[::-1]
        prev_index = int.from_bytes(s.read(4), "little")
        script_sig = s.read(read_varint(s))
        sequence = int.from_bytes(s.read(4), "little")
        return cls(prev_tx, prev_index, script_sig, sequence)

    def serialize(self) -> bytes:
        return (self.prev_tx[::-1] + self.prev_index.to_bytes(4, "little")
                + encode_varint(len(self.script_sig)) + self.script_sig
                + self.sequence.to_bytes(4, "little"))


class TxOut:
    def __init__(self, amount: int, script_pubkey: bytes):
        self.amount = amount            # satoshis
        self.script_pubkey = script_pubkey

    @classmethod
    def parse(cls, s: BytesIO) -> "TxOut":
        amount = int.from_bytes(s.read(8), "little")
        return cls(amount, s.read(read_varint(s)))

    def serialize(self) -> bytes:
        return self.amount.to_bytes(8, "little") + encode_varint(len(self.script_pubkey)) + self.script_pubkey


class Tx:
    def __init__(self, version: int, tx_ins, tx_outs, locktime: int):
        self.version, self.tx_ins, self.tx_outs, self.locktime = version, tx_ins, tx_outs, locktime

    @classmethod
    def parse(cls, s: BytesIO) -> "Tx":
        version = int.from_bytes(s.read(4), "little")
        tx_ins = [TxIn.parse(s) for _ in range(read_varint(s))]
        tx_outs = [TxOut.parse(s) for _ in range(read_varint(s))]
        locktime = int.from_bytes(s.read(4), "little")
        return cls(version, tx_ins, tx_outs, locktime)

    def serialize(self) -> bytes:
        return (self.version.to_bytes(4, "little")
                + encode_varint(len(self.tx_ins)) + b"".join(i.serialize() for i in self.tx_ins)
                + encode_varint(len(self.tx_outs)) + b"".join(o.serialize() for o in self.tx_outs)
                + self.locktime.to_bytes(4, "little"))

    def id(self) -> str:
        return hash256(self.serialize())[::-1].hex()

    def fee(self, input_values) -> int:
        return sum(input_values) - sum(o.amount for o in self.tx_outs)
