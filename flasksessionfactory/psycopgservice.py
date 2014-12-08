from flask import g
from psycopg2.extras import DictCursor

from .sessionitem import SessionItem


class PsycopgService(object):
    def __init__(self, core_session):
        None

    def save(self, session):
        item_list = []
        for key, value in dict(session).items():
            item_list.append(dict(sid=session.sid, key=key, val=value))

        conn = g.conn
        cur = conn.cursor()
        cur.execute('DELETE FROM gp_session WHERE sid = %(sid)s::varchar', dict(sid=session.sid))
        if item_list:
            cur.executemany(
                'INSERT INTO gp_session (sid, key, value) VALUES (%(sid)s::varchar, %(key)s::text, %(val)s::text)',
                item_list)
        conn.commit()
        cur.close()

    def get(self, sid):
        conn = g.conn
        cur = conn.cursor(cursor_factory=DictCursor)
        query_result = cur.execute('SELECT * FROM gp_session WHERE sid = %(sid)s::varchar', dict(sid=sid))
        cur.close()

        session = SessionItem(sid=sid)
        if query_result:
            for item in query_result:
                session[item.key] = item.val
        return session