"""
Bitcoin Dojo — Week 2 Exercises: Elliptic Curves
Code Orange Dev School | codeorange.dev

Based on Programming Bitcoin by Jimmy Song (Chapters 2-3)
https://github.com/jimmysong/programmingbitcoin

Prerequisites: Complete Week 1 (finite_fields.py) first.

Instructions:
- Complete each exercise by filling in the code where indicated
- Run this file with: python3 elliptic_curves.py
- Discuss your solutions at the weekly Monday 11:00 UTC call
"""

from week_01_solution import FieldElement  # Use your Week 1 solution
# If you haven't completed Week 1, uncomment and use this minimal version:
# class FieldElement:
#     def __init__(self, num, prime):
#         self.num = num % prime; self.prime = prime
#     def __repr__(self): return f"FieldElement_{self.prime}({self.num})"
#     def __eq__(self, other): return self.num == other.num and self.prime == other.prime
#     def __ne__(self, other): return not self.__eq__(other)
#     def __add__(self, o): return FieldElement((self.num + o.num) % self.prime, self.prime)
#     def __sub__(self, o): return FieldElement((self.num - o.num) % self.prime, self.prime)
#     def __mul__(self, o): return FieldElement((self.num * o.num) % self.prime, self.prime)
#     def __pow__(self, e): return FieldElement(pow(self.num, e % (self.prime-1), self.prime), self.prime)
#     def __truediv__(self, o): return self * (o ** (self.prime - 2))


# ============================================================
# Exercise 1: Implement the Point class (over real numbers)
# ============================================================
#
# An elliptic curve has the equation: y^2 = x^3 + ax + b
# A Point is a point on this curve (or the point at infinity).
#
# The point at infinity is represented by x=None, y=None.

class Point:
    """A point on an elliptic curve y^2 = x^3 + ax + b."""

    def __init__(self, x, y, a, b):
        self.a = a
        self.b = b
        self.x = x
        self.y = y

        # Point at infinity (identity element)
        if self.x is None and self.y is None:
            return

        # Verify the point is on the curve
        if self.y ** 2 != self.x ** 3 + a * x + b:
            raise ValueError(f"({x}, {y}) is not on the curve y^2 = x^3 + {a}x + {b}")

    def __repr__(self):
        if self.x is None:
            return "Point(infinity)"
        return f"Point({self.x}, {self.y})_{self.a}_{self.b}"

    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y
                and self.a == other.a and self.b == other.b)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        """Point addition on the elliptic curve.

        There are several cases:
        1. One point is infinity (identity) → return the other
        2. Points have same x but different y → return infinity (vertical line)
        3. Points are different → use the slope formula
        4. Points are the same → use the tangent formula (point doubling)
        5. Point doubling where y=0 → return infinity
        """
        if self.a != other.a or self.b != other.b:
            raise TypeError(f"Points are not on the same curve")

        # Case 1: self is point at infinity
        if self.x is None:
            return other

        # Case 1: other is point at infinity
        if other.x is None:
            return self

        # Case 2: x coordinates are equal but y coordinates are different
        # The line is vertical → result is point at infinity
        if self.x == other.x and self.y != other.y:
            return self.__class__(None, None, self.a, self.b)

        # Case 3: Points are different (x1 != x2)
        # YOUR CODE HERE
        # slope s = (y2 - y1) / (x2 - x1)
        # x3 = s^2 - x1 - x2
        # y3 = s * (x1 - x3) - y1
        if self.x != other.x:
            # s = ...
            # x3 = ...
            # y3 = ...
            # return self.__class__(x3, y3, self.a, self.b)
            pass

        # Case 4: Points are the same (point doubling, self == other)
        # YOUR CODE HERE
        # slope s = (3 * x1^2 + a) / (2 * y1)
        # x3 = s^2 - 2*x1
        # y3 = s * (x1 - x3) - y1
        if self == other:
            # Case 5: tangent is vertical (y = 0)
            if self.y == 0 * self.x:  # handles both int and FieldElement
                return self.__class__(None, None, self.a, self.b)

            # s = ...
            # x3 = ...
            # y3 = ...
            # return self.__class__(x3, y3, self.a, self.b)
            pass


# ============================================================
# Exercise 2: Point addition over real numbers
# ============================================================
#
# Verify point addition works on the curve y^2 = x^3 + 5x + 7

def test_point_addition_reals():
    """Test point addition over real numbers.

    Curve: y^2 = x^3 + 5x + 7

    YOUR TASK: Uncomment and verify these additions work.
    """
    print("Exercise 2: Point addition over real numbers")
    print("Curve: y^2 = x^3 + 5x + 7")

    # These points are on the curve y^2 = x^3 + 5x + 7:
    # Verify: (-1)^2 = (-1)^3 + 5*(-1) + 7 → 1 = -1 - 5 + 7 = 1 ✓
    # Verify: (2)^2 = (-1)^3 + 5*(-1) + 7 → nope, need to find real points

    # For integer testing, use curve y^2 = x^3 - 7x + 10
    # Point (1, 2): 4 = 1 - 7 + 10 = 4 ✓
    # Point (2, 2): 4 = 8 - 14 + 10 = 4 ✓

    # YOUR CODE HERE
    # p1 = Point(1, 2, -7, 10)
    # p2 = Point(2, 2, -7, 10)
    # p3 = p1 + p2
    # print(f"  {p1} + {p2} = {p3}")

    # Test identity element
    # inf = Point(None, None, -7, 10)
    # assert p1 + inf == p1, "Adding infinity should return the same point"
    # print(f"  {p1} + infinity = {p1 + inf} ... PASS")

    pass


# ============================================================
# Exercise 3: Point addition over finite fields
# ============================================================
#
# This is where it gets real! Bitcoin uses elliptic curves over
# finite fields, not over real numbers.

def test_point_addition_finite_field():
    """Test point addition over a finite field.

    Curve: y^2 = x^3 + 7 over F_223 (a=0, b=7, like Bitcoin's secp256k1!)
    """
    print("\nExercise 3: Point addition over finite field F_223")
    print("Curve: y^2 = x^3 + 7 (mod 223)")

    prime = 223
    a = FieldElement(0, prime)
    b = FieldElement(7, prime)

    # Verify that (192, 105) is on the curve:
    # 105^2 mod 223 = 11025 mod 223 = 81
    # 192^3 + 7 mod 223 = 7077881 mod 223 = 81  ✓
    x1 = FieldElement(192, prime)
    y1 = FieldElement(105, prime)
    p1 = Point(x1, y1, a, b)
    print(f"  Point 1: ({x1.num}, {y1.num})")

    # YOUR CODE HERE
    # 1. Verify that (17, 56) is also on the curve
    # x2 = FieldElement(17, prime)
    # y2 = FieldElement(56, prime)
    # p2 = Point(x2, y2, a, b)
    # print(f"  Point 2: ({x2.num}, {y2.num})")

    # 2. Add them together
    # p3 = p1 + p2
    # print(f"  P1 + P2 = ({p3.x.num}, {p3.y.num})")

    # 3. Try point doubling: p1 + p1
    # p4 = p1 + p1
    # print(f"  P1 + P1 = ({p4.x.num}, {p4.y.num})")

    pass


# ============================================================
# Exercise 4: Scalar multiplication and group order
# ============================================================
#
# Scalar multiplication: n * P = P + P + P + ... (n times)
# The order of a point is the smallest n such that n * P = infinity.

def scalar_multiplication():
    """Find the order of a generator point.

    On the curve y^2 = x^3 + 7 over F_223:
    Start with point G = (47, 71)
    Compute 2G, 3G, 4G, ... until you reach infinity.
    The number of steps is the order of G.
    """
    print("\nExercise 4: Scalar multiplication and group order")

    prime = 223
    a = FieldElement(0, prime)
    b = FieldElement(7, prime)

    x = FieldElement(47, prime)
    y = FieldElement(71, prime)
    G = Point(x, y, a, b)
    inf = Point(None, None, a, b)

    # YOUR CODE HERE
    # current = G
    # for n in range(2, 300):
    #     current = current + G
    #     if current.x is not None:
    #         print(f"  {n}G = ({current.x.num}, {current.y.num})")
    #     else:
    #         print(f"  {n}G = infinity  <-- ORDER FOUND: {n}")
    #         break

    # QUESTION: What is the order? Write your answer here:
    # order = ???
    # Discuss: Why does the group have a finite order?
    # Discuss: How does this relate to Bitcoin's n value in secp256k1?

    pass


# ============================================================
# Exercise 5: Towards secp256k1
# ============================================================
#
# Bitcoin's elliptic curve secp256k1 uses:
# - Equation: y^2 = x^3 + 7 (same a=0, b=7 as our exercises!)
# - Prime p = 2^256 - 2^32 - 977
# - Generator point G = (huge_x, huge_y)
# - Order n = a very large prime
#
# The security of Bitcoin depends on the fact that given Q = k*G,
# it is computationally infeasible to find k (the private key)
# even though you know Q (the public key) and G.
# This is the Elliptic Curve Discrete Logarithm Problem (ECDLP).

def secp256k1_intro():
    """Demonstrate that secp256k1 uses the same curve equation as our exercises."""
    print("\nExercise 5: secp256k1 — Bitcoin's elliptic curve")

    P = 2**256 - 2**32 - 977
    print(f"  Prime p = 2^256 - 2^32 - 977")
    print(f"  p = {P}")
    print(f"  p has {len(str(P))} digits")
    print(f"  Curve: y^2 = x^3 + 7 (a=0, b=7) — same as our exercises!")

    # The generator point G (in hex):
    Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
    Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

    print(f"\n  Generator G:")
    print(f"    x = {hex(Gx)}")
    print(f"    y = {hex(Gy)}")

    # Verify G is on the curve: Gy^2 mod P should equal (Gx^3 + 7) mod P
    lhs = pow(Gy, 2, P)
    rhs = (pow(Gx, 3, P) + 7) % P
    assert lhs == rhs, "G is not on the curve!"
    print(f"\n  Verification: Gy^2 mod p == Gx^3 + 7 mod p ... PASSED")
    print(f"  G is on the secp256k1 curve!")

    # The group order:
    N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    print(f"\n  Group order n = {hex(N)}")
    print(f"  This means n*G = infinity (point at infinity)")
    print(f"  Any private key k must satisfy: 1 <= k < n")

    # YOUR CODE HERE
    # QUESTION: If a private key is a random 256-bit number, how many
    # possible private keys are there? (Answer: approximately 2^256 or ~10^77)
    # QUESTION: How does this compare to the number of atoms in the observable
    # universe? (~10^80)


# ============================================================
# Run all exercises
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Bitcoin Dojo — Week 2: Elliptic Curves")
    print("=" * 60)

    test_point_addition_reals()
    test_point_addition_finite_field()
    scalar_multiplication()
    secp256k1_intro()

    print("\n" + "=" * 60)
    print("Week 2 exercises complete!")
    print("Bring your solutions to the Monday 11:00 UTC call.")
    print("=" * 60)
