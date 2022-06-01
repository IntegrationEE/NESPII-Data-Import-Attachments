import logging
import os
from cleaner import data_cleaner
from file_reader import file_reader
from osm_tags_to_dict import osm_tags_to_dict
from transformer import transformer


# default paths

CURRENT_PATH = os.getcwd()
INPUT_PATH = ""
OUTPUT_PATH = ""
TAGS_PATH = os.path.join(CURRENT_PATH, "taglist.csv")


def main():
    # logging settings
    logging.basicConfig(filename="logs.log", level=logging.INFO)
    osm_tags_dict = osm_tags_to_dict(TAGS_PATH)
    for root, dirs, files in os.walk(INPUT_PATH):
        for filename in files:
            shapefile = filename if filename.endswith(".shp") else None
            if shapefile:

                raw_filename = filename.split(".")[0]
                logging.info(f"Working on {raw_filename}")
                shapefile_path = os.path.join(INPUT_PATH, raw_filename, shapefile)
                logging.info(f"Reading {raw_filename}")
                raw_geodataframe = file_reader(shapefile_path)
                logging.info(f"Successfully opened {raw_filename}")
                logging.info(f"Cleaning {raw_filename}")
                cleaned_geodataframe = data_cleaner(raw_geodataframe)
                logging.info(f"Successfully cleaned {raw_filename}")
                logging.info(f"Transforming {raw_filename}")
                transformed_geodataframe = transformer(
                    cleaned_geodataframe, osm_tags_dict
                )
                logging.info(f"Successfully transformed {raw_filename}")
                output_path = os.path.join(OUTPUT_PATH, raw_filename)
                logging.info(f"Saving to geojson: {raw_filename}")
                transformed_geodataframe.to_file(
                    f"{output_path}.geojson", driver="GeoJSON"
                )
                logging.info(f"Operation completed successfully {raw_filename}")


if __name__ == "__main__":
    main()
