import pandas as pd
from dataclasses import dataclass
from typing import Sequence

# from datasets import LA_population_count, LSOA_population_count


@dataclass
class Variable:

    data: pd.Series  # Should call variable from variables.py?
    name: str  # Variable name in dataset
    label: str  # Human readable label
    data_class: str  # Is the data 'support' or 'challenge'
    la: bool  # Is this an LA level variable?
    invert: bool  # Does the direction of the data need to be inverted before mapping?
    data_type: str  # Is the data a percentage, a count or a rank?
    # Is this data available at LSOA level too? (Only needed for LA level varbs)
    lsoa_available: bool = False

    # @property
    # def is_valid(self):
    #     # Some method for making sure the variable exists - if not then PROBLEM -
    #     # run pipeline?
    #     try:
    #         _ = self.something
    #     except FileNotFoundError:
    #         return False
    #     else:
    #         return True

    def transform(self):
        """Based on variable type, perform transformation"""

        if self.data_type == "percentage":
            return self.data * 1000
        # elif transformation == 'count':
        #    return (data/datasets.population_count)*100000
        elif self.data_type == "density":
            return self.data
        elif self.data_type == "rank":
            return self.data
        elif self.data_type == "per100k":
            return self.data
        else:
            raise Exception("Transformations of this data type are not yet supported")

    def to_json(self):
        return {
            "name": self.name,
            "label": self.label,
            "class": self.data_class,
            "lsoa": self.lsoa_available,
        }


@dataclass
class Variables:
    variables: Sequence[Variable]

    def to_json(self):
        return [var.to_json() for var in self.variables]


@dataclass
class DataDashboard:
    variables: Variables
    las: bool

    def to_json(self):
        return {"variables": self.variables.to_json(), "LAs": self.las}


LA_POPDENSITY = Variable(
    name="pop_density_persqkm",
    label="Population Density",
    data_class="challenge",
    la=True,
    lsoa_available=True,
    invert=False,
    data_type="density",
)

LSOA_POPDENSITY = Variable(
    name="pop_density_persqkm",
    label="Population Density",
    data_class="challenge",
    la=False,
    invert=False,
    data_type="density",
)

LA_OVER_65 = Variable(
    name="over_65_count",
    label="Population Over Age 65",
    data_class="challenge",
    la=True,
    lsoa_available=True,
    invert=False,
    data_type="count",
)

LSOA_OVER_65 = Variable(
    name="over_65_count",
    label="Population Over Age 65",
    data_class="challenge",
    la=False,
    invert=False,
    data_type="count",
)

LA_WIMD = Variable(
    name="wimd_2019",
    label="Deprivation (WIMD)",
    data_class="challenge",
    la=True,
    lsoa_available=True,
    invert=False,
    data_type="percentage",
)

LSOA_WIMD = Variable(
    name="wimd_2019",
    label="Deprivation (WIMD)",
    data_class="challenge",
    la=False,
    invert=True,
    data_type="rank",
)

HAS_INTERNET = Variable(
    name="has_internet_pct",
    label="Population Without Internet Access",
    data_class="challenge",
    la=True,
    lsoa_available=False,
    invert=True,  # originally percent WITH internet but we need inverse for map
    data_type="percentage",
)

VULNERABLE = Variable(
    name="vulnerable_pct",
    label="At Risk Population",
    data_class="challenge",
    la=True,
    lsoa_available=False,
    invert=False,
    data_type="percentage",
)

BELONGING = Variable(
    name="belong_percent",
    label="Community Cohesion",
    data_class="support",
    la=True,
    lsoa_available=False,
    invert=False,
    data_type="percentage",
)

COVID_CASES = Variable(
    name="covid_per100k",
    label="COVID-19 Known Cases",
    data_class="challenge",
    la=True,
    lsoa_available=False,
    invert=False,
    data_type="per100k",
)

GROUPS = Variable(
    name="groups_count",
    label="Community Support Groups",
    data_class="support",
    la=True,
    lsoa_available=False,
    invert=False,
    data_type="count",
)

SHIELDING = Variable(
    name="shielded_percent",
    label="Sheilding Population",
    data_class="challenge",
    la=True,
    lsoa_available=False,
    invert=False,
    data_type="count",
)

TWEETS = Variable(
    name="tweets_count",
    label="Tweets About Community Support",
    data_class="support",
    la=True,
    lsoa_available=False,
    invert=False,
    data_type="count",
)
