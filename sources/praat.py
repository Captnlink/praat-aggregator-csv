from dataclasses import dataclass
from algorithms.normalized_time import Normalized_time
from algorithms.metadata import Sentence_metadata
from algorithms.algorithms import get_serializer
from csv_writer import write_csv_header, write_csv_data
from pathlib import Path
import json

@dataclass
class Formatted_normalized_time():
    metadata: Sentence_metadata
    normalized_time: Normalized_time


class Analysis():
    output_location:str
    input_location:str
    algorithm:str

    def __init__(self, input_location:str, output_location:str, algorithm):
        self.input_location = input_location
        self.output_location = output_location
        self.algorithm = algorithm
        pass


    def _get_list_of_files_to_extract(self) -> list[Path]:
        files_to_extract = []
        for path in self.input_location.rglob(f'*.{self.algorithm}'):
            files_to_extract.append(path)
        return files_to_extract
    

    def extract_metadata_as_json(self):
        files_to_extract = self._get_list_of_files_to_extract()
        participants_metadata:dict = {}

        for file in files_to_extract:
            serializer = get_serializer('metadata')
            file_metadata = serializer(file)

            if file_metadata.person_id not in participants_metadata:

                participants_metadata[file_metadata.person_id] = {}
            
            if file_metadata.session not in participants_metadata[file_metadata.person_id]:
                participants_metadata[file_metadata.person_id][file_metadata.session] = 1
            else:
                participants_metadata[file_metadata.person_id][file_metadata.session] = participants_metadata[file_metadata.person_id][file_metadata.session] + 1
        
        return participants_metadata
    

    def save_metadata(self, participant_metadata:str):

        json_object = json.dumps(participant_metadata, indent = 4) 
        with open(f"{self.output_location}/{self.algorithm}_participants.json", "w+") as file:
            file.write(json_object)
        print(f"number of participants {len(participant_metadata)}")


    def _create_csv_header(self) -> list[str]:
        m = Sentence_metadata("", "", "", "", "", "")
        d = Normalized_time([0,0,0,0,0,0,0,0,0,0])
        return list(m.__annotations__.keys()) + list(d.__annotations__.keys())


    def _concat_data_to_metadata(self, m:Sentence_metadata, d:Normalized_time):
        return list(m.__dict__.values()) + list(d.__dict__.values())


    def aggregate_and_save_data_to_csv(self):

        files_to_extract = self._get_list_of_files_to_extract()
        extracted_data_file:Path = Path(f"{self.output_location}/{self.algorithm}_aggregation.csv")
        
        write_csv_header(extracted_data_file, self._create_csv_header())

        for file in files_to_extract:
            metadata_serializer = get_serializer('metadata')
            exercise = metadata_serializer(file)

            data_serializer = get_serializer(self.algorithm)
            data = data_serializer(file)

            write_csv_data(extracted_data_file, [self._concat_data_to_metadata(exercise, data)])
