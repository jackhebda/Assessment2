from __future__ import absolute_import

import abc
import asyncio
import logging
import csv
from functools import wraps
from typing import Type

import sqlalchemy
from sqlalchemy import *
from databases import Database
from starlette.requests import Request

metadata = sqlalchemy.MetaData()


def get_db(request: Request):
    engine = create_engine(DB_DSN, echo = False)
    conn = engine.connect()

    with open('/app/data/zipcodes.csv', newline='') as f:
            zipcode_dict = {}
            reader = csv.reader(f)
            for row in reader:
                if len(row[0]) == 4:
                    zipcode_dict[int(row[0])] = row[1]
                else:
                    for zip in range(int(row[0][:4]), int(row[0][7:]) + 1):
                        zipcode_dict[zip] = row[1]

    metadata = MetaData()

    riskfactor = Table('riskfactor', metadata,
        Column('zipcode', Integer, primary_key=True),
        Column('risk_factor', String))                
                    
    metadata.create_all(engine)

    for k, v in zipcode_dict.items():
        conn.execute(insert(riskfactor).values(zipcode = k, risk_factor = v))
    return request.app.db.db


def db_semaphore(func):
    @wraps(func)
    async def wrapped(request, *args, **kwargs):
        async with request.app.db.semaphore:
            return await func(request, *args, **kwargs)

    return wrapped


def db_transaction(func):
    @wraps(func)
    async def wrapped(request, *args, **kwargs):
        async with request.app.db.db.conn.transaction():
            async with request.app.db.semaphore:
                return await func(request, *args, **kwargs)

    return wrapped


class AbstractDB(abc.ABC):
    db: Type[Database]
    dsn: str
    testing: bool = False

    def __init__(self) -> None:
        self.conn = None

    @abc.abstractmethod
    async def setup(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def teardown(self) -> None:
        raise NotImplementedError()


class DB(AbstractDB):
    def __init__(self, dsn) -> None:
        self.conn: Type[Database] = None
        self.dsn: str = dsn
        self.testing: bool = False
        self.connected: bool = False

    async def setup(self, app) -> None:
        self.semaphore = asyncio.Semaphore(500)
        try:
            self.conn = Database(self.dsn, min_size=3, max_size=6)
            await self.conn.connect()
            # test connection
            await self.conn.execute("SELECT now()")
            self.connected = True
        except Exception as e:
            logging.warning(f"[DB_SETUP] FAILED - {e}")

    async def teardown(self) -> None:
        if self.db.conn.is_connected:
            logging.info("DISCONNECTING DB CONNECTION")
            await self.db.conn.disconnect()
