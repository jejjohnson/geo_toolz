import xarray as xr
import regionmask
import numpy as np


def add_ocean_mask(ds: xr.Dataset, ocean: str="indian") -> xr.Dataset:

    # get land-sea-mask mask
    oceans = regionmask.defined_regions.natural_earth_v5_0_0.ocean_basins_50
    # 
    mask = oceans.mask_3D(ds)

    mask = mask.rename({"region": "region_ocean", "names": "names_ocean", "abbrevs": "abbrevs_ocean"})
    # create land mask variable
    # ds = ds.assign_coords({"region_ocean": mask.region})
    ds = xr.merge([ds, mask])

    return ds