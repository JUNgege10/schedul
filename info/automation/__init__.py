from flask import Blueprint

automation_blue = Blueprint('automation',__name__)

from ..automation import automation_views