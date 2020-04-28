import csv
import json
from shapely.geometry import shape, Point


def filterGeographies(fileNm_Wales, fileNm_in, fileNm_out):

    output = []

    # Import welsh boundaries
    with open(fileNm_Wales) as boundaries:
        boundaries_js = json.load(boundaries)

        features = boundaries_js["features"]
        for feature in features:
            properties = feature["properties"]
            if properties["ctry19cd"] == "W92000004":
                polygon = shape(feature["geometry"])
                print("BOUNDARY GEOJSON: Welsh borders found and imported.")

    with open(fileNm_in) as LAs:
        LAs_js = json.load(LAs)

        features = LAs_js["features"]
        for feature in features:
            properties = feature["properties"]

            # Construct point from coords
            point = shape(feature["geometry"]).representative_point()
            # print(point)

            # Check polygon for Wales to see if it contains the point
            if polygon.contains(point):
                try:
                    nmTest = properties["LSOA11CD"]
                    print("Found: ", nmTest)
                    output.append(feature)
                except:
                    print("unable to process: ", properties.keys())

    # Write to geojson
    geoJSON_groups = {"type": "FeatureCollection", "features": output}
    with open(fileNm_out, "w") as grps:
        json.dump(geoJSON_groups, grps)


filterGeographies(
    "data/geography/boundaries_Wales.geojson",
    "data/geography/boundaries_LSOAs.geojson",
    "data/geography/boundaries_LSOAsNEW.geojson",
)
