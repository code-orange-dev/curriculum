"""
Bitcoin Dojo — Week 1 REFERENCE SOLUTION: Finite Fields
Code Orange Dev School | codeorange.dev

Based on Programming Bitcoin by Jimmy Song (Chapter 1)
https://github.com/jimmysong/programmingbitcoin

Instructions:
- Complete each exercise by filling in the code where indicated
- Run this file with: python3 finite_fields.py
- All tests should pass when your implementation is correct
- Discuss your solutions at the weekly Monday 11:00 UTC call
"""


# ============================================================
# Exercise 1: Implement the FieldElement class
# ============================================================
#
# A finite field element is a number within a set {0, 1, 2, ..., p-1}
# where p is a prime number (the "order" of the field).
#
# All arithmetic operations wrap around using modulo p.
#
# Your task: implement __eq__, __ne__, __add__, __sub__, __mul__,
# __pow__, and __truediv__ for the FieldElement class.

class FieldElement:
    """Represents an element in a finite field F_p (integers mod prime p)."""

    def __init__(self, num, prime):
        if num >= prime or num < 0:
            error = f"Num {num} not in field range 0 to {prime - 1}"
            raise ValueError(error)
        self.num = num
        self.prime = prime

    def __repr__(self):
        return f"FieldElement_{self.prime}({self.num})"

    def __eq__(self, other):
        """Two field elements are equal if they have the same num and prime."""
        # YOUR CODE HERE
        # Hint: check that both num and prime match
        return other is not None and self.num == other.num and self.prime == other.prime

    def __ne__(self, other):
        """Two field elements are not equal if __eq__ returns False."""
        # YOUR CODE HERE
        return not (self == other)

    def __add__(self, other):
        """Add two field elements: (a + b) mod p"""
        if self.prime != other.prime:
            raise TypeError("Cannot add two numbers in different Fields")
        # YOUR CODE HERE
        # Hint: (self.num + other.num) % self.prime
        return self.__class__((self.num + other.num) % self.prime, self.prime)

    def __sub__(self, other):
        """Subtract two field elements: (a - b) mod p"""
        if self.prime != other.prime:
            raise TypeError("Cannot subtract two numbers in different Fields")
        # YOUR CODE HERE
        # Hint: (self.num - other.num) % self.prime
        return self.__class__((self.num - other.num) % self.prime, self.prime)

    def __mul__(self, other):
        """Multiply two field elements: (a * b) mod p"""
        if self.prime != other.prime:
            raise TypeError("Cannot multiply two numbers in different Fields")
        # YOUR CODE HERE
        return self.__class__((self.num * other.num) % self.prime, self.prime)

    def __pow__(self, exponent):
        """Raise a field element to a power: (a ** exp) mod p

        Important: use Fermat's Little Theorem to handle negative exponents.
        a^(p-1) = 1 (mod p), so a^(-1) = a^(p-2) (mod p)
        Therefore: a^n = a^(n % (p-1)) (mod p)
        """
        # YOUR CODE HERE
        # Hint: n = exponent % (self.prime - 1)
        #       then use Python's built-in pow(self.num, n, self.prime)
        n = exponent % (self.prime - 1)
        return self.__class__(pow(self.num, n, self.prime), self.prime)

    def __rmul__(self, coefficient):
        """PROVIDED: lets you write 3 * element. Week 2's elliptic-curve
        formulas need this (e.g. 3 * x**2 when doubling a point)."""
        return self.__class__((self.num * coefficient) % self.prime, self.prime)

    def __truediv__(self, other):
        """Divide two field elements: a / b = a * b^(p-2) mod p

        Division in a finite field uses Fermat's Little Theorem:
        b^(-1) = b^(p-2) mod p
        So a / b = a * b^(p-2) mod p
        """
        if self.prime != other.prime:
            raise TypeError("Cannot divide two numbers in different Fields")
        # YOUR CODE HERE
        # Hint: use self * (other ** (self.prime - 2))
        # Or compute directly: (self.num * pow(other.num, self.prime - 2, self.prime)) % self.prime
        return self * (other ** (self.prime - 2))


# ============================================================
# Exercise 2: Verify field properties
# ============================================================
#
# A finite field must satisfy these properties:
# 1. Closure: a + b and a * b are in the field
# 2. Associativity: (a + b) + c = a + (b + c)
# 3. Commutativity: a + b = b + a
# 4. Additive identity: a + 0 = a
# 5. Multiplicative identity: a * 1 = a
# 6. Additive inverse: a + (-a) = 0
# 7. Multiplicative inverse: a * a^(-1) = 1 (for a != 0)

def verify_field_properties(prime):
    """Verify all field properties hold for F_prime.

    Test with several random elements. Print results.
    Returns True if all properties hold.
    """
    import random

    all_passed = True

    # Pick random elements
    a_num = random.randint(0, prime - 1)
    b_num = random.randint(0, prime - 1)
    c_num = random.randint(0, prime - 1)

    a = FieldElement(a_num, prime)
    b = FieldElement(b_num, prime)
    c = FieldElement(c_num, prime)
    zero = FieldElement(0, prime)
    one = FieldElement(1, prime)

    # YOUR CODE HERE: Test each property and print results
    # Example:
    # 1. Closure
    result = a + b
    assert result.num >= 0 and result.num < prime, "Closure failed for addition"
    print(f"  Closure (addition): {a} + {b} = {result} ... PASS")

    # 2. Commutativity of addition
    assert a + b == b + a
    # print(f"  Commutativity (addition): PASS")

    # 3. Associativity of addition
    assert (a + b) + c == a + (b + c)

    # 4. Additive identity
    assert a + zero == a

    # 5. Multiplicative identity
    assert a * one == a

    # 6. Additive inverse
    neg_a = FieldElement((prime - a_num) % prime, prime)
    assert a + neg_a == zero

    # 7. Multiplicative inverse (for non-zero elements)
    if a_num != 0:
        a_inv = a ** (prime - 2)
        assert a * a_inv == one
    print("  Commutativity, associativity, identities, inverses ... PASS")

    

    return all_passed


# ============================================================
# Exercise 3: Why must the prime be prime?
# ============================================================
#
# Try creating a "field" with a composite (non-prime) modulus.
# Show that multiplicative inverses break.

def demonstrate_composite_failure():
    """Show that a composite modulus breaks the field properties.

    Try modulus = 15 (= 3 * 5).
    Find an element that has no multiplicative inverse.

    Hint: 3 has no inverse mod 15 because gcd(3, 15) = 3 != 1
    """
    modulus = 15  # composite!

    print(f"\nTrying modulus = {modulus} (composite = 3 x 5)")
    print("Looking for elements without multiplicative inverses:")

    # YOUR CODE HERE
    # For each element a in {1, 2, ..., 14}, try to find b such that (a*b) % 15 == 1
    # Print which elements have no inverse
    #
    for a in range(1, modulus):
        if not any((a * b) % modulus == 1 for b in range(1, modulus)):
            print(f"  {a} has NO multiplicative inverse mod {modulus}")


# ============================================================
# Exercise 4: Bitcoin's finite field
# ============================================================
#
# Bitcoin uses the prime:
# p = 2^256 - 2^32 - 977
#
# This is the prime for the secp256k1 elliptic curve.

def bitcoin_field_element():
    """Create a FieldElement using Bitcoin's actual prime.

    Demonstrate that arithmetic works even with these huge numbers.
    """
    P = 2**256 - 2**32 - 977

    print(f"\nBitcoin's prime p = {P}")
    print(f"Number of digits: {len(str(P))}")

    # YOUR CODE HERE
    # Create two field elements and perform operations
    a = FieldElement(42, P)
    b = FieldElement(99, P)
    print(f"  a + b = {(a + b).num}")
    print(f"  a / b, times b, gives back a: {(a / b) * b == a}")
    assert (a / b) * b == a, "Division verification failed!"


# ============================================================
# TESTS — Run these to verify your implementation
# ============================================================

def _check(name, fn):
    """Run one test. Unimplemented methods return None, which shows up as
    'not implemented yet' instead of crashing the whole file."""
    try:
        detail = fn()
        print(f"  ✓  {name}" + (f"  {detail}" if detail else ""))
        return "pass"
    except (TypeError, AttributeError) as e:
        if "NoneType" in str(e) or "None" in str(e):
            print(f"  ·  {name}\n        not implemented yet")
            return "todo"
        print(f"  ✗  {name}\n        {type(e).__name__}: {e}")
        return "fail"
    except AssertionError as e:
        if str(e).endswith("got None"):
            print(f"  ·  {name}\n        not implemented yet")
            return "todo"
        print(f"  ✗  {name}\n        {e or 'assertion failed'}")
        return "fail"


def _test_equality():
    a, b, c = FieldElement(7, 13), FieldElement(7, 13), FieldElement(6, 13)
    if a.__eq__(b) is None:
        raise TypeError("__eq__ returned None")
    assert a == b, "Equal elements should be equal (implement __eq__)"
    assert a != c, "Different elements should not be equal (implement __ne__)"


def _test_add():
    a, b = FieldElement(7, 13), FieldElement(12, 13)
    assert a + b == FieldElement(6, 13), f"(7 + 12) % 13 should be 6, got {a + b}"


def _test_sub():
    a, b = FieldElement(6, 19), FieldElement(13, 19)
    assert a - b == FieldElement(12, 19), f"(6 - 13) % 19 should be 12, got {a - b}"


def _test_mul():
    a, b = FieldElement(3, 13), FieldElement(12, 13)
    assert a * b == FieldElement(10, 13), f"(3 * 12) % 13 should be 10, got {a * b}"


def _test_pow():
    a = FieldElement(3, 13)
    assert a ** 3 == FieldElement(1, 13), f"3^3 % 13 should be 1, got {a ** 3}"


def _test_div():
    a, b = FieldElement(2, 19), FieldElement(7, 19)
    assert a / b == FieldElement(3, 19), f"2/7 in F_19 should be 3, got {a / b}"


def _test_negative_exponent():
    a = FieldElement(7, 13)
    assert (a ** -3) * (a ** 3) == FieldElement(1, 13), "a^-3 * a^3 should be 1 (use Fermat's little theorem)"


def run_tests():
    print("=" * 60)
    print("Bitcoin Dojo — Week 1: Finite Field Tests")
    print("=" * 60)
    tests = [
        ("Equality", _test_equality),
        ("Addition", _test_add),
        ("Subtraction", _test_sub),
        ("Multiplication", _test_mul),
        ("Exponentiation", _test_pow),
        ("Division", _test_div),
        ("Negative exponent", _test_negative_exponent),
    ]
    results = [_check(name, fn) for name, fn in tests]
    passed = results.count("pass")
    print(f"\n{passed}/{len(tests)} tests passing")
    if passed < len(tests):
        print("Keep going: the exercises below need a working FieldElement.")
        return

    print("\n\nExercise 2: Verify field properties for F_31")
    verify_field_properties(31)

    print("\n\nExercise 3: Why must the modulus be prime?")
    demonstrate_composite_failure()

    print("\n\nExercise 4: Bitcoin's actual finite field")
    bitcoin_field_element()


if __name__ == "__main__":
    run_tests()
