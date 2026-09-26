#!/usr/bin/env python3
"""
Grade your Silent Payments code against the official BIP352 test vectors.

    python3 run_vectors.py send              # grade send.py      (Session 1)
    python3 run_vectors.py receive           # grade receive.py   (Session 2)
    python3 run_vectors.py send --solution   # run the reference solution instead
    python3 run_vectors.py send -v           # show got/expected on failure

The vectors are the ones Bitcoin Core, libsecp256k1, rust-silentpayments and
every other implementation test against. Passing them all means your code
interoperates with real wallets.
"""

import argparse
import importlib.util
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from secp import G, N, Point  # noqa: E402
from txin import input_pubkey, serialize_outpoint  # noqa: E402

VECTORS = HERE / "vectors" / "send_and_receive_test_vectors.json"


def load(name, solution):
    path = HERE / ("solutions" if solution else "") / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"{name}_under_test", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class NotImplementedYet(Exception):
    pass


def need(value, what):
    if value is None:
        raise NotImplementedYet(what)
    return value


def eligible_inputs(vins, with_privkeys):
    keys, pubs = [], []
    for vin in vins:
        got = input_pubkey(vin)
        if got is None:
            continue
        pub, is_taproot = got
        pubs.append(pub)
        if with_privkeys:
            keys.append((int(vin["private_key"], 16), is_taproot))
    return keys, pubs


# --------------------------------------------------------------------------- send

def grade_send(case, mod, verbose):
    for test in case["sending"]:
        given, expected = test["given"], test["expected"]
        keys, _ = eligible_inputs(given["vin"], with_privkeys=True)
        outpoints = [serialize_outpoint(v["txid"], v["vout"]) for v in given["vin"]]
        recipients = []
        for r in given["recipients"]:
            recipients += [r["address"]] * r.get("count", 1)

        if not keys:  # no eligible inputs: a sender must not create SP outputs
            if expected["outputs"] != [[]]:
                return False, "vector expects outputs but no eligible inputs found"
            continue

        # Step-by-step checks give a precise hint about which exercise is wrong.
        if "input_private_key_sum" in expected:
            a_sum = need(mod.sum_input_private_keys(keys), "sum_input_private_keys")
            if a_sum != int(expected["input_private_key_sum"], 16):
                return False, "Exercise 2: a_sum is wrong (did you negate odd-y taproot keys?)"

        B_scan0, _ = need(mod.decode_sp_address(recipients[0]), "decode_sp_address")
        if B_scan0.to_bytes().hex() != given["recipients"][0]["scan_pub_key"]:
            return False, "Exercise 1: decoded B_scan does not match"

        outputs = need(mod.create_outputs(keys, outpoints, recipients), "create_outputs")
        got = {o.hex() for o in outputs}
        if not any(got == set(option) for option in expected["outputs"]):
            msg = "outputs don't match"
            if verbose:
                msg += f"\n      got      {sorted(got)}\n      expected one of {expected['outputs']}"
            return False, msg
    return True, ""


# ------------------------------------------------------------------------ receive

def grade_receive(case, mod, verbose):
    input_hash = load("send", solution=True).input_hash  # sender side is Session 1's job
    for test in case["receiving"]:
        given, expected = test["given"], test["expected"]
        b_scan = int(given["key_material"]["scan_priv_key"], 16)
        b_spend = int(given["key_material"]["spend_priv_key"], 16)
        B_scan, B_spend = b_scan * G, b_spend * G

        addresses = [need(mod.encode_sp_address(B_scan, B_spend, "sp"), "encode_sp_address")]
        labels = {}
        for m in given["labels"]:
            label = need(mod.generate_label(b_scan, m), "generate_label")
            labels[(label * G).to_bytes()] = label
            B_m = need(mod.labeled_spend_key(b_scan, B_spend, m), "labeled_spend_key")
            addresses.append(mod.encode_sp_address(B_scan, B_m, "sp"))
        if addresses != expected["addresses"]:
            return False, "Exercise 1/4: your addresses don't match (encoding or labels)"

        _, pubs = eligible_inputs(given["vin"], with_privkeys=False)
        found = []
        if pubs:
            A_sum = Point.infinity()
            for p in pubs:
                A_sum = A_sum + p
            if A_sum.is_infinity:
                continue  # receiver must skip this tx
            outpoints = [serialize_outpoint(v["txid"], v["vout"]) for v in given["vin"]]
            tweak = need(mod.compute_tweak(A_sum, input_hash(outpoints, A_sum)), "compute_tweak")
            if "tweak" in expected and tweak.to_bytes().hex() != expected["tweak"]:
                return False, "Exercise 2: tweak is wrong"
            outputs = [bytes.fromhex(o) for o in given["outputs"]]
            found = need(mod.scan(b_scan, B_spend, tweak, outputs, labels or None), "scan")

        if "n_outputs" in expected:
            if len(found) != expected["n_outputs"]:
                return False, f"Exercise 3: found {len(found)} outputs, expected {expected['n_outputs']}"
            continue
        want = {(o["pub_key"], o["priv_key_tweak"]) for o in expected["outputs"]}
        got = {(o["pub_key"], o["priv_key_tweak"]) for o in found}
        if got != want:
            hint = "Exercise 4: labels" if given["labels"] else "Exercise 3: scan"
            msg = f"{hint} - found {len(got)} outputs, expected {len(want)}"
            if verbose:
                msg += f"\n      got      {sorted(got)}\n      expected {sorted(want)}"
            return False, msg

        # Stretch goal: prove you can actually spend what you found.
        for o in found:
            d = mod.spend_key(b_spend, int(o["priv_key_tweak"], 16))
            if d is None:
                break
            if (d * G).to_xonly().hex() != o["pub_key"] or not (d * G).has_even_y():
                return False, "Exercise 5: spend_key doesn't match the output key"
    return True, ""


# --------------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("side", choices=["send", "receive"])
    ap.add_argument("--solution", action="store_true", help="grade the reference solution")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    mod = load(args.side, args.solution)
    grade = grade_send if args.side == "send" else grade_receive
    cases = json.loads(VECTORS.read_text())

    passed = failed = todo = 0
    start = time.time()
    for i, case in enumerate(cases, 1):
        name = case["comment"]
        try:
            ok, why = grade(case, mod, args.verbose)
        except NotImplementedYet as e:
            print(f"  ·  {i:2} {name}\n        not implemented yet: {e}()")
            todo += 1
            continue
        except Exception as e:  # a crash in participant code is just a failure
            ok, why = False, f"crashed: {type(e).__name__}: {e}"
        if ok:
            passed += 1
            print(f"  ✓  {i:2} {name}")
        else:
            failed += 1
            print(f"  ✗  {i:2} {name}\n        {why}")

    total = passed + failed + todo
    print(f"\n{passed}/{total} vectors passing  ({time.time() - start:.1f}s)")
    if passed == total:
        print("All green. Your code agrees with every BIP352 implementation. 🟠")
    sys.exit(0 if failed == 0 and todo == 0 else 1)


if __name__ == "__main__":
    main()
