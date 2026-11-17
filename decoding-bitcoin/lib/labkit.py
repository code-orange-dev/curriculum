"""
Decoding Bitcoin lab toolkit. PROVIDED - you don't need to edit this file.

    hash256(b)                double SHA256
    load_lab(check_file, name, solution)   import exercises/<name> or solutions/<name>
    run_checks(title, checks) run a list of (name, function) checks and print a score
    TXS                       the real mainnet transactions in data/transactions.json
"""

import hashlib
import importlib.util
import json
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TXS = json.loads((ROOT / "data" / "transactions.json").read_text())


def hash256(b: bytes) -> bytes:
    return hashlib.sha256(hashlib.sha256(b).digest()).digest()


def load_lab(check_file, name, solution=False):
    folder = "solutions" if solution else "exercises"
    path = Path(check_file).resolve().parent / folder / name
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    print(f"Checking {path.relative_to(ROOT)}\n")
    return mod


def run_checks(title, checks):
    passed = todo = 0
    print(title)
    print("-" * len(title))
    for name, fn in checks:
        try:
            fn()
            print(f"  PASS  {name}")
            passed += 1
        except NotImplementedError:
            print(f"  ....  {name}: not implemented yet")
            todo += 1
        except AssertionError as e:
            print(f"  FAIL  {name}: {e}")
        except Exception:
            print(f"  FAIL  {name}: crashed")
            traceback.print_exc(limit=2, file=sys.stdout)
    print(f"\n{passed}/{len(checks)} checks passing" + (f" ({todo} not implemented yet)" if todo else ""))
    return passed == len(checks)
