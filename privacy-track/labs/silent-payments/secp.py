"""
Tiny pure-Python secp256k1, just enough for BIP352. PROVIDED - you don't edit this.

Teaching code: slow and NOT constant-time. Never use it with real keys.

    G                  the generator point
    N                  the group order (private keys / scalars live in [1, N-1])
    Point              a curve point; supports  P + Q,  P - Q,  -P,  k * P
    Point.infinity()   the "zero" point (e.g. the sum of P and -P)
    tagged_hash(t, m)  BIP340 tagged hash: SHA256(SHA256(t) || SHA256(t) || m)
"""

import hashlib

P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141


def tagged_hash(tag: str, msg: bytes) -> bytes:
    t = hashlib.sha256(tag.encode()).digest()
    return hashlib.sha256(t + t + msg).digest()


class Point:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x = x
        self.y = y

    # --- construction -------------------------------------------------
    @staticmethod
    def infinity() -> "Point":
        return Point(None, None)

    @staticmethod
    def lift_x(x: int, even_y: bool = True) -> "Point":
        """Find the point with this x coordinate (even y by default, as BIP340)."""
        if not 0 <= x < P:
            raise ValueError("x out of range")
        c = (pow(x, 3, P) + 7) % P
        y = pow(c, (P + 1) // 4, P)
        if y * y % P != c:
            raise ValueError("x is not on the curve")
        if (y % 2 == 0) != even_y:
            y = P - y
        return Point(x, y)

    @staticmethod
    def from_bytes(b: bytes) -> "Point":
        """Parse a 33-byte compressed (02/03 || x) or 32-byte x-only key."""
        if len(b) == 32:
            return Point.lift_x(int.from_bytes(b, "big"))
        if len(b) == 33 and b[0] in (2, 3):
            return Point.lift_x(int.from_bytes(b[1:], "big"), even_y=(b[0] == 2))
        raise ValueError("expected 32 or 33 bytes of public key")

    # --- properties / serialization -----------------------------------
    @property
    def is_infinity(self) -> bool:
        return self.x is None

    def has_even_y(self) -> bool:
        return self.y % 2 == 0

    def to_bytes(self) -> bytes:
        """33-byte compressed encoding. BIP352 calls this ser_P(P)."""
        return (b"\x02" if self.has_even_y() else b"\x03") + self.x.to_bytes(32, "big")

    def to_xonly(self) -> bytes:
        """32-byte x-only encoding - what a taproot output commits to."""
        return self.x.to_bytes(32, "big")

    # --- arithmetic ---------------------------------------------------
    def __eq__(self, other):
        return isinstance(other, Point) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __neg__(self):
        return self if self.is_infinity else Point(self.x, (-self.y) % P)

    def __add__(self, other: "Point") -> "Point":
        if self.is_infinity:
            return other
        if other.is_infinity:
            return self
        if self.x == other.x:
            if (self.y + other.y) % P == 0:
                return Point.infinity()
            lam = 3 * self.x * self.x * pow(2 * self.y, -1, P) % P
        else:
            lam = (other.y - self.y) * pow(other.x - self.x, -1, P) % P
        x3 = (lam * lam - self.x - other.x) % P
        return Point(x3, (lam * (self.x - x3) - self.y) % P)

    def __sub__(self, other: "Point") -> "Point":
        return self + (-other)

    def __rmul__(self, k: int) -> "Point":
        k %= N
        if self is G or self == G:
            return _mul_G(k)
        result, addend = Point.infinity(), self
        while k:
            if k & 1:
                result = result + addend
            addend = addend + addend
            k >>= 1
        return result

    def __repr__(self):
        return "Point(infinity)" if self.is_infinity else f"Point({self.to_bytes().hex()})"


G = Point(0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
          0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)

# Precomputed 2^i * G makes k * G about twice as fast (only additions).
_G_TABLE = [G]
for _ in range(255):
    _G_TABLE.append(_G_TABLE[-1] + _G_TABLE[-1])


def _mul_G(k: int) -> Point:
    result = Point.infinity()
    i = 0
    while k:
        if k & 1:
            result = result + _G_TABLE[i]
        k >>= 1
        i += 1
    return result
