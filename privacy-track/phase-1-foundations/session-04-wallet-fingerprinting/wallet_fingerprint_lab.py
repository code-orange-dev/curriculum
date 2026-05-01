"""
Wallet Fingerprinting Exercise
===============================

This exercise teaches students how to identify which wallet software created a Bitcoin transaction
by analyzing characteristic patterns and heuristics. Real-world wallets often have distinctive
behaviors that can leak information about the user, even without identifying personal information.

Learning Objectives:
- Understand wallet fingerprinting and privacy implications
- Identify common fingerprinting vectors: locktime, sequence numbers, script types, fee patterns
- Implement heuristic matching to guess wallet software
- Learn how to construct privacy-aware transactions

Students must implement seven analysis functions and one construction function to complete this lab.
"""

from typing import Dict, List, Set, Tuple
from dataclasses import dataclass


@dataclass
class Transaction:
    """Represents a simplified Bitcoin transaction for analysis."""
    version: int
    locktime: int
    inputs: List[Dict]  # Each has: sequence, script_type, amount
    outputs: List[Dict]  # Each has: script_type, amount
    fee_rate: float  # satoshis per byte


# Sample transaction data representing different wallets
SAMPLE_TRANSACTIONS = [
    # TX 1: Bitcoin Core - anti-fee-sniping, max sequence, P2WPKH outputs
    Transaction(
        version=2,
        locktime=856000,  # Anti-fee-sniping: recent block height
        inputs=[
            {"sequence": 0xfffffffe, "script_type": "P2WPKH", "amount": 50000},
            {"sequence": 0xfffffffe, "script_type": "P2WPKH", "amount": 30000},
        ],
        outputs=[
            {"script_type": "P2WPKH", "amount": 45000},
            {"script_type": "P2WPKH", "amount": 34500},
        ],
        fee_rate=2.5,
    ),
    # TX 2: Electrum - always zero locktime, RBF signaling
    Transaction(
        version=2,
        locktime=0,
        inputs=[
            {"sequence": 0xfffffffd, "script_type": "P2PKH", "amount": 100000},
        ],
        outputs=[
            {"script_type": "P2PKH", "amount": 95000},
        ],
        fee_rate=1.8,
    ),
    # TX 3: BlueWallet - random locktime, mixed script types
    Transaction(
        version=2,
        locktime=712345,
        inputs=[
            {"sequence": 0xffffffff, "script_type": "P2WPKH", "amount": 75000},
        ],
        outputs=[
            {"script_type": "P2WPKH", "amount": 50000},
            {"script_type": "P2WSH", "amount": 24500},
        ],
        fee_rate=3.2,
    ),
    # TX 4: Wasabi - all-max sequence, multiple outputs, round change
    Transaction(
        version=2,
        locktime=0,
        inputs=[
            {"sequence": 0xffffffff, "script_type": "P2WPKH", "amount": 100000},
            {"sequence": 0xffffffff, "script_type": "P2WPKH", "amount": 50000},
        ],
        outputs=[
            {"script_type": "P2WPKH", "amount": 100000},
            {"script_type": "P2WPKH", "amount": 50000},
        ],
        fee_rate=2.0,
    ),
    # TX 5: Sparrow - structured output ordering, precise fee
    Transaction(
        version=2,
        locktime=0,
        inputs=[
            {"sequence": 0xffffffff, "script_type": "P2WPKH", "amount": 200000},
        ],
        outputs=[
            {"script_type": "P2WPKH", "amount": 100000},
            {"script_type": "P2WPKH", "amount": 99567},
        ],
        fee_rate=4.33,
    ),
    # TX 6: Samourai - multiple inputs, complex output set, suspicious ordering
    Transaction(
        version=2,
        locktime=0,
        inputs=[
            {"sequence": 0xfffffffe, "script_type": "P2WPKH", "amount": 50000},
            {"sequence": 0xfffffffe, "script_type": "P2WPKH", "amount": 40000},
            {"sequence": 0xfffffffe, "script_type": "P2WPKH", "amount": 30000},
        ],
        outputs=[
            {"script_type": "P2WPKH", "amount": 45000},
            {"script_type": "P2WPKH", "amount": 35000},
            {"script_type": "P2WPKH", "amount": 39250},
        ],
        fee_rate=2.75,
    ),
    # TX 7: Trezor Suite - consistent sequence, P2WPKH preference
    Transaction(
        version=2,
        locktime=0,
        inputs=[
            {"sequence": 0xffffffff, "script_type": "P2WPKH", "amount": 80000},
        ],
        outputs=[
            {"script_type": "P2WPKH", "amount": 75000},
            {"script_type": "P2WPKH", "amount": 4800},
        ],
        fee_rate=0.5,
    ),
    # TX 8: Ledger Live - round amounts, consistent approach
    Transaction(
        version=2,
        locktime=0,
        inputs=[
            {"sequence": 0xffffffff, "script_type": "P2WPKH", "amount": 100000},
        ],
        outputs=[
            {"script_type": "P2WPKH", "amount": 50000},
            {"script_type": "P2WPKH", "amount": 50000},
        ],
        fee_rate=1.0,
    ),
    # TX 9: Blockstream Green - segwit native, specific patterns
    Transaction(
        version=2,
        locktime=0,
        inputs=[
            {"sequence": 0xffffffff, "script_type": "P2WSH", "amount": 150000},
        ],
        outputs=[
            {"script_type": "P2WSH", "amount": 145000},
        ],
        fee_rate=0.8,
    ),
    # TX 10: Unknown wallet - mixed signals
    Transaction(
        version=2,
        locktime=567890,
        inputs=[
            {"sequence": 0xffffffff, "script_type": "P2PKH", "amount": 60000},
            {"sequence": 0xfffffffd, "script_type": "P2WPKH", "amount": 40000},
        ],
        outputs=[
            {"script_type": "P2PKH", "amount": 50000},
            {"script_type": "P2WPKH", "amount": 48500},
        ],
        fee_rate=2.1,
    ),
]


# Known wallet fingerprints - characteristics of different wallet implementations
WALLET_FINGERPRINTS = {
    "Bitcoin Core": {
        "locktime_pattern": "anti-fee-sniping",
        "sequence_pattern": "all-max-or-rbf",
        "script_types": {"P2WPKH", "P2WSH"},
        "rbf_signaling": True,
        "output_ordering": "default",
    },
    "Electrum": {
        "locktime_pattern": "always-zero",
        "sequence_pattern": "rbf-default",
        "script_types": {"P2PKH", "P2WPKH"},
        "rbf_signaling": True,
        "output_ordering": "default",
    },
    "BlueWallet": {
        "locktime_pattern": "random",
        "sequence_pattern": "all-max",
        "script_types": {"P2WPKH", "P2WSH"},
        "rbf_signaling": False,
        "output_ordering": "default",
    },
    "Wasabi": {
        "locktime_pattern": "always-zero",
        "sequence_pattern": "all-max",
        "script_types": {"P2WPKH"},
        "rbf_signaling": False,
        "output_ordering": "deterministic",
    },
    "Sparrow": {
        "locktime_pattern": "always-zero",
        "sequence_pattern": "all-max",
        "script_types": {"P2WPKH", "P2WSH"},
        "rbf_signaling": False,
        "output_ordering": "bip69-ordered",
    },
    "Samourai": {
        "locktime_pattern": "always-zero",
        "sequence_pattern": "rbf-default",
        "script_types": {"P2WPKH"},
        "rbf_signaling": True,
        "output_ordering": "shuffled",
    },
    "Trezor Suite": {
        "locktime_pattern": "always-zero",
        "sequence_pattern": "all-max",
        "script_types": {"P2WPKH"},
        "rbf_signaling": False,
        "output_ordering": "default",
    },
    "Ledger Live": {
        "locktime_pattern": "always-zero",
        "sequence_pattern": "all-max",
        "script_types": {"P2WPKH"},
        "rbf_signaling": False,
        "output_ordering": "default",
    },
    "Blockstream Green": {
        "locktime_pattern": "always-zero",
        "sequence_pattern": "all-max",
        "script_types": {"P2WSH"},
        "rbf_signaling": False,
        "output_ordering": "default",
    },
}


def identify_locktime_pattern(tx: Transaction) -> str:
    """
    Analyze the locktime field to identify wallet patterns.

    Locktime patterns:
    - "anti-fee-sniping": locktime is recent block height (suggests Bitcoin Core)
    - "always-zero": locktime is 0 (many mobile/exchange wallets)
    - "random": locktime appears arbitrary
    - "unknown": cannot be classified

    Args:
        tx: Transaction to analyze

    Returns:
        String describing the locktime pattern
    """
    # TODO: Implement locktime pattern identification
    # Hint: Check if locktime is 0, a recent block height, or random
    # Recent blocks would be values > 500,000,000 (block heights)
    pass


def identify_sequence_pattern(tx: Transaction) -> str:
    """
    Analyze input sequence numbers to identify wallet behavior.

    Sequence patterns:
    - "all-max": All inputs have sequence 0xffffffff (no RBF, typical hardware wallets)
    - "rbf-signaling": Some inputs have sequence < 0xfffffffe (RBF enabled)
    - "rbf-default": Mix of sequences suggesting RBF awareness
    - "unknown": Cannot be classified

    Args:
        tx: Transaction to analyze

    Returns:
        String describing the sequence pattern
    """
    # TODO: Implement sequence pattern identification
    # Hint: 0xffffffff = 4294967295, 0xfffffffe = 4294967294
    # Check all input sequences to determine pattern
    pass


def identify_script_types(tx: Transaction) -> Set[str]:
    """
    Identify all script types used in transaction inputs and outputs.

    This helps identify wallet capabilities and preferences.
    Common types: P2PKH, P2WPKH, P2WSH, P2SH, P2TR

    Args:
        tx: Transaction to analyze

    Returns:
        Set of script types found in inputs and outputs
    """
    # TODO: Implement script type identification
    # Hint: Collect script types from all inputs and outputs
    pass


def check_output_ordering(tx: Transaction) -> str:
    """
    Analyze output ordering to detect wallet-specific patterns.

    Patterns:
    - "bip69-ordered": Outputs appear sorted (BIP69 lexicographic ordering)
    - "deterministic": Consistent but non-standard ordering
    - "shuffled": Randomized order (privacy-aware)
    - "default": Standard/default ordering

    Args:
        tx: Transaction to analyze

    Returns:
        String describing the output ordering pattern
    """
    # TODO: Implement output ordering detection
    # Hint: Check if outputs are sorted by script, amount, or appear randomized
    pass


def estimate_fee_pattern(tx: Transaction) -> str:
    """
    Identify fee rate patterns that can fingerprint wallets.

    Patterns:
    - "round": Fee rate is a round number (1, 2, 5, 10 sat/byte)
    - "precise": Fee rate is precise/unusual (3.33, 4.47, etc.)
    - "very-low": Extremely low fee rate (<0.5 sat/byte)
    - "unknown": Cannot be classified

    Args:
        tx: Transaction to analyze

    Returns:
        String describing the fee pattern
    """
    # TODO: Implement fee pattern identification
    # Hint: Check if fee_rate is a whole number, very low, or has decimals
    pass


def identify_wallet(tx: Transaction) -> Tuple[str, float]:
    """
    Use all heuristics to identify which wallet likely created this transaction.

    This is the main analysis function that combines all fingerprinting signals.

    Args:
        tx: Transaction to analyze

    Returns:
        Tuple of (wallet_name, confidence_score)
        confidence_score ranges from 0.0 to 1.0
    """
    # TODO: Implement wallet identification
    # Hint: Call the other analysis functions and compare results to WALLET_FINGERPRINTS
    # Score matches and return the best match with confidence
    pass


def construct_privacy_clean_tx(inputs: List[Dict], outputs: List[Dict]) -> Transaction:
    """
    Construct a transaction that minimizes fingerprinting vectors.

    This is the defensive counterpart to wallet fingerprinting - if you're trying
    to avoid identification, follow these principles:
    - Use deterministic script types only
    - Randomize sequence numbers appropriately
    - Set appropriate locktime
    - Use non-standard fee rates
    - Shuffle output ordering

    Args:
        inputs: List of input specifications
        outputs: List of output specifications

    Returns:
        A Transaction object designed to minimize fingerprinting
    """
    # TODO: Implement privacy-conscious transaction construction
    # Hint: Create a transaction that doesn't match known wallet patterns
    pass


def main():
    """
    Main analysis function - runs the complete fingerprinting analysis on all samples.
    """
    print("=" * 70)
    print("BITCOIN WALLET FINGERPRINTING LAB")
    print("=" * 70)
    print()

    for i, tx in enumerate(SAMPLE_TRANSACTIONS, 1):
        print(f"Transaction {i} Analysis:")
        print("-" * 70)

        # Analyze locktime pattern
        locktime_pat = identify_locktime_pattern(tx)
        print(f"  Locktime Pattern: {locktime_pat} (locktime={tx.locktime})")

        # Analyze sequence pattern
        sequence_pat = identify_sequence_pattern(tx)
        print(f"  Sequence Pattern: {sequence_pat}")

        # Identify script types
        script_types = identify_script_types(tx)
        print(f"  Script Types Used: {script_types}")

        # Check output ordering
        output_order = check_output_ordering(tx)
        print(f"  Output Ordering: {output_order}")

        # Estimate fee pattern
        fee_pat = estimate_fee_pattern(tx)
        print(f"  Fee Pattern: {fee_pat} ({tx.fee_rate} sat/byte)")

        # Identify wallet with confidence
        wallet_guess, confidence = identify_wallet(tx)
        print(f"  Wallet Guess: {wallet_guess} (confidence: {confidence:.1%})")
        print()

    print("=" * 70)
    print("PRIVACY-AWARE TRANSACTION CONSTRUCTION")
    print("=" * 70)
    print()

    # Example: Construct a privacy-clean transaction
    clean_tx = construct_privacy_clean_tx(
        inputs=[
            {"sequence": 0xffffffff, "script_type": "P2WPKH", "amount": 100000},
        ],
        outputs=[
            {"script_type": "P2WPKH", "amount": 50000},
            {"script_type": "P2WPKH", "amount": 49500},
        ],
    )

    if clean_tx:
        print("Constructed Privacy-Clean Transaction:")
        print(f"  Locktime: {clean_tx.locktime}")
        print(f"  Input Sequences: {[i['sequence'] for i in clean_tx.inputs]}")
        print(f"  Output Script Types: {[o['script_type'] for o in clean_tx.outputs]}")
        print(f"  Fee Rate: {clean_tx.fee_rate} sat/byte")
        print()

        # Try to fingerprint your own transaction
        wallet_guess, confidence = identify_wallet(clean_tx)
        print(f"  Fingerprinting Result: {wallet_guess} ({confidence:.1%} confidence)")
        print("  (Good privacy-aware construction should have low confidence)")


if __name__ == "__main__":
    main()
