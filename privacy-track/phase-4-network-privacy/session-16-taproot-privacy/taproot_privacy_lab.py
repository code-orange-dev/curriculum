"""
Taproot Privacy Analysis Lab: Evaluating Privacy Improvements of SegWit v1
===========================================================================

In this exercise, you will learn:
1. How Taproot (BIP 341) improves Bitcoin privacy on-chain
2. Why uniform output sizes enhance privacy
3. How key-path spending is more efficient than script-path
4. Why distinguishability of transaction types reduces anonymity
5. How CoinJoin becomes more efficient with CISA (Cross-Input Signature Aggregation)
6. How to measure Taproot adoption and its privacy implications

Taproot Context:
- Bitcoin address format: P2PK, P2PKH, P2SH, P2WPKH (SegWit v0), P2WSH, P2TR (SegWit v1)
- SegWit v0 (2016): Separated signatures from transaction data (reduced on-chain footprint)
- Taproot/SegWit v1 (2021): Unified all types into uniform output format

Privacy Benefits of Taproot:
1. UNIFORM OUTPUTS: All Taproot outputs (P2TR) are 32 bytes
   - Old: P2PKH=25 bytes, P2SH=20 bytes, P2WPKH=22 bytes - easily distinguished
   - New: P2TR=32 bytes - identical for key-path and script-path spends
   - Benefit: Observer cannot distinguish spend type

2. EFFICIENT KEY-PATH SPENDING: Default Taproot spend is key-path aggregate
   - Signature: 64 bytes (vs 71-73 bytes for ECDSA)
   - Witness witness data smaller
   - Benefit: Honest users pay less for privacy (key-path is default/cheapest)

3. SCRIPT-PATH FLEXIBILITY: Taproot scripts are more flexible
   - Supports multiple keys with lower witness overhead
   - Benefit: Multi-sig becomes cheaper, encouraging its use for privacy

4. CISA POTENTIAL: Cross-Input Signature Aggregation (not yet deployed)
   - CoinJoin with n participants could have 1 signature instead of n
   - Massive fee savings and scalability improvement
   - Would make privacy much more accessible

Why This Matters for Privacy:
- Transaction surveillance is a real threat to Bitcoin privacy
- Heuristics can link addresses: "change address", "same-input-outputs", etc.
- If spend types are distinguishable, attacker knows your transaction structure
- Uniform outputs limit attacker's ability to identify transaction types
- Larger Taproot adoption increases anonymity set (you blend in better)

This exercise simulates transaction data. Real analysis uses blockchain APIs
like blockchain.info, mempool.space, or Glassnode to track actual transactions.
"""

from typing import List, Dict, Tuple
from collections import Counter
import json


# ============================================================================
# Sample Transaction Data
# ============================================================================

# Each transaction has:
# - type: Address format (P2PKH, P2SH-P2WPKH, P2WPKH, P2WSH, P2TR key-path, P2TR script-path)
# - witness_size: Bytes of witness data (includes signatures)
# - scriptPubKey_size: Bytes of output script (what goes on chain)
# - on_chain_distinguishable: Can observer identify the type from on-chain data?

SAMPLE_TX_TYPES = [
    {
        'type': 'P2PKH',
        'witness_size': 0,  # P2PKH has no witness (pre-SegWit)
        'scriptPubKey_size': 25,  # OP_DUP OP_HASH160 <pubkeyhash> OP_EQUALVERIFY OP_CHECKSIG
        'on_chain_distinguishable': True,
        'typical_input_size': 148,  # bytes
        'description': 'Pay to Public Key Hash (Legacy, pre-2015)'
    },
    {
        'type': 'P2SH-P2WPKH',
        'witness_size': 108,  # 1 signature + 1 pubkey
        'scriptPubKey_size': 20,  # OP_HASH160 <hash160> OP_EQUAL
        'on_chain_distinguishable': True,
        'typical_input_size': 23 + 108,
        'description': 'P2SH-wrapped SegWit v0 (Segwit compatibility mode, 2016-2017)'
    },
    {
        'type': 'P2WPKH',
        'witness_size': 108,  # 1 signature + 1 pubkey
        'scriptPubKey_size': 22,  # OP_0 <pubkeyhash>
        'on_chain_distinguishable': True,
        'typical_input_size': 22 + 108,
        'description': 'Native SegWit v0: Pay to Witness Public Key Hash (2016-present)'
    },
    {
        'type': 'P2WSH',
        'witness_size': 180,  # Multi-sig: multiple sigs + script
        'scriptPubKey_size': 34,  # OP_0 <script_hash>
        'on_chain_distinguishable': True,
        'typical_input_size': 34 + 180,
        'description': 'SegWit v0 Multi-sig: Pay to Witness Script Hash (2-of-3)'
    },
    {
        'type': 'P2TR-key',
        'witness_size': 65,  # Single 64-byte signature + 1-byte flag
        'scriptPubKey_size': 34,  # OP_1 <32-byte key>
        'on_chain_distinguishable': False,
        'typical_input_size': 34 + 65,
        'description': 'Taproot key-path spend (most common case, 2021-present)'
    },
    {
        'type': 'P2TR-script',
        'witness_size': 130,  # Signature + script + merkle proof
        'scriptPubKey_size': 34,  # OP_1 <32-byte key> - IDENTICAL to key-path!
        'on_chain_distinguishable': False,
        'typical_input_size': 34 + 130,
        'description': 'Taproot script-path spend (fallback if key path unavailable)'
    }
]


# Block data for adoption tracking
SAMPLE_BLOCKS = [
    {
        'height': 700000,
        'date': '2021-11-13',
        'p2pkh_count': 150,
        'p2sh_count': 100,
        'p2wpkh_count': 250,
        'p2wsh_count': 30,
        'p2tr_count': 5,
        'total_outputs': 535
    },
    {
        'height': 702000,
        'date': '2021-12-05',
        'p2pkh_count': 140,
        'p2sh_count': 95,
        'p2wpkh_count': 280,
        'p2wsh_count': 35,
        'p2tr_count': 50,
        'total_outputs': 600
    },
    {
        'height': 704000,
        'date': '2021-12-27',
        'p2pkh_count': 130,
        'p2sh_count': 90,
        'p2wpkh_count': 310,
        'p2wsh_count': 40,
        'p2tr_count': 130,
        'total_outputs': 700
    },
    {
        'height': 750000,
        'date': '2023-04-04',
        'p2pkh_count': 80,
        'p2sh_count': 70,
        'p2wpkh_count': 400,
        'p2wsh_count': 80,
        'p2tr_count': 470,
        'total_outputs': 1100
    },
    {
        'height': 800000,
        'date': '2024-05-15',
        'p2pkh_count': 50,
        'p2sh_count': 40,
        'p2wpkh_count': 380,
        'p2wsh_count': 100,
        'p2tr_count': 930,
        'total_outputs': 1500
    }
]


# ============================================================================
# Exercise Functions - Implement These!
# ============================================================================

def compare_output_sizes(tx_types: List[Dict]) -> Dict[str, int]:
    """
    Compare scriptPubKey sizes across different transaction types.

    This reveals the privacy issue: Legacy formats have different output sizes.
    An observer can identify address types just by looking at output length!

    Args:
        tx_types: List of transaction type dicts

    Returns:
        Dict mapping tx_type name -> scriptPubKey_size

    Privacy Insight:
    - P2PKH outputs are 25 bytes: instantly recognizable
    - P2SH outputs are 20 bytes: known script hash size
    - Segwit v0 outputs are 22 bytes: identifiable
    - Taproot outputs are 34 bytes: UNIFORM regardless of spend type
      (key-path spending looks identical to script-path!)

    This is crucial: with Taproot, observer cannot distinguish common cases.
    """
    # TODO: Implement this function
    # Hint: Extract scriptPubKey_size from each tx_type, return as dict
    pass


def compare_spend_sizes(tx_types: List[Dict]) -> Dict[str, int]:
    """
    Compare witness (input) sizes across transaction types.

    Witness data is what's needed to spend coins (signatures). Smaller witnesses
    mean cheaper transactions. This incentivizes privacy-preserving spends.

    Args:
        tx_types: List of transaction type dicts

    Returns:
        Dict mapping tx_type name -> total_input_size

    Privacy Insight:
    - P2PKH inputs are ~148 bytes (no witness separation)
    - Segwit witnesses are ~108 bytes for P2WPKH (30% smaller)
    - Taproot key-path is only 65 bytes (50% smaller than P2WPKH!)
      - This is because signatures are smaller and more efficient
      - Honest users are incentivized to use the private option

    Economic incentive for privacy: Taproot key-path is the CHEAPEST option,
    so privacy-conscious users naturally choose it for cost reasons alone.
    This creates a large anonymity set of "normal" transactions.
    """
    # TODO: Implement this function
    # Hint: Extract typical_input_size from each tx_type, return as dict
    pass


def analyze_privacy_improvement(tx_types: List[Dict]) -> Dict[str, List[str]]:
    """
    Identify which transaction types are distinguishable on-chain.

    A transaction type is distinguishable if an observer can identify it
    just from public blockchain data (output size, witness structure, etc).

    Distinguishability is bad for privacy: attacker knows your transaction type,
    limiting anonymity and enabling targeted surveillance.

    Args:
        tx_types: List of transaction type dicts

    Returns:
        Dict with keys:
        - 'distinguishable': list of types that can be identified on-chain
        - 'indistinguishable': list of types that look identical on-chain
        - 'taproot_advantage': explanation of why Taproot improves privacy

    Privacy Implication:
    - With old types: attacker knows instantly "this is P2PKH" or "this is P2WPKH"
      They know your spending pattern, address reuse habits, change patterns
    - With Taproot: attacker cannot distinguish key-path from script-path
      (or from other advanced spending conditions that might exist)
    """
    # TODO: Implement this function
    # Hint: Check on_chain_distinguishable for each type
    pass


def calculate_anonymity_set(tx_type: str, network_usage: Dict[str, float]) -> float:
    """
    Calculate the anonymity set for a given transaction type.

    The anonymity set is: "How many other users have the same transaction type?"
    Larger anonymity set = better privacy (harder to single you out).

    If 99% of network uses P2WPKH and you use P2WSH, you stand out.
    If 50% uses P2TR and you use P2TR, you blend in with millions.

    Args:
        tx_type: The type to calculate anonymity for (e.g., 'P2TR-key')
        network_usage: Dict mapping tx_type -> percentage (0-100) of network

    Returns:
        float representing the fraction of the network using this type

    Privacy Insight:
    - Anonymity set = % of network using the same type
    - P2TR adoption growing rapidly (as of 2024, ~60%+ of new outputs)
    - Users choosing P2TR benefit from large anonymity set
    - Users still using P2PKH are alone in a pool of 0.5%

    Example:
    If network_usage = {'P2TR-key': 60, 'P2WPKH': 30, 'P2WSH': 5, ...}
    calculate_anonymity_set('P2TR-key', network_usage) -> 60.0
    """
    # TODO: Implement this function
    # Hint: Return the percentage value from network_usage dict for given tx_type
    pass


def simulate_cisa_savings(num_inputs: int) -> Dict[str, float]:
    """
    Calculate fee savings from Cross-Input Signature Aggregation (CISA).

    CISA is a Taproot feature (not yet deployed) that allows multiple signatures
    to be aggregated into one. In a CoinJoin with 10 people, you could have
    1 signature instead of 10 - massive savings!

    Signature size assumptions:
    - Taproot: 65 bytes per signature
    - With CISA: 1 signature covers all inputs (only 65 bytes total!)

    Args:
        num_inputs: Number of CoinJoin participants (inputs)

    Returns:
        Dict with:
        - 'without_cisa_bytes': witness bytes needed without CISA
        - 'with_cisa_bytes': witness bytes with CISA
        - 'bytes_saved': absolute savings
        - 'percent_saved': % reduction in transaction size
        - 'fee_savings_at_50sat_per_byte': cost savings in sats

    Fee calculation (simplified):
    - Transaction cost = size_in_bytes × fee_rate (sats/byte)
    - Typical high-priority fee: ~50 sats/byte
    - If CISA saves 500 bytes, that's 500 × 50 = 25,000 sats saved!

    Network Effect:
    - CoinJoin becomes radically cheaper with CISA
    - More people join for privacy (CoinJoins become larger)
    - Privacy becomes accessible to everyone (not just wealthy users)
    - Network privacy improves as more people participate
    """
    # TODO: Implement this function
    # Hint: Calculate based on num_inputs * 65 bytes per signature
    pass


def taproot_adoption_analysis(blocks: List[Dict]) -> Dict:
    """
    Analyze Taproot adoption trends over time.

    This function tracks how many outputs in each block are P2TR vs other types.
    High adoption = large anonymity set = better privacy for P2TR users.

    Args:
        blocks: List of block data dicts with output counts by type

    Returns:
        Dict with:
        - 'first_block': block height of first sample
        - 'last_block': block height of last sample
        - 'initial_adoption_percent': P2TR % in first block
        - 'final_adoption_percent': P2TR % in last block
        - 'growth_rate_percent_per_block': average growth per 2000 blocks
        - 'adoption_by_block': dict mapping block height -> adoption %
        - 'anonymity_trajectory': string describing trend

    Privacy Timeline:
    - Early (2021-2022): Low P2TR adoption (<5%), small anonymity set
    - Growth (2022-2023): Rapid adoption as wallets add support (~30%)
    - Mainstream (2023-2024): Majority of new outputs are P2TR (~60%+)
    - Future: P2TR dominance, excellent privacy from size alone

    Note: High adoption doesn't mean perfect privacy, but it's a key factor
    in making privacy the default for economically rational users.
    """
    # TODO: Implement this function
    # Hint: Calculate P2TR percentage for each block, track growth trend
    pass


# ============================================================================
# Main Analysis Block
# ============================================================================

def main():
    """
    Run comprehensive Taproot privacy analysis.

    This demonstrates all concepts by comparing transaction types,
    calculating anonymity, and projecting CISA benefits.
    """

    print("=" * 80)
    print("TAPROOT PRIVACY ANALYSIS LAB")
    print("=" * 80)
    print()

    # ========================================================================
    # Part 1: Output Size Comparison
    # ========================================================================
    print("PART 1: OUTPUT SIZE COMPARISON")
    print("-" * 80)
    print("Privacy Issue: If outputs have different sizes, observer identifies type")
    print()

    output_sizes = compare_output_sizes(SAMPLE_TX_TYPES)
    if output_sizes:
        for tx_type, size in sorted(output_sizes.items(), key=lambda x: x[1]):
            print(f"  {tx_type:15s}: {size:2d} bytes", end="")
            if size == 34:
                print(" <- Taproot (uniform)")
            else:
                print(f" <- Legacy (recognizable: {size} byte fingerprint)")
        print()

    # ========================================================================
    # Part 2: Input/Witness Size Comparison
    # ========================================================================
    print("PART 2: INPUT/WITNESS SIZE COMPARISON")
    print("-" * 80)
    print("Privacy Insight: Smaller witnesses incentivize privacy-preserving spends")
    print("Economic incentive: Key-path is cheapest, so privacy becomes default")
    print()

    spend_sizes = compare_spend_sizes(SAMPLE_TX_TYPES)
    if spend_sizes:
        # Sort by size to show efficiency improvement
        sorted_sizes = sorted(spend_sizes.items(), key=lambda x: x[1])
        min_size = sorted_sizes[0][1]
        for tx_type, size in sorted_sizes:
            percent_overhead = ((size - min_size) / min_size) * 100
            print(f"  {tx_type:15s}: {size:3d} bytes", end="")
            if percent_overhead == 0:
                print(" <- CHEAPEST (key-path Taproot)")
            else:
                print(f" ({percent_overhead:+5.0f}% overhead)")
        print()

    # ========================================================================
    # Part 3: Distinguishability Analysis
    # ========================================================================
    print("PART 3: ON-CHAIN DISTINGUISHABILITY ANALYSIS")
    print("-" * 80)
    print("Privacy Risk: If type is identifiable, attacker knows your structure")
    print()

    privacy_analysis = analyze_privacy_improvement(SAMPLE_TX_TYPES)
    if privacy_analysis:
        print("Distinguishable types (attacker knows your type instantly):")
        if privacy_analysis.get('distinguishable'):
            for tx_type in privacy_analysis['distinguishable']:
                print(f"  - {tx_type}")
        print()
        print("Indistinguishable types (attacker cannot tell them apart):")
        if privacy_analysis.get('indistinguishable'):
            for tx_type in privacy_analysis['indistinguishable']:
                print(f"  - {tx_type}")
        print()
        if privacy_analysis.get('taproot_advantage'):
            print(f"Taproot Advantage: {privacy_analysis['taproot_advantage']}")
        print()

    # ========================================================================
    # Part 4: Anonymity Set Analysis
    # ========================================================================
    print("PART 4: ANONYMITY SET ANALYSIS")
    print("-" * 80)
    print("Larger anonymity set = harder for attacker to target you")
    print()

    # Simulate network usage (actual network data from mid-2024)
    network_usage = {
        'P2PKH': 3,
        'P2SH': 2,
        'P2WPKH': 25,
        'P2WSH': 5,
        'P2TR-key': 60,
        'P2TR-script': 5
    }

    print("Network adoption (% of new outputs):")
    for tx_type, percent in sorted(network_usage.items(), key=lambda x: -x[1]):
        anonymity = calculate_anonymity_set(tx_type, network_usage)
        if anonymity:
            print(f"  {tx_type:15s}: {anonymity:5.1f}% of network", end="")
            if anonymity >= 50:
                print(" <- Large anonymity set (excellent privacy)")
            elif anonymity >= 20:
                print(" <- Medium anonymity set (good privacy)")
            else:
                print(" <- Small anonymity set (poor privacy)")
    print()

    # ========================================================================
    # Part 5: CISA Savings Simulation
    # ========================================================================
    print("PART 5: CROSS-INPUT SIGNATURE AGGREGATION (CISA) SAVINGS")
    print("-" * 80)
    print("CISA: Single signature covers all inputs (potential future upgrade)")
    print("Use case: CoinJoin transactions with many participants")
    print()

    coinjoin_sizes = [3, 5, 10, 50, 100]
    for size in coinjoin_sizes:
        savings = simulate_cisa_savings(size)
        if savings:
            print(f"CoinJoin with {size:3d} participants:")
            print(f"  Without CISA: {savings['without_cisa_bytes']:5.0f} bytes witness")
            print(f"  With CISA:    {savings['with_cisa_bytes']:5.0f} bytes witness")
            print(f"  Savings:      {savings['bytes_saved']:5.0f} bytes ({savings['percent_saved']:5.1f}%)")
            print(f"  Fee savings:  {savings['fee_savings_at_50sat_per_byte']:7.0f} sats at 50sat/byte")
            print()

    # ========================================================================
    # Part 6: Adoption Trajectory
    # ========================================================================
    print("PART 6: TAPROOT ADOPTION TRAJECTORY")
    print("-" * 80)
    print("Privacy improves as more users adopt Taproot")
    print()

    adoption_data = taproot_adoption_analysis(SAMPLE_BLOCKS)
    if adoption_data:
        print(f"Analysis period: Block {adoption_data['first_block']} to {adoption_data['last_block']}")
        print(f"Initial adoption:  {adoption_data['initial_adoption_percent']:.1f}% P2TR")
        print(f"Final adoption:    {adoption_data['final_adoption_percent']:.1f}% P2TR")
        print(f"Growth rate:       {adoption_data['growth_rate_percent_per_block']:.3f}% per 2000 blocks")
        print(f"Trajectory:        {adoption_data['anonymity_trajectory']}")
        print()

        # Adoption timeline
        if adoption_data.get('adoption_by_block'):
            print("Adoption by block:")
            for block_height in sorted(adoption_data['adoption_by_block'].keys()):
                adoption_pct = adoption_data['adoption_by_block'][block_height]
                bar_length = int(adoption_pct / 5)
                bar = "█" * bar_length
                print(f"  Block {block_height}: {adoption_pct:6.1f}% {bar}")
            print()

    # ========================================================================
    # Summary
    # ========================================================================
    print("=" * 80)
    print("PRIVACY IMPLICATIONS SUMMARY")
    print("=" * 80)
    print()
    print("Taproot (SegWit v1) improves Bitcoin privacy through:")
    print("1. UNIFORM OUTPUTS: All P2TR outputs look identical (32 bytes)")
    print("   - Prevents attacker from identifying transaction type")
    print("   - Makes script-path spends indistinguishable from key-path")
    print()
    print("2. EFFICIENT KEY-PATH: Smallest signature (65 bytes vs 71-73 bytes)")
    print("   - Economic incentive: key-path is cheapest")
    print("   - Privacy becomes the default choice (not premium feature)")
    print()
    print("3. LARGE ANONYMITY SET: Majority of new outputs are P2TR")
    print("   - As adoption increases, P2TR users blend in naturally")
    print("   - You can't identify users by transaction type alone")
    print()
    print("4. CISA POTENTIAL: Future upgrade for even better CoinJoin")
    print("   - Massive fee savings for privacy transactions")
    print("   - Makes CoinJoin accessible to regular users")
    print()


if __name__ == '__main__':
    main()
