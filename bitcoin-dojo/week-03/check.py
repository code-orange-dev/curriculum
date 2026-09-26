#!/usr/bin/env python3
"""
Grade Week 3 (keys, addresses, encoding).

    python3 week-03/check.py              # grades exercises/keys_addresses.py
    python3 week-03/check.py --solution   # grades the reference solution

Expected values come from outside this repo: private key 1 is the example
in BIP173 (its P2WPKH address is BIP173's first test vector), and the rest are
the answers to Programming Bitcoin's Chapter 4 exercises.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
from dojo import G, hash160, need, run_checks, load_week  # noqa: E402

m = load_week(__file__, "keys_addresses.py", "--solution" in sys.argv)


def sec_compressed():
    got = need(m.sec(1 * G, compressed=True), "sec").hex()
    assert got == "0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798", f"got {got}"


def sec_uncompressed():
    got = need(m.sec(1 * G, compressed=False), "sec").hex()
    assert got.startswith("0479be667e") and got.endswith("fb10d4b8") and len(got) == 130, f"got {got}"


def base58():
    assert need(m.encode_base58(bytes.fromhex("00000a")), "encode_base58") == "11B", \
        "leading zero bytes become '1's: 00000a -> 11B"
    got = m.encode_base58(bytes.fromhex("7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d"))
    assert got == "9MA8fRQrT4u8Zj8ZRd6MAiiyaxb2Y1CMpvVkHQu5hVM6", f"got {got}"


def p2pkh_key1():
    got = need(m.p2pkh_address(m.sec(1 * G, True)), "p2pkh_address")
    assert got == "1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH", f"got {got}"


def p2pkh_uncompressed_differs():
    got = m.p2pkh_address(m.sec(1 * G, False))
    assert got == "1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm", f"got {got} - same key, different address!"


def p2pkh_book_answers():
    cases = [(5002, False, True, "mmTPbXQFxboEtNRkwfh6K51jvdtHLxGeMA"),
             (2020 ** 5, True, True, "mopVkxp8UhXqRYbCYJsbeE1h1fiF64jcoH"),
             (0x12345DEADBEEF, True, False, "1F1Pn2y6pDb68E5nYJJeba4TLg2U7B6KF1")]
    for secret, compressed, testnet, want in cases:
        got = m.p2pkh_address(m.sec(secret * G, compressed), testnet=testnet)
        assert got == want, f"secret {secret}: got {got}, want {want}"


def p2wpkh_bip173():
    got = need(m.p2wpkh_address(m.sec(1 * G, True)), "p2wpkh_address")
    assert got == "bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4", f"got {got} (BIP173 test vector)"


def wif_key1():
    assert need(m.wif(1, compressed=True), "wif") == "KwDiBf89QgGbjEhKnhXJuH7LrciVrZi3qYjgd9M7rFU73sVHnoWn"
    assert m.wif(1, compressed=False) == "5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEsreAnchuDf"


def decode_roundtrip():
    payload = need(m.decode_base58_check("1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH"), "decode_base58_check")
    assert payload == b"\x00" + hash160(bytes.fromhex("0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798")), \
        "decoding should return version byte + hash160"
    try:
        m.decode_base58_check("1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMJ")
    except ValueError:
        return
    raise AssertionError("a corrupted address must raise ValueError (bad checksum)")


run_checks("Bitcoin Dojo - Week 3: Keys, Addresses & Encoding", [
    ("SEC: compressed public key of secret 1", sec_compressed),
    ("SEC: uncompressed public key of secret 1", sec_uncompressed),
    ("Base58 encoding", base58),
    ("P2PKH address of secret 1", p2pkh_key1),
    ("Uncompressed key gives a different address", p2pkh_uncompressed_differs),
    ("P2PKH: Programming Bitcoin ch.4 answers (incl. testnet)", p2pkh_book_answers),
    ("P2WPKH (bech32) address = BIP173 test vector", p2wpkh_bip173),
    ("WIF private keys", wif_key1),
    ("Base58Check decode + checksum validation", decode_roundtrip),
]) or sys.exit(1)
