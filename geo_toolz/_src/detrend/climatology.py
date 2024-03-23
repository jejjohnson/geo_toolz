from typing import List, Dict
import xarray as xr


SEASONS_DICT = dict(0='DJF', 1='MAM', 2='JJA', 3='SON')
CLIMATOLOGY_DICT = dict(day="dayofyear", month="month", year="year")


def calculate_climatology(da: xr.DataArray, freq: str="day") -> xr.DataArray:
    """
    Calculate the climatology of a given DataArray.

    Parameters:
        da (xr.DataArray): The input DataArray.
        freq (str, optional): The frequency at which to calculate the climatology. Defaults to "dayofyear".
        ( "month", "year" )

    Returns:
        xr.DataArray: The climatology of the input DataArray.
    """
    # get climatology key
    key = CLIMATOLOGY_DICT[freq]

    # Group by the climatology coordinate and calculate the mean
    return da.groupby(f"time.{key}").mean('time')


def calculate_daily_climatology_smoothed(da: xr.DataArray) -> xr.DataArray:
    """
    Calculate the smoothed climatology of a given DataArray.
    Applies a +/- 30 day circular boundary conditions to the climatology.
    Takes a rolling mean. Selects the middle days.

    Parameters:
        da (xr.DataArray): The input DataArray.

    Returns:
        xr.DataArray: The smoothed climatology of the input DataArray.
    """
    # get climatology key
    da_clim = calculate_climatology(da=da, freq="day")

    # Pad the data using circular padding
    da_clim = da_clim.pad(dayofyear=(30, 30), mode='wrap')

    # Apply the rolling window with circular boundary conditions
    da_clim = da_clim.rolling(dayofyear=60, center=True, min_periods=1).mean()

    # select the middle points
    da_clim = da_clim.isel(dayofyear=slice(30, -30))

    return da_clim


def calculate_climatology_season(da: xr.DataArray, seasons_dict: Dict=SEASONS_DICT) -> xr.DataArray:
    """
    Calculate the climatology for each season in the given DataArray.

    Parameters:
    - da (xr.DataArray): The input DataArray containing the data.
    - seasons_dict (Dict): A dictionary mapping month numbers to season names.

    Returns:
    - xr.DataArray: The calculated climatology for each season.

    """
    # Map the season string to the month of the DataArray
    da['season'] = da['time.month'].map(seasons_dict)

    # Group by the new season coordinate and calculate the mean
    return da.groupby('season').mean('time')
