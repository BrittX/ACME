# ACME
Sure 2022 Backend Take Home Prompt

## Setup

The ACME repository assumes python 3.11+ and poetry are installed on the machine.

Clone the repository in your project directory, navigate into the cloned directory and install the requirements using poetry.

```bash
git clone git@github.com:BrittX/ACME.git
cd ACME
poetry install --without dev
```

### Running the application

After setup, enter your virtual environment, migrate the database, run the server and interact with the API.

```bash
source $(poetry env info --path)/bin/activate
cd acme
./manage.py migrate && ./mange.py runserver
```

## Interacting with API

When the server is running, you can head to [`localhost:8000`](localhost:8000) in a web browser to see the API root for the `quotes` endpoint. Click the URL to go directly to the `quotes` endpoint ([`localhost:8000/quotes/`](localhost:8000/quotes/)), and enter the Quote information to generate an object in the database and return the pricing information.

Click the link in the "url" field to go directly to a specific saved quote or enter the quote uuid to access a specific quote. E.g. [localhost:8000/quotes/{quote_uuid}/](localhost:8000/quotes/{quote_uuid})


### Testing

The `poetry install` will include the test dependencies from setup. While in the virtual environment, run `./manage.py test` to run the projects tests.

```bash
# Make sure you're in the `ACME/acme` directory
./manage.py test
```

Expected Output:
```bash
(acme-py3.11) bash-5.2$ ./manage.py test
Found 9 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.........
----------------------------------------------------------------------
Ran 9 tests in 0.007s

OK
Destroying test database for alias 'default'...
```