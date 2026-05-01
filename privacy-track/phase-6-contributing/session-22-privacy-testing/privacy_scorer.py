"""
Bitcoin Transaction Privacy Scoring Tool
==========================================

This exercise teaches students to evaluate the privacy characteristics of Bitcoin transactions.
Students build a comprehensive scoring system that identifies privacy leaks and helps users
understand the tradeoffs in their transaction construction.

The scoring system evaluates transactions across 10 different privacy dimensions:
1. Address reuse (major leak)
2. Script type mixing (moderate leak)
3. Round amounts (minor leak)
4. Change detection (major leak)
5. Fee fingerprinting (minor leak)
6. Broadcast timing (minor leak)
7. Locktime analysis (minor leak)
8. Unnecessary inputs (moderate leak)
9. Output ordering (minor leak)
10. Overall scoring (aggregate 0-100)

Learning Objectives:
- Understand the various privacy vectors in Bitcoin transactions
- Implement heuristic-based privacy analysis
- Learn how to score and rank privacy concerns
- Build a user-friendly privacy report system

Final score ranges from 0 (completely private) to 100 (highly identifiable).
"""

from typing import List, Dict, Tuple, Set
from dataclasses import dataclass
from enum import Enum


class PrivacyLevel(Enum):
    """Privacy level categories."""
    EXCELLENT = "Excellent"
    GOOD = "Good"
    FAIR = "Fair"
    POOR = "Poor"
    CRITICAL = "Critical"


@dataclass
class PrivacyFinding:
    """Represents a single privacy issue found in a transaction."""
    category: str
    issue: str
    points_lost: int
    severity: str  # "low", "medium", "high", "critical"
    recommendation: str


@dataclass
class PrivacyReport:
    """Complete privacy analysis report for a transaction."""
    transaction_id: str
    findings: List[PrivacyFinding]
    score: int  # 0-100, lower is more private
    privacy_level: PrivacyLevel
    summary: str
    recommendations: List[str]


# Sample transactions for testing and learning
SAMPLE_TRANSACTIONS = [
    {
        "id": "tx_001",
        "inputs": [
            {"address": "bc1qxyz123", "amount": 50000, "script_type": "P2WPKH"},
        ],
        "outputs": [
            {"address": "bc1qabc123", "amount": 25000, "script_type": "P2WPKH"},
            {"address": "bc1qdef456", "amount": 24500, "script_type": "P2WPKH"},
        ],
        "fee_rate": 2.5,
        "broadcast_time": 1400,  # 14:00 UTC (predictable business hours)
        "locktime": 0,
        "address_history": {"bc1qxyz123": 5, "bc1qabc123": 0, "bc1qdef456": 0},
    },
    {
        "id": "tx_002",
        "inputs": [
            {"address": "1ABC1234", "amount": 100000, "script_type": "P2PKH"},
        ],
        "outputs": [
            {"address": "1DEF5678", "amount": 50000, "script_type": "P2PKH"},
            {"address": "1GHI9012", "amount": 50000, "script_type": "P2PKH"},
        ],
        "fee_rate": 1.0,
        "broadcast_time": 340,  # 03:40 UTC (random time)
        "locktime": 856000,
        "address_history": {"1ABC1234": 12, "1DEF5678": 0, "1GHI9012": 0},
    },
    {
        "id": "tx_003",
        "inputs": [
            {"address": "bc1qaa111", "amount": 75000, "script_type": "P2WPKH"},
            {"address": "bc1qbb222", "amount": 50000, "script_type": "P2WPKH"},
        ],
        "outputs": [
            {"address": "bc1qcc333", "amount": 50000, "script_type": "P2WPKH"},
            {"address": "bc1qdd444", "amount": 75000, "script_type": "P2WPKH"},
        ],
        "fee_rate": 3.333,
        "broadcast_time": 1200,
        "locktime": 0,
        "address_history": {"bc1qcc333": 8, "bc1qdd444": 0},
    },
    {
        "id": "tx_004",
        "inputs": [
            {"address": "bc1qprivate1", "amount": 100000, "script_type": "P2WSH"},
        ],
        "outputs": [
            {"address": "bc1qnew001", "amount": 99567, "script_type": "P2WSH"},
        ],
        "fee_rate": 4.33,
        "broadcast_time": 245,  # 02:45 UTC
        "locktime": 0,
        "address_history": {"bc1qprivate1": 0, "bc1qnew001": 0},
    },
    {
        "id": "tx_005",
        "inputs": [
            {"address": "bc1qmixed1", "amount": 100000, "script_type": "P2WPKH"},
            {"address": "3Mix1111", "amount": 50000, "script_type": "P2SH"},
        ],
        "outputs": [
            {"address": "1Legacy111", "amount": 75000, "script_type": "P2PKH"},
            {"address": "bc1qchange1", "amount": 74500, "script_type": "P2WPKH"},
        ],
        "fee_rate": 2.0,
        "broadcast_time": 1800,
        "locktime": 0,
        "address_history": {
            "bc1qmixed1": 0,
            "3Mix1111": 0,
            "1Legacy111": 0,
            "bc1qchange1": 0,
        },
    },
]


def check_address_reuse(tx: Dict) -> Tuple[int, str]:
    """
    Check if transaction addresses have been used before (address reuse vulnerability).

    Address reuse is a critical privacy leak as it directly links transactions together
    on the public blockchain. Each address should ideally be used only once.

    Points deducted: up to 20 pts (each reused address = 5 pts)

    Args:
        tx: Transaction dict with 'address_history' field

    Returns:
        Tuple of (points_lost, description)
    """
    # TODO: Implement address reuse detection
    # Hint: Check address_history values. Count reused addresses (history > 0)
    # Deduct 5 points per reused address, up to 20 maximum
    pass


def check_script_type_mixing(tx: Dict) -> Tuple[int, str]:
    """
    Check if transaction mixes different script types (P2PKH, P2WPKH, P2SH, P2WSH, P2TR).

    Mixing script types can leak information about wallet capabilities and create
    identifiable patterns. Consistent script type usage is more private.

    Points deducted: 0-15 pts

    Args:
        tx: Transaction dict with inputs/outputs having 'script_type' field

    Returns:
        Tuple of (points_lost, description)
    """
    # TODO: Implement script type mixing detection
    # Hint: Collect all script types from inputs and outputs
    # If more than one type is used, deduct points proportional to mixing
    pass


def check_round_amounts(tx: Dict) -> Tuple[int, str]:
    """
    Check if output amounts are suspiciously round (100000, 50000, 1000000, etc).

    Round amounts (divisible by 10000, 100000, etc.) are easier to identify and
    fingerprint. More random/specific amounts provide better privacy.

    Points deducted: 0-10 pts

    Args:
        tx: Transaction dict with outputs having 'amount' field

    Returns:
        Tuple of (points_lost, description)
    """
    # TODO: Implement round amount detection
    # Hint: Check if output amounts end in zeros (divisible by 10000, 100000, etc.)
    # Deduct points based on how many outputs are suspiciously round
    pass


def check_change_detection(tx: Dict) -> Tuple[int, str]:
    """
    Check if the change output can be easily identified using heuristics.

    Change detection is critical for privacy. If an attacker can identify which
    output is change, they can link the recipient address to the sender.

    Common heuristics:
    - Smallest output is change
    - Largest output is change
    - Only new address is change
    - Specific ordering pattern

    Points deducted: 0-15 pts

    Args:
        tx: Transaction dict with inputs/outputs

    Returns:
        Tuple of (points_lost, description)
    """
    # TODO: Implement change detection analysis
    # Hint: Use multiple heuristics to score how easily change can be identified
    # Consider: size differences, address reuse, ordering
    pass


def check_fee_fingerprint(tx: Dict) -> Tuple[int, str]:
    """
    Check if the fee rate matches known wallet implementations.

    Certain fee rates (1.0, 2.0, 5.0, etc.) are characteristic of specific wallets.
    Custom or unusual fee rates provide some privacy against fingerprinting.

    Points deducted: 0-5 pts

    Args:
        tx: Transaction dict with 'fee_rate' field

    Returns:
        Tuple of (points_lost, description)
    """
    # TODO: Implement fee fingerprinting detection
    # Hint: Check if fee_rate is a round number (1, 2, 5, 10, etc.)
    # These are highly recognizable. Precise rates like 3.33 are better.
    pass


def check_timing(tx: Dict) -> Tuple[int, str]:
    """
    Check if transaction was broadcast at a predictable/suspicious time.

    Broadcasting at 14:00 UTC every time suggests a human or automated schedule.
    Random times at night (02:45) are more typical of automated/privacy-conscious tx.

    Points deducted: 0-5 pts

    Args:
        tx: Transaction dict with 'broadcast_time' field (minutes since midnight UTC)

    Returns:
        Tuple of (points_lost, description)
    """
    # TODO: Implement broadcast timing analysis
    # Hint: Business hours (8:00-18:00 UTC = 480-1080) are more suspicious
    # Random night times are less suspicious
    pass


def check_locktime(tx: Dict) -> Tuple[int, str]:
    """
    Check if locktime reveals wallet implementation details.

    Locktime patterns can fingerprint wallets:
    - Bitcoin Core: Recent block height (anti-fee-sniping)
    - Most others: locktime = 0
    - Some wallets: Random values

    Points deducted: 0-5 pts

    Args:
        tx: Transaction dict with 'locktime' field

    Returns:
        Tuple of (points_lost, description)
    """
    # TODO: Implement locktime analysis
    # Hint: Recent block heights (>500000) suggest Bitcoin Core
    # Zero locktime is neutral. Very old values are suspicious.
    pass


def check_unnecessary_input(tx: Dict) -> Tuple[int, str]:
    """
    Check if transaction uses more inputs than necessary (inefficient UTXO selection).

    Using more inputs than needed can leak information about wallet state and
    increase privacy risks through blockchain analysis.

    Points deducted: 0-10 pts

    Args:
        tx: Transaction dict with inputs/outputs

    Returns:
        Tuple of (points_lost, description)
    """
    # TODO: Implement unnecessary input detection
    # Hint: Compare total input value vs total output value + reasonable fee
    # Excess inputs (where one input alone would suffice) loses points
    pass


def check_output_ordering(tx: Dict) -> Tuple[int, str]:
    """
    Check if output ordering follows wallet-specific patterns.

    Some wallets use:
    - Default ordering (as specified by user)
    - BIP69 lexicographic ordering (deterministic)
    - Random/shuffled ordering

    Recognizable patterns lose privacy points.

    Points deducted: 0-5 pts

    Args:
        tx: Transaction dict with outputs

    Returns:
        Tuple of (points_lost, description)
    """
    # TODO: Implement output ordering analysis
    # Hint: Check if outputs are sorted or follow a recognizable pattern
    pass


def overall_privacy_score(tx: Dict, findings: List[PrivacyFinding]) -> int:
    """
    Calculate the overall privacy score aggregating all findings.

    Score ranges from 0-100:
    - 0-20: Excellent privacy
    - 21-40: Good privacy
    - 41-60: Fair privacy
    - 61-80: Poor privacy
    - 81-100: Critical privacy issues

    Args:
        tx: Transaction being scored
        findings: List of all privacy findings

    Returns:
        Overall score (0-100)
    """
    # TODO: Implement overall scoring
    # Hint: Sum all points_lost from findings, cap at 100
    pass


def generate_report(tx: Dict) -> PrivacyReport:
    """
    Generate a complete privacy report for a transaction.

    Coordinates all individual checks and produces a structured report with
    findings, score, privacy level, and recommendations.

    Args:
        tx: Transaction to analyze

    Returns:
        PrivacyReport object with complete analysis
    """
    # TODO: Implement report generation
    # Hint:
    # 1. Call each check_* function to collect findings
    # 2. Calculate overall score
    # 3. Determine privacy level based on score
    # 4. Generate recommendations based on findings
    # 5. Return populated PrivacyReport
    pass


def print_report(report: PrivacyReport) -> None:
    """
    Pretty-print a privacy report for user review.

    Args:
        report: PrivacyReport to display
    """
    print(f"\n{'=' * 75}")
    print(f"PRIVACY ANALYSIS REPORT: {report.transaction_id}")
    print(f"{'=' * 75}")
    print()

    # Display score and privacy level
    print(f"OVERALL SCORE: {report.score}/100")
    print(f"PRIVACY LEVEL: {report.privacy_level.value}")
    print()

    if report.score <= 20:
        emoji = "✓"
    elif report.score <= 40:
        emoji = "~"
    elif report.score <= 60:
        emoji = "!"
    else:
        emoji = "✗"

    print(f"Summary: {emoji} {report.summary}")
    print()

    # Display findings
    if report.findings:
        print("FINDINGS:")
        print("-" * 75)
        for finding in report.findings:
            severity_indicator = {
                "low": "[*]",
                "medium": "[!]",
                "high": "[!!]",
                "critical": "[!!!]",
            }.get(finding.severity, "[?]")

            print(
                f"{severity_indicator} {finding.category}: {finding.issue} (-{finding.points_lost} pts)"
            )
            print(f"    Recommendation: {finding.recommendation}")
        print()
    else:
        print("No significant privacy issues detected!")
        print()

    # Display recommendations
    if report.recommendations:
        print("RECOMMENDATIONS FOR IMPROVEMENT:")
        print("-" * 75)
        for i, rec in enumerate(report.recommendations, 1):
            print(f"{i}. {rec}")
        print()

    print(f"{'=' * 75}\n")


def main():
    """
    Main function - demonstrates privacy scoring on sample transactions.
    """
    print("\n" + "=" * 75)
    print("BITCOIN TRANSACTION PRIVACY SCORER")
    print("=" * 75)
    print()
    print("This tool evaluates the privacy characteristics of Bitcoin transactions")
    print("by analyzing 10 different privacy vectors and assigning a comprehensive score.")
    print()

    # Analyze each sample transaction
    for tx in SAMPLE_TRANSACTIONS:
        report = generate_report(tx)
        if report:
            print_report(report)
        else:
            print(f"Unable to generate report for {tx['id']}")

    # Summary statistics
    print("=" * 75)
    print("ANALYSIS COMPLETE")
    print("=" * 75)
    print()
    print("Privacy Tips for Better Bitcoin Transactions:")
    print()
    print("1. ADDRESS REUSE")
    print("   - Use a new address for each transaction")
    print("   - Maintain a wallet that generates fresh addresses automatically")
    print()
    print("2. SCRIPT TYPE CONSISTENCY")
    print("   - Stick to one script type (P2WPKH for modern wallets)")
    print("   - Avoid mixing P2PKH, P2SH, and P2WPKH in same transaction")
    print()
    print("3. AMOUNT SELECTION")
    print("   - Use precise amounts instead of round numbers")
    print("   - Avoid round values like 100000, 50000, 1000000 satoshis")
    print()
    print("4. CHANGE OBFUSCATION")
    print("   - Use CoinJoin or mixing services to break change detection")
    print("   - Make change output and payment output similar in size")
    print()
    print("5. TIMING")
    print("   - Broadcast at random times (not business hours)")
    print("   - Use scheduled transactions if possible")
    print()
    print("6. FEE RATES")
    print("   - Use non-standard fee rates (3.33, 4.47, 5.67)")
    print("   - Avoid round numbers (1, 2, 5, 10 sat/byte)")
    print()
    print("7. INPUT SELECTION")
    print("   - Minimize inputs (coin selection efficiency)")
    print("   - Avoid using many small inputs unnecessarily")
    print()
    print("8. OUTPUT ORDERING")
    print("   - Randomize output ordering")
    print("   - Don't follow BIP69 deterministic ordering")
    print()


if __name__ == "__main__":
    main()
