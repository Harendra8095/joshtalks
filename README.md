# JoshTalks
## Backend Task
To make an API to fetch latest videos sorted in reverse chronological order of their publishing date-time from YouTube for a given tag/search query in a paginated response.
## Basic Requirements:
- Server should call the YouTube API continuously in background (async) with some interval (say 10 seconds) for fetching the latest videos for a predefined search query and should store the data of videos (specifically these fields - Video title, description, publishing datetime, thumbnails URLs and any other fields you require) in a database with proper indexes.
- A GET API which returns the stored video data in a paginated response sorted in descending order of published datetime.
- A basic search API to search the stored videos using their title and description.
## Instructions:
- You are free to choose any search query, for example official, cricket, football etc. (choose something that has a high frequency of video uploads)
- Try and keep your commit messages clean, and leave comments explaining what you are doing wherever it makes sense.
- Also try and use meaningful variable/function names, and maintain indentation and code style.
- Submission should have a `README` file containing instructions to run the server and test the API.
- Preferred language & Framework
    Python (DRF, Django, Flask)
## Reference:
- YouTube data v3 API: [https://developers.google.com/youtube/v3/getting-started](https://developers.google.com/youtube/v3/getting-started)
- Search API reference: [https://developers.google.com/youtube/v3/docs/search/list](https://developers.google.com/youtube/v3/docs/search/list)
    - To fetch the latest videos you need to specify these: type=video, order=date, publishedAfter=<SOME_DATE_TIME>
    - Without publishedAfter, it will give you cached results which will be too old

## Prerequisite:
- Python3
- PostgreSQL
- npx(Optional but recommended)


# Settingup Project

- #### Step 1 (optional but recommended)

  Create a python virtual environment by using virtualenv or conda

  ```bash
  conda create -n environment python3.6
  ```

  or

  ```bash
  python3 -m venv environment && source venv/bin/activate
  ```

- #### Step 2

  Clone this repo

  ```bash
  git clone https://github.com/Harendra8095/joshtalks.git && cd joshtalks
  ```

- #### Step 3

  Install dependencies

  ```bash
  pip install -r requirements.txt
  ```

- #### Step 4

  Create following environment variables
  
  or

  make an .env file and remove export from below variables

  You must create Database first in your postgresql

  ```bash
    export DB_DIALECT=postgresql
    export DB_HOST=< Your Postgres Host >
    export DB_PORT=< Your Postgres Port >
    export DB_USER=< Your Postgres User >
    export DB_PASS=< Your Postgres Password >
    export DB_NAME=< Your Postgres Database name >
    export BASE_URL=http://127.0.0.1:5000/
    export GOOGLE_API_KEY=< Your Google Api Key >
    export QUERY_PARAM=< Any QueryString to Search Youtube >
    export PER_PAGE=< Number of Result Per Page >
  ```

- #### Step 5

  To Initiate Database

  ```bash
  python manage.py initdb

  ```

- #### Step 6
  running the server
  ```bash
    python server.py
  ```

## API

The Api end points are `'/v1/'`

### For api documentations

  ```bash
    cd docs && npx serve
  ```
