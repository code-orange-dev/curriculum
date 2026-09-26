"""
REFERENCE SOLUTION - Silent Payments receiver / scanner (BIP352).

Passes every receiving vector in vectors/. Run with:
    python3 run_vectors.py receive --solution
"""

from secp import G, N, Point, tagged_hash
import bech32m

K_MAX = 2323


def encode_sp_address(B_scan: Point, B_spend: Point, hrp: str = "sp") -> str:
    return bech32m.encode(hrp, 0, B_scan.to_bytes() + B_spend.to_bytes())


def generate_label(b_scan: int, m: int) -> int:
    return int.from_bytes(tagged_hash("BIP0352/Label", b_scan.to_bytes(32, "big") + m.to_bytes(4, "big")), "big")


def labeled_spend_key(b_scan: int, B_spend: Point, m: int) -> Point:
    return B_spend + generate_label(b_scan, m) * G


def compute_tweak(A_sum: Point, input_hash: int) -> Point:
    return input_hash * A_sum


def scan(b_scan: int, B_spend: Point, tweak: Point, outputs, labels=None):
    labels = labels or {}
    ecdh_shared_secret = b_scan * tweak
    remaining = list(outputs)
    found = []
    k = 0
    while k < K_MAX:
        t_k = int.from_bytes(tagged_hash("BIP0352/SharedSecret",
                                         ecdh_shared_secret.to_bytes() + k.to_bytes(4, "big")), "big")
        P_k = B_spend + t_k * G
        match = None
        for out in remaining:
            if out == P_k.to_xonly():
                match = (out, t_k)
                break
            if labels:
                # The output could be P_k + label*G. The x-only output hides its y,
                # so try both candidates: output - P_k and -output - P_k.
                O = Point.from_bytes(out)
                for diff in (O - P_k, -O - P_k):
                    if not diff.is_infinity and diff.to_bytes() in labels:
                        match = (out, (t_k + labels[diff.to_bytes()]) % N)
                        break
                if match:
                    break
        if match is None:
            break
        remaining.remove(match[0])
        found.append({"pub_key": match[0].hex(), "priv_key_tweak": match[1].to_bytes(32, "big").hex()})
        k += 1
    return found


def spend_key(b_spend: int, priv_key_tweak: int) -> int:
    d = (b_spend + priv_key_tweak) % N
    return d if (d * G).has_even_y() else N - d
