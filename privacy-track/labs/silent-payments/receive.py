"""
Session 2 lab - build a Silent Payments RECEIVER / scanner (BIP352)

Grade yourself against the official BIP352 test vectors:

    python3 run_vectors.py receive

You don't need to have finished Session 1: the grader computes the input hash
for you (that's the sender-side math).

Same toolbox as send.py: G, N, Point, a * G, P + Q, P - Q, -P, P.to_bytes(),
P.to_xonly(), Point.from_bytes(b), tagged_hash(tag, m).

Spec: https://github.com/bitcoin/bips/blob/master/bip-0352.mediawiki
      (sections "Scanning" and "Labels")
"""

from secp import G, N, Point, tagged_hash
import bech32m

K_MAX = 2323


# ---------------------------------------------------------------------------
# Exercise 1 - Make your address
#
# bech32m.encode(hrp, 0, B_scan.to_bytes() + B_spend.to_bytes())
# ---------------------------------------------------------------------------
def encode_sp_address(B_scan: Point, B_spend: Point, hrp: str = "sp") -> str:
    # YOUR CODE HERE
    return None


# ---------------------------------------------------------------------------
# Exercise 2 - The tweak (what an indexer serves you)
#
# For every transaction, the receiver needs  input_hash * A_sum.
# This doesn't depend on your keys at all, so a server can precompute it
# for every tx in every block and hand it to light clients. That's exactly
# what BlindBit Oracle, Frigate, and Bitcoin Core's upcoming index do.
# ---------------------------------------------------------------------------
def compute_tweak(A_sum: Point, input_hash: int) -> Point:
    # YOUR CODE HERE
    return None


# ---------------------------------------------------------------------------
# Exercise 3 - Scan one transaction
#
#   ecdh_shared_secret = b_scan * tweak
#   k = 0
#   loop:
#       t_k = tagged_hash("BIP0352/SharedSecret", ser_P(ecdh_shared_secret) || ser_32(k))
#       P_k = B_spend + t_k * G
#       if P_k.to_xonly() equals ANY remaining output:
#           record {"pub_key": out.hex(), "priv_key_tweak": t_k as 32-byte hex}
#           remove that output, k += 1, keep looping
#       else: stop
#   (never go past K_MAX)
#
# Two classic bugs: checking only outputs[k] (outputs can be in any order!),
# and stopping after the first match (one tx can pay you several times).
#
# Ignore `labels` until Exercise 4.
# ---------------------------------------------------------------------------
def scan(b_scan: int, B_spend: Point, tweak: Point, outputs, labels=None):
    """outputs: list of 32-byte x-only keys. Returns a list of dicts."""
    # YOUR CODE HERE
    return None


# ---------------------------------------------------------------------------
# Exercise 4 - Labels (stretch)
#
# Labels let one wallet hand out distinguishable addresses (donations vs
# invoices vs change) while scanning only once.
#
#   label_m  = tagged_hash("BIP0352/Label", ser_256(b_scan) || ser_32(m))  as int
#   B_m      = B_spend + label_m * G       <- the labeled address's spend key
#
# Then extend scan(): `labels` maps label_point.to_bytes() -> label_m.
# When an output doesn't equal P_k, it may equal P_k + label_m * G. Because
# the output is x-only you don't know its y, so for O = Point.from_bytes(out)
# check both  O - P_k  and  -O - P_k  against `labels`. On a hit the
# priv_key_tweak is (t_k + label_m) mod N.
# ---------------------------------------------------------------------------
def generate_label(b_scan: int, m: int) -> int:
    # YOUR CODE HERE
    return None


def labeled_spend_key(b_scan: int, B_spend: Point, m: int) -> Point:
    # YOUR CODE HERE
    return None


# ---------------------------------------------------------------------------
# Exercise 5 - Prove you can spend it (stretch)
#
# d = b_spend + priv_key_tweak (mod N). Taproot needs the even-y key, so if
# d * G has odd y, return N - d instead.
# ---------------------------------------------------------------------------
def spend_key(b_spend: int, priv_key_tweak: int) -> int:
    # YOUR CODE HERE
    return None


# ---------------------------------------------------------------------------
# Discussion (bring to the call):
#  - Your scan key can find payments but not spend them. What can someone
#    who steals b_scan learn? What can't they do?
#  - Exercise 2 runs on a server. What does that server learn about you?
#    Compare: downloading tweaks (BlindBit) vs sending b_scan (Frigate).
#  - Run scan_benchmark.py. How long for one day of mainnet on your laptop?
# ---------------------------------------------------------------------------
