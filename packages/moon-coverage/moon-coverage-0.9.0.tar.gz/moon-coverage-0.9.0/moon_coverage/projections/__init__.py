"""Projections module.

Projection are based on PROJ project:

    * https://proj.org/

"""

from .equi import Equirectangular
from .equi_gc import Equirectangular as EquirectangularGC
from .ticks import (
    UnitFormatter, deg_ticks, hr_ticks, km_s_ticks,
    km_ticks, lat_ticks, lon_e_ticks, lon_w_ticks
)


__all__ = [
    'Equirectangular',
    'EquirectangularGC',
    'UnitFormatter',
    'km_ticks',
    'km_s_ticks',
    'deg_ticks',
    'hr_ticks',
    'lat_ticks',
    'lon_e_ticks',
    'lon_w_ticks',
]
