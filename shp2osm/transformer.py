import pandas as pd
import geopandas as gpd
import random


def transformer(cleaned_data: pd.DataFrame, osm_tags_dict) -> gpd.GeoDataFrame:
    """
    This function transforms the data and grab the appropriate osm tags from the osm tag dict
    """
    # OSM data structure
    # osm_id(negative), osm_type(node), long, lat, key, key2, key3...

    transformed_data = {}
    osm_ids = []
    geometries = []
    has_tag = 0
    facilities_with_tag = []
    building_type_of_facilities_with_tag = []

    # get facilites as a list
    facilities = cleaned_data["facility"].to_list()

    # create a list of facilities with tag and the lenght

    for facility in facilities:
        try:
            if osm_tags_dict.get(facility):
                facilities_with_tag.append(facility)
                has_tag += 1
        except Exception:
            pass

    # update the geometries and osm ids of the facilities with tag

    for index, columns in cleaned_data.iterrows():

        facility = columns["facility"]
        building_type = columns["building_type"]

        if facility in facilities_with_tag:
            geometries.append(columns["geometry"])
            osm_ids.append(random.randint(-100000, 0))
            building_type_of_facilities_with_tag.append(building_type)

    for facility_index, facility in enumerate(facilities_with_tag):

        random_list = [None for x in range(0, has_tag)]
        tag = osm_tags_dict.get(facility)

        # tag_key and tag_value are the default OSM tags
        # key_1.key_2 ,value_1 and value_2 are the optional osm tags

        tag_key = tag.get("key")
        tag_value = tag.get("value")
        key_1 = tag.get("key1")
        value_1 = tag.get("value1")
        key_2 = tag.get("key2")
        value_2 = tag.get("value2")

        random_list[facility_index] = tag_value

        if not tag_key in transformed_data:

            transformed_data.update({tag_key: random_list})

        else:

            # update the list of the previous tag key with a new value
            transformed_data[tag_key][facility_index] = tag_value

        if not pd.isna(key_1):

            new_random_list = [None for x in range(0, has_tag)]

            if not key_1 in transformed_data:

                new_random_list[facility_index] = value_1

                transformed_data.update({key_1: new_random_list})

            else:
                # update the list of the previous tag key with a new value
                transformed_data[key_1][facility_index] = value_1

        elif not pd.isna(key_2):

            new_random_list_2 = [None for x in range(0, has_tag)]

            if not key_2 in transformed_data:

                new_random_list_2[facility_index] = value_2

                transformed_data.update({key_2: new_random_list_2})

            else:
                # update the list of the previous tag key with a new value
                transformed_data[key_2][facility_index] = value_2

    # convert dictionary to a dataframe
    transformed_dataframe = pd.DataFrame(transformed_data)

    # add osm_type=node to all data and update with the geometry and auto generated ids

    transformed_dataframe["osm_type"] = "node"
    transformed_dataframe["geometry"] = geometries
    transformed_dataframe["osm_id"] = osm_ids
    transformed_dataframe["building_type"] = building_type_of_facilities_with_tag
    transformed_dataframe["building"] = None
    transformed_dataframe["construction"] = None

    # include building type tags

    transformed_dataframe.loc[
        transformed_dataframe["building_type"]
        == "structure consists of a roof with open sides",
        ["building"],
    ] = "roof"

    transformed_dataframe.loc[
        transformed_dataframe["building_type"]
        == "structure consists of walls and a roof",
        ["building"],
    ] = "yes"

    transformed_dataframe.loc[
        transformed_dataframe["building_type"] == "structure is under construction",
        ["building"],
    ] = "construction"

    transformed_dataframe.loc[
        transformed_dataframe["building_type"] == "structure is under construction",
        ["construction"],
    ] = "commercial"

    # remove the building type column

    transformed_dataframe.drop(["building_type"], axis=1, inplace=True)

    # return as a geodataframe for export
    return gpd.GeoDataFrame(transformed_dataframe)
