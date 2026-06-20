"""Unit tests for the rotation matrices and transform logic.

Verifies known analytic results for Rz(180), Ry(90 - phi), the composite
matrix, orthogonality, and determinant properties.
"""

import numpy as np
import pytest

from src.rotation_matrices import rz_180, ry_90_minus_phi, composite_matrix
from src.transform import transform_point


class TestRz180:
    """Tests for the constant 180-degree Z-rotation matrix."""

    def test_exact_values(self) -> None:
        """Rz(180) must equal [[-1,0,0],[0,-1,0],[0,0,1]] exactly."""
        expected = np.array([[-1.0, 0.0, 0.0],
                             [0.0, -1.0, 0.0],
                             [0.0, 0.0, 1.0]])
        np.testing.assert_array_equal(rz_180(), expected)

    def test_shape(self) -> None:
        """Rz(180) must be 3x3."""
        assert rz_180().shape == (3, 3)

    def test_orthogonal(self) -> None:
        """Rz(180) must be orthogonal: R^T = R^{-1}."""
        r = rz_180()
        np.testing.assert_array_almost_equal(r.T @ r, np.eye(3))

    def test_determinant_one(self) -> None:
        """Rz(180) must have determinant = 1."""
        assert np.linalg.det(rz_180()) == pytest.approx(1.0)


class TestRy90MinusPhi:
    """Tests for the Y-axis rotation matrix Ry(90 - phi)."""

    def test_phi_90_degrees(self) -> None:
        """At phi=90, (90-90)=0 so Ry(0) should be the identity."""
        r = ry_90_minus_phi(90.0)
        np.testing.assert_array_almost_equal(r, np.eye(3))

    def test_phi_0_degrees(self) -> None:
        """At phi=0, (90-0)=90 so Ry(90) should match analytic form."""
        r = ry_90_minus_phi(0.0)
        expected = np.array([[0.0, 0.0, 1.0],
                             [0.0, 1.0, 0.0],
                             [-1.0, 0.0, 0.0]])
        np.testing.assert_array_almost_equal(r, expected)

    def test_phi_180_degrees(self) -> None:
        """At phi=180, (90-180)=-90, verify symmetry."""
        r = ry_90_minus_phi(180.0)
        expected = np.array([[0.0, 0.0, -1.0],
                             [0.0, 1.0, 0.0],
                             [1.0, 0.0, 0.0]])
        np.testing.assert_array_almost_equal(r, expected)


class TestCompositeMatrix:
    """Tests for the composite rotation Rz(180) @ Ry(90 - phi)."""

    @pytest.mark.parametrize("phi", [0.0, 45.0, 90.0, 180.0, 270.0, 360.0])
    def test_orthogonal(self, phi: float) -> None:
        """The composite matrix must be orthogonal for several phi values."""
        r = composite_matrix(phi)
        np.testing.assert_array_almost_equal(r.T @ r, np.eye(3),
                                             err_msg=f"Failed at phi={phi}")

    @pytest.mark.parametrize("phi", [0.0, 30.0, 60.0, 120.0, 200.0, 315.0])
    def test_determinant_one(self, phi: float) -> None:
        """The composite matrix must have determinant = 1 for several phi."""
        r = composite_matrix(phi)
        det = np.linalg.det(r)
        assert det == pytest.approx(1.0, abs=1e-10), \
            f"Determinant deviates from 1 at phi={phi}: {det}"

    def test_transform_unit_x(self) -> None:
        """Apply composite to (1,0,0) at phi=0 and verify manually.

        At phi=0: Rz(180) @ Ry(90).  Ry(90) maps (1,0,0) -> (0,0,-1);
        then Rz(180) maps (0,0,-1) -> (0,0,-1).  Result: (0, 0, -1).
        """
        r = composite_matrix(0.0)
        result = r @ np.array([1.0, 0.0, 0.0])
        expected = np.array([0.0, 0.0, -1.0])
        np.testing.assert_array_almost_equal(result, expected)

    def test_transform_unit_y(self) -> None:
        """Apply composite to (0,1,0) at phi=0 and verify.

        Ry(90) maps (0,1,0) -> (0,1,0); then Rz(180) maps (0,1,0) -> (0,-1,0).
        """
        r = composite_matrix(0.0)
        result = r @ np.array([0.0, 1.0, 0.0])
        expected = np.array([0.0, -1.0, 0.0])
        np.testing.assert_array_almost_equal(result, expected)

    @pytest.mark.parametrize("phi", [0.0, 30.0, 90.0, 180.0, 270.0])
    def test_regression_z_sign(self, phi: float) -> None:
        """Regression: transform_point(1,0,0,phi) must be (-sin,0,-cos).

        This guards against the Z-sign bug where Z was +cos(phi) instead
        of -cos(phi).
        """
        import numpy as np
        phi_rad: float = np.deg2rad(phi)
        result = transform_point(1.0, 0.0, 0.0, phi)
        expected = np.array([-np.sin(phi_rad), 0.0, -np.cos(phi_rad)])
        np.testing.assert_array_almost_equal(result, expected,
                                             err_msg=f"Failed at phi={phi}")
