import xarray as xr


def validate_ssh(ds: xr.Dataset, variable: str = 'ssh') -> xr.Dataset:
    """ Assign ssh attributes to variable """
    ds = ds.copy()
    ds[variable] = ds[variable].assign_attrs(
        units="m",
        standard_name="sea_surface_height",
        long_name="Sea Surface Height",
    )
    return ds
