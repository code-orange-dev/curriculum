"""
Bitcoin Dojo - Week 5 REFERENCE SOLUTION: Script & Transaction Validation
(Programming Bitcoin, Chapters 3, 6 and 7)

Grade it:  python3 week-05/check.py --solution
"""

import copy
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "lib"))
from dojo import G, N, Point, hash160, hash256, parse_der  # noqa: E402

# PROVIDED: last week's transaction parser (reference version).
_spec = importlib.util.spec_from_file_location("week4", ROOT / "week-04" / "solutions" / "transactions.py")
_week4 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_week4)
Tx = _week4.Tx

OP_0, OP_DUP, OP_HASH160, OP_EQUAL, OP_EQUALVERIFY, OP_CHECKSIG, OP_CHECKMULTISIG = 0x00, 0x76, 0xA9, 0x87, 0x88, 0xAC, 0xAE
SIGHASH_ALL = 1


def parse_script(raw: bytes):
    """PROVIDED: bytes -> list of items. Data pushes become bytes, opcodes stay ints."""
    items, i = [], 0
    while i < len(raw):
        op = raw[i]
        i += 1
        if 1 <= op <= 75:
            items.append(raw[i:i + op])
            i += op
        elif op == 0x4C:  # OP_PUSHDATA1
            n = raw[i]
            items.append(raw[i + 1:i + 1 + n])
            i += 1 + n
        else:
            items.append(op)
    return items


def sig_hash(tx, input_index: int, script_pubkey: bytes) -> int:
    t = copy.deepcopy(tx)
    for i, tx_in in enumerate(t.tx_ins):
        tx_in.script_sig = script_pubkey if i == input_index else b""
    return int.from_bytes(hash256(t.serialize() + SIGHASH_ALL.to_bytes(4, "little")), "big")


def verify(z: int, r: int, s: int, pubkey: Point) -> bool:
    if not (1 <= r < N and 1 <= s < N):
        return False
    s_inv = pow(s, N - 2, N)
    R = (z * s_inv % N) * G + (r * s_inv % N) * pubkey
    return not R.is_infinity and R.x % N == r


def check_sig(der_with_type: bytes, sec: bytes, z: int) -> bool:
    """PROVIDED glue: strip the sighash byte, parse DER and the key, then verify."""
    r, s = parse_der(der_with_type[:-1])
    return verify(z, r, s, Point.from_sec(sec))


def evaluate(script_sig: bytes, script_pubkey: bytes, z: int) -> bool:
    stack = []
    for item in parse_script(script_sig) + parse_script(script_pubkey):
        if isinstance(item, bytes):
            stack.append(item)
        elif item == OP_0:
            stack.append(b"")
        elif 0x51 <= item <= 0x60:  # OP_1 .. OP_16 push the number 1..16
            stack.append(bytes([item - 0x50]))
        elif item == OP_DUP:
            if not stack:
                return False
            stack.append(stack[-1])
        elif item == OP_HASH160:
            if not stack:
                return False
            stack.append(hash160(stack.pop()))
        elif item in (OP_EQUAL, OP_EQUALVERIFY):
            if len(stack) < 2:
                return False
            equal = stack.pop() == stack.pop()
            if item == OP_EQUALVERIFY:
                if not equal:
                    return False
            else:
                stack.append(b"\x01" if equal else b"")
        elif item == OP_CHECKSIG:
            if len(stack) < 2:
                return False
            sec, sig = stack.pop(), stack.pop()
            stack.append(b"\x01" if check_sig(sig, sec, z) else b"")
        elif item == OP_CHECKMULTISIG:
            if not op_checkmultisig(stack, z):
                return False
        else:
            return False  # opcode not supported in this mini interpreter
    return bool(stack) and stack[-1] not in (b"", b"\x00")


def op_checkmultisig(stack, z: int) -> bool:
    """Stack (top last): dummy, sig_1..sig_m, m, key_1..key_n, n. Pushes result."""
    n = int.from_bytes(stack.pop(), "little")
    keys = [stack.pop() for _ in range(n)][::-1]
    m = int.from_bytes(stack.pop(), "little")
    sigs = [stack.pop() for _ in range(m)][::-1]
    stack.pop()  # the off-by-one: CHECKMULTISIG consumes one extra element
    k = 0
    for sig in sigs:  # signatures must appear in the same order as the keys
        while k < len(keys) and not check_sig(sig, keys[k], z):
            k += 1
        if k == len(keys):
            stack.append(b"")
            return True
        k += 1
    stack.append(b"\x01")
    return True
