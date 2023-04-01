"""Main module for the project"""
import argparse
from etl import ETL

def main():
    """Main function for the project"""
    parser = argparse.ArgumentParser(
        description="Receives src file and load to target location",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("src", help="Source file in csv format")
    parser.add_argument("target", help="Target location")
    args = parser.parse_args()
    config = vars(args)
    # print(config)

    # Run ETL process
    etl_obj = ETL(config["src"], config["target"])
    etl_obj.run()


if __name__ == "__main__":
    main()