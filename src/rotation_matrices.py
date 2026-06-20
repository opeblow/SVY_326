"""Build the rotation matrices for Equation 2-28.

Provides:
  - rz_180()         : constant Z-axis rotation of 180 degrees
  - ry_90_minus_phi() : Y-axis rotation of (90 degrees - phi)
  - composite_matrix() : Rz(180) @ Ry(90 - phi)
"""

import numpy as np

# ---------------------------------------------------------------------------
# Named constants
# ---------------------------------------------------------------------------
Z_AXIS_ROTATION_DEG: float = 180.0
"""Fixed rotation about the Z-axis in degrees (Equation 2-28, first factor)."""

Y_AXIS_OFFSET_DEG: float = 90.0
"""Constant offset subtracted from phi before the Y-axis rotation."""


def rz_180() -> np.ndarray:
    """Return the exact 3x3 rotation matrix for 180 degrees about the Z-axis.

    Since cos(180) = -1 and sin(180) = 0 exactly, the matrix is hardcoded
    rather than computed via floating-point trigonometric calls.

    Returns:
        numpy.ndarray: Shape (3, 3) rotation matrix.
    """
    return np.array([
        [-1.0,  0.0,  0.0],
        [ 0.0, -1.0,  0.0],
        [ 0.0,  0.0,  1.0],
    ])


def ry_90_minus_phi(phi_degrees: float) -> np.ndarray:
    """Build the Y-axis rotation matrix for angle (90 - phi) degrees.

    Args:
        phi_degrees: Angle phi in degrees.  The actual rotation angle applied
            is (90 - phi_degrees).

    Returns:
        numpy.ndarray: Shape (3, 3) Y-rotation matrix.
    """
    angle_deg: float = Y_AXIS_OFFSET_DEG - phi_degrees
    angle_rad: float = np.deg2rad(angle_deg)
    c: float = np.cos(angle_rad)
    s: float = np.sin(angle_rad)
    return np.array([
        [ c,  0.0,  s],
        [ 0.0, 1.0,  0.0],
        [-s,  0.0,  c],
    ])


def composite_matrix(phi_degrees: float) -> np.ndarray:
    """Compute the full composite rotation Rz(180) * Ry(90 - phi).

    Args:
        phi_degrees: Angle phi in degrees.

    Returns:
        numpy.ndarray: Shape (3, 3) composite rotation matrix.
    """
    return rz_180() @ ry_90_minus_phi(phi_degrees)
