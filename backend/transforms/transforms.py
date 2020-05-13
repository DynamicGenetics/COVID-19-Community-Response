"""General Transformers"""

from typing import Sequence, Callable
from pandas import DataFrame

Transformer = Callable[[DataFrame], DataFrame]

__all__ = ["Compose"]


class Compose:
    """Compose a pipeline of multiple transformers"""

    def __init__(self, transforms: Sequence[Transformer]):
        self.transforms = transforms

    def __call__(self, df: DataFrame) -> DataFrame:
        for t in self.transforms:
            df = t(df)
        return df
