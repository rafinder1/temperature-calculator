import pandas as pd


class FileHelper:
    @staticmethod
    def read_csv(file):
        # Read the text file into a DataFrame
        return pd.read_csv(file, sep=",", header=0)
