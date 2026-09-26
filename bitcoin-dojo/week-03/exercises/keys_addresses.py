"""
Bitcoin Dojo - Week 3 Exercises: Keys, Addresses & Encoding
Code Orange Dev School | codeorange.dev

Based on Programming Bitcoin, Chapter 4
https://github.com/jimmysong/programmingbitcoin

Fill in the functions, then grade yourself (from the bitcoin-dojo folder):

    python3 week-03/check.py

The checks use real, public test vectors: BIP173's example key and the
answers to the book's exercises. Unfinished functions show up as
"not implemented yet", so you can go one at a time.

Provided (from lib/dojo.py - you built the curve math in Weeks 1-2):
    G                    the secp256k1 generator; secret * G is a public key Point
    point.x, point.y     coordinates (ints)
    sha256(b), hash256(b), hash160(b)
    bech32_segwit(hrp, version, program)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from dojo import G, Point, sha256, hash256, hash160, bech32_segwit  # noqa: E402,F401

BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


# ---------------------------------------------------------------------------
# Exercise 1 - SEC format (serializing a public key)
#
#   uncompressed:  04 || x (32 bytes) || y (32 bytes)             65 bytes
#   compressed:    02 if y is even, 03 if odd || x (32 bytes)     33 bytes
#
# Numbers are big-endian: n.to_bytes(32, "big")
# ---------------------------------------------------------------------------
def sec(point: Point, compressed: bool = True) -> bytes:
    # YOUR CODE HERE
    return None


# ---------------------------------------------------------------------------
# Exercise 2 - Base58
#
# Treat the bytes as one big number (int.from_bytes(b, "big")), repeatedly
# divmod by 58, and map each remainder to BASE58_ALPHABET (building the string
# from the right). Every leading 0x00 byte becomes a leading "1".
#
# Why not base64? No 0/O/I/l to confuse, and no +/ characters.
# ---------------------------------------------------------------------------
def encode_base58(b: bytes) -> str:
    # YOUR CODE HERE
    return None


# ---------------------------------------------------------------------------
# Exercise 3 - Base58Check: append a 4-byte checksum, hash256(payload)[:4]
# ---------------------------------------------------------------------------
def encode_base58_check(payload: bytes) -> str:
    # YOUR CODE HERE
    return None


# ---------------------------------------------------------------------------
# Exercise 4 - Decode Base58Check and verify the checksum
#
# Reverse Exercise 2: num = num * 58 + ALPHABET.index(c), convert back to bytes,
# restore one 0x00 per leading "1". Split off the last 4 bytes and raise
# ValueError if they don't equal hash256(payload)[:4]. Return the payload.
# ---------------------------------------------------------------------------
def decode_base58_check(s: str) -> bytes:
    # YOUR CODE HERE
    return None


# ---------------------------------------------------------------------------
# Exercise 5 - P2PKH address:  base58check(version || hash160(sec))
#   version byte: 0x00 mainnet, 0x6f testnet
# ---------------------------------------------------------------------------
def p2pkh_address(sec_bytes: bytes, testnet: bool = False) -> str:
    # YOUR CODE HERE
    return None


# ---------------------------------------------------------------------------
# Exercise 6 - Native segwit (P2WPKH) address
#   bech32_segwit("bc" or "tb", 0, hash160(sec))
# Compare with Exercise 5: same hash160, different wrapper.
# ---------------------------------------------------------------------------
def p2wpkh_address(sec_bytes: bytes, testnet: bool = False) -> str:
    # YOUR CODE HERE
    return None


# ---------------------------------------------------------------------------
# Exercise 7 - WIF (Wallet Import Format) for a private key
#   base58check( 0x80 mainnet / 0xef testnet
#                || secret as 32 bytes big-endian
#                || 0x01 if the matching public key is compressed )
# ---------------------------------------------------------------------------
def wif(secret: int, compressed: bool = True, testnet: bool = False) -> str:
    # YOUR CODE HERE
    return None


# ---------------------------------------------------------------------------
# Discussion (bring to the call):
#  1. Walk the full path from a 256-bit secret to a bc1q... address. Why does
#     each step exist?
#  2. The same secret gives two different P2PKH addresses (compressed and
#     uncompressed). Why can that lose people money when they restore a wallet?
#  3. Why hash160 and not just sha256? What do we gain and give up with 20 bytes?
# ---------------------------------------------------------------------------
