import typing
import flask
from . import db


def noop_authentication_function(action, parameters) -> typing.Optional[flask.Response]:
    return None


db_connection: typing.Optional[db.DatabaseProvider] = None
template_name = 'page.html'
upload_folder = 'media/cms'
authentication_function = noop_authentication_function
