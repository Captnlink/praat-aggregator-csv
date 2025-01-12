from dataclasses import dataclass
from pathlib import Path

@dataclass
class Sentence_metadata():
    person_id: str
    session: str
    project: str
    sentence: str
    frequency_range: str
    algorithm: str

def deserialize_metadata_from_file(file:Path) -> Sentence_metadata:
        algorithm = file.name.split('.')[1]
        header = file.name.split('.')[0].split('_')
        frequency_range = file.parent.name

        return Sentence_metadata(algorithm=algorithm, person_id=header[0], session=header[1], project=header[2], sentence=header[3], frequency_range=frequency_range)

