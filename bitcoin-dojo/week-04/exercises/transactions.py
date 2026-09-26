"""
Bitcoin Dojo - Week 4 Exercises: Serialisation & Transactions
Code Orange Dev School | codeorange.dev

Based on Programming Bitcoin, Chapter 5
https://github.com/jimmysong/programmingbitcoin

Build a transaction parser and serializer, then prove it works on REAL
mainnet transactions: the checker only passes if you reproduce their actual
txids byte for byte. Run from the bitcoin-dojo folder:

    python3 week-04/check.py

The transactions live in data/transactions.json, including block 170's
transaction, the first bitcoin payment between two people (Satoshi to Hal Finney).

Byte order cheat sheet:
    int.from_bytes(s.read(4), "little")    read a little-endian uint32
    n.to_bytes(8, "little")                write a little-endian uint64
    b[::-1]                                reverse bytes (txids are displayed reversed)
"""

import sys
from io import BytesIO
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from dojo import hash256  # noqa: E402


# ---------------------------------------------------------------------------
# Exercise 1 - Varints (CompactSize)
#   < 0xfd            1 byte
#   <= 0xffff         0xfd + 2 bytes little-endian
#   <= 0xffffffff     0xfe + 4 bytes little-endian
#   otherwise         0xff + 8 bytes little-endian
# ---------------------------------------------------------------------------
def read_varint(s: BytesIO) -> int:
    # YOUR CODE HERE
    return None


def encode_varint(i: int) -> bytes:
    # YOUR CODE HERE
    return None


# ---------------------------------------------------------------------------
# Exercise 2 - Inputs and outputs
#
# TxIn on the wire:   prev_tx (32 bytes, reversed!) | prev_index (4, LE)
#                     | script_sig length (varint) | script_sig | sequence (4, LE)
# TxOut on the wire:  amount (8, LE) | script_pubkey length (varint) | script_pubkey
#
# Store prev_tx the way explorers display it (big-endian): reverse after reading,
# reverse again before writing.
# ---------------------------------------------------------------------------
class TxIn:
    def __init__(self, prev_tx: bytes, prev_index: int, script_sig: bytes, sequence: int):
        self.prev_tx = prev_tx
        self.prev_index = prev_index
        self.script_sig = script_sig
        self.sequence = sequence

    @classmethod
    def parse(cls, s: BytesIO) -> "TxIn":
        # YOUR CODE HERE
        return None

    def serialize(self) -> bytes:
        # YOUR CODE HERE
        return None


class TxOut:
    def __init__(self, amount: int, script_pubkey: bytes):
        self.amount = amount
        self.script_pubkey = script_pubkey

    @classmethod
    def parse(cls, s: BytesIO) -> "TxOut":
        # YOUR CODE HERE
        return None

    def serialize(self) -> bytes:
        # YOUR CODE HERE
        return None


# ---------------------------------------------------------------------------
# Exercise 3 - The transaction
#
#   version (4, LE) | input count (varint) | inputs | output count (varint)
#   | outputs | locktime (4, LE)
#
# (This is the legacy format. Segwit adds a marker, a flag and witnesses - Week 6.)
# ---------------------------------------------------------------------------
class Tx:
    def __init__(self, version: int, tx_ins, tx_outs, locktime: int):
        self.version, self.tx_ins, self.tx_outs, self.locktime = version, tx_ins, tx_outs, locktime

    @classmethod
    def parse(cls, s: BytesIO) -> "Tx":
        # YOUR CODE HERE
        return None

    def serialize(self) -> bytes:
        # YOUR CODE HERE
        return None

    # -----------------------------------------------------------------------
    # Exercise 4 - txid = hash256(serialization), reversed, as hex
    # -----------------------------------------------------------------------
    def id(self) -> str:
        # YOUR CODE HERE
        return None

    # -----------------------------------------------------------------------
    # Exercise 5 - fee = sum of input values - sum of output amounts
    # A transaction doesn't store its input values. Why not? (See discussion.)
    # -----------------------------------------------------------------------
    def fee(self, input_values) -> int:
        # YOUR CODE HERE
        return None


# ---------------------------------------------------------------------------
# Discussion (bring to the call):
#  1. Why are txids displayed in the reverse byte order of the hash?
#  2. The fee isn't written anywhere in the transaction. How does a node know it?
#     What does that imply for a hardware wallet that must show you the fee?
#  3. Block 170's transaction paid a fee of 0. Why was that fine in 2009?
# ---------------------------------------------------------------------------
