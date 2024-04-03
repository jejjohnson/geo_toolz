import xarray as xr
import regionmask
import numpy as np


def add_ocean_mask(ds: xr.Dataset, ocean: str="indian") -> xr.Dataset:

    # get land-sea-mask mask
    oceans = regionmask.defined_regions.natural_earth_v5_0_0.ocean_basins_50
    # 
    mask = oceans.mask_3D(ds)

    ds[f"ocean_mask"] = mask.isel(region=(mask.names==ocean)).squeeze().astype(np.int16)

    ds = ds.assign_coords({f"ocean_mask": ds[f"ocean_mask"]})
    # remove extra variables
    ds[f"ocean_mask"].attrs["region"] = ds["region"].values
    ds[f"ocean_mask"].attrs["abbrevs"] = ds["abbrevs"].values
    ds[f"ocean_mask"].attrs["standard_name"] = "ocean_mask"
    ds[f"ocean_mask"].attrs["full_name"] = "Ocean Mask"

    # drop variables
    ds = ds.drop_vars(["region", "names", "abbrevs"])

    return ds