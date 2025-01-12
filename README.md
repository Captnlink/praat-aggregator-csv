# PRAAT file aggregator

This script is used to aggregate the output of algorithms generated with PRAAT into a CSV

The scrip will find all files in a directory and its sub-directory that match the algorithm and perform the operation on them.

It reads all files with an extension equal to the `chosen_algorithm` and transform each of them in a single line of a CSV.

## Installation

### Install dependencies

Depending on your OS, do these following steps to install the required software dependencies.

MacOS systems

``` shell
brew install python
```

Linux Systems (Debian)

``` shell
sudo apt get install python
```

Windows System

- Download and install [Python](https://www.python.org/downloads/)

### Install the script

Open a terminal and navigate to the directory you want to install the script.

Clone this repository using this line:

``` shell
git clone https://github.com/Captnlink/praat-aggregator-csv.git
```

## How to use

### Data files structure

Each file should be named `participantID_sessionName_projectName_SentenceName.algorithm`.
Each file should be in a subfolder named after the frequency range of the PRAAT analysis

You should prepare the folder containing the PRAAT data like this:

``` text
.
└── PRAAT_data/
    └── frequency_range/
        └── participantID_sessionName_projectName_SentenceName.algorithm
        └── ...
```

``` text
.
└── PRAAT_data/
    └── 250-300/
        └── p12345_v1_projectX_s1.norntimef0
        └── ...
```

### Executing the script

Execute the following command line replacing `PATH/TO/DIRECTORY"` with the path of the PRAAT file location and `chosen_algorithm` with the appropriate algorithm.

``` shell
python praat-aggregator-csv/sources/main.py -d "PATH/TO/DIRECTORY" -a chosen_algorithm
```

The possible algorithms are:

- normtimef0
- normtime_f0acceleration
- normtime_f0velocity
- normtime_semitonef0

### Generated files

The generated files will be located under `praat-aggregator-csv/output`

- algorithm_aggregation.csv: The aggregated values of all praat files with target algorithm
- algorithm_participants.json: The count of the number of occurrence of a certain algorithm
