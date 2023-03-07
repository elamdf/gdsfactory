"""Calculate effective index for a 1D mode."""

from __future__ import annotations

from typing import List

import numpy as np
import numpy.typing as npt
from scipy.optimize import fsolve
from typing_extensions import Literal


def get_effective_indices(
    ncore: float,
    nsubstrate: float,
    ncladding: float,
    thickness: float,
    wavelength: float,
    polarization: Literal["te", "tm"],
) -> List[float]:
    """Returns the effective refractive indices for a 1D mode.

    Args:
        epsilon_core: Relative permittivity of the film.
        epsilon_substrate: Relative permittivity of the substrate.
        epsilon_cladding: Relative permittivity of the cladding.
        thickness: Thickness of the film in um.
        wavelength: Wavelength in um.
        polarization: Either "te" or "tm".

    .. code::

        -----------------      |
        ncladding             inf
        -----------------      |
        ncore              thickness
        -----------------      |
        nsubstrate            inf
        -----------------      |

    .. code::

        import gdsfactory.simulation as sim

        neffs = sim.get_effective_indices(
            ncore=3.4777,
            ncladding=1.444,
            nsubstrate=1.444,
            thickness=0.22,
            wavelength=1.55,
            polarization="te",
        )

    """
    epsilon_core = ncore**2
    epsilon_cladding = ncladding**2
    epsilon_substrate = nsubstrate**2

    thickness *= 1e-6
    wavelength *= 1e-6

    if polarization == "te":
        tm = False
    elif polarization == "tm":
        tm = True
    else:
        raise ValueError('Polarization must be "te" or "tm"')

    k_0 = 2 * np.pi / wavelength

    # these are correctly typed, numpy type annotations don't seem to want to cooperate
    def k_f(e_eff: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        return k_0 * np.sqrt(epsilon_core - e_eff) / (epsilon_core if tm else 1)  # type: ignore

    def k_s(e_eff: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        return (  # type: ignore
            k_0 * np.sqrt(e_eff - epsilon_substrate) / (epsilon_substrate if tm else 1)
        )

    def k_c(e_eff: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        return k_0 * np.sqrt(e_eff - epsilon_cladding) / (epsilon_cladding if tm else 1)  # type: ignore

    def objective(e_eff: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        return 1 / np.tan(k_f(e_eff) * thickness) - (  # type: ignore
            k_f(e_eff) ** 2 - k_s(e_eff) * k_c(e_eff)
        ) / (k_f(e_eff) * (k_s(e_eff) + k_c(e_eff)))

    # scan roughly for indices
    # use a by 1e-10 smaller search area to avoid division by zero
    x = np.linspace(
        min(epsilon_substrate, epsilon_cladding) + 1e-10, epsilon_core - 1e-10, 1000
    )
    indices_temp = x[np.abs(objective(x)) < 0.1]
    if not len(indices_temp):
        return []

    # and then use fsolve to get exact indices
    indices_temp = fsolve(objective, indices_temp)

    indices: list[float] = []
    for index in indices_temp:
        if not any(np.isclose(index, i, atol=1e-5) for i in indices):
            indices.append(index)

    # cast to please mypy
    return list(np.sqrt(indices).tolist())


def test_effective_index() -> None:
    neff = get_effective_indices(
        ncore=3.4777,
        ncladding=1.444,
        nsubstrate=1.444,
        thickness=0.22,
        wavelength=1.55,
        polarization="te",
    )
    assert np.isclose(neff[0], 2.8494636999424405)


if __name__ == "__main__":
    print(
        get_effective_indices(
            ncore=3.4777,
            ncladding=1.444,
            nsubstrate=1.444,
            thickness=0.22,
            wavelength=1.55,
            polarization="te",
        )
    )
