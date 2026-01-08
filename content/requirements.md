# Requirements

## Discussion

I took the following notes during a discussion with my colleague to better understand the scope of the project.

- The proteins exist in two states: active and inactive.
  - In the absence of blue light they are inactive.
  - Under illumination by blue light they will transition to the active state.
- The proteins become sensitive to environmental disturbances in the active state.
  - The nature of these disturbances are outside the scope of this design document.
- The proteins are supposedly very sensitive to illumination by blue light. Exposure to even very small doses will cause them to rapidly transition to the active state.
  - No hard numbers were given, but I got the impression that very little light is required.
- Once the illumination is removed, the proteins will stay in the active state for timescales between seconds to days. They will naturally return to the inactive state.
- The proteins will diffuse and reorient freely within solution due to Brownian motion.

### Model of Protein State Transitions

From the discussion summarized above I understand that the protein state model looks like the following:

:::{figure} protein_state_model.png
:label: fig:protein_state_model

The state model for the proteins. The rate constant to switch from the inactive to the active state $k_{ON}$ is proportional to the irradiance $E_e$ integrated across the protein's absorption cross section. The rate constant to switch from the active to the inactive state is $k_{OFF}$.
:::

Strictly speaking $k_{ON}$ should also depend on the angle between the light's electric field vector (the polarization direction) and the orientation of the protein's absorption dipole moment. I assume that thermal fluctations of the protein's orientation result in an effectively complete sampling of directions on time scales much shorter than an experiment. In other words, the polarization should not matter much.

## Requirements

This is a basic research project. Priority is placed on making something work, even if imperfectly, just to see if the protein's sensitivity to the environment is measurable and can be switched on and off as expected.

- The irradiance should be nearly constant across all cross sections through the cuvette.
  - This is desirable but not essential because:
    - The proteins will diffuse rapidly through the volume of the cuvette, effectively averaging over any inhomogenities in the illumination.
    - The proteins response to the light is supposedly very rapid and they are slow to return to the inactive state. Pumping them all into the active state should therefore take at most a few seconds.
- The illumination should be circularly polarized.
  - My colleague insisted on this to better ensure absorption of illumination photons by the proteins.
  - I doubt that it matters very much in solution due thermal reorientation of the proteins' absorption dipole moments.
