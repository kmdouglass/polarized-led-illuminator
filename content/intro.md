# Introduction

I was recently asked by a colleague in biophysics to design a module that would illuminate proteins with circularly polarized light. The purpose is to use the light as a switch that induces a reversible change in the proteins' conformations, making them sensitive to certain environmental markers. In this stage of the project, the proteins simply sit in solution in a standard 3 mL cuvette ( 10 mm x 10 mm x 30 mm ) under constant illumination. Their conformational state and their reactions to the different environmental perturbations are monitored at the same time by a photospectrometer.

As in most basic research projects, the requirements for this design are sparse. Since the probability that a protein will absorb a photon is proportional to the irradiance across the protein's cross section, I decided that the primary design goal should be to make the irradiance as uniform as possible throughout the length of the cuvette. This would help minimize any confounding factors due to a differential rate of absorption inside the cuvette. My colleague additionally insisted that the light be circularly polarized. I doubt that the polarization state of the light will ultimately matter much because the absorption dipole moment of the proteins in solution will undergo constant and fast Brownian rotation.

:::{figure} led-illuminator-schema.png
:label: fig:project_schema

A graphical schema of the project's concept. Proteins in solution are illuminated from above by circularly polarized light and from the side by probe light from a spectrophotometer.
:::
