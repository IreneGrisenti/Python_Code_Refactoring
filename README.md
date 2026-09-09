## Project description  
This project reads order data from a CSV file, cleans, validates the data and produces sales/returns reports.

The unrefactored script is `original_order_report.py` and its output is saved in the `output` folder. The originals were kept to be able to compare outputs after refactoring.   
The refactored version is organized into `src/order_report` and its output is saved in `output_after_refactoring`.


## Quick Start
Clone the repo and install dependencies:  
`git clone https://github.com/IreneGrisenti/Python_Code_Refactoring.git`  
`cd Python_Code_Refactoring`   

Create and activate a virtual environment:  
`python -m venv .venv`  

Windows PowerShell  
`.venv\Scripts\Activate`  

macOS/Linux  
`source .venv/bin/activate`  

Install dependencies:  
`python -m pip install -e .`  


## Environment  
Python 3.13.7  
Packages: NumPy, Pandas, Pytest (see `pyproject.toml`)  


## How to run the program
Run the pipeline from the project root:   
`python __main__.py`


## How to run the tests
Run the full test suite with detailed output showing each test individually:  
`pytest -v`


## Project structure

```text
Python_Code_Refactoring/
├── data/
│   └── orders.csv                # sample input data
├── output/                       # output from the original, unrefactored script
├── output_after_refactoring/     # output from the refactored pipeline
├── src/
│   └── order_report/
│       ├── __init__.py           # public API
│       ├── config.py             # report configuration
│       ├── file_handler.py       # reads input data, saves reports
│       ├── logging_config.py     # logging setup
│       ├── pipeline.py           # orchestrates load > validate > process > save
│       ├── processing.py         # transformations and report generation
│       └── validation.py         # data cleaning and validation
├── tests/
│   ├── test_file_handler.py
│   ├── test_processing.py
│   └── test_validation.py
├── __main__.py                   # entry point
├── original_order_report.py      # original, unrefactored script
├── pyproject.toml                # project metadata and dependencies
├── code_review.md                # review and suggested improvements for the original script
├── reflection.md                 # final reflection
└── README.md
```