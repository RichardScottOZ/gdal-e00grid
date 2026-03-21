# gdal-old-drivers: E00Grid Driver

This repository provides the **E00Grid** raster driver for [GDAL/OGR](https://gdal.org),
built as a GDAL plugin with Python bindings support.

The E00Grid driver reads DEMs/rasters exported as Arc/Info Export E00 Grids.
It was originally part of GDAL core (versions prior to 3.3) but was removed
due to lack of maintenance interest. The driver source comes from the
[OSGeo/gdal-extra-drivers](https://github.com/OSGeo/gdal-extra-drivers) repository.

## Features

- Reads both compressed and uncompressed E00 grid files
- Supports georeferencing and spatial reference (projection) information
- Supports virtual I/O operations
- Provides NoData value, statistics, and unit type metadata
- Works with GDAL Python bindings (`from osgeo import gdal`)

## Build Requirements

- GDAL >= 3.3 headers and development library
- CMake >= 3.10
- C++11 compatible compiler
- Python 3 with GDAL Python bindings (for running tests)

## How to Build

```shell
mkdir _build
cd _build
cmake ..
make
make install
```

A `gdal_E00GRID.so` plugin is installed in `${PREFIX}/lib/gdalplugins`.

## Docker

A Dockerfile is provided for a complete build environment:

```shell
docker build -t gdal-e00grid .
docker run --rm -it gdal-e00grid python3 -c "from osgeo import gdal; print(gdal.GetDriverByName('E00GRID'))"
```

## Usage with Python

Once the plugin is installed in GDAL's plugin directory, use it like any
other GDAL driver:

```python
from osgeo import gdal

ds = gdal.Open('my_file.e00')
if ds is not None:
    band = ds.GetRasterBand(1)
    print(f"Size: {ds.RasterXSize} x {ds.RasterYSize}")
    print(f"NoData: {band.GetNoDataValue()}")
    print(f"GeoTransform: {ds.GetGeoTransform()}")
    data = band.ReadAsArray()
    print(f"Data shape: {data.shape}")
```

## Running Tests

Tests use pytest and require the GDAL Python bindings and the E00GRID plugin
to be installed:

```shell
cd tests
python3 -m pytest -v
```

Or using Docker:

```shell
docker build -t gdal-e00grid .
docker run --rm gdal-e00grid
```

## Driver Documentation

See [doc/e00grid.rst](doc/e00grid.rst) for the full driver documentation.

## License

X/MIT. See [LICENSE.TXT](LICENSE.TXT)

## Credits

- Original E00Grid driver: Even Rouault (Sketchy)
- E00 compression library: Daniel Morissette
- Source: [OSGeo/gdal-extra-drivers](https://github.com/OSGeo/gdal-extra-drivers)
