import pandas as pd


def main():
    file_path = "csdata.csv"

    df = pd.read_csv(file_path)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    print(df)









main()