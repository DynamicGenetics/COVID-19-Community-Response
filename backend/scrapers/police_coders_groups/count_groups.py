from re import search
import csv
import json
from shapely.geometry import shape, Point
import pandas as pd


def count_groups():

    summary = []

    with open("data/scrapers/police_coders_groups/groups_Latest.csv", newline="") as f:
        data = csv.DictReader(f)

        with open("data/geography/boundaries_LSOAs.geojson", newline="") as f:
            boundaries = csv.DictReader(f)

            for feature in boundaries:
                print(feature)

                groups = []
                area_polygon = shape(feature["geometry"])

                for row in data:
                    print(row)

                    if area_polygon.contains(Point(row["Lng"], row["Lat"])):

                        groups.append(row)

                summary.append(
                    {
                        "areaID": feature["properties"]["LSOA11CD"],
                        "groups": groups,
                        "groupCount": len(groups),
                    }
                )

    with open("data/scrapers/police_coders_groups/groupCount.csv", "w") as f:
        for row in summary:
            json.dumps(row, f)

    return "count success"
