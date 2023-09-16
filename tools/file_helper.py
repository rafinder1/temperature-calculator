import pandas as pd
import json


class FileHelper:
    @staticmethod
    def read_csv(file):
        return pd.read_csv(file, sep=",", header=0)

    @staticmethod
    def read_json(file_path):
        with open(file_path, "r") as json_file:
            return json.load(json_file)

    @staticmethod
    def read_excel(file, sheet_name):
        return pd.read_excel(file, sheet_name=sheet_name)
