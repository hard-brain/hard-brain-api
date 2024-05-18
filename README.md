# Hard Brain API

A service for providing song data and audio files for Beatmania IIDX music.

## Installation (for development)

### Requirements

- Python (3.10.10)
- Poetry (1.7.1 recommended)

### Steps

1. Clone the project and run `poetry install`. This should create a new virtual environment with all dependencies.
2. Run `poetry shell` and `uvicorn src.main:app --reload`

Songs used for Hard Brain quiz questions are placed here, but not included on the main repo due to file size and legal
reasons. [Songs can be downloaded from here](https://corndog.galaxy.usbx.me/nextcloud/s/Q56JdfDpy8GMocd) and are
required for the `/audio/{song_id}` endpoint to work. Unzip the archive and place the contents in a folder called
`songs` in the project root directory. When running this project via
[hard-brain-deploy](https://github.com/hard-brain/hard-brain-deploy), the songs will bind mount onto the hard-brain-api
container under `/app/src/resources/songs/`

## Building and running via Docker

Please refer to the [hard-brain-deploy](https://github.com/hard-brain/hard-brain-deploy) for instructions on how to
deploy the backend for development or production environments.

### Running tests

A Compose file is included for running the tests against. Once running, run the `test_main.py` file with the following
environment variables set:

| Environment Variable | Value           |
|----------------------|-----------------|
| PGUSER               | "postgres"      |
| POSTGRES_DB          | "hard-brain-db" |
| DB_HOSTNAME          | "db"            |
| POSTGRES_PASSWORD:   | "testdb"        |
