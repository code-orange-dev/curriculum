"""
Bitcoin Privacy Track — Module 4, Session 2: Compact Block Filters
Code Orange Dev School | codeorange.dev

Implement a simplified compact block filter (BIP158) from scratch,
then use it to understand how light clients can scan for transactions
privately.

This is critical infrastructure for Silent Payments on mobile devices.

Prerequisites:
- Understanding of hash functions and probabilistic data structures
- Completed Module 2 (Silent Payments scanning)
- Python 3.8+

References:
- BIP158: https://bips.dev/158/
- Golomb-Rice Coding: https://en.wikipedia.org/wiki/Golomb_coding

Instructions:
- Complete each function by filling in the code where indicated
- Run: python3 compact_block_filters.py
- Bring your results to the weekly session
"""

import hashlib
import struct
import math
import secrets
import time
from typing import List, Set, Optional
from io import BytesIO


# ============================================================
# Helpers (provided)
# ============================================================

def siphash(key: bytes, data: bytes) -> int:
    """SipHash-2-4 — the hash function used in BIP158 filters.

    For simplicity, we use a SHA256-based simulation.
    Real BIP158 uses SipHash-2-4 (much faster).
    """
    h = hashlib.sha256(key + data).digest()
    return int.from_bytes(h[:8], 'little')


def hash_to_range(item: bytes, f: int, key: bytes) -> int:
    """Hash an item to a value in [0, f).

    This maps each item uniformly into the filter's range,
    which is N * M where N = number of items and M = 784931 (BIP158).

    Args:
        item: the data element to hash
        f: the range upper bound (N * M)
        key: the hash key (derived from block hash)

    Returns:
        integer in [0, f)
    """
    h = siphash(key, item)
    return (h * f) >> 64 if f < (1 << 64) else h % f


# ============================================================
# BIP158 Parameters
# ============================================================

# BIP158 basic filter parameters
P = 19          # Golomb-Rice parameter (2^19 = 524288 — the false positive rate denominator)
M = 784931      # M ≈ 1.497137 * 2^P — optimized for minimum filter size


# ============================================================
# Exercise 1: Golomb-Rice Encoding
# ============================================================

class BitWriter:
    """Write individual bits to a byte buffer."""
    def __init__(self):
        self.data = bytearray()
        self.current_byte = 0
        self.bit_position = 0  # 0-7, MSB first

    def write_bit(self, bit: int):
        """Write a single bit (0 or 1)."""
        if bit:
            self.current_byte |= (1 << (7 - self.bit_position))
        self.bit_position += 1
        if self.bit_position == 8:
            self.data.append(self.current_byte)
            self.current_byte = 0
            self.bit_position = 0

    def write_bits(self, value: int, num_bits: int):
        """Write num_bits bits from value (MSB first)."""
        for i in range(num_bits - 1, -1, -1):
            self.write_bit((value >> i) & 1)

    def flush(self):
        """Flush remaining bits (pad with zeros)."""
        if self.bit_position > 0:
            self.data.append(self.current_byte)
            self.current_byte = 0
            self.bit_position = 0

    def get_bytes(self) -> bytes:
        self.flush()
        return bytes(self.data)


class BitReader:
    """Read individual bits from a byte buffer."""
    def __init__(self, data: bytes):
        self.data = data
        self.byte_index = 0
        self.bit_position = 0  # 0-7, MSB first

    def read_bit(self) -> int:
        """Read a single bit."""
        if self.byte_index >= len(self.data):
            raise EOFError("No more bits to read")
        bit = (self.data[self.byte_index] >> (7 - self.bit_position)) & 1
        self.bit_position += 1
        if self.bit_position == 8:
            self.byte_index += 1
            self.bit_position = 0
        return bit

    def read_bits(self, num_bits: int) -> int:
        """Read num_bits bits and return as integer."""
        value = 0
        for _ in range(num_bits):
            value = (value << 1) | self.read_bit()
        return value


def golomb_rice_encode(values: List[int], p: int = P) -> bytes:
    """Encode a sorted list of deltas using Golomb-Rice coding.

    Golomb-Rice coding splits each value into:
    - quotient q = value >> p  (encoded as q ones followed by a zero)
    - remainder r = value & ((1 << p) - 1)  (encoded as p bits)

    Args:
        values: list of non-negative integers (sorted deltas)
        p: Golomb-Rice parameter (number of bits for remainder)

    Returns:
        compressed bytes
    """
    # YOUR CODE HERE
    #
    # For each value in the list:
    # 1. Compute quotient: q = value >> p
    # 2. Compute remainder: r = value & ((1 << p) - 1)
    # 3. Write q ones followed by a zero (unary encoding of q)
    #    Example: q=3 → write bits 1, 1, 1, 0
    # 4. Write r as p bits (binary encoding)
    #
    # Use the BitWriter class to write bits
    # Return writer.get_bytes()

    pass


def golomb_rice_decode(data: bytes, n: int, p: int = P) -> List[int]:
    """Decode n Golomb-Rice coded values from data.

    Args:
        data: compressed bytes
        n: number of values to decode
        p: Golomb-Rice parameter

    Returns:
        list of decoded values
    """
    # YOUR CODE HERE
    #
    # For each of n values:
    # 1. Read unary-encoded quotient:
    #    Count consecutive 1-bits until you hit a 0
    #    q = count of 1-bits
    # 2. Read p bits for the remainder r
    # 3. value = (q << p) | r
    #
    # Use the BitReader class to read bits
    # Return list of decoded values

    pass


# ============================================================
# Exercise 2: Build a Compact Block Filter
# ============================================================

def build_filter(elements: List[bytes], block_hash: bytes) -> bytes:
    """Build a BIP158-style compact block filter.

    The filter contains all scriptPubKeys from the block's outputs
    and spent outputs. A light client can test whether their
    scriptPubKey appears in the filter WITHOUT downloading the block.

    Args:
        elements: list of scriptPubKey bytes to include in the filter
        block_hash: the block hash (used to derive the hash key)

    Returns:
        the compact block filter as bytes
    """
    # YOUR CODE HERE
    #
    # Algorithm:
    # 1. N = number of elements
    # 2. F = N * M  (the hash range)
    # 3. key = block_hash[:16]  (first 16 bytes as SipHash key)
    #
    # 4. Hash each element to a value in [0, F):
    #    hashed_values = [hash_to_range(elem, F, key) for elem in elements]
    #
    # 5. Sort the hashed values
    #
    # 6. Compute deltas (differences between consecutive sorted values):
    #    deltas[0] = sorted_values[0]
    #    deltas[i] = sorted_values[i] - sorted_values[i-1]
    #
    # 7. Golomb-Rice encode the deltas
    #
    # 8. Prepend N as a varint (CompactSize encoding):
    #    if N < 253: 1 byte
    #    if N < 65536: 0xfd + 2 bytes little-endian
    #    etc.
    #
    # 9. Return N_bytes + encoded_deltas

    pass


# ============================================================
# Exercise 3: Query the Filter
# ============================================================

def match_filter(filter_data: bytes, query_elements: List[bytes],
                 block_hash: bytes) -> bool:
    """Test if any of the query elements might be in the filter.

    This is what a light client does: given a compact block filter
    and a set of scriptPubKeys it's watching, determine if this
    block might contain a relevant transaction.

    Args:
        filter_data: the compact block filter bytes
        query_elements: list of scriptPubKeys to search for
        block_hash: the block hash (for deriving the hash key)

    Returns:
        True if any query element matches (may be a false positive!)
        False if definitely no match
    """
    # YOUR CODE HERE
    #
    # Algorithm:
    # 1. Parse N from the filter data (varint)
    # 2. F = N * M
    # 3. key = block_hash[:16]
    #
    # 4. Hash each query element to [0, F):
    #    query_values = sorted([hash_to_range(q, F, key) for q in query_elements])
    #
    # 5. Decode the filter to get the sorted set of hashed values
    #    (decode the Golomb-Rice deltas and compute cumulative sums)
    #
    # 6. Check if any query_value appears in the filter's sorted set
    #    Use a sorted merge (two-pointer technique) for efficiency:
    #    - Pointer i through filter values, pointer j through query values
    #    - If filter[i] == query[j]: MATCH → return True
    #    - If filter[i] < query[j]: advance i
    #    - If filter[i] > query[j]: advance j
    #
    # 7. If no match found → return False

    pass


# ============================================================
# Exercise 4: Measure Filter Properties
# ============================================================

def analyze_filter_properties():
    """Measure the size, false positive rate, and query time of filters.

    Simulates realistic block data and measures key properties.
    """
    print("\n" + "=" * 60)
    print("FILTER ANALYSIS")
    print("=" * 60)

    # Simulate a block with N unique scriptPubKeys
    sizes = [100, 500, 1000, 2500, 5000]

    for n_elements in sizes:
        # Generate random "scriptPubKeys"
        elements = [secrets.token_bytes(32) for _ in range(n_elements)]
        block_hash = secrets.token_bytes(32)

        # Build filter
        start = time.time()
        filter_data = build_filter(elements, block_hash)
        build_time = time.time() - start

        if filter_data is None:
            print(f"\n  {n_elements} elements: build_filter() not implemented")
            continue

        filter_size = len(filter_data)
        raw_size = n_elements * 32  # 32 bytes per scriptPubKey

        # Measure query time
        # Test with elements that ARE in the filter (should all match)
        true_positives = 0
        sample_size = min(100, n_elements)
        query_sample = elements[:sample_size]

        start = time.time()
        for q in query_sample:
            if match_filter(filter_data, [q], block_hash):
                true_positives += 1
        query_time = time.time() - start

        # Measure false positive rate
        # Test with elements NOT in the filter
        false_positives = 0
        fp_tests = 10000
        for _ in range(fp_tests):
            fake = secrets.token_bytes(32)
            if match_filter(filter_data, [fake], block_hash):
                false_positives += 1

        fp_rate = false_positives / fp_tests
        theoretical_fp = 1 / M  # BIP158's theoretical FP rate

        print(f"\n  Block with {n_elements} scriptPubKeys:")
        print(f"    Filter size:     {filter_size:,} bytes ({filter_size/raw_size*100:.1f}% of raw)")
        print(f"    Compression:     {raw_size/filter_size:.1f}x")
        print(f"    Build time:      {build_time*1000:.1f} ms")
        print(f"    Query time:      {query_time/sample_size*1000:.3f} ms per element")
        print(f"    True positives:  {true_positives}/{sample_size} ({true_positives/sample_size*100:.0f}%)")
        print(f"    False positives: {false_positives}/{fp_tests} ({fp_rate*100:.4f}%)")
        print(f"    Theoretical FP:  {theoretical_fp*100:.4f}%")

    # YOUR CODE HERE: Answer these questions
    #
    # 1. How does filter size scale with the number of elements?
    #    (Linear? Sub-linear? What's the per-element cost?)
    #
    # 2. Mainnet averages ~3000 outputs per block. What would the
    #    filter size be? Compare to the full block size (~1.5 MB).
    #
    # 3. If a wallet watches 100 addresses, how many false positive
    #    block downloads per day? (Mainnet: ~144 blocks/day)
    #
    # 4. How does this compare to BIP37 Bloom filters in terms of privacy?
    #    With Bloom filters, the server knows which addresses you're watching.
    #    With compact block filters, the server knows nothing.

    pass


# ============================================================
# Exercise 5: Silent Payments + Compact Block Filters
# ============================================================

def simulate_sp_scanning_with_filters():
    """Simulate how compact block filters improve Silent Payment scanning.

    Without filters: scan every transaction in every block (ECDH per tx)
    With filters: first check filter, only scan matching blocks

    This is the key optimization that makes Silent Payments viable
    on mobile devices.
    """
    print("\n" + "=" * 60)
    print("SILENT PAYMENTS + COMPACT BLOCK FILTERS")
    print("=" * 60)

    # Simulate 144 blocks (1 day of mainnet)
    num_blocks = 144
    txs_per_block = 3000
    ecdh_time_ms = 0.5  # ~0.5ms per ECDH operation (mobile device estimate)

    # Without filters: scan everything
    total_txs = num_blocks * txs_per_block
    scan_time_no_filter = total_txs * ecdh_time_ms / 1000  # seconds

    print(f"\n  Scenario: {num_blocks} blocks, {txs_per_block} tx/block")
    print(f"  Total transactions: {total_txs:,}")
    print(f"  ECDH time estimate: {ecdh_time_ms} ms/operation")

    print(f"\n  WITHOUT filters:")
    print(f"    ECDH operations: {total_txs:,}")
    print(f"    Scan time: {scan_time_no_filter:.0f} seconds ({scan_time_no_filter/60:.1f} minutes)")

    # With filters: check filter first, only download matching blocks
    # A filter match means "this block MIGHT have your payment"
    # False positive rate determines how many extra blocks you download

    # YOUR CODE HERE
    #
    # Calculate:
    # 1. filter_download_size = num_blocks * estimated_filter_size_per_block
    #    (Use your analysis from Exercise 4 for a 3000-element block)
    #
    # 2. Expected false positive blocks per day:
    #    Each block filter has FP rate ≈ 1/M ≈ 1/784931
    #    But the receiver is checking against their tweaked output key
    #    Expected matches = num_blocks * (1/M)
    #    Add 1 for the actual payment block
    #
    # 3. For matching blocks only, scan all transactions (ECDH per tx)
    #    matching_blocks = expected_false_positives + 1
    #    scan_time_with_filter = matching_blocks * txs_per_block * ecdh_time_ms / 1000
    #
    # 4. Total time = filter_check_time + scan_time_with_filter
    #    filter_check_time is negligible (just bit matching, no ECDH)
    #
    # 5. Print the comparison:
    #    Speedup = scan_time_no_filter / total_time_with_filter
    #
    # QUESTION: Is the filtered scanning time acceptable for a mobile wallet
    # that syncs once per day? What about once per hour?

    pass


# ============================================================
# Run all exercises
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("Bitcoin Privacy Track — Compact Block Filters")
    print("Code Orange Dev School | codeorange.dev")
    print("=" * 70)

    # Exercise 1: Test Golomb-Rice coding
    print("\nExercise 1: Golomb-Rice Encoding/Decoding")
    test_values = [5, 12, 3, 100, 0, 7, 42, 1, 88, 15]
    encoded = golomb_rice_encode(test_values)
    if encoded is None:
        print("  golomb_rice_encode() not implemented yet")
    else:
        decoded = golomb_rice_decode(encoded, len(test_values))
        if decoded is None:
            print("  golomb_rice_decode() not implemented yet")
        else:
            match = decoded == test_values
            print(f"  Original:  {test_values}")
            print(f"  Decoded:   {decoded}")
            print(f"  Match: {'PASS' if match else 'FAIL'}")
            print(f"  Raw size:  {len(test_values) * 4} bytes (32-bit ints)")
            print(f"  Encoded:   {len(encoded)} bytes")
            print(f"  Ratio:     {len(encoded) / (len(test_values) * 4) * 100:.0f}%")

    # Exercise 2-3: Build and query a filter
    print("\nExercise 2-3: Build and Query Filter")
    elements = [f"scriptpubkey_{i}".encode() for i in range(100)]
    block_hash = hashlib.sha256(b"test_block").digest()

    filter_data = build_filter(elements, block_hash)
    if filter_data is None:
        print("  build_filter() not implemented yet")
    else:
        print(f"  Filter built: {len(filter_data)} bytes for {len(elements)} elements")

        # Test: element IN the filter
        found = match_filter(filter_data, [elements[42]], block_hash)
        print(f"  Query known element: {'MATCH (correct)' if found else 'NO MATCH (bug!)'}")

        # Test: element NOT in the filter
        found = match_filter(filter_data, [b"not_in_filter"], block_hash)
        print(f"  Query unknown element: {'FALSE POSITIVE' if found else 'NO MATCH (correct)'}")

    # Exercise 4: Filter analysis
    print("\nExercise 4: Filter Properties")
    analyze_filter_properties()

    # Exercise 5: SP + CBF simulation
    print("\nExercise 5: Silent Payments + Compact Block Filters")
    simulate_sp_scanning_with_filters()

    print("\n" + "=" * 70)
    print("REFLECTION QUESTIONS:")
    print("=" * 70)
    print("""
    1. Why does BIP158 use Golomb-Rice coding instead of simpler
       compression? What property of the delta values makes GR efficient?

    2. If you increase the parameter P (and thus M), what happens to:
       a) Filter size?
       b) False positive rate?
       c) Number of blocks a light client downloads unnecessarily?

    3. A malicious full node could send you a WRONG filter (omitting
       your transaction). How does BIP157 handle this?
       Hint: filter headers form a chain, and you can ask multiple peers.

    4. For Silent Payments specifically, the "query element" changes
       for every block (because it depends on the sender's inputs).
       How does this affect the filter-checking approach?

    5. Could compact block filters be used to improve Payjoin receiver
       efficiency? Why or why not?
    """)
    print("=" * 70)
    print("Done! Bring your results to the weekly session.")
    print("=" * 70)
