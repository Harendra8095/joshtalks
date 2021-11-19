from flask_sqlalchemy import BaseQuery
import os

PER_PAGE = int(os.environ.get("PER_PAGE"))


def paginate_query(sa_query, page, per_page=PER_PAGE, error_out=True):
    sa_query.__class__ = BaseQuery
    return sa_query.paginate(page, per_page, error_out)
