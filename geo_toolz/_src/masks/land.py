import xarray as xr
import regionmask
import numpy as np


def add_land_mask(ds: xr.Dataset) -> xr.Dataset:

    # get land-sea-mask mask
    land_110 = regionmask.defined_regions.natural_earth_v5_0_0.land_110
    # create land mask variable
    ds["land_mask"] = land_110.mask_3D(ds).squeeze().astype(np.int16)

    ds = ds.assign_coords({f"land_mask": ds[f"land_mask"]})
    # remove extra variables
    ds[f"land_mask"].attrs["region"] = ds["region"].values
    ds[f"land_mask"].attrs["abbrevs"] = ds["abbrevs"].values
    ds[f"land_mask"].attrs["standard_name"] = "land_mask"
    ds[f"land_mask"].attrs["full_name"] = "Land Mask"

    # drop variables
    ds = ds.drop_vars(["region", "names", "abbrevs"])
    

    return ds