"""
Bitcoin Privacy Track — Module 4, Session 1: Coin Selection Simulator
Code Orange Dev School | codeorange.dev

Build and compare coin selection algorithms, measuring their privacy
and fee-efficiency trade-offs.

You will implement 4 coin selection strategies, run them against
realistic UTXO sets, and score each one on privacy and cost.

Prerequisites:
- Understanding of UTXOs and transaction construction
- Python 3.8+

Instructions:
- Complete each function by filling in the code where indicated
- Run: python3 coin_selection_simulator.py
- Bring your results and analysis to the weekly session
"""

import random
import hashlib
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass, field
from enum import Enum


# ============================================================
# Data Structures
# ============================================================

class ScriptType(Enum):
    P2PKH = "p2pkh"
    P2SH_P2WPKH = "p2sh-p2wpkh"
    P2WPKH = "p2wpkh"
    P2TR = "p2tr"


@dataclass
class UTXO:
    """Represents an unspent transaction output."""
    txid: str
    vout: int
    value: int              # satoshis
    script_type: ScriptType
    label: str = ""         # e.g., "exchange", "salary", "coinjoin", "unknown"
    confirmations: int = 6
    address: str = ""

    @property
    def input_weight(self) -> int:
        """Estimated weight units for spending this UTXO."""
        weights = {
            ScriptType.P2PKH: 592,         # ~148 vbytes
            ScriptType.P2SH_P2WPKH: 364,   # ~91 vbytes
            ScriptType.P2WPKH: 272,         # ~68 vbytes
            ScriptType.P2TR: 230,           # ~57.5 vbytes
        }
        return weights.get(self.script_type, 272)

    def __repr__(self):
        btc = self.value / 100_000_000
        return f"UTXO({btc:.8f} BTC, {self.script_type.value}, label={self.label})"


@dataclass
class CoinSelectionResult:
    """Result of a coin selection algorithm."""
    selected: List[UTXO]
    change_amount: int       # 0 if no change needed
    fee: int
    total_input: int
    target_amount: int

    @property
    def num_inputs(self) -> int:
        return len(self.selected)

    @property
    def has_change(self) -> bool:
        return self.change_amount > 0

    @property
    def waste(self) -> int:
        """Waste metric: excess fees + cost of creating/spending change."""
        CHANGE_OUTPUT_COST = 31 * 4  # ~31 vbytes for P2WPKH change output
        CHANGE_SPEND_COST = 68 * 4   # ~68 vbytes to spend the change later
        change_cost = (CHANGE_OUTPUT_COST + CHANGE_SPEND_COST) if self.has_change else 0
        excess = self.total_input - self.target_amount - self.fee
        return change_cost + max(0, excess - self.change_amount)


# ============================================================
# Helper: Fee Calculation
# ============================================================

def estimate_tx_fee(num_inputs: int, num_outputs: int,
                    input_types: List[ScriptType],
                    fee_rate: float = 5.0) -> int:
    """Estimate transaction fee in satoshis.

    Args:
        num_inputs: number of inputs
        num_outputs: number of outputs
        input_types: script types of inputs (for weight calculation)
        fee_rate: fee rate in sat/vB

    Returns:
        estimated fee in satoshis
    """
    # Transaction overhead: 10.5 vbytes (version, marker, flag, locktime)
    overhead_weight = 42

    # Input weights
    input_weight = sum(
        {ScriptType.P2PKH: 592, ScriptType.P2SH_P2WPKH: 364,
         ScriptType.P2WPKH: 272, ScriptType.P2TR: 230}.get(t, 272)
        for t in input_types
    )

    # Output weights (assume P2WPKH outputs: 31 vbytes each)
    output_weight = num_outputs * 124  # 31 * 4

    total_weight = overhead_weight + input_weight + output_weight
    total_vbytes = (total_weight + 3) // 4  # round up

    return int(total_vbytes * fee_rate)


# ============================================================
# Generate Realistic UTXO Sets
# ============================================================

def generate_utxo_set(scenario: str = "typical") -> List[UTXO]:
    """Generate a realistic UTXO set for testing.

    Scenarios:
        'typical': mixed UTXOs from various sources (20 UTXOs)
        'exchange_heavy': mostly large UTXOs from exchange withdrawals
        'dust_heavy': many small UTXOs from mining/faucets
        'privacy_conscious': UTXOs from CoinJoin with clean labels
    """
    random.seed(42)  # Reproducible
    utxos = []

    def make_utxo(value, script_type, label, confs=None):
        txid = hashlib.sha256(f"{value}{label}{len(utxos)}".encode()).hexdigest()
        return UTXO(
            txid=txid, vout=random.randint(0, 3),
            value=value, script_type=script_type, label=label,
            confirmations=confs or random.randint(1, 1000),
            address=f"bc1q_addr_{len(utxos):04d}"
        )

    if scenario == "typical":
        # Mixed wallet: salary deposits, exchange withdrawals, received payments
        utxos = [
            make_utxo(5_000_000, ScriptType.P2WPKH, "salary"),        # 0.05 BTC
            make_utxo(2_500_000, ScriptType.P2WPKH, "salary"),        # 0.025 BTC
            make_utxo(10_000_000, ScriptType.P2WPKH, "exchange"),     # 0.1 BTC
            make_utxo(500_000, ScriptType.P2WPKH, "friend_payment"),  # 0.005 BTC
            make_utxo(1_000_000, ScriptType.P2TR, "donation"),        # 0.01 BTC
            make_utxo(50_000, ScriptType.P2WPKH, "dust"),             # 0.0005 BTC
            make_utxo(3_000_000, ScriptType.P2WPKH, "salary"),        # 0.03 BTC
            make_utxo(750_000, ScriptType.P2SH_P2WPKH, "old_wallet"), # 0.0075 BTC
            make_utxo(20_000_000, ScriptType.P2WPKH, "exchange"),     # 0.2 BTC
            make_utxo(100_000, ScriptType.P2WPKH, "lightning_close"), # 0.001 BTC
            make_utxo(8_000_000, ScriptType.P2TR, "coinjoin"),        # 0.08 BTC
            make_utxo(200_000, ScriptType.P2WPKH, "unknown"),         # 0.002 BTC
            make_utxo(15_000_000, ScriptType.P2WPKH, "salary"),       # 0.15 BTC
            make_utxo(400_000, ScriptType.P2WPKH, "friend_payment"),  # 0.004 BTC
            make_utxo(6_000_000, ScriptType.P2TR, "exchange"),        # 0.06 BTC
            make_utxo(30_000, ScriptType.P2WPKH, "dust"),             # 0.0003 BTC
            make_utxo(1_500_000, ScriptType.P2WPKH, "unknown"),       # 0.015 BTC
            make_utxo(4_000_000, ScriptType.P2WPKH, "salary"),        # 0.04 BTC
            make_utxo(900_000, ScriptType.P2TR, "coinjoin"),          # 0.009 BTC
            make_utxo(7_000_000, ScriptType.P2WPKH, "exchange"),      # 0.07 BTC
        ]

    elif scenario == "exchange_heavy":
        for i in range(8):
            utxos.append(make_utxo(
                random.choice([10_000_000, 20_000_000, 50_000_000, 100_000_000]),
                ScriptType.P2WPKH, "exchange"
            ))

    elif scenario == "dust_heavy":
        for i in range(50):
            utxos.append(make_utxo(
                random.randint(5_000, 100_000),
                ScriptType.P2WPKH, random.choice(["mining", "faucet", "dust"])
            ))

    elif scenario == "privacy_conscious":
        for i in range(15):
            utxos.append(make_utxo(
                random.choice([1_000_000, 2_000_000, 5_000_000, 10_000_000]),
                ScriptType.P2TR, "coinjoin"
            ))

    return utxos


# ============================================================
# Exercise 1: Largest-First Selection
# ============================================================

def select_largest_first(utxos: List[UTXO], target: int,
                         fee_rate: float = 5.0) -> Optional[CoinSelectionResult]:
    """Select UTXOs by picking the largest first.

    Simple and deterministic, but creates obvious change outputs
    and links large UTXOs unnecessarily.

    Args:
        utxos: available UTXOs
        target: amount to send (satoshis)
        fee_rate: fee rate in sat/vB

    Returns:
        CoinSelectionResult or None if insufficient funds
    """
    # YOUR CODE HERE
    #
    # 1. Sort UTXOs by value, largest first
    # 2. Iterate through sorted UTXOs, adding each to the selection
    # 3. After each addition, calculate the fee for the current selection
    #    fee = estimate_tx_fee(len(selected), 2 if change else 1,
    #                          [u.script_type for u in selected], fee_rate)
    # 4. Check if total_input >= target + fee
    #    - If total_input - target - fee < DUST_LIMIT (546 sats): no change needed
    #    - Otherwise: change_amount = total_input - target - fee
    # 5. Return CoinSelectionResult
    #
    # DUST_LIMIT = 546  # satoshis

    pass


# ============================================================
# Exercise 2: Branch and Bound (Exact Match)
# ============================================================

def select_branch_and_bound(utxos: List[UTXO], target: int,
                            fee_rate: float = 5.0,
                            max_tries: int = 100_000) -> Optional[CoinSelectionResult]:
    """Select UTXOs to exactly match the target (no change output).

    This is Bitcoin Core's preferred algorithm. Finding an exact match
    eliminates the change output entirely — great for privacy.

    Args:
        utxos: available UTXOs
        target: amount to send (satoshis)
        fee_rate: fee rate in sat/vB
        max_tries: maximum iterations before giving up

    Returns:
        CoinSelectionResult with change_amount=0, or None if no exact match found
    """
    # YOUR CODE HERE
    #
    # Branch and bound algorithm:
    #
    # The "effective value" of a UTXO = value - cost_to_spend_it
    # cost_to_spend = (utxo.input_weight / 4) * fee_rate
    #
    # The "effective target" = target + overhead_fee
    # overhead_fee = estimate_tx_fee(0, 1, [], fee_rate)  # just the non-input overhead
    #
    # TOLERANCE = 50 * fee_rate  # Allow overpaying up to 50 vbytes worth of fees
    #
    # Algorithm (depth-first search with backtracking):
    # 1. Sort UTXOs by effective value, descending
    # 2. Maintain a selection set and current_value = 0
    # 3. For each depth (UTXO index):
    #    a. TRY INCLUDING this UTXO:
    #       current_value += effective_value[i]
    #       If current_value >= effective_target AND
    #          current_value <= effective_target + TOLERANCE:
    #         → FOUND exact match! Return it.
    #       If current_value > effective_target + TOLERANCE:
    #         → Backtrack (undo inclusion, skip to exclusion branch)
    #    b. TRY EXCLUDING this UTXO:
    #       Check if remaining UTXOs can still reach effective_target
    #       If not → backtrack further
    # 4. If max_tries exceeded or no match found → return None
    #
    # This is a simplified version. The full Bitcoin Core implementation
    # is in src/wallet/coinselection.cpp (SelectCoinsBnB).

    pass


# ============================================================
# Exercise 3: Privacy-Optimized Selection
# ============================================================

def select_privacy_optimized(utxos: List[UTXO], target: int,
                             fee_rate: float = 5.0) -> Optional[CoinSelectionResult]:
    """Select UTXOs with privacy as the primary objective.

    Privacy rules:
    1. NEVER mix UTXOs from different labels/sources
       (e.g., don't combine "exchange" + "coinjoin" UTXOs)
    2. Prefer UTXOs from CoinJoin outputs (already mixed)
    3. Prefer same script type for all inputs (avoid fingerprinting)
    4. Try to avoid change (use branch-and-bound within label groups)
    5. If change is needed, prefer smaller change amounts

    Args:
        utxos: available UTXOs
        target: amount to send (satoshis)
        fee_rate: fee rate in sat/vB

    Returns:
        CoinSelectionResult or None if insufficient funds
    """
    # YOUR CODE HERE
    #
    # Strategy:
    # 1. Group UTXOs by label
    # 2. For each label group (prioritize "coinjoin" > "unknown" > others):
    #    a. Try branch_and_bound within this group (best: no change!)
    #    b. If no exact match, try largest_first within this group
    #    c. If this group alone can cover target + fee, use it
    # 3. If no single group suffices:
    #    a. Fall back to combining groups (privacy degradation!)
    #    b. Prefer combining groups with the same script type
    #    c. Log a WARNING: "Privacy degradation: mixing UTXO sources"
    # 4. Return the result with the best privacy properties
    #
    # Scoring (for choosing between valid selections):
    #   - No change: +50
    #   - Single label group: +40
    #   - CoinJoin UTXOs: +30
    #   - Same script type: +20
    #   - Fewer inputs: +10 per input avoided (fewer CIOH links)

    pass


# ============================================================
# Exercise 4: Random Selection (Knapsack-style)
# ============================================================

def select_random(utxos: List[UTXO], target: int,
                  fee_rate: float = 5.0,
                  rounds: int = 1000) -> Optional[CoinSelectionResult]:
    """Select UTXOs randomly, picking the best result from many attempts.

    Adds entropy to defeat deterministic analysis, while still
    trying to minimize waste.

    Args:
        utxos: available UTXOs
        target: amount to send (satoshis)
        fee_rate: fee rate in sat/vB
        rounds: number of random attempts

    Returns:
        CoinSelectionResult with lowest waste score
    """
    # YOUR CODE HERE
    #
    # For each round:
    # 1. Shuffle the UTXOs randomly
    # 2. Walk through shuffled list, accumulating until target + fee is met
    # 3. Calculate the CoinSelectionResult (including waste)
    # 4. Keep track of the result with the lowest waste
    #
    # After all rounds, return the best result
    #
    # BONUS: Instead of pure random, use a weighted random:
    #   - UTXOs closer to the target get higher weight
    #   - This makes exact matches more likely

    pass


# ============================================================
# Exercise 5: Privacy Scoring
# ============================================================

def score_privacy(result: CoinSelectionResult, all_utxos: List[UTXO]) -> Dict[str, any]:
    """Score the privacy properties of a coin selection result.

    Args:
        result: the coin selection result to score
        all_utxos: the full UTXO set (for context)

    Returns:
        dict with:
            'total_score': int 0-100
            'breakdown': dict of individual scores
            'warnings': list of privacy warnings
            'recommendations': list of suggestions
    """
    # YOUR CODE HERE
    #
    # Scoring criteria:
    #
    # 1. CHANGE OUTPUT (0-25 points):
    #    - No change: 25 points
    #    - Change < 1% of target: 20 points
    #    - Change < 10% of target: 10 points
    #    - Change > 50% of target: 0 points (obvious pattern)
    #
    # 2. INPUT MIXING (0-25 points):
    #    - All UTXOs from same label: 25 points
    #    - 2 labels mixed: 10 points
    #    - 3+ labels mixed: 0 points
    #    WARNING: "Mixing UTXOs from {labels} links these identities"
    #
    # 3. SCRIPT TYPE UNIFORMITY (0-20 points):
    #    - All inputs same script type: 20 points
    #    - 2 script types: 10 points
    #    - 3+ script types: 0 points (obvious wallet migration)
    #
    # 4. NUMBER OF INPUTS (0-15 points):
    #    - 1 input: 15 points (minimal CIOH exposure)
    #    - 2 inputs: 10 points
    #    - 3+ inputs: 5 points
    #    - 5+ inputs: 0 points
    #
    # 5. CHANGE AMOUNT PATTERN (0-15 points):
    #    - No change: 15 points
    #    - Non-round change: 10 points
    #    - Round change amount: 5 points (suspicious pattern)
    #    - Change matches a common denomination: 0 points
    #
    # Generate warnings and recommendations based on the analysis

    pass


# ============================================================
# Exercise 6: Comparative Analysis
# ============================================================

def run_comparison(utxos: List[UTXO], targets: List[int], fee_rate: float = 5.0):
    """Run all coin selection algorithms against multiple targets and compare.

    Prints a comparison table showing fee cost, privacy score,
    number of inputs, and whether change was created.
    """
    algorithms = {
        "Largest First": select_largest_first,
        "Branch & Bound": select_branch_and_bound,
        "Privacy Optimized": select_privacy_optimized,
        "Random (best of 1000)": select_random,
    }

    print(f"\n{'='*90}")
    print(f"COIN SELECTION COMPARISON — {len(utxos)} UTXOs, fee rate {fee_rate} sat/vB")
    print(f"{'='*90}")

    total_balance = sum(u.value for u in utxos)
    print(f"Total balance: {total_balance / 100_000_000:.8f} BTC")
    print(f"UTXO labels: {', '.join(set(u.label for u in utxos))}")
    print(f"Script types: {', '.join(set(u.script_type.value for u in utxos))}")

    for target in targets:
        print(f"\n{'─'*90}")
        print(f"TARGET: {target / 100_000_000:.8f} BTC ({target:,} sats)")
        print(f"{'─'*90}")
        print(f"{'Algorithm':<25} {'Inputs':>6} {'Fee':>8} {'Change':>12} {'Waste':>8} {'Privacy':>8}")
        print(f"{'─'*25} {'─'*6} {'─'*8} {'─'*12} {'─'*8} {'─'*8}")

        for name, algo in algorithms.items():
            result = algo(utxos, target, fee_rate)
            if result is None:
                print(f"{name:<25} {'FAILED':>6}")
                continue

            privacy = score_privacy(result, utxos)
            privacy_score = privacy['total_score'] if privacy else "N/A"

            change_str = f"{result.change_amount:,}" if result.has_change else "none"
            print(f"{name:<25} {result.num_inputs:>6} {result.fee:>7}s "
                  f"{change_str:>12} {result.waste:>7}s {privacy_score:>7}")

            if privacy and privacy.get('warnings'):
                for w in privacy['warnings']:
                    print(f"  ⚠ {w}")


# ============================================================
# Run everything
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("Bitcoin Privacy Track — Coin Selection Simulator")
    print("Code Orange Dev School | codeorange.dev")
    print("=" * 70)

    # Test with different UTXO sets
    scenarios = ["typical", "exchange_heavy", "dust_heavy", "privacy_conscious"]

    # Common payment amounts to test
    targets = [
        100_000,       # 0.001 BTC — small payment
        1_000_000,     # 0.01 BTC  — medium payment
        5_000_000,     # 0.05 BTC  — larger payment
        25_000_000,    # 0.25 BTC  — significant payment
    ]

    for scenario in scenarios:
        print(f"\n\n{'#'*70}")
        print(f"SCENARIO: {scenario.upper()}")
        print(f"{'#'*70}")

        utxos = generate_utxo_set(scenario)
        run_comparison(utxos, targets)

    print("\n" + "=" * 70)
    print("REFLECTION QUESTIONS:")
    print("=" * 70)
    print("""
    1. Which algorithm produced the best privacy scores? Did it also
       have the lowest fees? Explain the trade-off you observed.

    2. In the 'typical' scenario, the privacy-optimized algorithm
       refuses to mix labels. What practical problem does this create
       for users with many small UTXOs from different sources?

    3. Branch-and-bound finds no-change solutions but doesn't always
       succeed. In which scenarios did it fail most? Why?

    4. If you were designing a wallet for activists in a hostile regime,
       which coin selection algorithm would you use by default? Why?

    5. BONUS: Implement a 5th algorithm that combines branch-and-bound
       with privacy optimization. Can you beat both on their own metrics?
    """)

    print("=" * 70)
    print("Done! Bring your results to the weekly session.")
    print("=" * 70)
