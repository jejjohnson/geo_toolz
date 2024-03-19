from typing import List, Optional
from tqdm.auto import tqdm
import xarray as xr
import numpy as np
from geo_toolz._src.discretize.grid import RegularLonLat, RegularLonLatTime
from geo_toolz._src.validation.coords import validate_latitude, validate_longitude


def da_binning_2D(da: xr.DataArray, target_grid: RegularLonLat, statistics: str="mean") -> xr.DataArray:
    """
    Bins a 2D xr.DataArray onto a target grid using the specified statistics.

    Parameters:
    da (xr.DataArray): The input 2D xr.DataArray with lon and lat coordinates.
    target_grid (RegularLonLat): The target grid onto which the data will be binned.
    statistics (str, optional): The statistics to be computed for each bin. Defaults to "mean".

    Returns:
    xr.DataArray: The binned xr.DataArray.

    """
    binning = target_grid.binning

    new_da = apply_binning_2D(da, binning=binning, statistics=statistics)
    
    return new_da


def apply_binning_2D(da: xr.DataArray, binning, statistics: str="mean") -> xr.DataArray:
    """
    Apply 2D binning to a DataArray.

    Parameters:
    - da (xr.DataArray): The input DataArray with lon and lat coordinates.
    - binning (pyinterp.Binning): The binning object.
    - statistics (str, optional): The statistics to compute for each bin. Default is "mean".

    Returns:
    - xr.DataArray: The binned DataArray.

    Notes:
    - The binning object is modified in-place.
    - The input DataArray should have lon and lat coordinates.

    Example:
    >>> da = xr.DataArray(...)
    >>> binning = pyinterp.Binning(...)
    >>> binned_da = apply_binning_2D(da, binning, statistics="mean")
    """

    binning.clear()
    values = np.ravel(da.values)
    lons = np.ravel(da.lon.values)
    lats = np.ravel(da.lat.values)
    msk = np.isfinite(values)
    binning.push(lons[msk], lats[msk], values[msk])
    binned_values = binning.variable(statistics=statistics).T
    new_da = xr.DataArray(
        data=binned_values, 
        coords={"lon": np.array(binning.x), "lat": np.array(binning.y)},
        name=da.name,
        attrs=da.attrs
    )

    # keep attributes on coordinates
    new_da = validate_latitude(new_da)
    new_da = validate_longitude(new_da)
    
    return new_da


def da_binning_2D_Time(da: xr.DataArray, target_grid: RegularLonLatTime, statistics: str="mean") -> xr.DataArray:
    """
    Perform 2D binning of a DataArray along the time dimension.

    Parameters:
    - da (xr.DataArray): The input DataArray with lon and lat coordinates.
    - target_grid (RegularLonLatTime): The target grid for binning.
    - statistics (str, optional): The statistics to compute for each bin. Default is "mean".

    Returns:
    - xr.DataArray: The binned DataArray along the time dimension.

    """
    time_coords = target_grid.coordinates.time

    t_res = time_coords.diff("time").values.mean()
    
    # grab binning
    binning = target_grid.binning

    grid_das = []

    for time in tqdm(time_coords):
        # subset the data
        ids = da.isel(time=(da.time > (time - t_res / 2)) & (da.time <= (time + t_res / 2)))
        # apply 2D binning
        ids = apply_binning_2D(ids, binning=binning, statistics=statistics)
        # assign time coordinates
        ids = ids.assign_coords({"time": time.values})
        # stack grid
        grid_das.append(ids)

    # combine all grids
    grid_das = xr.concat(grid_das, dim="time")
    
    return grid_das


# TODO: Dataset Version with multiple variables
def ds_binning_2D_Time(ds: xr.Dataset, target_grid: RegularLonLatTime, statistics: str="mean", data_vars: Optional[List[str]]=None) -> xr.Dataset:
    """


    Perform 2D binning of a DataArray along the time dimension.

    Parameters:
    - da (xr.DataArray): The input DataArray with lon and lat coordinates.
    - target_grid (RegularLonLatTime): The target grid for binning.
    - statistics (str, optional): The statistics to compute for each bin. Default is "mean".

    Returns:
    - xr.DataArray: The binned DataArray along the time dimension.

    """
    if data_vars is None:
        data_vars = set(ds.variables) - {"time", "lat", "lon"}

    time_coords = target_grid.coordinates.time

    t_res = time_coords.diff("time").values.mean()
    
    # grab binning
    binning = target_grid.binning

    grid_das = []

    for time in tqdm(time_coords):
        # subset the data
        ids = ds.isel(time=(ds.time > (time - t_res / 2)) & (ds.time <= (time + t_res / 2)))
        # apply 2D binning
        ids = {v: apply_binning_2D(ids[v], binning=binning, statistics=statistics) for v in data_vars}
        # assign time coordinates
        ids = xr.Dataset(ids)
        ids = ids.assign_coords({"time": time.values})
        # stack grid
        grid_das.append(ids)

    # combine all grids
    grid_das = xr.concat(grid_das, dim="time")
    
    return grid_das

def to_dim(ds, v):
    """
    ds: xr.Dataset
    v: one dimensional variable or coordinates name

    Return: xr.Dataset  with v as a dimension
    """
    if v in ds.dims:
        return ds
    return ds.swap_dims({ds[v].dims[0]: v})