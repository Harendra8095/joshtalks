from flask import Blueprint, request
from joshBack.models import VideoMeta
from joshBack.utils.paginate import paginate_query
from joshBack.response.response import make_response
from joshBack.response.statusCodes import HTTPStatus
from sqlalchemy import func, or_

homeBP = Blueprint("homeApi", __name__)


@homeBP.route("/home", methods=["GET"])
def home():
    try:
        page = request.args.get("page", 1, type=int)
    except:
        return make_response("Page argument not found", HTTPStatus.BadRequest)
    from server import SQLSession

    session = SQLSession()
    connection = session.connection()
    query = session.query(VideoMeta).order_by(VideoMeta.publish_datetime.desc())
    video_query = paginate_query(query, page=page)
    resp = []
    for video in video_query.items:
        video_meta = {
            "id": video.id,
            "title": video.title,
            "description": video.description,
            "publish_datetime": video.publish_datetime,
            "default_url": video.default_url,
            "medium_url": video.medium_url,
            "high_url": video.high_url,
            "channeltitle": video.channeltitle,
        }
        resp.append(video_meta)
    session.close()
    connection.close()
    return make_response("Success", HTTPStatus.Success, resp)


@homeBP.route("/search", methods=["GET"])
def search():
    try:
        q = request.args.get("q", type=str)
    except:
        return make_response("Query Parameter (q) is missing.", HTTPStatus.BadRequest)
    from server import SQLSession

    session = SQLSession()
    connection = session.connection()
    query = session.query(VideoMeta).filter(
        or_(
            VideoMeta.title_tsvector.op("@@")(func.to_tsquery(q)),
            VideoMeta.description_tsvector.op("@@")(func.to_tsquery(q)),
        )
    )
    resp = []
    page = request.args.get("page", 1, type=int)
    video_query = paginate_query(query, page=page)
    for video in video_query.items:
        video_meta = {
            "id": video.id,
            "title": video.title,
            "description": video.description,
            "publish_datetime": video.publish_datetime,
            "default_url": video.default_url,
            "medium_url": video.medium_url,
            "high_url": video.high_url,
            "channeltitle": video.channeltitle,
        }
        resp.append(video_meta)
    session.close()
    connection.close()
    return make_response("Success", HTTPStatus.Success, resp)
