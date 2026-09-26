"""
Bitcoin Dojo shared toolbox. PROVIDED - you built most of this in earlier weeks.

Weeks 3-6 import from here so each week can focus on its own topic:

    G, N, P               secp256k1 generator, group order, field prime
    Point                 curve point:  P + Q,  -P,  k * P,  P.x, P.y, P.is_infinity
    Point.from_sec(b)     parse a 33- or 65-byte SEC public key
    sha256, hash256       single and double SHA256
    hash160               RIPEMD160(SHA256(x))
    bech32_segwit(hrp, version, program)   segwit address encoder (BIP173/350)
    parse_der(sig)        DER signature -> (r, s)

Teaching code: slow and not constant-time. Never use it with real keys.
"""

import hashlib

P = 2**256 - 2**32 - 977
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141


# --------------------------------------------------------------------- curve
class Point:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x, self.y = x, y

    @staticmethod
    def infinity():
        return Point(None, None)

    @property
    def is_infinity(self):
        return self.x is None

    @staticmethod
    def from_sec(b: bytes) -> "Point":
        if b[0] == 4 and len(b) == 65:
            return Point(int.from_bytes(b[1:33], "big"), int.from_bytes(b[33:], "big"))
        if b[0] in (2, 3) and len(b) == 33:
            x = int.from_bytes(b[1:], "big")
            y = pow((pow(x, 3, P) + 7) % P, (P + 1) // 4, P)
            if (y % 2 == 0) != (b[0] == 2):
                y = P - y
            return Point(x, y)
        raise ValueError("not a SEC public key")

    def __eq__(self, o):
        return isinstance(o, Point) and self.x == o.x and self.y == o.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __neg__(self):
        return self if self.is_infinity else Point(self.x, (-self.y) % P)

    def __add__(self, o):
        if self.is_infinity:
            return o
        if o.is_infinity:
            return self
        if self.x == o.x:
            if (self.y + o.y) % P == 0:
                return Point.infinity()
            s = 3 * self.x * self.x * pow(2 * self.y, P - 2, P) % P
        else:
            s = (o.y - self.y) * pow(o.x - self.x, P - 2, P) % P
        x3 = (s * s - self.x - o.x) % P
        return Point(x3, (s * (self.x - x3) - self.y) % P)

    def __rmul__(self, k):
        k %= N
        result, addend = Point.infinity(), self
        while k:
            if k & 1:
                result = result + addend
            addend = addend + addend
            k >>= 1
        return result

    def __repr__(self):
        return "Point(infinity)" if self.is_infinity else f"Point({self.x:#066x}, {self.y:#066x})"


G = Point(0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
          0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)


# -------------------------------------------------------------------- hashes
def sha256(b: bytes) -> bytes:
    return hashlib.sha256(b).digest()


def hash256(b: bytes) -> bytes:
    return sha256(sha256(b))


def hash160(b: bytes) -> bytes:
    try:
        return hashlib.new("ripemd160", sha256(b)).digest()
    except ValueError:  # some OpenSSL builds drop ripemd160
        return _ripemd160(sha256(b))


# -------------------------------------------------------------------- bech32
_CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"


def _polymod(values):
    gen = [0x3B6A57B2, 0x26508E6D, 0x1EA119FA, 0x3D4233DD, 0x2A1462B3]
    chk = 1
    for v in values:
        top = chk >> 25
        chk = (chk & 0x1FFFFFF) << 5 ^ v
        for i in range(5):
            chk ^= gen[i] if ((top >> i) & 1) else 0
    return chk


def bech32_segwit(hrp: str, version: int, program: bytes) -> str:
    """Segwit address: bech32 for version 0 (BIP173), bech32m for 1+ (BIP350)."""
    acc, bits, data = 0, 0, [version]
    for byte in program:
        acc = (acc << 8) | byte
        bits += 8
        while bits >= 5:
            bits -= 5
            data.append((acc >> bits) & 31)
    if bits:
        data.append((acc << (5 - bits)) & 31)
    const = 1 if version == 0 else 0x2BC830A3
    expanded = [ord(c) >> 5 for c in hrp] + [0] + [ord(c) & 31 for c in hrp]
    pm = _polymod(expanded + data + [0] * 6) ^ const
    return hrp + "1" + "".join(_CHARSET[d] for d in data + [(pm >> 5 * (5 - i)) & 31 for i in range(6)])


# ----------------------------------------------------------------------- DER
def parse_der(sig: bytes):
    """DER-encoded ECDSA signature -> (r, s). Trailing sighash byte must be stripped first."""
    if sig[0] != 0x30 or sig[1] + 2 != len(sig):
        raise ValueError("bad DER signature")
    assert sig[2] == 0x02
    rlen = sig[3]
    r = int.from_bytes(sig[4:4 + rlen], "big")
    assert sig[4 + rlen] == 0x02
    slen = sig[5 + rlen]
    s = int.from_bytes(sig[6 + rlen:6 + rlen + slen], "big")
    return r, s


# --------------------------------------------------------------- the grader
class NotImplementedYet(Exception):
    pass


def need(value, what):
    """Raise NotImplementedYet if an exercise returned None."""
    if value is None:
        raise NotImplementedYet(what)
    return value


def run_checks(title, checks):
    """checks: list of (name, fn). Prints ✓ / ✗ / · and returns True if all pass."""
    print("=" * 60 + f"\n{title}\n" + "=" * 60)
    passed = todo = 0
    for name, fn in checks:
        try:
            fn()
            passed += 1
            print(f"  ✓  {name}")
        except NotImplementedYet as e:
            todo += 1
            print(f"  ·  {name}\n        not implemented yet: {e}()")
        except AssertionError as e:
            print(f"  ✗  {name}\n        {e}")
        except Exception as e:
            print(f"  ✗  {name}\n        crashed: {type(e).__name__}: {e}")
    print(f"\n{passed}/{len(checks)} checks passing")
    if passed == len(checks):
        print("All green. Bring your code and your discussion answers to the call. 🟠")
    return passed == len(checks)


def load_week(file, module_path, solution):
    """Import the participant's exercise file (or the reference solution)."""
    import importlib.util
    from pathlib import Path
    folder = Path(file).resolve().parent / ("solutions" if solution else "exercises")
    spec = importlib.util.spec_from_file_location("under_test", folder / module_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ------------------------------------------ RIPEMD160 fallback (pure python)
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
