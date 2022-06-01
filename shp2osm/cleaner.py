import geopandas
import pandas as pd
from enum import Enum


class SurveyColumn(Enum):

    geometry = "geometry"
    building_type = "bui_type"
    commercial_type = "com_type"
    other_commercial = "other_com"
    craft = "craft"
    other_craft = "other_crft"
    productive = "productive"
    other_productive = "other_prdt"
    public_amenity = "publ_amnt"
    other_public_amenity = "other_publ"
    education = "education"
    other_education = "other_educ"
    health = "health"
    other_health = "other_hlth"


def data_cleaner(geodataframe: geopandas.geodataframe) -> pd.DataFrame:
    """
    This function extract only the needed columns from the imported geodataframe and cleans the geodataframe
    Accepts: Shapefile path
    Returns: Geodataframe
    """

    uploadable_data = geodataframe[
        list(map(lambda x: x.value, SurveyColumn._member_map_.values()))
    ]

    # create a new dictionary to store the cleaned version of the uploadable data frame
    # we only need the geometry and the facility type for that particular business

    cleaned_data: dict = {"geometry": [], "facility": [], "building_type": []}

    for _, rows in uploadable_data.iterrows():

        # find the index in the row with a valid input.
        response_index = rows.last_valid_index()
        # get the actual facility type for the survey
        response_value = rows[response_index]

        # update the new dict with the information. Geometry is the first field.(0)
        building_type = rows["bui_type"]
        cleaned_data["geometry"].append(rows[0])

        cleaned_data["facility"].append(response_value)

        cleaned_data["building_type"].append(rows[1])

    # return the cleaned data as a dataframe

    return pd.DataFrame(cleaned_data)
