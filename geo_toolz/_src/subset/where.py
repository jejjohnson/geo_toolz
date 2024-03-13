import xarray as xr

def where_slice(ds: xr.Dataset, variable: str, min_val: float, max_val: float, drop=True) -> xr.Dataset:

    ds = ds.where(
        (ds[variable] >= float(min_val)) & (ds[variable] <= float(max_val)),
        drop=drop
    )
        
    return ds