"""ETL module for data cleaning and export to csv file"""
import pandas as pd
import os

# ETL for pandas if data source is database may be change some code
# Example: pd.read_sql_table('table_name', 'postgres:///db_name') 

class ETL:
    """ETL class for data cleaning and export to csv file"""

    def __init__(self, csv_path: str, target_path: str):
        self.csv_path = csv_path
        self.target_path = target_path
        self.data_frame = pd.read_csv(
            self.csv_path, names=["date", "name", "email", "phone"]
        )
        self.valid_data_frame = pd.DataFrame()
        self.invalid_data_frame = pd.DataFrame()

    def clean_data(self):
        """Clean data"""
        self.data_frame["phone"] = self.data_frame["phone"].str.replace(
            "[^\d]+", "", regex=True
        )

    def transform_data(self):
        """Transform data"""

        # Split date to day, month, year
        self.data_frame[["day", "month", "year"]] = self.data_frame["date"].str.split(
            "/", expand=True
        )
        self.data_frame["day"] = self.data_frame["day"].str.strip().str.zfill(2)
        self.data_frame["month"] = self.data_frame["month"].str.strip().str.zfill(2)
        self.data_frame["year"] = self.data_frame["year"].str.strip().astype(int) - 543

        # Create ISO date
        self.data_frame["format_date"] = (
            self.data_frame["year"].astype(str)
            + "-"
            + self.data_frame["month"]
            + "-"
            + self.data_frame["day"]
        )

        # Split name to first name and last name
        self.data_frame[["first_name", "last_name"]] = self.data_frame[
            "name"
        ].str.split(" ", expand=True)

        # Tag valid date column
        date_series = pd.to_datetime(self.data_frame["format_date"], errors="coerce")
        self.data_frame["is_valid_date"] = ~date_series.isna()

        # Tag valid email column
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        self.data_frame["is_valid_email"] = self.data_frame["email"].str.contains(
            email_pattern
        )

        # Tag valid phone column
        self.data_frame["is_valid_phone"] = (
            self.data_frame["phone"].str.len() >= 9
        ) & (self.data_frame["phone"].str.len() <= 10)

        # Masking phone number (assume length 9 or 10)
        self.data_frame.loc[
            self.data_frame["phone"].str.len() == 9, "phone"
        ] = self.data_frame["phone"].str.replace(
            r"^(\d{3})(\d{4})(\d{2})$", r"\1" + r"x" * 4 + r"\3", regex=True
        )
        self.data_frame.loc[
            self.data_frame["phone"].str.len() == 10, "phone"
        ] = self.data_frame["phone"].str.replace(
            r"^(\d{3})(\d{5})(\d{2})$", r"\1" + r"x" * 5 + r"\3", regex=True
        )

        # Masking email (assume fix star count to 4)
        self.data_frame["email"] = self.data_frame["email"].replace(
            r"(.{1}).*(.{1}@.+\..+)", r"\1****\2", regex=True
        )

        # Drop unnecessary columns
        self.data_frame.drop(
            ["name", "date", "day", "month", "year"], inplace=True, axis=1
        )

        # Split data to valid and invalid dataframe
        self.valid_data_frame = self.data_frame[
            self.data_frame["is_valid_date"]
            & self.data_frame["is_valid_email"]
            & self.data_frame["is_valid_phone"]
        ].copy()
        self.valid_data_frame.drop(
            ["is_valid_date", "is_valid_email", "is_valid_phone"], axis=1, inplace=True
        )

        self.invalid_data_frame = self.data_frame[
            ~(
                self.data_frame["is_valid_date"]
                & self.data_frame["is_valid_email"]
                & self.data_frame["is_valid_phone"]
            )
        ].copy()
        self.invalid_data_frame.drop(
            ["is_valid_date", "is_valid_email", "is_valid_phone"], axis=1, inplace=True
        )

    def export_data(self):
        """Export data to csv file"""
        self.valid_data_frame.to_csv(
            os.path.join(self.target_path, "valid_data.csv"),
            columns=["format_date", "first_name", "last_name", "email", "phone"],
            index=False,
        )
        self.invalid_data_frame.to_csv(
            os.path.join(self.target_path, "invalid_data.csv"),
            columns=["format_date", "first_name", "last_name", "email", "phone"],
            index=False,
        )

    def run(self):
        """Run the ETL process"""
        self.clean_data()
        self.transform_data()
        self.export_data()
