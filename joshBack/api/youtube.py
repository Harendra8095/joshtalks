from logging import exception
import threading
from flask import Blueprint
import requests
import time
import os
import httpx
from datetime import datetime

from joshBack.models import VideoMeta

youtubeBP = Blueprint("youtubeApi", __name__)

BASE_URL = os.environ.get("BASE_URL")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
QUERY = os.environ.get("QUERY_PARAM")
NEXT_PAGE = "CB4QAA"


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
                time.sleep(3)

    thread = threading.Thread(target=fetch_videos)
    thread.start()


# function converted to coroutine
async def get_videos():
    # async client used for async functions
    async with httpx.AsyncClient() as session:
        url = "https://youtube.googleapis.com/youtube/v3/search?part=snippet&q={}&key={}".format(
            QUERY, GOOGLE_API_KEY
        )
        if NEXT_PAGE != "":
            url = url + "&pageToken={}".format(NEXT_PAGE)
        print(url)
        # dont wait for the response of API
        res = await session.get(url)
        result = res.json()
        # Storing result of youtube api to the database
        from server import SQLSession

        session = SQLSession()
        connection = session.connection()
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
            session.add(vmeta)
        try:
            session.commit()
            session.close()
            connection.close()
        except Exception as e:
            print("DB Error: ", e)
            session.close()
            connection.close()
    return result


@youtubeBP.get("/")
async def hello():
    res = await get_videos()
    try:
        NEXT_PAGE = res["nextPageToken"]
    except:
        pass
    return res
