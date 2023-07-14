from flask import Blueprint

role_blue = Blueprint('role',__name__)

from ..roles import roles_views