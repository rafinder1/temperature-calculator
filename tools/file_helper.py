import pandas as pd
import json


class FileHelper:
    @staticmethod
    def read_csv(file):
        return pd.read_csv(file, sep=",", header=0)
