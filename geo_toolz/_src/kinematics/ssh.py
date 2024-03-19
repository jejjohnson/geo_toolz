import xarray as xr


def calculate_ssh_alongtrack(ds: xr.Dataset) -> xr.Dataset:
    ds["ssh"] = ds.sla_filtered + ds.mdt - ds.lwe
    return ds

