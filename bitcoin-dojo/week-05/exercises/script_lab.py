"""
Bitcoin Dojo - Week 5 Exercises: Script & Transaction Validation
Code Orange Dev School | codeorange.dev

Based on Programming Bitcoin, Chapters 3, 6 and 7
https://github.com/jimmysong/programmingbitcoin

You'll verify the signature on a REAL transaction from block 250,000 (2013),
using your own sighash, your own ECDSA and your own Script interpreter.
Run from the bitcoin-dojo folder:

    python3 week-05/check.py

Provided: the curve (G, N, Point), hash160/hash256, parse_der, last week's Tx
parser, parse_script(), and check_sig() glue once your verify() works.
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
    """Exercise 1 - the legacy signature hash (SIGHASH_ALL).

    What the signer actually signed:
      1. copy the transaction (copy.deepcopy)
      2. empty every input's script_sig (b"")...
      3. ...except input_index, which gets the script_pubkey of the coin it spends
      4. serialize, append SIGHASH_ALL as 4 bytes little-endian
      5. hash256 it and return int.from_bytes(..., "big")
    """
    # YOUR CODE HERE
    return None


def verify(z: int, r: int, s: int, pubkey: Point) -> bool:
    """Exercise 2 - ECDSA verification (Programming Bitcoin ch. 3).

      s_inv = pow(s, N - 2, N)           # modular inverse via Fermat
      u = z * s_inv % N
      v = r * s_inv % N
      R = u * G + v * pubkey
      valid if R.x % N == r

    Return True/False (reject r or s outside [1, N-1]).
    """
    # YOUR CODE HERE
    return None


def check_sig(der_with_type: bytes, sec: bytes, z: int) -> bool:
    """PROVIDED glue: strip the sighash byte, parse DER and the key, then verify."""
    r, s = parse_der(der_with_type[:-1])
    return verify(z, r, s, Point.from_sec(sec))


def evaluate(script_sig: bytes, script_pubkey: bytes, z: int) -> bool:
    """Exercise 3 - a tiny Script interpreter.

    Run the scriptSig items, then the scriptPubKey items, on ONE stack.
    Items are bytes (push them) or opcode ints. Implement:
      OP_0             push b""
      OP_1..OP_16      (0x51-0x60) push bytes([item - 0x50])
      OP_DUP           duplicate the top item
      OP_HASH160       pop, push hash160(item)
      OP_EQUAL         pop two, push b"\x01" if equal else b""
      OP_EQUALVERIFY   pop two, return False immediately if not equal
      OP_CHECKSIG      pop sec (top), then sig; push b"\x01" if check_sig(sig, sec, z) else b""
      OP_CHECKMULTISIG call op_checkmultisig(stack, z); return False if it returns False
      anything else    return False (unsupported)
    Any opcode with too few stack items -> return False.
    At the end: True if the stack is non-empty and the top isn't b"" or b"\x00".
    """
    stack = []
    for item in parse_script(script_sig) + parse_script(script_pubkey):
        if isinstance(item, bytes):
            stack.append(item)
        elif item == OP_DUP:
            if not stack:
                return False
            stack.append(stack[-1])
        # YOUR CODE HERE: the other opcodes
        else:
            return None  # replace with: return False, once the others are done
    return None  # replace with the final stack check


def op_checkmultisig(stack, z: int) -> bool:
    """Exercise 4 - OP_CHECKMULTISIG, bug and all.

    Stack, top last:   <dummy> <sig_1> ... <sig_m> <m> <key_1> ... <key_n> <n>
      1. pop n, then n keys (restore their order), then m, then m sigs
      2. pop ONE MORE item: the famous off-by-one. Satoshi's code pops an extra
         element, so every multisig scriptSig starts with OP_0. It can't be
         fixed without a hard fork.
      3. each signature must match a key, in order: walk the keys forward and
         never go back
      4. push b"\x01" if all m sigs matched, else b"". Return True (it ran).
    m and n arrive as 1-byte numbers: int.from_bytes(b, "little").
    """
    # YOUR CODE HERE
    return None


# ---------------------------------------------------------------------------
# Discussion (bring to the call):
#  1. Trace the real P2PKH script: what's on the stack after each opcode?
#  2. Why does the signer put the *previous* scriptPubKey into the sighash?
#  3. The off-by-one bug: why has Bitcoin kept it for 15+ years? What did
#     BIP147 (NULLDUMMY) do about the extra element?
#  4. Look at the real transaction: its public key is uncompressed (65 bytes).
#     What did that cost the sender in fees, compared to a compressed key?
# ---------------------------------------------------------------------------
