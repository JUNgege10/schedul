from flask import Blueprint

db_blue = Blueprint('db',__name__)

from ..dbs import dbs_views