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
8. Test the service runs correctly: `python3 main.py`
9. Now that the service is running correctly we need to setup the service to run in the background. Please close the
   running service.
10. Run the service in the background: `nohup python3 main.py &`

## Usage

**NOTE:** If the computer has been shut down or the service has been stopped and has been previously setup, then the
following steps are all that is needed to run the service:

1. Activate the venv: `source venv/bin/activate`
2. Test the services still runs correctly: `python3 main.py`
3. Now that the service is running correctly we need to setup the service to run in the background. Please close the
   running service.
4.Run the service in the background: `nohup python3 main.py &` 
