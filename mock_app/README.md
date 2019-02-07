# CLI application

The aim of the application is to process a set of SAM files resulting from the CRISPR screen experiment and generate a TSV file with counts of genes related to the identified gRNAs. The application requires also a FASTA file with a the screen library gRNAs sequences. Additionally, the appliation may generate plots summarizin results for all sam files.

## Running the application in virtual environment

Prepare the environment:
```virtualenv  .venv```
```source .venv/bin/activate```
```cd mock_app```
```pip install -r requirements.txt```

## Running the application in docker

Build the docker image:
```docker build -t contra-python .```

Run the container with the app included:
```docker run -it --rm -v <path to the folder with app and data>:/tutorial contra-python bash ```

In the container you may need to run additional commands:
```export LC_ALL=C.UTF-8```
```export LANG=C.UTF-8```


## Usage of the application

Help: 

```python3 main.py build --help```

Running the app:

```python3 main.py build --sam ../data/sam_files --fasta ../data/screen_library.fasta --plot```

Running tests:

```python3 -m unittest discover -v ```

