import pandas as pd

from io import StringIO
from typing import Union


class CsvFileException(Exception):
    pass


class Utils:
    @staticmethod
    def read_csv(data: bytes) -> Union[dict, None]:
        try:
            df = pd.read_csv(StringIO(data.decode('utf-8')), dtype={
                "name": str,
                "governmentId": str,
                "email": str,
                "debtAmount": float,
                "debtDueDate": str,
                "debtId": str
            })
            return df.to_dict(orient="records")
        except pd.errors.EmptyDataError:
            raise CsvFileException("No data: empty file.")
        except Exception as e:
            raise CsvFileException(f"An unexpected error occurred: {e}")
