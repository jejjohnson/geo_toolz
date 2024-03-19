from dataclasses import dataclass
from typing import Tuple
import xarray as xr
import pyinterp
from odc.geo.xr import xr_coords
from odc.geo.geom import BoundingBox
from odc.geo.geobox import GeoBox
from geo_toolz._src.validation.coords import validate_latitude, validate_longitude
from geo_toolz._src.discretize.period import Period


@dataclass
class RegularLonLat:
    bbox: BoundingBox
    resolution: float
    gbox: GeoBox
    coordinates: xr.Dataset

    @classmethod
    def init_from_bounds(cls, lon_bnds: Tuple[float, float], lat_bnds: Tuple[float, float], resolution: float):

        # initialize bounding box
        bbox = BoundingBox.from_xy(x=lon_bnds, y=lat_bnds, crs="4326")
        
        # initialize geobox
        gbox = GeoBox.from_bbox(bbox, resolution=resolution, crs="4326")

        # create xarray coordinates
        coords = xr.Dataset(xr_coords(gbox))
        coords = validate_latitude(coords)
        coords = validate_longitude(coords)
        return cls(bbox=bbox, resolution=resolution, gbox=gbox, coordinates=coords)

    @property
    def binning(self):
        return pyinterp.Binning2D(
            x=pyinterp.Axis(self.coordinates.lon.values),
            y=pyinterp.Axis(self.coordinates.lat.values),
        )


@dataclass
class RegularLonLatTime:
    bbox: BoundingBox
    resolution: float
    gbox: GeoBox
    coordinates: xr.Dataset

    @classmethod
    def init_from_bounds(
        cls, 
        lon_bnds: Tuple[float, float], 
        lat_bnds: Tuple[float, float], 
        resolution: float,
        time_min: str,
        time_max: str,
        time_step: float,
        time_unit: str
        ):

        # initialize bounding box
        bbox = BoundingBox.from_xy(x=lon_bnds, y=lat_bnds, crs="4326")

        gbox = GeoBox.from_bbox(bbox, resolution=resolution, crs="4326")

        # create xarray coordinates
        coords = xr.Dataset(xr_coords(gbox))
        coords = validate_latitude(coords)
        coords = validate_longitude(coords)
        # time coordinates
        period = Period(time_min=time_min, time_max=time_max, freq_step=time_step, unit=time_unit)
        coords = coords.assign_coords({"time": period.date_range})
        return cls(bbox=bbox, resolution=resolution, gbox=gbox, coordinates=coords)
    
    @classmethod
    def init_from_grid_and_period(
        cls,
        grid: RegularLonLat,
        period: Period,
    ):
        
        coords = grid.coordinates
        coords = coords.assign_coords({"time": period.date_range})
        return cls(bbox=grid.bbox, gbox=grid.gbox, resolution=grid.resolution, coordinates=coords)

    @property
    def binning(self):
        return pyinterp.Binning2D(
            x=pyinterp.Axis(self.coordinates.lon.values),
            y=pyinterp.Axis(self.coordinates.lat.values),
        )
