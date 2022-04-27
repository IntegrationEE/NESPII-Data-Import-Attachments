import pandas as pd


def osm_tags_to_dict(tags_path: str) -> dict:

    """
    This function converts the osm tags in the csv to dictionary.
    Returns: OSM Tags in dict
    """
    # read the OSM tag list and return as a geodataframe

    osm_tags = pd.read_csv(tags_path)

    # create an osm tag dictionary in the appropriate osm data structure

    new_tags: dict = {}

    for x, y in osm_tags.iterrows():

        key_value: dict = {
            y["Name"]: {
                "key": y["Key"],
                "value": y["Value"],
                "key1": y["Key2"],
                "value1": y["value2"],
                "key2": y["key3"],
                "value2": y["value3"],
            }
        }

        new_tags.update(key_value)

    return new_tags
