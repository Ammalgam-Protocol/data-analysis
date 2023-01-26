import pandas as pd
from pandas import DataFrame


class ArrayToDF:
    @staticmethod
    def convert_to_df(array) -> DataFrame:
        return pd.json_normalize(array)
