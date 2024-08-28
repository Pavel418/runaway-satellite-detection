import numpy as np
import random
import rasterio
from shapely.geometry import shape, Point, LineString, Polygon
import geopandas as gpd
import math
import os

class ImageAugmentation:
    def get_images(self, dataset_path):
        images_shapes = []
        for part in os.listdir(dataset_path):
            part_path = os.path.join(dataset_path, part)
            for date in os.listdir(part_path):
                date_path = os.path.join(part_path, date)
                images = [os.path.join(date_path, file) for file in os.listdir(date_path) if file.endswith('.tif')]
                shapes = [os.path.join(date_path, file) for file in os.listdir(date_path) if file.endswith('.shp')]
                for shape in shapes:
                    images_shapes.append((images, shape))
        return images_shapes
    
    def load_images_and_shape(self, image_paths, shape_path):
        images = []
        meta = []
        for image_path in image_paths:
            with rasterio.open(image_path) as src:
                image_data = src.read()
                image_data = np.transpose(image_data, (1, 2, 0))
                images.append(image_data)
                meta.append({"width": src.width, "height": src.height, "bounds": src.bounds})
        gdf = gpd.read_file(shape_path)
        return images, meta, gdf["geometry"]

    def convert_to_relative(self, shape, meta):
        bounds = meta["bounds"]
        width, height = meta["width"], meta["height"]
        x_min, y_max = bounds.left, bounds.top
        x_max, y_min = bounds.right, bounds.bottom

        bbox_polygon = Polygon([(x_min, y_min), (x_max, y_min), (x_max, y_max), (x_min, y_max), (x_min, y_min)])

        filtered_geometry = shape[shape.apply(lambda x: x is not None and x.intersects(bbox_polygon))]
        filtered_geometry = filtered_geometry.apply(lambda x: x.intersection(bbox_polygon))

        relative_geometry = []

        for geom in filtered_geometry:
            x, y = geom.xy
            x_img = (np.array(x) - x_min) / (x_max - x_min) * width
            y_img = (y_max - np.array(y)) / (y_max - y_min) * height
            relative_geometry.append((x_img, y_img))

        return relative_geometry

    def random_crop_with_object(self, image, line, crop_size):
        img_height, img_width = image.shape[:2]
        crop_height, crop_width = crop_size

        array1 , array2 = line[0]
        x1, x2 = array1
        y1, y2 = array2

        x_min = min(x1, x2)
        y_min = min(y1, y2)
        x_max = max(x1, x2)
        y_max = max(y1, y2)

        x_min_valid = max(0, x_max - crop_width)
        x_max_valid = min(img_width - crop_width, x_min)
        y_min_valid = max(0, y_max - crop_height)
        y_max_valid = min(img_height - crop_height, y_min)

        if x_max_valid <= x_min_valid or y_max_valid <= y_min_valid:
            raise ValueError(f"Crop size is too large to contain the object. x_min_valid: {x_min_valid}, x_max_valid: {x_max_valid}, y_min_valid: {y_min_valid}, y_max_valid: {y_max_valid}")

        crop_x = random.randint(math.ceil(x_min_valid), math.floor(x_max_valid))
        crop_y = random.randint(math.floor(y_min_valid), math.floor(y_max_valid))

        cropped_image = image[crop_y:crop_y + crop_height, crop_x:crop_x + crop_width]

        new_x1 = x1 - crop_x
        new_y1 = y1 - crop_y
        new_x2 = x2 - crop_x
        new_y2 = y2 - crop_y

        new_line = (np.array([new_x1, new_x2]), np.array([new_y1, new_y2]))

        return cropped_image, new_line