from .coresession import CoreSession
from .cookiesession import CookieSession
from .cookielesssession import CookielessSession
from .sqlalchemyservice import SqlAlchemyService
import importlib
import os, sys, inspect


class FlaskSessionFabric(object):
    OWN_GROUP_KEY = 'FLASK_SESSION_FABRIC'
    SESSION_INTERFACE = 'SESSION_INTERFACE'
    SERVICE_PROVIDER = 'SERVICE_PROVIDER'
    PARAM_NAME_COOKIE_LESS = 'PARAM_NAME_COOKIE_LESS'
    CREATE_DB = 'CREATE_DB'
    TABLE_NAME = 'TABLE_NAME'

    @staticmethod
    def get_class(class_name):
        cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
        if cmd_folder not in sys.path:
            sys.path.insert(0, cmd_folder)

        # use this if you want to include modules from a subfolder
        cmd_subfolder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
        if cmd_subfolder not in sys.path:
            sys.path.insert(0, cmd_subfolder)

        module = __import__('.'+class_name.lower())
        return getattr(module, class_name)

    @staticmethod
    def get(app, db):
        session_interface_class = FlaskSessionFabric.get_class(app.config[FlaskSessionFabric.OWN_GROUP_KEY][FlaskSessionFabric.SESSION_INTERFACE])
        service_provider_class = FlaskSessionFabric.get_class(app.config[FlaskSessionFabric.OWN_GROUP_KEY][FlaskSessionFabric.SERVICE_PROVIDER])
        result = session_interface_class(app, db)
        result.session_service = service_provider_class(result)
        return result
        #
        # mode = app.config[CoreSession.OWN_GROUP_KEY][CoreSession.MODE]
        # if mode == CoreSession.MODE_COOKIE:
        #     return CookieSession(app, db)
        # elif mode == CoreSession.MODE_COOKIE_LESS:
        #     session = CookielessSession(app, db)
        #     session.session_service = SqlAlchemyService(session)
        #     return session
        # else:
        #     raise NotImplementedError()
