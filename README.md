# SRT Backend

## Description
This service is meant to be run on the computer that is connected to the SRT telescope at Johns Hopkins University.
In order for the user requests from the accompanying website to be fulfilled, this service must be running. The website
will remain operational even if this service is not running, but the user requests will not be fulfilled and users, will 
be waiting for email with their results that will not come.

## Installation and Setup
1. Install Python 3.10 or higher
2. Install pip
3. Run the following command to create a venv: `python3 -m venv venv`
4. Activate the venv: `source venv/bin/activate`
5. Install the requirements: `pip install -r requirements.txt`
6. Create a `.env` file and copy the values from the `.env.example` file
7. Populate the `.env` file with the correct values
8. Run the service: `python3 main.py`
