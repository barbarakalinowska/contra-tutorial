# CLI application

The aim of the application is to process a set of SAM files resulting from the CRISPR screen experiment and generate  TSV files with counts of genes related to the identified gRNAs. The application requires also a FASTA file with a the screen library gRNAs sequences. Additionally, the application may generate plots summarizing results for all SAM files.

## Running the application in virtual environment

Prepare the environment:

```virtualenv  .venv```
```source .venv/bin/activate```
```cd app```
```pip install -r requirements.txt```

## Running the application in docker

Build the docker image:
```docker build -t contra-python .```

Please note that the Dockerfile copies one file from `app` directory, so this path needs to be updated if the requirements.txt file is located in a different place.

Run the container with the app included:
```docker run -it --rm -v <path to the folder with app and data>:/tutorial contra-python bash ```


## Usage of the application

Help:

```python3 main.py build --help```

Running the app:

```python3 main.py build --sam ../data/sam_files --fasta ../data/screen_library.fasta --plot```

Running tests:

```python3 -m unittest discover -v ```
