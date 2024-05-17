# Hard Brain

A service for song quizzes for Beatmania IIDX music.

## Installation (for development)

### Requirements

- Python (3.10.10)
- Poetry (1.7.1 recommended)

1. Clone the project and run `poetry install`. This should create a new virtual environment with all dependencies.
2. Run `poetry shell` and `uvicorn src.main:app --reload`

Songs used for Hard Brain quiz questions are placed here, but not included on the main repo due to file size and legal
reasons. [Songs can be downloaded from here](https://corndog.galaxy.usbx.me/nextcloud/s/Q56JdfDpy8GMocd) and are
required for the `/audio/{song_id}` endpoint to work. Unzip the archive and place the contents in a folder called
`songs` in the project root directory.

## Building and running via Docker

Before building the Docker image, please ensure the songs are placed in the `src/resources/songs/` directory. A .env
file should also be created using the template and placed in the project root.

The service can be started via docker-compose by running `docker compose up -d`. This will start the backend, database
and Adminer on ports 8000, 5432 and 8080 respectively.
