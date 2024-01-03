# Patient Similarity Measurement Using variety of medical taxonomies and their combinations
# Research Overview


## Objective
This study aims to answer the research questions:

> "In Patient Similarity, which medical taxonomy gives optimal results in patient similarity? And which combination of taxonomies gives optimal results in patient similarity? And in this case, what ratio gives the optimal result when combining taxonomies?

## Importance
Understanding the effectiveness of these strategies is crucial to:
- Identify state-of-the-art approaches to background knowledge integration.
- Enhance the performance of existing models.
- Guide future research in argument mining.

## Benefits
Through this study, we will:
- Understand the strengths and weaknesses of different strategies.
- Provide insights to improve model performances.
- Contribute to the advancement of argument mining by identifying effective strategies.

## Goals
The study hopes to:
- Create different types of models using the similarity metrics from Informarion Content formulas (IC, CS, SS).
- Observe the model with the optimal weighted f-score results using k-NN machine learning algorithm.
- Observe which medical taxonomy has optimal results, or combinations between them, and even ratios in combining them.

# Project Setup

1. Install git and python
2. Clone the repo
3. Run `python -m venv .venv`
4. Make sure that the venv is activated

## Tool Configuration: Poetry
This project uses Poetry for dependency management and packaging.

5. Install poetry: `pip install poetry`
6. Run `poetry install`

## Dependencies
python = ">=3.10,<3.13"
pandas = "^2.0.3"
ipykernel = "^6.25.0"
scipy = "^1.11.1"
simple-icd-10-cm = "^1.1.2"
numpy = "^1.25.1"
scikit-learn = "^1.3.0"
xmltodict = "^0.13.0"
seaborn = "^0.13.0"

## Running the Project
To evaluate the models using the provided script:

1. Run the file (`drg_to_icd_cm.py`) in order to convert the DRG codes to ICD-10-CM. It should create a new csv file (`drg_to_icd.csv`) in the data folder.
2. Ensure that the configuration file (`config.py`) has been set up correctly and that any paths to datasets, models, or other resources are correct. Main 4 variables in (`config.py`) to be filled are: 'TAXONOMIES', 'IC', 'CS', 'SS', 'WEIGHTS', 'K'.
3. Run the evaluation script using:
```bash
python main.py  
```

## Author
Bilal Mehyar

## Acknowledgments
I would like to thank everyone who contributed to the open-source libraries used in this project and the supervisors who guided me through this research journey.
