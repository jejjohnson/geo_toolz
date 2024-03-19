---
title: Geo0Operations
subject: Machine Learning for Earth Observations
short_title: Introduction
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


**Core Operations**
* Input
* Split
* Apply
* Combine

```{figure} https://comptools.climatematch.io/_images/t5_split_apply_combine.png
:name: earth-sys-decomp
:width: 490px
:alt: Random image of the beach or ocean!
:align: center

Example of a decomposition of the Earth system based on a domain. [[Source](https://www.energy.gov/science/doe-explainsearth-system-and-climate-models)]
```


***

* Functions - Unary Binary, etc
* Grouped Computations
* Windowed Computations


***

## **High-Level Operations**


**Window Operations**
* Coarsen - block windows of fixed length
* Rolling - Sliding windows of fixed length

**Group Operations**
* GroupBy
* Resample

Agnostic Operations
* Apply uFunc 

**Recipes**
* Interpolation
* Climatology
* Anomalies
* Regridding
* Fill-NANs
* Calculating Exceedences
* Discretization 


***
## Detailed Operations


***

### **Resampling**

> This will be useful for selecting the min/max values of a time series possibly over a given threshold.

* [xarray - StackOverFlow](https://stackoverflow.com/questions/54431557/xarray-use-groupby-to-group-by-every-day-over-a-years-climatological-hourly-n)
* [xarray-docs](https://docs.xarray.dev/en/stable/user-guide/time-series.html#)
* xcdat time averages - [Notebook](https://xcdat.readthedocs.io/en/latest/examples/temporal-average.html)


***

### **Coarsen**

> This will be useful for selecting the min/max values of a spatial field possibly over a given threshold.

* [xarray-docs](https://docs.xarray.dev/en/stable/user-guide/computation.html#coarsen-large-arrays)
* xcdat for geospatial weighted averaging - [Notebook](https://xcdat.readthedocs.io/en/latest/examples/spatial-average.html)
* climatology with coarsen - [Notebook](https://climate-cms.org/posts/2021-07-29-coarsen_climatology.html)

***

### **Rolling**

> This is useful for capturing events with memory.

* Calculating heatwaves with rolling - [gist](https://gist.github.com/ScottWales/dd9358bea2547c99e46b197bc9f53d21)


***

### **Counting Exceedences**

> This will be a string of operations but we essentially want a workflow to count the number of occurrences given a specific threshold.

* count occurrences over threshold - [xarray-stackoverflow](https://stackoverflow.com/questions/62698837/calculating-percentile-for-each-gridpoint-in-xarray)
* climate event detection - [Notebook](https://climate-cms.org/posts/2020-09-28-eventdetection.html)


***

### **Regions**

* regions and zonal statistics - [Notebook](https://climate-cms.org/posts/2023-07-05-select-region-shapefile.html)

***

### **Climatology**

* Calculating Seasonality with selectors and masks - [Notebook](https://climate-cms.org/posts/2023-11-04-seasonal-means.html)
* Removing Climatology with mapping - [Notebook](https://earth-env-data-science.github.io/lectures/xarray/xarray-part2.html)
* Calculating ENSO with xarray - [Pythia](https://foundations.projectpythia.org/core/xarray/enso-xarray.html)
* Simple Example with Hostorical Period - [Notebook](https://tutorials.dkrz.de/use-case_ensemble-analysis_intake-xarray_cmip6.html)
* Simple Climatology - [Notebook](https://comptools.climatematch.io/tutorials/W1D1_ClimateSystemOverview/student/W1D1_Tutorial5.html)
* xcdat for climatologies - [Notebook](https://xcdat.readthedocs.io/en/latest/examples/climatology-and-departures.html)
* Extended Tutorial - [CDS Docs](https://ecmwf-projects.github.io/copernicus-training-c3s/reanalysis-climatology.html)
* Example of different means (daily, monthly, seasonly, yearly) - [geocat docs](https://geocat-comp.readthedocs.io/en/stable/examples/calendar_average.html)
* code with climatology and anomaly abstraction - [Geocat ](https://github.com/andersy005/geocat-comp/blob/eb5352209ff2ced8c1885ede7d60008dea5fc0c7/src/geocat/comp/climatology.py#L148)

***

### **Anomalies**

* Calculating Anomalies with Climatology and Weighted Means - [Notebook](https://comptools.climatematch.io/tutorials/W1D1_ClimateSystemOverview/student/W1D1_Tutorial6.html)
* xcdat for anomalies - [Notebook](https://xcdat.readthedocs.io/en/latest/examples/climatology-and-departures.html)
* Extended Tutorial - [CDS Website](https://ecmwf-projects.github.io/copernicus-training-c3s/reanalysis-climatology.html)
* Calculating Climatology & Anomalies with Dask - [Gist](https://gist.github.com/rabernat/30e7b747f0e3583b5b776e4093266114)
* Rainfall Anomalies and Climatology with Dask - [Notebook](https://docs.digitalearthafrica.org/sandbox/notebooks/Real_world_examples/Rainfall_anomaly_CHIRPS.html)


***

### **Interpolation**

> Synonyms - Regrid, Resample, Reproject

In general, we often need to interpolate data because of various reasons. For example, we may have some messy *unstructured* data structure which are basically point clouds with arbitrary and we want to move them to a *structured* data structure.

**Resampling** - Moving data to a higher or lower resolution

**Regridding** - Moving data from one grid resolution/composition to different one


**Guides**

* [Introduction to Interpolation](https://www.neonscience.org/resources/learning-hub/tutorials/spatial-interpolation-basics)
* [NCAR Regridding Guide](https://climatedataguide.ucar.edu/climate-tools/regridding-overview)

**Packages**


* xcdat for horizontal regridding - [Notebook](https://xcdat.readthedocs.io/en/latest/examples/regridding-horizontal.html)
* xcdat for vertical regridding - [Notebook](https://xcdat.readthedocs.io/en/latest/examples/regridding-vertical.html)
* Comparison of Interpolation Methods - xarray, pyinterp, xegrid, scipy - [Notebook](https://github.com/GeospatialGeeks/Py4Geo/blob/master/Regridding%20and%20Spatial%20Interpolation%20in%20Python.ipynb)
* Simple example with rioxarray & `xarray` - [blog](https://www.theurbanist.com.au/2022/02/updated-how-to-create-an-xarray-dataset-from-scratch-reproject-and-save/)
* Example with GOES and rioxarray - [stackoverflow](https://gis.stackexchange.com/questions/349886/using-rioxarray-qgis-projection)
* Pyresample Tutorial - [ipynb](https://github.com/pytroll/tutorial-satpy-half-day/blob/main/notebooks/04_resampling.ipynb)
* Example with `GOES,pyproj,pyresample,cartopy` - [ipynb](https://github.com/joaohenry23/GOES/blob/master/examples/v3.2/G16_IR__SRCYL_plot.ipynb)
