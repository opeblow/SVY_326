"""Coordinate transformation logic for Equation 2-28.

Applies the composite rotation matrix to individual points and sweeps the
angle parameter phi across a user-defined range.
"""

from pathlib import Path

import numpy as np
import pandas as pd

from src.rotation_matrices import composite_matrix

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
DATA_DIR: Path = Path(__file__).resolve().parent.parent / "data"
RESULTS_TXT: Path = DATA_DIR / "results.txt"


def transform_point(
    x: float, y: float, z: float, phi_degrees: float
) -> np.ndarray:
    """Transform a point from the HA frame to the H frame.

    Applies the composite rotation Rz(180) * Ry(90 - phi) to the input
    coordinate vector [x, y, z] in the HA frame, producing the corresponding
    vector in the H frame.

    Args:
        x: X-coordinate in the HA frame.
        y: Y-coordinate in the HA frame.
        z: Z-coordinate in the HA frame.
        phi_degrees: Angle phi in degrees.

    Returns:
        numpy.ndarray: Shape (3,) vector [X, Y, Z] in the H frame.
    """
    vec_ha: np.ndarray = np.array([x, y, z], dtype=float)
    rot: np.ndarray = composite_matrix(phi_degrees)
    return rot @ vec_ha


def sweep_angles(
    x: float,
    y: float,
    z: float,
    start: float = 0.0,
    stop: float = 360.0,
    step: float = 15.0,
) -> pd.DataFrame:
    """Sweep phi from start to stop (inclusive) and tabulate the transformed
    coordinates.

    For each phi in the range defined by [start, stop] with the given step,
    the function computes the H-frame coordinates and returns the results
    as a DataFrame.  All numeric values are rounded to 4 decimal places.

    Args:
        x: X-coordinate in the HA frame.
        y: Y-coordinate in the HA frame.
        z: Z-coordinate in the HA frame.
        start: Starting phi value in degrees (default 0.0).
        stop: Final phi value in degrees (default 360.0).
        step: Step size in degrees (default 15.0).

    Returns:
        pandas.DataFrame: Columns ``phi_deg``, ``X``, ``Y``, ``Z``.

    Raises:
        ValueError: If step is zero or negative.
    """
    if step <= 0:
        raise ValueError(f"Step must be positive; got {step}")

    phi_values: np.ndarray = np.arange(start, stop + step, step)
    rows: list[dict[str, float]] = []

    for phi in phi_values:
        vec_h: np.ndarray = transform_point(x, y, z, phi)
        rows.append({
            "phi_deg": round(phi, 4),
            "X": round(vec_h[0], 4),
            "Y": round(vec_h[1], 4),
            "Z": round(vec_h[2], 4),
        })

    return pd.DataFrame(rows)


def format_results_table(df: pd.DataFrame, label: str) -> str:
    """Build a formatted plain-text table for one test vector (no file header).

    Args:
        df: DataFrame with columns ``phi_deg``, ``X``, ``Y``, ``Z``.
        label: Human-readable label for the test vector, e.g. "(1, 0, 0)".

    Returns:
        str: Formatted multi-line table string.
    """
    display_df: pd.DataFrame = df.copy()
    display_df = display_df.rename(
        columns={"phi_deg": "Phi (deg)"}
    )

    table_str: str = display_df.to_string(
        index=False,
        justify="center",
        float_format=lambda v: f"{v:8.4f}",
    )

    line_width: int = max(len(line) for line in table_str.splitlines())

    lines: list[str] = [
        f"Test vector: [{label}]_HA",
        "-" * line_width,
        table_str,
    ]

    return "\n".join(lines)


def save_all_results(
    dfs_and_labels: list[tuple[pd.DataFrame, str]],
) -> Path:
    """Save formatted results from multiple test vectors to a single text file.

    Writes each vector's sweep as a separate section in ``data/results.txt``.

    Args:
        dfs_and_labels: List of (DataFrame, label_string) pairs.

    Returns:
        Path: The path to the saved file.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    all_lines: list[str] = []
    for i, (df, label) in enumerate(dfs_and_labels):
        if i > 0:
            all_lines.append("")
        section_lines = _build_section(df, label, i == 0)
        all_lines.append(section_lines)

    RESULTS_TXT.write_text("\n".join(all_lines), encoding="utf-8")
    return RESULTS_TXT


def _build_section(df: pd.DataFrame, label: str, is_first: bool) -> str:
    """Build one section of the results file for a single test vector.

    Args:
        df: Sweep DataFrame.
        label: Test vector label.
        is_first: Whether this section should include the file header title.

    Returns:
        str: Section text.
    """
    body = format_results_table(df, label)
    if not is_first:
        return body

    line_width: int = max(len(line) for line in body.splitlines())
    header: str = (
        "SVY 326 - Equation 2-28 Rotation Sweep Results\n"
        + "=" * line_width
        + "\n"
    )
    return header + "\n" + body
