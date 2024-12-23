import csv
from pathlib import Path
from dataclasses import dataclass
import json
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

@dataclass
class Exercise_metadata():
    person_id: str
    session: str
    project: str
    sentence: str
    frequency_range: str
    algorithm: str

def extract_metadata_from_praat_file(file:Path) -> Exercise_metadata:
    algorithm = file.name.split('.')[1]
    header = file.name.split('.')[0].split('_')
    frequency_range = file.parent.name

    return Exercise_metadata(algorithm=algorithm, person_id=header[0], session=header[1], project=header[2], sentence=header[3], frequency_range=frequency_range)

@dataclass
class Normalized_time():
    def __init__(self,measures:list[float]):
         if len(measures) != 10:
              raise ValueError("Normalized_time need to have 10 samples")
         self.nt_0 = measures[0]
         self.nt_1 = measures[1]
         self.nt_2 = measures[2]
         self.nt_3 = measures[3]
         self.nt_4 = measures[4]
         self.nt_5 = measures[5]
         self.nt_6 = measures[6]
         self.nt_7 = measures[7]
         self.nt_8 = measures[8]
         self.nt_9 = measures[9]

    nt_0: float
    nt_1: float
    nt_2: float
    nt_3: float
    nt_4: float
    nt_5: float
    nt_6: float
    nt_7: float
    nt_8: float
    nt_9: float

def extract_normalized_time_information(file:Path)-> Normalized_time:
    with open(file) as nt_file:
        reader = csv.reader(nt_file, delimiter='\t')
        frequency = []
        try:
            for row in reader:
                row = row
                if row[2] == 'F0':
                    continue
                frequency.append(row[2])
        except Exception as e: 
            print(e)
            exit(-1)

        return Normalized_time(frequency)
    
@dataclass
class Formatted_normalized_time():
    exercise_metadata: Exercise_metadata
    normalized_time: Normalized_time


def write_csv_header(file_path:Path):
    with open(file_path, mode='w+', newline='') as file:
        writer = csv.writer(file)
        
        m = Exercise_metadata("", "", "", "", "", "")
        d = Normalized_time([0,0,0,0,0,0,0,0,0,0])
        data_instance = Formatted_normalized_time(m,d)
        row = list(data_instance.exercise_metadata.__annotations__.keys()) + list(data_instance.normalized_time.__annotations__.keys())
        writer.writerow(row)

def write_csv_data(file_path, data_instances:Formatted_normalized_time):
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)

        for instance in data_instances:
            row = list(instance.exercise_metadata.__dict__.values()) + list(instance.normalized_time.__dict__.values())
            writer.writerow(row)

def get_list_of_files_to_extract(path_name:Path, praat_algorithm:str) -> list[Path]:
    files_to_extract = []
    for path in Path(path_name).rglob(f'*.{praat_algorithm}'):
        files_to_extract.append(path)
    return files_to_extract

def gather_metadata(praat_directory:Path, praat_algorithm:str):
    files_to_extract: list[Path]
    files_to_extract = get_list_of_files_to_extract(praat_directory, praat_algorithm)

    participants:dict = {}

    for file in files_to_extract:
        exercise = extract_metadata_from_praat_file(file)

        if exercise.person_id not in participants:

            participants[exercise.person_id] = {}
        
        if exercise.session not in participants[exercise.person_id]:
            participants[exercise.person_id][exercise.session] = 1
        else:
           participants[exercise.person_id][exercise.session] = participants[exercise.person_id][exercise.session] + 1
        pass

    json_object = json.dumps(participants, indent = 4) 
    with open(f"output/{praat_algorithm}_participants.json", "w+") as metadata_file:
        metadata_file.write(json_object)
    print(f"number of participants {len(participants)}")
    

def create_new_csv_file_with_header(extracted_data_file, path_to_praat_files:str, praat_algorithm:str):

    files_to_extract = get_list_of_files_to_extract(path_to_praat_files, praat_algorithm)

    write_csv_header(extracted_data_file)

    for file in files_to_extract:
        exercise = extract_metadata_from_praat_file(file)
        data = extract_normalized_time_information(file)
        write_csv_data(extracted_data_file, [Formatted_normalized_time(exercise,data)])



def print_number_of_rows_in_csv(filename:Path):
    with filename.open('r') as file:
        row_count = sum(1 for row in file)
        print(f"the number of files analyzed is {row_count-1}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser = argparse.ArgumentParser(description="Find files with extension '*.normtimef0' and aggregate the "
                                    "10 frequencies in a csv file \n"
                                    "The files should be in a folder hierarchy like this:  \n"
                                    " . \n"
                                    " └── praat_data_d/ \n"
                                    "    └── frequency_range/ \n"
                                    "        └── participant_session_project_sentence.algorithm \n"
                                    "\n"
                                    " . \n"
                                    " └── praat_data_d/ \n"
                                    "    └── F100-F400/ \n"
                                    "       └── ABC123_sesv1_alice_aliceAndBob.normtimef0 \n"
                                    ,formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("-d", "--directory", type=str, help="path to PRAAT files")
    parser.add_argument("-a", "--algorithm", type=str, help="PRAAT algorithm")
    parser.add_argument("-o", "--output", type=str, help="name of outputted files", default="output")
    args = parser.parse_args()

    praat_algorithm:str = args.algorithm
    extracted_data_file:Path = Path(args.output)/ Path(f"{praat_algorithm}_aggregation.csv")
    path_to_praat_files:Path = Path(args.directory) 

    if not path_to_praat_files.resolve().exists():
        eprint(f"Directory '{path_to_praat_files}' does not exist")
        exit(1)

    Path("output").mkdir(parents=True, exist_ok=True)

    gather_metadata(path_to_praat_files, praat_algorithm)

    create_new_csv_file_with_header(extracted_data_file, path_to_praat_files, praat_algorithm)

    print_number_of_rows_in_csv(extracted_data_file)




