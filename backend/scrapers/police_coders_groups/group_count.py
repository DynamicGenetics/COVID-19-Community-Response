"""
Intended purpose of this script:
1. Get LA and LSOA boundaries as shape objects
2. Get list of groups and their coordinates
3. Locate groups to LA and LSOA boundaries
4. Count how many groups are in each LA & LSOA
5. Save LA and LSOA counts into seperate csvs

"""

import pandas as pd
from pandas import Series
import json
from shapely.geometry import shape, Point


# Count the number of groups per LA and LSOA
def count_groups(input_path, boundary_info, areaID_name):

    # Seperate information about boundaries from the data packages given as paramaters
    polygons = boundary_info["polygons"]
    areaID_list = boundary_info["areaID_list"]

    # Read in identified welsh group csv
    df = pd.read_csv(input_path)

    # Search boundary polygons to see if they contain a groups point coord location
    df[areaID_name] = df.apply(
        # Pass polygons and point coordinates object to geolocation function to search polygons for point
        lambda row: locate_group(polygons, Point(row["Lng"], row["Lat"])),
        axis=1,
    )

    # Count the number of groups per area
    count = Series.value_counts(df[areaID_name])

    # Make a blank series containing all areas with a groupCount of 0
    blanks = Series(0, index=areaID_list)

    # Since the geolocation function only returns areas with groups in them, we need to add blank rows for areas without any groups
    df = Series.add(count, blanks, fill_value=0)

    # Transform to dataframe for easier csv output
    df = df.to_frame()

    # Rename columns to be consistent with other csvs
    df = df.reset_index()
    df = df.rename(columns={"index": "area_code", 0: "groupCount"})

    return df


# Import LA boundaries as shape object
def get_boundaries_LA(fileNm_areas):

    with open(fileNm_areas) as boundaries:
        bounds = json.load(boundaries)
        polygons = []
        areaID_list = []

        features = bounds["features"]
        for feature in features:
            polygon = {
                "id": feature["properties"]["lad18cd"],
                "geom": shape(feature["geometry"]),
            }
            polygons.append(polygon)
            areaID_list.append(feature["properties"]["lad18cd"])

    return {"polygons": polygons, "areaID_list": areaID_list}


# Import LSOA boundaries as shape object
def get_boundaries_LSOA(fileNm_areas):

    with open(fileNm_areas) as boundaries:
        bounds = json.load(boundaries)
        polygons = []
        areaID_list = []

        features = bounds["features"]
        for feature in features:
            polygon = {
                "id": feature["properties"]["LSOA11CD"],
                "geom": shape(feature["geometry"]),
            }
            polygons.append(polygon)
            areaID_list.append(feature["properties"]["LSOA11CD"])

    return {"polygons": polygons, "areaID_list": areaID_list}


# Locate which area the group is located
def locate_group(polygons, group_coords):

    # Check all the boundaries to see which one contains the group point location
    for polygon in polygons:

        if polygon["geom"].contains(group_coords):
            return polygon["id"]

    # If not located return error code
    print("Warning (groupCount): Unable to locate group ({})".format(group_coords))
