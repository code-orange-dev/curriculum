"""
Bitcoin Privacy Track — Module 1: Chain Analysis Lab
Code Orange Dev School | codeorange.dev

Hands-on chain analysis exercise: parse real Bitcoin transactions,
apply surveillance heuristics, and measure their accuracy.

This lab simulates what chain analysis firms do — then teaches you
how to defeat it.

Prerequisites:
- Python 3.8+
- pip install requests (for fetching from mempool.space API)
- Understanding of Bitcoin transaction structure (inputs, outputs, scripts)

Instructions:
- Complete each function by filling in the code where indicated
- Run: python3 chain_analysis_lab.py
- Bring your results to the weekly session
"""

import json
import hashlib
import struct
from typing import List, Dict, Tuple, Optional


# ============================================================
# Transaction Data Structures (provided)
# ============================================================

class TxInput:
    """Represents a transaction input."""
    def __init__(self, txid: str, vout: int, script_type: str, address: str, value: int):
        self.txid = txid          # Previous transaction hash
        self.vout = vout          # Output index being spent
        self.script_type = script_type  # e.g., "p2wpkh", "p2tr", "p2sh-p2wpkh", "p2pkh"
        self.address = address
        self.value = value        # Value in satoshis

    def __repr__(self):
        return f"Input({self.address[:12]}..., {self.value} sats, {self.script_type})"


class TxOutput:
    """Represents a transaction output."""
    def __init__(self, index: int, script_type: str, address: str, value: int):
        self.index = index
        self.script_type = script_type
        self.address = address
        self.value = value        # Value in satoshis

    def __repr__(self):
        return f"Output({self.address[:12]}..., {self.value} sats, {self.script_type})"


class Transaction:
    """Represents a Bitcoin transaction with metadata."""
    def __init__(self, txid: str, inputs: List[TxInput], outputs: List[TxOutput],
                 version: int = 2, locktime: int = 0, size: int = 0, fee: int = 0):
        self.txid = txid
        self.inputs = inputs
        self.outputs = outputs
        self.version = version
        self.locktime = locktime
        self.size = size
        self.fee = fee

    @property
    def fee_rate(self) -> float:
        """Fee rate in sat/vB."""
        return self.fee / self.size if self.size > 0 else 0

    def __repr__(self):
        return f"TX({self.txid[:12]}..., {len(self.inputs)} in, {len(self.outputs)} out, fee={self.fee})"


# ============================================================
# Sample Transactions (simulated mainnet-like data)
# ============================================================

def load_sample_transactions() -> List[Transaction]:
    """Load sample transactions for analysis.

    These simulate real mainnet patterns. In practice, you'd fetch
    these from mempool.space or your own full node.
    """
    transactions = []

    # TX 1: Simple payment — 1 input, 2 outputs (classic change pattern)
    transactions.append(Transaction(
        txid="a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456",
        inputs=[
            TxInput("prev_tx_01", 0, "p2wpkh", "bc1q sender_addr_001", 500_000),
        ],
        outputs=[
            TxOutput(0, "p2wpkh", "bc1q recipient_addr_01", 100_000),
            TxOutput(1, "p2wpkh", "bc1q change_addr_00001", 399_500),
        ],
        version=2, locktime=840_100, size=141, fee=500
    ))

    # TX 2: Multi-input consolidation — 3 inputs, 1 output
    transactions.append(Transaction(
        txid="b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef1234567a",
        inputs=[
            TxInput("prev_tx_02", 0, "p2wpkh", "bc1q sender_addr_002", 50_000),
            TxInput("prev_tx_03", 1, "p2wpkh", "bc1q sender_addr_003", 30_000),
            TxInput("prev_tx_04", 0, "p2wpkh", "bc1q sender_addr_004", 20_000),
        ],
        outputs=[
            TxOutput(0, "p2wpkh", "bc1q consolidation_001", 99_500),
        ],
        version=2, locktime=840_101, size=250, fee=500
    ))

    # TX 3: Possible Payjoin — 2 inputs (different script types!), 2 outputs
    transactions.append(Transaction(
        txid="c3d4e5f6789012345678901234567890abcdef1234567890abcdef1234567ab0",
        inputs=[
            TxInput("prev_tx_05", 0, "p2wpkh", "bc1q sender_addr_005", 300_000),
            TxInput("prev_tx_06", 2, "p2tr",   "bc1p receiver_addr_01", 200_000),
        ],
        outputs=[
            TxOutput(0, "p2tr",   "bc1p output_addr_00001", 450_000),
            TxOutput(1, "p2wpkh", "bc1q output_addr_00002",  49_500),
        ],
        version=2, locktime=840_102, size=210, fee=500
    ))

    # TX 4: Round amount payment — 1 input, 2 outputs
    transactions.append(Transaction(
        txid="d4e5f6789012345678901234567890abcdef1234567890abcdef1234567ab0c1",
        inputs=[
            TxInput("prev_tx_07", 0, "p2tr", "bc1p sender_addr_006", 1_000_000),
        ],
        outputs=[
            TxOutput(0, "p2tr", "bc1p output_addr_00003", 500_000),   # Round 0.005 BTC
            TxOutput(1, "p2tr", "bc1p output_addr_00004", 499_200),   # Non-round
        ],
        version=2, locktime=840_103, size=154, fee=800
    ))

    # TX 5: Address reuse (same output address as a previous TX)
    transactions.append(Transaction(
        txid="e5f6789012345678901234567890abcdef1234567890abcdef1234567ab0c1d2",
        inputs=[
            TxInput("prev_tx_08", 0, "p2wpkh", "bc1q sender_addr_007", 200_000),
        ],
        outputs=[
            TxOutput(0, "p2wpkh", "bc1q recipient_addr_01", 150_000),  # SAME as TX 1!
            TxOutput(1, "p2wpkh", "bc1q change_addr_00002",  49_300),
        ],
        version=1, locktime=0, size=141, fee=700    # Note: version 1, locktime 0
    ))

    # TX 6: Likely CoinJoin — 3 inputs, 3 equal outputs + 2 change
    transactions.append(Transaction(
        txid="f6789012345678901234567890abcdef1234567890abcdef1234567ab0c1d2e3",
        inputs=[
            TxInput("prev_tx_09", 0, "p2wpkh", "bc1q cj_input_001", 600_000),
            TxInput("prev_tx_10", 0, "p2wpkh", "bc1q cj_input_002", 500_000),
            TxInput("prev_tx_11", 0, "p2wpkh", "bc1q cj_input_003", 400_000),
        ],
        outputs=[
            TxOutput(0, "p2wpkh", "bc1q cj_out_001", 300_000),  # Equal
            TxOutput(1, "p2wpkh", "bc1q cj_out_002", 300_000),  # Equal
            TxOutput(2, "p2wpkh", "bc1q cj_out_003", 300_000),  # Equal
            TxOutput(3, "p2wpkh", "bc1q cj_change_01", 299_000),
            TxOutput(4, "p2wpkh", "bc1q cj_change_02", 199_500),
        ],
        version=2, locktime=840_105, size=500, fee=1500
    ))

    # TX 7: Mixed script types in inputs — wallet migration?
    transactions.append(Transaction(
        txid="789012345678901234567890abcdef1234567890abcdef1234567ab0c1d2e3f4",
        inputs=[
            TxInput("prev_tx_12", 0, "p2pkh",       "1LegacyAddr0001", 100_000),
            TxInput("prev_tx_13", 0, "p2sh-p2wpkh", "3WrappedSegwit01", 100_000),
            TxInput("prev_tx_14", 0, "p2wpkh",      "bc1q native_sw001", 100_000),
        ],
        outputs=[
            TxOutput(0, "p2tr", "bc1p taproot_addr01", 299_000),
        ],
        version=2, locktime=840_106, size=350, fee=1000
    ))

    # TX 8: Unnecessary input heuristic — one input would suffice
    transactions.append(Transaction(
        txid="9012345678901234567890abcdef1234567890abcdef1234567ab0c1d2e3f456",
        inputs=[
            TxInput("prev_tx_15", 0, "p2wpkh", "bc1q sender_addr_010", 800_000),
            TxInput("prev_tx_16", 0, "p2wpkh", "bc1q sender_addr_011", 300_000),
        ],
        outputs=[
            TxOutput(0, "p2wpkh", "bc1q payment_addr_001", 50_000),
            TxOutput(1, "p2wpkh", "bc1q change_addr_003", 1_049_300),
        ],
        version=2, locktime=840_107, size=210, fee=700
    ))

    return transactions


# ============================================================
# Exercise 1: Common-Input-Ownership Heuristic (CIOH)
# ============================================================

def apply_cioh(tx: Transaction) -> Dict[str, List[str]]:
    """Apply the Common-Input-Ownership Heuristic.

    CIOH states: all inputs in a transaction are controlled by the same entity.

    Args:
        tx: a Transaction object

    Returns:
        dict with keys:
            'cluster': list of input addresses assumed to belong to the same entity
            'confidence': 'high', 'medium', or 'low'
            'reasoning': string explaining your confidence level
    """
    # YOUR CODE HERE
    #
    # 1. Extract all input addresses into a list (the "cluster")
    #
    # 2. Determine your confidence level:
    #    - HIGH: all inputs have the same script type (wallet probably combined its own UTXOs)
    #    - MEDIUM: mixed script types but could be wallet migration
    #    - LOW: signs suggest this might be a CoinJoin or Payjoin (CIOH would be wrong)
    #
    # Hints for detecting LOW confidence:
    #    - If there are equal-value outputs (CoinJoin signal)
    #    - If inputs have very different script types AND outputs do too (Payjoin signal)
    #    - If the number of outputs is much larger than 2
    #
    # 3. Write your reasoning string explaining why you chose that confidence level
    #
    # Return: {'cluster': [...], 'confidence': '...', 'reasoning': '...'}

    pass


# ============================================================
# Exercise 2: Change Output Detection
# ============================================================

def detect_change_output(tx: Transaction) -> Dict[str, any]:
    """Detect which output is the change output.

    Apply multiple heuristics and score each output.

    Args:
        tx: a Transaction object

    Returns:
        dict with keys:
            'likely_change_index': int (output index) or None if can't determine
            'heuristics_applied': list of strings describing each heuristic used
            'scores': dict mapping output index to a confidence score (0-100)
            'reasoning': string explaining your analysis
    """
    # YOUR CODE HERE
    #
    # Apply these heuristics (each one adds or subtracts from the score):
    #
    # 1. ROUND AMOUNT HEURISTIC:
    #    - If one output is a round number (divisible by 100,000 sats = 0.001 BTC),
    #      it's likely the PAYMENT, not change.
    #    - The non-round output is likely change.
    #    Score: +30 for the non-round output being change
    #
    # 2. SCRIPT TYPE MATCHING:
    #    - Change usually matches the script type of the inputs
    #    - If inputs are p2wpkh and one output is p2wpkh (matching), that's likely change
    #    Score: +25 for the output matching input script type
    #
    # 3. LARGEST OUTPUT HEURISTIC:
    #    - In a simple payment, the larger output is often change
    #      (because the sender had more than they needed)
    #    Score: +10 for the larger output being change
    #
    # 4. UNNECESSARY INPUT HEURISTIC:
    #    - If removing any single input still covers the smaller output,
    #      the smaller output is likely the payment.
    #    Score: +20 for the smaller output being payment (larger = change)
    #
    # 5. ADDRESS REUSE:
    #    - If an output address appears in the inputs of the same or other txs,
    #      it's likely a payment to a known entity (not change)
    #    - We can't check this in isolation, but flag it if output address
    #      matches any input address in this tx
    #
    # Combine scores and return your analysis

    pass


# ============================================================
# Exercise 3: Wallet Fingerprinting
# ============================================================

def fingerprint_wallet(tx: Transaction) -> Dict[str, str]:
    """Identify likely wallet software from transaction metadata.

    Args:
        tx: a Transaction object

    Returns:
        dict with keys:
            'likely_wallet': string (e.g., "Bitcoin Core", "Electrum", "Mobile wallet", "Unknown")
            'fingerprints': list of strings describing each fingerprint found
            'confidence': 'high', 'medium', or 'low'
    """
    # YOUR CODE HERE
    #
    # Check these fingerprints:
    #
    # 1. VERSION FIELD:
    #    - Version 1: older wallets (some Electrum versions, legacy software)
    #    - Version 2: most modern wallets (Bitcoin Core, BDK-based, etc.)
    #
    # 2. nLockTime:
    #    - 0: Electrum, many mobile wallets, some hardware wallet software
    #    - Current block height (> 500,000 and recent): Bitcoin Core (anti-fee-sniping)
    #    - Non-zero but not block height: unusual, possibly custom software
    #
    # 3. INPUT SCRIPT TYPES:
    #    - p2pkh only: very old wallet or intentionally legacy
    #    - p2sh-p2wpkh: transitional period wallet (2017-2020 era)
    #    - p2wpkh: modern SegWit wallet
    #    - p2tr: cutting-edge Taproot wallet (Bitcoin Core 24+, Sparrow, etc.)
    #    - Mixed types: wallet migration or consolidation
    #
    # 4. FEE RATE:
    #    - Round fee rate (exact multiples of 1 sat/vB): many wallets
    #    - Non-round: Bitcoin Core's estimatesmartfee
    #    - Very high or very low: possible RBF or batch transaction
    #
    # 5. NUMBER OF OUTPUTS:
    #    - Exactly 2: standard wallet payment
    #    - 1: consolidation or sweep
    #    - 3+: batched payment (exchange) or CoinJoin
    #
    # Combine fingerprints and return your analysis

    pass


# ============================================================
# Exercise 4: CoinJoin Detection
# ============================================================

def detect_coinjoin(tx: Transaction) -> Dict[str, any]:
    """Detect if a transaction is likely a CoinJoin.

    Args:
        tx: a Transaction object

    Returns:
        dict with keys:
            'is_likely_coinjoin': bool
            'equal_output_groups': list of lists (groups of equal-value output indices)
            'anonymity_set_size': int (number of equal outputs in largest group)
            'signals': list of strings describing CoinJoin signals found
    """
    # YOUR CODE HERE
    #
    # CoinJoin signals:
    #
    # 1. EQUAL-VALUE OUTPUTS:
    #    - Group outputs by value
    #    - If any group has 2+ outputs with the same value, that's a strong CoinJoin signal
    #    - The size of the largest equal-value group = the anonymity set
    #
    # 2. MANY INPUTS FROM DIFFERENT ADDRESSES:
    #    - CoinJoins typically have 3+ inputs from different addresses
    #    - All addresses being unique (no address reuse) is expected
    #
    # 3. MORE OUTPUTS THAN INPUTS:
    #    - CoinJoins often have more outputs than a normal transaction
    #    - Equal outputs + change outputs for each participant
    #
    # 4. INPUT/OUTPUT RATIO:
    #    - Normal tx: 1-3 inputs, 1-2 outputs
    #    - CoinJoin: 3+ inputs, 3+ outputs (often many more)
    #
    # Return your analysis

    pass


# ============================================================
# Exercise 5: Full Transaction Analysis Report
# ============================================================

def analyze_transaction(tx: Transaction) -> Dict[str, any]:
    """Produce a full chain analysis report for a transaction.

    Combines all heuristics into a comprehensive analysis.

    Args:
        tx: a Transaction object

    Returns:
        dict with keys:
            'txid': transaction hash
            'tx_type': 'simple_payment', 'consolidation', 'coinjoin', 'payjoin',
                       'batch_payment', 'sweep', or 'unknown'
            'cioh_analysis': result from apply_cioh()
            'change_detection': result from detect_change_output()
            'wallet_fingerprint': result from fingerprint_wallet()
            'coinjoin_detection': result from detect_coinjoin()
            'privacy_score': int 0-100 (100 = most private/hardest to analyze)
            'summary': string summarizing the analysis
    """
    # YOUR CODE HERE
    #
    # 1. Run all four analysis functions above
    #
    # 2. Determine the transaction type:
    #    - 1 input, 2 outputs, one round amount → simple_payment
    #    - Multiple inputs, 1 output → consolidation
    #    - Equal outputs detected → coinjoin
    #    - Multiple inputs with mixed script types, 2 outputs → possible payjoin
    #    - 1 input, many outputs → batch_payment
    #    - Multiple inputs, 1 output, all from same script type → sweep
    #
    # 3. Calculate privacy score (0-100):
    #    - Start at 50
    #    - Subtract 10 if change output is obvious
    #    - Subtract 10 if wallet fingerprint confidence is high
    #    - Subtract 15 if CIOH confidence is high
    #    - Add 20 if could be CoinJoin
    #    - Add 15 if could be Payjoin
    #    - Add 10 if all outputs are same script type (harder to distinguish)
    #    - Subtract 10 for address reuse
    #
    # 4. Write a summary paragraph
    #
    # Return the full analysis

    pass


# ============================================================
# Exercise 6: De-anonymization Chain (Advanced)
# ============================================================

def trace_entity(transactions: List[Transaction], start_address: str,
                 max_hops: int = 5) -> List[Dict]:
    """Trace an entity across multiple transactions using heuristics.

    Starting from a known address, follow the chain of transactions
    to build an activity profile.

    Args:
        transactions: list of Transaction objects (the "blockchain")
        start_address: the address to start tracing from
        max_hops: maximum number of transaction hops to follow

    Returns:
        list of dicts, each representing one hop:
            {'txid': str, 'role': 'sender' or 'receiver',
             'value': int, 'linked_addresses': [str]}
    """
    # YOUR CODE HERE
    #
    # Algorithm:
    # 1. Find all transactions where start_address appears (as input or output)
    # 2. For each transaction:
    #    a. If address is in inputs → entity is SENDING
    #       - Apply CIOH to find other addresses owned by same entity
    #       - Identify the change output → that's the entity's next address
    #       - Add the change address to the entity's known addresses
    #    b. If address is in outputs → entity is RECEIVING
    #       - The entity now controls this UTXO
    # 3. Follow the change output to the next transaction
    # 4. Build the trace until max_hops or no more transactions
    #
    # This simulates what chain analysis firms do at scale.
    # The key insight: each hop can reveal new addresses,
    # and CIOH links them all together.

    pass


# ============================================================
# Run all exercises
# ============================================================

def run_analysis():
    print("=" * 70)
    print("Bitcoin Privacy Track — Chain Analysis Lab")
    print("Code Orange Dev School | codeorange.dev")
    print("=" * 70)

    transactions = load_sample_transactions()

    # Exercise 1: CIOH
    print("\n" + "=" * 70)
    print("EXERCISE 1: Common-Input-Ownership Heuristic")
    print("=" * 70)
    for i, tx in enumerate(transactions):
        result = apply_cioh(tx)
        if result is None:
            print(f"\n  TX {i+1}: apply_cioh() not implemented yet")
        else:
            print(f"\n  TX {i+1} ({tx.txid[:16]}...):")
            print(f"    Cluster: {result['cluster']}")
            print(f"    Confidence: {result['confidence']}")
            print(f"    Reasoning: {result['reasoning']}")

    # Exercise 2: Change Detection
    print("\n" + "=" * 70)
    print("EXERCISE 2: Change Output Detection")
    print("=" * 70)
    for i, tx in enumerate(transactions):
        if len(tx.outputs) < 2:
            continue
        result = detect_change_output(tx)
        if result is None:
            print(f"\n  TX {i+1}: detect_change_output() not implemented yet")
        else:
            print(f"\n  TX {i+1} ({tx.txid[:16]}...):")
            print(f"    Likely change: output {result['likely_change_index']}")
            print(f"    Heuristics: {result['heuristics_applied']}")
            print(f"    Scores: {result['scores']}")

    # Exercise 3: Wallet Fingerprinting
    print("\n" + "=" * 70)
    print("EXERCISE 3: Wallet Fingerprinting")
    print("=" * 70)
    for i, tx in enumerate(transactions):
        result = fingerprint_wallet(tx)
        if result is None:
            print(f"\n  TX {i+1}: fingerprint_wallet() not implemented yet")
        else:
            print(f"\n  TX {i+1}:")
            print(f"    Likely wallet: {result['likely_wallet']}")
            print(f"    Fingerprints: {result['fingerprints']}")
            print(f"    Confidence: {result['confidence']}")

    # Exercise 4: CoinJoin Detection
    print("\n" + "=" * 70)
    print("EXERCISE 4: CoinJoin Detection")
    print("=" * 70)
    for i, tx in enumerate(transactions):
        result = detect_coinjoin(tx)
        if result is None:
            print(f"\n  TX {i+1}: detect_coinjoin() not implemented yet")
        else:
            print(f"\n  TX {i+1}:")
            print(f"    CoinJoin? {result['is_likely_coinjoin']}")
            if result['is_likely_coinjoin']:
                print(f"    Anonymity set: {result['anonymity_set_size']}")
            print(f"    Signals: {result['signals']}")

    # Exercise 5: Full Analysis
    print("\n" + "=" * 70)
    print("EXERCISE 5: Full Transaction Analysis")
    print("=" * 70)
    for i, tx in enumerate(transactions):
        result = analyze_transaction(tx)
        if result is None:
            print(f"\n  TX {i+1}: analyze_transaction() not implemented yet")
        else:
            print(f"\n  TX {i+1} ({tx.txid[:16]}...):")
            print(f"    Type: {result['tx_type']}")
            print(f"    Privacy score: {result['privacy_score']}/100")
            print(f"    Summary: {result['summary']}")

    # Exercise 6: Entity Tracing
    print("\n" + "=" * 70)
    print("EXERCISE 6: Entity Tracing")
    print("=" * 70)
    trace = trace_entity(transactions, "bc1q recipient_addr_01", max_hops=3)
    if trace is None:
        print("\n  trace_entity() not implemented yet")
    else:
        print(f"\n  Tracing entity from bc1q recipient_addr_01:")
        for hop in trace:
            print(f"    Hop: {hop['txid'][:16]}... | Role: {hop['role']} | "
                  f"Value: {hop['value']} sats | Linked: {hop['linked_addresses']}")

    print("\n" + "=" * 70)
    print("REFLECTION QUESTIONS (write 2-3 sentences each):")
    print("=" * 70)
    print("""
    1. Which heuristic was most reliable across the sample transactions?
       Which was most often wrong?

    2. TX 3 might be a Payjoin. How does this affect every other heuristic
       you applied to that transaction?

    3. TX 5 reuses an address from TX 1. What does this single data point
       reveal about the entity behind bc1q recipient_addr_01?

    4. TX 6 looks like a CoinJoin. If you were a chain analysis firm,
       how would you try to unmix it? What additional data would you need?

    5. If you could change ONE thing about Bitcoin's transaction format
       to defeat chain analysis, what would it be?
    """)

    print("=" * 70)
    print("Done! Bring your code and reflection answers to the weekly call.")
    print("=" * 70)


if __name__ == "__main__":
    run_analysis()
