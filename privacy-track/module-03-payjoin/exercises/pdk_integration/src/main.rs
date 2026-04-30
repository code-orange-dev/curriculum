// Bitcoin Privacy Track — Module 3: Payjoin Dev Kit Integration
// Code Orange Dev School | codeorange.dev
//
// Build a working Payjoin sender and receiver using the Payjoin Dev Kit (PDK).
//
// This exercise connects to a local Bitcoin Core regtest node and performs
// a real Payjoin transaction, demonstrating the full BIP77/78 flow.
//
// Prerequisites:
// - Bitcoin Core running in regtest mode with two wallets ("sender", "receiver")
// - Rust toolchain (1.70+)
// - Completed the manual Payjoin exercise (payjoin_testnet.md)
//
// Setup:
//   bitcoind -regtest -daemon -server -rpcuser=bitcoin -rpcpassword=bitcoin
//   bitcoin-cli -regtest createwallet "sender"
//   bitcoin-cli -regtest createwallet "receiver"
//   bitcoin-cli -regtest -rpcwallet=sender generatetoaddress 101 $(bitcoin-cli -regtest -rpcwallet=sender getnewaddress)
//
// Run:
//   cargo run
//
// This exercise has 5 parts. Complete each TODO section.

use anyhow::{Context, Result};
use bitcoin::Amount;
use bitcoincore_rpc::{Auth, Client, RpcApi};

/// Connect to a Bitcoin Core regtest wallet.
fn connect_wallet(wallet_name: &str) -> Result<Client> {
    let url = format!("http://127.0.0.1:18443/wallet/{}", wallet_name);
    let auth = Auth::UserPass("bitcoin".to_string(), "bitcoin".to_string());
    Client::new(&url, auth).context(format!("Failed to connect to wallet '{}'", wallet_name))
}

// ============================================================
// Exercise 1: Verify Environment
// ============================================================
//
// Confirm both wallets exist, have funds, and are ready for Payjoin.

fn verify_environment() -> Result<()> {
    println!("=== Exercise 1: Verify Environment ===\n");

    let sender = connect_wallet("sender")?;
    let receiver = connect_wallet("receiver")?;

    // TODO: Get and print the balance of both wallets
    // Use: sender.get_balance(None, None)?
    //
    // If the sender has no funds, mine 101 blocks:
    //   let addr = sender.get_new_address(None, None)?;
    //   sender.generate_to_address(101, &addr.assume_checked())?;
    //
    // Fund the receiver with 5 BTC from the sender:
    //   let recv_addr = receiver.get_new_address(None, None)?;
    //   sender.send_to_address(&recv_addr.assume_checked(), Amount::from_btc(5.0)?, ...)?;
    //   // Mine a block to confirm
    //   let addr = sender.get_new_address(None, None)?;
    //   sender.generate_to_address(1, &addr.assume_checked())?;

    // YOUR CODE HERE

    println!("  Environment verified!\n");
    Ok(())
}

// ============================================================
// Exercise 2: Create the Original PSBT (Sender Side)
// ============================================================
//
// The sender creates a standard transaction (PSBT) that pays the receiver.
// This is the "original" transaction before Payjoin modification.

fn create_original_psbt() -> Result<String> {
    println!("=== Exercise 2: Create Original PSBT ===\n");

    let sender = connect_wallet("sender")?;
    let receiver = connect_wallet("receiver")?;

    // TODO:
    // 1. Get a fresh address from the receiver
    //    let payment_addr = receiver.get_new_address(None, None)?;
    //
    // 2. Create a funded PSBT from the sender paying 1 BTC to the receiver
    //    Use: sender.wallet_create_funded_psbt(
    //        &[],                    // inputs (empty = auto-select)
    //        &[outputs],             // outputs
    //        None,                   // locktime
    //        Some(options),          // options
    //        None,                   // bip32derivs
    //    )?;
    //
    // 3. Print the PSBT details:
    //    - Number of inputs
    //    - Number of outputs
    //    - Fee amount
    //    - Which output is the payment and which is change
    //
    // 4. Sign the PSBT with the sender's wallet
    //    let signed = sender.wallet_process_psbt(&psbt, ...)?;
    //
    // 5. Return the signed PSBT as a base64 string

    // YOUR CODE HERE

    todo!("Implement create_original_psbt")
}

// ============================================================
// Exercise 3: Receiver Modifies the PSBT (The Payjoin)
// ============================================================
//
// The receiver takes the sender's PSBT and adds their own input.
// This is the core Payjoin operation.

fn receiver_modify_psbt(original_psbt: &str) -> Result<String> {
    println!("=== Exercise 3: Receiver Modifies PSBT ===\n");

    let receiver = connect_wallet("receiver")?;

    // TODO:
    // 1. Decode the original PSBT to inspect it
    //    let decoded = receiver.decode_psbt(original_psbt)?;
    //    Print: "Original TX has N inputs and M outputs"
    //
    // 2. List the receiver's UTXOs
    //    let utxos = receiver.list_unspent(None, None, None, None, None)?;
    //    Pick one UTXO to contribute to the Payjoin
    //    Print: "Receiver contributing UTXO: {txid}:{vout} ({amount} BTC)"
    //
    // 3. This is the hard part — construct a new PSBT that includes:
    //    a) All inputs from the original PSBT
    //    b) The receiver's additional input
    //    c) The payment output (increased by the receiver's input value)
    //    d) The sender's change output (unchanged)
    //
    //    In production, the Payjoin Dev Kit handles this automatically.
    //    For this exercise, you can either:
    //    - Use PDK's receive module (preferred)
    //    - Manually construct the modified PSBT using createpsbt RPC
    //
    // 4. Sign the receiver's input
    //    let receiver_signed = receiver.wallet_process_psbt(&modified_psbt, ...)?;
    //
    // 5. Print the modified PSBT details:
    //    - New number of inputs (should be original + 1)
    //    - Updated output amounts
    //    - "Chain analyst sees: N inputs, M outputs — applies CIOH — WRONG"
    //
    // 6. Return the receiver-signed modified PSBT

    // YOUR CODE HERE

    todo!("Implement receiver_modify_psbt")
}

// ============================================================
// Exercise 4: Sender Verifies and Signs (Security Checks)
// ============================================================
//
// The sender MUST verify the receiver's modifications before signing.
// A malicious receiver could steal funds if the sender doesn't check.

fn sender_verify_and_sign(original_psbt: &str, modified_psbt: &str) -> Result<String> {
    println!("=== Exercise 4: Sender Verifies and Signs ===\n");

    let sender = connect_wallet("sender")?;

    // TODO: Implement ALL of these verification checks.
    // These are critical for security — a real wallet must perform every one.
    //
    // VERIFICATION CHECKLIST:
    //
    // 1. SENDER'S INPUTS UNCHANGED:
    //    All inputs from the original PSBT must still be present
    //    in the modified PSBT with identical scriptPubKeys.
    //    "Check: sender's inputs are preserved"
    //
    // 2. SENDER'S PAYMENT OUTPUT UNCHANGED:
    //    The output paying the receiver must have the same or greater value.
    //    (Greater is fine — the receiver is adding value.)
    //    "Check: payment output value >= original"
    //
    // 3. SENDER'S CHANGE OUTPUT UNCHANGED:
    //    The sender's change output must have the same value.
    //    If the receiver reduced the sender's change, they're stealing.
    //    "Check: sender's change output preserved"
    //
    // 4. NO NEW OUTPUTS TO UNKNOWN ADDRESSES:
    //    The modified PSBT should not add outputs to addresses
    //    the sender doesn't recognize. (The receiver's output increasing
    //    is expected; a new third output is suspicious.)
    //    "Check: no unexpected new outputs"
    //
    // 5. FEE IS REASONABLE:
    //    The total fee should not increase unreasonably.
    //    The receiver may slightly increase the fee (they added an input),
    //    but a massive fee increase could be an attack.
    //    "Check: fee increase is reasonable"
    //
    // 6. TRANSACTION IS VALID:
    //    The modified PSBT must be a valid Bitcoin transaction.
    //
    // If all checks pass:
    //   Sign the sender's inputs: sender.wallet_process_psbt(&modified_psbt, ...)?
    //   Finalize: sender.finalize_psbt(&both_signed, None)?
    //   Return the final raw transaction hex
    //
    // If any check fails:
    //   Print which check failed and return an error
    //   The sender should broadcast the ORIGINAL transaction instead

    // YOUR CODE HERE

    todo!("Implement sender_verify_and_sign")
}

// ============================================================
// Exercise 5: Broadcast and Analyze
// ============================================================
//
// Broadcast the Payjoin transaction, then analyze it from a
// chain analyst's perspective.

fn broadcast_and_analyze(final_tx_hex: &str) -> Result<()> {
    println!("=== Exercise 5: Broadcast and Analyze ===\n");

    let sender = connect_wallet("sender")?;

    // TODO:
    // 1. Broadcast the transaction
    //    let txid = sender.send_raw_transaction(final_tx_hex)?;
    //    println!("  Payjoin txid: {}", txid);
    //
    // 2. Mine a block
    //    let addr = sender.get_new_address(None, None)?;
    //    sender.generate_to_address(1, &addr.assume_checked())?;
    //
    // 3. Decode the confirmed transaction
    //    let tx = sender.get_raw_transaction_info(&txid, None)?;
    //
    // 4. Print the chain analyst's view:
    //    println!("\n  === Chain Analyst's View ===");
    //    println!("  Inputs: {}", tx.vin.len());
    //    println!("  Outputs: {}", tx.vout.len());
    //    println!();
    //    println!("  Applying CIOH: 'All {} inputs belong to the same entity'", tx.vin.len());
    //    println!("  This conclusion is: WRONG");
    //    println!();
    //    println!("  Applying change detection:");
    //    // Analyze which output looks like change
    //    // The analyst will likely identify the wrong entity as the sender
    //    println!();
    //    println!("  The Payjoin has created ambiguity:");
    //    println!("  - Possible interpretation 1: ...");
    //    println!("  - Possible interpretation 2: ...");
    //    println!("  - Possible interpretation 3: ...");
    //    println!("  The analyst cannot determine which is correct.");
    //
    // 5. Now create a NORMAL (non-Payjoin) transaction for comparison
    //    Send the same amount to the same receiver, but without Payjoin
    //    Broadcast and decode it
    //    Print the same analysis
    //    Show how the normal transaction reveals much more information

    // YOUR CODE HERE

    todo!("Implement broadcast_and_analyze")
}

// ============================================================
// Main
// ============================================================

fn main() -> Result<()> {
    println!("================================================================");
    println!("Bitcoin Privacy Track — Payjoin Dev Kit Integration");
    println!("Code Orange Dev School | codeorange.dev");
    println!("================================================================\n");

    // Exercise 1: Verify environment
    verify_environment()?;

    // Exercise 2: Sender creates original PSBT
    let original_psbt = create_original_psbt()?;

    // Exercise 3: Receiver modifies the PSBT
    let modified_psbt = receiver_modify_psbt(&original_psbt)?;

    // Exercise 4: Sender verifies and signs
    let final_tx = sender_verify_and_sign(&original_psbt, &modified_psbt)?;

    // Exercise 5: Broadcast and analyze
    broadcast_and_analyze(&final_tx)?;

    println!("\n================================================================");
    println!("REFLECTION QUESTIONS:");
    println!("================================================================");
    println!();
    println!("1. In Exercise 4, you implemented 5 security checks.");
    println!("   Which check is the most important? What happens if");
    println!("   a wallet skips it?");
    println!();
    println!("2. The Payjoin Dev Kit handles the PSBT modification");
    println!("   automatically. What advantage does manual implementation");
    println!("   (as in this exercise) give you as a developer?");
    println!();
    println!("3. How would you modify this code to use BIP77 (V2)");
    println!("   with a Payjoin Directory instead of direct communication?");
    println!();
    println!("4. If you were integrating Payjoin into a mobile wallet,");
    println!("   what UX would you show the user during the PSBT");
    println!("   exchange? Should the user even know a Payjoin is");
    println!("   happening?");
    println!();
    println!("================================================================");
    println!("Done! Bring your code and analysis to the weekly session.");
    println!("================================================================");

    Ok(())
}
