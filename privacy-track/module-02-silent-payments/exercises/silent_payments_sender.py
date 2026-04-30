"""
Bitcoin Privacy Track — Module 2, Session 2: Silent Payments Sender
Code Orange Dev School | codeorange.dev

Implement a minimal Silent Payments (BIP352) sender in Python.

Prerequisites:
- Understanding of elliptic curve cryptography (Bitcoin Dojo Week 1-2)
- Python 3.8+
- pip install secp256k1 (or use the pure-Python fallback below)

References:
- BIP352: https://bips.dev/352/
- Bitcoin Optech: https://bitcoinops.org/en/topics/silent-payments/

Instructions:
- Complete each function by filling in the code where indicated
- Run this file with: python3 silent_payments_sender.py
- Discuss your solutions at the weekly call
"""

import hashlib
import secrets


# ============================================================
# Helpers (provided)
# ============================================================

def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def tagged_hash(tag: str, data: bytes) -> bytes:
    """BIP340-style tagged hash: SHA256(SHA256(tag) || SHA256(tag) || data)"""
    tag_hash = sha256(tag.encode())
    return sha256(tag_hash + tag_hash + data)


# Secp256k1 curve parameters
P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8


def point_add(p1, p2):
    """Add two points on secp256k1. None represents the point at infinity."""
    if p1 is None:
        return p2
    if p2 is None:
        return p1

    x1, y1 = p1
    x2, y2 = p2

    if x1 == x2 and y1 != y2:
        return None

    if x1 == x2:
        s = (3 * x1 * x1 * pow(2 * y1, P - 2, P)) % P
    else:
        s = ((y2 - y1) * pow(x2 - x1, P - 2, P)) % P

    x3 = (s * s - x1 - x2) % P
    y3 = (s * (x1 - x3) - y1) % P
    return (x3, y3)


def scalar_mult(k, point):
    """Multiply a point by a scalar on secp256k1."""
    result = None
    addend = point
    while k:
        if k & 1:
            result = point_add(result, addend)
        addend = point_add(addend, addend)
        k >>= 1
    return result


G = (Gx, Gy)


def privkey_to_pubkey(privkey: int) -> tuple:
    """Derive the public key (point) from a private key (scalar)."""
    return scalar_mult(privkey, G)


def serialize_pubkey(point: tuple, compressed: bool = True) -> bytes:
    """Serialize a public key point to bytes."""
    x, y = point
    if compressed:
        prefix = b'\x02' if y % 2 == 0 else b'\x03'
        return prefix + x.to_bytes(32, 'big')
    return b'\x04' + x.to_bytes(32, 'big') + y.to_bytes(32, 'big')


# ============================================================
# Exercise 1: Generate a Silent Payment Address
# ============================================================
#
# A Silent Payment address contains two public keys:
#   B_scan  — used to detect payments (can be on a hot device)
#   B_spend — used to spend received coins (kept cold)
#
# Both are derived from a master key at BIP352 derivation paths.
# For this exercise, we generate them directly from random scalars.

def generate_silent_payment_keypair():
    """Generate a Silent Payment scan/spend keypair.

    Returns:
        tuple: (b_scan_privkey, b_scan_pubkey, b_spend_privkey, b_spend_pubkey)
               where privkeys are ints and pubkeys are (x, y) tuples
    """
    # YOUR CODE HERE
    # 1. Generate a random private key for scanning (b_scan)
    #    b_scan = random integer in range [1, N-1]
    # 2. Derive B_scan = b_scan * G
    # 3. Generate a random private key for spending (b_spend)
    # 4. Derive B_spend = b_spend * G
    # 5. Return (b_scan, B_scan, b_spend, B_spend)

    pass


# ============================================================
# Exercise 2: Derive the Shared Secret
# ============================================================
#
# When sending a Silent Payment, the sender computes a shared
# secret using ECDH between their input keys and the receiver's
# scan public key.
#
# The process:
# 1. Sum all input private keys: a_sum = a_1 + a_2 + ... (mod N)
# 2. Compute input_hash = hash(smallest_outpoint || A_sum)
# 3. Shared secret = input_hash * a_sum * B_scan

def derive_shared_secret(input_privkeys: list, outpoints: list, B_scan: tuple) -> tuple:
    """Derive the ECDH shared secret for a Silent Payment.

    Args:
        input_privkeys: list of private keys (ints) for the sender's inputs
        outpoints: list of outpoint bytes (txid + vout) for ordering
        B_scan: receiver's scan public key (x, y)

    Returns:
        tuple: the shared secret point (x, y)
    """
    # YOUR CODE HERE
    # 1. Sum all input private keys modulo N
    #    a_sum = sum(input_privkeys) % N
    #
    # 2. Compute A_sum = a_sum * G (the summed public key)
    #
    # 3. Sort outpoints lexicographically, take the smallest
    #    smallest_outpoint = sorted(outpoints)[0]
    #
    # 4. Compute input_hash = tagged_hash("BIP0352/Inputs",
    #                                      smallest_outpoint + serialize_pubkey(A_sum))
    #    Convert to integer: input_hash_int = int.from_bytes(input_hash, 'big') % N
    #
    # 5. Compute the shared secret point:
    #    shared_secret = scalar_mult((input_hash_int * a_sum) % N, B_scan)
    #
    # 6. Return shared_secret

    pass


# ============================================================
# Exercise 3: Compute the Output Key
# ============================================================
#
# The output key is what appears on-chain as a Taproot output.
# It's derived from the shared secret and the receiver's spend key.
#
# output_key = B_spend + t_k * G
# where t_k = tagged_hash("BIP0352/SharedSecret", ser(shared_secret) || k)

def compute_output_key(shared_secret: tuple, B_spend: tuple, k: int = 0) -> tuple:
    """Compute the Silent Payment output key.

    Args:
        shared_secret: the ECDH shared secret point (x, y)
        B_spend: receiver's spend public key (x, y)
        k: output index (0 for first output, 1 for second, etc.)

    Returns:
        tuple: the output public key (x, y) for the Taproot output
    """
    # YOUR CODE HERE
    # 1. Serialize the shared secret's x-coordinate (32 bytes, big-endian)
    #    ss_bytes = shared_secret[0].to_bytes(32, 'big')
    #
    # 2. Compute the tweak:
    #    t_k = tagged_hash("BIP0352/SharedSecret", ss_bytes + k.to_bytes(4, 'big'))
    #    t_k_int = int.from_bytes(t_k, 'big') % N
    #
    # 3. Compute the tweak point: T = t_k_int * G
    #
    # 4. Add to the spend key: output_key = point_add(B_spend, T)
    #
    # 5. Return output_key

    pass


# ============================================================
# Exercise 4: Full Silent Payment Send
# ============================================================
#
# Combine exercises 1-3 to simulate a full Silent Payment.

def send_silent_payment():
    """Simulate sending a Silent Payment.

    1. Receiver generates a Silent Payment address (scan + spend keys)
    2. Sender has some UTXOs with known private keys
    3. Sender computes the output key
    4. The on-chain output is a P2TR output paying to the output key
    5. Receiver can detect this payment using their scan key
    """
    print("=" * 60)
    print("Silent Payment Sender — Full Simulation")
    print("=" * 60)

    # YOUR CODE HERE
    #
    # Step 1: Receiver generates their Silent Payment keypair
    # result = generate_silent_payment_keypair()
    # b_scan, B_scan, b_spend, B_spend = result
    # print(f"\nReceiver's scan pubkey:  {serialize_pubkey(B_scan).hex()}")
    # print(f"Receiver's spend pubkey: {serialize_pubkey(B_spend).hex()}")
    #
    # Step 2: Sender has 2 inputs (simulated)
    # sender_key_1 = secrets.randbelow(N - 1) + 1
    # sender_key_2 = secrets.randbelow(N - 1) + 1
    # outpoint_1 = secrets.token_bytes(36)  # simulated txid:vout
    # outpoint_2 = secrets.token_bytes(36)
    #
    # Step 3: Sender derives the shared secret
    # shared_secret = derive_shared_secret(
    #     [sender_key_1, sender_key_2],
    #     [outpoint_1, outpoint_2],
    #     B_scan
    # )
    # print(f"\nShared secret x: {shared_secret[0]}")
    #
    # Step 4: Sender computes the output key
    # output_key = compute_output_key(shared_secret, B_spend, k=0)
    # print(f"\nOutput key (on-chain Taproot address):")
    # print(f"  x: {output_key[0]}")
    # print(f"  Serialized: {serialize_pubkey(output_key).hex()}")
    #
    # Step 5: Verify — receiver can derive the same output key
    # (Receiver uses b_scan instead of a_sum to get the same shared secret)
    # a_sum = (sender_key_1 + sender_key_2) % N
    # A_sum = privkey_to_pubkey(a_sum)
    # smallest_outpoint = sorted([outpoint_1, outpoint_2])[0]
    # input_hash = tagged_hash("BIP0352/Inputs",
    #                          smallest_outpoint + serialize_pubkey(A_sum))
    # input_hash_int = int.from_bytes(input_hash, 'big') % N
    #
    # # Receiver's ECDH: b_scan * (input_hash * A_sum)
    # tweaked_A = scalar_mult(input_hash_int, A_sum)
    # receiver_shared_secret = scalar_mult(b_scan, tweaked_A)
    #
    # assert receiver_shared_secret == shared_secret, "Shared secrets don't match!"
    # print("\n✓ Receiver derived the same shared secret")
    #
    # receiver_output_key = compute_output_key(receiver_shared_secret, B_spend, k=0)
    # assert receiver_output_key == output_key, "Output keys don't match!"
    # print("✓ Receiver derived the same output key — payment detected!")
    #
    # print(f"\n{'=' * 60}")
    # print("On-chain, this looks like a normal Taproot output.")
    # print("Only the receiver (with b_scan) can detect it's theirs.")
    # print(f"{'=' * 60}")

    pass


# ============================================================
# TESTS
# ============================================================

def run_tests():
    print("=" * 60)
    print("Bitcoin Privacy Track — Silent Payments Sender Tests")
    print("=" * 60)

    # Test 1: Keypair generation
    print("\nTest 1: Keypair generation")
    result = generate_silent_payment_keypair()
    if result is None:
        print("  SKIPPED — generate_silent_payment_keypair() not implemented yet")
    else:
        b_scan, B_scan, b_spend, B_spend = result
        assert B_scan == privkey_to_pubkey(b_scan), "B_scan doesn't match b_scan"
        assert B_spend == privkey_to_pubkey(b_spend), "B_spend doesn't match b_spend"
        print("  PASSED")

    # Test 2: Shared secret derivation
    print("\nTest 2: Shared secret derivation")
    if result is None:
        print("  SKIPPED — depends on Exercise 1")
    else:
        test_privkeys = [secrets.randbelow(N - 1) + 1, secrets.randbelow(N - 1) + 1]
        test_outpoints = [secrets.token_bytes(36), secrets.token_bytes(36)]
        ss = derive_shared_secret(test_privkeys, test_outpoints, B_scan)
        if ss is None:
            print("  SKIPPED — derive_shared_secret() not implemented yet")
        else:
            assert ss[0] > 0 and ss[1] > 0, "Shared secret should be a valid point"
            print("  PASSED")

    # Test 3: Output key computation
    print("\nTest 3: Output key computation")
    if result is None or ss is None:
        print("  SKIPPED — depends on Exercises 1-2")
    else:
        ok = compute_output_key(ss, B_spend, k=0)
        if ok is None:
            print("  SKIPPED — compute_output_key() not implemented yet")
        else:
            assert ok[0] > 0 and ok[1] > 0, "Output key should be a valid point"
            print("  PASSED")

    # Test 4: Full simulation
    print("\nTest 4: Full Silent Payment simulation")
    send_silent_payment()

    print("\n" + "=" * 60)
    print("Done! Bring your solutions to the weekly call.")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()
