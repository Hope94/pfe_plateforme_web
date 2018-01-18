import os
import sqlite3
from pfe_plateforme_web.settings import DATABASES

DETECTION_DB_PATH = DATABASES['detection_db']['NAME']


_SQL_create_parameter = """ CREATE TABLE IF NOT EXISTS parameter(
                                                    intercept real,
                                                    threshold real,
                                                    sumMalignantFeatures real,
                                                    sumBenignFeatures real
                                                    );"""

_SQL_insert_parameter = """ INSERT INTO parameter(intercept, threshold,sumMalignantFeatures,sumBenignFeatures)
                           VALUES (:intercept,:threshold, :sumMalignantFeatures, :sumBenignFeatures)"""

_SQL_get_all_parameter= """SELECT intercept,threshold,sumMalignantFeatures,sumBenignFeatures 
                          FROM parameter 
                          ORDER BY rowid DESC"""

_SQL_get_intercept = """SELECT intercept FROM parameter WHERE rowid = :id"""
_SQL_get_threshold = """SELECT threshold FROM parameter WHERE rowid = :id"""
_SQL_get_sumMalignantFeatures = """SELECT sumMalignantFeatures FROM parameter WHERE rowid = :id"""
_SQL_get_sumBenignFeatures = """SELECT sumBenignFeatures FROM parameter WHERE rowid = :id"""

_SQL_get_features_weight = """ SELECT feature,weight FROM feature_weight_mapping WHERE feature IN (%s)"""

class OpenReaderCursor:
    def __init__(self, sql: str, args=()):
        self._SQL = sql
        self.args = args

    def __enter__(self) -> 'cursor':
            self.conn = sqlite3.connect(DETECTION_DB_PATH)
            self.cursor = self.conn.cursor()
            self.cursor.execute(self._SQL, self.args)
            return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.cursor.close()
        self.conn.close()


class OpenWriterCursor(OpenReaderCursor):
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close()


class OpenMultiWriterCursor(OpenWriterCursor):
    def __enter__(self) -> 'cursor':
            self.conn = sqlite3.connect(DETECTION_DB_PATH)
            self.cursor = self.conn.cursor()
            self.cursor.executemany(self._SQL, self.args)
            return self.cursor


def insert_parameter(intercept,threshold,sumMalignantFeatures, sumBenignFeatures)->int:
    with OpenWriterCursor(_SQL_insert_parameter,{
                                            'intercept': intercept,
                                            'threshold': threshold,
                                            'sumMalignantFeatures': sumMalignantFeatures,
                                            'sumBenignFeatures': sumBenignFeatures})as cursor:
        return cursor.lastrowid


def get_all_paramatere() -> dict:
    with OpenReaderCursor(_SQL_get_all_parameter) as cursor:
        row = cursor.fetchone()
        if row != ():
            return  {'intercept':row[0],
                     'threshold': row[1],
                     'sumMalignantFeatures': row[2],
                     'sumBenignFeatures': row[3]}
        else:
          return {}



def get_features_weight(list_features: list) -> dict:
    sql_request = _SQL_get_features_weight % ('?,' * len(list_features))[:-1]
    with OpenReaderCursor(sql_request, list_features) as cursor:
         return {row[0]:row[1] for row in cursor.fetchall() }
