from flask import redirect, url_for, request, session

from .coresession import CoreSession


class CookielessSession(CoreSession):
    def init(self):
        from . import FlaskSessionFabric
        self.param_name = self.app.config[FlaskSessionFabric.OWN_GROUP_KEY][FlaskSessionFabric.PARAM_NAME_COOKIE_LESS]
        self.app.template_context_processors[None].append(self.override_url_for)
        self.app.before_request_funcs.setdefault(None, []).append(self.before_request)

    def before_request(self):
        if '/'+request.endpoint == self.app.static_url_path:
            return
        if self.param_name not in request.args:
            values = request.args.to_dict()
            values[self.param_name] = session.sid
            return redirect(url_for(request.endpoint, **values), code=307)

    def cookie_less_url_for(self, endpoint, **values):
        if self.param_name not in values:
            values[self.param_name] = session.sid
        return url_for(endpoint, **values)

    def override_url_for(self):
        return dict(url_for=self.cookie_less_url_for)

    def get_sid(self, app, request):
        sid = None
        if self.param_name in request.args:
            sid = request.args[self.param_name]
            if not sid:
                if self.param_name in request.form:
                    sid = request.form[self.param_name]
        return sid