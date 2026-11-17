"""
Week 3 lab: take a raw transaction apart, byte by byte.

Fill in every function marked TODO, then grade it from the decoding-bitcoin/ folder:

    python3 week-03/check.py

Byte layout (see the week 3 notes and the Transaction Structure lesson):

    version       4 bytes, little-endian
    marker, flag  0x00 0x01, only in segwit transactions
    input count   compact size
      each input: txid 32 bytes (reversed!), vout 4, script_sig (compact size + bytes), sequence 4
    output count  compact size
      each output: value 8 bytes, script_pubkey (compact size + bytes)
    witness       segwit only: for each input, an item count, then each item (compact size + bytes)
    locktime      4 bytes
"""

import hashlib
from io import BytesIO


def hash256(b: bytes) -> bytes:
    return hashlib.sha256(hashlib.sha256(b).digest()).digest()


def read_compact_size(s) -> int:
    # TODO: read 1 byte. Below 0xfd it IS the number; 0xfd, 0xfe, 0xff mean the next 2, 4 or 8 bytes (little-endian) hold it
    raise NotImplementedError


def encode_compact_size(n: int) -> bytes:
    """PROVIDED: the opposite of read_compact_size."""
    if n < 0xFD:
        return bytes([n])
    if n <= 0xFFFF:
        return b"\xfd" + n.to_bytes(2, "little")
    if n <= 0xFFFFFFFF:
        return b"\xfe" + n.to_bytes(4, "little")
    return b"\xff" + n.to_bytes(8, "little")


def parse_tx(raw: bytes) -> dict:
    # TODO: return a dict like {"version": 2, "segwit": True, "inputs": [{"txid", "vout", "script_sig", "sequence", "witness": [hex, ...]}], "outputs": [{"value", "script_pubkey"}], "locktime": 0}. Bytes as hex strings; show the input txid reversed (big-endian)
    raise NotImplementedError


def strip_witness(raw: bytes) -> bytes:
    """The transaction without marker, flag and witness: what the txid commits to."""
    # TODO: rebuild the transaction WITHOUT marker, flag and witness (use parse_tx and encode_compact_size)
    raise NotImplementedError


def txid(raw: bytes) -> str:
    # TODO: hash256 of the stripped transaction, shown reversed
    raise NotImplementedError


def wtxid(raw: bytes) -> str:
    # TODO: hash256 of the full raw transaction, shown reversed
    raise NotImplementedError
