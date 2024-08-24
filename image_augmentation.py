import numpy as np
import random
import rasterio
from shapely.geometry import shape, Point, LineString, Polygon
import geopandas as gpd

class ImageAugmentation:
    def convert_to_relative(self, image_path, shape_path):
        # Read the shapefile once
        gdf = gpd.read_file(shape_path)
        geometry = gdf['geometry']

        with rasterio.open(image_path) as src:
            bounds = src.bounds
            width, height = src.width, src.height
            x_min, y_max = bounds.left, bounds.top
            x_max, y_min = bounds.right, bounds.bottom

        bbox_polygon = Polygon([(x_min, y_min), (x_max, y_min), (x_max, y_max), (x_min, y_max), (x_min, y_min)])

        filtered_geometry = geometry.apply(lambda x: x.intersection(bbox_polygon))

        def to_relative_coords(geom):
            x, y = geom.xy
            x_img = (np.array(x) - x_min) / (x_max - x_min) * width
            y_img = (y_max - np.array(y)) / (y_max - y_min) * height
            return (x_img, y_img)

        relative_geometry = filtered_geometry.apply(to_relative_coords).tolist()

        return relative_geometry

    def random_crop(self, image, mask, crop_size):
        pass