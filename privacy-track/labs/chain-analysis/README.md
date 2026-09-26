# Chain Analysis Lab (S4)

Play the surveillance firm. Implement the heuristics analysts use on sample transactions, then see how far they get and where they break.

```bash
python3 chain_analysis_lab.py
```

| Exercise | Heuristic |
|---|---|
| `apply_cioh` | Common-input-ownership: all inputs belong to one entity |
| `detect_change_output` | Script-type match, round amounts, unnecessary inputs |
| `fingerprint_wallet` | Version, nLockTime, script types, fee rate, output count |
| `detect_coinjoin` | Equal-value outputs and anonymity sets |
| `trace_entity` | Follow an address through the graph |

Unimplemented functions are skipped, so you can go one at a time. The sample data is synthetic. In the session, test your `fingerprint_wallet` guesses against the real transactions the room builds, and trust the real ones over the hints.

No dependencies. Python 3.8+.
