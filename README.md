# amadeus-api

lien vers le cahier des charges : https://docs.google.com/document/d/1iVH0wNnciFB2ZnLl3I72BhiNmuMY6s5fuKCwJGCaiDU/edit


## Run the project

Create a virtual enviroment:
    ```python3 -m venv env```

Make sure to install all the librairies needed in your virtual environment:
    ```pip install -r /requirements.txt```

create a file called tokens.py in / and add your amadeus credentials:
    ```client_id='my_client_id'
    client_secret='my_client_secret_pass'```

run the next command (from /) to start the server:
    ```python3 manage.py runserver```

## Make a test

You can make a test to verify if it works as it should!
    ```python3 api_calls.py```

NOTE: The test is currently not working:
*- Modules not found*
*- Libraries not found in the venv*
