from typing import Optional, Callable
import xarray as xr
import numpy as np
from .pot import calculate_pot_quantile


def count_exceedences(x, threshold, *args, **kwargs):
    """
    Counts the number of values in array `x` that exceed the given `threshold`.

    Parameters:
    - x (array-like): Input array.
    - threshold (float): Threshold value.
    - *args: Additional positional arguments.
    - **kwargs: Additional keyword arguments.

    Returns:
    - int: Number of values in `x` that exceed the `threshold`.
    """
    x = np.where(x > threshold)
    x = np.sum(x, keepdims=True)
    return x


def calculate_pp_counts_ts(da: xr.DataArray, quantile: float=0.98, time_freq: Optional[int]=5, boundary: str="trim", side: str="center") -> xr.DataArray:
    """
    Calculate the counts of exceedances for a given threshold in a time series.

    Parameters:
    - da (xr.DataArray): The input time series data.
    - quantile (float): The quantile value used to calculate the threshold for exceedances. Default is 0.98.
    - time_freq (Optional[int]): The frequency at which to reshape the time series data. Default is 5.
    - boundary (str): The boundary condition used when reshaping the time series data. Default is "trim".
    - side (str): The side used when reshaping the time series data. Default is "center".

    Returns:
    - xr.DataArray: The counts of exceedances for each time block.

    """
    # calculate threshold for point process
    threshold = calculate_pot_quantile(da, quantile=quantile)

    # reshape to non-overlapping blocks
    da = da.coarsen(time=time_freq, side=side, boundary=boundary).construct(time=("time", "block"))

    # apply ufunc to count exceedences
    extremes_counts = xr.apply_ufunc(
        count_exceedences, da.squeeze(), 
        input_core_dims=[["block"]], 
        output_core_dims=[["block"]], 
        exclude_dims=set(("block",)), 
        vectorize=True,
        kwargs=dict(threshold=threshold)
    )

    # re-add time dimension
    center_block = int(np.floor(np.mean(np.arange(0, da.time.shape[1]))))
    extremes_counts = extremes_counts.assign_coords({"time": da.time.isel(block=center_block)}).squeeze()

    return extremes_counts


def calculate_pp_stats_ts(da: xr.DataArray, fn: Callable=np.mean, quantile: float=0.98, time_freq: Optional[int]=5, boundary: str="trim", side: str="center") -> xr.DataArray:
    """
    Calculate point process statistics for a time series.

    Parameters:
    - da (xr.DataArray): The input time series data.
    - fn (Callable): The function to apply to the exceedances. Default is np.mean.
    - quantile (float): The quantile used to calculate the threshold for the point process. Default is 0.98.
    - time_freq (Optional[int]): The frequency at which to reshape the time series. Default is 5.
    - boundary (str): The boundary condition for reshaping the time series. Default is "trim".
    - side (str): The side of the blocks used for reshaping the time series. Default is "center".

    Returns:
    - xr.DataArray: The calculated point process statistics.

    """
    def stat_fn(x, threshold, *args, **kwargs):
        x = np.where(x > threshold)
        x = fn(x[0])
        x = np.atleast_1d(x)
        return x

    # calculate threshold for point process
    threshold = calculate_pot_quantile(da, quantile=quantile)

    # reshape to non-overlapping blocks
    da = da.coarsen(time=time_freq, side=side, boundary=boundary).construct(time=("time", "block"))

    # apply ufunc to count exceedences
    extremes_counts = xr.apply_ufunc(
        stat_fn, da.squeeze(), 
        input_core_dims=[["block"]], 
        output_core_dims=[["block"]], 
        exclude_dims=set(("block",)), 
        vectorize=True,
        kwargs=dict(threshold=threshold)
    )

    # re-add time dimension
    center_block = int(np.floor(np.mean(np.arange(0, da.time.shape[1]))))
    extremes_counts = extremes_counts.assign_coords({"time": da.time.isel(block=center_block)}).squeeze()

    return extremes_counts