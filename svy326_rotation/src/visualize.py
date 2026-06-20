"""Plotting routines for the Equation 2-28 rotation sweep.

Generates four professional-grade figures and saves each to the ``graphs/``
directory as a PNG image.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.rotation_matrices import ry_90_minus_phi

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
GRAPHS_DIR: Path = Path(__file__).resolve().parent.parent / "graphs"


def _ensure_graphs_dir() -> None:
    """Create the graphs output directory if it does not already exist."""
    GRAPHS_DIR.mkdir(parents=True, exist_ok=True)


def plot_3d_path(df: pd.DataFrame, label: str = "(1, 0, 0)") -> None:
    """Plot 1 -- 3D scatter / line of the rotated point's path in space.

    Args:
        df: DataFrame with columns ``X``, ``Y``, ``Z``.
        label: Legend label describing the test vector.
    """
    _ensure_graphs_dir()
    fig = plt.figure(figsize=(8, 7))
    ax = fig.add_subplot(111, projection="3d")

    ax.plot(
        df["X"], df["Y"], df["Z"],
        color="#1f3a5f", linewidth=1.5, marker="o", markersize=4,
        label=label,
    )

    # Mark the start and end points
    ax.scatter(
        df["X"].iloc[0], df["Y"].iloc[0], df["Z"].iloc[0],
        color="#e63946", s=60, label="Start (phi = 0 deg)", zorder=5,
    )
    ax.scatter(
        df["X"].iloc[-1], df["Y"].iloc[-1], df["Z"].iloc[-1],
        color="#2a9d8f", s=60, label="End (phi = 360 deg)", zorder=5,
    )

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("Equation 2-28: 3D Path of Rotated Vector in H Frame")
    ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig(GRAPHS_DIR / "plot1_3d_path.png", dpi=150)
    plt.close(fig)


def plot_xyz_vs_phi_separate(df: pd.DataFrame) -> None:
    """Plot 2 -- Three subplots showing X, Y, and Z individually vs phi.

    Args:
        df: DataFrame with columns ``phi_deg``, ``X``, ``Y``, ``Z``.
    """
    _ensure_graphs_dir()
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 9), sharex=True)

    colors = ["#1f3a5f", "#e63946", "#2a9d8f"]
    labels = ["X", "Y", "Z"]
    data = [df["X"], df["Y"], df["Z"]]

    for ax, vals, col, lab in zip([ax1, ax2, ax3], data, colors, labels):
        ax.plot(df["phi_deg"], vals, color=col, marker="o", linewidth=1.5,
                markersize=4, label=lab)
        ax.set_ylabel(lab)
        ax.legend(loc="best")
        ax.grid(True, alpha=0.3)

    ax3.set_xlabel("phi (degrees)")
    fig.suptitle("Equation 2-28: Coordinate Components vs phi")
    fig.tight_layout()
    fig.savefig(GRAPHS_DIR / "plot2_xyz_vs_phi_separate.png", dpi=150)
    plt.close(fig)


def plot_sine_cosine_comparison() -> None:
    """Plot 3 -- Continuous sin(90 - phi) and cos(90 - phi) curves with the
    15-degree sample points overlaid.

    Uses a fine-grained phi array (0.1 degree steps) for smooth curves.
    """
    _ensure_graphs_dir()
    phi_fine: np.ndarray = np.linspace(0.0, 360.0, 3601)
    phi_step15: np.ndarray = np.arange(0.0, 360.1, 15.0)

    # Build the Ry(90 - phi) matrix for each angle and extract (0,0) and (0,2)
    # which correspond to cos(90-phi) and -sin(90-phi) respectively.
    cos_vals: np.ndarray = np.array([
        ry_90_minus_phi(p)[0, 0] for p in phi_fine
    ])
    sin_vals: np.ndarray = np.array([
        -ry_90_minus_phi(p)[0, 2] for p in phi_fine
    ])

    cos_step: np.ndarray = np.array([
        ry_90_minus_phi(p)[0, 0] for p in phi_step15
    ])
    sin_step: np.ndarray = np.array([
        -ry_90_minus_phi(p)[0, 2] for p in phi_step15
    ])

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.plot(phi_fine, cos_vals, color="#1f3a5f", linewidth=1.5,
            label="cos(90 - phi)")
    ax.plot(phi_fine, sin_vals, color="#e63946", linewidth=1.5,
            label="sin(90 - phi)")
    ax.scatter(phi_step15, cos_step, color="#1f3a5f", s=30, zorder=5,
               label="cos(90 - phi) @ 15-deg steps")
    ax.scatter(phi_step15, sin_step, color="#e63946", s=30, zorder=5,
               label="sin(90 - phi) @ 15-deg steps")

    ax.set_xlabel("phi (degrees)")
    ax.set_ylabel("Function value")
    ax.set_title(
        "Equation 2-28: sin(90 - phi) and cos(90 - phi) vs phi"
    )
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(GRAPHS_DIR / "plot3_sine_cosine_comparison.png", dpi=150)
    plt.close(fig)


def plot_xyz_overlay(df: pd.DataFrame) -> None:
    """Plot 4 -- Overlay X, Y, Z vs phi on a single 2D plot.

    Args:
        df: DataFrame with columns ``phi_deg``, ``X``, ``Y``, ``Z``.
    """
    _ensure_graphs_dir()
    fig, ax = plt.subplots(figsize=(9, 5))

    styles = [
        ("X", "#1f3a5f", "o-"),
        ("Y", "#e63946", "s-"),
        ("Z", "#2a9d8f", "^-"),
    ]

    for col, color, marker in styles:
        ax.plot(
            df["phi_deg"], df[col],
            marker, color=color, linewidth=1.5, markersize=4,
            label=col,
        )

    ax.set_xlabel("phi (degrees)")
    ax.set_ylabel("Coordinate value")
    ax.set_title(
        "Equation 2-28: X, Y, Z vs phi (Overlay)"
    )
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(GRAPHS_DIR / "plot4_xyz_overlay.png", dpi=150)
    plt.close(fig)


def generate_all_plots(df: pd.DataFrame) -> None:
    """Convenience function to generate all four plots at once.

    Args:
        df: DataFrame with columns ``phi_deg``, ``X``, ``Y``, ``Z``.
    """
    plot_3d_path(df)
    plot_xyz_vs_phi_separate(df)
    plot_sine_cosine_comparison()
    plot_xyz_overlay(df)
