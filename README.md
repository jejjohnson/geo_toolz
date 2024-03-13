# Geoscience Toolz (In-Progress)
### *A composable set of routines for manipulating Earth System Data Cubes*.

[**About**](#about) 
| [**Functionality**](#functionality)
| [**Installation**](#installation)



![pyver](https://img.shields.io/badge/python-3.9%203.10%203.11_-red)
![codestyle](https://img.shields.io/badge/codestyle-black-black)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/jejjohnson/oceanbench)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
<!-- [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jejjohnson/xrpatcher/blob/main/notebooks/pytorch_integration.ipynb) -->

## About<a id="about"></a>

**`Geo-Toolz`** are a set of useful functions that are necessary for preprocessing data to be machine-learning ready.

**Background**.
In geoscience, most data that we obtain is heterogeneous, i.e., it comes from many different sources with different standards and different quirks.
As an applied machine learning researcher, I have spent more time on the preprocessing chains rather than the actual modeling.
The excuse has always been that every problem is different and requires some.
However, I would argue that there are some *common patterns* that we see for many preprocessing operations that are data independent. **`xarray`** is a testiment to this.
One could draw parallels to the machine learning world where we have frameworks such as `tensorflow`, `pytorch`, `keras` or `jax` whereby each of these frameworks cater to an incomprehensible amount of use cases while still having coherent software.

> An agnostic suite of geoprocessing tools for [xarray](https://docs.xarray.dev/en/stable/) datasets that were aggregated from different sources.


**What are `geo-toolz`??**
It is lightweight in terms of the core functionality.
We keep the code base simple and focus more on how the user can combine each piece.
We adopt a strict functional style because it is easier to maintain and combine sequential transformations.
This enables us to have easier compatibility with python packages that can pipe transformations together like sequential tools like: [`toolz`](https://github.com/pytoolz/toolz/), [`mlx-data`](https://github.com/ml-explore/mlx-data), [`pypeln`](https://github.com/cgarciae/pypeln), [`sklearn.Pipeline`](https://scikit-learn.org/stable/modules/compose.html#pipeline), or [`dask`](https://www.dask.org). 
In addition, this also enables us to create explicit parameterized functions using [`hydra`](https://hydra.cc)/[`hydra-zen`](https://mit-ll-responsible-ai.github.io/hydra-zen/).
This will allow us to document pipelines with easy configuration via the command-line.


***
## Functionality<a id="functionality"></a>

### Data Harmonization

> Input EO data tends to be very messy and heterogeneous. 
> Even the best packages have certain quirks when loading the data. The routines in this part are meant to clean the data in an attempt to "harmonize" them.

**`validation`** - some routines to validate the coordinates.
This includes the usual suspects like lat, lon and time.
We also have some other candidates like sea surface height or temperature.

**`subset`** - these are routines to be able to effectively select a subset of the dataset based on regions and periods.

**`masks`** - these are some routines to add masks to our datasets.
Some usual suspects include the land and ocean as well as some countries, peninsulas, or other official scientific zones.

**`crs`** - some routines for embedding and validating coordinate reference systems.

**`datastructure`** - these hold general purpose methods for converting to xarray datastructures (aka rasters) from other data structures including numpy arrays, polygons, or unstructured coordinates. 

**`dtypes`** - we have some custom data types which are in the form of xarray coordinates or variable names.
These are useful for generating datasets and/or validating datasets.

***
### High-Level Routines

**`grid`** - some general routines for defining grids and transforming grids.
Some subroutines include `regridding` whereby we provide some target grid to regrid our current coordinates to that grid.
Another subroutine includes `resample/coarsen` whereby we reduce the resolution based on some metric like the resolution or a factor.


**`encoders`** - has some subroutines to calculate transformations on the coordinates themselves.
The `spatial` subroutine deals with spatial coordinates like lat-lon and spherical, cartesian or cartesian.
The `time` subroutine deals with absolute groups as well as some temporal embeddings.
The `wavelength` subroutine deals with spectral channels.


**`kinematics`** - a tool to calculate physical quantities.
For example, in remote sensing we have radiance, reflectance. 
In oceanography and meteorology, we have sea surface height, stream function, etc.

**`spectral`** - a tool to calculate some spectral transformations for space and time.
These include some isotropic metrics and some space-time specific transformations.

**`discretization`** - some recipes to calculate some discretization schemes using histograms.
We have options to do it in a windowed formulation in space and time or just space.
Some options include counts, max, and mean.

**`interpolation`** - Som general recipes for doing interpolation.
The `grids` subroutine has functions for transforming with all grids like Unstructured, Curvilinear, Rectilinear, or Regular.
The `fillnan` subroutine is particular for interpolating NANs within a defined boundary.


**`detrend`** - Some general routines for detrending the data.
The `climatology` subroutine calculates trends based on definite frequency groups, e.g., *season*.
The `anomalies` subroutine removes trends based on climatology and filtering (optional).
The `filter` subroutine removes trends based on some filtering scheme in wavelength, space, and/or time.

**`extremes`** - some general routines for calculating extremes from data.
The `bm` subroutine uses the *block-maxima* method calculates the trends based on a block-wise, typically a year or a season.
The `pot` subroutine uses the *peak-over-threshold* method to calculate the extremes based on a threshold.
It also features a declustering method which uses a moving window.


***
### Metrics

**`pixel`** - are pixel-based metrics that operate on the pixels individually.
In general, we can simply use these custom functions directly or we can use them with `xarray.u_func` to vectorize the operations and preserve dimensions. 

**`spectral`** - are spectral-based metrics.
This means applying a Fourier or Wavelet decomposition and then applying the metrics on the spectral space.

**`multiscale`** - are multiscale metrics which operate on different spatial scales.
This means applying a spatial filter at a particular scale and then applying the metrics.

***
### Visualizations

> The `viz` package has some lightweight visualizations that might be useful for users.


***
### `Toolz` Compatibility

The objective is to be able to pipe these transformations through functions like `xarray.Dataset.pipe` and `toolz`.
These are immensely helpful when trying out different preprocessing and geoprocessing operations in conjunction with machine learning.
This gives the user the flexibility to try out different preprocessing strategies to see which yield the best results. 
The user could also use some of these transformations to process data on the fly for training or for inference.
Furthermore, this exposes some of the preprocessing decisions in a more transparent manner that is readable and extendible which allows users to understand, critique and improve.

**Example (PseudoCode)**

```python
# create the function type
FN_TYPE: Callable[[xr.Dataset], xr.Dataset]
# create preprocessing functions
fn1: FN_TYPE = validate_lon
fn2: FN_TYPE = partial(reproject, crs="crs")
fn3: FN_TYPE = partial(fillnans, method="gauss_siedel")
# create sequential function
fnX: FN_TYPE = compose_left(fn1, fn2, fn3)
# open xarray datarray with function composition
ds: xr.Dataset = xr.open_mfdataset("path/to/files/*.nc", preprocess=fnX, engine="netcdf4")
```


***
### `Hydra` Compatibility

In addition to the toolz




## Installation<a id="installation"></a>

### `conda` (RECOMMENDED)

We use conda/mamba as our package manager. To install from the provided environment files
run the following command.

```bash
git clone https://github.com/jejjohnson/geo_toolz.git
cd esdc_tools
mamba env create -n environments/linux.yaml
```

#### Jupyter 
if you want to add the oceanbench conda environment as a jupyter kernel, you need to set the ESMF environment variable:

```
conda activate geo_toolz
mamba install ipykernel -y 
python -m ipykernel install --user --name=esdc_tools --env ESMFMKFILE "$ESMFMKFILE"
```

### `pip`

We can directly install it via pip from the repo.

```bash
conda create -n geo_toolz
conda activate geo_toolz
mamba install xesmf -c conda-forge
pip install "git+https://github.com/jejjohnson/geo_toolz.git"
```

**Note**: There are some known dependency issues related to `pyinterp` and `xesmf`. 
You will need to manually install some of the dependencies before installing oceanbench via pip.
See the [pyinterp](https://pangeo-pyinterp.readthedocs.io/en/latest/setup/pip.html) and [xesmf](https://xesmf.readthedocs.io/en/latest/installation.html) packages for more information.

### `poetry` (TODO)

For developers who want all of the dependencies via pip, we can use poetry to install the package.


```bash
git clone https://github.com/jejjohnson/geo_toolz.git
cd geo_toolz
conda create -n geo_toolz python=3.11 poetry
poetry install
```



