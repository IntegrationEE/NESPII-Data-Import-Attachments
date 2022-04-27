import geopandas as gpd
import geopandas
import logging
import os



def file_reader(shapefile_path: str) -> geopandas.geodataframe:

    """
    This function receives the cleaned shapefile from Hanovia, validates it, reads it and returns a geodataframe version of the data.
    Accepts: Shapefile
    Returns: Geodataframe
    """
    logging.info(f"Reading shapefile: {shapefile_path}")
    # check if the path is a valid string
    assert isinstance(shapefile_path, str), "The shapefile path is not a valid string"

    # check that the path exist
    assert os.path.exists(shapefile_path), "The shapefile provided does not exist"

    # read the shapefile with geopandas
    geodataframe = gpd.read_file(shapefile_path)

    return geodataframe
