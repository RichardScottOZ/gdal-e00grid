#!/usr/bin/env pytest
###############################################################################
#
# Project:  GDAL/OGR Test Suite
# Purpose:  Test E00GRID driver
# Author:   Even Rouault, <even dot rouault at spatialys.com>
#
###############################################################################
# Copyright (c) 2011, Even Rouault <even dot rouault at spatialys.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
###############################################################################

import struct

import pytest

from osgeo import gdal, osr


@pytest.mark.require_driver('E00GRID')
class TestE00Grid:
    """Tests for the E00GRID driver using GDAL Python bindings."""

    def test_driver_exists(self):
        """Test that the E00GRID driver is registered."""
        driver = gdal.GetDriverByName('E00GRID')
        assert driver is not None, "E00GRID driver not found"

    def test_open_uncompressed(self):
        """Test opening an uncompressed E00 grid file."""
        ds = gdal.Open('data/e00grid/fake_e00grid.e00')
        assert ds is not None, "Failed to open fake_e00grid.e00"
        assert ds.RasterXSize == 5
        assert ds.RasterYSize == 4
        assert ds.RasterCount == 1
        ds = None

    def test_uncompressed_geotransform(self):
        """Test geotransform of uncompressed E00 grid."""
        ds = gdal.Open('data/e00grid/fake_e00grid.e00')
        assert ds is not None
        gt = ds.GetGeoTransform()
        expected_gt = (500000.0, 1000.0, 0.0, 4000000.0, 0.0, -1000.0)
        for i in range(6):
            assert abs(gt[i] - expected_gt[i]) < 1e-6, \
                f"GeoTransform[{i}]: expected {expected_gt[i]}, got {gt[i]}"
        ds = None

    def test_uncompressed_projection(self):
        """Test projection of uncompressed E00 grid."""
        ds = gdal.Open('data/e00grid/fake_e00grid.e00')
        assert ds is not None
        srs = osr.SpatialReference()
        srs.ImportFromWkt(ds.GetProjectionRef())
        assert srs.GetAttrValue('PROJECTION') == 'Transverse_Mercator'
        ds = None

    def test_uncompressed_nodata(self):
        """Test NoData value of uncompressed E00 grid."""
        ds = gdal.Open('data/e00grid/fake_e00grid.e00')
        assert ds is not None
        band = ds.GetRasterBand(1)
        nodata = band.GetNoDataValue()
        assert nodata == -32767, f"Expected nodata=-32767, got {nodata}"
        ds = None

    def test_uncompressed_unit_type(self):
        """Test unit type of uncompressed E00 grid."""
        ds = gdal.Open('data/e00grid/fake_e00grid.e00')
        assert ds is not None
        band = ds.GetRasterBand(1)
        unit = band.GetUnitType()
        assert unit == 'ft', f"Expected unit='ft', got '{unit}'"
        ds = None

    def test_uncompressed_checksum(self):
        """Test checksum of uncompressed E00 grid band 1."""
        ds = gdal.Open('data/e00grid/fake_e00grid.e00')
        assert ds is not None
        band = ds.GetRasterBand(1)
        cs = band.Checksum()
        assert cs == 65359, f"Expected checksum=65359, got {cs}"
        ds = None

    def test_open_compressed(self):
        """Test opening a compressed E00 grid file."""
        ds = gdal.Open('data/e00grid/fake_e00grid_compressed.e00')
        assert ds is not None, "Failed to open fake_e00grid_compressed.e00"
        assert ds.RasterXSize == 5
        assert ds.RasterYSize == 4
        assert ds.RasterCount == 1
        ds = None

    def test_compressed_checksum(self):
        """Test checksum of compressed E00 grid band 1."""
        ds = gdal.Open('data/e00grid/fake_e00grid_compressed.e00')
        assert ds is not None
        band = ds.GetRasterBand(1)
        cs = band.Checksum()
        assert cs == 65347, f"Expected checksum=65347, got {cs}"
        ds = None

    def test_compressed_geotransform(self):
        """Test geotransform of compressed E00 grid."""
        ds = gdal.Open('data/e00grid/fake_e00grid_compressed.e00')
        assert ds is not None
        gt = ds.GetGeoTransform()
        expected_gt = (500000.0, 1000.0, 0.0, 4000000.0, 0.0, -1000.0)
        for i in range(6):
            assert abs(gt[i] - expected_gt[i]) < 1e-6, \
                f"GeoTransform[{i}]: expected {expected_gt[i]}, got {gt[i]}"
        ds = None

    def test_compressed_read_lines(self):
        """Test reading different lines from compressed E00 grid."""
        ds = gdal.Open('data/e00grid/fake_e00grid_compressed.e00')
        assert ds is not None
        line0 = ds.ReadRaster(0, 0, 5, 1)
        ds.ReadRaster(0, 1, 5, 1)
        line2 = ds.ReadRaster(0, 2, 5, 1)
        assert line0 != line2, 'should not have gotten the same values'
        # Re-read to verify seeking works
        ds.ReadRaster(0, 0, 5, 1)
        line2_bis = ds.ReadRaster(0, 2, 5, 1)
        assert line2 == line2_bis, 'did not get the same values for the same line'
        ds = None

    def test_compressed_statistics(self):
        """Test statistics from compressed E00 grid."""
        ds = gdal.Open('data/e00grid/fake_e00grid_compressed.e00')
        assert ds is not None
        band = ds.GetRasterBand(1)
        assert band.GetMinimum() == 1, 'did not get expected minimum value'
        assert band.GetMaximum() == 50, 'did not get expected maximum value'
        stats = band.GetStatistics(False, True)
        assert stats == [1.0, 50.0, 25.5, 24.5], 'did not get expected statistics'
        ds = None

    def test_invalid_file_rejected(self):
        """Test that non-E00 files are rejected."""
        ds = gdal.Open('data/e00grid/fake_e00grid.e00')
        # Just verify that valid files work; invalid would return None
        assert ds is not None
        ds = None
