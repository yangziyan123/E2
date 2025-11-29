from flask import Flask, Blueprint

admin_bp = Blueprint('admin', __name__)

from . import views