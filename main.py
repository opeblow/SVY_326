#!/usr/bin/env python3
"""Equation 2-28 3D Coordinate Rotation Sweep -- SVY 326.

This module serves as the entry point for the project.  It:

  1. Builds the constant Rz(180) and variable Ry(90 - phi) rotation
     matrices defined in Equation 2-28.
  2. Sweeps phi from 0 to 360 degrees in 15-degree increments for three
     test vectors in the HA frame: (1,0,0), (0,1,0), and (1,1,1).
  3. Prints a formatted table of results to the console.
  4. Exports the formatted results to ``data/results.txt``.
  5. Generates four professional-grade plots saved to ``graphs/``.

Usage:
    python main.py
"""

import pandas as pd

from src.rotation_matrices import composite_matrix
from src.transform import format_results_table, save_all_results, sweep_angles
from src.visualize import generate_all_plots

# ---------------------------------------------------------------------------
# Test vectors in the HA frame  [X, Y, Z]_HA
# ---------------------------------------------------------------------------
TEST_VECTORS: list[tuple[float, float, float, str]] = [
    (1.0, 0.0, 0.0, "(1, 0, 0)"),
    (0.0, 1.0, 0.0, "(0, 1, 0)"),
    (1.0, 1.0, 1.0, "(1, 1, 1)"),
]

PHI_START: float = 0.0
PHI_STOP: float = 360.0
PHI_STEP: float = 15.0


def _print_separator(char: str = "=", width: int = 78) -> None:
    """Print a horizontal separator line.

    Args:
        char: Character to repeat.
        width: Total line width.
    """
    print(char * width)


def _print_equation_header() -> None:
    """Print the equation reference and course information."""
    _print_separator()
    print("  SVY 326 -- Geodesy and Surveying")
    print("  Equation 2-28: Composite 3D Coordinate Rotation")
    print("  HA Frame -> H Frame via Rz(180) @ Ry(90 - phi)")
    _print_separator()


def _print_matrix_inspections() -> None:
    """Print the constant Rz(180) matrix and a sample composite matrix."""
    rz = composite_matrix(0.0)  # Rz(180) @ Ry(90)
    print("\nComposite matrix at phi = 0 deg:")
    print(pd.DataFrame(rz, columns=["X'", "Y'", "Z'"],
                       index=["X", "Y", "Z"]).to_string())
    print()


def main() -> None:
    """Execute the full Equation 2-28 analysis pipeline."""
    _print_equation_header()
    _print_matrix_inspections()

    results: list[tuple[pd.DataFrame, str]] = []
    df_plots: pd.DataFrame | None = None

    for x, y, z, label in TEST_VECTORS:
        df: pd.DataFrame = sweep_angles(x, y, z, PHI_START, PHI_STOP,
                                        PHI_STEP)
        results.append((df, label))

        table_text: str = format_results_table(df, label)
        print(table_text)
        print()

        if label == "(1, 0, 0)":
            df_plots = df

    # Save all results to a single formatted text file
    results_path = save_all_results(results)
    _print_separator()
    print(f"\nResults saved to: {results_path}")
    print("Generating plots ...")

    if df_plots is not None:
        generate_all_plots(df_plots)
        print("Plots saved to: graphs/")
        print("  - plot1_3d_path.png")
        print("  - plot2_xyz_vs_phi_separate.png")
        print("  - plot3_sine_cosine_comparison.png")
        print("  - plot4_xyz_overlay.png")

    _print_separator()
    print("Done.")


if __name__ == "__main__":
    main()
