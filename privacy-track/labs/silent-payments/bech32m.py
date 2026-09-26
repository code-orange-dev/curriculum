"""
Bech32m encoding for Silent Payment addresses. PROVIDED - you don't edit this.

An SP address is  hrp + "1" + bech32m(version || B_scan || B_spend)
  hrp      "sp" on mainnet, "tsp" on testnet/signet/regtest
  version  0 (a single 5-bit character, "q")
  payload  33-byte B_scan followed by 33-byte B_spend (66 bytes)

SP addresses are ~116 characters, so BIP352 raises bech32's 90-character
limit to 1023.
"""

CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"
BECH32M_CONST = 0x2BC830A3
MAX_LEN = 1023


def _polymod(values):
    gen = [0x3B6A57B2, 0x26508E6D, 0x1EA119FA, 0x3D4233DD, 0x2A1462B3]
    chk = 1
    for v in values:
        top = chk >> 25
        chk = (chk & 0x1FFFFFF) << 5 ^ v
        for i in range(5):
            chk ^= gen[i] if ((top >> i) & 1) else 0
    return chk


def _hrp_expand(hrp):
    return [ord(c) >> 5 for c in hrp] + [0] + [ord(c) & 31 for c in hrp]


def _convertbits(data, frombits, tobits, pad):
    acc, bits, out, maxv = 0, 0, [], (1 << tobits) - 1
    for value in data:
        acc = (acc << frombits) | value
        bits += frombits
        while bits >= tobits:
            bits -= tobits
            out.append((acc >> bits) & maxv)
    if pad and bits:
        out.append((acc << (tobits - bits)) & maxv)
    elif not pad and (bits >= frombits or ((acc << (tobits - bits)) & maxv)):
        raise ValueError("invalid padding")
    return out


def encode(hrp: str, version: int, payload: bytes) -> str:
    data = [version] + _convertbits(payload, 8, 5, True)
    values = _hrp_expand(hrp) + data
    polymod = _polymod(values + [0] * 6) ^ BECH32M_CONST
    checksum = [(polymod >> 5 * (5 - i)) & 31 for i in range(6)]
    return hrp + "1" + "".join(CHARSET[d] for d in data + checksum)


def decode(addr: str):
    """Return (hrp, version, payload_bytes). Raises ValueError if invalid."""
    if addr.lower() != addr and addr.upper() != addr:
        raise ValueError("mixed case")
    addr = addr.lower()
    if len(addr) > MAX_LEN:
        raise ValueError("too long")
    pos = addr.rfind("1")
    if pos < 1 or pos + 7 > len(addr):
        raise ValueError("bad separator position")
    hrp, rest = addr[:pos], addr[pos + 1:]
    if any(c not in CHARSET for c in rest):
        raise ValueError("invalid character")
    data = [CHARSET.find(c) for c in rest]
    if _polymod(_hrp_expand(hrp) + data) != BECH32M_CONST:
        raise ValueError("bad checksum (is this bech32m?)")
    version, payload = data[0], bytes(_convertbits(data[1:-6], 5, 8, False))
    return hrp, version, payload
