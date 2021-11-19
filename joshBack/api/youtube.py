import threading
from flask import Blueprint
from random import randint
import requests
import time
import os
import httpx
from datetime import datetime, timedelta

from joshBack.models import VideoMeta
from joshBack.response.response import make_response
from joshBack.response.statusCodes import HTTPStatus

youtubeBP = Blueprint("youtubeApi", __name__)

BASE_URL = os.environ.get("BASE_URL", "http://localhost:5000/")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
QUERY = os.environ.get("QUERY_PARAM", "cricket")


def run_background_job():
    def fetch_videos():
        from joshBack.api import API_VERSION_V1

        while True:
            try:
                r = requests.get("{}{}/youtube/".format(BASE_URL, API_VERSION_V1))
                if r.status_code == 200:
                    print("Server started, Called Youtube API")
                print(r.status_code)
            except:
                print("Server not yet started")
            finally:
                time.sleep(120)

    thread = threading.Thread(target=fetch_videos)
    thread.start()


# function converted to coroutine
async def get_videos(date):
    # async client used for async functions
    async with httpx.AsyncClient() as session:
        url = "https://youtube.googleapis.com/youtube/v3/search?part=snippet&order=date&q={}&type=video&publishedAfter={}&key={}".format(
            QUERY, date, GOOGLE_API_KEY
        )
        print(url)
        # dont wait for the response of API
        res = await session.get(url)
        result = res.json()
        # Storing result of youtube api to the database
        try:
            for video in result["items"]:
                vmeta = VideoMeta(
                    title=video["snippet"]["title"],
                    description=video["snippet"]["description"],
                    publish_datetime=datetime.fromisoformat(
                        video["snippet"]["publishTime"][:-1]
                    ),
                    default_url=video["snippet"]["thumbnails"]["default"]["url"],
                    medium_url=video["snippet"]["thumbnails"]["medium"]["url"],
                    high_url=video["snippet"]["thumbnails"]["high"]["url"],
                    channeltitle=video["snippet"]["channelTitle"],
                )
                from server import SQLSession

                session = SQLSession()
                connection = session.connection()
                session.add(vmeta)
                try:
                    session.commit()
                    session.close()
                    connection.close()
                except Exception as e:
                    print(
                        "DB Error:", e, "\nDuplicate Video:", video["snippet"]["title"]
                    )
                    session.rollback()
                    session.close()
                    connection.close()
        except Exception as e:
            print("Error from Youtube api", e)
    return result


@youtubeBP.get("/")
async def hello():
    delta = randint(1, 10)
    date = ((datetime.utcnow() - timedelta(delta)).isoformat()) + "Z"
    res = await get_videos(date)
    return make_response("Success", HTTPStatus.Success, res)
