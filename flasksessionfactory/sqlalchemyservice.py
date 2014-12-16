from sqlalchemy import Column, String, DateTime, PrimaryKeyConstraint, func, Text

from .sessionitem import SessionItem


class SqlAlchemyService(object):
    def __init__(self, core_session):
        self.core_session = core_session
        self.model_class = None

    def get_model(self):
        if not self.model_class:
            # class SqlAlchemySession(self.core_session.db.Model):
            # __tablename__ = 'el_session'
            # sid = Column('sid', String(200))
            # date = Column('date', DateTime, default=func.now())
            # key = Column('key', Text)
            #     val = Column('value', Text)
            #     __table_args__ = (PrimaryKeyConstraint(sid, key), {'useexisting': True})
            #self.model_class = SqlAlchemySession
            from . import FlaskSessionFabric

            table_name = self.core_session.app.config[FlaskSessionFabric.OWN_GROUP_KEY][FlaskSessionFabric.TABLE_NAME]
            self.model_class = type('SqlAlchemySession', (self.core_session.db.Model,),
                                    {
                                        '__tablename__': table_name,
                                        'sid': Column('sid', String(200)),
                                        'date': Column('date', DateTime, default=func.now()),
                                        'key': Column('key', Text),
                                        'val': Column('value', Text),
                                        '__table_args__': (PrimaryKeyConstraint('sid', 'key'), {'useexisting': True}),
                                    })
            #self.model_class.create(self.core_session.db.engine, checkfirst=True)
        return self.model_class

    def save(self, session):
        model_class = self.get_model()
        model_class.query.filter_by(sid=session.sid).delete()
        for key, value in dict(session).items():
            item = model_class()
            item.sid = session.sid
            item.key = key
            item.val = value
            self.core_session.db.session.add(item)
        self.core_session.db.session.flush()

    def get(self, sid):
        model_class = self.get_model()
        from . import FlaskSessionFabric

        if self.core_session.app.config[FlaskSessionFabric.OWN_GROUP_KEY][FlaskSessionFabric.CREATE_DB]:
            self.core_session.db.create_all()
            self.core_session.db.session.flush()
        query_result = model_class.query.filter_by(sid=sid).all()
        session = SessionItem(sid=sid)
        for item in query_result:
            session[item.key] = item.val
        return session