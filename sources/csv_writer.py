from pathlib import Path
import csv

def write_csv_header(file_path:Path, header:list[str]):
    with open(file_path, mode='w+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)

def write_csv_data(file_path:Path, rows):
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)

        for row in rows:
            writer.writerow(row)
