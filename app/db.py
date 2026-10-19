"""Database utilities and simple migration (create tables) for MAGNTA.

This module uses SQLAlchemy to create a 'signals' table to persist ingested signals.
"""

import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Text

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./magnta_dev.db")

metadata = MetaData()

signals = Table(
    "signals",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("source", String(128), nullable=False),
    Column("timestamp", Float, nullable=False),
    Column("payload", Text, nullable=False),
)


def get_engine():
    return create_engine(DATABASE_URL)


def migrate():
    engine = get_engine()
    metadata.create_all(engine)
    print("Migration complete: tables created (if not existed)")


if __name__ == "__main__":
    migrate()
