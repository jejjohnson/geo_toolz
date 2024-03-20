from typing import Optional
import xarray as xr
from .bm import calculate_block_maxima_ts


def calculate_pot_quantile(da: xr.DataArray, quantile: float=0.98) -> float:
    """
    Calculate the quantile value for a given DataArray.

    Parameters:
        da (xr.DataArray): The input DataArray.
        quantile (float, optional): The quantile value to calculate (default is 0.98).

    Returns:
        float: The quantile value.

    """
    return da.quantile(q=[quantile], dim="time").values


def calculate_pot_ts(da: xr.DataArray, quantile: float=0.98, decluster_freq: Optional[int]=None) -> xr.DataArray:
    """
    Calculate the Peaks Over Threshold (POT) time series.

    Parameters:
        da (xr.DataArray): The input data array.
        quantile (float, optional): The quantile value used to calculate the threshold for POT. Defaults to 0.98.
        decluster_freq (int, optional): The frequency at which declustering is performed. If not provided, declustering is not performed.

    Returns:
        xr.DataArray: The POT time series.

    """
    # calculate threshold for pot
    threshold = calculate_pot_quantile(da, quantile=quantile)

    # select points above threshold
    da = da.where(da >= threshold, drop=False if decluster_freq is not None else True)

    # run declustering
    if decluster_freq is not None:
        da = calculate_block_maxima_ts(da, decluster_freq).dropna(dim="time")

    return da