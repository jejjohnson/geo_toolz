---
title: GeoSoftware
subject: Machine Learning for Earth Observations
short_title: GeoSoftware
authors:
  - name: J. Emmanuel Johnson
    affiliations:
      - CSIC
      - UCM
      - IGEO
    orcid: 0000-0002-6739-0053
    email: juanjohn@ucm.es
license: CC-BY-4.0
keywords: simulations
---



**File Management**

* [pathlib](https://docs.python.org/3/library/pathlib.html)
* [fsspec](https://github.com/fsspec)
* [upath](https://github.com/fsspec/universal_pathlib)
* **[CloudPathLib](https://github.com/drivendataorg/cloudpathlib)** - nice package for dealing with cloud data.
* [toolz](https://toolz.readthedocs.io/en/latest/api.html)

**Data Management**

* [dvc](https://dvc.org/)

**Satellites**

* [SatPy](https://satpy.readthedocs.io/en/stable/) - read some common satellite data into xarray datasets.
* [GeoWombat](https://geowombat.readthedocs.io/en/latest/index.html) - General purpose raster processor


***

**Vectors**

* [GeoCube](https://corteva.github.io/geocube/latest/index.html) - compatibility between rasters and vectors

***

**Coordinate Projections**

* [GeoBox](https://github.com/opendatacube/odc-geo) - A great little library for handling coordinates and projections. [GeoCube-Rioxarray Compatibility](https://github.com/corteva/geocube/blob/master/geocube/geo_utils/geobox.py)
* [rioxarray](https://corteva.github.io/rioxarray/stable/) - rasterio and xarray compatibility

***

**Math**

* [xarray-einstats](https://einstats.python.arviz.org/en/latest/) - linear algebra, Einops and statistics
* [xskillscore](https://github.com/xarray-contrib/xskillscore) - pixel-wise metrics using ufuncs 
* [xrft](https://github.com/xgcm/xrft) - Fourier transforms 
* [xeofs](https://github.com/xarray-contrib/xeofs) - empirical orthogonal functions (PCA)
* [MetPy](https://unidata.github.io/MetPy/latest/index.html) - derivatives and geophysical calculations
* [xinvert](https://xinvert.readthedocs.io/en/latest/) - Poisson equation inversion with numba
* [pint-xarray](https://pint-xarray.readthedocs.io/en/stable/index.html) - units aware xarray

***

**Interpolation**

* [xarray-regrid](https://github.com/EXCITED-CO2/xarray-regrid) - regrid rectilinear grids
* [pyinterp](https://pangeo-pyinterp.readthedocs.io/en/latest/) - interpolation for unstructured grids and nans
* [xesmf](https://pangeo-xesmf.readthedocs.io/en/latest/) - regrid curvilinear grids
* [pyresample](https://pyresample.readthedocs.io/en/latest/)
* [geotiepoints](https://python-geotiepoints.readthedocs.io/en/latest/)

***
**Filtering**

* [GCM-filter](https://gcm-filters.readthedocs.io/en/latest/)
* [xr-scipy](https://github.com/hippalectryon-0/xr-scipy)

***

**Masking**

* [regionmask](https://regionmask.readthedocs.io/en/stable/) - working with masks and shape files for xarray

***

**Climate**

* [xcdat](https://xcdat.readthedocs.io/en/latest/) - climatology and weighted spatiotemporal reductions

***

**Data Structures**

* [xarray-dataclasses](https://github.com/astropenguin/xarray-dataclasses) - create standardized xarray datasets and dataarrays

***

**Scale**

> We often need to deal with a large amount of data which is more

* **[Dask Ecosystem]()**.
* **[xarray-beam](https://xarray-beam.readthedocs.io/en/latest/index.html)**.

***

**Visualization**

* [Holoviz](https://holoviz.org/)
* [Terracotta ](https://github.com/DHI/terracotta) - easily create a nice database for visualizing geotiffs.
* Matplotlib
* Seaborn
* Cartopy

***

**Deployment**

* Streamlit
* FastAPI
* [Daytona](https://github.com/daytonaio/daytona) + DevContainer


***

* Hydra, Hydra-Zen
* Typer
* Ruff
* Pyright
* MyPy
* Isort
* pre-commit-config
* GitHub Actions
* Scalene


**Help**

* GitHub Copilot - [Guides](https://www.youtube.com/playlist?list=PLj6YeMhvp2S5_hvBl2SE-7YCHYlLQ0bPt)
