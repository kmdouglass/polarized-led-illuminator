from dataclasses import dataclass

import numpy as np
import optiland.backend as be
from optiland import optic
from optiland.rays import PolarizationState
from optiland.rays.real_rays import RealRays


class Collimator(optic.Optic):
    def __init__(self) -> None:
        super().__init__()
        

        self.add_surface(index=0, thickness=13.0512, material="Air")   # Air gap before lens
        self.add_surface(index=1, thickness=12.0163, material="B270", is_stop=True)  # Planar surface
        self.add_surface(
            index=2,
            thickness=25.0,
            material="Air",
           radius=-10.462,
           conic=-0.6265,
           surface_type="even_asphere",
           coefficients=[0.0, 1.5e-5]  # Aspheric surface
        )
        self.add_surface(index=3)

        self.set_aperture("float_by_stop_size", 22.5)

        self.set_field_type(field_type="object_height")
        self.add_field(y=0.0)
        self.add_field(y=-1.06)

        self.add_wavelength(0.45, is_primary=True)
    

@dataclass
class LED:
    length_x_mm: float = 1.5
    length_y_mm: float = 1.5
    viewing_angle_deg: float = 120.0
    center_wavelength_um: float = 0.45
    fwhm_wavelength_um: float = 0.018

    def lambertian_order(self) -> float:
        """Compute the Lambertian order of the LED from its viewing angle."""
        theta_half_rad = np.deg2rad(self.viewing_angle_deg / 2.0)
        m = -np.log(2) / np.log(np.cos(theta_half_rad))
        return m

    def generate_rays(self, num_rays: int, power_watts: float = 3.0) -> RealRays:
        x_min, x_max = -self.length_x_mm / 2.0, self.length_x_mm / 2.0
        y_min, y_max = -self.length_y_mm / 2.0, self.length_y_mm / 2.0

        # Random starting positions on the LED surface
        x, y = np.random.uniform(x_min, x_max, num_rays), np.random.uniform(y_min, y_max, num_rays)
        z = np.zeros(num_rays)

        # Random directions based on generalized Lambertian distribution
        u, phi = np.random.uniform(0, 1, num_rays), np.random.uniform(0, 2 * np.pi, num_rays)
        theta = np.arccos((1 - u) ** (1 / (self.lambertian_order() + 1)))

        # Direction cosines
        l = np.sin(theta) * np.cos(phi)
        m = np.sin(theta) * np.sin(phi)
        n = np.cos(theta)

        # Ray intensities
        watts_per_ray = np.full(num_rays, power_watts / num_rays)

        # Wavelengths
        wavelengths_um = np.random.normal(
            loc=self.center_wavelength_um, scale=self.fwhm_wavelength_um / 2.355, size=num_rays
        )

        return RealRays(x, y, z, l, m, n, watts_per_ray, wavelengths_um)


def propagate_to_z(rays, z_target):
    """Free-space drift of ray (x, y) to a target z plane."""
    dz = z_target - be.to_numpy(rays.z)
    x = be.to_numpy(rays.x) + be.to_numpy(rays.L) / be.to_numpy(rays.N) * dz
    y = be.to_numpy(rays.y) + be.to_numpy(rays.M) / be.to_numpy(rays.N) * dz
    return x, y


def _finite_mask(*arrays):
    """Rays vignetted upstream carry NaN x/y/z/i - drop them before binning."""
    mask = np.ones(arrays[0].shape, dtype=bool)
    for a in arrays:
        mask &= np.isfinite(a)
    return mask


def beam_radius(rays, z_target):
    """Max |x| or |y| among surviving rays at z_target - used to size a fixed
    grid extent so heat maps at different z share the same pixel scale."""
    x, y = propagate_to_z(rays, z_target)
    power = be.to_numpy(rays.i)
    valid = _finite_mask(x, y, power) & (power > 0)
    x, y = x[valid], y[valid]
    return max(np.abs(x).max(), np.abs(y).max())


def irradiance_map(rays, z_target, bins=128, extent=None):
    x, y = propagate_to_z(rays, z_target)
    power = be.to_numpy(rays.i)
    valid = _finite_mask(x, y, power) & (power > 0)
    x, y, power = x[valid], y[valid], power[valid]

    if extent is None:
        r = max(np.abs(x).max(), np.abs(y).max())
        extent = (-r, r, -r, r)
    x_edges = np.linspace(extent[0], extent[1], bins + 1)
    y_edges = np.linspace(extent[2], extent[3], bins + 1)

    hist, _, _ = np.histogram2d(x, y, bins=[x_edges, y_edges], weights=power)
    pixel_area = (x_edges[1] - x_edges[0]) * (y_edges[1] - y_edges[0])
    return hist / pixel_area, x_edges, y_edges


def stokes_components(rays):
    """Per-ray Stokes parameters, decomposing an unpolarized source into an
    incoherent 50/50 mix of two orthogonal input states (same convention as
    `PolarizedRays.update_intensity` for `is_polarized=False`)."""
    state_x = PolarizationState(is_polarized=True, Ex=1.0, Ey=0.0, phase_x=0.0, phase_y=0.0)
    state_y = PolarizationState(is_polarized=True, Ex=0.0, Ey=1.0, phase_x=0.0, phase_y=0.0)

    E1_x = be.to_numpy(rays.get_output_field(rays._get_3d_electric_field(state_x)))
    E1_y = be.to_numpy(rays.get_output_field(rays._get_3d_electric_field(state_y)))
    i0 = be.to_numpy(rays._i0)

    Ex1, Ey1 = E1_x[:, 0], E1_x[:, 1]   # global-frame transverse components
    Ex2, Ey2 = E1_y[:, 0], E1_y[:, 1]

    S0 = 0.5 * (np.abs(Ex1) ** 2 + np.abs(Ey1) ** 2 + np.abs(Ex2) ** 2 + np.abs(Ey2) ** 2) * i0
    S1 = 0.5 * (np.abs(Ex1) ** 2 - np.abs(Ey1) ** 2 + np.abs(Ex2) ** 2 - np.abs(Ey2) ** 2) * i0
    S2 = (np.real(Ex1 * np.conj(Ey1)) + np.real(Ex2 * np.conj(Ey2))) * i0
    S3 = (np.imag(Ex1 * np.conj(Ey1)) + np.imag(Ex2 * np.conj(Ey2))) * i0
    return S0, S1, S2, S3   # S0 equals rays.i after update_intensity(is_polarized=False)


def stokes_map(rays, z_target, bins=128, extent=None):
    x, y = propagate_to_z(rays, z_target)
    S0, S1, S2, S3 = stokes_components(rays)
    valid = _finite_mask(x, y, S0, S1, S2, S3) & (S0 > 0)
    x, y = x[valid], y[valid]
    S0, S1, S2, S3 = S0[valid], S1[valid], S2[valid], S3[valid]

    if extent is None:
        r = max(np.abs(x).max(), np.abs(y).max())
        extent = (-r, r, -r, r)
    x_edges = np.linspace(extent[0], extent[1], bins + 1)
    y_edges = np.linspace(extent[2], extent[3], bins + 1)

    maps = [np.histogram2d(x, y, bins=[x_edges, y_edges], weights=S)[0] for S in (S0, S1, S2, S3)]
    return (*maps, x_edges, y_edges)
