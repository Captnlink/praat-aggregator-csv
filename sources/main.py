from pathlib import Path
import argparse
from praat import Analysis


if __name__ == "__main__":
    
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
    output_directory:Path =  Path(args.output)
    extracted_data_file:Path = output_directory / Path(f"{praat_algorithm}_aggregation.csv")
    praat_directory:Path = Path(args.directory) 

    if not praat_directory.resolve().exists():
        print(f"Directory '{praat_directory}' does not exist")
        exit(1)

    output_directory.mkdir(parents=True, exist_ok=True)

    a = Analysis(praat_directory, output_directory, praat_algorithm)

    if praat_algorithm is not "wav":
        a.aggregate_and_save_data_to_csv()

    participant_metadata = a.extract_metadata_as_json()
    a.save_metadata(participant_metadata)

  





