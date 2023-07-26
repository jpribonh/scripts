import boto3
import csv

def count_files_in_s3(bucket_name, csv_file_path):
    # Initialize the S3 client
    s3 = boto3.client('s3')

    # Read the CSV file containing the list of file names
    file_names = []
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            file_names.extend(row)
    print(file_names)
    # Count the number of files in the S3 bucket
    file_count = 0
    for file_name in file_names:
        try:
            s3.head_object(Bucket=bucket_name, Key=file_name)
            file_count += 1
        except s3.exceptions.NoSuchKey:
            pass
        except Exception as e:
            print(f"Error occurred while processing file '{file_name}': {e}")
            # Handle other types of exceptions here if needed.


    return file_count

if __name__ == "__main__":
    # Replace 'your-bucket-name' with the name of your S3 bucket
    bucket_name = 'skywellprod'
    
    # Replace 'your-csv-file.csv' with the path to your CSV file containing the file names
    csv_file_path = 'key_names.csv'

    num_files = count_files_in_s3(bucket_name, csv_file_path)
    print(f"Number of files found in S3 bucket '{bucket_name}': {num_files}")