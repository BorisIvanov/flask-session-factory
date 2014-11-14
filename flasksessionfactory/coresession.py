from uuid import uuid4

from flask.sessions import SessionInterface


class CoreSession(SessionInterface):
    def __init__(self, app, db):
        self.app = app
        self.db = db
        self.init()
        self.session_service = None

    def init(self, app):
        pass

    def get_sid(self, app, request):
        pass

    def open_session(self, app, request):
        sid = self.get_sid(app, request)
        if not sid:
            sid = str(uuid4())
        return self.session_service.get(sid)

    def save_session(self, app, session, response):
        self.session_service.save(session)