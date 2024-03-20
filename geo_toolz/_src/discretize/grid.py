from dataclasses import dataclass
from typing import Tuple
import xarray as xr
import pyinterp
from odc.geo.xr import xr_coords
from odc.geo.geom import BoundingBox
from odc.geo.geobox import GeoBox
from odc.geo.geom import Geometry
from odc.geo.crs import CRS
from geo_toolz._src.validation.coords import validate_latitude, validate_longitude
from geo_toolz._src.discretize.period import Period
import regionmask


@dataclass
class RegularLonLat:
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
        return cls(resolution=resolution, gbox=gbox, coordinates=coords)
    
    @property
    def bbox(self):
        return self.gbox.boundingbox
    
    @classmethod
    def init_from_country(cls, country: str, resolution: float):

        # get countries
        countries = regionmask.defined_regions.natural_earth_v5_0_0.countries_110

        # get polygon
        polygon = countries[country.upper()].polygon

        # convert it to geometry
        odc_crs = CRS("EPSG:4326")
        odc_geom = Geometry(geom=polygon, crs=odc_crs)
        
        # initialize geobox
        gbox = GeoBox.from_geopolygon(odc_geom, resolution=resolution, crs=odc_crs)

        # create xarray coordinates
        coords = xr.Dataset(xr_coords(gbox))
        coords = validate_latitude(coords)
        coords = validate_longitude(coords)
        return cls(resolution=resolution, gbox=gbox, coordinates=coords)

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


def init_bounds_from_country(country: str="spain") -> BoundingBox:

    # get countries
    countries = regionmask.defined_regions.natural_earth_v5_0_0.countries_110

    # select country
    country = countries[country]

    return None