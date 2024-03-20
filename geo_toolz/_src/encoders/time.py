from typing import Optional, Union
import numpy as np
import xarray as xr
import pandas as pd
import pint_xarray


def time_rescale(
    ds: xr.Dataset,
    freq_dt: int = 1,
    freq_unit: str = "seconds",
    t0: Optional[Union[str, np.datetime64]] = None,
) -> xr.Dataset:
    """Rescales time dimensions of np.datetim64 to an output frequency.

    t' = (t - t_0) / dt

    Args:
        ds (xr.Dataset): the xr.Dataset with a time dimensions
        freq_dt (int): the frequency of the temporal coordinate
        freq_unit (str): the unit for the time frequency parameter
        t0 (datetime64, str): the starting point. Optional. If none, assumes the
            minimum value of the time coordinate

    Returns:
        ds (xr.Dataset): the xr.Dataset with the rescaled time dimensions in the
            freq_unit.
    """

    ds = ds.copy()

    # create time delta
    time_delta = pd.Timedelta(freq_dt, unit=freq_unit)

    if t0 is None:
        t0 = ds["time"].min()

    if isinstance(t0, str):
        t0 = np.datetime64(t0)

    # rescale
    ds["time"] = (ds["time"] - t0) / time_delta

    # change dtype
    ds["time"] = ds["time"].pipe(lambda x: x.astype(np.float32))

    # change attributes
    ds["time"].attrs["units"] = time_delta.unit
    ds["time"].attrs["freq"] = freq_dt
    ds["time"].attrs["t0"] = str(t0.values)

    ds = ds.pint.quantify({"time": freq_unit}).pint.dequantify()

    return ds


def time_unrescale(
    ds: xr.Dataset,
) -> xr.Dataset:
    """Rescales time dimensions of np.datetim64 to an output frequency.

    t' = t_0 + t * dt

    Args:
        ds (xr.Dataset): the xr.Dataset with a time dimensions
        freq_dt (int): the frequency of the temporal coordinate
        freq_unit (str): the unit for the time frequency parameter
        t0 (datetime64, str): the starting point. Optional. If none, assumes the
            minimum value of the time coordinate

    Returns:
        ds (xr.Dataset): the xr.Dataset with the rescaled time dimensions in the
            freq_unit.
    """

    ds = ds.copy()

    # create time delta
    freq_dt = ds["time"].attrs["freq"]
    freq_unit = ds["time"].attrs["units"]
    time_delta = pd.Timedelta(value=freq_dt, unit=freq_unit)

    t0 = pd.to_datetime(ds["time"].attrs["t0"])

    # rescale
    ds["time"] = pd.to_datetime(t0 + ds["time"] * time_delta)

    # change attributes
    ds["time"].attrs = {}

    ds = ds.pint.quantify({"time": "ns"}).pint.dequantify()

    return ds