"""
Bitcoin Dojo - Week 3 REFERENCE SOLUTION: Keys, Addresses & Encoding
(Programming Bitcoin, Chapter 4)

Grade it:  python3 week-03/check.py --solution
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from dojo import G, Point, sha256, hash256, hash160, bech32_segwit  # noqa: E402

BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def sec(point: Point, compressed: bool = True) -> bytes:
    if compressed:
        return (b"\x02" if point.y % 2 == 0 else b"\x03") + point.x.to_bytes(32, "big")
    return b"\x04" + point.x.to_bytes(32, "big") + point.y.to_bytes(32, "big")


def encode_base58(b: bytes) -> str:
    leading_zeros = len(b) - len(b.lstrip(b"\x00"))
    num = int.from_bytes(b, "big")
    out = ""
    while num > 0:
        num, mod = divmod(num, 58)
        out = BASE58_ALPHABET[mod] + out
    return "1" * leading_zeros + out


def encode_base58_check(payload: bytes) -> str:
    return encode_base58(payload + hash256(payload)[:4])


def decode_base58_check(s: str) -> bytes:
    num = 0
    for c in s:
        num = num * 58 + BASE58_ALPHABET.index(c)
    leading = len(s) - len(s.lstrip("1"))
    raw = b"\x00" * leading + (num.to_bytes((num.bit_length() + 7) // 8, "big") if num else b"")
    payload, checksum = raw[:-4], raw[-4:]
    if hash256(payload)[:4] != checksum:
        raise ValueError("bad checksum")
    return payload


def p2pkh_address(sec_bytes: bytes, testnet: bool = False) -> str:
    prefix = b"\x6f" if testnet else b"\x00"
    return encode_base58_check(prefix + hash160(sec_bytes))


def p2wpkh_address(sec_bytes: bytes, testnet: bool = False) -> str:
    return bech32_segwit("tb" if testnet else "bc", 0, hash160(sec_bytes))


def wif(secret: int, compressed: bool = True, testnet: bool = False) -> str:
    prefix = b"\xef" if testnet else b"\x80"
    suffix = b"\x01" if compressed else b""
    return encode_base58_check(prefix + secret.to_bytes(32, "big") + suffix)
