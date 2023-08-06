import typing
import flask
from . import db


def noop_authentication_function(action, parameters) -> typing.Optional[flask.Response]:
    return None


editor_paths = ['editor', 'upload_image', 'delete_image', 'list_images']
viewer_paths = ['page', 'get_image']

db_connection: typing.Optional[db.DatabaseProvider] = None
template_name = 'cms/example_templates/page.html'
upload_folder = 'media/cms'
authentication_function = noop_authentication_function
