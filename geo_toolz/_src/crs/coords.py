from typing import List, Tuple
import numpy as np
import xarray as xr
from pyproj import Transformer



def convert_lat_lon_to_x_y(crs: str, lon: List[float], lat: List[float]) -> Tuple[float, float]:
    """
    Converts latitude and longitude coordinates to x and y coordinates in the specified CRS.

    Args:
        crs (str): The target coordinate reference system (CRS) to convert to.
        lon (List[float]): A list of longitude values.
        lat (List[float]): A list of latitude values.

    Returns:
        Tuple[float, float]: A tuple containing the x and y coordinates in the specified CRS.
    """
    transformer = Transformer.from_crs("epsg:4326", crs, always_xy=True)
    x, y = transformer.transform(lon, lat)
    return x, y


def convert_x_y_to_lat_lon(crs: str, x: List[float], y: List[float]) -> Tuple[float, float]:
    """
    Converts x and y coordinates to latitude and longitude using the specified CRS.

    Args:
        crs (str): The coordinate reference system (CRS) of the input coordinates.
        x (List[float]): The x-coordinates to be converted.
        y (List[float]): The y-coordinates to be converted.

    Returns:
        Tuple[float, float]: A tuple containing the converted longitude and latitude values.
    """
    transformer = Transformer.from_crs(crs, "epsg:4326", always_xy=True)
    lon, lat = transformer.transform(x, y)
    return lon, lat


def calc_latlon(ds: xr.Dataset) -> xr.Dataset:
    """
    Calculate the latitude and longitude coordinates for the given dataset

    Args:
        ds (xr.Dataset): Xarray Dataset to calculate the lat/lon coordinates for, with x and y coordinates

    Returns:
        xr.Dataset: Xarray Dataset with the latitude and longitude coordinates added
    """
    XX, YY = np.meshgrid(ds.x.data, ds.y.data)
    lons, lats = convert_x_y_to_lat_lon(ds.rio.crs, XX, YY)
    # Check if lons and lons_trans are close in value
    # Set inf to NaN values
    lons[lons == np.inf] = np.nan
    lats[lats == np.inf] = np.nan

    ds = ds.assign_coords({"latitude": (["y", "x"], lats), "longitude": (["y", "x"], lons)})
    ds.latitude.attrs["units"] = "degrees_north"
    ds.longitude.attrs["units"] = "degrees_east"
    return ds