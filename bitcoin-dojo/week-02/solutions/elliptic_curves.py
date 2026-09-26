"""
Bitcoin Dojo — Week 2 REFERENCE SOLUTION: Elliptic Curves
Code Orange Dev School | codeorange.dev

Based on Programming Bitcoin by Jimmy Song (Chapters 2-3)
https://github.com/jimmysong/programmingbitcoin

Prerequisites: Complete Week 1 (finite_fields.py) first.

Instructions:
- Complete each exercise by filling in the code where indicated
- Run this file with: python3 elliptic_curves.py
- Discuss your solutions at the weekly Monday 11:00 UTC call
"""

import importlib.util
from pathlib import Path


def _load_field_element():
    """Use YOUR Week 1 FieldElement if it works; otherwise the reference one."""
    week1 = Path(__file__).resolve().parents[2] / "week-01"
    for label, path in (("your Week 1", week1 / "exercises" / "finite_fields.py"),
                        ("the Week 1 reference solution", week1 / "solutions" / "finite_fields.py")):
        try:
            spec = importlib.util.spec_from_file_location(f"ff_{path.parent.name}", path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            FE = mod.FieldElement
            if FE(3, 7) + FE(5, 7) == FE(1, 7) and FE(2, 7) / FE(4, 7) == FE(4, 7):
                print(f"(using FieldElement from {label})")
                return FE
        except Exception:
            continue
    raise SystemExit("No working FieldElement found - finish week-01/exercises/finite_fields.py first.")


FieldElement = _load_field_element()


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
            s = (other.y - self.y) / (other.x - self.x)
            x3 = s ** 2 - self.x - other.x
            y3 = s * (self.x - x3) - self.y
            return self.__class__(x3, y3, self.a, self.b)

        # Case 4: Points are the same (point doubling, self == other)
        # YOUR CODE HERE
        # slope s = (3 * x1^2 + a) / (2 * y1)
        # x3 = s^2 - 2*x1
        # y3 = s * (x1 - x3) - y1
        if self == other:
            # Case 5: tangent is vertical (y = 0)
            if self.y == 0 * self.x:  # handles both int and FieldElement
                return self.__class__(None, None, self.a, self.b)

            s = (3 * self.x ** 2 + self.a) / (2 * self.y)
            x3 = s ** 2 - 2 * self.x
            y3 = s * (self.x - x3) - self.y
            return self.__class__(x3, y3, self.a, self.b)


# ============================================================
# Exercise 2: Point addition over real numbers
# ============================================================
#
# Verify point addition works on the curve y^2 = x^3 + 5x + 7

def test_point_addition_reals():
    """Test point addition over real numbers.

    Curve: y^2 = x^3 - 7x + 10

    YOUR TASK: Uncomment and verify these additions work.
    """
    print("Exercise 2: Point addition over real numbers")
    print("Curve: y^2 = x^3 - 7x + 10")

    # For integer testing, use curve y^2 = x^3 - 7x + 10
    # Point (1, 2): 4 = 1 - 7 + 10 = 4 ✓
    # Point (2, 2): 4 = 8 - 14 + 10 = 4 ✓

    # YOUR CODE HERE (reference solution below)
    p1 = Point(1, 2, -7, 10)
    p2 = Point(2, 2, -7, 10)
    p3 = p1 + p2
    print(f"  {p1} + {p2} = {p3}")

    # Test identity element
    inf = Point(None, None, -7, 10)
    assert p1 + inf == p1, "Adding infinity should return the same point"
    print(f"  {p1} + infinity = {p1 + inf} ... PASS")



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

    # YOUR CODE HERE (reference solution below)
    # 1. Verify that (17, 56) is also on the curve
    x2 = FieldElement(17, prime)
    y2 = FieldElement(56, prime)
    p2 = Point(x2, y2, a, b)
    print(f"  Point 2: ({x2.num}, {y2.num})")

    # 2. Add them together
    p3 = p1 + p2
    print(f"  P1 + P2 = ({p3.x.num}, {p3.y.num})")

    # 3. Try point doubling: p1 + p1
    p4 = p1 + p1
    print(f"  P1 + P1 = ({p4.x.num}, {p4.y.num})")



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

    # YOUR CODE HERE (reference solution below)
    current = G
    for n in range(2, 300):
        current = current + G
        if current.x is not None:
            print(f"  {n}G = ({current.x.num}, {current.y.num})")
        else:
            print(f"  {n}G = infinity  <-- ORDER FOUND: {n}")
            break

    # QUESTION: What is the order? Write your answer here:
    order = n  # 21 - the group generated by (47, 71) has 21 elements
    # Discuss: Why does the group have a finite order?
    # Discuss: How does this relate to Bitcoin's n value in secp256k1?



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
# Checks - does your Point.__add__ give the textbook answers?
# ============================================================

def _check(name, fn):
    try:
        fn()
        print(f"  ✓  {name}")
        return True
    except (TypeError, AttributeError) as e:
        print(f"  ·  {name}\n        not implemented yet ({e})")
    except AssertionError as e:
        print(f"  ✗  {name}\n        {e}")
    return False


def _pt(x, y, a=0, b=7, prime=223):
    F = lambda n: FieldElement(n % prime, prime)
    return Point(F(x), F(y), F(a), F(b))


def _inf(a=0, b=7, prime=223):
    return Point(None, None, FieldElement(a, prime), FieldElement(b, prime))


def _checks():
    def reals_add():
        r = Point(2, 5, 5, 7) + Point(-1, -1, 5, 7)
        assert r == Point(3, -7, 5, 7), f"(2,5)+(-1,-1) on y^2=x^3+5x+7 should be (3,-7), got {r}"

    def reals_double():
        r = Point(-1, -1, 5, 7) + Point(-1, -1, 5, 7)
        assert r == Point(18, 77, 5, 7), f"2*(-1,-1) on y^2=x^3+5x+7 should be (18,77), got {r}"

    def identity():
        p = _pt(192, 105)
        assert p + _inf() == p and _inf() + p == p, "P + infinity should be P"

    def inverse():
        assert _pt(192, 105) + _pt(192, -105) == _inf(), "P + (-P) should be infinity"

    def field_add():
        r = _pt(192, 105) + _pt(17, 56)
        assert r == _pt(170, 142), f"(192,105)+(17,56) over F_223 should be (170,142), got {r}"

    def field_double():
        r = _pt(47, 71) + _pt(47, 71)
        assert r == _pt(36, 111), f"2*(47,71) over F_223 should be (36,111), got {r}"

    def group_order():
        G, cur, n = _pt(47, 71), _pt(47, 71), 1
        while cur != _inf():
            cur, n = cur + G, n + 1
            assert n < 300, "never reached infinity"
        assert n == 21, f"order of (47,71) should be 21, got {n}"

    results = [_check(n, f) for n, f in (
        ("Real numbers: P1 + P2", reals_add),
        ("Real numbers: point doubling", reals_double),
        ("Identity: P + infinity", identity),
        ("Inverse: P + (-P) = infinity", inverse),
        ("F_223: P1 + P2", field_add),
        ("F_223: point doubling", field_double),
        ("F_223: order of (47, 71)", group_order),
    )]
    print(f"\n{sum(results)}/{len(results)} checks passing\n")
    return all(results)


# ============================================================
# Run all exercises
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Bitcoin Dojo — Week 2: Elliptic Curves")
    print("=" * 60)
    if not _checks():
        raise SystemExit("Finish Point.__add__ (Exercise 1), then the walkthroughs below will run.")

    test_point_addition_reals()
    test_point_addition_finite_field()
    scalar_multiplication()
    secp256k1_intro()

    print("\n" + "=" * 60)
    print("Week 2 exercises complete!")
    print("Bring your solutions to the Monday 11:00 UTC call.")
    print("=" * 60)
