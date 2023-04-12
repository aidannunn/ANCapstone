import pandas as pd

class LoadData:
    """Class used to load a CSV file of data into a pandas dataframe for use in the logic modules"""

    def __init__(self, file):
        self.df = pd.read_excel(file)

    def printDataFrame(self):
        """Method for printing the dataframe to a terminal window."""
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(self.df)