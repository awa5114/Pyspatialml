from unittest import TestCase
from pyspatialml.sampling import extract
from copy import deepcopy
import os
import geopandas
import rasterio
import numpy as np

os.chdir(os.path.join('.', 'pyspatialml', 'tests'))

class TestExtract(TestCase):

    band1 = 'lsat7_2000_10.tif'
    band2 = 'lsat7_2000_20.tif'
    band3 = 'lsat7_2000_30.tif'
    band4 = 'lsat7_2000_40.tif'
    band5 = 'lsat7_2000_50.tif'
    band7 = 'lsat7_2000_70.tif'
    predictors = [band1, band2, band3, band4, band5, band7]

    def test_extract_points(self):

        # extract training data from points
        stack = Raster(self.predictors)
        training_pt = geopandas.read_file('landsat96_points.shp')
        X, y, xy = stack.extract_vector(response=training_pt, field='id', return_array=True)

        # check shapes of extracted pixels
        self.assertTupleEqual(X.shape, (885, 6))
        self.assertTupleEqual(y.shape, (885, ))
        self.assertTupleEqual(xy.shape, (885, 2))

        # check number of masked values
        masked_rows, masked_cols = np.nonzero(X.mask == True)
        self.assertTupleEqual(masked_rows.shape, (988, ))
        self.assertTupleEqual(masked_cols.shape, (988, ))

        # check values of extracted y values
        self.assertTrue(
            np.equal(np.bincount(y),
                     np.asarray([0, 267, 5, 102, 53, 438, 17, 3])).all()
        )

        # check extracted X values
        self.assertAlmostEqual(X[:, 0].mean(), 80.92952, places=2)
        self.assertAlmostEqual(X[:, 1].mean(), 66.90026, places=2)
        self.assertAlmostEqual(X[:, 2].mean(), 66.39095, places=2)
        self.assertAlmostEqual(X[:, 3].mean(), 68.50531, places=2)
        self.assertAlmostEqual(X[:, 4].mean(), 88.52925, places=2)
        self.assertAlmostEqual(X[:, 5].mean(), 59.55871, places=2)

    def test_extract_polygons(self):

        # extract training data from polygons
        stack = Raster(self.predictors)
        training_py = geopandas.read_file('landsat96_polygons.shp')
        X, y, xy = stack.extract_vector(response=training_py, field='id', return_array=True)

        # check shapes of extracted pixels
        self.assertTupleEqual(X.shape, (2264, 6))
        self.assertTupleEqual(y.shape, (2264, ))
        self.assertTupleEqual(xy.shape, (2264, 2))

    def test_extract_lines(self):

        # extract training data from lines
        training_py = geopandas.read_file('landsat96_polygons.shp')
        training_lines = deepcopy(training_py)
        training_lines['geometry'] = training_lines.geometry.boundary
        stack = Raster(self.predictors)
        X, y, xy = stack.extract_vector(response=training_lines, field='id', return_array=True)

    def test_extract_raster(self):

        # extract training data from labelled pixels
        training_px = rasterio.open('landsat96_labelled_pixels.tif')
        X, y, xy = stack.extract_raster(response=training_px, value_name='id', return_array=True)
