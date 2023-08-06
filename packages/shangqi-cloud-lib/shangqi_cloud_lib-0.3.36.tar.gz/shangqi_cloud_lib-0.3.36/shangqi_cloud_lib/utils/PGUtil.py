import re

import psycopg2
from web_frame.utils.DBUtil import BaseSession

import logging
import traceback

from shangqi_cloud_lib.context import config


def postgis_connect(host=config.postgis_ip, user=config.postgis_user, port=config.postgis_port, db=config.postgis_db,
                    pwd=config.postgis_password):
    try:
        conn = psycopg2.connect(host=host, port=port, user=user, password=pwd, dbname=db)
        cursor = conn.cursor()
        return conn, cursor
    except Exception as e:
        logging.warning("连接数据库异常:" + traceback.format_exc())
        return "", str(e)


class PGSession(BaseSession):
    def __init__(self, host=config.postgis_ip, user=config.postgis_user, port=config.postgis_port, db=config.postgis_db,
                 pwd=config.postgis_password, auto_commit: bool = True):
        """
        :param host: str
        :param user: str
        :param port: int
        :param db: str
        :param pwd: str
        :param auto_commit: bool
        """
        super().__init__(auto_commit)
        self.conn, self.cursor = postgis_connect(host, user, port, db, pwd)
        self.protocol = "postgis"
        if self.conn == "":
            raise Exception(self.cursor)


pg_conn = dict(host="120.92.89.196", user="work", port=5454, pwd="ksPG@2021")

pattern = re.compile(r"[0-9]+\.[0-9]+,[0-9]+\.[0-9]+")


def is_valid_coord(coord):
    global pattern
    match = pattern.match(coord)
    if not match or len(coord) != match.span()[1] - match.span()[0]:
        return False
    return True


def clear_pg(table, db_name="cube"):
    with PGSession(db=db_name, **pg_conn) as pg_session:
        if isinstance(table, list):
            for t in table:
                sql = f"TRUNCATE TABLE {t} RESTART IDENTITY"
                pg_session.ori_execute(sql)
        elif isinstance(table, str):
            sql = f"TRUNCATE TABLE {table} RESTART IDENTITY"
            pg_session.ori_execute(sql)
