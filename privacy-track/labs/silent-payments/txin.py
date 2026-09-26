"""
Transaction-input plumbing for BIP352. PROVIDED - read it, but you don't edit it.

BIP352 only uses inputs whose public key can be read straight from the
spending transaction ("eligible inputs"):

    P2TR          key from the output itself (x-only, even y)
                  - skipped if it is a script-path spend whose internal key
                    is the NUMS point H (a provably unspendable key)
    P2WPKH        key is the last witness item
    P2SH-P2WPKH   key is the last witness item
    P2PKH         key is found in the scriptSig by hashing 33-byte windows

Anything else (P2WSH multisig, bare scripts, uncompressed keys...) is skipped.
The sender and the receiver MUST agree on this list, or they derive
different shared secrets and the payment is lost. That's why this code is
full of edge cases, and why it's a good place to review upstream PRs.
"""

import hashlib
import struct
from io import BytesIO

from secp import Point

NUMS_H = bytes.fromhex("50929b74c1a04954b78b4b6035e97a5e078a5a0f28ec96d547bfee9ace803ac0")


def serialize_outpoint(txid_hex: str, vout: int) -> bytes:
    """36 bytes: txid in *internal* (little-endian) byte order || vout as uint32 LE.

    txids are displayed big-endian, so the hex string is reversed first.
    """
    return bytes.fromhex(txid_hex)[::-1] + struct.pack("<I", vout)


def _hash160(b: bytes) -> bytes:
    sha = hashlib.sha256(b).digest()
    try:
        return hashlib.new("ripemd160", sha).digest()
    except ValueError:  # some OpenSSL builds drop ripemd160
        return _ripemd160(sha)


def _read_witness(hex_str: str):
    f = BytesIO(bytes.fromhex(hex_str))

    def compact_size():
        n = f.read(1)
        if not n:
            return 0
        n = n[0]
        if n == 253:
            return struct.unpack("<H", f.read(2))[0]
        if n == 254:
            return struct.unpack("<I", f.read(4))[0]
        if n == 255:
            return struct.unpack("<Q", f.read(8))[0]
        return n

    return [f.read(compact_size()) for _ in range(compact_size())]


def _is_p2tr(s):   return len(s) == 34 and s[0] == 0x51 and s[1] == 0x20
def _is_p2wpkh(s): return len(s) == 22 and s[0] == 0x00 and s[1] == 0x14
def _is_p2sh(s):   return len(s) == 23 and s[0] == 0xA9 and s[1] == 0x14 and s[-1] == 0x87
def _is_p2pkh(s):  return (len(s) == 25 and s[:3] == b"\x76\xa9\x14"
                           and s[-2:] == b"\x88\xac")


def _compressed(b: bytes):
    if len(b) != 33 or b[0] not in (2, 3):
        return None
    try:
        return Point.from_bytes(b)
    except ValueError:
        return None


def input_pubkey(vin: dict):
    """Return (Point, is_taproot) for an eligible input, or None to skip it.

    `vin` is one entry of the test vectors' "vin" list:
        {"txid", "vout", "scriptSig", "txinwitness", "prevout": {"scriptPubKey": {"hex"}}}
    """
    spk = bytes.fromhex(vin["prevout"]["scriptPubKey"]["hex"])
    script_sig = bytes.fromhex(vin["scriptSig"])
    witness = _read_witness(vin["txinwitness"]) if vin["txinwitness"] else []

    if _is_p2pkh(spk):
        # Slide a 33-byte window from the back of the scriptSig and look for
        # the key that hashes to the scriptPubKey's hash. Finds the key even
        # in malleated (non-standard) scriptSigs.
        for end in range(len(script_sig), 32, -1):
            candidate = script_sig[end - 33:end]
            if _hash160(candidate) == spk[3:23]:
                pk = _compressed(candidate)
                if pk:
                    return pk, False
        return None

    if _is_p2sh(spk):
        redeem = script_sig[1:]
        if _is_p2wpkh(redeem) and witness:
            pk = _compressed(witness[-1])
            return (pk, False) if pk else None
        return None

    if _is_p2wpkh(spk):
        pk = _compressed(witness[-1]) if witness else None
        return (pk, False) if pk else None

    if _is_p2tr(spk):
        if not witness:
            return None
        stack = list(witness)
        if len(stack) > 1 and stack[-1][:1] == b"\x50":
            stack.pop()  # annex
        if len(stack) > 1 and stack[-1][1:33] == NUMS_H:
            return None  # script-path spend with unspendable internal key
        try:
            return Point.from_bytes(spk[2:]), True
        except ValueError:
            return None

    return None


# --- pure-python RIPEMD160 fallback (only used if hashlib lacks it) ---------
def _ripemd160(msg: bytes) -> bytes:
    import struct as s
    def rol(x, n): return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF
    def f(j, x, y, z):
        return [x ^ y ^ z, (x & y) | (~x & z), (x | ~y) ^ z, (x & z) | (y & ~z), x ^ (y | ~z)][j // 16] & 0xFFFFFFFF
    K1 = [0, 0x5A827999, 0x6ED9EBA1, 0x8F1BBCDC, 0xA953FD4E]
    K2 = [0x50A28BE6, 0x5C4DD124, 0x6D703EF3, 0x7A6D76E9, 0]
    R1 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,7,4,13,1,10,6,15,3,12,0,9,5,2,14,11,8,3,10,14,4,9,15,8,1,2,7,0,6,13,11,5,12,1,9,11,10,0,8,12,4,13,3,7,15,14,5,6,2,4,0,5,9,7,12,2,10,14,1,3,8,11,6,15,13]
    R2 = [5,14,7,0,9,2,11,4,13,6,15,8,1,10,3,12,6,11,3,7,0,13,5,10,14,15,8,12,4,9,1,2,15,5,1,3,7,14,6,9,11,8,12,2,10,0,4,13,8,6,4,1,3,11,15,0,5,12,2,13,9,7,10,14,12,15,10,4,1,5,8,7,6,2,13,14,0,3,9,11]
    S1 = [11,14,15,12,5,8,7,9,11,13,14,15,6,7,9,8,7,6,8,13,11,9,7,15,7,12,15,9,11,7,13,12,11,13,6,7,14,9,13,15,14,8,13,6,5,12,7,5,11,12,14,15,14,15,9,8,9,14,5,6,8,6,5,12,9,15,5,11,6,8,13,12,5,12,13,14,11,8,5,6]
    S2 = [8,9,9,11,13,15,15,5,7,7,8,11,14,14,12,6,9,13,15,7,12,8,9,11,7,7,12,7,6,15,13,11,9,7,15,11,8,6,6,14,12,13,5,14,13,13,7,5,15,5,8,11,14,14,6,14,6,9,12,9,12,5,15,8,8,5,12,9,12,5,14,6,8,13,6,5,15,13,11,11]
    h = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]
    msg = msg + b"\x80" + b"\x00" * ((55 - len(msg)) % 64) + s.pack("<Q", 8 * len(msg))
    for i in range(0, len(msg), 64):
        X = s.unpack("<16I", msg[i:i + 64])
        a1, b1, c1, d1, e1 = h
        a2, b2, c2, d2, e2 = h
        for j in range(80):
            t = (rol((a1 + f(j, b1, c1, d1) + X[R1[j]] + K1[j // 16]) & 0xFFFFFFFF, S1[j]) + e1) & 0xFFFFFFFF
            a1, e1, d1, c1, b1 = e1, d1, rol(c1, 10), b1, t
            t = (rol((a2 + f(79 - j, b2, c2, d2) + X[R2[j]] + K2[j // 16]) & 0xFFFFFFFF, S2[j]) + e2) & 0xFFFFFFFF
            a2, e2, d2, c2, b2 = e2, d2, rol(c2, 10), b2, t
        t = (h[1] + c1 + d2) & 0xFFFFFFFF
        h[1] = (h[2] + d1 + e2) & 0xFFFFFFFF
        h[2] = (h[3] + e1 + a2) & 0xFFFFFFFF
        h[3] = (h[4] + a1 + b2) & 0xFFFFFFFF
        h[4] = (h[0] + b1 + c2) & 0xFFFFFFFF
        h[0] = t
    return s.pack("<5I", *h)
