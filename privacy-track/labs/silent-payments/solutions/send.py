"""
REFERENCE SOLUTION - Silent Payments sender (BIP352).

Facilitators: this passes every sending vector in vectors/. Participants:
try the exercise in ../send.py first. Run with:  python3 run_vectors.py send --solution
"""

from secp import G, N, Point, tagged_hash
import bech32m

K_MAX = 2323  # BIP352 per-group recipient limit


def decode_sp_address(address: str):
    hrp, version, payload = bech32m.decode(address)
    if hrp not in ("sp", "tsp"):
        raise ValueError("not a silent payment address")
    if version != 0 or len(payload) != 66:
        raise ValueError("unsupported version or bad length")
    return Point.from_bytes(payload[:33]), Point.from_bytes(payload[33:])


def sum_input_private_keys(inputs):
    a_sum = 0
    for a, is_taproot in inputs:
        if is_taproot and not (a * G).has_even_y():
            a = N - a
        a_sum = (a_sum + a) % N
    return a_sum


def input_hash(outpoints, A_sum: Point) -> int:
    smallest = min(outpoints)
    return int.from_bytes(tagged_hash("BIP0352/Inputs", smallest + A_sum.to_bytes()), "big")


def output_pubkey(ecdh_shared_secret: Point, B_m: Point, k: int) -> Point:
    t_k = tagged_hash("BIP0352/SharedSecret", ecdh_shared_secret.to_bytes() + k.to_bytes(4, "big"))
    return B_m + int.from_bytes(t_k, "big") * G


def create_outputs(inputs, outpoints, recipients):
    a_sum = sum_input_private_keys(inputs)
    if a_sum == 0:
        return []
    h = input_hash(outpoints, a_sum * G)

    groups = {}
    for address in recipients:
        B_scan, B_m = decode_sp_address(address)
        groups.setdefault(B_scan, []).append(B_m)
    if any(len(g) > K_MAX for g in groups.values()):
        return []

    outputs = []
    for B_scan, B_ms in groups.items():
        ecdh_shared_secret = (h * a_sum % N) * B_scan
        for k, B_m in enumerate(B_ms):
            outputs.append(output_pubkey(ecdh_shared_secret, B_m, k).to_xonly())
    return outputs
