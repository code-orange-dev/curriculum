"""
Bitcoin Privacy Track — Module 2, Session 3: Silent Payments Scanner
Code Orange Dev School | codeorange.dev

Implement a minimal Silent Payments receiver/scanner.

The challenge: to detect a Silent Payment, the receiver must scan
every transaction in every block and perform an ECDH computation
to check if any output belongs to them.

Prerequisites:
- Completed silent_payments_sender.py (Session 2)
- Understanding of ECDH and BIP352 key derivation

Instructions:
- Complete each function by filling in the code where indicated
- Run this file with: python3 silent_payments_scanner.py
- Discuss your solutions at the weekly call
"""

import hashlib
import secrets
import time

# Import helpers from the sender exercise
# (In practice, you'd have these in a shared module)
from silent_payments_sender import (
    sha256, tagged_hash, P, N, G, Gx, Gy,
    point_add, scalar_mult, privkey_to_pubkey,
    serialize_pubkey, generate_silent_payment_keypair,
    derive_shared_secret, compute_output_key
)


# ============================================================
# Exercise 1: Scan a Single Transaction
# ============================================================
#
# Given a transaction's input public keys and outputs,
# check if any output is a Silent Payment to the receiver.

def scan_transaction(tx_input_pubkeys: list, tx_outpoints: list,
                     tx_output_keys: list, b_scan: int, B_spend: tuple) -> list:
    """Scan a transaction for Silent Payments to the receiver.

    Args:
        tx_input_pubkeys: list of public key points [(x,y), ...] from tx inputs
        tx_outpoints: list of outpoint bytes from tx inputs
        tx_output_keys: list of output public key points [(x,y), ...] (Taproot outputs)
        b_scan: receiver's scan private key (int)
        B_spend: receiver's spend public key (x, y)

    Returns:
        list of tuples: [(output_index, output_key), ...] for detected payments
    """
    # YOUR CODE HERE
    #
    # 1. Sum all input public keys: A_sum = P1 + P2 + ...
    #    (Use point_add repeatedly)
    #
    # 2. Find the smallest outpoint (lexicographic sort)
    #
    # 3. Compute input_hash = tagged_hash("BIP0352/Inputs",
    #                                      smallest_outpoint + serialize_pubkey(A_sum))
    #    input_hash_int = int.from_bytes(input_hash, 'big') % N
    #
    # 4. Compute the tweaked sum: tweaked_A = input_hash_int * A_sum
    #
    # 5. Receiver's ECDH: shared_secret = b_scan * tweaked_A
    #
    # 6. For each output index k, compute:
    #    expected_output = compute_output_key(shared_secret, B_spend, k)
    #    If expected_output matches tx_output_keys[k], it's a payment to us!
    #
    # 7. Return list of (output_index, output_key) for matches

    pass


# ============================================================
# Exercise 2: Scan a Block
# ============================================================
#
# Scan all transactions in a simulated block.

def scan_block(block_txs: list, b_scan: int, B_spend: tuple) -> list:
    """Scan all transactions in a block for Silent Payments.

    Args:
        block_txs: list of dicts, each with keys:
            'input_pubkeys': list of (x,y) tuples
            'outpoints': list of bytes
            'output_keys': list of (x,y) tuples
        b_scan: receiver's scan private key
        B_spend: receiver's spend public key

    Returns:
        list of tuples: [(tx_index, output_index, output_key), ...]
    """
    # YOUR CODE HERE
    #
    # For each transaction in block_txs:
    #   results = scan_transaction(tx['input_pubkeys'], tx['outpoints'],
    #                              tx['output_keys'], b_scan, B_spend)
    #   For each match, append (tx_index, output_index, output_key)
    #
    # Return all matches

    pass


# ============================================================
# Exercise 3: Benchmark Scanning Performance
# ============================================================
#
# How fast can you scan? This exercise generates simulated blocks
# and measures scanning time.

def benchmark_scanning(num_blocks: int = 10, txs_per_block: int = 50):
    """Benchmark Silent Payment scanning performance.

    Generates simulated blocks with random transactions, plants
    one Silent Payment in a random block, and measures how long
    it takes to find it.
    """
    print(f"\nBenchmark: scanning {num_blocks} blocks x {txs_per_block} txs")

    # Generate receiver keys
    b_scan, B_scan, b_spend, B_spend = generate_silent_payment_keypair()

    # Generate simulated blocks
    blocks = []
    planted_block = secrets.randbelow(num_blocks)
    planted_tx = secrets.randbelow(txs_per_block)

    for block_idx in range(num_blocks):
        txs = []
        for tx_idx in range(txs_per_block):
            # Random sender keys
            num_inputs = secrets.randbelow(3) + 1
            sender_keys = [secrets.randbelow(N - 1) + 1 for _ in range(num_inputs)]
            input_pubkeys = [privkey_to_pubkey(k) for k in sender_keys]
            outpoints = [secrets.token_bytes(36) for _ in range(num_inputs)]

            # Random outputs (2-4 per tx)
            num_outputs = secrets.randbelow(3) + 2
            output_keys = [privkey_to_pubkey(secrets.randbelow(N - 1) + 1)
                          for _ in range(num_outputs)]

            # Plant a real Silent Payment in one specific transaction
            if block_idx == planted_block and tx_idx == planted_tx:
                shared_secret = derive_shared_secret(sender_keys, outpoints, B_scan)
                real_output = compute_output_key(shared_secret, B_spend, k=0)
                output_keys[0] = real_output
                print(f"  Planted SP in block {block_idx}, tx {tx_idx}, output 0")

            txs.append({
                'input_pubkeys': input_pubkeys,
                'outpoints': outpoints,
                'output_keys': output_keys
            })
        blocks.append(txs)

    # YOUR CODE HERE
    # Time the scanning process
    #
    # start = time.time()
    # found = []
    # for block_idx, block_txs in enumerate(blocks):
    #     matches = scan_block(block_txs, b_scan, B_spend)
    #     for tx_idx, out_idx, out_key in matches:
    #         found.append((block_idx, tx_idx, out_idx))
    # elapsed = time.time() - start
    #
    # print(f"\n  Scanned {num_blocks * txs_per_block} transactions in {elapsed:.3f}s")
    # print(f"  Rate: {num_blocks * txs_per_block / elapsed:.0f} tx/s")
    # print(f"  Found {len(found)} Silent Payment(s): {found}")
    #
    # # Mainnet has ~300,000 tx/day. How long would that take?
    # mainnet_estimate = 300_000 / (num_blocks * txs_per_block / elapsed)
    # print(f"\n  Estimated mainnet scanning time: {mainnet_estimate:.0f}s ({mainnet_estimate/60:.1f} min) per day of blocks")
    #
    # QUESTION: Is this fast enough for a mobile wallet?
    # QUESTION: How would compact block filters (BIP157/158) help?

    pass


# ============================================================
# Run all exercises
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Bitcoin Privacy Track — Silent Payments Scanner")
    print("=" * 60)

    # Test scanning with a known payment
    print("\nExercise 1-2: Scan for a planted Silent Payment")

    b_scan, B_scan, b_spend, B_spend = generate_silent_payment_keypair()

    if b_scan is None:
        print("  Complete silent_payments_sender.py first!")
    else:
        # Create a transaction with a Silent Payment
        sender_key = secrets.randbelow(N - 1) + 1
        outpoint = secrets.token_bytes(36)

        shared_secret = derive_shared_secret([sender_key], [outpoint], B_scan)
        sp_output = compute_output_key(shared_secret, B_spend, k=0)
        random_output = privkey_to_pubkey(secrets.randbelow(N - 1) + 1)

        if shared_secret is not None and sp_output is not None:
            found = scan_transaction(
                tx_input_pubkeys=[privkey_to_pubkey(sender_key)],
                tx_outpoints=[outpoint],
                tx_output_keys=[sp_output, random_output],
                b_scan=b_scan,
                B_spend=B_spend
            )

            if found is None:
                print("  scan_transaction() not implemented yet")
            elif len(found) == 1 and found[0][0] == 0:
                print(f"  PASSED — detected Silent Payment at output index {found[0][0]}")
            else:
                print(f"  FAILED — expected 1 match at index 0, got: {found}")

    # Benchmark
    print("\nExercise 3: Benchmark scanning performance")
    benchmark_scanning(num_blocks=5, txs_per_block=20)

    print("\n" + "=" * 60)
    print("Done! Bring your solutions and benchmark results to the weekly call.")
    print("=" * 60)
