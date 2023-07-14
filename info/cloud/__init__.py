from flask import Blueprint

cloud_blue = Blueprint('cloud',__name__)

from ..cloud import cloud_views