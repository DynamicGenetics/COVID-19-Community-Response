import pandas as pd
from dataclasses import dataclass
from typing import Sequence
from warnings import warn
import os
import json

# Local imports
from datasets.live import LA_LIVE
from datasets.static import LA_STATIC, LSOA_STATIC

from datasets import BASE_FOLDER

LA_STATIC_MASTER = LA_STATIC.master_dataset
LSOA_STATIC_MASTER = LSOA_STATIC.master_dataset
LA_LIVE_MASTER = LA_LIVE.master_dataset


@dataclass
class Variable:
    data: pd.Series
    label: str  # Human readable label
    data_class: str  # Is the data 'support' or 'challenge'
    invert: bool  # Does the direction of the data need to be inverted before mapping?
    data_type: str  # Is the data a percentage, a count or a rank?
    la_and_lsoa: bool = True  # If LA, is it available at both levels?
    data_transformed_: pd.Series = None

    @property
    def res(self):
        """Guess resolution of the data depending on its size"""
        if self.data.shape[0] == 22:
            return "LA"
        elif self.data.shape[0] == 1909:
            return "LSOA"
        else:
            warn(
                "Series length of {} does not match LA or LSOA".format(
                    self.data.shape[0]
                )
            )

    def transform(self):
        self.data_transformed_ = self.data
        self.data_transformed_ = self.transform_per100()
        if self.invert:
            self.data_transformed_ = self.invert_data()

        # Rename without the _ string section defining data type
        self.data_transformed_.name = self.new_name()

        return self

    @property
    def transformed_data(self):
        return self.data_transformed_

    def new_name(self):
        name_to_change = self.data.name
        new_name = "_".join(name_to_change.split("_")[:-1])
        return new_name

    def transform_per100(self):
        """Based on variable type, perform transformation"""
        if self.data_type == "percentage":
            return self.data_transformed_
        elif self.data_type == "count":
            if self.res == "LA":
                return (self.data_transformed_ / LA_POPULATION) * 100
            elif self.res == "LSOA":
                return (self.data_transformed_ / LSOA_POPULATION) * 100
        elif self.data_type == "density":
            return self.data_transformed_
        elif self.data_type == "rank":
            return self.data_transformed_
        elif self.data_type == "per100k":
            return self.data_transformed_ / 1000
        else:
            raise Exception(
                "Transformation of data type: {} are not suppored".format(
                    self.data_type
                )
            )

    def invert_data(self):
        """Invert data direction AFTER transformation"""
        if self.data_type in ["percentage", "count", "per100k"]:
            return 100 - self.data_transformed_
        elif self.data_type == "rank":
            return (self.data_transformed_.max() + 1) - self.data_transformed_
        else:
            raise Exception(
                "Inversion of data type: {} are not suppored".format(self.data_type)
            )

    def meta_to_json(self):
        return {
            "name": self.new_name(),
            "label": self.label,
            "class": self.data_class,
            "lsoa": self.la_and_lsoa,
        }


@dataclass
class Variables:
    variables: Sequence[Variable]

    @property
    def is_valid(self):
        # Check resolutions are same for all variables
        resolutions = map(lambda v: v.res, self.variables)
        if len(set(resolutions)) < 2:
            return True
        else:
            return False

    def metadata_to_json(self):
        return [var.meta_to_json() for var in self.variables]

    def data_to_json(self):
        vars = map(lambda v: v.transform(), self.variables)
        vars = map(lambda v: v.transformed_data, vars)

        data = pd.concat(vars, axis=1)
        # Reset index the dataframe first, becasue we want the index values in json
        data = data.round(3)
        data = data.reset_index()

        return data.to_dict(orient="records")


@dataclass
class DataDashboard:
    la_data: Variables
    lsoa_data: Variables

    def to_json(self):
        # Currently only returning LA level meta data as it encompasses both
        return {
            "variables": self.la_data.metadata_to_json(),
            "LAs": self.la_data.data_to_json(),
            "LSOAs": self.lsoa_data.data_to_json(),
        }

    def write(self):
        JSON_OUT = os.path.join(
            BASE_FOLDER, "..", "..", "frontend", "map", "data", "data.json",
        )
        with open(JSON_OUT, "w") as outfile:
            json.dump(self.to_json(), outfile)


LA_POPULATION = LA_STATIC_MASTER["population_count"]
LSOA_POPULATION = LSOA_STATIC_MASTER["population_count"]

LA_POPDENSITY = Variable(
    data=LA_STATIC_MASTER["pop_density_persqkm"],
    label="Population Density (sq. km)",
    data_class="challenge",
    la_and_lsoa=True,
    invert=False,
    data_type="density",
)

LSOA_POPDENSITY = Variable(
    data=LSOA_STATIC_MASTER["pop_density_persqkm"],
    label="Population Density (sq. km)",
    data_class="challenge",
    invert=False,
    data_type="density",
)

LA_OVER_65 = Variable(
    data=LA_STATIC_MASTER["over_65_count"],
    label="Over Age 65 (%)",
    data_class="challenge",
    la_and_lsoa=True,
    invert=False,
    data_type="count",
)

LSOA_OVER_65 = Variable(
    data=LSOA_STATIC_MASTER["over_65_count"],
    label="Over Age 65 (%)",
    data_class="challenge",
    invert=False,
    data_type="count",
)

LA_WIMD = Variable(
    data=LA_STATIC_MASTER["wimd_2019"],
    label="20% Most Deprived (%)",
    data_class="challenge",
    la_and_lsoa=True,
    invert=False,
    data_type="percentage",
)

LSOA_WIMD = Variable(
    data=LSOA_STATIC_MASTER["wimd_2019"],
    label="Index of Multiple Deprivation (Rank)",
    data_class="challenge",
    invert=True,
    data_type="rank",
)

HAS_INTERNET = Variable(
    data=LA_STATIC_MASTER["has_internet_percent"],
    label="No Internet Access (%)",
    data_class="challenge",
    la_and_lsoa=False,
    invert=True,  # originally percent WITH internet but we need inverse for map
    data_type="percentage",
)

VULNERABLE = Variable(
    data=LA_STATIC_MASTER["vulnerable_pct"],
    label="At Risk Population (%)",
    data_class="challenge",
    la_and_lsoa=False,
    invert=False,
    data_type="percentage",
)

BELONGING = Variable(
    data=LA_STATIC_MASTER["belong_percent"],
    label="Community Cohesion (%)",
    data_class="support",
    la_and_lsoa=False,
    invert=False,
    data_type="percentage",
)

COVID_CASES = Variable(
    data=LA_LIVE_MASTER["covidIncidence_100k"],
    label="COVID-19 Known Cases (%)",
    data_class="challenge",
    la_and_lsoa=False,
    invert=False,
    data_type="per100k",
)

GROUPS = Variable(
    data=LA_LIVE_MASTER["groups_count"],
    label="Community Support Groups (%)",
    data_class="support",
    la_and_lsoa=False,
    invert=False,
    data_type="count",
)

SHIELDING = Variable(
    data=LA_STATIC_MASTER["shielded_count"],
    label="Shielding Population (%)",
    data_class="challenge",
    la_and_lsoa=False,
    invert=False,
    data_type="count",
)

VOLS_TOTAL = Variable(
    data=LA_LIVE_MASTER["total_vol_count"],
    label="Registered Volunteers (%)",
    data_class="support",
    la_and_lsoa=False,
    invert=False,
    data_type="count",
)

VOLS_INCREASE = Variable(
    data=LA_LIVE_MASTER["vol_increase_pct"],
    label="Volunteer Increase since March (%)",
    data_class="support",
    la_and_lsoa=False,
    invert=False,
    data_type="percentage",
)


GP_DIGITAL = Variable(
    data=LA_STATIC_MASTER["MHOL_pct"],
    label="GP Patients registered online",
    data_class="challenge",
    la_and_lsoa=False,
    invert=True,
    data_type="percentage",
)

TWEETS = Variable(
    data=LA_LIVE_MASTER["tweets_percent"],
    label="Tweets About Community Support (%)",
    data_class="support",
    la_and_lsoa=False,
    invert=False,
    data_type="percentage",
)


LA_VARBS = Variables(
    (
        LA_POPDENSITY,
        LA_OVER_65,
        LA_WIMD,
        HAS_INTERNET,
        VULNERABLE,
        BELONGING,
        COVID_CASES,
        SHIELDING,
        GROUPS,
        VOLS_TOTAL,
        VOLS_INCREASE,
        GP_DIGITAL,
        TWEETS,
    )
)

LSOA_VARBS = Variables((LSOA_POPDENSITY, LSOA_OVER_65, LSOA_WIMD))

# Finally, create the data with the json function!
DATA = DataDashboard(la_data=LA_VARBS, lsoa_data=LSOA_VARBS)


if __name__ == "__main__":
    DATA.write()
