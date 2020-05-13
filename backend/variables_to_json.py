import pandas as pd
from dataclasses import dataclass
from typing import Sequence
from warnings import warn
import os
import json

# Local imports
from master_datasets import LA_MASTER, LSOA_MASTER

##### Local Files for Debugging/Testing
# LA_MASTER = pd.read_csv('la_master.csv', index_col=['area_code'])
# LA_MASTER.rename(columns={'wimd_20pct_percent':'wimd_2019'}, inplace=True)
# LSOA_MASTER = pd.read_csv('lsoa_master.csv',index_col=['area_code', 'area_name'])


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
        self.data_transformed_ = self.transform_per100k()
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

    def transform_per100k(self):
        """Based on variable type, perform transformation"""
        if self.data_type == "percentage":
            return self.data_transformed_ * 1000
        elif self.data_type == "count":
            if self.res == "LA":
                return (self.data_transformed_ / LA_POPULATION) * 1000
            elif self.res == "LSOA":
                return (self.data_transformed_ / LSOA_POPULATION) * 1000
        elif self.data_type == "density":
            return self.data_transformed_
        elif self.data_type == "rank":
            return self.data_transformed_
        elif self.data_type == "per100k":
            return self.data_transformed_
        else:
            raise Exception(
                "Transformation of data type: {} are not suppored".format(
                    self.data_type
                )
            )

    def invert_data(self):
        """Invert data direction AFTER transformation"""
        if self.data_type in ["percentage", "count", "per100k"]:
            return 100000 - self.data_transformed_
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
            os.path.abspath(os.path.dirname(__file__)),
            "..",
            "frontend",
            "map",
            "data",
            "data.json",
        )
        with open(JSON_OUT, "w") as outfile:
            json.dump(self.to_json(), outfile)


LA_POPULATION = LA_MASTER["population_count"]
LSOA_POPULATION = LSOA_MASTER["population_count"]

LA_POPDENSITY = Variable(
    data=LA_MASTER["pop_density_persqkm"],
    label="Population Density (people per sq km)",
    data_class="challenge",
    la_and_lsoa=True,
    invert=False,
    data_type="density",
)

LSOA_POPDENSITY = Variable(
    data=LSOA_MASTER["pop_density_persqkm"],
    label="Population Density (people per sq km)",
    data_class="challenge",
    invert=False,
    data_type="density",
)

LA_OVER_65 = Variable(
    data=LA_MASTER["over_65_count"],
    label="Over Age 65 (per 100,000 people)",
    data_class="challenge",
    la_and_lsoa=True,
    invert=False,
    data_type="count",
)

LSOA_OVER_65 = Variable(
    data=LSOA_MASTER["over_65_count"],
    label="Over Age 65 (per 100,000 people)",
    data_class="challenge",
    invert=False,
    data_type="count",
)

LA_WIMD = Variable(
    data=LA_MASTER["wimd_2019"],
    label="20% Most Deprived (per 100,000 people)",
    data_class="challenge",
    la_and_lsoa=True,
    invert=False,
    data_type="percentage",
)

LSOA_WIMD = Variable(
    data=LSOA_MASTER["wimd_2019"],
    label="Index of Multiple Deprivation (Rank)",
    data_class="challenge",
    invert=True,
    data_type="rank",
)

HAS_INTERNET = Variable(
    data=LA_MASTER["has_internet_percent"],
    label="No Internet Access (per 100,000 people)",
    data_class="challenge",
    la_and_lsoa=False,
    invert=True,  # originally percent WITH internet but we need inverse for map
    data_type="percentage",
)

VULNERABLE = Variable(
    data=LA_MASTER["vulnerable_pct"],
    label="At Risk Population (per 100,000 people)",
    data_class="challenge",
    la_and_lsoa=False,
    invert=False,
    data_type="percentage",
)

BELONGING = Variable(
    data=LA_MASTER["belong_percent"],
    label="Community Cohesion (per 100,000 people)",
    data_class="support",
    la_and_lsoa=False,
    invert=False,
    data_type="percentage",
)

COVID_CASES = Variable(
    data=LA_MASTER["covidIncidence_100k"],
    label="COVID-19 Known Cases (per 100,000 people)",
    data_class="challenge",
    la_and_lsoa=False,
    invert=False,
    data_type="per100k",
)

GROUPS = Variable(
    data=LA_MASTER["group_count"],
    label="Community Support Groups",
    data_class="support",
    la_and_lsoa=False,
    invert=False,
    data_type="count",
)

SHIELDING = Variable(
    data=LA_MASTER["shielded_count"],
    label="Sheilding Population",
    data_class="challenge",
    la_and_lsoa=False,
    invert=False,
    data_type="count",
)

# TWEETS = Variable(
#     data=LA_MASTER["tweets_count"],
#     label="Tweets About Community Support",
#     data_class="support",
#     la_and_lsoa=False,
#     invert=False,
#     data_type="count",
# )


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
        # TWEETS
    )
)

LSOA_VARBS = Variables((LSOA_POPDENSITY, LSOA_OVER_65, LSOA_WIMD))

# Finally, create the data with the json function!
DATA = DataDashboard(la_data=LA_VARBS, lsoa_data=LSOA_VARBS)


if __name__ == "__main__":
    DATA.write()
