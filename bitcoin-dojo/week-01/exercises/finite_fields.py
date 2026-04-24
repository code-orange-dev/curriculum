"""
Bitcoin Dojo — Week 1 Exercises: Finite Fields
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
        pass

    def __ne__(self, other):
        """Two field elements are not equal if __eq__ returns False."""
        # YOUR CODE HERE
        pass

    def __add__(self, other):
        """Add two field elements: (a + b) mod p"""
        if self.prime != other.prime:
            raise TypeError("Cannot add two numbers in different Fields")
        # YOUR CODE HERE
        # Hint: (self.num + other.num) % self.prime
        pass

    def __sub__(self, other):
        """Subtract two field elements: (a - b) mod p"""
        if self.prime != other.prime:
            raise TypeError("Cannot subtract two numbers in different Fields")
        # YOUR CODE HERE
        # Hint: (self.num - other.num) % self.prime
        pass

    def __mul__(self, other):
        """Multiply two field elements: (a * b) mod p"""
        if self.prime != other.prime:
            raise TypeError("Cannot multiply two numbers in different Fields")
        # YOUR CODE HERE
        pass

    def __pow__(self, exponent):
        """Raise a field element to a power: (a ** exp) mod p

        Important: use Fermat's Little Theorem to handle negative exponents.
        a^(p-1) = 1 (mod p), so a^(-1) = a^(p-2) (mod p)
        Therefore: a^n = a^(n % (p-1)) (mod p)
        """
        # YOUR CODE HERE
        # Hint: n = exponent % (self.prime - 1)
        #       then use Python's built-in pow(self.num, n, self.prime)
        pass

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
        pass


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
    # assert a + b == b + a
    # print(f"  Commutativity (addition): PASS")

    # 3. Associativity of addition
    # assert (a + b) + c == a + (b + c)

    # 4. Additive identity
    # assert a + zero == a

    # 5. Multiplicative identity
    # assert a * one == a

    # 6. Additive inverse
    # neg_a = FieldElement((prime - a_num) % prime, prime)
    # assert a + neg_a == zero

    # 7. Multiplicative inverse (for non-zero elements)
    # if a_num != 0:
    #     a_inv = a ** (prime - 2)
    #     assert a * a_inv == one

    # Uncomment the above and add print statements

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
    # for a in range(1, modulus):
    #     found_inverse = False
    #     for b in range(1, modulus):
    #         if (a * b) % modulus == 1:
    #             found_inverse = True
    #             break
    #     if not found_inverse:
    #         print(f"  {a} has NO multiplicative inverse mod {modulus}")

    pass


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
    # a = FieldElement(42, P)
    # b = FieldElement(99, P)
    # print(f"  {a} + {b} = {a + b}")
    # print(f"  {a} * {b} = {a * b}")
    # print(f"  {a} / {b} = {a / b}")
    # Verify: (a / b) * b should equal a
    # print(f"  (a / b) * b = {(a / b) * b}")
    # assert (a / b) * b == a, "Division verification failed!"

    pass


# ============================================================
# TESTS — Run these to verify your implementation
# ============================================================

def run_tests():
    print("=" * 60)
    print("Bitcoin Dojo — Week 1: Finite Field Tests")
    print("=" * 60)

    # Test 1: Equality
    print("\nTest 1: Equality")
    a = FieldElement(7, 13)
    b = FieldElement(7, 13)
    c = FieldElement(6, 13)
    assert a == b, "Equal elements should be equal"
    assert a != c, "Different elements should not be equal"
    print("  PASSED")

    # Test 2: Addition
    print("\nTest 2: Addition")
    a = FieldElement(7, 13)
    b = FieldElement(12, 13)
    c = FieldElement(6, 13)  # (7 + 12) % 13 = 6
    assert a + b == c, f"Expected {c}, got {a + b}"
    print(f"  {a} + {b} = {a + b} ... PASSED")

    # Test 3: Subtraction
    print("\nTest 3: Subtraction")
    a = FieldElement(6, 19)
    b = FieldElement(13, 19)
    c = FieldElement(12, 19)  # (6 - 13) % 19 = -7 % 19 = 12
    assert a - b == c, f"Expected {c}, got {a - b}"
    print(f"  {a} - {b} = {a - b} ... PASSED")

    # Test 4: Multiplication
    print("\nTest 4: Multiplication")
    a = FieldElement(3, 13)
    b = FieldElement(12, 13)
    c = FieldElement(10, 13)  # (3 * 12) % 13 = 36 % 13 = 10
    assert a * b == c, f"Expected {c}, got {a * b}"
    print(f"  {a} * {b} = {a * b} ... PASSED")

    # Test 5: Exponentiation
    print("\nTest 5: Exponentiation")
    a = FieldElement(3, 13)
    b = FieldElement(1, 13)  # 3^3 % 13 = 27 % 13 = 1
    assert a ** 3 == b, f"Expected {b}, got {a ** 3}"
    print(f"  {a} ** 3 = {a ** 3} ... PASSED")

    # Test 6: Division
    print("\nTest 6: Division")
    a = FieldElement(2, 19)
    b = FieldElement(7, 19)
    c = FieldElement(3, 19)  # 2/7 = 2 * 7^(19-2) % 19 = 2 * 7^17 % 19 = 3
    assert a / b == c, f"Expected {c}, got {a / b}"
    print(f"  {a} / {b} = {a / b} ... PASSED")

    # Test 7: Negative exponent (Fermat's Little Theorem)
    print("\nTest 7: Negative exponent")
    a = FieldElement(7, 13)
    b = a ** -3  # 7^(-3) mod 13
    # Verify: b * (a**3) should equal 1
    one = FieldElement(1, 13)
    assert b * (a ** 3) == one, "Negative exponent failed"
    print(f"  {a} ** -3 = {b} ... PASSED")

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60)

    # Run additional exercises
    print("\n\nExercise 2: Verify field properties for F_31")
    verify_field_properties(31)

    print("\n\nExercise 3: Why must the modulus be prime?")
    demonstrate_composite_failure()

    print("\n\nExercise 4: Bitcoin's actual finite field")
    bitcoin_field_element()


if __name__ == "__main__":
    run_tests()
