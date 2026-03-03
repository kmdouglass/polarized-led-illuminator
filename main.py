from dataclasses import dataclass

import numpy as np
from optiland import optic
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
        watts_per_ray = power_watts / num_rays

        # Wavelengths
        wavelengths_um = np.random.normal(
            loc=self.center_wavelength_um, scale=self.fwhm_wavelength_um / 2.355, size=num_rays
        )

        return RealRays(x, y, z, l, m, n, watts_per_ray, wavelengths_um)
