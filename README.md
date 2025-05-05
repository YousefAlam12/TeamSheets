### TeamSheets
to run project:

## NOTE (Only if zip file does not work): 
You will need to change settings.py, and change the variable EMAIL_HOST_PASSWORD to use the registered authentication key.
For security reasons this has been removed from the GIT repository.  Please contact me to get the key or use key in zip file (this is only for email notifications).

### Create Conda Environment
Install miniconda https://docs.conda.io/en/latest/miniconda.html

Create a conda environment for this project and activate the environment:

$ conda create --name fyp python=3.11
$ conda activate fyp

install the following:

$ conda install conda-forge::gdal


### Install backend (Python) dependencies
With the conda environment active, enter the backend directory (folder where requirements.txt is inside):

(fyp)$ pip install -r requirements.txt


### Start backend server
Run backend server:

(fyp)$ python manage.py runserver


### Start frontend server
Create a seperate terminal and enter the frontend directory, then to run frontend server:

$ npm install
$ npm run dev
and the server will start on http://localhost:5173 (use this link)



Note: all test users have password=test1234

When running tests exceptions can be ignored (occurs due to Django blocking sending emails during tests)
