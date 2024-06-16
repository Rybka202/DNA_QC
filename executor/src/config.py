from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

S3_HOST=os.environ.get("S3_HOST")
S3_PORT=os.environ.get("S3_PORT")
S3_NAME=os.environ.get("S3_NAME")
S3_PASS=os.environ.get("S3_PASS")