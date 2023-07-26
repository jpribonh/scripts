import pandas as pd

def print_message(row):
    SystemId = row['SystemId']
    key = row['FileName']
    print(f"aws s3 rm s3://skywellprod/{SystemId}/{key}")


csvFile = pd.read_csv('DocumentsToBeDeleted.csv')
csvFile.apply(print_message, axis=1)
