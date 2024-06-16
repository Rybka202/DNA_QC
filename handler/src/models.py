from datetime import datetime

from sqlalchemy import MetaData, Table, Column, String, Integer, ForeignKey, TIMESTAMP


metadata = MetaData()

file = Table(
    "file",
    metadata,
    Column("id", String, primary_key=True),
    Column("fileName", String, nullable=False),
    Column("analyze_id", String, nullable=False),
    Column("time", TIMESTAMP, default=datetime.utcnow),
    Column("stage", Integer, ForeignKey("stage.id")),
)

stage = Table(
    "stage",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("stepOfDevelopment", String),
)