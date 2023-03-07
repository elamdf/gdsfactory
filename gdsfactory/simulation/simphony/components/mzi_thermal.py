from __future__ import annotations

import numpy as np


def delta_temperature(
    wavelength: np.float64, length: np.float64, dn: np.float64 = 1.87e-4
) -> np.float64:
    """Return the delta temperature for a pi phase shift on a MZI interferometer."""
    return wavelength / 2 / length / dn


def test_delta_temperature() -> None:
    dt = delta_temperature(1.55, 100)
    np.isclose(dt, 41.44385026737968)
    dt = delta_temperature(1.55, 1000)
    np.isclose(dt, 4.44385026737968)
    # TODO maybe assert all(np.isclose) or something? This check doesn't do anything, isclose returns a bool array


if __name__ == "__main__":
    test_delta_temperature()  # FIXME this doesn't do anything- np.isclose isn't an assert
