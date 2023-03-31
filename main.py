import argparse
import pathlib
import os
import pandas as pd
import numpy as np


def transform_data(df):
    """Transforms the data to the desired format.
    1. Convert data to ISO format
    2. Separate first name and last name
    3. Masking email (a****z@domain.com)
    4. Masking phone number (081xxxxx00)"""


def main(config):
    """Main function of the project."""
    # Read data from csv file
    df = pd.read_csv(config["src"])
    print(df.head())
    # Transform data
    # df = transform_data(df)
    # Save data to csv file
    # df.to_csv(config["target"], index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Receives src file and load to target location",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("src", help="Source file in csv format")
    parser.add_argument("target", help="Target location")
    args = parser.parse_args()
    config = vars(args)
    # print(config)

    main(config)
