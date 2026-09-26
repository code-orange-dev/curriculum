"""
Session 1 lab - build a Silent Payments SENDER (BIP352)

Fill in the five functions below, then grade yourself against the official
BIP352 test vectors (the same ones Bitcoin Core and every wallet use):

    python3 run_vectors.py send

Each function returns None until you implement it; the grader marks it
"not implemented yet" and moves on, so you can go one exercise at a time.

Toolbox (from secp.py):
    G, N                  generator point, group order
    a * G                 scalar times point  ->  Point
    P + Q, P - Q, -P      point arithmetic
    P.to_bytes()          33-byte compressed key   (BIP352's ser_P)
    P.to_xonly()          32-byte x-only key       (what a taproot output holds)
    P.has_even_y()        parity of y
    Point.from_bytes(b)   parse 33-byte or 32-byte key
    tagged_hash(tag, m)   BIP340-style tagged hash -> 32 bytes
    int.from_bytes(b, "big"),  n.to_bytes(4, "big")

Spec: https://github.com/bitcoin/bips/blob/master/bip-0352.mediawiki
      (section "Creating outputs")
"""

from secp import G, N, Point, tagged_hash
import bech32m

K_MAX = 2323  # BIP352: max outputs to one recipient (per B_scan) in one tx


# ---------------------------------------------------------------------------
# Exercise 1 - Read a silent payment address
#
# An SP address is bech32m: hrp "sp" (mainnet) or "tsp" (test networks),
# version 0, and a 66-byte payload = B_scan (33 bytes) || B_m (33 bytes).
# B_m is the spend key, possibly with a label added (Session 2).
#
# Use bech32m.decode(address) -> (hrp, version, payload).
# Reject anything that isn't hrp sp/tsp, version 0 and 66 bytes.
# ---------------------------------------------------------------------------
def decode_sp_address(address: str):
    """Return (B_scan, B_m) as Points."""
    # YOUR CODE HERE
    return None


# ---------------------------------------------------------------------------
# Exercise 2 - Sum the input private keys
#
# `inputs` is a list of (private_key: int, is_taproot: bool) for each
# eligible input. a_sum = a_1 + a_2 + ... (mod N).
#
# Catch: a taproot output only stores an x-only key, which always means the
# EVEN-y point. If a taproot private key a gives an odd-y point (a*G), the
# key actually in use is its negation N - a. Non-taproot keys are used as-is.
# ---------------------------------------------------------------------------
def sum_input_private_keys(inputs) -> int:
    # YOUR CODE HERE
    return None


# ---------------------------------------------------------------------------
# Exercise 3 - The input hash
#
# input_hash = tagged_hash("BIP0352/Inputs", outpoint_L || ser_P(A_sum))
#
#   outpoint_L  the smallest outpoint, comparing the 36-byte serializations
#               byte-by-byte (Python's min() on bytes does exactly that)
#   A_sum       a_sum * G
#
# Return it as an int. Why it exists: it makes the shared secret unique per
# transaction, so paying the same person twice from the same key does NOT
# produce the same address twice.
# ---------------------------------------------------------------------------
def input_hash(outpoints, A_sum: Point) -> int:
    # YOUR CODE HERE
    return None


# ---------------------------------------------------------------------------
# Exercise 4 - One output key
#
# t_k = tagged_hash("BIP0352/SharedSecret", ser_P(ecdh_shared_secret) || ser_32(k))
# P_k = B_m + t_k * G
#
#   ser_P      33-byte COMPRESSED point (not x-only! a classic bug)
#   ser_32(k)  k as 4 bytes, big-endian
# ---------------------------------------------------------------------------
def output_pubkey(ecdh_shared_secret: Point, B_m: Point, k: int) -> Point:
    # YOUR CODE HERE
    return None


# ---------------------------------------------------------------------------
# Exercise 5 - Put it together
#
#   1. a_sum = sum_input_private_keys(inputs). If it's 0, return [] (can't pay).
#   2. h = input_hash(outpoints, a_sum * G)
#   3. Group recipients by B_scan (same person, several addresses/labels).
#      If any group has more than K_MAX members, return [].
#   4. For each group:  ecdh_shared_secret = (h * a_sum mod N) * B_scan
#      then for k = 0, 1, 2 ... over that group's B_m values:
#          output = output_pubkey(ecdh_shared_secret, B_m, k)
#   5. Return the list of outputs as x-only bytes (P.to_xonly()).
#
# `outpoints` is a list of 36-byte serialized outpoints (ALL inputs).
# `recipients` is a list of SP address strings (may repeat).
# ---------------------------------------------------------------------------
def create_outputs(inputs, outpoints, recipients):
    # YOUR CODE HERE
    return None


# ---------------------------------------------------------------------------
# Discussion (bring to the call):
#  - The receiver can't know which of your inputs are "yours". Why does BIP352
#    sum ALL eligible inputs instead of using just one?
#  - Why must k restart at 0 for each recipient group?
#  - What breaks if you pay an SP address from a P2WSH multisig input only?
# ---------------------------------------------------------------------------
