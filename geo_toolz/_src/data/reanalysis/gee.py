from typing import Optional
import ee
import xarray as xr
from geo_toolz._src.discretize.grid import RegularLonLat


GEE_ERA5_DATASETS_NAMES = dict(
    era5_land_hourly="ECMWF/ERA5_LAND/HOURLY",
    era5_land_daily="ECMWF/ERA5_LAND/DAILY_AGGR",
    era5_land_monthly="ECMWF/ERA5_LAND/MONTHLY_AGGR",
    era5_daily="ECMWF/ERA5/DAILY",
    era5_monthly="ECMWF/ERA5/MONTHLY"
)

def download_era5_gee(dataset: str, bbox: Optional[RegularLonLat]=None, crs: str="EPSG:4326", scale: Optional[float]=None) -> xr.Dataset:

    # initialize GEE
    ee.Initialize(opt_url='https://earthengine-highvolume.googleapis.com')
    # get image collection
    ic = ee.ImageCollection(GEE_ERA5_DATASETS_NAMES[dataset])

    # get geometry
    if bbox is not None:
        geometry = ee.Geometry.BBox(*bbox.bbox)
    else:
        geometry = None

    # get projection
    projection = ic.first().select(0).projection()

    return xr.open_dataset(ic, engine='ee', crs=crs, scale=scale, projection=projection, geometry=geometry)