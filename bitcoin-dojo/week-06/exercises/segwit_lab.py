"""
Bitcoin Dojo - Week 6 Exercises: SegWit & Advanced Transactions
Code Orange Dev School | codeorange.dev

Based on Programming Bitcoin (Chapter 13), BIP141 and BIP143
https://github.com/jimmysong/programmingbitcoin

You'll take apart a REAL native-segwit payment from block 800,000, match its
txid and weight to mainnet, and verify its signature with the BIP143 sighash.
Run from the bitcoin-dojo folder:

    python3 week-06/check.py

Provided: Tx / TxIn / TxOut / read_varint / encode_varint (Week 4 reference),
hash256, and (inside the checker) Week 5's ECDSA verify.
"""

import importlib.util
import sys
from io import BytesIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "lib"))
from dojo import hash256  # noqa: E402

_spec = importlib.util.spec_from_file_location("week4", ROOT / "week-04" / "solutions" / "transactions.py")
_w4 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_w4)
Tx, TxIn, TxOut, read_varint, encode_varint = _w4.Tx, _w4.TxIn, _w4.TxOut, _w4.read_varint, _w4.encode_varint


# ---------------------------------------------------------------------------
# Exercise 1 - Parse the segwit serialization (BIP144)
#
#   version (4) | marker 0x00 | flag 0x01 | inputs | outputs
#   | witnesses: for EACH input, a varint item count, then varint-prefixed items
#   | locktime (4)
#
# Return (Tx(version, tx_ins, tx_outs, locktime), witnesses) where witnesses is
# a list (one per input) of lists of bytes. Raise ValueError if marker/flag are
# not 00 01. Reuse TxIn.parse / TxOut.parse on a BytesIO.
# ---------------------------------------------------------------------------
def parse_segwit(raw: bytes):
    # YOUR CODE HERE
    return None


# ---------------------------------------------------------------------------
# Exercise 2 - Two ids
#   txid:  hash256 of the LEGACY serialization (tx.serialize() has no witness)
#   wtxid: hash256 of the full raw bytes (with marker, flag, witnesses)
# Both displayed reversed, as hex. Why does fixing malleability need this split?
# ---------------------------------------------------------------------------
def txid(tx) -> str:
    # YOUR CODE HERE
    return None


def wtxid(raw: bytes) -> str:
    # YOUR CODE HERE
    return None


# ---------------------------------------------------------------------------
# Exercise 3 - Weight and virtual size (BIP141)
#   weight = base_size * 3 + total_size
#     base_size  = length without witness data (len(tx.serialize()))
#     total_size = length with everything (len(raw))
#   vsize = weight / 4, rounded UP
# Fee rates are sat/vB, so this is the number wallets actually pay for.
# ---------------------------------------------------------------------------
def weight(tx, raw: bytes) -> int:
    # YOUR CODE HERE
    return None


def vsize(w: int) -> int:
    # YOUR CODE HERE
    return None


# ---------------------------------------------------------------------------
# Exercise 4 - BIP143 signature hash for a P2WPKH input
#
# double-SHA256 of:
#   version (4 LE)
#   hashPrevouts   = hash256(all inputs' prev_tx reversed + prev_index 4 LE)
#   hashSequence   = hash256(all inputs' sequence 4 LE)
#   this input's outpoint (prev_tx reversed + prev_index 4 LE)
#   scriptCode     = 0x19 76 a9 14 <pubkey_hash> 88 ac
#   amount         (8 LE)   <- NEW: signatures commit to the value being spent
#   this input's sequence (4 LE)
#   hashOutputs    = hash256(all outputs serialized)
#   locktime (4 LE)
#   sighash type   (4 LE) = 1
# Return int.from_bytes(..., "big").
#
# Spec + test vectors: https://github.com/bitcoin/bips/blob/master/bip-0143.mediawiki
# ---------------------------------------------------------------------------
def bip143_sighash_p2wpkh(tx, input_index: int, pubkey_hash: bytes, amount: int) -> int:
    # YOUR CODE HERE
    return None


# ---------------------------------------------------------------------------
# Exercise 5 - Timelocks
#
# describe_locktime(n): ("none", 0) if n == 0, ("height", n) if n < 500,000,000,
#                       otherwise ("time", n) - a UNIX timestamp.
#
# cltv_p2pkh_script(height, pubkey_hash): a P2PKH that can't be spent before
# a block height:
#   <height as script number> OP_CHECKLOCKTIMEVERIFY OP_DROP
#   OP_DUP OP_HASH160 <20-byte hash> OP_EQUALVERIFY OP_CHECKSIG
# Opcodes: CLTV 0xb1, DROP 0x75, DUP 0x76, HASH160 0xa9, EQUALVERIFY 0x88, CHECKSIG 0xac.
# Script numbers are minimal little-endian; if the top bit of the last byte is
# set, append 0x00 (it would otherwise mean "negative"). Push = length byte + data.
# ---------------------------------------------------------------------------
def describe_locktime(n: int):
    # YOUR CODE HERE
    return None


def cltv_p2pkh_script(height: int, pubkey_hash: bytes) -> bytes:
    # YOUR CODE HERE
    return None


# ---------------------------------------------------------------------------
# Discussion (bring to the call):
#  1. How does moving signatures out of the txid fix third-party malleability,
#     and why did Lightning need that fix?
#  2. The BIP143 sighash commits to the input amount. What attack on hardware
#     wallets does that prevent?
#  3. nLockTime vs nSequence (BIP68) vs OP_CHECKLOCKTIMEVERIFY vs
#     OP_CHECKSEQUENCEVERIFY: absolute or relative? transaction or script?
# ---------------------------------------------------------------------------
