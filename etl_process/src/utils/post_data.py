from pathlib import Path
import pandas as pd


def post(location: str, fileName: str, data: pd.DataFrame) -> bool:
    """
        Save a pandas DataFrame to a CSV file in the specified location.

        Args:
            location (str): Subdirectory within the data folder where the file will be saved
            fileName (str): Name of the CSV file to create (should include .csv extension)
            data (pd.DataFrame): DataFrame to save as CSV

        Returns:
            bool: True if file was saved successfully, False if an error occurred
    """
    data_path = Path(__file__).parent.parent.parent / "data" / location / fileName
    try:
        with open(data_path, "w+", newline='') as file:
            data.to_csv(file)
        return True
    except Exception as e:
        print(e)
        return False


if __name__ == "__main__":
    testDF = pd.DataFrame(
        {
            "A": [1, 2],
            "B": [3, 4]
        }
    )
    result = main("test", "sample.csv", testDF)
    print(f"result:{result}")
