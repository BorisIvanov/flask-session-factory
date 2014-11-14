class FlaskSessionFabric(object):
    OWN_GROUP_KEY = 'FLASK_SESSION_FABRIC'
    SESSION_INTERFACE = 'SESSION_INTERFACE'
    SERVICE_PROVIDER = 'SERVICE_PROVIDER'
    PARAM_NAME_COOKIE_LESS = 'PARAM_NAME_COOKIE_LESS'
    CREATE_DB = 'CREATE_DB'
    TABLE_NAME = 'TABLE_NAME'

    @staticmethod
    def get_class(class_name):
        module = __import__('flasksessionfactory.' + class_name.lower(), fromlist=[class_name.lower()])
        return getattr(module, class_name)

    @staticmethod
    def get(app, db):
        session_interface_class = FlaskSessionFabric.get_class(
            app.config[FlaskSessionFabric.OWN_GROUP_KEY][FlaskSessionFabric.SESSION_INTERFACE])
        service_provider_class = FlaskSessionFabric.get_class(
            app.config[FlaskSessionFabric.OWN_GROUP_KEY][FlaskSessionFabric.SERVICE_PROVIDER])
        result = session_interface_class(app, db)
        result.session_service = service_provider_class(result)
        return result