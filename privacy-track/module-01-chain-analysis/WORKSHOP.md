This plan replaces the one in README.md

# 0:00–0:10 — Set the investigation

Give everyone access to the same private Signet node.

Present one realistic case:

We know:

- Address A received funds from a ransomware payment.
- We know the approximate time and amount.

We want to find:

- Where did the funds go?
- Which addresses appear to belong to the same actor?
- What behavioral pattern is being used?
- Where does our evidence become uncertain?

Don't explain what an input/output/UTXO is. Assume all of that.

# 0:10–0:30 — Investigation 1: Fund tracing

Students work directly with bitcoin-cli / RPC.

Give them only the starting address.

Their task:

1. Identify relevant transactions.
2. Follow the funds.
3. Record the path.
4. Identify splits, consolidations and dormant periods.
5. Produce a small graph of the flow.

5-minute group discussion:
Different groups will usually choose different interpretations of the same flow. That's useful.

# 0:30–0:50 — Investigation 2: Address attribution

Now give them:

We know:
- 3 addresses belong to Exchange X.

We want to find:
- Which other addresses are likely controlled by Exchange X?

Students investigate using evidence such as:
- common-input relationships
- consolidation
- sweep patterns
- change behavior
- repeated transaction structures
- temporal patterns

Crucially, require:
- Address -> evidence -> confidence, rather than simply "I think these belong together."

This introduces the distinction between clustering and attribution.

# 0:50–1:00 — Break / compare findings

Put 2–3 competing attribution hypotheses on the screen.

Ask:
> Which evidence actually increases confidence?

This is where I would introduce the idea that on-chain attribution is usually probabilistic rather than cryptographic proof of ownership.

# 1:00–1:30 — Investigation 3: Behavioral analysis

Give them a cluster containing, say, 30–50 addresses.

Don't tell them what the entity is.

We know:
- These addresses are related to one organization.
We want to find:
- What kind of organization/activity does the cluster resemble?

Have them calculate/visualize:
- transaction frequency
- active periods
- holding time
- fan-in / fan-out
- transaction-size distributions
- number of counterparties
- consolidation behavior
- periodic sweeps
- dormant → active transitions

The important part is that **the answer isn't a label**.

They should produce something like:

"This cluster appears to operate as a payment processor because..."

# 1:30–1:50 — Red team / blue team

This is the part I think would make the workshop distinctive.

Give them a deliberately simple detection rule:

> Detector: flag clusters with high fan-out + short holding times + repeated transactions.

Split the room:

Blue team: improve the detector.

Red team: construct synthetic Signet behavior that causes the detector to fail without simply changing the underlying economic story.

Then compare:

- What did the detector catch?
- What did it miss?
- Which features were actually useful?
- Which were easy to manipulate?

This turns chain analysis into an adversarial problem rather than another blockchain tutorial.

# 1:50–2:00 — Final investigation

Give everyone one final question:

> We know: Address A is connected to Entity X.
> We want to find: What is the strongest evidence that Address B is also controlled by X?

Each group gets 60 seconds to present its conclusion.

Finish by showing the "ground truth" that you built into the Signet scenario.
