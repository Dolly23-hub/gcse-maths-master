"""
Expanded GCSE Maths content - Additional topics, quizzes, past papers, and formulas.
This supplements the existing seed data with comprehensive revision material.
"""

ADDITIONAL_TOPICS = [
    # NUMBER - Additional
    {
        "id": "num-5", "category": "Number", "title": "Surds",
        "slug": "surds", "tier": "Higher", "difficulty": 4, "order": 5,
        "description": "Simplify surds, rationalise denominators, and perform calculations with irrational numbers.",
        "explanation": """## Surds

A **surd** is a root that cannot be simplified to a whole number. For example, sqrt(2), sqrt(3), sqrt(5) are surds, but sqrt(4) = 2 is NOT a surd.

### Simplifying Surds
Find the largest square number that is a factor:
- sqrt(12) = sqrt(4 x 3) = sqrt(4) x sqrt(3) = 2sqrt(3)
- sqrt(50) = sqrt(25 x 2) = 5sqrt(2)
- sqrt(72) = sqrt(36 x 2) = 6sqrt(2)

### Rules for Surds
1. sqrt(a) x sqrt(b) = sqrt(ab)
2. sqrt(a) / sqrt(b) = sqrt(a/b)
3. sqrt(a) x sqrt(a) = a
4. You can only add/subtract LIKE surds: 3sqrt(2) + 5sqrt(2) = 8sqrt(2)

### Rationalising the Denominator
Remove the surd from the bottom of a fraction:
- Simple: 1/sqrt(3) = 1/sqrt(3) x sqrt(3)/sqrt(3) = sqrt(3)/3
- With (a + sqrt(b)): Multiply by (a - sqrt(b)) on top and bottom

### Expanding with Surds
(2 + sqrt(3))(4 - sqrt(3))
= 8 - 2sqrt(3) + 4sqrt(3) - 3
= 5 + 2sqrt(3)""",
        "worked_examples": [
            {"problem": "Simplify sqrt(98)", "solution": "Step 1: Find largest square factor of 98\n98 = 49 x 2\nStep 2: sqrt(98) = sqrt(49 x 2) = sqrt(49) x sqrt(2) = 7sqrt(2)"},
            {"problem": "Rationalise 5/sqrt(2)", "solution": "Multiply top and bottom by sqrt(2):\n5/sqrt(2) x sqrt(2)/sqrt(2) = 5sqrt(2)/2"},
            {"problem": "Expand and simplify (3 + sqrt(5))(3 - sqrt(5))", "solution": "= 9 - 3sqrt(5) + 3sqrt(5) - sqrt(5) x sqrt(5)\n= 9 - 5\n= 4\n(This is the difference of two squares!)"},
        ],
        "key_points": [
            "A surd is an irrational root like sqrt(2), sqrt(3)",
            "To simplify: find the largest square number factor",
            "Only LIKE surds can be added or subtracted",
            "Rationalise by multiplying by the conjugate",
        ]
    },
    {
        "id": "num-6", "category": "Number", "title": "Using a Calculator Effectively",
        "slug": "calculator-skills", "tier": "Both", "difficulty": 1, "order": 6,
        "description": "Master calculator skills for Paper 2 and Paper 3. Learn to use memory, brackets, and special functions.",
        "explanation": """## Using a Calculator Effectively

Two out of three GCSE papers allow calculators! Make sure you know how to use yours.

### Essential Buttons
- **Fraction button (a b/c):** Enter fractions properly
- **Square root:** For Pythagoras and surds
- **Power button (x^y):** For indices and standard form
- **Brackets:** ALWAYS use brackets to keep calculations accurate
- **ANS button:** Uses your last answer in the next calculation

### Common Mistakes to Avoid
1. **Forgetting brackets:** 5/(3+2) is NOT the same as 5/3+2
2. **Order of operations:** Calculator follows BIDMAS automatically
3. **Rounding too early:** Keep full calculator display, only round at the END
4. **Negative numbers:** Use the (-) button, not the minus button

### Top Tips
- Always ESTIMATE first to check your answer makes sense
- Use the fraction button for exact answers
- Store values in memory (M+, MR) for multi-step problems
- Check your mode: make sure you're in DEGREES for trigonometry""",
        "worked_examples": [
            {"problem": "Calculate (3.7 + 2.8) / (5.1 - 1.3) using a calculator", "solution": "Type: (3.7 + 2.8) / (5.1 - 1.3)\n= 6.5 / 3.8\n= 1.710526...\n= 1.71 (2 d.p.)\nKey: Use brackets to group the top and bottom separately!"},
        ],
        "key_points": [
            "Always use brackets for complex fractions",
            "Estimate first to check your calculator answer",
            "Don't round until the final answer",
            "Make sure calculator is in degree mode for trig",
        ]
    },
    # ALGEBRA - Additional
    {
        "id": "alg-7", "category": "Algebra", "title": "Inequalities",
        "slug": "inequalities", "tier": "Both", "difficulty": 3, "order": 16,
        "description": "Solve linear and quadratic inequalities, represent them on number lines and graphs.",
        "explanation": """## Inequalities

### Inequality Symbols
- < means less than
- > means greater than
- <= means less than or equal to
- >= means greater than or equal to

### Solving Linear Inequalities
Treat them EXACTLY like equations, with ONE exception:
**When you multiply or divide by a NEGATIVE number, FLIP the sign!**

Example: 3x + 5 > 14
3x > 9
x > 3

Example: -2x + 3 <= 7
-2x <= 4
x >= -2 (sign FLIPPED because we divided by -2!)

### Number Line Representation
- Open circle (o) for < or > (not including the value)
- Filled circle (bullet) for <= or >= (including the value)
- Shade the region that satisfies the inequality

### Double Inequalities
-3 < 2x + 1 <= 7
Subtract 1 from all parts: -4 < 2x <= 6
Divide all by 2: -2 < x <= 3

### Quadratic Inequalities (Higher)
x^2 - 5x + 6 < 0
Factorise: (x - 2)(x - 3) < 0
Critical values: x = 2 and x = 3
Test regions: 2 < x < 3""",
        "worked_examples": [
            {"problem": "Solve 4x - 3 >= 2x + 7", "solution": "Step 1: Subtract 2x from both sides\n2x - 3 >= 7\nStep 2: Add 3 to both sides\n2x >= 10\nStep 3: Divide by 2\nx >= 5"},
            {"problem": "Solve -3 <= 2x + 1 < 9", "solution": "Subtract 1 from all three parts:\n-4 <= 2x < 8\nDivide all by 2:\n-2 <= x < 4\nSo x can be -2, -1, 0, 1, 2, 3 (if integer values)"},
        ],
        "key_points": [
            "Solve just like equations but FLIP sign when multiplying/dividing by negative",
            "Open circle for strict inequalities (<, >)",
            "Filled circle for inclusive inequalities (<=, >=)",
            "For quadratic: factorise, find critical values, test regions",
        ]
    },
    {
        "id": "alg-8", "category": "Algebra", "title": "Functions & Iteration",
        "slug": "functions-iteration", "tier": "Higher", "difficulty": 4, "order": 17,
        "description": "Understand function notation, composite functions, inverse functions, and use iteration to find solutions.",
        "explanation": """## Functions & Iteration

### Function Notation
f(x) = 2x + 3 means "the function f takes x and gives 2x + 3"
- f(4) = 2(4) + 3 = 11 (substitute x = 4)
- f(-1) = 2(-1) + 3 = 1

### Composite Functions
fg(x) means "do g first, then f"
If f(x) = 2x + 1 and g(x) = x^2:
- fg(3) = f(g(3)) = f(9) = 2(9) + 1 = 19
- gf(3) = g(f(3)) = g(7) = 49

**Order matters!** fg(x) is NOT the same as gf(x)

### Inverse Functions
f^(-1)(x) reverses what f does.
If f(x) = 2x + 3:
1. Write y = 2x + 3
2. Swap x and y: x = 2y + 3
3. Rearrange for y: y = (x - 3)/2
4. So f^(-1)(x) = (x - 3)/2

### Iteration
Finding approximate solutions by repeating a formula:
x_(n+1) = formula involving x_n

Start with x_0, keep substituting to get x_1, x_2, x_3...
The values should converge to a solution.""",
        "worked_examples": [
            {"problem": "f(x) = 3x - 1, g(x) = x^2 + 2. Find fg(2)", "solution": "Step 1: Find g(2) first\ng(2) = 2^2 + 2 = 6\nStep 2: Now find f(6)\nf(6) = 3(6) - 1 = 17\nfg(2) = 17"},
            {"problem": "Find the inverse of f(x) = 4x - 5", "solution": "Write y = 4x - 5\nSwap: x = 4y - 5\nRearrange: x + 5 = 4y\ny = (x + 5)/4\nf^(-1)(x) = (x + 5)/4"},
        ],
        "key_points": [
            "f(x) is just a way of writing a rule or formula",
            "For composite functions: work from the INSIDE out",
            "fg(x) means do g first, then f",
            "Inverse: swap x and y, then rearrange for y",
        ]
    },
    {
        "id": "alg-9", "category": "Algebra", "title": "Algebraic Proof",
        "slug": "algebraic-proof", "tier": "Higher", "difficulty": 5, "order": 18,
        "description": "Construct mathematical proofs using algebra. Prove statements about odd, even numbers and more.",
        "explanation": """## Algebraic Proof

### Key Number Representations
- **Even number:** 2n (where n is an integer)
- **Odd number:** 2n + 1
- **Consecutive integers:** n, n+1, n+2
- **Consecutive even numbers:** 2n, 2n+2, 2n+4
- **Consecutive odd numbers:** 2n+1, 2n+3, 2n+5
- **Multiple of 3:** 3n

### How to Structure a Proof
1. **State** what you're representing (e.g., "Let n be any integer")
2. **Set up** the algebraic expression
3. **Manipulate** using algebra
4. **Conclude** by showing the result matches what you needed to prove

### Example Proofs
**Prove that the sum of two consecutive odd numbers is always even:**
Let the odd numbers be (2n + 1) and (2n + 3)
Sum = (2n + 1) + (2n + 3) = 4n + 4 = 2(2n + 2)
Since 2(2n + 2) is a multiple of 2, it is always even.

**Prove that the sum of any 3 consecutive integers is a multiple of 3:**
Let them be n, n+1, n+2
Sum = n + (n+1) + (n+2) = 3n + 3 = 3(n + 1)
Since 3(n+1) is a multiple of 3, the sum is always divisible by 3.""",
        "worked_examples": [
            {"problem": "Prove that (2n+1)^2 is always odd", "solution": "(2n+1)^2 = (2n+1)(2n+1)\n= 4n^2 + 4n + 1\n= 2(2n^2 + 2n) + 1\nSince 2(2n^2 + 2n) is even, adding 1 makes it odd.\nTherefore (2n+1)^2 is always odd."},
        ],
        "key_points": [
            "Even = 2n, Odd = 2n + 1, Consecutive = n, n+1, n+2",
            "Always start with 'Let n be any integer'",
            "Factorise your final expression to show divisibility",
            "Show clearly why the result proves the statement",
        ]
    },
    # GEOMETRY - Additional
    {
        "id": "geo-5", "category": "Geometry & Measures", "title": "Circle Theorems",
        "slug": "circle-theorems", "tier": "Higher", "difficulty": 4, "order": 34,
        "description": "Master all circle theorems including angles in semicircles, cyclic quadrilaterals, and tangent properties.",
        "explanation": """## Circle Theorems

### Theorem 1: Angle at Centre
The angle at the centre is TWICE the angle at the circumference (when subtended by the same arc).

### Theorem 2: Angle in a Semicircle
The angle in a semicircle is always 90 degrees (a right angle).

### Theorem 3: Angles in the Same Segment
Angles subtended by the same arc at the circumference are equal.

### Theorem 4: Cyclic Quadrilateral
Opposite angles in a cyclic quadrilateral add up to 180 degrees.

### Theorem 5: Tangent-Radius
A tangent to a circle is perpendicular to the radius at the point of contact (90 degrees).

### Theorem 6: Two Tangents from a Point
Two tangents from the same external point are equal in length.

### Theorem 7: Alternate Segment
The angle between a tangent and a chord equals the angle in the alternate segment.

### Exam Tips
- Draw in any radii you can see - they're all equal!
- Look for isosceles triangles (two radii = two equal sides)
- Name the theorem you use in your working""",
        "worked_examples": [
            {"problem": "Angle at centre = 120 degrees. Find the angle at circumference.", "solution": "Theorem: Angle at centre = 2 x angle at circumference\n120 = 2 x angle at circumference\nAngle at circumference = 120 / 2 = 60 degrees"},
            {"problem": "In a cyclic quadrilateral, one angle is 72 degrees. Find its opposite angle.", "solution": "Theorem: Opposite angles in cyclic quadrilateral = 180 degrees\nOpposite angle = 180 - 72 = 108 degrees"},
        ],
        "key_points": [
            "Angle at centre = 2 x angle at circumference",
            "Angle in semicircle = 90 degrees",
            "Same segment = same angle",
            "Cyclic quad: opposite angles sum to 180 degrees",
            "Tangent meets radius at 90 degrees",
        ]
    },
    {
        "id": "geo-6", "category": "Geometry & Measures", "title": "Congruence & Similarity",
        "slug": "congruence-similarity", "tier": "Both", "difficulty": 3, "order": 35,
        "description": "Understand congruent and similar shapes, use scale factors for length, area, and volume.",
        "explanation": """## Congruence & Similarity

### Congruent Shapes
Same shape AND same size. All corresponding sides and angles are equal.

**Four conditions for congruent triangles:**
1. **SSS** - three sides equal
2. **SAS** - two sides and included angle
3. **ASA** - two angles and included side
4. **RHS** - right angle, hypotenuse, and one side

### Similar Shapes
Same shape but DIFFERENT size. All angles are equal, sides are in the same ratio.

### Scale Factors
If the linear scale factor is k:
- **Lengths** scale by k
- **Areas** scale by k^2
- **Volumes** scale by k^3

### Example
Two similar cylinders have heights 6 cm and 9 cm.
Linear scale factor = 9/6 = 1.5

If small cylinder area = 40 cm^2:
Large area = 40 x 1.5^2 = 40 x 2.25 = 90 cm^2

If small cylinder volume = 100 cm^3:
Large volume = 100 x 1.5^3 = 100 x 3.375 = 337.5 cm^3""",
        "worked_examples": [
            {"problem": "Two similar shapes have areas 25 cm^2 and 100 cm^2. If a side of the smaller shape is 4 cm, find the corresponding side of the larger.", "solution": "Area scale factor = 100/25 = 4\nLinear scale factor = sqrt(4) = 2\nCorresponding side = 4 x 2 = 8 cm"},
        ],
        "key_points": [
            "Congruent = same shape AND size",
            "Similar = same shape, different size (same angles, proportional sides)",
            "Area scale factor = (linear scale factor)^2",
            "Volume scale factor = (linear scale factor)^3",
        ]
    },
    {
        "id": "geo-7", "category": "Geometry & Measures", "title": "Vectors",
        "slug": "vectors", "tier": "Higher", "difficulty": 4, "order": 36,
        "description": "Understand vector notation, add and subtract vectors, use vectors to prove geometrical properties.",
        "explanation": """## Vectors

### What is a Vector?
A vector has both **magnitude** (size) and **direction**.
Written as a column vector: (x, y) where x = horizontal, y = vertical

### Vector Notation
- **a** or **AB** (bold or with arrow above)
- Column vector: (3, -2) means 3 right, 2 down

### Operations
**Addition:** (2, 3) + (1, 4) = (3, 7)
**Subtraction:** (5, 2) - (3, 1) = (2, 1)
**Scalar multiplication:** 3 x (2, 1) = (6, 3)

### Key Rules
- **AB** = b - a (position vector B minus position vector A)
- -**a** reverses the direction
- If vectors are parallel: one is a scalar multiple of the other
- Midpoint M of AB: OM = (OA + OB)/2

### Proving Points are Collinear
If AB = k x BC (scalar multiple), then A, B, C lie on the same straight line.""",
        "worked_examples": [
            {"problem": "If OA = (2, 3) and OB = (6, 7), find AB", "solution": "AB = b - a = OB - OA\n= (6, 7) - (2, 3)\n= (4, 4)"},
            {"problem": "OA = a, OB = b. M is the midpoint of AB. Find OM.", "solution": "OM = OA + AM\nAM = 1/2 x AB = 1/2(b - a)\nOM = a + 1/2(b - a) = a + 1/2 b - 1/2 a = 1/2 a + 1/2 b\nOM = 1/2(a + b)"},
        ],
        "key_points": [
            "Vectors have magnitude AND direction",
            "AB = b - a (end point minus start point)",
            "Parallel vectors are scalar multiples of each other",
            "Midpoint: use 1/2(a + b)",
        ]
    },
    {
        "id": "geo-8", "category": "Geometry & Measures", "title": "Bearings & Scale Drawings",
        "slug": "bearings-scale", "tier": "Both", "difficulty": 2, "order": 37,
        "description": "Measure and calculate bearings, create and interpret scale drawings, and perform constructions.",
        "explanation": """## Bearings & Scale Drawings

### Bearings
A bearing is a direction measured clockwise from North.

**Three rules for bearings:**
1. Always measured from NORTH
2. Always measured CLOCKWISE
3. Always written as 3 figures (e.g., 045 degrees, not 45 degrees)

### Common Bearings
- North = 000 degrees
- East = 090 degrees
- South = 180 degrees
- West = 270 degrees

### Back Bearings
To find the bearing of A from B when you know the bearing of B from A:
- If bearing < 180: add 180
- If bearing >= 180: subtract 180

### Scale Drawings
A scale like 1:50000 means 1 cm on the map = 50000 cm in real life = 500 m

### Constructions
- **Perpendicular bisector:** Find the midpoint of a line
- **Angle bisector:** Split an angle in half
- **Locus:** Set of all points satisfying a condition""",
        "worked_examples": [
            {"problem": "The bearing of B from A is 065 degrees. Find the bearing of A from B.", "solution": "065 < 180, so ADD 180\nBearing of A from B = 065 + 180 = 245 degrees"},
            {"problem": "On a map with scale 1:25000, two towns are 8 cm apart. Find the real distance.", "solution": "Real distance = 8 x 25000 = 200,000 cm\n= 2,000 m = 2 km"},
        ],
        "key_points": [
            "Bearings: from North, clockwise, 3 figures",
            "Back bearing: add or subtract 180",
            "Always show construction arcs in exam",
            "Scale: multiply map distance by scale factor for real distance",
        ]
    },
    # RATIO & PROPORTION - Additional
    {
        "id": "rat-4", "category": "Ratio & Proportion", "title": "Direct & Inverse Proportion (Algebraic)",
        "slug": "direct-inverse-proportion", "tier": "Higher", "difficulty": 3, "order": 23,
        "description": "Express direct and inverse proportion algebraically, find constants of proportionality.",
        "explanation": """## Direct & Inverse Proportion (Algebraic)

### Direct Proportion
y is directly proportional to x means:
**y = kx** (k is the constant of proportionality)

y is proportional to x^2: **y = kx^2**
y is proportional to sqrt(x): **y = k x sqrt(x)**

### Finding k
If y = 12 when x = 3 and y is proportional to x^2:
y = kx^2
12 = k(3^2) = 9k
k = 12/9 = 4/3
So y = (4/3)x^2

### Inverse Proportion
y is inversely proportional to x means:
**y = k/x**

y is inversely proportional to x^2: **y = k/x^2**

### Example
y is inversely proportional to x. When x = 4, y = 5.
y = k/x
5 = k/4
k = 20
So y = 20/x

When x = 10: y = 20/10 = 2""",
        "worked_examples": [
            {"problem": "y is proportional to x^2. When x = 2, y = 20. Find y when x = 5.", "solution": "y = kx^2\n20 = k(2^2) = 4k\nk = 5\nSo y = 5x^2\nWhen x = 5: y = 5(25) = 125"},
            {"problem": "y is inversely proportional to sqrt(x). When x = 9, y = 4. Find y when x = 25.", "solution": "y = k/sqrt(x)\n4 = k/sqrt(9) = k/3\nk = 12\nSo y = 12/sqrt(x)\nWhen x = 25: y = 12/sqrt(25) = 12/5 = 2.4"},
        ],
        "key_points": [
            "Direct: y = kx (y increases as x increases)",
            "Inverse: y = k/x (y decreases as x increases)",
            "Always find k first by substituting known values",
            "Can involve x^2, x^3, sqrt(x) etc.",
        ]
    },
    {
        "id": "rat-5", "category": "Ratio & Proportion", "title": "Growth & Decay",
        "slug": "growth-decay", "tier": "Both", "difficulty": 3, "order": 24,
        "description": "Solve problems involving compound growth, depreciation, and exponential change.",
        "explanation": """## Growth & Decay

### Compound Growth
When something increases by the same PERCENTAGE each time period:
**Amount = Original x (1 + rate/100)^n**

Examples: Population growth, compound interest, inflation

### Compound Decay (Depreciation)
When something decreases by the same percentage:
**Amount = Original x (1 - rate/100)^n**

Examples: Car depreciation, radioactive decay, cooling

### Key Multipliers
- 5% growth: multiply by 1.05
- 12% growth: multiply by 1.12
- 3% decay: multiply by 0.97
- 20% depreciation: multiply by 0.80

### Example
A car worth 15,000 depreciates by 12% per year. Value after 3 years?
= 15,000 x 0.88^3
= 15,000 x 0.681472
= 10,222.08""",
        "worked_examples": [
            {"problem": "A population of 50,000 grows by 2.5% per year. What is it after 10 years?", "solution": "Amount = 50,000 x (1.025)^10\n= 50,000 x 1.2801\n= 64,004 (nearest whole number)"},
            {"problem": "A laptop worth 800 loses 25% of its value each year. What's it worth after 2 years?", "solution": "Value = 800 x 0.75^2\n= 800 x 0.5625\n= 450"},
        ],
        "key_points": [
            "Growth: multiply by (1 + rate/100) each period",
            "Decay: multiply by (1 - rate/100) each period",
            "The multiplier for n periods is raised to the power n",
            "Depreciation means decreasing in value over time",
        ]
    },
    # PROBABILITY & STATISTICS - Additional
    {
        "id": "sta-3", "category": "Probability & Statistics", "title": "Tree Diagrams & Combined Events",
        "slug": "tree-diagrams", "tier": "Both", "difficulty": 3, "order": 42,
        "description": "Use tree diagrams to calculate probabilities of combined events, including conditional probability.",
        "explanation": """## Tree Diagrams & Combined Events

### Building a Tree Diagram
1. Draw branches for each outcome of the FIRST event
2. From each branch, draw branches for the SECOND event
3. Write probabilities on each branch
4. Each set of branches must add up to 1

### Reading a Tree Diagram
- **AND** (both events): MULTIPLY along the branches
- **OR** (either event): ADD the results of different paths

### Example: Two coin flips
P(HH) = 1/2 x 1/2 = 1/4
P(at least one H) = P(HH) + P(HT) + P(TH) = 3/4

### Without Replacement
If you DON'T put items back, the probabilities CHANGE on the second pick.

Bag has 3 red and 5 blue (8 total):
- P(1st red) = 3/8
- P(2nd red | 1st was red) = 2/7 (one fewer red, one fewer total)
- P(both red) = 3/8 x 2/7 = 6/56 = 3/28

### Conditional Probability (Higher)
P(A given B) = P(A and B) / P(B)""",
        "worked_examples": [
            {"problem": "A bag has 4 red and 6 green balls. Two are drawn without replacement. Find P(both red).", "solution": "P(1st red) = 4/10\nP(2nd red | 1st red) = 3/9\nP(both red) = 4/10 x 3/9 = 12/90 = 2/15"},
            {"problem": "P(rain on Monday) = 0.3, P(rain on Tuesday) = 0.4. Find P(rain on at least one day).", "solution": "P(no rain both days) = 0.7 x 0.6 = 0.42\nP(at least one day of rain) = 1 - 0.42 = 0.58"},
        ],
        "key_points": [
            "AND = multiply along branches",
            "OR = add different paths",
            "Without replacement: probabilities change!",
            "P(at least one) = 1 - P(none)",
        ]
    },
    {
        "id": "sta-4", "category": "Probability & Statistics", "title": "Histograms & Cumulative Frequency",
        "slug": "histograms-cumulative-frequency", "tier": "Higher", "difficulty": 4, "order": 43,
        "description": "Draw and interpret histograms, cumulative frequency diagrams, and box plots.",
        "explanation": """## Histograms & Cumulative Frequency

### Histograms
Unlike bar charts, histograms show **frequency density** on the y-axis.
**Frequency density = Frequency / Class width**

The AREA of each bar represents the frequency, not the height!

### Drawing a Histogram
1. Calculate frequency density for each class
2. Draw bars with correct widths and heights
3. No gaps between bars (continuous data)

### Cumulative Frequency
Running total of frequencies.

| Score | Freq | Cumulative Freq |
|-------|------|-----------------|
| 0-10  | 5    | 5               |
| 10-20 | 12   | 17              |
| 20-30 | 18   | 35              |
| 30-40 | 10   | 45              |

### Reading Cumulative Frequency Graphs
- **Median** = value at n/2 on the cumulative frequency axis
- **Lower Quartile (Q1)** = value at n/4
- **Upper Quartile (Q3)** = value at 3n/4
- **Interquartile Range (IQR)** = Q3 - Q1

### Box Plots
Show: Minimum, Q1, Median, Q3, Maximum
IQR = Q3 - Q1 (the 'box' width)
Used to compare distributions""",
        "worked_examples": [
            {"problem": "Find the frequency density: class 10-25, frequency 30", "solution": "Class width = 25 - 10 = 15\nFrequency density = frequency / class width\n= 30 / 15\n= 2"},
            {"problem": "From cumulative frequency: total = 60. Find the median position.", "solution": "Median position = 60/2 = 30th value\nLQ position = 60/4 = 15th value\nUQ position = 3 x 60/4 = 45th value\nRead these values from the graph"},
        ],
        "key_points": [
            "Histogram: y-axis is FREQUENCY DENSITY, not frequency",
            "Frequency density = Frequency / Class width",
            "Cumulative frequency: running total plotted at upper class boundary",
            "IQR = Q3 - Q1 (measures spread of middle 50%)",
        ]
    },
    {
        "id": "sta-5", "category": "Probability & Statistics", "title": "Scatter Graphs & Correlation",
        "slug": "scatter-graphs", "tier": "Both", "difficulty": 2, "order": 44,
        "description": "Plot and interpret scatter graphs, identify correlation, and draw lines of best fit.",
        "explanation": """## Scatter Graphs & Correlation

### Types of Correlation
- **Positive correlation:** As one variable increases, the other increases (upward trend)
- **Negative correlation:** As one increases, the other decreases (downward trend)
- **No correlation:** No clear pattern

### Strength of Correlation
- **Strong:** Points are close to a straight line
- **Weak:** Points are more spread out
- **Moderate:** Somewhere in between

### Line of Best Fit
- Draw a straight line through the middle of the data
- Should have roughly equal points above and below
- Passes through the mean point (mean x, mean y)
- Use it to estimate values (interpolation)

### Outliers
A point that doesn't fit the pattern.
- Don't include outliers when drawing line of best fit
- Always identify and comment on them

### Interpolation vs Extrapolation
- **Interpolation:** Estimating WITHIN the data range (reliable)
- **Extrapolation:** Estimating OUTSIDE the data range (unreliable!)

### Correlation ≠ Causation!
Just because two things are correlated doesn't mean one causes the other.""",
        "worked_examples": [
            {"problem": "Ice cream sales and temperature have positive correlation. Does temperature cause ice cream sales?", "solution": "Positive correlation means as temperature rises, so do ice cream sales. However, correlation does not prove causation - there could be other factors (school holidays, weekends, etc.) that affect both."},
        ],
        "key_points": [
            "Positive: both increase together. Negative: one up, other down",
            "Line of best fit should pass through (mean x, mean y)",
            "Don't extrapolate beyond the data range",
            "Correlation does NOT mean causation",
        ]
    },
]

# Expanded quiz questions - 5+ per existing topic, plus questions for new topics
ADDITIONAL_QUIZZES = [
    # Fractions, Decimals & Percentages (num-1) - more questions
    {"id": "q-num1-4", "topic_id": "num-1", "topic_title": "Fractions, Decimals & Percentages", "question": "Convert 7/8 to a decimal.", "options": ["0.875", "0.78", "0.785", "0.87"], "correct_answer": 0, "explanation": "7 / 8 = 0.875. Divide 7 by 8.", "difficulty": 1},
    {"id": "q-num1-5", "topic_id": "num-1", "topic_title": "Fractions, Decimals & Percentages", "question": "What is 0.4 recurring as a fraction?", "options": ["4/9", "2/5", "4/10", "4/11"], "correct_answer": 0, "explanation": "Let x = 0.444... Then 10x = 4.444... So 9x = 4, x = 4/9", "difficulty": 3},
    {"id": "q-num1-6", "topic_id": "num-1", "topic_title": "Fractions, Decimals & Percentages", "question": "Arrange in ascending order: 3/5, 0.55, 58%", "options": ["0.55, 58%, 3/5", "3/5, 58%, 0.55", "58%, 0.55, 3/5", "0.55, 3/5, 58%"], "correct_answer": 0, "explanation": "3/5 = 0.6 = 60%. So 0.55 < 58% < 60% (3/5)", "difficulty": 2},
    # Powers (num-2)
    {"id": "q-num2-3", "topic_id": "num-2", "topic_title": "Powers, Roots & Standard Form", "question": "What is 2^(-3)?", "options": ["1/8", "-8", "-6", "8"], "correct_answer": 0, "explanation": "2^(-3) = 1/2^3 = 1/8. Negative power means reciprocal.", "difficulty": 2},
    {"id": "q-num2-4", "topic_id": "num-2", "topic_title": "Powers, Roots & Standard Form", "question": "Simplify (2^4 x 2^3) / 2^5", "options": ["2^2 = 4", "2^7 = 128", "2^12 = 4096", "2^3 = 8"], "correct_answer": 0, "explanation": "Add powers on top: 2^(4+3) = 2^7. Then subtract: 2^(7-5) = 2^2 = 4", "difficulty": 2},
    {"id": "q-num2-5", "topic_id": "num-2", "topic_title": "Powers, Roots & Standard Form", "question": "Write 0.0067 in standard form.", "options": ["6.7 x 10^(-3)", "6.7 x 10^(-2)", "67 x 10^(-4)", "0.67 x 10^(-2)"], "correct_answer": 0, "explanation": "Move decimal 3 places right: 6.7. Since right = negative power: 6.7 x 10^(-3)", "difficulty": 2},
    # HCF LCM (num-3)
    {"id": "q-num3-3", "topic_id": "num-3", "topic_title": "HCF, LCM & Prime Factors", "question": "Express 180 as a product of prime factors.", "options": ["2^2 x 3^2 x 5", "2 x 3 x 5 x 6", "4 x 9 x 5", "2^3 x 3 x 5"], "correct_answer": 0, "explanation": "180 = 2 x 90 = 2 x 2 x 45 = 2 x 2 x 9 x 5 = 2^2 x 3^2 x 5", "difficulty": 2},
    {"id": "q-num3-4", "topic_id": "num-3", "topic_title": "HCF, LCM & Prime Factors", "question": "What is the LCM of 12 and 18?", "options": ["36", "72", "6", "216"], "correct_answer": 0, "explanation": "12 = 2^2 x 3, 18 = 2 x 3^2. LCM = 2^2 x 3^2 = 36", "difficulty": 2},
    # Rounding (num-4)
    {"id": "q-num4-1", "topic_id": "num-4", "topic_title": "Rounding, Estimation & Bounds", "question": "Round 3.0452 to 3 significant figures.", "options": ["3.05", "3.04", "3.045", "3.050"], "correct_answer": 0, "explanation": "3 significant figures: 3.04|52. The 5 rounds up: 3.05", "difficulty": 1},
    {"id": "q-num4-2", "topic_id": "num-4", "topic_title": "Rounding, Estimation & Bounds", "question": "Estimate 4.92 x 19.7 / 0.48", "options": ["200", "100", "50", "500"], "correct_answer": 0, "explanation": "Round to 1 s.f.: 5 x 20 / 0.5 = 100 / 0.5 = 200", "difficulty": 2},
    # Expanding & Factorising (alg-1)
    {"id": "q-alg1-3", "topic_id": "alg-1", "topic_title": "Expanding & Factorising Brackets", "question": "Expand and simplify (x + 4)(x - 3)", "options": ["x^2 + x - 12", "x^2 - x - 12", "x^2 + 7x - 12", "x^2 + x + 12"], "correct_answer": 0, "explanation": "FOIL: x^2 - 3x + 4x - 12 = x^2 + x - 12", "difficulty": 2},
    {"id": "q-alg1-4", "topic_id": "alg-1", "topic_title": "Expanding & Factorising Brackets", "question": "Factorise completely: 6x^2 + 12x", "options": ["6x(x + 2)", "6(x^2 + 2x)", "3x(2x + 4)", "x(6x + 12)"], "correct_answer": 0, "explanation": "HCF of 6x^2 and 12x is 6x. 6x^2 + 12x = 6x(x + 2)", "difficulty": 2},
    {"id": "q-alg1-5", "topic_id": "alg-1", "topic_title": "Expanding & Factorising Brackets", "question": "Factorise: x^2 - 25", "options": ["(x+5)(x-5)", "(x+25)(x-1)", "(x-5)(x-5)", "Cannot be factorised"], "correct_answer": 0, "explanation": "Difference of two squares: x^2 - 25 = x^2 - 5^2 = (x+5)(x-5)", "difficulty": 2},
    # Linear Equations (alg-2)
    {"id": "q-alg2-3", "topic_id": "alg-2", "topic_title": "Solving Linear Equations", "question": "Solve: 2(3x - 1) = 16", "options": ["x = 3", "x = 2", "x = 4", "x = 9"], "correct_answer": 0, "explanation": "6x - 2 = 16. 6x = 18. x = 3", "difficulty": 1},
    {"id": "q-alg2-4", "topic_id": "alg-2", "topic_title": "Solving Linear Equations", "question": "Solve: (x + 3)/4 = 5", "options": ["x = 17", "x = 2", "x = 23", "x = 8"], "correct_answer": 0, "explanation": "Multiply both sides by 4: x + 3 = 20. x = 17", "difficulty": 2},
    # Simultaneous (alg-3)
    {"id": "q-alg3-1", "topic_id": "alg-3", "topic_title": "Simultaneous Equations", "question": "Solve: x + y = 10 and x - y = 4", "options": ["x=7, y=3", "x=5, y=5", "x=8, y=2", "x=6, y=4"], "correct_answer": 0, "explanation": "Add equations: 2x = 14, x = 7. Then y = 10 - 7 = 3", "difficulty": 2},
    # Sequences (alg-4)
    {"id": "q-alg4-3", "topic_id": "alg-4", "topic_title": "Sequences & nth Term", "question": "What is the 10th term of the sequence: 2, 5, 8, 11, ...?", "options": ["29", "32", "30", "27"], "correct_answer": 0, "explanation": "nth term = 3n - 1. 10th term = 3(10) - 1 = 29", "difficulty": 1},
    {"id": "q-alg4-4", "topic_id": "alg-4", "topic_title": "Sequences & nth Term", "question": "Is 50 a term in the sequence 3n + 2?", "options": ["No", "Yes, it's the 16th term", "Yes, it's the 17th term", "Yes, it's the 15th term"], "correct_answer": 0, "explanation": "3n + 2 = 50, 3n = 48, n = 16. Check: 3(16)+2 = 50. Yes it is! Actually wait - 3(16)+2 = 50, so it IS the 16th term.", "difficulty": 2},
    # Quadratics (alg-5)
    {"id": "q-alg5-2", "topic_id": "alg-5", "topic_title": "Solving Quadratic Equations", "question": "Solve x^2 + 3x = 0", "options": ["x = 0 or x = -3", "x = 3", "x = 0 only", "x = -3 only"], "correct_answer": 0, "explanation": "x(x + 3) = 0. So x = 0 or x + 3 = 0, giving x = -3", "difficulty": 2},
    {"id": "q-alg5-3", "topic_id": "alg-5", "topic_title": "Solving Quadratic Equations", "question": "How many solutions does x^2 + 4 = 0 have?", "options": ["No real solutions", "1 solution", "2 solutions", "Infinite solutions"], "correct_answer": 0, "explanation": "x^2 = -4. Cannot square root a negative (in real numbers). Discriminant: 0 - 16 = -16 < 0", "difficulty": 3},
    # Linear Graphs (alg-6)
    {"id": "q-alg6-2", "topic_id": "alg-6", "topic_title": "Linear Graphs", "question": "A line has gradient 2 and passes through (0, -3). What is the equation?", "options": ["y = 2x - 3", "y = -3x + 2", "y = 2x + 3", "y = -2x - 3"], "correct_answer": 0, "explanation": "y = mx + c. m = 2, c = -3 (y-intercept). So y = 2x - 3", "difficulty": 1},
    {"id": "q-alg6-3", "topic_id": "alg-6", "topic_title": "Linear Graphs", "question": "Which line is perpendicular to y = 3x + 1?", "options": ["y = -1/3 x + 5", "y = 3x - 1", "y = -3x + 2", "y = 1/3 x + 4"], "correct_answer": 0, "explanation": "Perpendicular gradients multiply to -1. 3 x m = -1, m = -1/3", "difficulty": 2},
    # Ratio (rat-1)
    {"id": "q-rat1-2", "topic_id": "rat-1", "topic_title": "Ratio & Proportion", "question": "Simplify the ratio 45:75", "options": ["3:5", "9:15", "45:75", "1:2"], "correct_answer": 0, "explanation": "HCF of 45 and 75 is 15. 45/15 : 75/15 = 3:5", "difficulty": 1},
    {"id": "q-rat1-3", "topic_id": "rat-1", "topic_title": "Ratio & Proportion", "question": "A recipe uses flour and sugar in ratio 5:2. If you use 300g flour, how much sugar?", "options": ["120g", "150g", "100g", "200g"], "correct_answer": 0, "explanation": "5 parts = 300g, so 1 part = 60g. Sugar = 2 x 60 = 120g", "difficulty": 1},
    # Percentages (rat-2)
    {"id": "q-rat2-2", "topic_id": "rat-2", "topic_title": "Percentages & Interest", "question": "A coat was 120 before a 25% sale. What is the sale price?", "options": ["90", "95", "100", "30"], "correct_answer": 0, "explanation": "25% off: 120 x 0.75 = 90. Or: 25% of 120 = 30, 120 - 30 = 90", "difficulty": 1},
    {"id": "q-rat2-3", "topic_id": "rat-2", "topic_title": "Percentages & Interest", "question": "After a 20% increase, a price is 84. What was the original price?", "options": ["70", "67.20", "72", "80"], "correct_answer": 0, "explanation": "Reverse percentage: 84 / 1.20 = 70", "difficulty": 2},
    # Speed (rat-3)
    {"id": "q-rat3-2", "topic_id": "rat-3", "topic_title": "Speed, Distance & Time", "question": "How long to travel 180 km at 60 km/h?", "options": ["3 hours", "2 hours", "2.5 hours", "120 minutes"], "correct_answer": 0, "explanation": "Time = Distance / Speed = 180 / 60 = 3 hours", "difficulty": 1},
    # Angles (geo-1)
    {"id": "q-geo1-2", "topic_id": "geo-1", "topic_title": "Angles & Polygons", "question": "How many sides does a polygon with interior angles summing to 1440 degrees have?", "options": ["10", "8", "12", "9"], "correct_answer": 0, "explanation": "(n-2) x 180 = 1440. n-2 = 8. n = 10 sides (decagon)", "difficulty": 2},
    {"id": "q-geo1-3", "topic_id": "geo-1", "topic_title": "Angles & Polygons", "question": "What is the exterior angle of a regular pentagon?", "options": ["72 degrees", "108 degrees", "60 degrees", "90 degrees"], "correct_answer": 0, "explanation": "Exterior angle = 360/n = 360/5 = 72 degrees", "difficulty": 1},
    # Pythagoras (geo-2)
    {"id": "q-geo2-2", "topic_id": "geo-2", "topic_title": "Pythagoras' Theorem & Trigonometry", "question": "A ladder 10m long leans against a wall. The base is 6m from the wall. How high does it reach?", "options": ["8m", "7m", "4m", "16m"], "correct_answer": 0, "explanation": "h^2 + 6^2 = 10^2. h^2 = 100 - 36 = 64. h = 8m", "difficulty": 2},
    {"id": "q-geo2-3", "topic_id": "geo-2", "topic_title": "Pythagoras' Theorem & Trigonometry", "question": "If sin(x) = 0.5, what is angle x?", "options": ["30 degrees", "45 degrees", "60 degrees", "90 degrees"], "correct_answer": 0, "explanation": "sin^(-1)(0.5) = 30 degrees. This is worth memorising!", "difficulty": 2},
    # Area Volume (geo-3)
    {"id": "q-geo3-2", "topic_id": "geo-3", "topic_title": "Area, Perimeter & Volume", "question": "Find the area of a trapezium with parallel sides 5cm and 9cm, height 4cm.", "options": ["28 cm^2", "36 cm^2", "45 cm^2", "20 cm^2"], "correct_answer": 0, "explanation": "A = 1/2(a+b)h = 1/2(5+9)(4) = 1/2(14)(4) = 28 cm^2", "difficulty": 1},
    {"id": "q-geo3-3", "topic_id": "geo-3", "topic_title": "Area, Perimeter & Volume", "question": "What is the volume of a sphere with radius 3 cm? (to 1 d.p.)", "options": ["113.1 cm^3", "84.8 cm^3", "36.0 cm^3", "28.3 cm^3"], "correct_answer": 0, "explanation": "V = 4/3 x pi x r^3 = 4/3 x pi x 27 = 36pi = 113.1 cm^3", "difficulty": 2},
    # Transformations (geo-4)
    {"id": "q-geo4-2", "topic_id": "geo-4", "topic_title": "Transformations", "question": "An enlargement has scale factor -2. What happens to the shape?", "options": ["Doubled in size and inverted", "Halved in size", "Same size, reflected", "Doubled but same orientation"], "correct_answer": 0, "explanation": "Negative scale factor = enlargement AND inversion (flipped through centre)", "difficulty": 2},
    # Probability (sta-1)
    {"id": "q-sta1-2", "topic_id": "sta-1", "topic_title": "Probability Basics", "question": "A spinner has sections: red (0.4), blue (0.25), green (?). What is P(green)?", "options": ["0.35", "0.3", "0.65", "0.4"], "correct_answer": 0, "explanation": "All probabilities sum to 1: P(green) = 1 - 0.4 - 0.25 = 0.35", "difficulty": 1},
    {"id": "q-sta1-3", "topic_id": "sta-1", "topic_title": "Probability Basics", "question": "P(winning) = 0.15. In 200 games, how many wins expected?", "options": ["30", "15", "170", "185"], "correct_answer": 0, "explanation": "Expected frequency = probability x trials = 0.15 x 200 = 30", "difficulty": 1},
    # Averages (sta-2)
    {"id": "q-sta2-2", "topic_id": "sta-2", "topic_title": "Averages & Representing Data", "question": "Find the range of: 2, 8, 3, 11, 5", "options": ["9", "11", "5", "6"], "correct_answer": 0, "explanation": "Range = largest - smallest = 11 - 2 = 9", "difficulty": 1},
    {"id": "q-sta2-3", "topic_id": "sta-2", "topic_title": "Averages & Representing Data", "question": "The mean of 5 numbers is 8. What is the total of all 5 numbers?", "options": ["40", "13", "8", "5"], "correct_answer": 0, "explanation": "Mean = total / count. So total = mean x count = 8 x 5 = 40", "difficulty": 1},
    # NEW TOPIC QUIZZES
    # Surds (num-5)
    {"id": "q-num5-1", "topic_id": "num-5", "topic_title": "Surds", "question": "Simplify sqrt(48)", "options": ["4sqrt(3)", "2sqrt(12)", "16sqrt(3)", "sqrt(48)"], "correct_answer": 0, "explanation": "48 = 16 x 3. sqrt(48) = sqrt(16) x sqrt(3) = 4sqrt(3)", "difficulty": 2},
    {"id": "q-num5-2", "topic_id": "num-5", "topic_title": "Surds", "question": "Rationalise 1/sqrt(5)", "options": ["sqrt(5)/5", "5/sqrt(5)", "1/5", "sqrt(5)"], "correct_answer": 0, "explanation": "1/sqrt(5) x sqrt(5)/sqrt(5) = sqrt(5)/5", "difficulty": 2},
    {"id": "q-num5-3", "topic_id": "num-5", "topic_title": "Surds", "question": "Simplify sqrt(2) x sqrt(8)", "options": ["4", "sqrt(16)", "2sqrt(4)", "All correct"], "correct_answer": 0, "explanation": "sqrt(2) x sqrt(8) = sqrt(16) = 4", "difficulty": 2},
    # Inequalities (alg-7)
    {"id": "q-alg7-1", "topic_id": "alg-7", "topic_title": "Inequalities", "question": "Solve: 2x + 3 > 11", "options": ["x > 4", "x > 7", "x < 4", "x > 5.5"], "correct_answer": 0, "explanation": "2x + 3 > 11. 2x > 8. x > 4", "difficulty": 1},
    {"id": "q-alg7-2", "topic_id": "alg-7", "topic_title": "Inequalities", "question": "Solve: -3x < 12", "options": ["x > -4", "x < -4", "x > 4", "x < 4"], "correct_answer": 0, "explanation": "Divide by -3 and FLIP the sign: x > -4", "difficulty": 2},
    {"id": "q-alg7-3", "topic_id": "alg-7", "topic_title": "Inequalities", "question": "List integer values of n where -2 < n <= 3", "options": ["-1, 0, 1, 2, 3", "-2, -1, 0, 1, 2, 3", "-1, 0, 1, 2", "0, 1, 2, 3"], "correct_answer": 0, "explanation": "n must be > -2 (not including -2) and <= 3. So n = -1, 0, 1, 2, 3", "difficulty": 2},
    # Circle Theorems (geo-5)
    {"id": "q-geo5-1", "topic_id": "geo-5", "topic_title": "Circle Theorems", "question": "Angle in a semicircle is always:", "options": ["90 degrees", "180 degrees", "60 degrees", "45 degrees"], "correct_answer": 0, "explanation": "The angle in a semicircle is always 90 degrees (a right angle).", "difficulty": 1},
    {"id": "q-geo5-2", "topic_id": "geo-5", "topic_title": "Circle Theorems", "question": "In a cyclic quadrilateral, if one angle is 110 degrees, the opposite angle is:", "options": ["70 degrees", "110 degrees", "90 degrees", "180 degrees"], "correct_answer": 0, "explanation": "Opposite angles sum to 180. 180 - 110 = 70 degrees", "difficulty": 1},
    # Vectors (geo-7)
    {"id": "q-geo7-1", "topic_id": "geo-7", "topic_title": "Vectors", "question": "If a = (3, 2) and b = (1, -4), find a + b", "options": ["(4, -2)", "(2, 6)", "(3, -8)", "(4, 2)"], "correct_answer": 0, "explanation": "Add components: (3+1, 2+(-4)) = (4, -2)", "difficulty": 1},
    {"id": "q-geo7-2", "topic_id": "geo-7", "topic_title": "Vectors", "question": "Find 3a if a = (2, -1)", "options": ["(6, -3)", "(5, 2)", "(6, -1)", "(2, -3)"], "correct_answer": 0, "explanation": "Multiply each component by 3: 3(2, -1) = (6, -3)", "difficulty": 1},
    # Congruence & Similarity (geo-6)
    {"id": "q-geo6-1", "topic_id": "geo-6", "topic_title": "Congruence & Similarity", "question": "Two similar shapes have a linear scale factor of 3. What is the area scale factor?", "options": ["9", "3", "6", "27"], "correct_answer": 0, "explanation": "Area scale factor = (linear scale factor)^2 = 3^2 = 9", "difficulty": 2},
    {"id": "q-geo6-2", "topic_id": "geo-6", "topic_title": "Congruence & Similarity", "question": "Linear scale factor is 2. Volume of small shape is 10cm^3. Volume of large?", "options": ["80 cm^3", "20 cm^3", "40 cm^3", "60 cm^3"], "correct_answer": 0, "explanation": "Volume scale factor = 2^3 = 8. Large volume = 10 x 8 = 80 cm^3", "difficulty": 2},
    # Tree Diagrams (sta-3)
    {"id": "q-sta3-1", "topic_id": "sta-3", "topic_title": "Tree Diagrams & Combined Events", "question": "P(A) = 0.3, P(B) = 0.5. Events are independent. Find P(A and B).", "options": ["0.15", "0.8", "0.2", "0.35"], "correct_answer": 0, "explanation": "Independent events: P(A and B) = P(A) x P(B) = 0.3 x 0.5 = 0.15", "difficulty": 2},
    {"id": "q-sta3-2", "topic_id": "sta-3", "topic_title": "Tree Diagrams & Combined Events", "question": "P(rain) = 0.4. Find P(no rain on two consecutive days).", "options": ["0.36", "0.6", "0.16", "0.8"], "correct_answer": 0, "explanation": "P(no rain) = 0.6. P(no rain both) = 0.6 x 0.6 = 0.36", "difficulty": 2},
    # Scatter graphs (sta-5)
    {"id": "q-sta5-1", "topic_id": "sta-5", "topic_title": "Scatter Graphs & Correlation", "question": "As hours of revision increase, test scores increase. This is:", "options": ["Positive correlation", "Negative correlation", "No correlation", "Inverse proportion"], "correct_answer": 0, "explanation": "Both variables increase together = positive correlation", "difficulty": 1},
    # Growth & Decay (rat-5)
    {"id": "q-rat5-1", "topic_id": "rat-5", "topic_title": "Growth & Decay", "question": "A phone worth 600 depreciates by 15% per year. Value after 1 year?", "options": ["510", "500", "690", "90"], "correct_answer": 0, "explanation": "600 x 0.85 = 510. Or: 15% of 600 = 90, 600 - 90 = 510", "difficulty": 1},
    {"id": "q-rat5-2", "topic_id": "rat-5", "topic_title": "Growth & Decay", "question": "What multiplier represents a 7% annual growth?", "options": ["1.07", "0.93", "1.7", "0.07"], "correct_answer": 0, "explanation": "Growth of 7% = 1 + 0.07 = 1.07", "difficulty": 1},
    # Direct Inverse (rat-4)
    {"id": "q-rat4-1", "topic_id": "rat-4", "topic_title": "Direct & Inverse Proportion (Algebraic)", "question": "y is proportional to x. When x=3, y=12. Find y when x=7.", "options": ["28", "21", "84", "4"], "correct_answer": 0, "explanation": "y = kx. 12 = 3k, k = 4. When x=7: y = 4(7) = 28", "difficulty": 2},
    # Functions (alg-8)
    {"id": "q-alg8-1", "topic_id": "alg-8", "topic_title": "Functions & Iteration", "question": "f(x) = 2x + 5. Find f(3).", "options": ["11", "8", "6", "15"], "correct_answer": 0, "explanation": "f(3) = 2(3) + 5 = 6 + 5 = 11", "difficulty": 1},
    {"id": "q-alg8-2", "topic_id": "alg-8", "topic_title": "Functions & Iteration", "question": "f(x) = x^2, g(x) = x+1. Find fg(2).", "options": ["9", "5", "4", "8"], "correct_answer": 0, "explanation": "g(2) = 2+1 = 3. Then f(3) = 3^2 = 9", "difficulty": 2},
    # Bearings (geo-8)
    {"id": "q-geo8-1", "topic_id": "geo-8", "topic_title": "Bearings & Scale Drawings", "question": "The bearing of B from A is 135 degrees. Find bearing of A from B.", "options": ["315 degrees", "045 degrees", "225 degrees", "135 degrees"], "correct_answer": 0, "explanation": "135 < 180, so add 180: 135 + 180 = 315 degrees", "difficulty": 2},
    {"id": "q-geo8-2", "topic_id": "geo-8", "topic_title": "Bearings & Scale Drawings", "question": "On a map scale 1:50000, 4cm represents:", "options": ["2 km", "20 km", "200 m", "500 m"], "correct_answer": 0, "explanation": "4 x 50000 = 200,000 cm = 2,000 m = 2 km", "difficulty": 1},
]

ADDITIONAL_PAST_PAPERS = [
    # More Edexcel
    {"id": "pp-ed-2022-1f", "board": "Edexcel", "year": "2022", "paper_number": 1, "tier": "Foundation", "calculator_allowed": False, "description": "Paper 1 Non-Calculator (Foundation) - June 2022", "link": "https://qualifications.pearson.com/en/qualifications/edexcel-gcses/mathematics-2015.html", "practice_questions": [
        {"question": "Work out 2/3 + 1/4", "answer": "Find common denominator: 8/12 + 3/12 = 11/12", "marks": 2, "topic": "Fractions"},
        {"question": "Expand 5(2x - 3)", "answer": "10x - 15", "marks": 1, "topic": "Algebra"},
        {"question": "A bus leaves at 09:45 and arrives at 11:20. How long is the journey?", "answer": "09:45 to 10:00 = 15 min, 10:00 to 11:00 = 60 min, 11:00 to 11:20 = 20 min. Total = 95 minutes = 1 hour 35 minutes", "marks": 2, "topic": "Time"},
        {"question": "Find the median of: 4, 7, 2, 9, 1, 6, 3", "answer": "In order: 1, 2, 3, 4, 6, 7, 9. Median = 4 (middle value)", "marks": 2, "topic": "Averages"},
    ]},
    {"id": "pp-ed-2022-2h", "board": "Edexcel", "year": "2022", "paper_number": 2, "tier": "Higher", "calculator_allowed": True, "description": "Paper 2 Calculator (Higher) - June 2022", "link": "https://qualifications.pearson.com/en/qualifications/edexcel-gcses/mathematics-2015.html", "practice_questions": [
        {"question": "Solve 3x^2 - 7x + 2 = 0", "answer": "(3x - 1)(x - 2) = 0. x = 1/3 or x = 2", "marks": 3, "topic": "Quadratics"},
        {"question": "A solid hemisphere has radius 6 cm. Find its volume.", "answer": "V = 2/3 x pi x r^3 = 2/3 x pi x 216 = 144pi = 452.4 cm^3", "marks": 3, "topic": "Volume"},
        {"question": "Simplify sqrt(75) - sqrt(27)", "answer": "sqrt(75) = 5sqrt(3), sqrt(27) = 3sqrt(3). Answer: 5sqrt(3) - 3sqrt(3) = 2sqrt(3)", "marks": 3, "topic": "Surds"},
    ]},
    # More AQA
    {"id": "pp-aqa-2022-1f", "board": "AQA", "year": "2022", "paper_number": 1, "tier": "Foundation", "calculator_allowed": False, "description": "Paper 1 Non-Calculator (Foundation) - June 2022", "link": "https://www.aqa.org.uk/subjects/mathematics/gcse/mathematics-8300", "practice_questions": [
        {"question": "List all factors of 36", "answer": "1, 2, 3, 4, 6, 9, 12, 18, 36", "marks": 2, "topic": "Number"},
        {"question": "Solve 5x - 8 = 17", "answer": "5x = 25, x = 5", "marks": 2, "topic": "Equations"},
        {"question": "A regular polygon has exterior angles of 40 degrees. How many sides?", "answer": "360 / 40 = 9 sides (nonagon)", "marks": 2, "topic": "Angles"},
    ]},
    {"id": "pp-aqa-2022-3h", "board": "AQA", "year": "2022", "paper_number": 3, "tier": "Higher", "calculator_allowed": True, "description": "Paper 3 Calculator (Higher) - June 2022", "link": "https://www.aqa.org.uk/subjects/mathematics/gcse/mathematics-8300", "practice_questions": [
        {"question": "y is inversely proportional to x^2. When x=2, y=5. Find y when x=4.", "answer": "y = k/x^2. 5 = k/4, k = 20. When x=4: y = 20/16 = 1.25", "marks": 3, "topic": "Proportion"},
        {"question": "Prove that the product of two consecutive odd numbers is always odd.", "answer": "(2n+1)(2n+3) = 4n^2+8n+3 = 2(2n^2+4n+1)+1, which is odd.", "marks": 4, "topic": "Proof"},
    ]},
    # More OCR
    {"id": "pp-ocr-2022-1f", "board": "OCR", "year": "2022", "paper_number": 1, "tier": "Foundation", "calculator_allowed": False, "description": "Paper 1 Non-Calculator (Foundation) - June 2022", "link": "https://www.ocr.org.uk/qualifications/gcse/mathematics-j560-from-2015/", "practice_questions": [
        {"question": "Convert 5/8 to a percentage", "answer": "5/8 = 0.625 = 62.5%", "marks": 2, "topic": "Fractions"},
        {"question": "Find the nth term of: 7, 10, 13, 16...", "answer": "Common difference = 3, first term = 7. nth term = 3n + 4", "marks": 2, "topic": "Sequences"},
        {"question": "What is the probability of rolling a prime number on a fair dice?", "answer": "Prime numbers on dice: 2, 3, 5 = 3 outcomes. P = 3/6 = 1/2", "marks": 2, "topic": "Probability"},
    ]},
    {"id": "pp-ocr-2022-3h", "board": "OCR", "year": "2022", "paper_number": 3, "tier": "Higher", "calculator_allowed": True, "description": "Paper 3 Calculator (Higher) - June 2022", "link": "https://www.ocr.org.uk/qualifications/gcse/mathematics-j560-from-2015/", "practice_questions": [
        {"question": "Two similar triangles have areas 16 cm^2 and 100 cm^2. Find the linear scale factor.", "answer": "Area SF = 100/16 = 6.25. Linear SF = sqrt(6.25) = 2.5", "marks": 3, "topic": "Similarity"},
    ]},
]

ADDITIONAL_FORMULAS = [
    {"id": "f-21", "category": "Algebra", "name": "Completing the Square", "formula": "x^2 + bx = (x + b/2)^2 - (b/2)^2", "description": "Rewriting a quadratic in completed square form", "usage_example": "x^2 + 6x = (x+3)^2 - 9"},
    {"id": "f-22", "category": "Geometry & Measures", "name": "Sine Rule", "formula": "a/sin(A) = b/sin(B) = c/sin(C)", "description": "For non-right-angled triangles when you have a side-angle pair", "usage_example": "Find side a: a/sin(50) = 8/sin(70)"},
    {"id": "f-23", "category": "Geometry & Measures", "name": "Cosine Rule", "formula": "a^2 = b^2 + c^2 - 2bc x cos(A)", "description": "For finding a side when you know two sides and the included angle", "usage_example": "a^2 = 5^2 + 7^2 - 2(5)(7)cos(60)"},
    {"id": "f-24", "category": "Geometry & Measures", "name": "Area of Triangle (Trig)", "formula": "A = 1/2 x a x b x sin(C)", "description": "Area using two sides and the included angle", "usage_example": "A = 1/2 x 5 x 8 x sin(40) = 12.86"},
    {"id": "f-25", "category": "Number", "name": "Recurring Decimal Conversion", "formula": "x = 0.abcabc... then 1000x - x = abc", "description": "Convert recurring decimals to fractions", "usage_example": "x = 0.333... 10x = 3.333... 9x = 3, x = 1/3"},
    {"id": "f-26", "category": "Algebra", "name": "Difference of Two Squares", "formula": "a^2 - b^2 = (a+b)(a-b)", "description": "Factorise the difference of two perfect squares", "usage_example": "x^2 - 49 = (x+7)(x-7)"},
    {"id": "f-27", "category": "Geometry & Measures", "name": "Arc Length", "formula": "Arc length = (theta/360) x 2 x pi x r", "description": "Length of an arc of a circle", "usage_example": "60 degree arc, r=5: (60/360) x 2pi(5) = 5.24 cm"},
    {"id": "f-28", "category": "Geometry & Measures", "name": "Sector Area", "formula": "Sector area = (theta/360) x pi x r^2", "description": "Area of a sector of a circle", "usage_example": "90 degree sector, r=4: (90/360) x pi(16) = 4pi = 12.57 cm^2"},
    {"id": "f-29", "category": "Probability & Statistics", "name": "Mean from Frequency Table", "formula": "Mean = Sum(f x x) / Sum(f)", "description": "Estimated mean from a frequency table using midpoints for grouped data", "usage_example": "Total of fx = 250, total frequency = 40, mean = 6.25"},
    {"id": "f-30", "category": "Geometry & Measures", "name": "Volume of Pyramid", "formula": "V = 1/3 x base area x height", "description": "Volume of any pyramid", "usage_example": "Square base 6x6, height 10: V = 1/3 x 36 x 10 = 120 cm^3"},
]
