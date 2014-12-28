import os
from flask import g
from psycopg2.extras import DictCursor

from .sessionitem import SessionItem


class PsycopgService(object):
    def __init__(self, core_session, flask_app):
        self.env_name = 'FLASK_SESSION_FACTORY_PSYCOPG_SERVICE_TABLE_EXIST'
        if os.environ.get(self.env_name) is not None:
            return

        conn = flask_app.app_ctx_globals_class.pool.getconn()
        conn.autocommit = True
        try:
            with conn.cursor() as curs:
                curs.execute('''create table if not exists gp_session (
                sid varchar(256),
                time timestamp not null default (now() at time zone 'utc'),
                key text,
                value text)''')
        except Exception as e:
            flask_app.logger.error(e)
        finally:
            flask_app.app_ctx_globals_class.pool.putconn(conn)
        os.environ[self.env_name] = '1'

    def save(self, session):
        item_list = []
        for key, value in dict(session).items():
            item_list.append(dict(sid=session.sid, key=key, val=value))

        conn = g.pool.getconn()
        try:
            cur = conn.cursor()
            cur.execute('DELETE FROM gp_session WHERE sid = %(sid)s::varchar', dict(sid=session.sid))
            if item_list:
                cur.executemany(
                    'INSERT INTO gp_session (sid, key, value) VALUES (%(sid)s::varchar, %(key)s::text, %(val)s::text)',
                    item_list)
            conn.commit()
            cur.close()
        finally:
            g.pool.putconn(conn)

    def get(self, sid):
        conn = g.pool.getconn()
        try:
            cur = conn.cursor(cursor_factory=DictCursor)
            cur.execute('SELECT * FROM gp_session WHERE sid = %(sid)s::varchar', dict(sid=sid))
            query_result = cur.fetchall()
            cur.close()

            session = SessionItem(sid=sid)
            if query_result:
                for item in query_result:
                    session[item['key']] = item['value']
        finally:
            g.pool.putconn(conn)
        return session