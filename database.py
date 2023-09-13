import sqlalchemy
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.util import deprecations

load_dotenv()

deprecations.SILENCE_UBER_WARNING = 1

db_username = os.environ["DB_USERNAME"]
db_password = os.environ["DB_PASSWORD"]

DB_CONNECTION_STRING = f"mysql+pymysql://{db_username}:{db_password}@aws.connect.psdb.cloud/flaskcareers?charset=utf8mb4"

engine = create_engine(
    DB_CONNECTION_STRING,
    connect_args={
        "ssl": {
            "ssl_ca": "/etc/ssl/cert.pem",
        }
    },
)


def load_jobs_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from jobs"))

        jobs = []
        for row in result.all():
            jobs.append(dict(row))

        return jobs


def load_job_from_db(id):
    with engine.connect() as conn:
        result = conn.execute(text("select * from jobs where id = :val"), val=id)

        row = result.all()
        if len(row) == 0:
            return None

        return dict(row[0])


def add_application_to_db(job_id, data):
    with engine.connect() as conn:
        query = text(
            """INSERT INTO applications 
                (job_id, full_name, email, linkedin_url, education, work_experience, resume_url) 
                VALUES (:job_id, :full_name, :email, :linkedin_url, :education, :work_experience, :resume_url)"""
        )
        conn.execute(
            query,
            job_id=job_id,
            full_name=data["full_name"],
            email=data["email"],
            linkedin_url=data["linkedin_url"],
            education=data["education"],
            work_experience=data["work_experience"],
            resume_url=data["resume_url"],
        )
