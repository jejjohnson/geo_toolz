import numpy as np
import xarray as xr
import regionmask


def add_country_mask(ds: xr.Dataset, country: str="Spain") -> xr.Dataset:

    # get countries mask
    countries = regionmask.defined_regions.natural_earth_v5_0_0.countries_110

    # create mask variable
    mask = countries.mask_3D(ds)

    # select Spain mask
    var_name = country.lower()
    ds[f"{var_name}_mask"] = mask.isel(region=(mask.names==country)).squeeze().astype(np.int16)

    ds = ds.assign_coords({f"{var_name}_mask": ds[f"{var_name}_mask"]})
    # remove extra variables
    ds[f"{var_name}_mask"].attrs["region"] = ds["region"].values
    ds[f"{var_name}_mask"].attrs["abbrevs"] = ds["abbrevs"].values
    ds[f"{var_name}_mask"].attrs["standard_name"] = country.lower()
    ds[f"{var_name}_mask"].attrs["full_name"] = country.capitalize()

    # drop variables
    ds = ds.drop_vars(["region", "names", "abbrevs"])

    return ds
