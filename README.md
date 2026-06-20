<p align="center">
  <img src="assets/logo.svg" alt="Project logo" width="120">
</p>

<h1 align="center">SVY 326 -- Equation 2-28: 3D Coordinate Rotation Sweep</h1>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License MIT">
  <img src="https://img.shields.io/badge/tests-pytest%20passing-brightgreen" alt="Tests Passing">
  <img src="https://img.shields.io/badge/code%20style-Google-4285F4" alt="Google Python Style">
  <img src="https://img.shields.io/badge/numpy-%3E%3D1.24-013243" alt="NumPy">
  <img src="https://img.shields.io/badge/matplotlib-%3E%3D3.7-11557C" alt="Matplotlib">
</p>

A clean, professional Python implementation of Equation 2-28 from the SVY 326 (Geodesy and Surveying) curriculum.  The equation describes a composite 3D rotation that transforms a coordinate vector from the HA (horizon-astronomic) frame to the H (horizon) frame via a constant 180-degree rotation about the Z-axis followed by a rotation of (90 - phi) degrees about the Y-axis.  The project sweeps the angle parameter phi from 0 to 360 degrees, visualises the results in four publication-quality plots, and includes a full suite of unit tests.

## Table of Contents

- [Overview](#overview)
- [Equation](#equation)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Output](#output)
- [Sample Results](#sample-results)
- [License](#license)
- [Author](#author)

## Overview

In geodesy and surveying, coordinate frames must be rotated to align with different reference systems.  Equation 2-28 performs this transformation through two successive rotations:

1. **Rz(180 degrees)** -- A constant rotation of 180 degrees about the Z-axis (first factor applied to the vector).
2. **Ry(90 - phi degrees)** -- A rotation about the Y-axis by an angle that depends on the parameter phi (second factor applied).

The product Rz(180) * Ry(90 - phi) is orthogonal (det = 1) and therefore represents a proper rotation -- no scaling, shearing, or reflection is introduced.

## Equation

```
[X]     [-1  0  0]   [ cos(90-phi)   0   -sin(90-phi) ]   [X]
[Y]  =  [ 0 -1  0] * [      0        1        0       ] * [Y]
[Z]_H   [ 0  0  1]   [ sin(90-phi)   0    cos(90-phi) ]   [Z]_HA
```

Where:

- **phi** is the variable angle parameter (swept from 0 to 360 degrees in 15-degree steps).
- The left-hand vector is in the H frame (horizon).
- The right-hand vector is in the HA frame (horizon-astronomic).
- All trigonometric functions receive arguments converted to radians.

## Project Structure

```
.
  .gitignore                    Ignored file patterns (venv, __pycache__, etc.)
  README.md                     This file
  requirements.txt              Python dependencies
  main.py                       Entry point: runs the full pipeline
  src/
    __init__.py                 Package initialiser
    rotation_matrices.py        Rz(180), Ry(90-phi), and composite matrix
    transform.py                Point transformation and angle sweep
    visualize.py                Plotting routines (four figures)
  tests/
    __init__.py
    test_rotation.py            Pytest unit tests with known analytic values
  data/
    results.txt                 Formatted sweep results for all test vectors
  graphs/
    plot1_3d_path.png           3D scatter / line of the rotated path
    plot2_xyz_vs_phi_separate.png  X, Y, Z components vs phi (subplots)
    plot3_sine_cosine_comparison.png  Continuous trig curves + discrete samples
    plot4_xyz_overlay.png       X, Y, Z overlay on a single axes
  assets/
    logo.svg                    Geometric logo representing frame rotation
  venv/                         (virtual environment, not tracked)
```

## Installation

The virtual environment is already activated.  To install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the full pipeline from the project root:

```bash
python main.py
```

This will:

1. Print the composite matrix at phi = 0.
2. Sweep phi from 0 to 360 degrees at 15-degree increments for three test vectors.
3. Print formatted tables of results to the console.
4. Save formatted results for all three test vectors to `data/results.txt`.
5. Generate all four plots into the `graphs/` directory.

## Testing

Run the unit test suite with pytest:

```bash
pytest tests/ -v
```

Tests verify:

- Exact values of the constant Rz(180) matrix.
- Ry(90 - phi) at phi = 90 (identity) and phi = 0 (Ry(90)).
- Orthogonality (R^T * R = I) of the composite matrix at six phi values.
- Determinant = 1 (proper rotation) at six phi values.
- Analytic hand-check of the transform for unit vectors at phi = 0.
- Regression test: Z = -cos(phi) for transform_point(1,0,0,phi) at five phi values.

## Output

| File | Description |
|------|-------------|
| `data/results.txt` | Formatted plain-text results for all three test vectors. |
| `graphs/plot1_3d_path.png` | 3D path of the rotated vector through all 25 angle steps. |
| `graphs/plot2_xyz_vs_phi_separate.png` | Three stacked subplots of X, Y, Z vs phi. |
| `graphs/plot3_sine_cosine_comparison.png` | Continuous sin(90-phi) / cos(90-phi) curves with 15-degree sample markers. |
| `graphs/plot4_xyz_overlay.png` | X, Y, Z plotted together on a single 2D axes with legend. |

## Sample Results

Results for test vector (1, 0, 0)_HA swept from 0 to 45 degrees:

| Phi (deg) | X | Y | Z |
|-----------|---|---|---|
| 0.0 | 0.0000 | 0.0000 | -1.0000 |
| 15.0 | -0.2588 | 0.0000 | -0.9659 |
| 30.0 | -0.5000 | 0.0000 | -0.8660 |
| 45.0 | -0.7071 | 0.0000 | -0.7071 |

Note: The Y component remains zero for this particular test vector because the input vector (1, 0, 0) is orthogonal to the Y-axis and the composite rotation only introduces Y components for vectors with a non-zero Y input.  For the (1,0,0) test vector the analytic result is X = -sin(phi), Y = 0, Z = -cos(phi).

## License

Distributed under the MIT License.  See `LICENSE` for more information.

## Author

Developed for SVY 326 -- Geodesy and Surveying.
