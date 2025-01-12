# PRAAT file aggregator

This script is used to aggregate the output of algorithms generated with PRAAT into a CSV

## Installation

### Install dependencies

Macos systems

``` shell
brew install python
```

Linux Systems (Debian)

``` shell
sudo apt get install python
```

Windows system

- Download and install [Python](https://www.python.org/downloads/)
- Install [Pip](https://www.geeksforgeeks.org/how-to-install-pip-on-windows/)

### Install the script

Clone this repository

``` shell
git clone git@github.com:Captnlink/praat-aggregator-csv.git
```

## How to use

There is two operation available, `aggregate` and `count`.
The scrip will find all files in a directory and its sub-directory that match the algorithm and perform the operation on them.

### File naming scheme

Each file should be named `participantID_sessionName_projectName_SentenceName.algorithm`.
Each file should be in a subfolder named after the frequency range of the PRAAT analysis

### Aggregate function

The aggregate function read all files with an extension equal to `algorithm` and transform them in
a single line of a CSV.

In a terminal

``` shell
python sources/main.py -d "PATH/TO/DIRECTORY" -a algorithm aggregate
```

``` shell
python sources/main.py -d "PATH/TO/DIRECTORY" -a normtimef0 aggregate
```

### Count function

Count the number of occurrence of a certain algorithm and generate a JSON file

In a terminal

``` shell
python sources/main.py -d "PATH/TO/DIRECTORY" -a wav count
```
