# TraderMade CFD Data Processing

This project fetches, processes, and displays CFD data from the TraderMade API.

## Requirements

*   Python 3.6+
*   TraderMade API key (set as environment variable `TRADERMADE_API_KEY`)
*   Libraries: pandas, ipython, tradermade

## Setup

1.  Clone the repository.
2.  Install the requirements: `pip install -r requirements.txt`
3.  Set the `TRADERMADE_API_KEY` environment variable.

## Usage

1.  Run `src/main_fetch.py` to fetch and save data.
2.  Run `src/data_integrator.py` to integrate the data.
3.  Run `src/indicator_calculator.py` to calculate the indicators.
4.  Run `src/view.py` to display the results.