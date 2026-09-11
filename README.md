## Project description  
This project reads order data from a CSV file, validates, cleans the data and produces sales/returns reports.

The unrefactored script is `original_order_report.py` and its output is saved in the `output` folder. The originals were kept to be able to compare outputs after refactoring.   
The refactored version is organized into `src/order_report` and its output is saved in `output_after_refactoring`.


## Quick Start
Clone the repo:  
`git clone https://github.com/IreneGrisenti/Python_Code_Refactoring.git`  

Create and activate a virtual environment:  
`cd Python_Code_Refactoring`    
`python -m venv .venv`  

`source .venv/bin/activate` (for macOS/Linux)  
or  
`.venv\Scripts\Activate` (for Windows PowerShell)  

Install dependencies:  
`python -m pip install -e .`  


## Environment  
Python 3.13.7  
Packages: NumPy, Pandas, Pytest (see `pyproject.toml`)  


## How to run the program
Run the pipeline from the project root:   
`python -m order_report`


## How to run the tests
Run the full test suite with detailed output for each test:  
`pytest -v`


## Project structure

```text
Python_Code_Refactoring/
├── data/
│   └── orders.csv                # sample input data
├── output/                       # output from the original script
├── output_after_refactoring/     # output from the refactored pipeline
├── src/
│   └── order_report/
│       ├── __init__.py           # public API
│       ├── __main__.py           # entry point
│       ├── cleaning.py           # data validation and cleaning
│       ├── config.py             # report configuration
│       ├── file_handler.py       # reads input, saves outputs
│       ├── logging_config.py     # logging setup
│       ├── pipeline.py           # orchestrates load > clean > process > save
│       └── processing.py         # transformations and aggregation
├── tests/
│   ├── test_cleaning.py 
│   ├── test_file_handler.py
│   └── test_processing.py
├── original_order_report.py      # original script
├── pyproject.toml                # project metadata and dependencies
├── code_review.md                # review and suggested improvements for the original script
├── reflection.md                 # final reflection
└── README.md
```