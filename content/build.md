# Construction of the Illuminator

The illuminator was easily constructed with off-the-shelf parts. My colleague and I worked in tandem with a Thorlabs application specialist to identify the parts.

## Image of the Illuminator

:::{figure} led_illuminator.jpg
:label: fig:illuminator

The finished LED illuminator.
:::

## Parts List

| Part Name | Thorlabs Part # | Quantity | URL |
|---|---|---|---|
| LED | M450LP2 | 1 | <https://www.thorlabs.com/thorproduct.cfm?partnumber=M450LP2> |
| LED Driver | DC40 | 1 | <https://www.thorlabs.com/thorproduct.cfm?partnumber=DC40> |
| Collimator | SM1U25-A | 1 | <https://www.thorlabs.com/thorproduct.cfm?partnumber=SM1U25-A> |
| Adapter | SMA38 | 1 | <https://www.thorlabs.com/thorproduct.cfm?partnumber=SMA38> |
| Bandpass Filter (FWHM 40 nm) | FBH450-40 | 1 | <https://www.thorlabs.com/thorproduct.cfm?partnumber=FBH450-40> |
| Lens Tube | SM1L10 | 1 | <https://www.thorlabs.com/thorproduct.cfm?partnumber=SM1L10> |
| Rotation Mount | CLR1/M | 1 | <https://www.thorlabs.com/thorproduct.cfm?partnumber=CLR1/M> |
| Adapter | SM1T2 | 1 | <https://www.thorlabs.com/thorproduct.cfm?partnumber=SM1T2> |
| Linear Polarizer | LPVISE100-A | 1 | <https://www.thorlabs.com/thorproduct.cfm?partnumber=LPVISE100-A> |
| Quarter Waveplate | WPQ10M-445 | 1 | <https://www.thorlabs.com/thorproduct.cfm?partnumber=WPQ10M-445> |

## Build Notes

- The waveplate comes mounted. To remove it from its mount and insert it into the CLR1/M rotation mount, you must remove both the retainer ring **and the small rubber O-ring** before extracting the waveplate.
- The linear polarizer can be mounted statically inside the SM1L10 lens tube between 2 retainer rings. I used a polarimeter as feedback when rotating the waveplate and aligning it to the polarizer.
- The SM1T2 adapter is the weak point in this setup. The lock rings are not strong enough to prevent rotation of either the lens tube or the rotation, which makes it easy to ruin the alignment when handling the illuminator. I should investigate an alternative coupling mechanism in the future.
