import xarray as xr
from .climatology import calculate_climatology, CLIMATOLOGY_DICT, calculate_daily_climatology_smoothed


def calculate_anomaly(da: xr.DataArray, freq: str="day") -> xr.DataArray:
    """
    Calculate the anomalies of a given DataArray.

    Parameters:
        da (xr.DataArray): The input DataArray.
        freq (str, optional): The frequency at which to calculate the climatology. Defaults to "dayofyear".
            Valid options are "day", "month", and "year".

    Returns:
        xr.DataArray: The anomalies of the input DataArray, calculated as the difference between the input DataArray
            and its climatology.
    """
    # calculate climatology
    da_clim = calculate_climatology(da=da, freq=freq)

    # get climatology key
    key = CLIMATOLOGY_DICT[freq]

    # Group by the climatology coordinate and calculate the mean
    return da.groupby(f"time.{key}") - da_clim


def calculate_anomaly_daily_smoothed(da: xr.DataArray) -> xr.DataArray:
    """
    Calculate the daily smoothed anomaly of a given DataArray.

    Parameters:
        da (xr.DataArray): The input DataArray.

    Returns:
        xr.DataArray: The calculated anomaly DataArray.

    """
    # calculate climatology
    da_clim = calculate_daily_climatology_smoothed(da=da)

    # Pad the data using circular padding
    da_anom = da.groupby("time.dayofyear") - da_clim

    return da_anom